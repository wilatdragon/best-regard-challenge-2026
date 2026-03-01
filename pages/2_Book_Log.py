"""
📚 Book Log — Track books read for the Wildcard Q48 competition.
"""

import streamlit as st
import uuid
from datetime import date

from data_manager import load_data, save_data, invalidate_cache
from scoring import PLAYERS, PLAYER_COLORS, get_book_counts

st.set_page_config(page_title="Book Log | BR2026", page_icon="📚", layout="wide")

# ─── CSS ─────────────────────────────────────────────────────────────────
st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
.bcard{background:linear-gradient(165deg,#1e293b,#0f172a);border-radius:14px;
  padding:1.3rem;border:1px solid rgba(255,255,255,.06);text-align:center}
.bcard .cnt{font-size:2.8rem;font-weight:900;margin:.2rem 0}
.bcard .lab{color:#64748b;font-size:.82rem;font-weight:600}
.bcard .avg{color:#94a3b8;font-size:.78rem;margin-top:.3rem}
.book-row{background:linear-gradient(165deg,#1e293b,#0f172a);border-radius:12px;
  padding:.9rem 1.1rem;margin:.4rem 0;border:1px solid rgba(255,255,255,.05);
  display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:.5rem}
.book-info{flex:1}
.book-title{font-weight:700;font-size:.95rem;color:#e2e8f0}
.book-meta{color:#94a3b8;font-size:.8rem;margin-top:.15rem}
.stars{color:#fbbf24;font-size:.9rem}
.book-person{font-weight:700;font-size:.85rem}
</style>""", unsafe_allow_html=True)

# ─── Sidebar ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("# 📚 Book Log")
    st.caption("Q48: Who reads the most books?")
    st.markdown("---")
    st.info("Books must be **over 150 pages** and **exclude audiobooks** to count.")

# ─── Data ────────────────────────────────────────────────────────────────
books = load_data("books.json", [])
counts = get_book_counts(books)

# ─── Standings ───────────────────────────────────────────────────────────
st.markdown("### 📚 Book Reading Competition")
st.markdown("*Wildcard Q48 — Reads the most books (over 150 pages, excl. audiobooks)*")
st.markdown("")

cols = st.columns(3)
sorted_players = sorted(PLAYERS, key=lambda p: counts[p], reverse=True)

for i, p in enumerate(sorted_players):
    c = PLAYER_COLORS[p]
    medal = ["🥇", "🥈", "🥉"][i] if counts[p] > 0 or i == 0 else ""
    # Average rating
    player_books = [b for b in books if b.get("person") == p]
    ratings = [b.get("rating", 0) for b in player_books if b.get("rating")]
    avg_r = sum(ratings) / len(ratings) if ratings else 0
    stars_html = "⭐" * int(round(avg_r)) if avg_r else "—"

    with cols[i]:
        st.markdown(f"""
        <div class="bcard">
          <div style="font-size:1.5rem">{medal}</div>
          <div class="cnt" style="color:{c}">{counts[p]}</div>
          <div class="lab" style="color:{c}">{p}</div>
          <div class="avg">Avg rating: {stars_html} ({avg_r:.1f}/5)</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─── Add Book Form ──────────────────────────────────────────────────────
st.markdown("### ➕ Log a New Book")

with st.form("add_book", clear_on_submit=True):
    fc1, fc2 = st.columns(2)
    with fc1:
        person = st.selectbox("Reader", PLAYERS)
        title = st.text_input("Book Title")
        author = st.text_input("Author")
    with fc2:
        pages = st.number_input("Pages", min_value=1, value=200, step=1)
        rating = st.slider("Rating", 1.0, 5.0, 3.5, 0.5)
        date_finished = st.date_input("Date Finished", value=date.today())

    submitted = st.form_submit_button("📖 Add Book", type="primary", use_container_width=True)

    if submitted:
        if not title.strip():
            st.error("Please enter a book title.")
        elif pages < 151:
            st.warning("Only books over 150 pages count toward the competition.")
        else:
            new_book = {
                "id": str(uuid.uuid4())[:8],
                "person": person,
                "title": title.strip(),
                "author": author.strip(),
                "pages": pages,
                "rating": rating,
                "date_finished": str(date_finished),
                "date_logged": str(date.today()),
            }
            books.append(new_book)
            save_data("books.json", books)
            invalidate_cache("books.json")
            st.success(f"📖 Added **{title}** for {person}!")
            st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

# ─── Full Book Log ──────────────────────────────────────────────────────
st.markdown("### 📖 Full Book Log")

filter_person = st.selectbox("Filter by reader", ["All"] + PLAYERS, key="bfilter")
sorted_books = sorted(books, key=lambda b: b.get("date_finished", ""), reverse=True)

if filter_person != "All":
    sorted_books = [b for b in sorted_books if b.get("person") == filter_person]

if not sorted_books:
    st.info("No books logged yet. Start reading! 📚")
else:
    for book in sorted_books:
        p = book.get("person", "")
        c = PLAYER_COLORS.get(p, "#ccc")
        r = book.get("rating", 0)
        stars = "⭐" * int(round(r)) if r else ""
        st.markdown(f"""
        <div class="book-row">
          <div class="book-info">
            <div class="book-title">📗 {book.get('title', 'Untitled')}</div>
            <div class="book-meta">
              by {book.get('author', 'Unknown')} · {book.get('pages', '?')} pages ·
              Finished {book.get('date_finished', '?')}
            </div>
            <div class="stars">{stars} ({r:.1f})</div>
          </div>
          <div class="book-person" style="color:{c}">{p}</div>
        </div>""", unsafe_allow_html=True)

    # Delete option
    st.markdown("---")
    st.markdown("##### 🗑️ Remove a Book Entry")
    book_options = {
        f"{b.get('person','')} — {b.get('title','Untitled')} ({b.get('date_finished','')})": b.get("id")
        for b in sorted_books
    }
    if book_options:
        selected = st.selectbox("Select book to remove", list(book_options.keys()), key="bdel")
        if st.button("🗑️ Remove Selected Book", type="secondary"):
            book_id = book_options[selected]
            books = [b for b in books if b.get("id") != book_id]
            save_data("books.json", books)
            invalidate_cache("books.json")
            st.success("Book entry removed.")
            st.rerun()
