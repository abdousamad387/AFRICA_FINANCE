#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    AFRICA FINANCE OBSERVATORY — MAIN                       ║
║                                                                            ║
║  Main entry point for the African financial analysis project.              ║
║  54 countries · 2000-2024 · 12 dimensions · 15,000+ observations           ║
║                                                                            ║
║  Author  : Abdou Samad Faye                                                ║
║  Date    : April 2026                                                      ║
║  Sources : IMF, World Bank, AfDB, GSMA, UNCTAD, BIS, MIX Market           ║
╚══════════════════════════════════════════════════════════════════════════════╝

Usage:
    python main.py                   → Interactive menu
    python main.py --build           → Build the dashboard
    python main.py --serve           → Build + serve (localhost)
    python main.py --stats           → Display statistics in console
    python main.py --export-csv      → Export all data to CSV
    python main.py --export-excel    → Export analyses to Excel
    python main.py --check           → Check dependencies and data
    python main.py --info            → Database information
    python main.py --all             → Run everything (build + export + serve)
    python main.py --lang fr         → Run in French
"""

import sys
import os
import time
import argparse
import subprocess
import importlib
from pathlib import Path

# ─── CONFIGURATION ────────────────────────────────────────────────────────────

BASE_DIR = Path(__file__).parent
EXCEL_FILE = BASE_DIR / "AfricaFinance_Database_2000_2024.xlsx"
DASHBOARD_FILE = BASE_DIR / "AfricaFinance_Dashboard.html"
BUILD_SCRIPT = BASE_DIR / "build_dashboard.py"
EXPORT_DIR = BASE_DIR / "exports"
DEFAULT_PORT = 8888

REQUIRED_PACKAGES = {
    "pandas": "pandas",
    "openpyxl": "openpyxl",
    "numpy": "numpy",
    "scipy": "scipy",
}

OPTIONAL_PACKAGES = {
    "sklearn": "scikit-learn",
    "statsmodels": "statsmodels",
    "xlsxwriter": "xlsxwriter",
}

# ─── INTERNATIONALIZATION ────────────────────────────────────────────────────

LANG = "en"  # Default language — "en" or "fr"

TEXTS = {
    # ── Banner ──
    "banner_sub1": {
        "en": "54 Countries · 2000-2024 · 12 Dimensions",
        "fr": "54 Pays · 2000-2024 · 12 Dimensions",
    },
    "banner_sub2": {
        "en": "15,000+ Observations · Complete Database",
        "fr": "15 000+ Observations · Base de Données Complète",
    },
    # ── Dependencies ──
    "step_check_deps": {
        "en": "🔍 Checking dependencies",
        "fr": "🔍 Vérification des dépendances",
    },
    "missing_required": {
        "en": "MISSING (required)",
        "fr": "MANQUANT (requis)",
    },
    "optional_tag": {
        "en": "optional",
        "fr": "optionnel",
    },
    "not_installed": {
        "en": "not installed",
        "fr": "non installé",
    },
    # ── Data check ──
    "step_check_data": {
        "en": "📂 Checking data files",
        "fr": "📂 Vérification des données",
    },
    "file_not_found": {
        "en": "File not found",
        "fr": "Fichier introuvable",
    },
    "database_label": {
        "en": "Database",
        "fr": "Base de données",
    },
    "sheets_detected": {
        "en": "Sheets detected",
        "fr": "Feuilles détectées",
    },
    "excel_read_error": {
        "en": "Excel read error",
        "fr": "Erreur lecture Excel",
    },
    # ── Install ──
    "step_install": {
        "en": "📦 Installing missing packages",
        "fr": "📦 Installation des packages manquants",
    },
    "all_installed": {
        "en": "All packages are already installed.",
        "fr": "Tous les packages sont déjà installés.",
    },
    "packages_to_install": {
        "en": "Packages to install",
        "fr": "Packages à installer",
    },
    "packages_installed_ok": {
        "en": "packages installed successfully.",
        "fr": "packages installés avec succès.",
    },
    "install_error": {
        "en": "Installation error",
        "fr": "Erreur d'installation",
    },
    # ── Data loading ──
    "step_load_data": {
        "en": "📦 Loading the database",
        "fr": "📦 Chargement de la base de données",
    },
    "sheets_loaded_in": {
        "en": "sheets loaded in",
        "fr": "feuilles chargées en",
    },
    "sheet_not_found": {
        "en": "Sheet not found",
        "fr": "Feuille introuvable",
    },
    "loading_done_in": {
        "en": "Loading completed in",
        "fr": "Chargement terminé en",
    },
    "countries": {
        "en": "countries",
        "fr": "pays",
    },
    "total_rows": {
        "en": "total rows",
        "fr": "lignes totales",
    },
    # ── Info ──
    "step_info": {
        "en": "📋 Database information",
        "fr": "📋 Informations sur la base de données",
    },
    "info_database": {"en": "Database", "fr": "Base de données"},
    "info_size": {"en": "Size", "fr": "Taille"},
    "info_period": {"en": "Period", "fr": "Période"},
    "info_years": {"en": "years", "fr": "années"},
    "info_countries": {"en": "Countries", "fr": "Pays"},
    "info_regions": {"en": "Regions", "fr": "Régions"},
    "info_regions_label": {"en": "Regions", "fr": "Régions"},
    "info_country_word": {"en": "countries", "fr": "pays"},
    "info_dataframes": {"en": "DataFrames", "fr": "DataFrames"},
    "info_rows": {"en": "rows", "fr": "lignes"},
    "info_cols": {"en": "cols", "fr": "colonnes"},
    "info_country_list": {"en": "List of 54 countries", "fr": "Liste des 54 pays"},
    # ── Stats ──
    "step_stats": {
        "en": "📊 Descriptive statistics (2024)",
        "fr": "📊 Statistiques descriptives (2024)",
    },
    "macro_title": {"en": "MACROECONOMICS", "fr": "MACROÉCONOMIE"},
    "total_african_gdp": {"en": "Total African GDP", "fr": "PIB total africain"},
    "avg_gdp_growth": {"en": "Avg GDP growth", "fr": "Croissance PIB moy."},
    "avg_gdp_capita": {"en": "Avg GDP/capita", "fr": "PIB/habitant moyen"},
    "avg_inflation": {"en": "Avg inflation", "fr": "Inflation moyenne"},
    "avg_public_debt": {"en": "Avg public debt", "fr": "Dette publique moy."},
    "avg_unemployment": {"en": "Avg unemployment", "fr": "Chômage moyen"},
    "total_fdi_inflows": {"en": "Total FDI inflows", "fr": "FDI entrants total"},
    "total_remittances": {"en": "Total remittances", "fr": "Envois de fonds total"},
    "banking_title": {"en": "BANKING SECTOR", "fr": "SECTEUR BANCAIRE"},
    "avg_banking_rate": {"en": "Avg banking rate", "fr": "Taux bancarisation moy"},
    "avg_npl": {"en": "Avg NPL ratio", "fr": "NPL ratio moyen"},
    "avg_car": {"en": "Avg CAR (Basel III)", "fr": "CAR moyen (Bâle III)"},
    "avg_roe": {"en": "Avg ROE", "fr": "ROE moyen"},
    "avg_nim": {"en": "Avg NIM", "fr": "NIM moyen"},
    "avg_credit_gdp": {"en": "Avg credit/GDP", "fr": "Crédit/PIB moyen"},
    "fintech_title": {"en": "FINTECH & MOBILE MONEY", "fr": "FINTECH & MOBILE MONEY"},
    "total_mm_accounts": {"en": "Total M-Money accounts", "fr": "Comptes M-Money total"},
    "mm_transactions": {"en": "M-Money transactions", "fr": "Transactions M-Money"},
    "avg_mm_pop": {"en": "Avg pop. with M-Money", "fr": "Pop. avec M-Money moy."},
    "total_fintech_startups": {"en": "Total fintech startups", "fr": "Startups fintech total"},
    "microfinance_title": {"en": "MICROFINANCE", "fr": "MICROFINANCE"},
    "avg_par30": {"en": "Avg PAR30", "fr": "PAR30 moyen"},
    "avg_oss": {"en": "Avg OSS", "fr": "OSS moyen"},
    "avg_inclusion": {"en": "Avg inclusion score", "fr": "Score inclusion moy."},
    "total_clients": {"en": "Total clients (000)", "fr": "Clients total (000)"},
    "avg_women_pct": {"en": "Avg % women", "fr": "% femmes moyen"},
    "step_stat_tests": {
        "en": "🧪 Statistical tests (cross-section 2024)",
        "fr": "🧪 Tests statistiques (coupe transversale 2024)",
    },
    "linear_regressions": {"en": "Linear regressions", "fr": "Régressions linéaires"},
    "reg_gdp_banking": {
        "en": "GDP/cap → Banking rate",
        "fr": "PIB/hab → Bancarisation",
    },
    "reg_infl_growth": {
        "en": "Inflation → Growth",
        "fr": "Inflation → Croissance",
    },
    "reg_gdp_npl": {
        "en": "GDP/cap → NPL",
        "fr": "PIB/hab → NPL",
    },
    "anova_by_region": {"en": "ANOVA by region", "fr": "ANOVA par région"},
    # ── Dashboard build ──
    "step_build": {
        "en": "🔨 Building the interactive dashboard",
        "fr": "🔨 Construction du dashboard interactif",
    },
    "script_not_found": {
        "en": "Script not found",
        "fr": "Script introuvable",
    },
    "build_error": {
        "en": "Error during build:",
        "fr": "Erreur lors de la construction :",
    },
    "dashboard_generated": {
        "en": "Dashboard generated in",
        "fr": "Dashboard généré en",
    },
    "html_not_created": {
        "en": "The HTML file was not created.",
        "fr": "Le fichier HTML n'a pas été créé.",
    },
    # ── Server ──
    "step_serve": {
        "en": "🌐 Starting local server (port {port})",
        "fr": "🌐 Lancement du serveur local (port {port})",
    },
    "dashboard_not_found": {
        "en": "Dashboard not found. Building now...",
        "fr": "Dashboard non trouvé. Construction en cours...",
    },
    "dashboard_at": {
        "en": "Dashboard available at",
        "fr": "Dashboard accessible à",
    },
    "press_ctrl_c": {
        "en": "Press Ctrl+C to stop the server.",
        "fr": "Appuyez sur Ctrl+C pour arrêter le serveur.",
    },
    "port_in_use": {
        "en": "Port {port} already in use. Trying {port1}...",
        "fr": "Port {port} déjà utilisé. Tentative sur {port1}...",
    },
    "server_error": {
        "en": "Server error",
        "fr": "Erreur serveur",
    },
    "server_stopped": {
        "en": "Server stopped.",
        "fr": "Serveur arrêté.",
    },
    # ── Export CSV ──
    "step_csv": {"en": "📤 CSV Export", "fr": "📤 Export CSV"},
    "rows_word": {"en": "rows", "fr": "lignes"},
    "exported_to": {"en": "Exported to", "fr": "Exporté dans"},
    # ── Export Excel ──
    "step_excel": {
        "en": "📤 Excel Export (analyses)",
        "fr": "📤 Export Excel (analyses)",
    },
    "xlsxwriter_missing": {
        "en": "xlsxwriter not installed. Installing...",
        "fr": "xlsxwriter non installé. Installation en cours...",
    },
    "raw_data_exported": {
        "en": "Raw data exported (8 sheets)",
        "fr": "Données brutes exportées (8 feuilles)",
    },
    "desc_stats_label": {
        "en": "Descriptive statistics",
        "fr": "Statistiques descriptives",
    },
    "variables_word": {"en": "variables", "fr": "variables"},
    "pearson_corr": {
        "en": "Pearson correlation matrix",
        "fr": "Matrice de corrélation Pearson",
    },
    "continental_ts": {
        "en": "Continental time series",
        "fr": "Séries temporelles continentales",
    },
    "rankings_top15": {
        "en": "Rankings Top 15 (2024)",
        "fr": "Rankings Top 15 (2024)",
    },
    "file_exported": {
        "en": "File exported",
        "fr": "Fichier exporté",
    },
    # ── Menu ──
    "menu_title": {"en": "MAIN MENU", "fr": "MENU PRINCIPAL"},
    "menu_1": {"en": "Build the dashboard", "fr": "Construire le dashboard"},
    "menu_2": {"en": "Build + Launch server", "fr": "Construire + Lancer le serveur"},
    "menu_3": {"en": "Statistics (console)", "fr": "Statistiques (console)"},
    "menu_4": {"en": "Database information", "fr": "Informations base de données"},
    "menu_5": {"en": "Export to CSV", "fr": "Exporter en CSV"},
    "menu_6": {"en": "Export to Excel (analyses)", "fr": "Exporter en Excel (analyses)"},
    "menu_7": {"en": "Check dependencies", "fr": "Vérifier dépendances"},
    "menu_8": {"en": "Install missing packages", "fr": "Installer packages manquants"},
    "menu_9": {"en": "Run everything", "fr": "Tout exécuter"},
    "menu_0": {"en": "Quit", "fr": "Quitter"},
    "menu_lang": {
        "en": "Switch to French  [FR]",
        "fr": "Switch to English  [EN]",
    },
    "choice_prompt": {"en": "Choice", "fr": "Choix"},
    "goodbye": {"en": "Goodbye.", "fr": "Au revoir."},
    "invalid_choice": {
        "en": "Invalid choice. Type a number between 0 and L.",
        "fr": "Choix invalide. Tapez un numéro entre 0 et L.",
    },
    "lang_switched": {
        "en": "Language switched to English.",
        "fr": "Langue basculée en français.",
    },
    # ── Run all ──
    "step_run_all": {"en": "🚀 Full execution", "fr": "🚀 Exécution complète"},
    "auto_install_attempt": {
        "en": "Attempting automatic installation...",
        "fr": "Tentative d'installation automatique...",
    },
    "cannot_continue": {
        "en": "Cannot continue without the data file.",
        "fr": "Impossible de continuer sans le fichier de données.",
    },
    "pipeline_done": {
        "en": "Pipeline completed in",
        "fr": "Pipeline terminé en",
    },
    # ── Argparse ──
    "arg_desc": {
        "en": "🌍 Africa Finance Observatory — Financial analysis pipeline",
        "fr": "🌍 Africa Finance Observatory — Pipeline d'analyse financière",
    },
    "arg_build": {"en": "Build the HTML dashboard", "fr": "Construire le dashboard HTML"},
    "arg_serve": {"en": "Build + launch the server", "fr": "Construire + lancer le serveur"},
    "arg_stats": {"en": "Display statistics", "fr": "Afficher les statistiques"},
    "arg_info": {"en": "Database information", "fr": "Informations sur la base"},
    "arg_csv": {"en": "Export to CSV", "fr": "Exporter en CSV"},
    "arg_excel": {"en": "Export to Excel", "fr": "Exporter en Excel"},
    "arg_check": {"en": "Check dependencies", "fr": "Vérifier les dépendances"},
    "arg_install": {"en": "Install missing packages", "fr": "Installer les packages manquants"},
    "arg_all": {"en": "Full pipeline", "fr": "Pipeline complet"},
}

def t(key, **kwargs):
    """Get translated text for the current language."""
    entry = TEXTS.get(key, {})
    text = entry.get(LANG, entry.get("en", f"[{key}]"))
    if kwargs:
        text = text.format(**kwargs)
    return text

def set_lang(lang_code):
    """Set the active language."""
    global LANG
    LANG = lang_code if lang_code in ("en", "fr") else "en"

# ─── TERMINAL COLORS ─────────────────────────────────────────────────────────

class C:
    """ANSI color codes for terminal output."""
    RESET  = "\033[0m"
    BOLD   = "\033[1m"
    DIM    = "\033[2m"
    GREEN  = "\033[92m"
    RED    = "\033[91m"
    YELLOW = "\033[93m"
    BLUE   = "\033[94m"
    CYAN   = "\033[96m"
    MAGENTA= "\033[95m"
    WHITE  = "\033[97m"
    BG_GREEN = "\033[42m"
    BG_RED   = "\033[41m"
    BG_BLUE  = "\033[44m"

def ok(msg):     print(f"  {C.GREEN}✓{C.RESET} {msg}")
def fail(msg):   print(f"  {C.RED}✗{C.RESET} {msg}")
def warn(msg):   print(f"  {C.YELLOW}⚠{C.RESET} {msg}")
def info(msg):   print(f"  {C.CYAN}ℹ{C.RESET} {msg}")
def step(msg):   print(f"\n{C.BOLD}{C.BLUE}{'─'*60}{C.RESET}\n{C.BOLD}  {msg}{C.RESET}\n{C.BLUE}{'─'*60}{C.RESET}")

def banner():
    print(f"""
{C.CYAN}{C.BOLD}╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   {C.WHITE}🌍  AFRICA FINANCE OBSERVATORY{C.CYAN}                              ║
║   {C.DIM}{C.WHITE}{t('banner_sub1')}{C.RESET}{C.CYAN}{C.BOLD}                       ║
║   {C.DIM}{C.WHITE}{t('banner_sub2')}{C.RESET}{C.CYAN}{C.BOLD}            ║
║                                                              ║
║   {C.GREEN}Abdou Samad Faye{C.CYAN}  ·  Fullstack Geo Data Scientist          ║
║   {C.DIM}{C.WHITE}[{LANG.upper()}]{C.RESET}{C.CYAN}{C.BOLD}                                                       ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝{C.RESET}
""")


# ═══════════════════════════════════════════════════════════════════════════════
# 1. DEPENDENCY CHECK
# ═══════════════════════════════════════════════════════════════════════════════

def check_dependencies():
    """Check that all required packages are installed."""
    step(t("step_check_deps"))
    all_ok = True

    for module, pip_name in REQUIRED_PACKAGES.items():
        try:
            m = importlib.import_module(module)
            ver = getattr(m, "__version__", "?")
            ok(f"{pip_name:20s} v{ver}")
        except ImportError:
            fail(f"{pip_name:20s} — {t('missing_required')}")
            all_ok = False

    print()
    for module, pip_name in OPTIONAL_PACKAGES.items():
        try:
            m = importlib.import_module(module)
            ver = getattr(m, "__version__", "?")
            ok(f"{pip_name:20s} v{ver} {C.DIM}({t('optional_tag')}){C.RESET}")
        except ImportError:
            warn(f"{pip_name:20s} — {t('not_installed')} {C.DIM}({t('optional_tag')}){C.RESET}")

    return all_ok


def check_data():
    """Check the presence and integrity of the Excel source file."""
    step(t("step_check_data"))

    if not EXCEL_FILE.exists():
        fail(f"{t('file_not_found')} : {EXCEL_FILE.name}")
        return False

    size_mb = EXCEL_FILE.stat().st_size / (1024 * 1024)
    ok(f"{t('database_label')} : {EXCEL_FILE.name} ({size_mb:.1f} MB)")

    try:
        import pandas as pd
        sheets = pd.ExcelFile(EXCEL_FILE, engine="openpyxl").sheet_names
        ok(f"{t('sheets_detected')} : {len(sheets)}")
        for s in sheets:
            info(f"  └─ {s}")
        return True
    except Exception as e:
        fail(f"{t('excel_read_error')} : {e}")
        return False


def install_missing():
    """Automatically install missing packages."""
    step(t("step_install"))
    missing = []
    for module, pip_name in {**REQUIRED_PACKAGES, **OPTIONAL_PACKAGES}.items():
        try:
            importlib.import_module(module)
        except ImportError:
            missing.append(pip_name)

    if not missing:
        ok(t("all_installed"))
        return True

    info(f"{t('packages_to_install')} : {', '.join(missing)}")
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "--quiet"] + missing,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        ok(f"{len(missing)} {t('packages_installed_ok')}")
        return True
    except subprocess.CalledProcessError as e:
        fail(f"{t('install_error')} : {e}")
        return False


# ═══════════════════════════════════════════════════════════════════════════════
# 2. DATA LOADING
# ═══════════════════════════════════════════════════════════════════════════════

_loaded_data = {}

def load_data(force=False):
    """Load the Excel file and return the main DataFrames."""
    global _loaded_data
    if _loaded_data and not force:
        return _loaded_data

    step(t("step_load_data"))
    import pandas as pd
    import math

    t0 = time.time()

    all_sheets = pd.read_excel(EXCEL_FILE, sheet_name=None, header=1, engine="openpyxl")
    info(f"  {len(all_sheets)} {t('sheets_loaded_in')} {time.time()-t0:.1f}s")

    def get_sheet(name):
        for k in all_sheets:
            if name in k:
                return all_sheets[k]
        raise KeyError(f"{t('sheet_not_found')} : {name}")

    def safe_numeric(df, cols):
        for c in cols:
            if c in df.columns:
                df[c] = pd.to_numeric(df[c], errors="coerce")
        return df

    # ── Macroéconomie ──
    macro = get_sheet("Macroéconomie").iloc[1:].copy()
    macro.columns = [
        "Pays","Region","Annee","PIB_Mrd","Croissance_PIB","PIB_hab","Inflation",
        "Taux_directeur","Taux_change_USD","Chomage","Balance_courante",
        "Reserves_Mrd","Dette_publique","FDI_entrants","FDI_sortants",
        "Envois_fonds","Recettes_fiscales","Depenses_publiques","Deficit_budgetaire",
        "Exportations","Importations","IDH","Population_M","Urbanisation","Classement_revenu",
    ]
    num_cols_macro = [c for c in macro.columns if c not in ("Pays","Region","Classement_revenu")]
    macro = safe_numeric(macro, num_cols_macro)
    macro = macro.dropna(subset=["Pays","Annee"])
    macro["Annee"] = macro["Annee"].astype(int)

    # ── Secteur Bancaire ──
    bank = get_sheet("Secteur Bancaire").iloc[1:].copy()
    bank.columns = [
        "Pays","Region","Annee","Bancarisation","Nb_banques","Actifs_Mrd",
        "Actifs_PIB","Credit_PIB","Depots_PIB","NPL","CAR","ROE","ROA","NIM",
        "Taux_depot","Taux_pret","Spread_taux","Credit_PME","Credit_agri",
        "Credit_immo","Nb_ATM_100k","Nb_agences_100k","Assurance_vie","Assurance_non_vie",
        "Concentration_HHI","Score_stabilite",
    ]
    num_cols_bank = [c for c in bank.columns if c not in ("Pays","Region")]
    bank = safe_numeric(bank, num_cols_bank)
    bank = bank.dropna(subset=["Pays","Annee"])
    bank["Annee"] = bank["Annee"].astype(int)

    # ── Fintech & Mobile Money ──
    fintech = get_sheet("Fintech").iloc[1:].copy()
    fintech.columns = [
        "Pays","Region","Annee","Comptes_MM","Transactions_MM","Pop_MM",
        "Penetration_smartphone","Couverture_mobile","Nb_startups_fintech",
        "Invest_fintech","Paiements_num","Transferts_num","Open_Banking",
        "Regulation_fintech","MPesa","Orange_Money","MTN_MM","Airtel_Money",
        "Crypto_index","Ecommerce_PIB","Nb_agents_MM","Interop_MM",
        "Credit_digital","API_banking",
    ]
    num_cols_ft = ["Annee","Comptes_MM","Transactions_MM","Pop_MM","Penetration_smartphone",
                   "Couverture_mobile","Nb_startups_fintech","Invest_fintech","Paiements_num",
                   "Crypto_index","Ecommerce_PIB","Nb_agents_MM","Credit_digital"]
    fintech = safe_numeric(fintech, num_cols_ft)
    fintech = fintech.dropna(subset=["Pays","Annee"])
    fintech["Annee"] = fintech["Annee"].astype(int)

    # ── Marchés Financiers ──
    markets = get_sheet("Marchés Financiers").iloc[1:].copy()
    markets.columns = [
        "Pays","Region","Bourse","Annee","Indice","Variation_indice",
        "Capitalisation_Mrd","Capitalisation_PIB","Volume_Mrd","Nb_cotees",
        "PE_ratio","Rendement_div","Oblig_10Y","Spread_souverain","Notation",
        "Eurobond_Mrd","Liquidite","Volatilite","Flux_entrants","Flux_sortants",
        "Market_depth",
    ]
    num_cols_mk = ["Annee","Indice","Variation_indice","Capitalisation_Mrd","Capitalisation_PIB",
                   "Volume_Mrd","Nb_cotees","PE_ratio","Rendement_div","Spread_souverain",
                   "Eurobond_Mrd","Liquidite","Volatilite","Flux_entrants","Flux_sortants"]
    markets = safe_numeric(markets, num_cols_mk)
    markets = markets.dropna(subset=["Pays","Annee"])
    markets["Annee"] = markets["Annee"].astype(int)

    # ── Microfinance ──
    mfi = get_sheet("Microfinance").iloc[1:].copy()
    mfi.columns = [
        "Pays","Region","Annee","Nb_IMF","Portefeuille_M","Microcredit_PIB",
        "Clients_000","Pct_femmes","Pret_moyen","PAR30","PAR90","Rendement_portf",
        "OSS","Epargne_M","Pop_beneficiaire","Microcredit_agri","Microcredit_rural",
        "Score_inclusion","Cout_credit","Taux_remboursement","Scoring_alternatif",
    ]
    num_cols_mfi = ["Annee","Nb_IMF","Portefeuille_M","Microcredit_PIB","Clients_000",
                    "Pct_femmes","Pret_moyen","PAR30","PAR90","OSS","Score_inclusion",
                    "Taux_remboursement","Epargne_M","Pop_beneficiaire","Cout_credit"]
    mfi = safe_numeric(mfi, num_cols_mfi)
    mfi = mfi.dropna(subset=["Pays","Annee"])
    mfi["Annee"] = mfi["Annee"].astype(int)

    # ── Trimestrielles ──
    trim = get_sheet("Trimestrielles").iloc[1:].copy()
    trim.columns = [
        "Pays","Region","Annee","Trimestre","PIB_trim","Croissance_trim",
        "Taux_change","Credit_nouveau","Depots","Transactions_MM","Flux_FDI",
        "Emissions_oblig","Reserves","Taux_interbanc","Inflation_trim",
        "Prod_industrielle","Exports","Imports",
    ]
    num_cols_trim = ["Annee","PIB_trim","Croissance_trim","Taux_change","Credit_nouveau",
                     "Depots","Transactions_MM","Flux_FDI","Reserves","Taux_interbanc",
                     "Inflation_trim","Exports","Imports"]
    trim = safe_numeric(trim, num_cols_trim)
    trim = trim.dropna(subset=["Pays","Annee"])
    trim["Annee"] = trim["Annee"].astype(int)

    # ── Profil Pays ──
    profil = get_sheet("Profil Pays").iloc[1:].copy()
    profil.columns = [
        "Pays","Region","Sous_region","Monnaie","Banque_centrale","Bourse",
        "Zone_monetaire","Lat","Lon","Population_2024","PIB_2000","PIB_2024",
        "Bancarisation_2000","Bancarisation_2024","MM_2024","Export_petrole",
        "Richesse_miniere","Depend_fonds","Ease_business","Score_compet","Cluster",
    ]
    profil = safe_numeric(profil, ["Lat","Lon","Population_2024","PIB_2000","PIB_2024",
                                    "Bancarisation_2000","Bancarisation_2024","MM_2024",
                                    "Ease_business","Score_compet"])

    # ── Crises ──
    crises = get_sheet("Crises").iloc[1:].copy()
    crises.columns = [
        "Pays","Region","Annee","Type_crise","Severite","Impact_PIB",
        "Impact_bancarisation","Fuite_capitaux","Hausse_NPL","Depreciation",
        "Aide_FMI","Duree_trim","Mesures","Reprise_annees",
    ]
    crises = safe_numeric(crises, ["Annee","Severite","Impact_PIB","Hausse_NPL",
                                    "Aide_FMI","Duree_trim","Fuite_capitaux","Depreciation"])

    elapsed = time.time() - t0

    n_rows = sum(len(df) for df in [macro, bank, fintech, markets, mfi, trim, crises])
    ok(f"{t('loading_done_in')} {elapsed:.1f}s")
    ok(f"  {len(macro['Pays'].unique())} {t('countries')} | {n_rows:,} {t('total_rows')} | 9 DataFrames")

    _loaded_data = {
        "macro": macro,
        "bank": bank,
        "fintech": fintech,
        "markets": markets,
        "mfi": mfi,
        "trim": trim,
        "profil": profil,
        "crises": crises,
    }
    return _loaded_data


# ═══════════════════════════════════════════════════════════════════════════════
# 3. DATABASE INFORMATION
# ═══════════════════════════════════════════════════════════════════════════════

def show_info():
    """Display a complete summary of the database."""
    data = load_data()
    step(t("step_info"))

    macro = data["macro"]
    pays = sorted(macro["Pays"].unique())
    regions = sorted(macro["Region"].dropna().unique())
    annees = sorted(macro["Annee"].unique())

    print(f"""
  {C.BOLD}{t('info_database'):17s}:{C.RESET} {EXCEL_FILE.name}
  {C.BOLD}{t('info_size'):17s}:{C.RESET} {EXCEL_FILE.stat().st_size / (1024*1024):.1f} MB
  {C.BOLD}{t('info_period'):17s}:{C.RESET} {min(annees)} — {max(annees)} ({len(annees)} {t('info_years')})
  {C.BOLD}{t('info_countries'):17s}:{C.RESET} {len(pays)}
  {C.BOLD}{t('info_regions'):17s}:{C.RESET} {len(regions)}
