"""
✈️ Flight Log — Track flights for the Wildcard Q49 competition.
"""

import streamlit as st
import uuid
from datetime import date

from data_manager import load_data, save_data, invalidate_cache
from scoring import PLAYERS, PLAYER_COLORS, get_flight_counts

st.set_page_config(page_title="Flight Log | BR2026", page_icon="✈️", layout="wide")

# ─── CSS ─────────────────────────────────────────────────────────────────
st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
.fcard{background:linear-gradient(165deg,#1e293b,#0f172a);border-radius:14px;
  padding:1.3rem;border:1px solid rgba(255,255,255,.06);text-align:center}
.fcard .cnt{font-size:2.8rem;font-weight:900;margin:.2rem 0}
.fcard .lab{color:#64748b;font-size:.82rem;font-weight:600}
.fcard .dest{color:#94a3b8;font-size:.78rem;margin-top:.3rem}
.flight-row{background:linear-gradient(165deg,#1e293b,#0f172a);border-radius:12px;
  padding:.85rem 1.1rem;margin:.4rem 0;border:1px solid rgba(255,255,255,.05);
  display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:.5rem}
.flight-route{font-weight:700;font-size:.95rem;color:#e2e8f0}
.flight-meta{color:#94a3b8;font-size:.8rem;margin-top:.12rem}
.flight-person{font-weight:700;font-size:.85rem}
.route-arrow{color:#60a5fa;font-weight:800;margin:0 .3rem}
</style>""", unsafe_allow_html=True)

# ─── Sidebar ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("# ✈️ Flight Log")
    st.caption("Q49: Who takes the most flights?")
    st.markdown("---")
    st.info("Log each **one-way** flight journey separately.")

# ─── Data ────────────────────────────────────────────────────────────────
flights = load_data("flights.json", [])
counts = get_flight_counts(flights)

# ─── Standings ───────────────────────────────────────────────────────────
st.markdown("### ✈️ Flight Journey Competition")
st.markdown("*Wildcard Q49 — Takes the most number of flight journeys*")
st.markdown("")

cols = st.columns(3)
sorted_players = sorted(PLAYERS, key=lambda p: counts[p], reverse=True)

for i, p in enumerate(sorted_players):
    c = PLAYER_COLORS[p]
    medal = ["🥇", "🥈", "🥉"][i] if counts[p] > 0 or i == 0 else ""

    # Unique destinations
    player_flights = [f for f in flights if f.get("person") == p]
    dests = set()
    for fl in player_flights:
        if fl.get("to_airport"):
            dests.add(fl["to_airport"].upper())
        if fl.get("from_airport"):
            dests.add(fl["from_airport"].upper())
    dest_count = len(dests)

    with cols[i]:
        st.markdown(f"""
        <div class="fcard">
          <div style="font-size:1.5rem">{medal}</div>
          <div class="cnt" style="color:{c}">{counts[p]}</div>
          <div class="lab" style="color:{c}">{p}</div>
          <div class="dest">{dest_count} unique airport{'s' if dest_count!=1 else ''}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─── Add Flight Form ────────────────────────────────────────────────────
st.markdown("### ➕ Log a New Flight")

with st.form("add_flight", clear_on_submit=True):
    fc1, fc2 = st.columns(2)
    with fc1:
        person = st.selectbox("Traveller", PLAYERS)
        from_airport = st.text_input("From (airport code or city)", placeholder="e.g. YYZ")
    with fc2:
        to_airport = st.text_input("To (airport code or city)", placeholder="e.g. LAX")
        flight_date = st.date_input("Flight Date", value=date.today())

    submitted = st.form_submit_button("✈️ Add Flight", type="primary", use_container_width=True)

    if submitted:
        if not to_airport.strip():
            st.error("Please enter at least a destination.")
        else:
            new_flight = {
                "id": str(uuid.uuid4())[:8],
                "person": person,
                "from_airport": from_airport.strip().upper(),
                "to_airport": to_airport.strip().upper(),
                "date": str(flight_date),
                "date_logged": str(date.today()),
            }
            flights.append(new_flight)
            save_data("flights.json", flights)
            invalidate_cache("flights.json")
            st.success(f"✈️ Added flight for {person}: {from_airport.upper()} → {to_airport.upper()}")
            st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

# ─── Full Flight Log ────────────────────────────────────────────────────
st.markdown("### 🗺️ Full Flight Log")

filter_person = st.selectbox("Filter by traveller", ["All"] + PLAYERS, key="ffilter")
sorted_flights = sorted(flights, key=lambda f: f.get("date", ""), reverse=True)

if filter_person != "All":
    sorted_flights = [f for f in sorted_flights if f.get("person") == filter_person]

if not sorted_flights:
    st.info("No flights logged yet. Where are you headed? ✈️")
else:
    for fl in sorted_flights:
        p = fl.get("person", "")
        c = PLAYER_COLORS.get(p, "#ccc")
        fr = fl.get("from_airport", "???")
        to = fl.get("to_airport", "???")
        d  = fl.get("date", "?")
        arrow = "✈️"
        st.markdown(f"""
        <div class="flight-row">
          <div>
            <div class="flight-route">{fr if fr else '???'} <span class="route-arrow">→</span> {to if to else '???'}</div>
            <div class="flight-meta">{arrow} {d}</div>
          </div>
          <div class="flight-person" style="color:{c}">{p}</div>
        </div>""", unsafe_allow_html=True)

    # Delete option
    st.markdown("---")
    st.markdown("##### 🗑️ Remove a Flight Entry")
    flight_options = {
        f"{f.get('person','')} — {f.get('from_airport','?')} → {f.get('to_airport','?')} ({f.get('date','')})": f.get("id")
        for f in sorted_flights
    }
    if flight_options:
        selected = st.selectbox("Select flight to remove", list(flight_options.keys()), key="fdel")
        if st.button("🗑️ Remove Selected Flight", type="secondary"):
            flight_id = flight_options[selected]
            flights = [f for f in flights if f.get("id") != flight_id]
            save_data("flights.json", flights)
            invalidate_cache("flights.json")
            st.success("Flight entry removed.")
            st.rerun()
