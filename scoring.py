"""
Scoring engine for Best Regard Challenge 2026.

Scoring rules:
  Yes/No   — Correct: 2 pts, Incorrect: 0
  Multi    — Exact: 4 pts, Close: 1 pt, Incorrect: 0
  Wildcard — 1st: 5 pts, 2nd: 3 pts, 3rd: 0
             Tied 1st (2-way): 4 each, Tied last (2-way): 2 each
             3-way tie: 4 each

Confidence tokens  → double points when result is positive (any > 0)
Anti-dogpile rule  → Friend Life Events only; if all 3 pick the same, cap at 1 pt
                     Confidence tokens do NOT override the cap.
"""

PLAYERS = ["Arnav", "Sibi", "Nikhil"]

PLAYER_COLORS = {
    "Arnav": "#3B82F6",
    "Sibi": "#8B5CF6",
    "Nikhil": "#10B981",
}

PLAYER_EMOJIS = {
    "Arnav": "\U0001f9d1\u200d\U0001f4bb",   # technologist
    "Sibi": "\U0001f9d1\u200d\U0001f680",     # astronaut
    "Nikhil": "\U0001f9d1\u200d\U0001f3a8",   # artist
}

CATEGORY_COLORS = {
    "Sports & Entertainment": {"bg": "rgba(59,130,246,0.15)", "fg": "#60a5fa"},
    "World/Public Events": {"bg": "rgba(245,158,11,0.15)", "fg": "#fbbf24"},
    "Friend Life Events": {"bg": "rgba(236,72,153,0.15)", "fg": "#f472b6"},
    "Wildcard": {"bg": "rgba(139,92,246,0.15)", "fg": "#a78bfa"},
}

CATEGORIES = list(CATEGORY_COLORS.keys())


# ── helpers ──────────────────────────────────────────────────────────────

def _base_points(pred_type: str, result: str) -> int:
    """Return raw points before tokens / anti-dogpile."""
    if pred_type == "yes_no":
        return 2 if result == "correct" else 0
    elif pred_type == "multi_outcome":
        if result == "exact":
            return 4
        elif result == "close":
            return 1
        return 0
    elif pred_type == "wildcard_competition":
        return {
            "first": 5,
            "second": 3,
            "third": 0,
            "tied_first": 4,   # 2-way or 3-way tie for 1st
            "tied_second": 2,  # 2-way tie for last
        }.get(result, 0)
    return 0


def prediction_is_all_same(pred: dict) -> bool:
    """True when every player made the same pick (ignoring blanks)."""
    picks = []
    for p in PLAYERS:
        v = pred.get("picks", {}).get(p, "").strip().upper()
        if v and v != "N/A":
            picks.append(v)
    return len(set(picks)) == 1 and len(picks) == len(PLAYERS)


# ── per-prediction scoring ───────────────────────────────────────────────

def score_prediction(pred: dict, outcome: dict) -> dict:
    """
    Score one finalized prediction.

    Returns {player: {"points": int, "base": int, "token_applied": bool,
                       "anti_dogpile": bool, "result": str}}
    """
    pred_type = pred["type"]
    tokens = pred.get("tokens", {})
    anti_dogpile = pred.get("anti_dogpile", False)
    all_same = prediction_is_all_same(pred)

    scores = {}
    for player in PLAYERS:
        result = outcome.get("results", {}).get(player, "incorrect")
        base = _base_points(pred_type, result)

        token_applied = False
        if tokens.get(player) and base > 0:
            base *= 2
            token_applied = True

        dogpile_hit = False
        if anti_dogpile and all_same and base > 0:
            base = 1
            dogpile_hit = True

        scores[player] = {
            "points": base,
            "base": _base_points(pred_type, result),
            "token_applied": token_applied,
            "anti_dogpile": dogpile_hit,
            "result": result,
        }
    return scores


# ── aggregate scoring ────────────────────────────────────────────────────

