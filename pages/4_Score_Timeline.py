"""
📈 Score Timeline — Visualize how scores evolve over time.
"""

import streamlit as st
import plotly.graph_objects as go

from data_manager import load_data
from scoring import (
    calculate_all_scores, get_score_timeline,
    PLAYERS, PLAYER_COLORS,
)

st.set_page_config(page_title="Score Timeline | BR2026", page_icon="📈", layout="wide")

# ─── CSS ─────────────────────────────────────────────────────────────────
st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
.timeline-hero{text-align:center;padding:1.5rem;background:linear-gradient(165deg,#1e293b,#0f172a);
  border-radius:16px;margin-bottom:1.5rem;border:1px solid rgba(255,255,255,.06)}
.timeline-hero h2{margin:0;font-weight:800;color:#e2e8f0}
.timeline-hero p{color:#64748b;margin:.3rem 0 0;font-size:.9rem}
</style>""", unsafe_allow_html=True)

# ─── Sidebar ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("# 📈 Score Timeline")
    st.caption("Watch the race unfold")
    st.markdown("---")
    show_markers = st.checkbox("Show event markers", value=True)
    show_grid = st.checkbox("Show grid", value=True)

# ─── Data ────────────────────────────────────────────────────────────────
predictions = load_data("predictions.json", [])
outcomes    = load_data("outcomes.json", {})
books       = load_data("books.json", [])
flights     = load_data("flights.json", [])

scores   = calculate_all_scores(predictions, outcomes, books, flights)
timeline = get_score_timeline(predictions, outcomes)

# ─── Header ──────────────────────────────────────────────────────────────
st.markdown("""<div class="timeline-hero">
  <h2>📈 The Race Over Time</h2>
  <p>Cumulative scores based on finalized prediction dates</p>
</div>""", unsafe_allow_html=True)

# ─── Chart ───────────────────────────────────────────────────────────────
if not timeline:
    st.info("No finalized predictions yet. Scores will appear here as outcomes are locked in.")
    st.stop()

fig = go.Figure()

for player in PLAYERS:
    dates  = [t["date"] for t in timeline]
    vals   = [t[player] for t in timeline]
    labels = [t.get("label", "") for t in timeline]

    fig.add_trace(go.Scatter(
        x=dates,
        y=vals,
        name=player,
        mode="lines+markers" if show_markers else "lines",
        line=dict(color=PLAYER_COLORS[player], width=3),
        marker=dict(size=8, symbol="circle"),
        hovertemplate=(
            f"<b>{player}</b><br>"
            "Date: %{x}<br>"
            "Score: %{y}<br>"
            "%{text}<extra></extra>"
        ),
        text=labels,
    ))

fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, sans-serif"),
    height=500,
    margin=dict(l=40, r=20, t=40, b=40),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="center",
        x=0.5,
        font=dict(size=14),
    ),
    xaxis=dict(
        title="Date",
        showgrid=show_grid,
        gridcolor="rgba(255,255,255,0.05)",
        zeroline=False,
    ),
    yaxis=dict(
        title="Cumulative Score",
        showgrid=show_grid,
        gridcolor="rgba(255,255,255,0.05)",
        zeroline=False,
    ),
    hovermode="x unified",
)

st.plotly_chart(fig, use_container_width=True)

# ─── Score Table ─────────────────────────────────────────────────────────
st.markdown("### 📊 Finalization Log")

# Reverse chronological
for t in reversed(timeline):
    pts_str = " · ".join(
        f"**{p}:** {t[p]}" for p in PLAYERS
    )
    st.markdown(f"**{t['date']}** — {t.get('label','')}  \n{pts_str}")

st.markdown("<br>", unsafe_allow_html=True)

# ─── Head-to-Head Comparison ─────────────────────────────────────────────
st.markdown("### 🆚 Head-to-Head")

h2h_cols = st.columns(3)
pairs = [("Arnav", "Sibi"), ("Arnav", "Nikhil"), ("Sibi", "Nikhil")]
for i, (p1, p2) in enumerate(pairs):
    with h2h_cols[i]:
        s1, s2 = scores[p1]["total"], scores[p2]["total"]
        winner = p1 if s1 > s2 else (p2 if s2 > s1 else "Tied")
        icon = "🏆" if winner != "Tied" else "🤝"
        st.markdown(
            f"""<div style="background:linear-gradient(165deg,#1e293b,#0f172a);
            border-radius:14px;padding:1.2rem;text-align:center;
            border:1px solid rgba(255,255,255,.06)">
            <div style="font-size:.85rem;color:#64748b">{p1} vs {p2}</div>
            <div style="font-size:1.6rem;font-weight:800;margin:.3rem 0">
              <span style="color:{PLAYER_COLORS[p1]}">{s1}</span>
              <span style="color:#4b5563;margin:0 .3rem">—</span>
              <span style="color:{PLAYER_COLORS[p2]}">{s2}</span>
            </div>
            <div style="font-size:.82rem">{icon} {winner if winner != 'Tied' else 'Tied!'}</div>
            </div>""",
            unsafe_allow_html=True,
        )