""")

    print(f"  {C.BOLD}{t('info_regions_label')} :{C.RESET}")
    for reg in regions:
        n = macro[macro["Region"] == reg]["Pays"].nunique()
        print(f"    {C.GREEN}•{C.RESET} {reg} ({n} {t('info_country_word')})")

    print(f"\n  {C.BOLD}{t('info_dataframes')} :{C.RESET}")
    for name, df in data.items():
        print(f"    {C.CYAN}•{C.RESET} {name:15s} → {len(df):>6,} {t('info_rows')} × {len(df.columns):>2} {t('info_cols')}")

    print(f"\n  {C.BOLD}{t('info_country_list')} :{C.RESET}")
    for i, p in enumerate(pays):
        end = "\n" if (i + 1) % 4 == 0 else ""
        print(f"    {p:25s}", end=end)
    print()


# ═══════════════════════════════════════════════════════════════════════════════
# 4. CONSOLE STATISTICS
# ═══════════════════════════════════════════════════════════════════════════════

def show_stats():
    """Compute and display descriptive statistics in the console."""
    data = load_data()
    import numpy as np
    from scipy import stats as sp_stats

    macro, bank, fintech, mfi = data["macro"], data["bank"], data["fintech"], data["mfi"]

    step(t("step_stats"))

    m24 = macro[macro["Annee"] == 2024]
    b24 = bank[bank["Annee"] == 2024]
    f24 = fintech[fintech["Annee"] == 2024]
    mfi24 = mfi[mfi["Annee"] == 2024]

    print(f"""
  {C.BOLD}{C.GREEN}═══ {t('macro_title')} ═══{C.RESET}
  {t('total_african_gdp'):25s}: {C.BOLD}${m24['PIB_Mrd'].sum():>10,.1f} Bn{C.RESET}
  {t('avg_gdp_growth'):25s}: {m24['Croissance_PIB'].mean():>8.1f} %
  {t('avg_gdp_capita'):25s}: ${m24['PIB_hab'].mean():>8,.0f}
  {t('avg_inflation'):25s}: {m24['Inflation'].mean():>8.1f} %
  {t('avg_public_debt'):25s}: {m24['Dette_publique'].mean():>8.1f} % GDP
  {t('avg_unemployment'):25s}: {m24['Chomage'].mean():>8.1f} %
  {t('total_fdi_inflows'):25s}: ${m24['FDI_entrants'].sum():>8.1f} Bn
  {t('total_remittances'):25s}: ${m24['Envois_fonds'].sum():>8.1f} Bn

  {C.BOLD}{C.BLUE}═══ {t('banking_title')} ═══{C.RESET}
  {t('avg_banking_rate'):25s}: {b24['Bancarisation'].mean():>8.1f} %
  {t('avg_npl'):25s}: {b24['NPL'].mean():>8.1f} %
  {t('avg_car'):25s}: {b24['CAR'].mean():>8.1f} %
  {t('avg_roe'):25s}: {b24['ROE'].mean():>8.1f} %
  {t('avg_nim'):25s}: {b24['NIM'].mean():>8.1f} %
  {t('avg_credit_gdp'):25s}: {b24['Credit_PIB'].mean():>8.1f} %

  {C.BOLD}{C.MAGENTA}═══ {t('fintech_title')} ═══{C.RESET}
  {t('total_mm_accounts'):25s}: {f24['Comptes_MM'].sum():>8.0f} M
  {t('mm_transactions'):25s}: ${f24['Transactions_MM'].sum():>8.0f} Bn
  {t('avg_mm_pop'):25s}: {f24['Pop_MM'].mean():>8.1f} %
  {t('total_fintech_startups'):25s}: {f24['Nb_startups_fintech'].sum():>8,.0f}

  {C.BOLD}{C.YELLOW}═══ {t('microfinance_title')} ═══{C.RESET}
  {t('avg_par30'):25s}: {mfi24['PAR30'].mean():>8.1f} %
  {t('avg_oss'):25s}: {mfi24['OSS'].mean():>8.1f} %
  {t('avg_inclusion'):25s}: {mfi24['Score_inclusion'].mean():>8.1f} / 10
  {t('total_clients'):25s}: {mfi24['Clients_000'].sum():>8,.0f}
  {t('avg_women_pct'):25s}: {mfi24['Pct_femmes'].mean():>8.1f} %
