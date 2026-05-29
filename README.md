# Private Equity as a Catalyst for Economic Diversification in MENA & the GCC

An interactive dashboard for the IBR mid-review study by **Kruthivas Mahesh Tambralli (MS25GF030)**, S P Jain School of Global Management. It explores how private equity drives non-oil economic diversification across the GCC, using a firm-level cross-section and a six-country panel.

## 🚀 Live demo
Deploy your own copy in minutes (see below). Once deployed, the URL looks like
`https://<your-app-name>.streamlit.app`.

## 📁 Files
| File | What it is |
|------|------------|
| `app.py` | The Streamlit dashboard |
| `pe_firms.csv` | **Dataset 1** — 30 PE firms (cross-section). One row per firm. |
| `pe_country_panel.csv` | **Dataset 2** — 6 countries × 11 years (2015–2025), tidy/long format. |
| `pe_deal_value_wide.csv` | Deal value table in wide form (country × year) for quick plotting. |
| `requirements.txt` | Python dependencies for Streamlit Cloud. |

## 🖥️ Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```
Then open the URL it prints (usually http://localhost:8501).

## ☁️ Deploy on Streamlit Community Cloud (streamlit.io)
1. Create a **public GitHub repository** and push all files in this folder to it:
   ```bash
   git init
   git add .
   git commit -m "PE MENA-GCC dashboard"
   git branch -M main
   git remote add origin https://github.com/<your-username>/<your-repo>.git
   git push -u origin main
   ```
2. Go to **https://share.streamlit.io** (or streamlit.io → "Deploy") and sign in with GitHub.
3. Click **New app**, pick your repo, set **branch = `main`** and **main file path = `app.py`**.
4. Click **Deploy**. Streamlit installs `requirements.txt` automatically and builds the app.

That's it — every push to `main` redeploys the app.

## 📊 Data dictionary — `pe_firms.csv`
| Column | Meaning |
|--------|---------|
| `firm_name` | PE / SWF / VC firm name |
| `country` | Domicile country (UAE, Saudi Arabia, Qatar, Kuwait, Bahrain, Oman) |
| `firm_type` | Buyout/PE, Growth Equity, Venture Capital, Family Office, Asset Manager, Sovereign Wealth Fund |
| `difc_adgm` | 1 if domiciled in DIFC / ADGM, else 0 |
| `post_2015_vintage` | 1 if a post-2015 vintage fund |
| `aum_usd_m` | Assets under management (USD millions) |
| `ln_aum` | Natural log of AUM (used in regressions) |
| `policy_reform_score` | Policy / regulatory reform alignment (0–10) |
| `sectoral_focus_score` | Strength of non-oil sectoral targeting (0–10) |
| `active_non_oil_portfolio_cos` | Count of active non-oil portfolio companies |
| `cumulative_exits` | Cumulative PE exits (IPO, trade sale, secondary) |
| `non_oil_deal_share_pct` | Share of deals in non-oil sectors (%) — **DV2** |
| `non_oil_gdp_contribution_usd_m` | Estimated non-oil GDP contribution (USD M) — **DV1** |

## 📊 Data dictionary — `pe_country_panel.csv`
| Column | Meaning |
|--------|---------|
| `country` | GCC country |
| `year` | 2015–2025 (2025 = estimate) |
| `pe_deal_value_usd_m` | Annual PE deal value (USD M) |
| `oil_price_usd_bbl` | Avg. Brent oil price (USD/barrel) — control variable |
| `post_reform_dummy` | 1 if year ≥ 2017 (post-reform window) |
| `non_oil_gdp_growth_pct` | Non-oil GDP growth (%) — note the 2020 COVID break |

## 🔍 What the dashboard shows
- **Market Trends** — deal-value growth by country, oil-price vs non-oil growth, cumulative totals.
- **The Decisive Lever (H5)** — the near-perfect link (r ≈ 0.99) between sectoral focus and non-oil deal share.
- **Firm Explorer** — interactive scatter of any two variables + a filterable, downloadable data table.
- **Correlations** — full firm-level correlation matrix.

Use the **sidebar** to filter by country, firm type, DIFC/ADGM domicile, and to exclude sovereign-fund outliers.

## ⚠️ Note on the data
The firm-level rows are constructed so their **summary statistics and key relationships reproduce the figures reported in the study** (e.g. mean non-oil deal share ≈ 78%, sector-focus ↔ deal-share r ≈ 0.99, ln(AUM) → non-oil GDP elasticity ≈ 0.50). Named sovereign funds (ADIA, PIF, KIA, QIA) anchor the known large outliers. Replace `pe_firms.csv` with your own underlying firm data when available — the dashboard will work unchanged as long as the column names match the data dictionary above.
