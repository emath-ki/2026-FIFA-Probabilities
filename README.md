# World Cup 2026: Match Odds

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://YOUR_USERNAME-world-cup-2026-dashboard.streamlit.app)
![GitHub last commit](https://img.shields.io/github/last-commit/YOUR_USERNAME/world-cup-2026-dashboard)
![License](https://img.shields.io/badge/license-MIT-blue)

> **A human‑centred look at group‑stage uncertainty before the first kickoff by Eshwaree**  
> Elo‑based probabilities, storytelling, and an interactive dashboard.

---

## 🎯 What It Does

This dashboard turns raw match probability data into a clean, scannable story.  
Instead of numbers in a table, you get:

- 📊 **Upset Potential by Group** — where surprises are most likely  
- 🔄 **Competitive Balance** — the statistical “Group of Death”  
- 🐶 **Underdog‑Friendly Groups** — where the away team has real hope  
- 🎲 **Match‑level drill‑down** — every fixure, all three outcome probabilities  
- 🧭 **“How to Read” Guide** — plain‑language metrics, no jargon  

Everything is calculated live from a public dataset. No hard‑coded stats — the dashboard updates if the data changes.

---

## Data Source

The model predictions come from the [**WC2026 Match Probability Baseline Dataset**](https://www.kaggle.com/datasets/) on Kaggle.  
It provides `home_win`, `draw`, and `away_win` probabilities for every group‑stage match, derived from team Elo ratings.

Limitations are acknowledged.

---

## 🛠 Tech Stack
| Purpose | Tool |
|---------|------|
| **Dashboard framework** | [Streamlit](https://streamlit.io) |
| **Data manipulation** | Pandas |
| **Visualisation** | Plotly Express |

---

## 🚀 Run Locally (2 Minutes)

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/world-cup-2026-dashboard.git
cd world-cup-2026-dashboard

# 2. Install dependencies
pip install -r requirements.txt

# 3. Place the dataset
# Download wc_2026_probabilities.csv from Kaggle (or use the raw URL loading method)
# and place it in the project folder.

# 4. Launch
streamlit run app.py
