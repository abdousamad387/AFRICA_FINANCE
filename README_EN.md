# AFRICA FINANCE OBSERVATORY

**Interactive analytical dashboard of African finance (2000-2024)**

*Author: Abdou Samad Faye -- Fullstack Geo Data Scientist*

---

> [Version francaise disponible ici](README.md)

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Context](#2-context)
3. [Justification](#3-justification)
4. [Objectives](#4-objectives)
5. [Data and sources](#5-data-and-sources)
6. [Methodology](#6-methodology)
7. [Technical architecture](#7-technical-architecture)
8. [Results](#8-results)
9. [Discussion](#9-discussion)
10. [Conclusion](#10-conclusion)
11. [Installation and usage](#11-installation-and-usage)
12. [Project structure](#12-project-structure)

---

## 1. Introduction

The **Africa Finance Observatory** project is a comprehensive analytical and visualization system covering 54 African countries over the period 2000-2024. It gathers more than 15,000 structured observations across 12 thematic dimensions (macroeconomics, banking sector, fintech, microfinance, financial markets, crises, etc.) and produces a fully self-contained interactive HTML dashboard, along with a bilingual CLI orchestrator (French/English).

The goal is to provide a decision-making and research tool that combines statistical rigor (parametric and non-parametric tests, regressions, panel analyses) with professional-grade visualization (over 35 interactive charts, animated choropleth maps, treemaps, radar charts).

---

## 2. Context

The African continent comprises 54 economies with heterogeneous development trajectories. Despite average growth exceeding the global average over the past two decades, African financial systems remain fragmented: uneven banking penetration rates (from less than 10% to over 80% depending on the country), limited credit depth, vulnerability to external shocks, and growing reliance on mobile money as a vehicle for financial inclusion.

The data exists -- scattered across IMF, World Bank, AfDB, GSMA, UNCTAD, BIS, and MIX Market databases -- but no public tool synthesizes it within a unified, interactive, and statistically rigorous analytical framework covering the entire continent over a quarter century.

---

## 3. Justification

| Observation | Project Response |
|---|---|
| African financial data is scattered across heterogeneous databases | Unified database of 15,000+ observations, 12 dimensions, standardized Excel format |
| Existing dashboards are static or limited to a subset of countries | Interactive HTML dashboard covering 54 countries, 25 years, 13 thematic tabs |
| Analyses often remain purely descriptive | 10 statistical methods implemented (ANOVA, Kruskal-Wallis, Shapiro-Wilk, Spearman, panel OLS regression) |
| Language barriers limit the audience | Complete i18n system French/English (130+ translation keys) |
| Reproducibility is rarely ensured | Fully scriptable pipeline, CLI with 11 commands, deterministic dashboard generation |

---

## 4. Objectives

**General objective**: Design an interactive digital observatory of African finance combining data collection, processing, advanced statistical analysis, and visualization of financial data from 54 countries over 25 years.

**Specific objectives**:

| # | Objective |
|---|---|
| 1 | Consolidate data from 7 international sources into a structured database of 12 dimensions |
| 2 | Calculate 18 key performance indicators (KPIs) per year and per region |
| 3 | Apply 10 statistical methods (descriptive, inferential, panel) to financial data |
| 4 | Generate a self-contained HTML dashboard with over 35 interactive charts |
| 5 | Produce 13 interactive choropleth maps with a time slider spanning 2000-2024 |
| 6 | Enable comparative analysis by region (5 regions) and by country (54 profiles) |
| 7 | Provide a bilingual CLI tool for analytics pipeline automation |

---

## 5. Data and Sources

### 5.1 Data Sources

| Source | Acronym | Data Provided |
|---|---|---|
| International Monetary Fund | IMF | GDP, inflation, public debt, current account, reserves |
| World Bank | WB | Banking penetration, credit/GDP, HDI, unemployment, urbanization |
| African Development Bank | AfDB | Regional sectoral indicators, country profiles |
| GSMA | GSMA | Mobile money (accounts, transactions, penetration) |
| United Nations Conference on Trade and Development | UNCTAD | Inward/outward FDI, remittances |
| Bank for International Settlements | BIS | Sovereign spreads, policy rates, bonds |
| MIX Market | MIX | Microfinance (clients, portfolio, PAR30, OSS) |

### 5.2 Database Structure

The database `AfricaFinance_Database_2000_2024.xlsx` contains 11 sheets:

| # | Sheet | Observations | Variables | Description |
|---|---|---|---|---|
| 1 | Macroeconomie | 1,274 | 25 | GDP, growth, inflation, debt, unemployment, FDI, HDI |
| 2 | Secteur Bancaire | 1,274 | 26 | Banking penetration, NPL, CAR, ROE, NIM, credit, insurance |
| 3 | Fintech et Mobile Money | 1,274 | 23 | MM accounts, transactions, startups, investments |
| 4 | Marches Financiers | 849 | 21 | Market capitalization, indices, spreads, bonds |
| 5 | Microfinance | 1,274 | 21 | MFIs, portfolio, PAR30, OSS, clients, inclusion |
| 6 | Trimestrielles | 5,099 | 18 | Sub-annual data (GDP, credit, reserves) |
| 7 | Profil Pays | 50 | 21 | Metadata (currency, central bank, coordinates) |
| 8 | Correlations | -- | -- | Pre-computed correlation matrix |
| 9 | Crises | 173 | 14 | Crisis events (type, severity, GDP impact) |
| 10 | Classements | -- | -- | Rankings by indicator |
| 11 | Statistiques | -- | 12 | Regional descriptive statistics |

### 5.3 Geographic Coverage

54 African countries, grouped into 5 regions:

| Region | Countries (examples) |
|---|---|
| Southern Africa | South Africa, Botswana, Mozambique, Zambia, Zimbabwe |
| Central Africa | Cameroon, DRC, Gabon, Congo, Chad |
| North Africa | Morocco, Egypt, Tunisia, Algeria, Libya |
| West Africa | Nigeria, Ghana, Senegal, Cote d'Ivoire, Mali |
| East Africa | Kenya, Ethiopia, Tanzania, Uganda, Rwanda |

---

## 6. Methodology

### 6.1 Data Processing Pipeline

| Step | Operation | Detail |
|---|---|---|
| 1 | Loading | Reading 11 Excel sheets via `pandas.read_excel()` with `openpyxl` engine |
| 2 | Cleaning | Sub-header removal, column renaming, numeric conversion (`pd.to_numeric(..., errors='coerce')`), dropping rows without country/year |
| 3 | Temporal aggregation | Continental series (4 DataFrames), regional series (4 DataFrames), top/bottom 15 rankings for 10 indicators |
| 4 | Cross-sectional aggregation | 18 KPIs for year 2024, regional profiles (3 DataFrames) |
| 5 | Country-level data | Individual time series (macro: 6 variables, banking: 6, fintech: 4) per country |
| 6 | Choropleth data | 25 years x 54 countries x 13 indicators, ISO-3 codes |
| 7 | Radar data | 5 regions x 7 normalized dimensions |
| 8 | Treemap data | 54 countries: GDP, growth, region (hierarchy) |
| 9 | Advanced statistics | 10 methods (cf. section 6.2) |
| 10 | Serialization | JSON payload (732 KB), injection into HTML template |

### 6.2 Statistical Methods

#### 6.2.1 Descriptive Statistics

14 variables analyzed on the 2024 cross-section.

| Metric | Formula |
|---|---|
| Mean | $\bar{x} = \frac{1}{n}\sum_{i=1}^{n} x_i$ |
| Median | Central value of the ordered distribution |
| Standard deviation | $s = \sqrt{\frac{1}{n-1}\sum_{i=1}^{n}(x_i - \bar{x})^2}$ |
| Coefficient of variation | $CV = \frac{s}{\bar{x}} \times 100$ |
| Skewness | $g_1 = \frac{n}{(n-1)(n-2)} \sum \left(\frac{x_i - \bar{x}}{s}\right)^3$ |
| Kurtosis | $g_2 = \frac{n(n+1)}{(n-1)(n-2)(n-3)} \sum \left(\frac{x_i - \bar{x}}{s}\right)^4 - \frac{3(n-1)^2}{(n-2)(n-3)}$ |
| Quartiles | $Q_1$ (25th percentile), $Q_3$ (75th percentile) |

**Variables analyzed**: PIB_Mrd, Croissance_PIB, PIB_hab, Inflation, Dette_publique, Chomage, Bancarisation, NPL, CAR, ROE, Credit_PIB, Pop_MM, Score_inclusion, FDI_entrants.

#### 6.2.2 Simple Linear Regression (OLS)

Implementation via `scipy.stats.linregress()`.

$$\hat{y} = \beta_0 + \beta_1 x$$

$$R^2 = 1 - \frac{SS_{res}}{SS_{tot}} = 1 - \frac{\sum(y_i - \hat{y}_i)^2}{\sum(y_i - \bar{y})^2}$$

| # | Dependent Variable | Independent Variable | Hypothesis Tested |
|---|---|---|---|
| 1 | Banking penetration | GDP per capita | Income promotes banking access |
| 2 | Credit/GDP | GDP per capita | Income stimulates credit |
| 3 | Inclusion score | Banking penetration | Banking penetration improves inclusion |
| 4 | Banking penetration | Mobile Money (% pop.) | Mobile money complements banking |
| 5 | Growth | Inflation | Inflation hinders growth |
| 6 | Growth | NPL | Bad loans penalize growth |
| 7 | Growth | Public debt | Indebtedness affects growth |
| 8 | Growth | Inward FDI | FDI stimulates growth |
| 9 | Banking penetration | Urbanization | Urbanization facilitates banking access |
| 10 | Banking penetration | HDI | Human development promotes banking |

Significance threshold: $p < 0.05$.

#### 6.2.3 One-Way ANOVA

Mean comparison test across the 5 African regions.

$$F = \frac{MS_{between}}{MS_{within}} = \frac{\sum n_j(\bar{x}_j - \bar{x})^2 / (k-1)}{\sum\sum(x_{ij} - \bar{x}_j)^2 / (N-k)}$$

Implementation via `scipy.stats.f_oneway()`.

| Variable Tested | Description |
|---|---|
| Croissance_PIB | Do growth rates differ between regions? |
| Bancarisation | Do banking penetration levels differ between regions? |
| NPL | Do non-performing loan ratios differ between regions? |
| Inflation | Do inflation levels differ between regions? |
| Credit_PIB | Does credit depth differ between regions? |
| Pop_MM | Does mobile money penetration differ between regions? |
| Score_inclusion | Does financial inclusion differ between regions? |
| PIB_hab | Do GDP per capita levels differ between regions? |

#### 6.2.4 Shapiro-Wilk Test

Normality test applied to the 14 cross-sectional variables.

$$W = \frac{\left(\sum a_i x_{(i)}\right)^2}{\sum (x_i - \bar{x})^2}$$

Implementation via `scipy.stats.shapiro()`. Null hypothesis: the distribution follows a normal law ($p > 0.05$).

#### 6.2.5 Kruskal-Wallis Test

Non-parametric alternative to ANOVA, applied to the same 8 variables.

$$H = \frac{12}{N(N+1)} \sum_{j=1}^{k} \frac{R_j^2}{n_j} - 3(N+1)$$

Implementation via `scipy.stats.kruskal()`.

#### 6.2.6 Spearman Correlation

Rank correlation matrix for 9 variables.

$$\rho = 1 - \frac{6\sum d_i^2}{n(n^2-1)}$$

Implementation via `scipy.stats.spearmanr()`. Variables: PIB_hab, Bancarisation, NPL, Inflation, Credit_PIB, Pop_MM, Croissance_PIB, IDH, Score_inclusion.

#### 6.2.7 Temporal Trend Analysis

Spearman correlation between years and continental mean values, for 8 variables:

| Variable | Expected Trend |
|---|---|
| PIB_Mrd | Structural increase |
| Croissance_PIB | Fluctuating with trend |
| Inflation | Downward trend |
| Dette_publique | Increase post-2010 |
| Bancarisation | Gradual increase |
| NPL | Expected decrease |
| Pop_MM | Sharp increase |
| Score_inclusion | Gradual increase |

#### 6.2.8 Outlier Detection (IQR Method)

$$\text{Lower bound} = Q_1 - 1.5 \times IQR \quad ; \quad \text{Upper bound} = Q_3 + 1.5 \times IQR$$

$$IQR = Q_3 - Q_1$$

Applied to the 14 descriptive variables. Each outlier is identified with the corresponding country and value.

#### 6.2.9 Panel Regression (Pooled OLS)

Dependent variable: GDP Growth.

Independent variables (6 regressors):

| Variable | Justification |
|---|---|
| Inflation | Potentially negative effect on growth |
| Dette_publique | Over-indebtedness hypothesis |
| FDI_entrants | Expected catalytic effect |
| Chomage | Labor market dysfunction |
| Bancarisation | Financial inclusion as a driver |
| Credit_PIB | Financial depth |

Ordinary least squares estimation:

$$\hat{\beta} = (X^T X)^{-1} X^T y$$

Standard errors:

$$SE(\hat{\beta}_j) = \sqrt{MSE \cdot [(X^T X)^{-1}]_{jj}}$$

t-statistic:

$$t_j = \frac{\hat{\beta}_j}{SE(\hat{\beta}_j)}$$

p-values computed via `scipy.stats.t.cdf()`.

$R^2$ and adjusted $R^2$:

$$R^2_{adj} = 1 - \frac{(1-R^2)(n-1)}{n-k-1}$$

Implementation via `numpy.linalg.lstsq()`.

#### 6.2.10 Pearson Correlation Matrix

Extracted from the pre-computed sheet in the Excel file. 11 variables.

$$r = \frac{\sum(x_i - \bar{x})(y_i - \bar{y})}{\sqrt{\sum(x_i - \bar{x})^2 \sum(y_i - \bar{y})^2}}$$

### 6.3 Tools and Technologies

| Component | Technology | Version | Role |
|---|---|---|---|
| Main language | Python | 3.14 | Processing, statistics, generation |
| Data manipulation | pandas | -- | Loading, cleaning, aggregation |
| Numerical computing | NumPy | -- | Matrix algebra, panel OLS |
| Statistical tests | SciPy (scipy.stats) | -- | Regressions, ANOVA, Shapiro-Wilk, Kruskal-Wallis, Spearman |
| Excel reading | openpyxl | -- | .xlsx file reading engine |
| Excel export | xlsxwriter | -- | Multi-sheet .xlsx export |
| Visualization | Plotly.js | 2.35.0 | 35+ client-side interactive charts |
| Typography | Google Fonts | -- | Inter (UI), JetBrains Mono (monospace) |
| Layout | CSS3 | -- | Glassmorphism, CSS Grid, animations, responsive |
| Theme | Dark mode | -- | 30+ custom CSS variables |
| Internationalization | JavaScript (client) | -- | 130+ keys, FR/EN toggle |
| Local server | http.server (Python) | -- | Port 8888, automatic browser launch |

---

## 7. Technical Architecture

### 7.1 Project Structure

| File | Lines | Size | Description |
|---|---|---|---|
| `build_dashboard.py` | ~2,830 | ~130 KB | ETL + statistics + HTML generation |
| `main.py` | ~830 | ~38 KB | Bilingual CLI orchestrator |
| `AfricaFinance_Dashboard.html` | -- | ~0.8 MB | Generated dashboard (self-contained, embedded JSON data) |
| `AfricaFinance_Database_2000_2024.xlsx` | -- | ~1.2 MB | Source database |
| `.gitignore` | 4 | -- | Exclusions (.venv, __pycache__, temp files) |

### 7.2 Generation Pipeline

```
Excel (.xlsx)
    |
    v
[build_dashboard.py]
    |-- 1. Read 11 sheets
    |-- 2. Clean and type cast
    |-- 3. Compute aggregates (KPIs, time series, rankings)
    |-- 4. Build cartographic data (choropleths, treemap, radar)
    |-- 5. Compute advanced statistics (10 methods)
    |-- 6. JSON serialization (732 KB)
    |-- 7. Inject into HTML template
    v
Self-contained HTML Dashboard (0.8 MB)
    |-- CSS: dark theme, glassmorphism, 5 responsive breakpoints
    |-- JS: Plotly.js 2.35.0, i18n FR/EN, 13 renderers
    |-- Data: embedded JSON (no external requests)
```

### 7.3 Dashboard Tabs

| # | Tab | Content | Charts |
|---|---|---|---|
| 1 | Overview | KPIs, GDP/banking scatter, GDP treemap, histogram | 4 |
| 2 | Choropleth Maps | 2 maps + year slider + distribution histogram | 3 |
| 3 | Macroeconomics | Total GDP, growth/inflation, FDI/remittances, debt/unemployment, regional growth | 5 |
| 4 | Banking Sector | Banking penetration, NPL/CAR, ROE/NIM, credit/GDP, regional evolution, 5-region radar | 6 |
| 5 | Fintech and Mobile Money | Accounts/transactions, startups/investments, regional evolution, smartphone/digital payments | 4 |
| 6 | Financial Markets | Capitalization, sovereign spreads, stock exchange ranking | 3 |
| 7 | Microfinance | PAR30/OSS, clients/women, portfolio, inclusion score | 4 |
| 8 | Crises | Timeline, impact (scatter), detailed table | 3 |
| 9 | Rankings | Top 15 / Bottom 15 for 10 indicators (selector) | 2 |
| 10 | Correlations | Pearson correlation matrix (heatmap) | 1 |
| 11 | Country Detail | 4 charts per country (selector: 54 countries) | 4 |
| 12 | Regional Comparison | Regional GDP, banking indicators, fintech, temporal NPL | 4 |
| 13 | Advanced Statistics | Descriptive, normality, distributions, regressions, panel OLS, ANOVA, Spearman, trends, outliers | 9+ |

### 7.4 Computed KPIs (Year 2024)

| # | KPI | Unit |
|---|---|---|
| 1 | Total African GDP | Billion USD |
| 2 | Average GDP growth | % |
| 3 | Average inflation | % |
| 4 | Average banking penetration | % |
| 5 | Average NPL ratio | % |
| 6 | Average CAR ratio (Basel III) | % |
| 7 | Average ROE | % |
| 8 | Average NIM | % |
| 9 | Mobile Money accounts (total) | Millions |
| 10 | Number of fintech startups | Units |
| 11 | Total inward FDI | Billion USD |
| 12 | Average public debt | % GDP |
| 13 | Number of countries covered | -- |
| 14 | Number of years | -- |
| 15 | Average credit/GDP | % |
| 16 | Average inclusion score | 0-10 |
| 17 | Mobile Money transactions (total) | Billion USD |
| 18 | Population with Mobile Money | % |

### 7.5 Cartographic Indicators (Choropleths)

| # | Indicator | Color Scale | Range |
|---|---|---|---|
| 1 | GDP per capita ($) | Progressive green | 0 -- 8,000 |
| 2 | GDP growth (%) | Red-yellow-green | -5 -- 12 |
| 3 | Inflation (%) | Green-yellow-red | 0 -- 30 |
| 4 | Debt/GDP (%) | Green-yellow-red | 0 -- 120 |
| 5 | Banking penetration (%) | Progressive purple | 0 -- 100 |
| 6 | NPL (%) | Green-yellow-red | 0 -- 25 |
| 7 | CAR (%) | Red-yellow-green | 5 -- 25 |
| 8 | Credit/GDP (%) | Progressive blue | 0 -- 100 |
| 9 | Mobile Money (% pop.) | Progressive purple | 0 -- 90 |
| 10 | Inclusion score (0-10) | Progressive green | 0 -- 10 |
| 11 | FDI ($Bn) | Progressive blue | 0 -- 15 |
| 12 | Unemployment (%) | Green-yellow-red | 0 -- 35 |
| 13 | PAR30 (%) | Green-yellow-red | 0 -- 20 |

---

## 8. Results

### 8.1 Coverage and Completeness

| Metric | Value |
|---|---|
| Countries covered | 54 |
| Period | 2000-2024 (25 years) |
| Total observations | 15,000+ |
| Thematic dimensions | 12 |
| Variables analyzed | 170+ |
| Interactive charts generated | 35+ |
| Choropleth maps | 13 indicators x 25 years |
| Statistical tests performed | 10 methods, 50+ individual tests |

### 8.2 Synthetic Indicators (Typical Values, Year 2024)

| Indicator | Typical Value | Observation |
|---|---|---|
| Total African GDP | ~3,000 Bn USD | Sustained growth since 2000 |
| Average banking penetration | ~35-45% | Strong regional heterogeneity |
| Mobile Money penetration | ~30-40% | Exponential growth post-2010 |
| Average NPL | ~8-12% | Above international standards (5%) |
| Average CAR | ~15-18% | Compliant with Basel III minimum (10.5%) |
| Average inclusion score | ~4-5 / 10 | Progress but remains insufficient |

### 8.3 Significant Regressions (Typical Examples)

| Model | Expected R2 | Significance | Interpretation |
|---|---|---|---|
| GDP/capita -> Banking | High | p < 0.05 | Income is a major determinant of banking penetration |
| Mobile Money -> Banking | Medium | p < 0.05 | Mobile money / bank complementarity |
| HDI -> Banking | High | p < 0.05 | Human development promotes financial access |
| Debt -> Growth | Low to medium | Variable | Non-linear relationship, possible threshold effect |

### 8.4 Regional Comparisons (ANOVA)

ANOVA and Kruskal-Wallis tests reveal significant differences between the 5 African regions for the majority of financial indicators, confirming the structural heterogeneity of the continent.

---

## 9. Discussion

### 9.1 Contributions

| Contribution | Detail |
|---|---|
| Uniqueness | First interactive observatory covering 54 countries, 25 years, 12 dimensions in a single HTML file |
| Statistical rigor | 10 complementary methods (parametric and non-parametric) |
| Reproducibility | Fully automated pipeline via CLI |
| Accessibility | Bilingual interface, responsive, exportable (PNG, SVG, CSV, JSON) |
| Autonomy | No server dependency: the dashboard is a 0.8 MB HTML file |

### 9.2 Limitations

| Limitation | Explanation |
|---|---|
| Missing data | Some countries/years have gaps in original sources |
| Simplified panel regression | Pooled OLS without fixed or random effects |
| No post-hoc tests | ANOVA does not specify which region pairs differ |
| Causality | Regressions measure associations, not causal relationships |
| Updates | Data requires manual annual updates |

### 9.3 Future Directions

| Perspective | Description |
|---|---|
| Panel fixed effects | Integration of fixed and random effects models (Hausman test) |
| Post-hoc tests | Addition of Tukey HSD tests after significant ANOVA |
| Machine Learning | Clustering (K-Means), banking penetration prediction |
| Real-time data | Connection to APIs (IMF, World Bank) for automatic updates |
| Web deployment | Deployment on GitHub Pages or cloud server |

---

## 10. Conclusion

The **Africa Finance Observatory** project demonstrates that it is possible to synthesize a quarter century of African financial data into a single, rigorous, and accessible analytical tool. By combining 12 thematic dimensions, 10 statistical methods, and over 35 interactive visualizations in a self-contained 0.8 MB HTML file, this observatory offers researchers, decision-makers, and practitioners an instrument for understanding African finance that is unprecedented in its coverage and interactivity.

The chosen architecture -- a Python pipeline generating a static dashboard with embedded data -- ensures reproducibility, portability, and independence from any server infrastructure.

---

## 11. Installation and Usage

### 11.1 Prerequisites

| Component | Minimum Version |
|---|---|
| Python | 3.9+ |
| pip | 20+ |

### 11.2 Dependency Installation

```bash
pip install pandas openpyxl numpy scipy xlsxwriter
```

### 11.3 CLI Commands

```bash
# Generate the dashboard
python main.py --build

# Generate and start local server
python main.py --serve

# Display statistics in console
python main.py --stats

# Export to CSV
python main.py --export-csv

# Export to Excel
python main.py --export-excel

# Full pipeline
python main.py --all

# Check dependencies
python main.py --check

# Install missing packages
python main.py --install

# Set language (en/fr)
python main.py --lang en --build

# Interactive menu
python main.py
```

### 11.4 Direct Dashboard Generation

```bash
python build_dashboard.py
```

The `AfricaFinance_Dashboard.html` file is generated in the current directory. Open in a modern browser (Chrome, Firefox, Edge).

---

## 12. Project Structure

```
AFRICA_FINANCE/
|-- build_dashboard.py          # ETL + statistics + HTML generation (~2,830 lines)
|-- main.py                     # Bilingual CLI orchestrator (~830 lines)
|-- AfricaFinance_Dashboard.html        # Generated dashboard (self-contained, ~0.8 MB)
|-- AfricaFinance_Database_2000_2024.xlsx   # Source database (~1.2 MB)
|-- AfricaFinance_Senior_Report.docx    # Detailed report (Word)
|-- AfricaFinance_Senior_Report.pdf     # Detailed report (PDF)
|-- README.md                   # Documentation (French)
|-- README_EN.md                # Documentation (English)
|-- .gitignore                  # Git exclusions
```

---

*Abdou Samad Faye -- Fullstack Geo Data Scientist*
