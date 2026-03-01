"""Quick test for the scoring engine."""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))

from scoring import (
    score_prediction, calculate_all_scores, auto_results_yes_no,
    rank_wildcard, get_book_counts, get_flight_counts, PLAYERS
)

# Test 1: Super Bowl Q3 - Nikhil exact with confidence token
pred_q3 = {
    "index": 3, "type": "multi_outcome",
    "picks": {"Arnav": "Buffalo", "Sibi": "LAR", "Nikhil": "Seattle"},
    "tokens": {"Nikhil": True}, "anti_dogpile": False,
}
outcome_q3 = {
    "status": "finalized",
    "results": {"Arnav": "incorrect", "Sibi": "incorrect", "Nikhil": "exact"},
}
r3 = score_prediction(pred_q3, outcome_q3)
assert r3["Nikhil"]["points"] == 8, f"Expected 8, got {r3['Nikhil']['points']}"
assert r3["Arnav"]["points"] == 0
assert r3["Sibi"]["points"] == 0
print("Test 1 PASS: Q3 Super Bowl scoring correct (Nikhil=8 with token)")

# Test 2: Yes/No with anti-dogpile (Q43 all pick Y)
pred_q43 = {
    "index": 43, "type": "yes_no",
    "picks": {"Arnav": "Y", "Sibi": "Y", "Nikhil": "Y"},
    "tokens": {}, "anti_dogpile": True,
}
outcome_q43 = {
    "status": "finalized",
    "results": {"Arnav": "correct", "Sibi": "correct", "Nikhil": "correct"},
}
r43 = score_prediction(pred_q43, outcome_q43)
assert r43["Arnav"]["points"] == 1, f"Expected 1 (anti-dogpile), got {r43['Arnav']['points']}"
print("Test 2 PASS: Q43 anti-dogpile caps at 1 point")

# Test 3: auto_results_yes_no
pred_yes = {
    "index": 7, "type": "yes_no",
    "picks": {"Arnav": "Y", "Sibi": "Y", "Nikhil": "N"},
    "tokens": {}, "anti_dogpile": False,
}
results = auto_results_yes_no(pred_yes, "Y")
assert results["Arnav"] == "correct"
assert results["Nikhil"] == "incorrect"
print("Test 3 PASS: auto_results_yes_no works correctly")

# Test 4: Wildcard ranking
counts = {"Arnav": 5, "Sibi": 5, "Nikhil": 3}
rankings = rank_wildcard(counts)
assert rankings["Arnav"] == "tied_first"
assert rankings["Sibi"] == "tied_first"
assert rankings["Nikhil"] == "third"
print("Test 4 PASS: Wildcard tie for 1st gives tied_first")

# Test 5: 3-way tie
counts3 = {"Arnav": 4, "Sibi": 4, "Nikhil": 4}
r5 = rank_wildcard(counts3)
assert all(r5[p] == "tied_first" for p in PLAYERS)
print("Test 5 PASS: 3-way tie gives tied_first to all")

# Test 6: Confidence token on anti-dogpile (Q43 with hypothetical token)
pred_q44_tok = {
    "index": 44, "type": "yes_no",
    "picks": {"Arnav": "Y", "Sibi": "Y", "Nikhil": "Y"},
    "tokens": {"Arnav": True}, "anti_dogpile": True,
}
outcome_q44 = {
    "status": "finalized",
    "results": {"Arnav": "correct", "Sibi": "correct", "Nikhil": "correct"},
}
r6 = score_prediction(pred_q44_tok, outcome_q44)
assert r6["Arnav"]["points"] == 1, f"Expected 1 (anti-dogpile caps token), got {r6['Arnav']['points']}"
print("Test 6 PASS: Confidence token does NOT override anti-dogpile cap")

# Test 7: Full scoring calculation
predictions = json.load(open(os.path.join(os.path.dirname(__file__), "data", "predictions.json")))
outcomes = {
    "3": outcome_q3,
    "43": outcome_q43,
}
all_scores = calculate_all_scores(predictions, outcomes)
assert all_scores["Nikhil"]["total"] == 9  # 8 from Q3 + 1 from Q43
assert all_scores["Arnav"]["total"] == 1   # 0 from Q3 + 1 from Q43
assert all_scores["Sibi"]["total"] == 1    # 0 from Q3 + 1 from Q43
print("Test 7 PASS: Full scoring aggregation correct")

print("\n All 7 tests passed!")
