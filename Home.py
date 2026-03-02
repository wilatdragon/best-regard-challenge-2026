"""
🏆 Best Regard Challenge 2026 — Home / Dashboard
"""

import streamlit as st
from datetime import date

from data_manager import load_data
from scoring import (
    calculate_all_scores, get_book_counts, get_flight_counts,
    PLAYERS, PLAYER_COLORS, CATEGORIES, CATEGORY_COLORS,
)

# ─── Page config ─────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Best Regard Challenge 2026",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Load data ───────────────────────────────────────────────────────────
predictions = load_data("predictions.json", [])
outcomes     = load_data("outcomes.json", {})
books        = load_data("books.json", [])
flights      = load_data("flights.json", [])
scores       = calculate_all_scores(predictions, outcomes, books, flights)
book_counts  = get_book_counts(books)
flight_counts = get_flight_counts(flights)

finalized = sum(1 for o in outcomes.values() if o.get("status") == "finalized")
total     = len(predictions)
remaining = total - finalized
pct       = int(finalized / total * 100) if total else 0
days_left = max((date(2026, 12, 31) - date.today()).days, 0)

# ─── CSS ─────────────────────────────────────────────────────────────────
st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
section[data-testid="stSidebar"] .stMarkdown h1 {font-size:1.2rem;}
.hero{text-align:center;padding:2.5rem 1rem 2rem;
  background:linear-gradient(135deg,#0f0c29 0%,#302b63 50%,#24243e 100%);
  border-radius:20px;margin-bottom:1.8rem;
  border:1px solid rgba(255,215,0,.15);position:relative;overflow:hidden}
.hero::before{content:'';position:absolute;inset:-50%;width:200%;height:200%;
  background:radial-gradient(circle,rgba(255,215,0,.04) 0%,transparent 70%);
  animation:pulse 5s ease-in-out infinite}
@keyframes pulse{0%,100%{transform:scale(1)}50%{transform:scale(1.06)}}
.hero h1{font-family:'Inter',sans-serif;color:#FFD700;font-size:2.6rem;
  font-weight:900;margin:0;text-shadow:0 0 30px rgba(255,215,0,.3);position:relative;letter-spacing:-.02em}
.hero .sub{color:#94a3b8;font-size:1.1rem;margin-top:.5rem;font-weight:400;position:relative}
.hero .days{margin-top:.9rem;color:#64748b;font-size:.88rem;position:relative}
.hero .days b{color:#FFD700;font-size:1.7rem;font-weight:800}

.pod{text-align:center;padding:1.6rem 1rem;border-radius:16px;
  background:linear-gradient(165deg,#1e293b,#0f172a);border:2px solid;transition:transform .3s,box-shadow .3s}
.pod:hover{transform:translateY(-5px)}
.pod.g{border-color:#FFD700;box-shadow:0 8px 32px rgba(255,215,0,.15)}
.pod.s{border-color:#C0C0C0;box-shadow:0 6px 24px rgba(192,192,192,.10)}
.pod.b{border-color:#CD7F32;box-shadow:0 6px 24px rgba(205,127,50,.10)}
.pod .medal{font-size:2.4rem}
.pod .pname{font-size:1.3rem;font-weight:700;margin:.25rem 0}
.pod .pscore{font-size:2.8rem;font-weight:900;margin:.1rem 0}
.pod .pdetail{color:#94a3b8;font-size:.82rem}

.sc{background:linear-gradient(165deg,#1e293b,#0f172a);border-radius:14px;
  padding:1.3rem;border:1px solid rgba(255,255,255,.06);text-align:center}
.sc .lab{color:#64748b;font-size:.75rem;font-weight:600;text-transform:uppercase;letter-spacing:.08em}
.sc .val{font-family:'Inter',sans-serif;color:#f1f5f9;font-size:1.9rem;font-weight:800;margin-top:.15rem}

.tally{background:linear-gradient(165deg,#1e293b,#0f172a);border-radius:14px;
  padding:1.4rem;border:1px solid rgba(255,255,255,.06)}
.tally h4{font-size:1.05rem;font-weight:700;color:#e2e8f0;margin:0 0 .9rem}
.tr{display:flex;align-items:center;padding:.45rem 0;border-bottom:1px solid rgba(255,255,255,.04)}
.tr:last-child{border:none}
.tr .tn{font-weight:600;width:70px;font-size:.92rem}
.tr .tb{flex:1;height:10px;border-radius:5px;background:rgba(255,255,255,.06);margin:0 .8rem;overflow:hidden}
.tr .tf{height:100%;border-radius:5px;transition:width .6s ease}
.tr .tc{font-weight:800;font-size:1.15rem;min-width:28px;text-align:right}

.pbar-wrap{background:rgba(255,255,255,.06);border-radius:10px;height:14px;overflow:hidden;margin:.4rem 0}
.pbar-fill{height:100%;border-radius:10px;background:linear-gradient(90deg,#FFD700,#f59e0b);transition:width .6s}

.cat-chip{display:inline-block;padding:3px 10px;border-radius:20px;font-size:.72rem;font-weight:600;margin:2px}

.act-row{padding:.5rem 0;border-bottom:1px solid rgba(255,255,255,.04);font-size:.88rem}
.act-row:last-child{border:none}
.act-q{font-weight:700;color:#e2e8f0}
.act-d{color:#64748b;font-size:.78rem}
</style>""", unsafe_allow_html=True)

# ─── Sidebar ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("# 🏆 Best Regard 2026")
    st.caption("Arnav · Sibi · Nikhil")
    st.markdown("---")

    if st.button("🔄 Refresh Data", use_container_width=True):
        from data_manager import invalidate_cache
        invalidate_cache()
        st.rerun()

# ─── Hero ────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="hero">
  <h1>🏆 Best Regard Challenge 2026</h1>
  <div class="sub">The Ultimate Prediction Showdown &nbsp;·&nbsp; Arnav vs Sibi vs Nikhil</div>
  <div class="days"><b>{days_left}</b> days remaining in 2026</div>
</div>""", unsafe_allow_html=True)

# ─── Leaderboard (podium) ───────────────────────────────────────────────
sorted_p = sorted(PLAYERS, key=lambda p: scores[p]["total"], reverse=True)
medals   = ["🥇", "🥈", "🥉"]
css_cls  = ["g", "s", "b"]
order    = [1, 0, 2]  # 2nd | 1st | 3rd
widths   = [1, 1.2, 1]

cols = st.columns(widths)
for i, rank_idx in enumerate(order):
    p = sorted_p[rank_idx]
    c = PLAYER_COLORS[p]
    with cols[i]:
        token_str = f"{scores[p]['token_bonus']} token pts" if scores[p]['token_bonus'] else "0 token pts"
        st.markdown(f"""
        <div class="pod {css_cls[rank_idx]}" style="{'margin-top:1.6rem' if rank_idx!=0 else ''}">
          <div class="medal">{medals[rank_idx]}</div>
          <div class="pname" style="color:{c}">{p}</div>
          <div class="pscore" style="color:{c}">{scores[p]['total']}</div>
          <div class="pdetail">{scores[p]['correct_count']} correct &nbsp;·&nbsp; {token_str}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─── Progress + Stats ────────────────────────────────────────────────────
st.markdown(f"""
<div class="sc" style="margin-bottom:1.2rem">
  <div class="lab">Challenge Progress</div>
  <div class="val">{finalized} / {total} finalized</div>
  <div class="pbar-wrap"><div class="pbar-fill" style="width:{pct}%"></div></div>
</div>""", unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
for col, label, val in [
    (c1, "Finalized", finalized),
    (c2, "Pending", remaining),
    (c3, "Categories", len(CATEGORIES)),
    (c4, "Days Left", days_left),
]:
    with col:
        st.markdown(f'<div class="sc"><div class="lab">{label}</div><div class="val">{val}</div></div>',
                     unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─── Book & Flight Tallies ───────────────────────────────────────────────
tc1, tc2 = st.columns(2)

def tally_html(title, emoji, counts):
    max_c = max(counts.values()) if any(counts.values()) else 1
    rows = ""
    for p in sorted(PLAYERS, key=lambda x: counts[x], reverse=True):
        c = PLAYER_COLORS[p]
        w = int(counts[p] / max_c * 100) if max_c else 0
        rows += f"""<div class="tr">
          <div class="tn" style="color:{c}">{p}</div>
          <div class="tb"><div class="tf" style="width:{w}%;background:{c}"></div></div>
          <div class="tc" style="color:{c}">{counts[p]}</div>
        </div>"""
    return f'<div class="tally"><h4>{emoji} {title}</h4>{rows}</div>'

with tc1:
    st.markdown(tally_html("Books Read", "📚", book_counts), unsafe_allow_html=True)
with tc2:
    st.markdown(tally_html("Flights Taken", "✈️", flight_counts), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─── Category Breakdown ─────────────────────────────────────────────────
st.markdown("### 📊 Score by Category")

cat_tabs = st.tabs(["All Categories"] + CATEGORIES)

with cat_tabs[0]:
    # Summary — one row per player
    for p in sorted_p:
        bd = scores[p]["breakdown"]
        chips = ""
        for cat in CATEGORIES:
            pts = bd.get(cat, 0)
            cc = CATEGORY_COLORS.get(cat, {})
            chips += f'<span class="cat-chip" style="background:{cc.get("bg","#333")};color:{cc.get("fg","#ccc")}">{cat.split("/")[0][:12]}: {pts}</span> '
        st.markdown(
            f'<div style="padding:.5rem 0"><span style="font-weight:700;color:{PLAYER_COLORS[p]}">'
            f'{p}</span> &nbsp;—&nbsp; {chips}</div>',
            unsafe_allow_html=True,
        )

for ci, cat in enumerate(CATEGORIES, 1):
    with cat_tabs[ci]:
        cat_preds = [p for p in predictions if p["category"] == cat]
        for pred in cat_preds:
            idx_str = str(pred["index"])
            status_icon = "✅" if idx_str in outcomes and outcomes[idx_str].get("status") == "finalized" else "⏳"
            st.markdown(f"**{status_icon} Q{pred['index']}** — {pred['prediction']}")

st.markdown("<br>", unsafe_allow_html=True)

# ─── Recent Activity ─────────────────────────────────────────────────────
st.markdown("### 🕐 Recent Finalizations")

recent = []
pred_map = {p["index"]: p for p in predictions}
for idx_str, o in outcomes.items():
    if o.get("status") == "finalized":
        pred = pred_map.get(int(idx_str))
        if pred:
            recent.append({
                "index": int(idx_str),
                "prediction": pred["prediction"],
                "date": o.get("finalized_date", ""),
                "outcome": o.get("actual_outcome", ""),
                "by": o.get("finalized_by", ""),
            })

recent.sort(key=lambda r: r["date"], reverse=True)

if recent:
    for r in recent[:10]:
        st.markdown(
            f'<div class="act-row"><span class="act-q">Q{r["index"]}</span> '
            f'{r["prediction"][:55]} → <b>{r["outcome"]}</b> '
            f'<span class="act-d">{r["date"]} by {r["by"]}</span></div>',
            unsafe_allow_html=True,
        )
else:
    st.info("No predictions finalized yet. Head to the **Predictions** page to start locking in results!")

st.markdown("<br>", unsafe_allow_html=True)
st.caption("Best Regard Challenge 2026 · Built with Streamlit · May the best oracle win 🔮")