""")

    # ── Quick statistical tests ──
    step(t("step_stat_tests"))

    merged = m24.merge(b24[["Pays","Bancarisation","NPL","CAR"]], on="Pays", how="left")

    tests = [
        ("PIB_hab", "Bancarisation", t("reg_gdp_banking")),
        ("Inflation", "Croissance_PIB", t("reg_infl_growth")),
        ("PIB_hab", "NPL", t("reg_gdp_npl")),
    ]
    print(f"\n  {C.BOLD}{t('linear_regressions')} :{C.RESET}")
    for xv, yv, label in tests:
        tmp = merged[[xv, yv]].dropna()
        if len(tmp) < 5:
            continue
        slope, intercept, r, p, se = sp_stats.linregress(tmp[xv], tmp[yv])
        sig = f"{C.GREEN}★★★{C.RESET}" if p < 0.001 else f"{C.GREEN}★★{C.RESET}" if p < 0.01 else f"{C.GREEN}★{C.RESET}" if p < 0.05 else f"{C.RED}ns{C.RESET}"
        print(f"    {label:35s} R²={r**2:.3f}  p={p:.4f}  β={slope:.4f}  {sig}")

    # ANOVA
    print(f"\n  {C.BOLD}{t('anova_by_region')} :{C.RESET}")
    for v in ["Croissance_PIB", "Inflation", "PIB_hab"]:
        groups = [g[v].dropna().values for _, g in m24.groupby("Region") if len(g[v].dropna()) >= 2]
        if len(groups) < 2:
            continue
        F, p = sp_stats.f_oneway(*groups)
        sig = f"{C.GREEN}★★★{C.RESET}" if p < 0.001 else f"{C.GREEN}★{C.RESET}" if p < 0.05 else f"{C.RED}ns{C.RESET}"
        print(f"    {v:30s}  F={F:>8.2f}  p={p:.4f}  {sig}")


# ═══════════════════════════════════════════════════════════════════════════════
# 5. DASHBOARD BUILD
# ═══════════════════════════════════════════════════════════════════════════════

def build_dashboard():
    """Run build_dashboard.py to generate the HTML dashboard."""
    step(t("step_build"))

    if not BUILD_SCRIPT.exists():
        fail(f"{t('script_not_found')} : {BUILD_SCRIPT.name}")
        return False

    t0 = time.time()
    result = subprocess.run(
        [sys.executable, str(BUILD_SCRIPT)],
        cwd=str(BASE_DIR),
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        fail(t("build_error"))
        print(f"{C.RED}{result.stderr}{C.RESET}")
        return False

    for line in result.stdout.strip().split("\n"):
        if line.strip():
            info(line.strip())

    elapsed = time.time() - t0
    if DASHBOARD_FILE.exists():
        size = DASHBOARD_FILE.stat().st_size / (1024 * 1024)
        ok(f"{t('dashboard_generated')} {elapsed:.1f}s → {DASHBOARD_FILE.name} ({size:.1f} MB)")
        return True
    else:
        fail(t("html_not_created"))
        return False


# ═══════════════════════════════════════════════════════════════════════════════
# 6. LOCAL SERVER
# ═══════════════════════════════════════════════════════════════════════════════

def serve_dashboard(port=DEFAULT_PORT):
    """Launch a local HTTP server to view the dashboard."""
    step(t("step_serve", port=port))

    if not DASHBOARD_FILE.exists():
        warn(t("dashboard_not_found"))
        if not build_dashboard():
            return

    url = f"http://localhost:{port}/AfricaFinance_Dashboard.html"
    ok(f"{t('dashboard_at')} : {C.BOLD}{C.GREEN}{url}{C.RESET}")
    info(f"{t('press_ctrl_c')}\n")

    try:
        import webbrowser
        webbrowser.open(url)
    except Exception:
        pass

    try:
        import http.server
        import socketserver

        os.chdir(str(BASE_DIR))

        handler = http.server.SimpleHTTPRequestHandler
        handler.log_message = lambda *args: None

        with socketserver.TCPServer(("", port), handler) as httpd:
            httpd.serve_forever()
    except OSError as e:
        if "Address already in use" in str(e) or "10048" in str(e):
            warn(t("port_in_use", port=port, port1=port+1))
            serve_dashboard(port + 1)
        else:
            fail(f"{t('server_error')} : {e}")
    except KeyboardInterrupt:
        print(f"\n{C.DIM}  {t('server_stopped')}{C.RESET}")


# ═══════════════════════════════════════════════════════════════════════════════
# 7. EXPORTS
# ═══════════════════════════════════════════════════════════════════════════════

def export_csv():
    """Export all data to separate CSV files."""
    data = load_data()
    step(t("step_csv"))

    EXPORT_DIR.mkdir(exist_ok=True)
    csv_dir = EXPORT_DIR / "csv"
    csv_dir.mkdir(exist_ok=True)

    for name, df in data.items():
        filepath = csv_dir / f"AfricaFinance_{name}.csv"
        df.to_csv(filepath, index=False, encoding="utf-8-sig")
        ok(f"{filepath.name:45s} → {len(df):>6,} {t('rows_word')}")

    import pandas as pd
    merged = data["macro"].merge(
        data["bank"][["Pays","Annee","Bancarisation","NPL","CAR","ROE","NIM","Credit_PIB"]],
        on=["Pays","Annee"], how="left"
    ).merge(
        data["fintech"][["Pays","Annee","Pop_MM","Comptes_MM","Nb_startups_fintech"]],
        on=["Pays","Annee"], how="left"
    ).merge(
        data["mfi"][["Pays","Annee","Score_inclusion","PAR30","Portefeuille_M"]],
        on=["Pays","Annee"], how="left"
    )
    merged_path = csv_dir / "AfricaFinance_MERGED.csv"
    merged.to_csv(merged_path, index=False, encoding="utf-8-sig")
    ok(f"{'AfricaFinance_MERGED.csv':45s} → {len(merged):>6,} {t('rows_word')}")

    print(f"\n  {C.GREEN}{t('exported_to')} :{C.RESET} {csv_dir}")


def export_excel():
    """Export data and analyses to a multi-sheet Excel file."""
    data = load_data()
    step(t("step_excel"))

    EXPORT_DIR.mkdir(exist_ok=True)

    import pandas as pd
    import numpy as np
    from scipy import stats as sp_stats

    output_path = EXPORT_DIR / "AfricaFinance_Analyses.xlsx"

    try:
        writer = pd.ExcelWriter(output_path, engine="xlsxwriter")
    except ModuleNotFoundError:
        warn(t("xlsxwriter_missing"))
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "xlsxwriter", "--quiet"],
            stdout=subprocess.DEVNULL,
        )
        writer = pd.ExcelWriter(output_path, engine="xlsxwriter")

    macro, bank, fintech, mfi = data["macro"], data["bank"], data["fintech"], data["mfi"]

    for name, df in data.items():
        df.to_excel(writer, sheet_name=name[:31], index=False)
    ok(t("raw_data_exported"))

    m24, b24, f24, mfi24 = [df[df["Annee"]==2024] if "Annee" in df.columns else df
                             for df in [macro, bank, fintech, mfi]]
    desc_dfs = {"Macro": m24, "Banking": b24, "Fintech": f24, "MicroFi": mfi24}
    desc_rows = []
    for src, df in desc_dfs.items():
        for col in df.select_dtypes(include=[np.number]).columns:
            if col == "Annee":
                continue
            s = df[col].dropna()
            if len(s) < 3:
                continue
            desc_rows.append({
                "Dimension": src, "Variable": col,
                "N": len(s), "Mean": round(s.mean(), 2),
                "Median": round(s.median(), 2), "Std": round(s.std(), 2),
                "Min": round(s.min(), 2), "Max": round(s.max(), 2),
                "Q1": round(s.quantile(0.25), 2), "Q3": round(s.quantile(0.75), 2),
                "Skewness": round(s.skew(), 3), "Kurtosis": round(s.kurtosis(), 3),
                "CV%": round(s.std()/s.mean()*100, 1) if s.mean() != 0 else None,
            })
    pd.DataFrame(desc_rows).to_excel(writer, sheet_name="Descriptive_Stats", index=False)
    ok(f"{t('desc_stats_label')} : {len(desc_rows)} {t('variables_word')}")

    merged = m24.merge(b24[["Pays","Bancarisation","NPL","CAR","ROE","Credit_PIB"]], on="Pays", how="left")
    merged = merged.merge(f24[["Pays","Pop_MM"]], on="Pays", how="left")
    corr_vars = ["PIB_hab","Croissance_PIB","Inflation","Dette_publique","Bancarisation","NPL","CAR","Credit_PIB","Pop_MM"]
    corr_df = merged[corr_vars].corr()
    corr_df.to_excel(writer, sheet_name="Pearson_Correlations")
    ok(t("pearson_corr"))

    ts = macro.groupby("Annee").agg(
        GDP_total=("PIB_Mrd","sum"), Growth_avg=("Croissance_PIB","mean"),
        Inflation_avg=("Inflation","mean"), FDI_total=("FDI_entrants","sum"),
        Debt_avg=("Dette_publique","mean"),
    ).reset_index()
    ts.to_excel(writer, sheet_name="Continental_TS", index=False)
    ok(t("continental_ts"))

    rankings = []
    for col, label in [("PIB_Mrd","GDP"), ("Croissance_PIB","Growth"), ("PIB_hab","GDP_capita"),
                        ("Inflation","Inflation"), ("Dette_publique","Debt")]:
        top = m24.nlargest(15, col)[["Pays", col]].copy()
        top["Indicator"] = label
        top["Rank"] = range(1, len(top)+1)
        rankings.append(top)
    pd.concat(rankings).to_excel(writer, sheet_name="Rankings_2024", index=False)
    ok(t("rankings_top15"))

    writer.close()
    size = output_path.stat().st_size / (1024 * 1024)
    ok(f"{t('file_exported')} : {output_path.name} ({size:.1f} MB)")
    print(f"\n  {C.GREEN}{t('exported_to')} :{C.RESET} {output_path}")


# ═══════════════════════════════════════════════════════════════════════════════
# 8. INTERACTIVE MENU
# ═══════════════════════════════════════════════════════════════════════════════

def interactive_menu():
    """Main interactive menu."""
    while True:
        m = t  # shortcut
        print(f"""
{C.BOLD}  ┌──────────────────────────────────────────────┐
  │         {m('menu_title'):37s}│
  ├──────────────────────────────────────────────┤
  │                                              │
  │  {C.GREEN}1{C.RESET}{C.BOLD} │ 📊  {m('menu_1'):35s}  │
  │  {C.GREEN}2{C.RESET}{C.BOLD} │ 🌐  {m('menu_2'):35s}  │
  │  {C.GREEN}3{C.RESET}{C.BOLD} │ 📈  {m('menu_3'):35s}  │
  │  {C.GREEN}4{C.RESET}{C.BOLD} │ 📋  {m('menu_4'):35s}  │
  │  {C.GREEN}5{C.RESET}{C.BOLD} │ 📤  {m('menu_5'):35s}  │
  │  {C.GREEN}6{C.RESET}{C.BOLD} │ 📗  {m('menu_6'):35s}  │
  │  {C.GREEN}7{C.RESET}{C.BOLD} │ 🔍  {m('menu_7'):35s}  │
  │  {C.GREEN}8{C.RESET}{C.BOLD} │ 📦  {m('menu_8'):35s}  │
  │  {C.GREEN}9{C.RESET}{C.BOLD} │ 🚀  {m('menu_9'):35s}  │
  │  {C.YELLOW}L{C.RESET}{C.BOLD} │ 🌐  {m('menu_lang'):35s}  │
  │  {C.RED}0{C.RESET}{C.BOLD} │ 🚪  {m('menu_0'):35s}  │
  │                                              │
  └──────────────────────────────────────────────┘{C.RESET}""")

        try:
            choice = input(f"\n  {C.CYAN}{m('choice_prompt')} >{C.RESET} ").strip().upper()
        except (EOFError, KeyboardInterrupt):
            print(f"\n{C.DIM}  {m('goodbye')}{C.RESET}")
            break

        if choice == "1":
            build_dashboard()
        elif choice == "2":
            build_dashboard()
            serve_dashboard()
        elif choice == "3":
            show_stats()
        elif choice == "4":
            show_info()
        elif choice == "5":
            export_csv()
        elif choice == "6":
            export_excel()
        elif choice == "7":
            check_dependencies()
            check_data()
        elif choice == "8":
            install_missing()
        elif choice == "9":
            run_all()
        elif choice == "L":
            global LANG
            set_lang("fr" if LANG == "en" else "en")
            ok(t("lang_switched"))
            banner()
        elif choice == "0":
            print(f"\n  {C.DIM}{m('goodbye')} 🌍{C.RESET}\n")
            break
        else:
            warn(t("invalid_choice"))


# ═══════════════════════════════════════════════════════════════════════════════
# 9. FULL EXECUTION
# ═══════════════════════════════════════════════════════════════════════════════

def run_all():
    """Run the full chain: check → build → export → serve."""
    step(t("step_run_all"))
    t0 = time.time()

    deps_ok = check_dependencies()
    if not deps_ok:
        warn(t("auto_install_attempt"))
        install_missing()

    data_ok = check_data()
    if not data_ok:
        fail(t("cannot_continue"))
        return

    show_stats()
    export_csv()
    export_excel()

    if build_dashboard():
        elapsed = time.time() - t0
        step(f"✅ {t('pipeline_done')} {elapsed:.1f}s")
        ok(f"Dashboard : {DASHBOARD_FILE.name}")
        ok(f"Exports   : {EXPORT_DIR}/")
        serve_dashboard()


# ═══════════════════════════════════════════════════════════════════════════════
# ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    """Main entry point with CLI argument handling."""
    parser = argparse.ArgumentParser(
        description="🌍 Africa Finance Observatory — Financial analysis pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                 Interactive menu
  python main.py --build         Build the dashboard
  python main.py --serve         Build + serve
  python main.py --stats         Console statistics
  python main.py --export-csv    Export to CSV
  python main.py --all           Full pipeline
  python main.py --lang fr       Run in French
        """,
    )
    parser.add_argument("--build", action="store_true", help="Build the HTML dashboard")
    parser.add_argument("--serve", action="store_true", help="Build + launch the server")
    parser.add_argument("--stats", action="store_true", help="Display statistics")
    parser.add_argument("--info", action="store_true", help="Database information")
    parser.add_argument("--export-csv", action="store_true", help="Export to CSV")
    parser.add_argument("--export-excel", action="store_true", help="Export to Excel")
    parser.add_argument("--check", action="store_true", help="Check dependencies")
    parser.add_argument("--install", action="store_true", help="Install missing packages")
    parser.add_argument("--all", action="store_true", help="Full pipeline")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help=f"Server port (default: {DEFAULT_PORT})")
    parser.add_argument("--lang", choices=["en", "fr"], default="en", help="Language: en (default) or fr")

    args = parser.parse_args()

    # Set language before anything else
    set_lang(args.lang)

    banner()

    # No arguments → interactive menu
    if len(sys.argv) == 1:
        interactive_menu()
        return

    # Handle --lang only (no other flags) → interactive menu in that language
    if args.lang != "en" and len(sys.argv) == 3:
        interactive_menu()
        return

    if args.check:
        check_dependencies()
        check_data()
    if args.install:
        install_missing()
    if args.info:
        show_info()
    if args.stats:
        show_stats()
    if args.export_csv:
        export_csv()
    if args.export_excel:
        export_excel()
    if args.build:
        build_dashboard()
    if args.serve:
        build_dashboard()
        serve_dashboard(args.port)
    if args.all:
        run_all()


if __name__ == "__main__":
    main()
