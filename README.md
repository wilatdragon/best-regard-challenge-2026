# 🏆 Best Regard Challenge 2026

A Streamlit-powered prediction challenge tracker for Arnav, Sibi, and Nikhil.

## Features

- **Live Leaderboard** — Podium-style dashboard with cumulative scores
- **49 Predictions** — Browse, filter, and finalize outcomes across 4 categories
- **Confidence Tokens** — 3 per player; double points on correct picks
- **Anti-Dogpile Rule** — Friend Life Events capped at 1 pt when all agree
- **Book Log** (Q48) — Track books read with ratings, page counts
- **Flight Log** (Q49) — Track one-way flights with origins/destinations
- **Score Timeline** — Interactive Plotly chart showing the race over time
- **Head-to-Head** — Direct comparisons between any two players
- **Rules Reference** — Complete, styled scoring rulebook

## Running Locally

```bash
cd best-regard-challenge-2026-website
pip install -r requirements.txt
streamlit run Home.py
```

The app uses local JSON files in `data/` for persistence.

## Deploying to Streamlit Cloud

1. Push this folder to a GitHub repo.
2. Go to [share.streamlit.io](https://share.streamlit.io) and connect the repo.
3. Set the main file path to `Home.py`.
4. **(Required for durable data)** Add these secrets in Streamlit Cloud:

```toml
[github]
token = "ghp_your_personal_access_token"
repo  = "your-username/your-repo-name"
branch = "main"
data_path = "data"
```

Without GitHub secrets, the app writes to local ephemeral storage in the Streamlit
container. When the app sleeps/restarts, data can reset to repository defaults.

### GitHub Token Permissions

Your token must be able to update files in the repository:

- Classic token: `repo` scope
- Fine-grained token: repository access to this repo + `Contents: Read and write`

After adding secrets, restart the app in Streamlit Cloud once. The sidebar on
the Home page should show: `Persistence: GitHub (durable across app restarts)`.

## Project Structure

```
Home.py                   # Main dashboard / leaderboard
data_manager.py           # Data I/O (local + GitHub API)
scoring.py                # Scoring engine & helpers
requirements.txt
.streamlit/config.toml    # Theme configuration
data/
  predictions.json        # 49 locked-in predictions (read-only)
  outcomes.json           # Finalized outcomes
  books.json              # Book log entries
  flights.json            # Flight log entries
pages/
  1_Predictions.py        # Browse & finalize predictions
  2_Book_Log.py           # Book reading competition
  3_Flight_Log.py         # Flight journey competition
  4_Score_Timeline.py     # Score-over-time chart
  5_Rules.py              # Official rules reference
```

## Scoring Quick Reference

| Type | Result | Points |
|------|--------|--------|
| Yes/No | Correct | 2 |
| Yes/No | Incorrect | 0 |
| Multi-outcome | Exact | 4 |
| Multi-outcome | Close | 1 |
| Multi-outcome | Incorrect | 0 |
| Wildcard | 1st place | 5 |
| Wildcard | 2nd place | 3 |
| Wildcard | 3rd place | 0 |
| Confidence Token | Correct pick | 2× points |
| Anti-dogpile | All 3 agree (Friend only) | Max 1 pt |

---

*May the best oracle win 🔮*
