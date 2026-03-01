"""
📋 Predictions — Browse, filter, and finalize prediction outcomes.
"""

import streamlit as st
from datetime import date

from data_manager import load_data, save_data, invalidate_cache
from scoring import (
    PLAYERS, PLAYER_COLORS, CATEGORIES, CATEGORY_COLORS,
    score_prediction, auto_results_yes_no, prediction_is_all_same,
    rank_wildcard, get_book_counts, get_flight_counts,
)

st.set_page_config(page_title="Predictions | BR2026", page_icon="📋", layout="wide")

# ─── CSS ─────────────────────────────────────────────────────────────────
st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
.pcard{background:linear-gradient(165deg,#1e293b,#0f172a);border-radius:14px;
  padding:1.1rem 1.3rem;margin:.5rem 0;border-left:5px solid #4b5563;transition:border-color .3s}
.pcard.fin{border-left-color:#10B981;background:linear-gradient(165deg,rgba(16,185,129,.06),#0f172a)}
.pcard .pq{font-size:1rem;font-weight:700;color:#e2e8f0;margin-bottom:.35rem}
.pcard .pmeta{display:flex;gap:.6rem;flex-wrap:wrap;align-items:center;margin-bottom:.4rem}
.cat{display:inline-block;padding:2px 9px;border-radius:16px;font-size:.7rem;font-weight:600}
.tok{display:inline-block;background:linear-gradient(135deg,#f59e0b,#d97706);
  color:#000;padding:1px 7px;border-radius:10px;font-size:.65rem;font-weight:800}
.adp{display:inline-block;background:rgba(239,68,68,.12);color:#f87171;
  padding:1px 7px;border-radius:10px;font-size:.65rem;font-weight:700}
.pick-row{display:flex;gap:.8rem;flex-wrap:wrap;margin:.3rem 0}
.pick{padding:4px 10px;border-radius:8px;font-size:.82rem;font-weight:600;
  background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.08)}
.pick.correct{background:rgba(16,185,129,.12);border-color:rgba(16,185,129,.3);color:#34d399}
.pick.incorrect{background:rgba(239,68,68,.08);border-color:rgba(239,68,68,.2);color:#f87171}
.pick.close-r{background:rgba(251,191,36,.10);border-color:rgba(251,191,36,.25);color:#fbbf24}
.outcome-box{background:rgba(16,185,129,.08);border:1px solid rgba(16,185,129,.2);
  border-radius:10px;padding:.6rem .9rem;margin-top:.4rem;font-size:.88rem}
.pts{font-weight:800}
</style>""", unsafe_allow_html=True)

# ─── Sidebar ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("# 📋 Predictions")
    st.caption("Browse, filter & finalize")
    st.markdown("---")

    cat_filter = st.multiselect("Category", CATEGORIES, default=CATEGORIES)
    status_filter = st.radio("Status", ["All", "Pending", "Finalized"], horizontal=True)
    search = st.text_input("Search predictions", "")

# ─── Data ────────────────────────────────────────────────────────────────
predictions = load_data("predictions.json", [])
outcomes    = load_data("outcomes.json", {})
books       = load_data("books.json", [])
flights     = load_data("flights.json", [])

# ─── Filter ──────────────────────────────────────────────────────────────
filtered = []
for pred in predictions:
    idx_str = str(pred["index"])
    is_fin = idx_str in outcomes and outcomes[idx_str].get("status") == "finalized"

    if pred["category"] not in cat_filter:
        continue
    if status_filter == "Pending" and is_fin:
        continue
    if status_filter == "Finalized" and not is_fin:
        continue
    if search and search.lower() not in pred["prediction"].lower():
        continue
    filtered.append(pred)

st.markdown(f"### 📋 Predictions &nbsp; <span style='color:#64748b;font-size:.9rem'>"
            f"Showing {len(filtered)} of {len(predictions)}</span>",
            unsafe_allow_html=True)


# ─── Finalization logic (defined before use) ─────────────────────────────

def _finalize_prediction(pred, outcomes, books, flights):
    idx = pred["index"]
    idx_str = str(idx)
    p_type = pred["type"]

    with st.form(key=f"form_{idx}"):
        finalized_by = st.selectbox("Finalized by", PLAYERS, key=f"fb_{idx}")
        fin_date = st.date_input("Date", value=date.today(), key=f"fd_{idx}")

        if p_type == "yes_no":
            actual = st.radio("Actual outcome", ["Y", "N"],
                              horizontal=True, key=f"ao_{idx}")
            notes = st.text_input("Notes (optional)", key=f"n_{idx}")

            submitted = st.form_submit_button("✅ Finalize", type="primary",
                                              use_container_width=True)
            if submitted:
                results = auto_results_yes_no(pred, actual)
                outcome_obj = {
                    "status": "finalized",
                    "actual_outcome": actual,
                    "prediction_type": p_type,
                    "results": results,
                    "finalized_date": str(fin_date),
                    "finalized_by": finalized_by,
                    "notes": notes,
                }
                ps = score_prediction(pred, outcome_obj)
                st.markdown("**Score preview:**")
                for p in PLAYERS:
                    st.write(f"  {p}: {ps[p]['points']} pts "
                             f"({'🔥 token' if ps[p]['token_applied'] else ''}) "
                             f"({'🤝 anti-dogpile cap' if ps[p]['anti_dogpile'] else ''})")
                outcomes[idx_str] = outcome_obj
                save_data("outcomes.json", outcomes)
                invalidate_cache("outcomes.json")
                st.success(f"Q{idx} finalized!")
                st.rerun()

        elif p_type == "multi_outcome":
            actual = st.text_input("Actual winner / result", key=f"ao_{idx}")
            st.markdown("**Per-player results:**")
            player_results = {}
            for p in PLAYERS:
                pick = pred["picks"].get(p, "—")
                player_results[p] = st.selectbox(
                    f"{p} (picked **{pick}**)",
                    ["exact", "close", "incorrect"],
                    index=2,
                    key=f"pr_{idx}_{p}",
                )
            notes = st.text_input("Notes (optional)", key=f"n_{idx}")

            submitted = st.form_submit_button("✅ Finalize", type="primary",
                                              use_container_width=True)
            if submitted:
                outcome_obj = {
                    "status": "finalized",
                    "actual_outcome": actual,
                    "prediction_type": p_type,
                    "results": player_results,
                    "finalized_date": str(fin_date),
                    "finalized_by": finalized_by,
                    "notes": notes,
                }
                ps = score_prediction(pred, outcome_obj)
                st.markdown("**Score preview:**")
                for p in PLAYERS:
                    st.write(f"  {p}: {ps[p]['points']} pts")
                outcomes[idx_str] = outcome_obj
                save_data("outcomes.json", outcomes)
                invalidate_cache("outcomes.json")
                st.success(f"Q{idx} finalized!")
                st.rerun()

        elif p_type == "wildcard_competition":
            is_books = idx == 48
            if is_books:
                counts = get_book_counts(books)
                st.info(f"📚 Current book counts — "
                        f"Arnav: {counts['Arnav']}, Sibi: {counts['Sibi']}, Nikhil: {counts['Nikhil']}")
            else:
                counts = get_flight_counts(flights)
                st.info(f"✈️ Current flight counts — "
                        f"Arnav: {counts['Arnav']}, Sibi: {counts['Sibi']}, Nikhil: {counts['Nikhil']}")

            st.markdown("Override counts if needed:")
            override = {}
            for p in PLAYERS:
                override[p] = st.number_input(
                    f"{p} count", min_value=0, value=counts.get(p, 0), key=f"wc_{idx}_{p}"
                )

            notes = st.text_input("Notes (optional)", key=f"n_{idx}")
            submitted = st.form_submit_button("✅ Finalize", type="primary",
                                              use_container_width=True)
            if submitted:
                rankings = rank_wildcard(override)
                actual_str = ", ".join(f"{p}: {override[p]}" for p in PLAYERS)
                outcome_obj = {
                    "status": "finalized",
                    "actual_outcome": actual_str,
                    "prediction_type": p_type,
                    "results": rankings,
                    "counts": override,
                    "finalized_date": str(fin_date),
                    "finalized_by": finalized_by,
                    "notes": notes,
                }
                ps = score_prediction(pred, outcome_obj)
                st.markdown("**Score preview:**")
                for p in PLAYERS:
                    st.write(f"  {p} ({rankings[p]}): {ps[p]['points']} pts")
                outcomes[idx_str] = outcome_obj
                save_data("outcomes.json", outcomes)
                invalidate_cache("outcomes.json")
                st.success(f"Q{idx} finalized!")
                st.rerun()


# ─── Render predictions ─────────────────────────────────────────────────
for pred in filtered:
    idx = pred["index"]
    idx_str = str(idx)
    cat = pred["category"]
    p_type = pred["type"]
    tokens = pred.get("tokens", {})
    anti_dogpile = pred.get("anti_dogpile", False)
    all_same = prediction_is_all_same(pred)
    is_fin = idx_str in outcomes and outcomes[idx_str].get("status") == "finalized"

    cc = CATEGORY_COLORS.get(cat, {"bg": "#333", "fg": "#ccc"})
    cat_html = f'<span class="cat" style="background:{cc["bg"]};color:{cc["fg"]}">{cat}</span>'
    tok_html = ""
    for tp in PLAYERS:
        if tokens.get(tp):
            tok_html += f' <span class="tok">🔥 {tp}</span>'
    adp_html = ' <span class="adp">🤝 Anti-Dogpile</span>' if anti_dogpile and all_same else ""
    fin_badge = ' <span class="cat" style="background:rgba(16,185,129,.15);color:#34d399">✅ Finalized</span>' if is_fin else ""

    # Picks row
    outcome = outcomes.get(idx_str, {})
    results = outcome.get("results", {})
    pick_html = ""
    for p in PLAYERS:
        pick_val = pred["picks"].get(p, "—")
        result = results.get(p, "")
        cls = ""
        if is_fin:
            if result in ("correct", "exact", "first", "tied_first"):
                cls = "correct"
            elif result == "close":
                cls = "close-r"
            elif result in ("incorrect", "third"):
                cls = "incorrect"
        color = PLAYER_COLORS[p]
        token_mark = " 🔥" if tokens.get(p) else ""
        pick_html += f'<span class="pick {cls}"><span style="color:{color};font-weight:700">{p}:</span> {pick_val}{token_mark}</span>'

    # Outcome box
    outcome_html = ""
    if is_fin:
        actual = outcome.get("actual_outcome", "")
        fd = outcome.get("finalized_date", "")
        fb = outcome.get("finalized_by", "")
        ps = score_prediction(pred, outcome)
        pts_str = " · ".join(
            f'<span style="color:{PLAYER_COLORS[p]}"><b>{p}:</b> {ps[p]["points"]}pts</span>'
            for p in PLAYERS
        )
        outcome_html = f"""<div class="outcome-box">
          <b>Outcome:</b> {actual} &nbsp;|&nbsp; {pts_str}
          <br><span style="color:#64748b;font-size:.78rem">Finalized {fd} by {fb}</span>
        </div>"""

    # Card
    st.markdown(f"""
    <div class="pcard {'fin' if is_fin else ''}">
      <div class="pmeta">{cat_html}{tok_html}{adp_html}{fin_badge}</div>
      <div class="pq">Q{idx}. {pred['prediction']}</div>
      <div class="pick-row">{pick_html}</div>
      {outcome_html}
    </div>""", unsafe_allow_html=True)

    # ── Finalize / Revert controls ───────────────────────────────────────
    if is_fin:
        with st.expander(f"🔧 Manage Q{idx}", expanded=False):
            st.caption(f"Currently finalized as: **{outcome.get('actual_outcome', '')}**")
            if st.button(f"↩️ Revert Q{idx} to Pending", key=f"revert_{idx}"):
                outcomes.pop(idx_str, None)
                save_data("outcomes.json", outcomes)
                invalidate_cache("outcomes.json")
                st.success(f"Q{idx} reverted to pending.")
                st.rerun()
    else:
        with st.expander(f"⚡ Finalize Q{idx}", expanded=False):
            _finalize_prediction(pred, outcomes, books, flights)
