"""
📜 Rules — Official scoring rules and reference for Best Regard Challenge 2026.
"""

import streamlit as st

st.set_page_config(page_title="Rules | BR2026", page_icon="📜", layout="wide")

# ─── CSS ─────────────────────────────────────────────────────────────────
st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
.rule-section{background:linear-gradient(165deg,#1e293b,#0f172a);border-radius:14px;
  padding:1.4rem 1.6rem;margin:.8rem 0;border:1px solid rgba(255,255,255,.06)}
.rule-section h3{margin-top:0;color:#FFD700;font-weight:700}
.rule-section h4{color:#e2e8f0;margin-top:.8rem}
.rule-table{width:100%;border-collapse:collapse;margin:.6rem 0}
.rule-table th{text-align:left;padding:.5rem .8rem;border-bottom:2px solid rgba(255,255,255,.1);
  color:#94a3b8;font-weight:600;font-size:.82rem;text-transform:uppercase}
.rule-table td{padding:.5rem .8rem;border-bottom:1px solid rgba(255,255,255,.04);
  color:#e2e8f0;font-size:.9rem}
.rule-table tr:last-child td{border:none}
.token-ex{background:rgba(245,158,11,.08);border:1px solid rgba(245,158,11,.2);
  border-radius:10px;padding:.8rem 1rem;margin:.5rem 0;font-size:.88rem}
.adp-ex{background:rgba(239,68,68,.06);border:1px solid rgba(239,68,68,.15);
  border-radius:10px;padding:.8rem 1rem;margin:.5rem 0;font-size:.88rem}
.prize-box{background:linear-gradient(135deg,rgba(255,215,0,.08),rgba(255,215,0,.02));
  border:1px solid rgba(255,215,0,.2);border-radius:14px;padding:1.3rem;text-align:center;margin:1rem 0}
.prize-box h3{color:#FFD700;margin:0}
.prize-box p{color:#94a3b8;margin:.4rem 0 0}
</style>""", unsafe_allow_html=True)

# ─── Sidebar ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("# 📜 Rules")
    st.caption("Official rulebook")

# ─── Header ──────────────────────────────────────────────────────────────
st.markdown("# 📜 Best Regard Challenge 2026 — Official Rules")
st.markdown("*Locked in January 15, 2026*")
st.markdown("")

# ─── Lock-In ─────────────────────────────────────────────────────────────
st.markdown("""<div class="rule-section">
<h3>📅 Lock-In Date</h3>
<p>All predictions were submitted and finalized by <b>January 15, 2026 (11:59 PM EST)</b>.</p>
<p>After this date:</p>
<ul>
  <li>The prediction document is <b>view-only</b></li>
  <li>No edits, additions, or clarifications allowed</li>
  <li>Ambiguous predictions are scored conservatively</li>
</ul>
</div>""", unsafe_allow_html=True)

# ─── Categories ──────────────────────────────────────────────────────────
st.markdown("""<div class="rule-section">
<h3>🎯 Prediction Categories</h3>
<table class="rule-table">
<tr><th>Category</th><th>Questions</th><th>Description</th></tr>
<tr><td><span style="color:#60a5fa">🏟️ Sports & Entertainment</span></td><td>Q1 – Q15</td><td>Sports outcomes, cultural picks</td></tr>
<tr><td><span style="color:#fbbf24">🌍 World / Public Events</span></td><td>Q16 – Q41</td><td>Politics, economics, geopolitics</td></tr>
<tr><td><span style="color:#f472b6">👥 Friend Life Events</span></td><td>Q42 – Q46</td><td>Personal predictions about the group</td></tr>
<tr><td><span style="color:#a78bfa">🃏 Wildcards</span></td><td>Q47 – Q49</td><td>Fun picks & competitions</td></tr>
</table>
</div>""", unsafe_allow_html=True)

# ─── Scoring ─────────────────────────────────────────────────────────────
st.markdown("""<div class="rule-section">
<h3>📊 Scoring System</h3>

<h4>Yes / No Predictions</h4>
<table class="rule-table">
<tr><th>Result</th><th>Points</th><th>Example</th></tr>
<tr><td>✅ Correct</td><td><b>2</b></td><td>You predicted "Yes" and it happened</td></tr>
<tr><td>❌ Incorrect</td><td><b>0</b></td><td>You predicted "Yes" but it didn't happen</td></tr>
</table>

<h4>Multi-Outcome Predictions</h4>
<table class="rule-table">
<tr><th>Result</th><th>Points</th><th>Example</th></tr>
<tr><td>🎯 Exact</td><td><b>4</b></td><td>You predicted "OKC wins NBA" and they won</td></tr>
<tr><td>🔥 Close</td><td><b>1</b></td><td>Your pick lost in the finals (runner-up)</td></tr>
<tr><td>❌ Incorrect</td><td><b>0</b></td><td>Your pick didn't come close</td></tr>
</table>

<h4>Wildcard Competitions (Q48 & Q49)</h4>
<table class="rule-table">
<tr><th>Place</th><th>Points</th><th>Tie Rule</th></tr>
<tr><td>🥇 1st Place</td><td><b>+5</b></td><td>2-way tie for 1st → +4 each</td></tr>
<tr><td>🥈 2nd Place</td><td><b>+3</b></td><td>2-way tie for last → +2 each</td></tr>
<tr><td>🥉 3rd Place</td><td><b>0</b></td><td>3-way tie → +4 each</td></tr>
</table>
</div>""", unsafe_allow_html=True)

# ─── Confidence Tokens ──────────────────────────────────────────────────
st.markdown("""<div class="rule-section">
<h3>🔥 Confidence Tokens</h3>
<p>Each player receives <b>3 Confidence Tokens</b> total.</p>
<ul>
  <li>A token may be assigned to any single prediction</li>
  <li>Tokens were declared before the lock-in date</li>
  <li>If the prediction is <b>correct → double points</b></li>
  <li>If the prediction is <b>incorrect → 0 points</b> (no extra penalty)</li>
</ul>
<p>⚠️ Tokens cannot be reused or moved. Indicated by an asterisk (*) on the pick.</p>

<div class="token-ex">
<b>Token Allocations:</b><br>
🔵 <b>Arnav:</b> Q4 (F1 Driver), Q15 (Grand Slams), Q48 (Books Wildcard)<br>
🟣 <b>Sibi:</b> Q5 (F1 Constructor), Q29 (Ontario Project), Q42 (Company Switch)<br>
🟢 <b>Nikhil:</b> Q3 (Super Bowl), Q6 (Billboard), Q12 (FIFA World Cup)
</div>
</div>""", unsafe_allow_html=True)

# ─── Anti-Dogpile ──────────────────────────────────────────────────────
st.markdown("""<div class="rule-section">
<h3>🚫 Anti-Dogpile Rule</h3>
<p><b>Applies to: Friend Life Events (Q42–Q46) only</b></p>
<p>If <b>all three players</b> pick the same outcome, the <b>maximum score is 1 point</b>,
even if the prediction is correct.</p>
<p>Confidence Tokens <b>do not</b> override this rule.</p>

<div class="adp-ex">
<b>Affected predictions:</b> Q43 (all Y), Q44 (all Y), Q45 (all N), Q46 (all N)
</div>
</div>""", unsafe_allow_html=True)

# ─── Wildcard Scoring ──────────────────────────────────────────────────
st.markdown("""<div class="rule-section">
<h3>🎭 Wildcard Scoring</h3>
<p>Q47 ("One of us finds god") is scored as a normal Yes/No prediction.</p>
<p>Q48 (Books) and Q49 (Flights) are <b>competitions</b> — the winner is whoever
achieves the most by the end of 2026. These are scored by the wildcard point system
(+5 / +3 / 0 with tie rules).</p>
<p>Wildcards may also be scored by group vote at the end of 2026 if needed.</p>
</div>""", unsafe_allow_html=True)

# ─── Winner's Reward ─────────────────────────────────────────────────────
st.markdown("""<div class="prize-box">
<h3>🏅 Winner's Reward</h3>
<p>The <b>2026 Prediction Champion</b> wins a <b>free meal</b> when the group eats out together.</p>
<p style="font-size:.82rem;color:#64748b">
  Must be a single group outing (all players present) · Reasonable cost (good faith) ·
  Redeemable by December 31, 2027
</p>
</div>""", unsafe_allow_html=True)

# ─── Quick Reference ─────────────────────────────────────────────────────
st.markdown("---")
st.markdown("### ⚡ Quick Scoring Reference")

qcols = st.columns(4)
with qcols[0]:
    st.metric("Yes/No Correct", "2 pts")
with qcols[1]:
    st.metric("Multi Exact", "4 pts")
with qcols[2]:
    st.metric("Multi Close", "1 pt")
with qcols[3]:
    st.metric("Token Multiplier", "2×")