def calculate_all_scores(predictions: list, outcomes: dict,
                         books: list = None, flights: list = None) -> dict:
    """
    Return a dict keyed by player with totals and per-prediction detail.

    Structure per player:
        total, correct_count, exact_count, close_count, incorrect_count,
        token_bonus, details (list), breakdown_by_category
    """
    result = {}
    for player in PLAYERS:
        result[player] = {
            "total": 0,
            "correct_count": 0,
            "exact_count": 0,
            "close_count": 0,
            "incorrect_count": 0,
            "token_bonus": 0,
            "details": [],
            "breakdown": {},
        }

    for pred in predictions:
        idx = str(pred["index"])
        cat = pred["category"]
        if idx not in outcomes:
            continue
        outcome = outcomes[idx]
        if outcome.get("status") != "finalized":
            continue

        pred_scores = score_prediction(pred, outcome)
        for player in PLAYERS:
            ps = pred_scores[player]
            result[player]["total"] += ps["points"]
            result[player]["details"].append({
                "index": pred["index"],
                "category": cat,
                "points": ps["points"],
                "result": ps["result"],
                "token_applied": ps["token_applied"],
                "anti_dogpile": ps["anti_dogpile"],
                "finalized_date": outcome.get("finalized_date", ""),
            })

            # Counters
            r = ps["result"]
            if r in ("correct", "exact", "first", "tied_first"):
                result[player]["correct_count"] += 1
            if r == "exact":
                result[player]["exact_count"] += 1
            if r == "close":
                result[player]["close_count"] += 1
            if r in ("incorrect", "third"):
                result[player]["incorrect_count"] += 1
            if ps["token_applied"]:
                result[player]["token_bonus"] += (
                    ps["points"] - ps["base"]
                )

            # Category breakdown
            if cat not in result[player]["breakdown"]:
                result[player]["breakdown"][cat] = 0
            result[player]["breakdown"][cat] += ps["points"]

    return result


# ── wildcard helpers ─────────────────────────────────────────────────────

def rank_wildcard(counts: dict) -> dict:
    """
    Given {player: count}, return {player: "first"/"second"/"third"/tied_*}.
    Tie rules:
      - 2-way tie for 1st  → both "tied_first" (+4), 3rd gets "third" (0)
      - 2-way tie for last → "tied_second" (+2 each), 1st keeps "first" (+5)
      - 3-way tie          → all "tied_first" (+4)
    """
    sorted_players = sorted(PLAYERS, key=lambda p: counts.get(p, 0), reverse=True)
    vals = [counts.get(p, 0) for p in sorted_players]

    # 3-way tie
    if vals[0] == vals[1] == vals[2]:
        return {p: "tied_first" for p in PLAYERS}

    # 2-way tie for 1st
    if vals[0] == vals[1] and vals[1] != vals[2]:
        rankings = {}
        for p in sorted_players[:2]:
            rankings[p] = "tied_first"
        rankings[sorted_players[2]] = "third"
        return rankings

    # 2-way tie for last
    if vals[1] == vals[2] and vals[0] != vals[1]:
        rankings = {sorted_players[0]: "first"}
        for p in sorted_players[1:]:
            rankings[p] = "tied_second"
        return rankings

    # No ties
    return {
        sorted_players[0]: "first",
        sorted_players[1]: "second",
        sorted_players[2]: "third",
    }


def get_book_counts(books: list) -> dict:
    """Return {player: num_books}."""
    counts = {p: 0 for p in PLAYERS}
    for b in (books or []):
        person = b.get("person", "")
        if person in counts:
            counts[person] += 1
    return counts


def get_flight_counts(flights: list) -> dict:
    """Return {player: num_flights}."""
    counts = {p: 0 for p in PLAYERS}
    for f in (flights or []):
        person = f.get("person", "")
        if person in counts:
            counts[person] += 1
    return counts


# ── timeline ─────────────────────────────────────────────────────────────

def get_score_timeline(predictions: list, outcomes: dict) -> list:
    """
    Build a list of {date, Arnav, Sibi, Nikhil} rows for the cumulative
    score over time, ordered by finalized_date.
    """
    events = []
    pred_map = {p["index"]: p for p in predictions}

    for idx_str, outcome in outcomes.items():
        if outcome.get("status") != "finalized":
            continue
        idx = int(idx_str)
        pred = pred_map.get(idx)
        if not pred:
            continue
        pred_scores = score_prediction(pred, outcome)
        events.append({
            "date": outcome.get("finalized_date", "2026-01-01"),
            "prediction": pred["prediction"],
            "index": idx,
            "scores": {p: pred_scores[p]["points"] for p in PLAYERS},
        })

    events.sort(key=lambda e: e["date"])

    # Build cumulative
    running = {p: 0 for p in PLAYERS}
    timeline = []
    for ev in events:
        for p in PLAYERS:
            running[p] += ev["scores"][p]
        timeline.append({
            "date": ev["date"],
            "label": f"Q{ev['index']}: {ev['prediction'][:40]}",
            **{p: running[p] for p in PLAYERS},
        })

    return timeline


# ── auto-result helpers ──────────────────────────────────────────────────

def auto_results_yes_no(pred: dict, actual: str) -> dict:
    """For a yes/no prediction, return {player: 'correct'/'incorrect'}."""
    actual_upper = actual.strip().upper()
    results = {}
    for player in PLAYERS:
        pick = pred["picks"][player].strip().upper()
        results[player] = "correct" if pick == actual_upper else "incorrect"
    return results
