#!/usr/bin/env python3
"""
AFRICA FINANCE DASHBOARD BUILDER
Data Analyst Dashboard — 54 pays · 2000-2024 · 12 dimensions
Generates a self-contained interactive HTML dashboard from the Excel database.
"""

import pandas as pd
import json
import html
import math
import numpy as np
from scipy import stats as sp_stats
from pathlib import Path

EXCEL_FILE = Path(__file__).parent / "AfricaFinance_Database_2000_2024.xlsx"
OUTPUT_FILE = Path(__file__).parent / "AfricaFinance_Dashboard.html"

import warnings
warnings.filterwarnings('ignore')

# ─── UTILITIES ───────────────────────────────────────────────────────────────

def safe_float(v):
    try:
        f = float(v)
        return f if not (math.isnan(f) or math.isinf(f)) else None
    except (ValueError, TypeError):
        return None

def df_to_records(df):
    """Convert dataframe to list of dicts with safe JSON values."""
    records = []
    for _, row in df.iterrows():
        rec = {}
        for col in df.columns:
            v = row[col]
            if pd.isna(v):
                rec[col] = None
            elif isinstance(v, (int, float)):
                f = float(v)
                rec[col] = f if not (math.isnan(f) or math.isinf(f)) else None
            else:
                rec[col] = str(v)
        records.append(rec)
    return records

# ─── DATA LOADING ────────────────────────────────────────────────────────────

print("📦 Loading Excel database...")

# Load all sheets at once for efficiency
ALL_SHEETS = pd.read_excel(EXCEL_FILE, sheet_name=None, header=1, engine='openpyxl')

print('  Loading sheets...')

def get_sheet(name):
    for k in ALL_SHEETS:
        if name in k:
            return ALL_SHEETS[k]
    raise KeyError(f'Sheet not found: {name}')

# Macroeconomie
macro_raw = get_sheet('Macroéconomie')
macro = macro_raw.iloc[1:].copy()  # skip sub-header row
macro.columns = ['Pays','Region','Annee','PIB_Mrd','Croissance_PIB','PIB_hab','Inflation',
                 'Taux_directeur','Taux_change_USD','Chomage','Balance_courante',
                 'Reserves_Mrd','Dette_publique','FDI_entrants','FDI_sortants',
                 'Envois_fonds','Recettes_fiscales','Depenses_publiques','Deficit_budgetaire',
                 'Exportations','Importations','IDH','Population_M','Urbanisation','Classement_revenu']
for c in ['Annee','PIB_Mrd','Croissance_PIB','PIB_hab','Inflation','Taux_directeur',
          'Chomage','Balance_courante','Reserves_Mrd','Dette_publique','FDI_entrants',
          'FDI_sortants','Envois_fonds','Population_M','Urbanisation','IDH',
          'Exportations','Importations','Taux_change_USD','Recettes_fiscales',
          'Depenses_publiques','Deficit_budgetaire']:
    macro[c] = pd.to_numeric(macro[c], errors='coerce')
macro = macro.dropna(subset=['Pays','Annee'])
macro['Annee'] = macro['Annee'].astype(int)

# Secteur Bancaire
bank_raw = get_sheet('Secteur Bancaire')
bank = bank_raw.iloc[1:].copy()
bank.columns = ['Pays','Region','Annee','Bancarisation','Nb_banques','Actifs_Mrd',
                'Actifs_PIB','Credit_PIB','Depots_PIB','NPL','CAR','ROE','ROA','NIM',
                'Taux_depot','Taux_pret','Spread_taux','Credit_PME','Credit_agri',
                'Credit_immo','Nb_ATM_100k','Nb_agences_100k','Assurance_vie','Assurance_non_vie',
                'Concentration_HHI','Score_stabilite']
for c in ['Annee','Bancarisation','NPL','CAR','ROE','ROA','NIM','Credit_PIB','Depots_PIB',
          'Actifs_Mrd','Actifs_PIB','Nb_banques','Spread_taux','Credit_PME','Credit_agri',
          'Credit_immo','Nb_ATM_100k','Nb_agences_100k','Concentration_HHI','Score_stabilite',
          'Taux_depot','Taux_pret']:
    bank[c] = pd.to_numeric(bank[c], errors='coerce')
bank = bank.dropna(subset=['Pays','Annee'])
bank['Annee'] = bank['Annee'].astype(int)

# Fintech & Mobile Money
fintech_raw = get_sheet('Fintech')
fintech = fintech_raw.iloc[1:].copy()
fintech.columns = ['Pays','Region','Annee','Comptes_MM','Transactions_MM','Pop_MM',
                   'Penetration_smartphone','Couverture_mobile','Nb_startups_fintech',
                   'Invest_fintech','Paiements_num','Transferts_num','Open_Banking',
                   'Regulation_fintech','MPesa','Orange_Money','MTN_MM','Airtel_Money',
                   'Crypto_index','Ecommerce_PIB','Nb_agents_MM','Interop_MM',
                   'Credit_digital','API_banking']
for c in ['Annee','Comptes_MM','Transactions_MM','Pop_MM','Penetration_smartphone',
          'Couverture_mobile','Nb_startups_fintech','Invest_fintech','Paiements_num',
          'Crypto_index','Ecommerce_PIB','Nb_agents_MM','Credit_digital']:
    fintech[c] = pd.to_numeric(fintech[c], errors='coerce')
fintech = fintech.dropna(subset=['Pays','Annee'])
fintech['Annee'] = fintech['Annee'].astype(int)

# Marches Financiers
markets_raw = get_sheet('Marchés Financiers')
markets = markets_raw.iloc[1:].copy()
markets.columns = ['Pays','Region','Bourse','Annee','Indice','Variation_indice',
                   'Capitalisation_Mrd','Capitalisation_PIB','Volume_Mrd','Nb_cotees',
                   'PE_ratio','Rendement_div','Oblig_10Y','Spread_souverain','Notation',
                   'Eurobond_Mrd','Liquidite','Volatilite','Flux_entrants','Flux_sortants',
                   'Market_depth']
for c in ['Annee','Indice','Variation_indice','Capitalisation_Mrd','Capitalisation_PIB',
          'Volume_Mrd','Nb_cotees','PE_ratio','Rendement_div','Spread_souverain',
          'Eurobond_Mrd','Liquidite','Volatilite','Flux_entrants','Flux_sortants']:
    markets[c] = pd.to_numeric(markets[c], errors='coerce')
markets = markets.dropna(subset=['Pays','Annee'])
markets['Annee'] = markets['Annee'].astype(int)

# Microfinance
mfi_raw = get_sheet('Microfinance')
mfi = mfi_raw.iloc[1:].copy()
mfi.columns = ['Pays','Region','Annee','Nb_IMF','Portefeuille_M','Microcredit_PIB',
               'Clients_000','Pct_femmes','Pret_moyen','PAR30','PAR90','Rendement_portf',
               'OSS','Epargne_M','Pop_beneficiaire','Microcredit_agri','Microcredit_rural',
               'Score_inclusion','Cout_credit','Taux_remboursement','Scoring_alternatif']
for c in ['Annee','Nb_IMF','Portefeuille_M','Microcredit_PIB','Clients_000','Pct_femmes',
          'Pret_moyen','PAR30','PAR90','OSS','Score_inclusion','Taux_remboursement',
          'Epargne_M','Pop_beneficiaire','Cout_credit']:
    mfi[c] = pd.to_numeric(mfi[c], errors='coerce')
mfi = mfi.dropna(subset=['Pays','Annee'])
mfi['Annee'] = mfi['Annee'].astype(int)

# Trimestrielles
trim_raw = get_sheet('Trimestrielles')
trim = trim_raw.iloc[1:].copy()
trim.columns = ['Pays','Region','Annee','Trimestre','PIB_trim','Croissance_trim',
                'Taux_change','Credit_nouveau','Depots','Transactions_MM','Flux_FDI',
                'Emissions_oblig','Reserves','Taux_interbanc','Inflation_trim',
                'Prod_industrielle','Exports','Imports']
for c in ['Annee','PIB_trim','Croissance_trim','Taux_change','Credit_nouveau','Depots',
          'Transactions_MM','Flux_FDI','Reserves','Taux_interbanc','Inflation_trim',
          'Exports','Imports']:
    trim[c] = pd.to_numeric(trim[c], errors='coerce')
trim = trim.dropna(subset=['Pays','Annee'])
trim['Annee'] = trim['Annee'].astype(int)

# Profil Pays
profil_raw = get_sheet('Profil Pays')
profil = profil_raw.iloc[1:].copy()
profil.columns = ['Pays','Region','Sous_region','Monnaie','Banque_centrale','Bourse',
                  'Zone_monetaire','Lat','Lon','Population_2024','PIB_2000','PIB_2024',
                  'Bancarisation_2000','Bancarisation_2024','MM_2024','Export_petrole',
                  'Richesse_miniere','Depend_fonds','Ease_business','Score_compet','Cluster']
for c in ['Lat','Lon','Population_2024','PIB_2000','PIB_2024','Bancarisation_2000',
          'Bancarisation_2024','MM_2024','Depend_fonds','Ease_business','Score_compet']:
    profil[c] = pd.to_numeric(profil[c], errors='coerce')

# Correlations
corr_raw = get_sheet('Corrélations')
corr = corr_raw.iloc[1:].copy()

# Crises
crises_raw = get_sheet('Crises')
crises = crises_raw.iloc[1:].copy()
crises.columns = ['Pays','Region','Annee','Type_crise','Severite','Impact_PIB',
                  'Impact_bancarisation','Fuite_capitaux','Hausse_NPL','Depreciation',
                  'Aide_FMI','Duree_trim','Mesures','Reprise_annees']
for c in ['Annee','Severite','Impact_PIB','Impact_bancarisation','Fuite_capitaux',
          'Hausse_NPL','Depreciation','Aide_FMI','Duree_trim','Reprise_annees']:
    crises[c] = pd.to_numeric(crises[c], errors='coerce')

# Rankings
rankings_raw = get_sheet('Classements')

# Stats descriptives
stats_raw = get_sheet('Statistiques')
stats = stats_raw.iloc[1:].copy()
stats.columns = ['Region','Indicateur','Unite','N','Min','Max','Moyenne','Mediane',
                 'Ecart_type','P25','P75','CV']
for c in ['N','Min','Max','Moyenne','Mediane','Ecart_type','P25','P75','CV']:
    stats[c] = pd.to_numeric(stats[c], errors='coerce')

print(f"✅ Loaded: Macro={len(macro)}, Bank={len(bank)}, Fintech={len(fintech)}, Markets={len(markets)}, MFI={len(mfi)}, Quarterly={len(trim)}, Profiles={len(profil)}, Crises={len(crises)}")

# ─── COMPUTE AGGREGATES FOR DASHBOARD ─────────────────────────────────────

print("📊 Computing aggregates...")

# --- KPIs 2024 ---
m24 = macro[macro['Annee']==2024]
b24 = bank[bank['Annee']==2024]
f24 = fintech[fintech['Annee']==2024]
mfi24 = mfi[mfi['Annee']==2024]

kpis = {
    "pib_total": round(m24['PIB_Mrd'].sum(), 1),
    "pib_growth_avg": round(m24['Croissance_PIB'].mean(), 1),
    "inflation_avg": round(m24['Inflation'].mean(), 1),
    "bancarisation_avg": round(b24['Bancarisation'].mean(), 1),
    "npl_avg": round(b24['NPL'].mean(), 1),
    "car_avg": round(b24['CAR'].mean(), 1),
    "roe_avg": round(b24['ROE'].mean(), 1),
    "nim_avg": round(b24['NIM'].mean(), 1),
    "mobile_money_accounts": round(f24['Comptes_MM'].sum(), 1),
    "fintech_startups": int(f24['Nb_startups_fintech'].sum()),
    "fdi_total": round(m24['FDI_entrants'].sum(), 1),
    "dette_avg": round(m24['Dette_publique'].mean(), 1),
    "nb_pays": len(m24['Pays'].unique()),
    "nb_annees": len(macro['Annee'].unique()),
    "credit_pib_avg": round(b24['Credit_PIB'].mean(), 1),
    "score_inclusion_avg": round(mfi24['Score_inclusion'].mean(), 1),
    "mm_transactions": round(f24['Transactions_MM'].sum(), 1),
    "pop_mm_avg": round(f24['Pop_MM'].mean(), 1),
}

# --- Continental time series ---
ts_continental = macro.groupby('Annee').agg(
    PIB_total=('PIB_Mrd','sum'),
    Croissance_moy=('Croissance_PIB','mean'),
    Inflation_moy=('Inflation','mean'),
    FDI_total=('FDI_entrants','sum'),
    Dette_moy=('Dette_publique','mean'),
    Chomage_moy=('Chomage','mean'),
    Envois_fonds=('Envois_fonds','sum'),
    PIB_hab_moy=('PIB_hab','mean'),
).reset_index()

ts_banking = bank.groupby('Annee').agg(
    Bancarisation_moy=('Bancarisation','mean'),
    NPL_moy=('NPL','mean'),
    CAR_moy=('CAR','mean'),
    ROE_moy=('ROE','mean'),
    NIM_moy=('NIM','mean'),
    Credit_PIB_moy=('Credit_PIB','mean'),
    Spread_moy=('Spread_taux','mean'),
).reset_index()

ts_fintech = fintech.groupby('Annee').agg(
    Comptes_MM_total=('Comptes_MM','sum'),
    Transactions_total=('Transactions_MM','sum'),
    Pop_MM_moy=('Pop_MM','mean'),
    Startups_total=('Nb_startups_fintech','sum'),
    Invest_total=('Invest_fintech','sum'),
    Paiements_num_moy=('Paiements_num','mean'),
    Smartphone_moy=('Penetration_smartphone','mean'),
).reset_index()

ts_mfi = mfi.groupby('Annee').agg(
    PAR30_moy=('PAR30','mean'),
    OSS_moy=('OSS','mean'),
    Portefeuille_total=('Portefeuille_M','sum'),
    Clients_total=('Clients_000','sum'),
    Pct_femmes_moy=('Pct_femmes','mean'),
    Score_inclusion_moy=('Score_inclusion','mean'),
).reset_index()

# --- Regional aggregates ---
regions_macro = macro[macro['Annee']==2024].groupby('Region').agg(
    PIB_total=('PIB_Mrd','sum'),
    Croissance_moy=('Croissance_PIB','mean'),
    Inflation_moy=('Inflation','mean'),
    FDI_total=('FDI_entrants','sum'),
    Dette_moy=('Dette_publique','mean'),
    Nb_pays=('Pays','count'),
).reset_index()

regions_bank = bank[bank['Annee']==2024].groupby('Region').agg(
    Bancarisation_moy=('Bancarisation','mean'),
    NPL_moy=('NPL','mean'),
    CAR_moy=('CAR','mean'),
    ROE_moy=('ROE','mean'),
    NIM_moy=('NIM','mean'),
    Credit_PIB_moy=('Credit_PIB','mean'),
).reset_index()

regions_fintech = fintech[fintech['Annee']==2024].groupby('Region').agg(
    Comptes_MM_total=('Comptes_MM','sum'),
    Pop_MM_moy=('Pop_MM','mean'),
    Startups_total=('Nb_startups_fintech','sum'),
).reset_index()

# --- Time series by region ---
ts_region_growth = macro.groupby(['Annee','Region'])['Croissance_PIB'].mean().reset_index()
ts_region_banc = bank.groupby(['Annee','Region'])['Bancarisation'].mean().reset_index()
ts_region_npl = bank.groupby(['Annee','Region'])['NPL'].mean().reset_index()
ts_region_mm = fintech.groupby(['Annee','Region'])['Pop_MM'].mean().reset_index()

# --- Top/Bottom country rankings 2024 ---
def top_bottom(df, col, n=15):
    valid = df[df[col].notna()].sort_values(col, ascending=False)
    top = valid.head(n)[['Pays',col]].to_dict('records')
    bottom = valid.tail(n)[['Pays',col]].to_dict('records')
    return {"top": top, "bottom": bottom}

rankings_data = {
    "bancarisation": top_bottom(b24, 'Bancarisation'),
    "npl": top_bottom(b24, 'NPL'),
    "croissance": top_bottom(m24, 'Croissance_PIB'),
    "pib": top_bottom(m24, 'PIB_Mrd'),
    "inflation": top_bottom(m24, 'Inflation'),
    "fdi": top_bottom(m24, 'FDI_entrants'),
    "mobile_money": top_bottom(f24, 'Pop_MM'),
    "dette": top_bottom(m24, 'Dette_publique'),
    "credit_pib": top_bottom(b24, 'Credit_PIB'),
    "score_inclusion": top_bottom(mfi24, 'Score_inclusion'),
}

# --- Country detail data (for selector) ---
country_list = sorted(macro['Pays'].unique().tolist())

# Per-country time series for interactive selector
country_macro_ts = {}
for pays in country_list:
    df_p = macro[macro['Pays']==pays].sort_values('Annee')
    country_macro_ts[pays] = {
        'annees': df_p['Annee'].tolist(),
        'pib': [safe_float(v) for v in df_p['PIB_Mrd']],
        'croissance': [safe_float(v) for v in df_p['Croissance_PIB']],
        'inflation': [safe_float(v) for v in df_p['Inflation']],
        'dette': [safe_float(v) for v in df_p['Dette_publique']],
        'fdi': [safe_float(v) for v in df_p['FDI_entrants']],
        'chomage': [safe_float(v) for v in df_p['Chomage']],
    }

country_bank_ts = {}
for pays in country_list:
    df_p = bank[bank['Pays']==pays].sort_values('Annee')
    country_bank_ts[pays] = {
        'annees': df_p['Annee'].tolist(),
        'bancarisation': [safe_float(v) for v in df_p['Bancarisation']],
        'npl': [safe_float(v) for v in df_p['NPL']],
        'car': [safe_float(v) for v in df_p['CAR']],
        'roe': [safe_float(v) for v in df_p['ROE']],
        'nim': [safe_float(v) for v in df_p['NIM']],
        'credit_pib': [safe_float(v) for v in df_p['Credit_PIB']],
    }

country_fintech_ts = {}
for pays in country_list:
    df_p = fintech[fintech['Pays']==pays].sort_values('Annee')
    country_fintech_ts[pays] = {
        'annees': df_p['Annee'].tolist(),
        'comptes_mm': [safe_float(v) for v in df_p['Comptes_MM']],
        'transactions_mm': [safe_float(v) for v in df_p['Transactions_MM']],
        'pop_mm': [safe_float(v) for v in df_p['Pop_MM']],
        'startups': [safe_float(v) for v in df_p['Nb_startups_fintech']],
    }

# --- Correlations matrix ---
corr_data = []
try:
    corr_clean = corr_raw.iloc[2:].copy()
    corr_clean.columns = corr_raw.iloc[1].tolist()
    corr_labels = corr_clean.iloc[:,0].tolist()
    corr_values = []
    for _, row in corr_clean.iterrows():
        row_vals = []
        for c in corr_clean.columns[1:]:
            row_vals.append(safe_float(row[c]))
        corr_values.append(row_vals)
    corr_data = {"labels": [str(l) for l in corr_labels], "values": corr_values}
except Exception as e:
    print(f"⚠️ Correlation parse error: {e}")
    corr_data = {"labels": [], "values": []}

# --- Crises data ---
crises_list = df_to_records(crises[['Pays','Region','Annee','Type_crise','Severite',
                                     'Impact_PIB','Hausse_NPL','Aide_FMI','Duree_trim']].dropna(subset=['Pays']))

# --- Profil pays for map ---
profil_list = df_to_records(profil.dropna(subset=['Pays']))

# --- Stats descriptives ---
stats_list = df_to_records(stats.dropna(subset=['Region']))

# --- Scatter plot data: PIB/hab vs Bancarisation 2024 ---
scatter_data = []
merged_24 = m24.merge(b24[['Pays','Bancarisation','NPL','Credit_PIB']], on='Pays', how='inner')
merged_24 = merged_24.merge(f24[['Pays','Pop_MM']], on='Pays', how='left')
for _, row in merged_24.iterrows():
    scatter_data.append({
        'pays': row['Pays'],
        'region': row['Region_x'] if 'Region_x' in row else row.get('Region',''),
        'pib_hab': safe_float(row['PIB_hab']),
        'bancarisation': safe_float(row['Bancarisation']),
        'npl': safe_float(row['NPL']),
        'credit_pib': safe_float(row['Credit_PIB']),
        'pop_mm': safe_float(row.get('Pop_MM', 0)),
        'pib': safe_float(row['PIB_Mrd']),
    })

# --- Markets data ---
markets_2024 = markets[markets['Annee']==2024]
markets_list = df_to_records(markets_2024[['Pays','Bourse','Capitalisation_Mrd',
    'Capitalisation_PIB','Nb_cotees','Spread_souverain','Notation','Liquidite','Volatilite']].dropna(subset=['Pays']))

markets_ts = markets.groupby('Annee').agg(
    Cap_totale=('Capitalisation_Mrd','sum'),
    Spread_moy=('Spread_souverain','mean'),
    Nb_cotees_total=('Nb_cotees','sum'),
    Volume_total=('Volume_Mrd','sum'),
).reset_index()

print("✅ Aggregates computed.")

# ─── ISO-3 COUNTRY CODES FOR CHOROPLETH MAPS ────────────────────────────────

ISO3_MAP = {
    "Afrique du Sud":"ZAF","Algérie":"DZA","Angola":"AGO","Bénin":"BEN",
    "Botswana":"BWA","Burkina Faso":"BFA","Burundi":"BDI","Cabo Verde":"CPV",
    "Cameroun":"CMR","Centrafrique":"CAF","Comores":"COM","Congo":"COG",
    "Côte d'Ivoire":"CIV","Djibouti":"DJI","Égypte":"EGY","Érythrée":"ERI",
    "Eswatini":"SWZ","Éthiopie":"ETH","Gabon":"GAB","Gambie":"GMB",
    "Ghana":"GHA","Guinée":"GIN","Guinée-Bissau":"GNB","Guinée équatoriale":"GNQ",
    "Kenya":"KEN","Lesotho":"LSO","Liberia":"LBR","Libye":"LBY",
    "Madagascar":"MDG","Malawi":"MWI","Mali":"MLI","Maroc":"MAR",
    "Maurice":"MUS","Mauritanie":"MRT","Mozambique":"MOZ","Namibie":"NAM",
    "Niger":"NER","Nigeria":"NGA","Ouganda":"UGA","RD Congo":"COD",
    "Rwanda":"RWA","São Tomé":"STP","Sénégal":"SEN","Sierra Leone":"SLE",
    "Somalie":"SOM","Soudan":"SDN","Soudan du Sud":"SSD","Tanzanie":"TZA",
    "Tchad":"TCD","Togo":"TGO","Tunisie":"TUN","Zambie":"ZMB","Zimbabwe":"ZWE",
}

# --- Choropleth map data by year ---
print("🗺️ Building choropleth data...")
choropleth_years = sorted(macro['Annee'].unique().tolist())
choropleth_data = {}
for year in choropleth_years:
    my = macro[macro['Annee']==year]
    by = bank[bank['Annee']==year]
    fy = fintech[fintech['Annee']==year]
    mfiy = mfi[mfi['Annee']==year]
    
    year_data = {}
    for _, row in my.iterrows():
        pays = row['Pays']
        iso3 = ISO3_MAP.get(pays, '')
        if not iso3:
            continue
        br = by[by['Pays']==pays]
        fr = fy[fy['Pays']==pays]
        mr = mfiy[mfiy['Pays']==pays]
        year_data[iso3] = {
            'pays': pays,
            'pib': safe_float(row['PIB_Mrd']),
            'croissance': safe_float(row['Croissance_PIB']),
            'pib_hab': safe_float(row['PIB_hab']),
            'inflation': safe_float(row['Inflation']),
            'dette': safe_float(row['Dette_publique']),
            'fdi': safe_float(row['FDI_entrants']),
            'chomage': safe_float(row['Chomage']),
            'bancarisation': safe_float(br.iloc[0]['Bancarisation']) if len(br) else None,
            'npl': safe_float(br.iloc[0]['NPL']) if len(br) else None,
            'car': safe_float(br.iloc[0]['CAR']) if len(br) else None,
            'roe': safe_float(br.iloc[0]['ROE']) if len(br) else None,
            'credit_pib': safe_float(br.iloc[0]['Credit_PIB']) if len(br) else None,
            'pop_mm': safe_float(fr.iloc[0]['Pop_MM']) if len(fr) else None,
            'comptes_mm': safe_float(fr.iloc[0]['Comptes_MM']) if len(fr) else None,
            'score_inclusion': safe_float(mr.iloc[0]['Score_inclusion']) if len(mr) else None,
            'par30': safe_float(mr.iloc[0]['PAR30']) if len(mr) else None,
        }
    choropleth_data[str(year)] = year_data

# --- Radar chart data by region ---
radar_regions = {}
for _, row in regions_bank.iterrows():
    reg = row['Region']
    rm = regions_macro[regions_macro['Region']==reg]
    rf = regions_fintech[regions_fintech['Region']==reg]
    radar_regions[reg] = {
        'bancarisation': safe_float(row['Bancarisation_moy']),
        'car': safe_float(row['CAR_moy']),
        'roe': safe_float(row['ROE_moy']),
        'credit_pib': safe_float(row['Credit_PIB_moy']),
        'npl_inv': round(20 - (safe_float(row['NPL_moy']) or 0), 1),
        'croissance': safe_float(rm.iloc[0]['Croissance_moy']) if len(rm) else None,
        'mm': safe_float(rf.iloc[0]['Pop_MM_moy']) if len(rf) else None,
    }

# --- Treemap data PIB 2024 ---
treemap_data = []
for _, row in m24.iterrows():
    treemap_data.append({
        'pays': row['Pays'],
        'region': row['Region'],
        'pib': safe_float(row['PIB_Mrd']),
        'croissance': safe_float(row['Croissance_PIB']),
    })

# ─── ADVANCED STATISTICS ─────────────────────────────────────────────────────

print("📐 Computing advanced statistics...")

# Merge key variables for cross-sectional analysis (latest year per country)
stat_df = macro.merge(bank[['Pays','Annee','Bancarisation','NPL','CAR','ROE','Credit_PIB']],
                      on=['Pays','Annee'], how='left') \
               .merge(fintech[['Pays','Annee','Pop_MM','Comptes_MM','Nb_startups_fintech']],
                      on=['Pays','Annee'], how='left') \
               .merge(mfi[['Pays','Annee','Score_inclusion','PAR30','Portefeuille_M']],
                      on=['Pays','Annee'], how='left')

# Latest year cross-section for each country
stat_latest = stat_df.sort_values('Annee').groupby('Pays').last().reset_index()

# ── 1. Descriptive Statistics ──
desc_vars = ['PIB_Mrd','Croissance_PIB','PIB_hab','Inflation','Dette_publique','Chomage',
             'Bancarisation','NPL','CAR','ROE','Credit_PIB','Pop_MM','Score_inclusion','FDI_entrants']
desc_stats = {}
for v in desc_vars:
    s = stat_latest[v].dropna()
    if len(s) < 3:
        continue
    desc_stats[v] = {
        'n': int(len(s)),
        'mean': round(float(s.mean()), 2),
        'median': round(float(s.median()), 2),
        'std': round(float(s.std()), 2),
        'min': round(float(s.min()), 2),
        'max': round(float(s.max()), 2),
        'q1': round(float(s.quantile(0.25)), 2),
        'q3': round(float(s.quantile(0.75)), 2),
        'skew': round(float(s.skew()), 3),
        'kurtosis': round(float(s.kurtosis()), 3),
        'cv': round(float(s.std() / s.mean() * 100), 1) if s.mean() != 0 else None,
    }

# ── 2. Linear Regressions ──
reg_pairs = [
    ('PIB_hab', 'Bancarisation', 'PIB/hab → Bancarisation'),
    ('PIB_hab', 'Credit_PIB', 'PIB/hab → Crédit/PIB'),
    ('Bancarisation', 'Score_inclusion', 'Bancarisation → Score Inclusion'),
    ('Pop_MM', 'Bancarisation', 'Mobile Money → Bancarisation'),
    ('Inflation', 'Croissance_PIB', 'Inflation → Croissance'),
    ('NPL', 'Croissance_PIB', 'NPL → Croissance'),
    ('Dette_publique', 'Croissance_PIB', 'Dette → Croissance'),
    ('FDI_entrants', 'Croissance_PIB', 'FDI → Croissance'),
    ('Urbanisation', 'Bancarisation', 'Urbanisation → Bancarisation'),
    ('IDH', 'Bancarisation', 'IDH → Bancarisation'),
]
regressions = []
for xvar, yvar, label in reg_pairs:
    tmp = stat_latest[[xvar, yvar, 'Pays']].dropna()
    if len(tmp) < 5:
        continue
    x = tmp[xvar].values.astype(float)
    y = tmp[yvar].values.astype(float)
    slope, intercept, r_value, p_value, std_err = sp_stats.linregress(x, y)
    regressions.append({
        'label': label,
        'xvar': xvar, 'yvar': yvar,
        'n': int(len(tmp)),
        'r2': round(r_value**2, 4),
        'r': round(r_value, 4),
        'slope': round(slope, 6),
        'intercept': round(intercept, 4),
        'p_value': float(f"{p_value:.2e}") if p_value < 0.001 else round(p_value, 4),
        'std_err': round(std_err, 6),
        'significant': bool(p_value < 0.05),
        'points': [{'x': round(float(tmp.iloc[i][xvar]),2), 'y': round(float(tmp.iloc[i][yvar]),2),
                     'pays': tmp.iloc[i]['Pays']} for i in range(len(tmp))],
    })

# ── 3. ANOVA (by Region) ──
anova_vars = ['Croissance_PIB','Bancarisation','NPL','Inflation','Credit_PIB','Pop_MM','Score_inclusion','PIB_hab']
anova_results = []
stat_with_region = stat_latest.dropna(subset=['Region'])
for v in anova_vars:
    groups = [g[v].dropna().values for _, g in stat_with_region.groupby('Region') if len(g[v].dropna()) >= 2]
    if len(groups) < 2:
        continue
    F, p = sp_stats.f_oneway(*groups)
    if math.isnan(F):
        continue
    # Compute group means for chart
    gmeans = []
    for reg, g in stat_with_region.groupby('Region'):
        vals = g[v].dropna()
        if len(vals) >= 1:
            gmeans.append({'region': reg, 'mean': round(float(vals.mean()), 2),
                          'std': round(float(vals.std()), 2), 'n': int(len(vals))})
    anova_results.append({
        'variable': v,
        'F': round(float(F), 3),
        'p_value': float(f"{p:.2e}") if p < 0.001 else round(p, 4),
        'significant': bool(p < 0.05),
        'groups': gmeans,
        'k': len(groups),
        'N': sum(len(g) for g in groups),
    })

# ── 4. Normality Tests (Shapiro-Wilk) ──
normality_tests = []
for v in desc_vars:
    s = stat_latest[v].dropna()
    if 3 <= len(s) <= 5000:
        W, p = sp_stats.shapiro(s)
        normality_tests.append({
            'variable': v, 'W': round(float(W), 4),
            'p_value': float(f"{p:.2e}") if p < 0.001 else round(p, 4),
            'normal': bool(p > 0.05), 'n': int(len(s)),
        })

# ── 5. Non-parametric tests: Kruskal-Wallis ──
kruskal_results = []
for v in anova_vars:
    groups = [g[v].dropna().values for _, g in stat_with_region.groupby('Region') if len(g[v].dropna()) >= 2]
    if len(groups) < 2:
        continue
    H, p = sp_stats.kruskal(*groups)
    if not math.isnan(H):
        kruskal_results.append({
            'variable': v, 'H': round(float(H), 3),
            'p_value': float(f"{p:.2e}") if p < 0.001 else round(p, 4),
            'significant': bool(p < 0.05),
        })

# ── 6. Spearman Rank Correlations ──
spearman_vars = ['PIB_hab','Bancarisation','NPL','Inflation','Credit_PIB','Pop_MM','Croissance_PIB','IDH','Score_inclusion']
spearman_matrix = {'labels': [], 'rho': [], 'pval': []}
available_spearman = [v for v in spearman_vars if stat_latest[v].notna().sum() >= 5]
spearman_matrix['labels'] = available_spearman
for v1 in available_spearman:
    rho_row, p_row = [], []
    for v2 in available_spearman:
        tmp = stat_latest[[v1, v2]].dropna()
        if len(tmp) >= 5:
            res = sp_stats.spearmanr(tmp[v1].values, tmp[v2].values)
            rho = float(np.asarray(res.statistic).flat[0]) if hasattr(res, 'statistic') else float(res[0])
            p = float(np.asarray(res.pvalue).flat[0]) if hasattr(res, 'pvalue') else float(res[1])
            rho_row.append(round(rho, 3) if not math.isnan(rho) else None)
            p_row.append(round(p, 4) if not math.isnan(p) else None)
        else:
            rho_row.append(None)
            p_row.append(None)
    spearman_matrix['rho'].append(rho_row)
    spearman_matrix['pval'].append(p_row)

# ── 7. Time-series trend analysis (Mann-Kendall style via Spearman on time) ──
trend_analysis = []
trend_vars_ts = ['PIB_Mrd','Croissance_PIB','Inflation','Dette_publique','Bancarisation','NPL','Pop_MM','Score_inclusion']
for v in trend_vars_ts:
    ts_agg = stat_df.groupby('Annee')[v].mean().dropna()
    if len(ts_agg) < 5:
        continue
    res_t = sp_stats.spearmanr(np.array(ts_agg.index), ts_agg.values)
    rho = float(np.asarray(res_t.statistic).flat[0])
    p = float(np.asarray(res_t.pvalue).flat[0])
    direction = 'hausse' if rho > 0 else 'baisse'
    trend_analysis.append({
        'variable': v, 'rho': round(float(rho), 3),
        'p_value': round(float(p), 4), 'significant': bool(p < 0.05),
        'direction': direction, 'n_years': int(len(ts_agg)),
        'ts': [{'year': int(y), 'value': round(float(val), 2)} for y, val in ts_agg.items()],
    })

# ── 8. Distribution data (histograms + box plots) ──
distribution_data = {}
for v in desc_vars:
    s = stat_latest[v].dropna()
    if len(s) < 3:
        continue
    distribution_data[v] = {
        'values': [round(float(x), 2) for x in s.tolist()],
        'pays': stat_latest.loc[s.index, 'Pays'].tolist(),
    }

# ── 9. Outlier detection (IQR method) ──
outliers_data = {}
for v in desc_vars:
    s = stat_latest[['Pays', v]].dropna()
    if len(s) < 5:
        continue
    q1, q3 = s[v].quantile(0.25), s[v].quantile(0.75)
    iqr = q3 - q1
    low, high = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    out = s[(s[v] < low) | (s[v] > high)]
    if len(out) > 0:
        outliers_data[v] = [{'pays': r['Pays'], 'value': round(float(r[v]), 2)} for _, r in out.iterrows()]

# ── 10. Panel regression: PIB growth ~ macro factors (pooled OLS) ──
panel_vars = ['Inflation','Dette_publique','FDI_entrants','Chomage','Bancarisation','Credit_PIB']
panel_df = stat_df[['Pays','Annee','Croissance_PIB'] + panel_vars].dropna()
panel_reg = None
if len(panel_df) > 50:
    from numpy.linalg import lstsq
    X_cols = panel_vars
    X = panel_df[X_cols].values.astype(float)
    y_panel = panel_df['Croissance_PIB'].values.astype(float)
    X_aug = np.column_stack([np.ones(len(X)), X])
    coeffs, residuals, rank, sv = lstsq(X_aug, y_panel, rcond=None)
    y_pred = X_aug @ coeffs
    ss_res = float(np.sum((y_panel - y_pred)**2))
    ss_tot = float(np.sum((y_panel - y_panel.mean())**2))
    r2_panel = 1 - ss_res / ss_tot if ss_tot > 0 else 0
    n_p, k_p = len(y_panel), len(X_cols)
    r2_adj = 1 - (1 - r2_panel) * (n_p - 1) / (n_p - k_p - 1)
    mse = ss_res / (n_p - k_p - 1) if n_p > k_p + 1 else 0
    se_coeffs = np.sqrt(np.diag(mse * np.linalg.inv(X_aug.T @ X_aug))) if mse > 0 else np.zeros(k_p + 1)
    t_stats = coeffs / se_coeffs if mse > 0 else np.zeros(k_p + 1)
    p_vals = [float(2 * (1 - sp_stats.t.cdf(abs(t), n_p - k_p - 1))) for t in t_stats]
    panel_reg = {
        'dep_var': 'Croissance_PIB',
        'r2': round(r2_panel, 4), 'r2_adj': round(r2_adj, 4),
        'n': n_p, 'k': k_p,
        'coefficients': [{'var': 'Intercept' if i == 0 else X_cols[i-1],
                          'coeff': round(float(coeffs[i]), 4),
                          'se': round(float(se_coeffs[i]), 4),
                          't': round(float(t_stats[i]), 3),
                          'p': round(float(p_vals[i]), 4),
                          'sig': bool(p_vals[i] < 0.05)} for i in range(len(coeffs))],
    }

advanced_stats = {
    'descriptive': desc_stats,
    'regressions': regressions,
    'anova': anova_results,
    'normality': normality_tests,
    'kruskal': kruskal_results,
    'spearman': spearman_matrix,
    'trends': trend_analysis,
    'distributions': distribution_data,
    'outliers': outliers_data,
    'panel_regression': panel_reg,
}

print(f"  ✅ {len(regressions)} régressions, {len(anova_results)} ANOVA, {len(normality_tests)} tests normalité, {len(trend_analysis)} tendances")

# ─── BUILD JSON DATA PAYLOAD ─────────────────────────────────────────────────

print("🔧 Building JSON payload...")

dashboard_data = {
    "kpis": kpis,
    "ts_continental": df_to_records(ts_continental),
    "ts_banking": df_to_records(ts_banking),
    "ts_fintech": df_to_records(ts_fintech),
    "ts_mfi": df_to_records(ts_mfi),
    "ts_markets": df_to_records(markets_ts),
    "regions_macro": df_to_records(regions_macro),
    "regions_bank": df_to_records(regions_bank),
    "regions_fintech": df_to_records(regions_fintech),
    "ts_region_growth": df_to_records(ts_region_growth),
    "ts_region_banc": df_to_records(ts_region_banc),
    "ts_region_npl": df_to_records(ts_region_npl),
    "ts_region_mm": df_to_records(ts_region_mm),
    "rankings": rankings_data,
    "country_list": country_list,
    "country_macro": country_macro_ts,
    "country_bank": country_bank_ts,
    "country_fintech": country_fintech_ts,
    "correlations": corr_data,
    "crises": crises_list,
    "profil": profil_list,
    "stats": stats_list,
    "scatter": scatter_data,
    "markets": markets_list,
    "choropleth": choropleth_data,
    "choropleth_years": choropleth_years,
    "radar_regions": radar_regions,
    "treemap": treemap_data,
    "advanced_stats": advanced_stats,
}

data_json = json.dumps(dashboard_data, ensure_ascii=False)
print(f"✅ JSON payload: {len(data_json)//1024} KB")

# ─── HTML TEMPLATE ────────────────────────────────────────────────────────────

print("🎨 Generating professional HTML dashboard...")

html_template = r"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AFRICA FINANCE OBSERVATORY — Dashboard 2000-2024</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
<script src="https://cdn.plot.ly/plotly-2.35.0.min.js"></script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
/* ═══════════════════════════════════════════════════════════════════════════════
   AFRICA FINANCE OBSERVATORY — PREMIUM DARK DASHBOARD v4
   Advanced CSS: Glassmorphism · CSS Grid · Animations · Responsive
═══════════════════════════════════════════════════════════════════════════════ */
:root {
  --bg: #0d1117;
  --bg2: #161b22;
  --bg3: #1c2128;
  --bg4: #21262d;
  --accent: #00e5a0;
  --accent-dim: rgba(0,229,160,0.07);
  --accent2: #a78bfa;
  --accent3: #f59e0b;
  --accent4: #f85149;
  --accent5: #58a6ff;
  --accent6: #f472b6;
  --text: #e6edf3;
  --text2: #8b949e;
  --text3: #6e7681;
  --border: rgba(255,255,255,0.06);
  --border2: rgba(255,255,255,0.1);
  --green: #3fb950;
  --red: #f85149;
  --gold: #d29922;
  --glass: rgba(13,17,23,0.72);
  --glass-border: rgba(255,255,255,0.06);
  --glow: 0 4px 24px rgba(0,229,160,0.10);
  --glow-purple: 0 4px 24px rgba(167,139,250,0.10);
  --glow-blue: 0 4px 24px rgba(88,166,255,0.10);
  --radius: 20px;
  --radius-sm: 12px;
  --radius-xs: 8px;
  --shadow-sm: 0 2px 8px rgba(0,0,0,0.2);
  --shadow-md: 0 8px 32px rgba(0,0,0,0.3);
  --shadow-lg: 0 16px 48px rgba(0,0,0,0.4);
  --transition: cubic-bezier(0.4,0,0.2,1);
}
*,*::before,*::after { margin:0; padding:0; box-sizing:border-box; }
html { scroll-behavior: smooth; }
body {
  font-family: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
  background: var(--bg);
  color: var(--text);
  line-height: 1.6;
  overflow-x: hidden;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  min-height: 100vh;
}
/* Animated background mesh gradient */
body::before {
  content:''; position:fixed; inset:0; z-index:-1; pointer-events:none;
  background:
    radial-gradient(ellipse 80% 60% at 10% 20%, rgba(0,229,160,0.05) 0%, transparent 60%),
    radial-gradient(ellipse 60% 80% at 90% 80%, rgba(167,139,250,0.04) 0%, transparent 60%),
    radial-gradient(ellipse 50% 50% at 50% 50%, rgba(88,166,255,0.03) 0%, transparent 70%);
}

/* ═══ HEADER — Glassmorphism ═══ */
.header {
  background: var(--glass);
  border-bottom: 1px solid var(--glass-border);
  padding: 14px 36px;
  display: flex; align-items: center; justify-content: space-between;
  position: sticky; top: 0; z-index: 100;
  backdrop-filter: blur(24px) saturate(180%);
  -webkit-backdrop-filter: blur(24px) saturate(180%);
  transition: all 0.3s var(--transition);
}
.header.scrolled { padding: 10px 36px; box-shadow: var(--shadow-md); }
.header-brand { display: flex; align-items: center; gap: 16px; }
.header-logo {
  width: 46px; height: 46px; border-radius: 14px;
  background: linear-gradient(135deg, var(--accent) 0%, #047857 50%, var(--accent5) 100%);
  display: flex; align-items: center; justify-content: center;
  font-size: 18px; font-weight: 900; color: #fff; letter-spacing: -1px;
  box-shadow: 0 4px 20px rgba(0,229,160,0.25);
  position: relative; overflow: hidden;
}
.header-logo::after {
  content:''; position:absolute; inset:-50%; 
  background: linear-gradient(135deg, transparent 30%, rgba(255,255,255,0.15) 50%, transparent 70%);
  animation: logoShine 4s ease-in-out infinite;
}
@keyframes logoShine { 0%{transform:rotate(0deg)} 100%{transform:rotate(360deg)} }
.header h1 { font-size: 21px; font-weight: 800; letter-spacing: -0.8px; line-height:1.2; }
.header h1 span {
  background: linear-gradient(90deg, var(--accent), #00ffc8, var(--accent5), #a78bfa, var(--accent), #00ffc8);
  background-size: 300% 100%;
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  background-clip: text;
  animation: titleShimmer 6s ease-in-out infinite;
  filter: drop-shadow(0 0 12px rgba(0,229,160,0.3));
}
@keyframes titleShimmer {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}
.header h1 .obs-text {
  color: var(--text);
  -webkit-text-fill-color: var(--text);
  background: none;
  font-weight: 300;
  letter-spacing: 3px;
  text-transform: uppercase;
  font-size: 0.7em;
  opacity: 0.85;
  margin-left: 4px;
  position: relative;
}
.header h1 .obs-text::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 0;
  width: 100%;
  height: 1.5px;
  background: linear-gradient(90deg, var(--accent), transparent);
  animation: underlineGlow 3s ease-in-out infinite alternate;
}
@keyframes underlineGlow {
  0% { opacity: 0.3; transform: scaleX(0.5); transform-origin: left; }
  100% { opacity: 1; transform: scaleX(1); transform-origin: left; }
}
.header-sub { font-size: 11.5px; color: var(--text2); font-weight: 400; margin-top: 2px; letter-spacing: 0.2px; }
.header-actions { display: flex; gap: 10px; align-items: center; flex-wrap: wrap; }
.header-badge {
  background: var(--bg3); border: 1px solid var(--border2);
  border-radius: 24px; padding: 6px 16px; font-size: 11px;
  color: var(--text2); font-weight: 600; letter-spacing: 0.3px;
  transition: all 0.25s var(--transition);
}
.header-badge:hover { border-color: var(--accent); color: var(--text); }
.header-badge.live { 
  color: var(--accent); border-color: rgba(0,229,160,0.25);
  background: rgba(0,229,160,0.06);
}
.header-badge.live::before { content:'●'; margin-right:6px; animation:pulse 2s infinite; font-size:8px; }
@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.2} }

/* Buttons */
.btn-export {
  background: linear-gradient(135deg, var(--accent), #047857);
  color: #fff; border: none; padding: 9px 22px; border-radius: var(--radius-sm);
  font-size: 12px; font-weight: 700; cursor: pointer;
  transition: all 0.3s var(--transition); letter-spacing: 0.3px;
  font-family: 'Inter',sans-serif;
  box-shadow: 0 4px 15px rgba(0,229,160,0.2);
  position: relative; overflow: hidden;
}
.btn-export::before {
  content:''; position:absolute; top:0; left:-100%; width:100%; height:100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
  transition: left 0.5s;
}
.btn-export:hover::before { left: 100%; }
.btn-export:hover { transform: translateY(-2px); box-shadow: 0 8px 25px rgba(0,229,160,0.3); }
.btn-export:active { transform: translateY(0); }

.btn-lang {
  background: rgba(124,58,237,0.08); border: 1px solid rgba(124,58,237,0.25);
  color: var(--accent2); padding: 8px 16px; border-radius: var(--radius-sm);
  font-size: 12px; font-weight: 700; cursor: pointer;
  transition: all 0.3s var(--transition); letter-spacing: 0.5px;
  font-family: 'Inter',sans-serif;
}
.btn-lang:hover { 
  background: rgba(139,92,246,0.2); transform: translateY(-2px); 
  box-shadow: var(--glow-purple); border-color: rgba(139,92,246,0.5);
}
.btn-lang .flag { font-size: 14px; margin-right: 4px; }

/* ═══ NAV — Pill-style tabs ═══ */
.nav-wrap {
  background: var(--glass); 
  border-bottom: 1px solid var(--glass-border);
  padding: 0 36px; 
  position: sticky; top: 74px; z-index: 99;
  backdrop-filter: blur(20px) saturate(160%);
  -webkit-backdrop-filter: blur(20px) saturate(160%);
}
.nav {
  display: flex; gap: 4px; overflow-x: auto; scrollbar-width: none;
  -ms-overflow-style: none; padding: 10px 0;
  scroll-snap-type: x mandatory;
}
.nav::-webkit-scrollbar { display:none; }
.nav button {
  background: transparent; border: 1px solid transparent; color: var(--text2);
  padding: 10px 20px; border-radius: var(--radius-sm);
  cursor: pointer; font-size: 13px; font-weight: 500;
  white-space: nowrap; transition: all 0.3s var(--transition);
  font-family: 'Inter', sans-serif; position: relative;
  scroll-snap-align: start;
}
.nav button:hover { 
  background: rgba(255,255,255,0.04); color: var(--text); 
  border-color: var(--border2);
}
.nav button.active {
  background: var(--accent-dim); color: var(--accent); font-weight: 700;
  border-color: rgba(0,229,160,0.15);
  box-shadow: 0 0 20px rgba(0,229,160,0.06);
}
.nav button.active::after {
  content:''; position:absolute; bottom:-1px; left:25%; width:50%;
  height: 2.5px; background: linear-gradient(90deg, transparent, var(--accent), transparent); 
  border-radius: 2px;
}

/* ═══ MAIN CONTAINER ═══ */
.main { padding: 30px 36px; max-width: 1720px; margin: 0 auto; }

/* Section animations */
.section { display: none; animation: sectionIn 0.4s var(--transition); }
.section.active { display: block; }
@keyframes sectionIn { 
  from { opacity:0; transform:translateY(12px); filter:blur(4px); } 
  to { opacity:1; transform:translateY(0); filter:blur(0); } 
}

/* ═══ KPI GRID — Premium cards ═══ */
.kpi-grid {
  display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 16px; margin-bottom: 32px;
}
.kpi-card {
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: var(--radius); padding: 24px 22px;
  position: relative; overflow: hidden;
  transition: all 0.35s var(--transition);
  cursor: default;
}
.kpi-card::before {
  content:''; position:absolute; top:0; left:0; right:0; height:2.5px;
  background: linear-gradient(90deg, transparent, var(--accent), transparent);
  opacity:0; transition: opacity 0.3s;
}
.kpi-card:hover::before { opacity:1; }
.kpi-card::after {
  content:''; position:absolute; inset:0; 
  background: radial-gradient(circle at 50% 0%, rgba(0,229,160,0.04), transparent 70%);
  opacity:0; transition: opacity 0.3s;
}
.kpi-card:hover::after { opacity:1; }
.kpi-card:hover { 
  border-color: rgba(0,229,160,0.2); 
  box-shadow: var(--glow); 
  transform: translateY(-4px); 
}
.kpi-card .kpi-icon {
  width: 40px; height: 40px; border-radius: var(--radius-sm);
  display: flex; align-items: center; justify-content: center;
  font-size: 18px; margin-bottom: 14px; position: relative; z-index: 1;
}
.kpi-card .kpi-icon.teal { background: rgba(0,229,160,0.1); box-shadow: 0 2px 12px rgba(0,229,160,0.08); }
.kpi-card .kpi-icon.blue { background: rgba(88,166,255,0.1); box-shadow: 0 2px 12px rgba(88,166,255,0.08); }
.kpi-card .kpi-icon.purple { background: rgba(167,139,250,0.1); box-shadow: 0 2px 12px rgba(167,139,250,0.08); }
.kpi-card .kpi-icon.gold { background: rgba(245,158,11,0.1); box-shadow: 0 2px 12px rgba(245,158,11,0.08); }
.kpi-card .kpi-icon.red { background: rgba(248,81,73,0.1); box-shadow: 0 2px 12px rgba(248,81,73,0.08); }
.kpi-card .kpi-icon.pink { background: rgba(244,114,182,0.1); box-shadow: 0 2px 12px rgba(244,114,182,0.08); }
.kpi-label { font-size: 10.5px; color: var(--text2); text-transform: uppercase; letter-spacing: 1px; font-weight: 700; margin-bottom: 8px; position:relative; z-index:1; }
.kpi-value { font-size: 32px; font-weight: 900; letter-spacing: -1.5px; font-family: 'Inter',sans-serif; position:relative; z-index:1; line-height:1.1; }
.kpi-value.teal { color: var(--accent); }
.kpi-value.blue { color: var(--accent5); }
.kpi-value.purple { color: var(--accent2); }
.kpi-value.gold { color: var(--accent3); }
.kpi-value.red { color: var(--red); }
.kpi-value.pink { color: var(--accent6); }
.kpi-sub { font-size: 11px; color: var(--text3); margin-top: 6px; font-weight: 400; position:relative; z-index:1; }

/* ═══ CHART CONTAINERS — Glassmorphism cards ═══ */
.chart-row { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 24px; }
.chart-row.triple { grid-template-columns: repeat(3, 1fr); }
.chart-row.single { grid-template-columns: 1fr; }
.chart-row.r31 { grid-template-columns: 1.8fr 1fr; }
.chart-row.r13 { grid-template-columns: 1fr 1.8fr; }

.chart-box {
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: var(--radius); padding: 24px; min-height: 400px;
  position: relative; overflow: hidden;
  transition: all 0.35s var(--transition);
}
.chart-box::before {
  content:''; position:absolute; top:0; left:0; right:0; height:1px;
  background: linear-gradient(90deg, transparent 0%, rgba(255,255,255,0.06) 50%, transparent 100%);
}
.chart-box:hover { 
  border-color: var(--border2); 
  box-shadow: var(--shadow-sm);
}
.chart-box h3 {
  font-size: 14px; font-weight: 700; margin-bottom: 16px;
  color: var(--text); display: flex; align-items: center; gap: 10px;
  letter-spacing: -0.3px;
}
.chart-box h3 .icon {
  width: 30px; height: 30px; border-radius: var(--radius-xs);
  display: inline-flex; align-items: center; justify-content: center;
  font-size: 14px; background: var(--bg4);
  box-shadow: inset 0 1px 0 rgba(255,255,255,0.05);
}
.chart-box .chart-actions {
  position: absolute; top: 20px; right: 20px;
  display: flex; gap: 6px; z-index: 10; opacity: 0;
  transition: opacity 0.25s var(--transition);
}
.chart-box:hover .chart-actions { opacity: 1; }
.chart-box .chart-actions button {
  background: var(--bg2); border: 1px solid var(--border2);
  color: var(--text2); padding: 5px 12px; border-radius: var(--radius-xs);
  font-size: 10px; cursor: pointer; font-weight: 600;
  transition: all 0.2s var(--transition); font-family: 'Inter',sans-serif;
  backdrop-filter: blur(8px);
  box-shadow: var(--shadow-sm);
}
.chart-box .chart-actions button:hover { 
  background: rgba(0,229,160,0.08); color: var(--accent); border-color: rgba(0,229,160,0.3); 
}
.chart-div { width: 100%; height: 360px; }
.chart-div.tall { height: 480px; }
.chart-div.xtall { height: 560px; }
.chart-div.short { height: 280px; }

/* ═══ CONTROLS — Polished form elements ═══ */
.controls {
  display: flex; gap: 16px; margin-bottom: 24px;
  align-items: center; flex-wrap: wrap;
  padding: 16px 20px; border-radius: var(--radius);
  background: var(--bg2); border: 1px solid var(--border);
}
.controls label {
  font-size: 11px; color: var(--text2); font-weight: 700;
  text-transform: uppercase; letter-spacing: 0.8px;
}
select {
  background: var(--bg4); border: 1px solid var(--border2);
  color: var(--text); padding: 10px 18px; border-radius: var(--radius-sm);
  font-size: 13px; cursor: pointer; outline: none;
  font-family: 'Inter',sans-serif; font-weight: 500;
  transition: all 0.3s var(--transition);
  -webkit-appearance: none; -moz-appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' fill='%238b949e' viewBox='0 0 16 16'%3E%3Cpath d='M1.5 5.5l6.5 6.5 6.5-6.5'/%3E%3C/svg%3E");
  background-repeat: no-repeat; background-position: right 12px center;
  padding-right: 36px;
}
select:hover { border-color: var(--text3); }
select:focus { border-color: var(--accent); box-shadow: 0 0 0 3px rgba(0,229,160,0.1); }

input[type=range] {
  -webkit-appearance: none; width: 300px; height: 6px;
  background: linear-gradient(90deg, var(--accent), var(--accent5));
  border-radius: 3px; outline: none; opacity: 0.8;
}
input[type=range]:hover { opacity: 1; }
input[type=range]::-webkit-slider-thumb {
  -webkit-appearance: none; width: 20px; height: 20px;
  background: var(--accent); border-radius: 50%; cursor: pointer;
  border: 3px solid var(--bg2); box-shadow: 0 2px 8px rgba(0,229,160,0.3);
  transition: box-shadow 0.2s;
}
input[type=range]::-webkit-slider-thumb:hover {
  box-shadow: 0 2px 12px rgba(0,229,160,0.5);
}
.year-display {
  font-family: 'JetBrains Mono', monospace; font-size: 30px;
  font-weight: 700; color: var(--accent); min-width: 60px;
}

/* ═══ TABLES — Premium ═══ */
.data-table { width:100%; border-collapse: separate; border-spacing: 0; font-size: 12px; }
.data-table th {
  background: var(--bg3); padding: 14px 16px; text-align: left;
  font-weight: 700; color: var(--accent); border-bottom: 2px solid rgba(0,229,160,0.2);
  font-size: 10.5px; text-transform: uppercase; letter-spacing: 0.8px;
  position: sticky; top: 0; z-index: 2;
}
.data-table th:first-child { border-radius: var(--radius-xs) 0 0 0; }
.data-table th:last-child { border-radius: 0 var(--radius-xs) 0 0; }
.data-table td { 
  padding: 12px 16px; border-bottom: 1px solid var(--border); color: var(--text); 
  transition: background 0.15s;
}
.data-table tr:hover td { background: rgba(0,229,160,0.04); }
.data-table tr:last-child td:first-child { border-radius: 0 0 0 var(--radius-xs); }
.data-table tr:last-child td:last-child { border-radius: 0 0 var(--radius-xs) 0; }
.table-container {
  max-height: 520px; overflow-y: auto; border-radius: var(--radius);
  border: 1px solid var(--border); background: var(--bg2); margin-bottom: 24px;
  box-shadow: var(--shadow-sm);
}

/* ═══ SECTION HEADERS — Premium ═══ */
.section-header {
  display: flex; align-items: center; gap: 16px; margin-bottom: 28px;
  padding-bottom: 20px; border-bottom: 1px solid var(--border);
  position: relative;
}
.section-header::after {
  content:''; position:absolute; bottom:-1px; left:0; width:120px; height:2px;
  background: linear-gradient(90deg, var(--accent), transparent);
  border-radius: 2px;
}
.section-header h2 { font-size: 24px; font-weight: 800; letter-spacing: -0.8px; line-height:1.2; }
.section-header .tag {
  background: linear-gradient(135deg, rgba(0,229,160,0.08), rgba(88,166,255,0.06));
  padding: 6px 16px; border-radius: 24px;
  font-size: 10.5px; color: var(--accent); font-weight: 700;
  border: 1px solid rgba(0,229,160,0.18); letter-spacing: 0.5px;
}

/* ═══ SEVERITY ═══ */
.sev-1{color:#86efac} .sev-2{color:#fde047} .sev-3{color:#fb923c}
.sev-4{color:#f87171} .sev-5{color:#dc2626;font-weight:700}

/* ═══ FOOTER — Glass ═══ */
.footer {
  text-align: center; padding: 36px 40px; 
  border-top: 1px solid var(--border);
  color: var(--text3); font-size: 12px; margin-top: 56px;
  background: var(--bg2);
  position: relative;
}
.footer::before {
  content:''; position:absolute; top:0; left:10%; right:10%; height:1px;
  background: linear-gradient(90deg, transparent, var(--accent), transparent);
  opacity: 0.3;
}
.footer strong { color: var(--text2); }

/* ═══ RESPONSIVE — Fully adaptive ═══ */
@media (max-width:1400px) {
  .chart-row.triple { grid-template-columns: 1fr 1fr; }
  .kpi-grid { grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); }
}
@media (max-width:1200px) {
  .chart-row, .chart-row.triple, .chart-row.r31, .chart-row.r13 { grid-template-columns: 1fr; }
  .main { padding: 24px 24px; }
  .header { padding: 12px 24px; }
  .nav-wrap { padding: 0 24px; top: 64px; }
}
@media (max-width:768px) {
  .main { padding: 16px 14px; }
  .kpi-grid { grid-template-columns: repeat(2, 1fr); gap: 10px; }
  .kpi-card { padding: 18px 16px; }
  .kpi-value { font-size: 24px; }
  .header { padding: 10px 14px; flex-wrap: wrap; gap: 10px; }
  .header h1 { font-size: 16px; }
  .header-sub { font-size: 10px; }
  .header-actions { width: 100%; justify-content: flex-end; gap: 6px; }
  .header-badge { font-size: 10px; padding: 4px 10px; }
  .nav-wrap { padding: 0 10px; top: auto; position: relative; }
  .nav { padding: 6px 0; }
  .nav button { padding: 8px 14px; font-size: 12px; }
  .chart-box { padding: 16px; min-height: 320px; border-radius: var(--radius-sm); }
  .chart-div { height: 300px; }
  .chart-div.tall { height: 380px; }
  .section-header h2 { font-size: 18px; }
  .section-header .tag { display: none; }
  .footer { padding: 24px 14px; }
  .controls { padding: 12px 14px; gap: 10px; }
  select { padding: 8px 14px; font-size: 12px; }
  input[type=range] { width: 100%; }
}
@media (max-width:480px) {
  .kpi-grid { grid-template-columns: 1fr; }
  .kpi-card { padding: 16px; }
  .header-brand { gap: 10px; }
  .header-logo { width: 38px; height: 38px; font-size: 15px; }
  .btn-export, .btn-lang { padding: 6px 12px; font-size: 11px; }
  .year-display { font-size: 22px; }
}

/* ═══ SCROLLBAR — Premium thin ═══ */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--border2); border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: var(--accent); }
* { scrollbar-width: thin; scrollbar-color: var(--border2) transparent; }

/* ═══ MODAL — Premium overlay ═══ */
.modal-overlay {
  display: none; position: fixed; inset: 0; z-index: 1000;
  justify-content: center; align-items: center;
  background: rgba(0,0,0,0.6);
  backdrop-filter: blur(8px); -webkit-backdrop-filter: blur(8px);
}
.modal-overlay.active { display: flex; animation: modalIn 0.3s var(--transition); }
@keyframes modalIn { from{opacity:0} to{opacity:1} }
.modal {
  background: var(--bg2);
  border: 1px solid var(--border2);
  border-radius: var(--radius); padding: 36px; max-width: 520px; width: 92%;
  box-shadow: var(--shadow-lg);
  animation: modalSlide 0.35s var(--transition);
}
@keyframes modalSlide { from{transform:translateY(20px);opacity:0} to{transform:translateY(0);opacity:1} }
.modal h3 { font-size: 20px; font-weight: 800; margin-bottom: 12px; color: var(--accent); letter-spacing: -0.5px; }
.modal-btns { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
.modal-btns button {
  padding: 14px; border-radius: var(--radius-sm);
  border: 1px solid var(--border2); background: var(--bg4);
  color: var(--text); font-size: 13px; font-weight: 600; cursor: pointer;
  font-family: 'Inter',sans-serif; transition: all 0.25s var(--transition);
}
.modal-btns button:hover { 
  border-color: var(--accent); color: var(--accent); 
  background: rgba(0,229,160,0.06);
  transform: translateY(-1px);
}
.modal-close {
  margin-top: 16px; width: 100%; padding: 12px; border-radius: var(--radius-sm);
  border: 1px solid var(--border); background: transparent;
  color: var(--text2); font-size: 13px; cursor: pointer;
  font-family: 'Inter',sans-serif; font-weight: 600;
  transition: all 0.2s var(--transition);
}
.modal-close:hover { background: var(--bg4); color: var(--text); }

/* ═══ UTILITY ANIMATIONS ═══ */
@keyframes fadeUp { from{opacity:0;transform:translateY(16px)} to{opacity:1;transform:translateY(0)} }
.chart-box { animation: fadeUp 0.5s var(--transition) backwards; }
.chart-row .chart-box:nth-child(1) { animation-delay: 0.05s; }
.chart-row .chart-box:nth-child(2) { animation-delay: 0.12s; }
.chart-row .chart-box:nth-child(3) { animation-delay: 0.19s; }
.kpi-card { animation: fadeUp 0.4s var(--transition) backwards; }
.kpi-grid .kpi-card:nth-child(1) { animation-delay: 0.02s; }
.kpi-grid .kpi-card:nth-child(2) { animation-delay: 0.05s; }
.kpi-grid .kpi-card:nth-child(3) { animation-delay: 0.08s; }
.kpi-grid .kpi-card:nth-child(4) { animation-delay: 0.11s; }
.kpi-grid .kpi-card:nth-child(5) { animation-delay: 0.14s; }
.kpi-grid .kpi-card:nth-child(6) { animation-delay: 0.17s; }
.kpi-grid .kpi-card:nth-child(7) { animation-delay: 0.20s; }
.kpi-grid .kpi-card:nth-child(8) { animation-delay: 0.23s; }

/* Focus-visible for accessibility */
button:focus-visible, select:focus-visible, input:focus-visible {
  outline: 2px solid var(--accent); outline-offset: 2px;
}

/* Print styles */
@media print {
  .header, .nav-wrap, .chart-actions, .btn-export, .btn-lang, .footer { display: none !important; }
  .section { display: block !important; page-break-inside: avoid; }
  body { background: #0d1117; color: #e6edf3; }
  .chart-box { border: 1px solid #30363d; background: #161b22; }
}
</style>
</head>
<body>

<!-- HEADER -->
<div class="header">
  <div class="header-brand">
    <div class="header-logo">AF</div>
    <div>
      <h1><span>AFRICA FINANCE</span><span class="obs-text">Observatory</span></h1>
      <div class="header-sub" data-i18n="header_sub">54 Countries · 25 Years · 12 Dimensions · 15,000+ Observations — Analytics Dashboard</div>
    </div>
  </div>
  <div class="header-actions">
    <button class="btn-lang" id="btn-lang" onclick="toggleLang()"><span class="flag">🇫🇷</span> FR</button>
    <span class="header-badge">Abdou Samad Faye</span>
    <span class="header-badge live">2000 – 2024</span>
    <button class="btn-export" onclick="openExportModal()">⬇ Export All</button>
  </div>
</div>

<!-- NAV -->
<div class="nav-wrap">
<div class="nav" id="nav">
  <button class="active" onclick="showTab('overview')" data-i18n="nav_overview">📊 Overview</button>
  <button onclick="showTab('choropleth')" data-i18n="nav_choropleth">🗺️ Choropleth Maps</button>
  <button onclick="showTab('macro')" data-i18n="nav_macro">💰 Macroeconomics</button>
  <button onclick="showTab('banking')" data-i18n="nav_banking">🏦 Banking Sector</button>
  <button onclick="showTab('fintech')" data-i18n="nav_fintech">📱 Fintech & M-Money</button>
  <button onclick="showTab('markets')" data-i18n="nav_markets">📈 Markets</button>
  <button onclick="showTab('microfinance')" data-i18n="nav_microfinance">🏘️ Microfinance</button>
  <button onclick="showTab('crises')" data-i18n="nav_crises">⚠️ Crises</button>
  <button onclick="showTab('rankings')" data-i18n="nav_rankings">🏆 Rankings</button>
  <button onclick="showTab('correlations')" data-i18n="nav_correlations">🔗 Correlations</button>
  <button onclick="showTab('country')" data-i18n="nav_country">🔍 Country</button>
  <button onclick="showTab('regions')" data-i18n="nav_regions">🌍 Regions</button>
  <button onclick="showTab('statistics')" data-i18n="nav_statistics">📐 Advanced Statistics</button>
</div>
</div>

<!-- EXPORT MODAL -->
<div class="modal-overlay" id="export-modal">
  <div class="modal">
    <h3 data-i18n="modal_title">⬇ Export Charts</h3>
    <p style="color:var(--text2);font-size:13px;margin-bottom:20px;" data-i18n="modal_desc">Click the desired format. All visible charts will be exported.</p>
    <div class="modal-btns">
      <button onclick="exportAll('png')" data-i18n="export_png">📸 PNG (high resolution)</button>
      <button onclick="exportAll('svg')" data-i18n="export_svg">🎨 SVG (vector)</button>
      <button onclick="exportAll('jpeg')">🖼️ JPEG</button>
      <button onclick="exportAll('webp')">🌐 WebP</button>
      <button onclick="exportCSV()" data-i18n="export_csv">📊 CSV (data)</button>
      <button onclick="exportJSON()" data-i18n="export_json">🔧 JSON (data)</button>
    </div>
    <button class="modal-close" onclick="closeExportModal()" data-i18n="modal_close">Close</button>
  </div>
</div>

<!-- MAIN -->
<div class="main">

<!-- ═══════════ OVERVIEW ═══════════ -->
<div class="section active" id="tab-overview">
  <div class="section-header">
    <h2 data-i18n="sec_overview">📊 Executive Summary — Africa Finance 2024</h2>
    <span class="tag" data-i18n="tag_overview">ANALYTICS DASHBOARD</span>
  </div>
  <div class="kpi-grid" id="kpi-grid"></div>
  <div class="chart-row">
    <div class="chart-box">
      <h3><span class="icon">📈</span> <span data-i18n="chart_pib_total">Total African GDP ($Bn) — 25-Year Evolution</span></h3>
      <div class="chart-actions"><button onclick="dlChart('chart-pib-total','PIB_Total')">⬇ PNG</button><button onclick="dlChart('chart-pib-total','PIB_Total','svg')">SVG</button></div>
      <div id="chart-pib-total" class="chart-div"></div>
    </div>
    <div class="chart-box">
      <h3><span class="icon">📊</span> <span data-i18n="chart_growth_infl">Average GDP Growth vs Inflation</span></h3>
      <div class="chart-actions"><button onclick="dlChart('chart-growth','Croissance')">⬇ PNG</button><button onclick="dlChart('chart-growth','Croissance','svg')">SVG</button></div>
      <div id="chart-growth" class="chart-div"></div>
    </div>
  </div>
  <div class="chart-row">
    <div class="chart-box">
      <h3><span class="icon">🏦</span> <span data-i18n="chart_banc_npl">Banking Rate & NPL — Continental Trajectory</span></h3>
      <div class="chart-actions"><button onclick="dlChart('chart-banc-npl','Bancarisation_NPL')">⬇ PNG</button><button onclick="dlChart('chart-banc-npl','Bancarisation_NPL','svg')">SVG</button></div>
      <div id="chart-banc-npl" class="chart-div"></div>
    </div>
    <div class="chart-box">
      <h3><span class="icon">📱</span> <span data-i18n="chart_mm_explosion">Mobile Money — Continental Explosion</span></h3>
      <div class="chart-actions"><button onclick="dlChart('chart-mm-overview','MobileMoney')">⬇ PNG</button><button onclick="dlChart('chart-mm-overview','MobileMoney','svg')">SVG</button></div>
      <div id="chart-mm-overview" class="chart-div"></div>
    </div>
  </div>
  <div class="chart-row r31">
    <div class="chart-box">
      <h3><span class="icon">🔬</span> <span data-i18n="chart_scatter_gdp">GDP/capita vs Banking Rate (54 countries, 2024) — Analytical Scatter</span></h3>
      <div class="chart-actions"><button onclick="dlChart('chart-scatter-overview','Scatter_PIB_Banc')">⬇ PNG</button><button onclick="dlChart('chart-scatter-overview','Scatter_PIB_Banc','svg')">SVG</button></div>
      <div id="chart-scatter-overview" class="chart-div tall"></div>
    </div>
    <div class="chart-box">
      <h3><span class="icon">🌳</span> <span data-i18n="chart_treemap">Treemap — GDP by Country & Region</span></h3>
      <div class="chart-actions"><button onclick="dlChart('chart-treemap','Treemap_PIB')">⬇ PNG</button></div>
      <div id="chart-treemap" class="chart-div tall"></div>
    </div>
  </div>
</div>

<!-- ═══════════ CHOROPLETH MAPS ═══════════ -->
<div class="section" id="tab-choropleth">
  <div class="section-header">
    <h2 data-i18n="sec_choropleth">🗺️ Choropleth Maps — Financial Africa</h2>
    <span class="tag" data-i18n="tag_choropleth">GEOVISUALIZATION</span>
  </div>
  <div class="controls">
    <label data-i18n="lbl_indicator">Indicator</label>
    <select id="choro-indicator" onchange="renderChoropleth()">
      <option value="pib_hab" data-i18n="opt_gdp_cap">GDP per capita ($)</option>
      <option value="croissance" data-i18n="opt_growth">GDP Growth (%)</option>
      <option value="inflation" data-i18n="opt_inflation">Inflation (%)</option>
      <option value="dette" data-i18n="opt_debt">Public Debt (% GDP)</option>
      <option value="bancarisation" selected data-i18n="opt_banking">Banking Rate (%)</option>
      <option value="npl" data-i18n="opt_npl">NPL — Non-Performing Loans (%)</option>
      <option value="car" data-i18n="opt_car">CAR — Capital Adequacy (%)</option>
      <option value="credit_pib" data-i18n="opt_credit_gdp">Credit/GDP (%)</option>
      <option value="pop_mm" data-i18n="opt_mm_pop">Mobile Money (% pop.)</option>
      <option value="score_inclusion" data-i18n="opt_inclusion">Inclusion Score (0-10)</option>
      <option value="fdi" data-i18n="opt_fdi">FDI Inflows ($Bn)</option>
      <option value="chomage" data-i18n="opt_unemp">Unemployment (%)</option>
      <option value="par30" data-i18n="opt_par30">PAR30 Microfinance (%)</option>
    </select>
    <label style="margin-left:20px;" data-i18n="lbl_year">Year</label>
    <input type="range" id="choro-year" min="2000" max="2024" value="2024" oninput="updateChoroYear()">
    <span class="year-display" id="choro-year-display">2024</span>
    <button class="btn-export" style="margin-left:auto;" onclick="dlChart('chart-choropleth','Carte_Afrique')">⬇ PNG HD</button>
    <button class="btn-export" style="background:var(--accent2);" onclick="dlChart('chart-choropleth','Carte_Afrique','svg')">SVG</button>
  </div>
  <div class="chart-row single">
    <div class="chart-box" style="min-height:620px;">
      <div id="chart-choropleth" class="chart-div xtall" style="height:580px;"></div>
    </div>
  </div>
  <div class="chart-row">
    <div class="chart-box">
      <h3><span class="icon">🗺️</span> <span data-i18n="chart_map2">Map 2 — Secondary Comparison</span></h3>
      <div class="chart-actions">
        <select id="choro-indicator2" onchange="renderChoropleth2()" style="font-size:11px;padding:4px 8px;">
          <option value="npl">NPL (%)</option>
          <option value="pop_mm">Mobile Money (%)</option>
          <option value="inflation">Inflation (%)</option>
          <option value="croissance">Croissance (%)</option>
          <option value="dette">Dette (%PIB)</option>
        </select>
        <button onclick="dlChart('chart-choropleth2','Carte2')">⬇</button>
      </div>
      <div id="chart-choropleth2" class="chart-div tall"></div>
    </div>
    <div class="chart-box">
      <h3><span class="icon">📊</span> <span data-i18n="chart_distrib_indicator">Indicator Distribution</span></h3>
      <div class="chart-actions"><button onclick="dlChart('chart-choro-hist','Distribution')">⬇</button></div>
      <div id="chart-choro-hist" class="chart-div tall"></div>
    </div>
  </div>
</div>

<!-- ═══════════ MACRO ═══════════ -->
<div class="section" id="tab-macro">
  <div class="section-header">
    <h2 data-i18n="sec_macro">💰 Macroeconomic Analysis (2000-2024)</h2>
    <span class="tag">1 275 OBSERVATIONS</span>
  </div>
  <div class="chart-row">
    <div class="chart-box"><h3><span class="icon">📈</span> <span data-i18n="chart_gdp_growth">Total GDP & Growth</span></h3><div class="chart-actions"><button onclick="dlChart('chart-macro-pib','Macro_PIB')">⬇</button><button onclick="dlChart('chart-macro-pib','Macro_PIB','svg')">SVG</button></div><div id="chart-macro-pib" class="chart-div"></div></div>
    <div class="chart-box"><h3><span class="icon">💹</span> <span data-i18n="chart_infl_rate">Inflation & Policy Rate</span></h3><div class="chart-actions"><button onclick="dlChart('chart-macro-inflation','Macro_Inflation')">⬇</button></div><div id="chart-macro-inflation" class="chart-div"></div></div>
  </div>
  <div class="chart-row">
    <div class="chart-box"><h3><span class="icon">💵</span> <span data-i18n="chart_fdi_remit">FDI vs Remittances ($Bn)</span></h3><div class="chart-actions"><button onclick="dlChart('chart-macro-fdi','FDI')">⬇</button></div><div id="chart-macro-fdi" class="chart-div"></div></div>
    <div class="chart-box"><h3><span class="icon">📊</span> <span data-i18n="chart_debt_unemp">Public Debt & Unemployment (%)</span></h3><div class="chart-actions"><button onclick="dlChart('chart-macro-dette','Dette')">⬇</button></div><div id="chart-macro-dette" class="chart-div"></div></div>
  </div>
  <div class="chart-row single">
    <div class="chart-box"><h3><span class="icon">🌍</span> <span data-i18n="chart_growth_region">GDP Growth by Region</span></h3><div class="chart-actions"><button onclick="dlChart('chart-macro-region-growth','Growth_Region')">⬇</button></div><div id="chart-macro-region-growth" class="chart-div tall"></div></div>
  </div>
</div>

<!-- ═══════════ BANKING ═══════════ -->
<div class="section" id="tab-banking">
  <div class="section-header"><h2 data-i18n="sec_banking">🏦 African Banking Sector</h2><span class="tag">26 INDICATORS</span></div>
  <div class="chart-row">
    <div class="chart-box"><h3><span class="icon">📊</span> <span data-i18n="chart_banking_rate">Continental Banking Rate (%)</span></h3><div class="chart-actions"><button onclick="dlChart('chart-bank-banc','Bancarisation')">⬇</button><button onclick="dlChart('chart-bank-banc','Bancarisation','svg')">SVG</button></div><div id="chart-bank-banc" class="chart-div"></div></div>
    <div class="chart-box"><h3><span class="icon">⚠️</span> <span data-i18n="chart_npl_car">NPL vs CAR (%) — Basel III Thresholds</span></h3><div class="chart-actions"><button onclick="dlChart('chart-bank-npl-car','NPL_CAR')">⬇</button></div><div id="chart-bank-npl-car" class="chart-div"></div></div>
  </div>
  <div class="chart-row">
    <div class="chart-box"><h3><span class="icon">💰</span> <span data-i18n="chart_roe_nim">ROE & NIM (%)</span></h3><div class="chart-actions"><button onclick="dlChart('chart-bank-roe-nim','ROE_NIM')">⬇</button></div><div id="chart-bank-roe-nim" class="chart-div"></div></div>
    <div class="chart-box"><h3><span class="icon">🏘️</span> <span data-i18n="chart_credit_priv">Private Sector Credit (% GDP)</span></h3><div class="chart-actions"><button onclick="dlChart('chart-bank-credit','Credit')">⬇</button></div><div id="chart-bank-credit" class="chart-div"></div></div>
  </div>
  <div class="chart-row">
    <div class="chart-box"><h3><span class="icon">🗺️</span> <span data-i18n="chart_banking_region">Banking Rate by Region</span></h3><div class="chart-actions"><button onclick="dlChart('chart-bank-region-banc','Banc_Region')">⬇</button></div><div id="chart-bank-region-banc" class="chart-div"></div></div>
    <div class="chart-box"><h3><span class="icon">🎯</span> <span data-i18n="chart_radar_bank">Radar — Regional Banking Profile</span></h3><div class="chart-actions"><button onclick="dlChart('chart-radar-bank','Radar_Bancaire')">⬇</button></div><div id="chart-radar-bank" class="chart-div"></div></div>
  </div>
</div>

<!-- ═══════════ FINTECH ═══════════ -->
<div class="section" id="tab-fintech">
  <div class="section-header"><h2 data-i18n="sec_fintech">📱 Fintech & Mobile Money</h2><span class="tag" data-i18n="tag_fintech">FINANCIAL INNOVATION</span></div>
  <div class="chart-row">
    <div class="chart-box"><h3><span class="icon">📱</span> <span data-i18n="chart_mm_accounts">M-Money Accounts & Transactions</span></h3><div class="chart-actions"><button onclick="dlChart('chart-ft-mm','MM_Comptes')">⬇</button><button onclick="dlChart('chart-ft-mm','MM_Comptes','svg')">SVG</button></div><div id="chart-ft-mm" class="chart-div"></div></div>
    <div class="chart-box"><h3><span class="icon">🚀</span> <span data-i18n="chart_fintech_startups">Fintech Startups & Investments</span></h3><div class="chart-actions"><button onclick="dlChart('chart-ft-startups','Fintech_Startups')">⬇</button></div><div id="chart-ft-startups" class="chart-div"></div></div>
  </div>
  <div class="chart-row">
    <div class="chart-box"><h3><span class="icon">📊</span> <span data-i18n="chart_mm_region">M-Money Penetration by Region</span></h3><div class="chart-actions"><button onclick="dlChart('chart-ft-region','MM_Region')">⬇</button></div><div id="chart-ft-region" class="chart-div"></div></div>
    <div class="chart-box"><h3><span class="icon">📈</span> <span data-i18n="chart_smartphone">Smartphone vs Digital Payments (%)</span></h3><div class="chart-actions"><button onclick="dlChart('chart-ft-smartphone','Smartphone')">⬇</button></div><div id="chart-ft-smartphone" class="chart-div"></div></div>
  </div>
</div>

<!-- ═══════════ MARKETS ═══════════ -->
<div class="section" id="tab-markets">
  <div class="section-header"><h2 data-i18n="sec_markets">📈 African Financial Markets</h2><span class="tag" data-i18n="tag_markets">29 EXCHANGES · EUROBONDS</span></div>
  <div class="chart-row">
    <div class="chart-box"><h3><span class="icon">📈</span> <span data-i18n="chart_mkt_cap">Total Market Capitalization ($Bn)</span></h3><div class="chart-actions"><button onclick="dlChart('chart-mk-cap','Cap_Boursiere')">⬇</button></div><div id="chart-mk-cap" class="chart-div"></div></div>
    <div class="chart-box"><h3><span class="icon">⚡</span> <span data-i18n="chart_spread">Average Sovereign Spread (bps)</span></h3><div class="chart-actions"><button onclick="dlChart('chart-mk-spread','Spread')">⬇</button></div><div id="chart-mk-spread" class="chart-div"></div></div>
  </div>
  <div class="chart-row single">
    <div class="chart-box"><h3><span class="icon">🏛️</span> <span data-i18n="chart_exchanges">African Exchanges — Capitalization 2024</span></h3><div class="chart-actions"><button onclick="dlChart('chart-mk-bourses','Bourses')">⬇</button></div><div id="chart-mk-bourses" class="chart-div tall"></div></div>
  </div>
</div>

<!-- ═══════════ MICROFINANCE ═══════════ -->
<div class="section" id="tab-microfinance">
  <div class="section-header"><h2 data-i18n="sec_mfi">🏘️ Microfinance & Financial Inclusion</h2><span class="tag">1,200+ MFIs</span></div>
  <div class="chart-row">
    <div class="chart-box"><h3><span class="icon">📊</span> <span data-i18n="chart_par_oss">PAR30 & OSS (Quality Indicators)</span></h3><div class="chart-actions"><button onclick="dlChart('chart-mfi-par-oss','PAR_OSS')">⬇</button></div><div id="chart-mfi-par-oss" class="chart-div"></div></div>
    <div class="chart-box"><h3><span class="icon">👩</span> <span data-i18n="chart_clients_women">Clients & Women Percentage</span></h3><div class="chart-actions"><button onclick="dlChart('chart-mfi-clients','MFI_Clients')">⬇</button></div><div id="chart-mfi-clients" class="chart-div"></div></div>
  </div>
  <div class="chart-row">
    <div class="chart-box"><h3><span class="icon">💰</span> <span data-i18n="chart_portf">Total Microcredit Portfolio ($M)</span></h3><div class="chart-actions"><button onclick="dlChart('chart-mfi-portf','Portefeuille')">⬇</button></div><div id="chart-mfi-portf" class="chart-div"></div></div>
    <div class="chart-box"><h3><span class="icon">🎯</span> <span data-i18n="chart_inclusion_score">Financial Inclusion Score (0-10)</span></h3><div class="chart-actions"><button onclick="dlChart('chart-mfi-inclusion','Inclusion')">⬇</button></div><div id="chart-mfi-inclusion" class="chart-div"></div></div>
  </div>
</div>

<!-- ═══════════ CRISES ═══════════ -->
<div class="section" id="tab-crises">
  <div class="section-header"><h2 data-i18n="sec_crises">⚠️ Financial Crises & Shocks</h2><span class="tag" id="crises-count"></span></div>
  <div class="chart-row">
    <div class="chart-box"><h3><span class="icon">📊</span> <span data-i18n="chart_crises_year">Crises by Year</span></h3><div class="chart-actions"><button onclick="dlChart('chart-crises-year','Crises_Annee')">⬇</button></div><div id="chart-crises-year" class="chart-div"></div></div>
    <div class="chart-box"><h3><span class="icon">🔥</span> <span data-i18n="chart_crises_impact">GDP Impact vs Severity</span></h3><div class="chart-actions"><button onclick="dlChart('chart-crises-impact','Impact_Crises')">⬇</button></div><div id="chart-crises-impact" class="chart-div"></div></div>
  </div>
  <div class="table-container" id="crises-table-container"></div>
</div>

<!-- ═══════════ RANKINGS ═══════════ -->
<div class="section" id="tab-rankings">
  <div class="section-header"><h2 data-i18n="sec_rankings">🏆 Rankings & Classifications 2024</h2><span class="tag">TOP 15</span></div>
  <div class="controls">
    <label data-i18n="lbl_indicator">Indicator</label>
    <select id="ranking-select" onchange="renderRanking()">
      <option value="bancarisation" data-i18n="opt_banking">Banking Rate (%)</option>
      <option value="croissance" data-i18n="opt_growth">GDP Growth (%)</option>
      <option value="pib" data-i18n="opt_gdp">GDP ($Bn)</option>
      <option value="npl" data-i18n="opt_npl_short">NPL (%)</option>
      <option value="inflation" data-i18n="opt_inflation_short">Inflation (%)</option>
      <option value="fdi" data-i18n="opt_fdi_short">FDI Inflows ($Bn)</option>
      <option value="mobile_money" data-i18n="opt_mm">Mobile Money (% pop)</option>
      <option value="dette" data-i18n="opt_debt_short">Public Debt (% GDP)</option>
      <option value="credit_pib" data-i18n="opt_credit">Credit/GDP (%)</option>
      <option value="score_inclusion" data-i18n="opt_inclusion">Inclusion Score (0-10)</option>
    </select>
    <button class="btn-export" style="margin-left:auto;" onclick="dlChart('chart-ranking-top','Ranking_Top')">⬇ Top PNG</button>
  </div>
  <div class="chart-row">
    <div class="chart-box"><h3><span class="icon">🥇</span> Top 15</h3><div id="chart-ranking-top" class="chart-div tall"></div></div>
    <div class="chart-box"><h3><span class="icon">📉</span> Bottom 15</h3><div id="chart-ranking-bottom" class="chart-div tall"></div></div>
  </div>
</div>

<!-- ═══════════ CORRELATIONS ═══════════ -->
<div class="section" id="tab-correlations">
  <div class="section-header"><h2 data-i18n="sec_correlations">🔗 Correlation Matrix</h2><span class="tag">11 VARIABLES · PEARSON</span></div>
  <div class="chart-row single">
    <div class="chart-box" style="min-height:550px;">
      <h3><span class="icon">🔬</span> <span data-i18n="chart_heatmap">Heatmap — Pearson Correlations (54 countries aggregated)</span></h3>
      <div class="chart-actions"><button onclick="dlChart('chart-corr-heatmap','Correlations')">⬇ PNG</button><button onclick="dlChart('chart-corr-heatmap','Correlations','svg')">SVG</button></div>
      <div id="chart-corr-heatmap" class="chart-div xtall"></div>
    </div>
  </div>
</div>

<!-- ═══════════ COUNTRY ═══════════ -->
<div class="section" id="tab-country">
  <div class="section-header"><h2 data-i18n="sec_country">🔍 Detailed Country Analysis</h2><span class="tag">54 COUNTRIES</span></div>
  <div class="controls">
    <label data-i18n="lbl_country">Country</label>
    <select id="country-select" onchange="renderCountry()"></select>
    <button class="btn-export" style="margin-left:auto;" onclick="exportCountryAll()" data-i18n="btn_export_country">⬇ Export Country Sheet (PNG)</button>
  </div>
  <div class="chart-row">
    <div class="chart-box"><h3><span class="icon">💰</span> <span id="country-title-macro">PIB & Croissance</span></h3><div class="chart-actions"><button onclick="dlChart('chart-country-macro','Pays_Macro')">⬇</button></div><div id="chart-country-macro" class="chart-div"></div></div>
    <div class="chart-box"><h3><span class="icon">🏦</span> <span id="country-title-bank">Bancarisation & NPL</span></h3><div class="chart-actions"><button onclick="dlChart('chart-country-bank','Pays_Bank')">⬇</button></div><div id="chart-country-bank" class="chart-div"></div></div>
  </div>
  <div class="chart-row">
    <div class="chart-box"><h3><span class="icon">📱</span> <span id="country-title-fintech">Mobile Money</span></h3><div class="chart-actions"><button onclick="dlChart('chart-country-fintech','Pays_Fintech')">⬇</button></div><div id="chart-country-fintech" class="chart-div"></div></div>
    <div class="chart-box"><h3><span class="icon">📊</span> <span id="country-title-extra">Inflation & Dette</span></h3><div class="chart-actions"><button onclick="dlChart('chart-country-extra','Pays_Extra')">⬇</button></div><div id="chart-country-extra" class="chart-div"></div></div>
  </div>
</div>

<!-- ═══════════ REGIONS ═══════════ -->
<div class="section" id="tab-regions">
  <div class="section-header"><h2 data-i18n="sec_regions">🌍 Regional Comparative Analysis</h2><span class="tag" data-i18n="tag_regions">5 REGIONS</span></div>
  <div class="chart-row">
    <div class="chart-box"><h3><span class="icon">💰</span> <span data-i18n="chart_reg_gdp">GDP by Region (2024)</span></h3><div class="chart-actions"><button onclick="dlChart('chart-reg-pib','Region_PIB')">⬇</button></div><div id="chart-reg-pib" class="chart-div"></div></div>
    <div class="chart-box"><h3><span class="icon">🏦</span> <span data-i18n="chart_reg_bank">Banking Indicators by Region</span></h3><div class="chart-actions"><button onclick="dlChart('chart-reg-bank','Region_Bank')">⬇</button></div><div id="chart-reg-bank" class="chart-div"></div></div>
  </div>
  <div class="chart-row">
    <div class="chart-box"><h3><span class="icon">📱</span> <span data-i18n="chart_reg_mm">Mobile Money by Region</span></h3><div class="chart-actions"><button onclick="dlChart('chart-reg-fintech','Region_Fintech')">⬇</button></div><div id="chart-reg-fintech" class="chart-div"></div></div>
    <div class="chart-box"><h3><span class="icon">📊</span> <span data-i18n="chart_reg_npl">NPL by Region (2000-2024)</span></h3><div class="chart-actions"><button onclick="dlChart('chart-reg-npl-ts','Region_NPL')">⬇</button></div><div id="chart-reg-npl-ts" class="chart-div"></div></div>
  </div>
</div>

<!-- ═══════════ STATISTIQUES AVANCÉES ═══════════ -->
<div class="section" id="tab-statistics">
  <div class="section-header">
    <h2 data-i18n="sec_statistics">📐 Advanced Statistics & Econometric Tests</h2>
    <span class="tag" data-i18n="tag_statistics">REGRESSION · ANOVA · AUTOCORRELATION · DISTRIBUTIONS</span>
  </div>

  <!-- Descriptive Stats Table -->
  <div class="chart-box" style="margin-bottom:22px;">
    <h3><span class="icon">📋</span> <span data-i18n="chart_desc_stats">Descriptive Statistics (cross-section 2024)</span></h3>
    <div class="chart-actions"><button onclick="exportStatsCSV()">⬇ CSV</button></div>
    <div class="table-container" id="desc-stats-table" style="max-height:440px;"></div>
  </div>

  <!-- Normality + Kruskal -->
  <div class="chart-row">
    <div class="chart-box">
      <h3><span class="icon">🔔</span> <span data-i18n="chart_normality">Normality Tests (Shapiro-Wilk)</span></h3>
      <div class="table-container" id="normality-table" style="max-height:380px;"></div>
    </div>
    <div class="chart-box">
      <h3><span class="icon">📊</span> <span data-i18n="chart_distributions">Distributions & Box Plots</span></h3>
      <div class="controls" style="margin-bottom:10px;">
        <select id="dist-var-select" onchange="renderDistribution()"></select>
      </div>
      <div class="chart-actions"><button onclick="dlChart('chart-distribution','Distribution')">⬇</button></div>
      <div id="chart-distribution" class="chart-div"></div>
    </div>
  </div>

  <!-- Linear Regressions -->
  <div class="chart-box" style="margin-bottom:22px;">
    <h3><span class="icon">📈</span> <span data-i18n="chart_regressions">Linear Regressions (OLS) — Scatter + Regression Line</span></h3>
    <div class="controls" style="margin-bottom:10px;">
      <label data-i18n="lbl_model">Model</label>
      <select id="reg-select" onchange="renderRegression()"></select>
      <span id="reg-equation" style="font-family:'JetBrains Mono',monospace;font-size:12px;color:var(--accent);margin-left:18px;"></span>
    </div>
    <div class="chart-actions"><button onclick="dlChart('chart-regression','Regression')">⬇ PNG</button><button onclick="dlChart('chart-regression','Regression','svg')">SVG</button></div>
    <div id="chart-regression" class="chart-div tall"></div>
  </div>

  <!-- Regression summary table -->
  <div class="chart-box" style="margin-bottom:22px;">
    <h3><span class="icon">📊</span> <span data-i18n="chart_reg_summary">Summary — All Regressions</span></h3>
    <div class="table-container" id="reg-summary-table" style="max-height:400px;"></div>
  </div>

  <!-- Panel Regression -->
  <div class="chart-box" style="margin-bottom:22px;">
    <h3><span class="icon">🧮</span> <span data-i18n="chart_panel_reg">Panel Regression (Pooled OLS) — GDP Growth ~ Macro Factors</span></h3>
    <div class="chart-row" style="gap:18px;">
      <div id="panel-reg-info" style="flex:1;"></div>
      <div style="flex:2;"><div id="panel-reg-table-container" class="table-container" style="max-height:350px;"></div></div>
    </div>
  </div>

  <!-- ANOVA -->
  <div class="chart-row">
    <div class="chart-box">
      <h3><span class="icon">🧪</span> <span data-i18n="chart_anova">ANOVA — Regional Differences</span></h3>
      <div class="controls" style="margin-bottom:10px;">
        <select id="anova-select" onchange="renderAnova()"></select>
      </div>
      <div class="chart-actions"><button onclick="dlChart('chart-anova','ANOVA')">⬇</button></div>
      <div id="chart-anova" class="chart-div"></div>
    </div>
    <div class="chart-box">
      <h3><span class="icon">📊</span> <span data-i18n="chart_anova_results">ANOVA & Kruskal-Wallis Results</span></h3>
      <div class="table-container" id="anova-table" style="max-height:380px;"></div>
    </div>
  </div>

  <!-- Spearman Matrix -->
  <div class="chart-row single">
    <div class="chart-box" style="min-height:520px;">
      <h3><span class="icon">🔗</span> <span data-i18n="chart_spearman">Spearman Correlation Matrix (ρ) — Non-parametric</span></h3>
      <div class="chart-actions"><button onclick="dlChart('chart-spearman','Spearman')">⬇ PNG</button><button onclick="dlChart('chart-spearman','Spearman','svg')">SVG</button></div>
      <div id="chart-spearman" class="chart-div xtall"></div>
    </div>
  </div>

  <!-- Trends -->
  <div class="chart-row">
    <div class="chart-box">
      <h3><span class="icon">📉</span> <span data-i18n="chart_trends">Trend Analysis (Spearman over Time)</span></h3>
      <div class="controls" style="margin-bottom:10px;">
        <select id="trend-select" onchange="renderTrend()"></select>
      </div>
      <div class="chart-actions"><button onclick="dlChart('chart-trend','Tendance')">⬇</button></div>
      <div id="chart-trend" class="chart-div"></div>
    </div>
    <div class="chart-box">
      <h3><span class="icon">🎯</span> <span data-i18n="chart_trends_summary">Trend Summary 2000-2024</span></h3>
      <div class="table-container" id="trend-table" style="max-height:380px;"></div>
    </div>
  </div>

  <!-- Outliers -->
  <div class="chart-row single">
    <div class="chart-box">
      <h3><span class="icon">⚡</span> <span data-i18n="chart_outliers">Outlier Detection (IQR method)</span></h3>
      <div class="table-container" id="outliers-table" style="max-height:400px;"></div>
    </div>
  </div>
</div>

</div><!-- .main -->

<div class="footer">
  <strong>🌍 AFRICA FINANCE OBSERVATORY</strong> — <span data-i18n="footer_role">Data Analyst & WebGIS Expert Report</span><br>
  <span style="color:var(--accent);">Abdou Samad Faye</span> · Fullstack Geo Data Scientist<br>
  <span data-i18n="footer_desc">54 countries · 2000-2024 · 12 dimensions · IMF, WB, AfDB, GSMA, UNCTAD, BIS, MIX Market</span>
</div>

<script>
// ═══════════════════════════════════════════════════════════════════════════════
// DATA
// ═══════════════════════════════════════════════════════════════════════════════
const D = __DATA_PLACEHOLDER__;

// ═══════════════════════════════════════════════════════════════════════════════
// THEME & CONFIG
// ═══════════════════════════════════════════════════════════════════════════════
const COLORS = ['#00e5a0','#a78bfa','#f59e0b','#f85149','#58a6ff','#f472b6','#2dd4bf','#fb923c','#c084fc','#22d3ee'];
const REGION_COLORS = {'Afrique Australe':'#00e5a0','Afrique Centrale':'#a78bfa','Afrique du Nord':'#58a6ff','Afrique Occidentale':'#f59e0b','Afrique Orientale':'#f472b6'};
const FONT = 'Inter, system-ui, sans-serif';

const LAYOUT_BASE = {
  paper_bgcolor:'rgba(0,0,0,0)', plot_bgcolor:'rgba(0,0,0,0)',
  font:{family:FONT,color:'#e6edf3',size:12},
  margin:{t:35,r:35,b:55,l:65},
  xaxis:{gridcolor:'#21262d',zerolinecolor:'#30363d',tickfont:{size:11,color:'#8b949e'},linecolor:'#21262d'},
  yaxis:{gridcolor:'#21262d',zerolinecolor:'#30363d',tickfont:{size:11,color:'#8b949e'},linecolor:'#21262d'},
  legend:{orientation:'h',y:-0.15,x:0.5,xanchor:'center',font:{size:11,color:'#8b949e'},bgcolor:'rgba(0,0,0,0)'},
  hoverlabel:{bgcolor:'#161b22',bordercolor:'#00e5a0',font:{color:'#e6edf3',size:13,family:FONT}},
};

// Plotly config with download buttons
const CFG = {
  responsive:true,
  displayModeBar:true,
  modeBarButtonsToAdd:['toImage'],
  modeBarButtonsToRemove:['select2d','lasso2d','autoScale2d'],
  toImageButtonOptions:{format:'png',filename:'AfricaFinance_Chart',height:800,width:1400,scale:3},
  displaylogo:false,
  modeBarStyle:{backgroundColor:'rgba(0,0,0,0)'}
};

function L(o){return Object.assign({},JSON.parse(JSON.stringify(LAYOUT_BASE)),o||{});}

// ═══════════════════════════════════════════════════════════════════════════════
// EXPORT FUNCTIONS
// ═══════════════════════════════════════════════════════════════════════════════
function dlChart(id,name,format){
  format=format||'png';
  Plotly.downloadImage(id,{format:format,width:1600,height:900,scale:3,filename:'AfricaFinance_'+name+'_'+new Date().toISOString().slice(0,10)});
}

function openExportModal(){document.getElementById('export-modal').classList.add('active');}
function closeExportModal(){document.getElementById('export-modal').classList.remove('active');}

function exportAll(format){
  const charts=document.querySelectorAll('.section.active .chart-div');
  let i=0;
  charts.forEach(c=>{
    if(c.data&&c.data.length){
      setTimeout(()=>{
        Plotly.downloadImage(c.id,{format:format,width:1600,height:900,scale:3,
          filename:'AfricaFinance_'+c.id+'_'+new Date().toISOString().slice(0,10)});
      },i*800);
      i++;
    }
  });
  closeExportModal();
}

function exportCSV(){
  let csv='Pays,Annee,PIB_Mrd,Croissance_PIB,Inflation,Dette,Bancarisation,NPL,CAR,MobileMoney_pct\n';
  D.country_list.forEach(p=>{
    const cm=D.country_macro[p],cb=D.country_bank[p],cf=D.country_fintech[p];
    if(!cm)return;
    cm.annees.forEach((y,i)=>{
      csv+='"'+p+'",'+y+','+(cm.pib[i]||'')+','+(cm.croissance[i]||'')+','+(cm.inflation[i]||'')+','+
        (cm.dette[i]||'')+','+(cb?cb.bancarisation[i]||'':'')+','+(cb?cb.npl[i]||'':'')+','+
        (cb?cb.car[i]||'':'')+','+(cf?cf.pop_mm[i]||'':'')+'\n';
    });
  });
  const blob=new Blob([csv],{type:'text/csv;charset=utf-8;'});
  const a=document.createElement('a');a.href=URL.createObjectURL(blob);
  a.download='AfricaFinance_Data_Export.csv';a.click();
  closeExportModal();
}

function exportJSON(){
  const blob=new Blob([JSON.stringify(D,null,2)],{type:'application/json'});
  const a=document.createElement('a');a.href=URL.createObjectURL(blob);
  a.download='AfricaFinance_Data_Export.json';a.click();
  closeExportModal();
}

function exportCountryAll(){
  ['chart-country-macro','chart-country-bank','chart-country-fintech','chart-country-extra'].forEach((id,i)=>{
    setTimeout(()=>{
      const p=document.getElementById('country-select').value;
      Plotly.downloadImage(id,{format:'png',width:1600,height:900,scale:3,filename:p+'_'+id.replace('chart-country-','')});
    },i*600);
  });
}

// ═══════════════════════════════════════════════════════════════════════════════
// TAB NAVIGATION
// ═══════════════════════════════════════════════════════════════════════════════
function showTab(name){
  document.querySelectorAll('.section').forEach(s=>s.classList.remove('active'));
  document.querySelectorAll('.nav button').forEach(b=>b.classList.remove('active'));
  document.getElementById('tab-'+name).classList.add('active');
  document.querySelectorAll('.nav button').forEach(b=>{
    if(b.getAttribute('onclick')&&b.getAttribute('onclick').includes("'"+name+"'"))b.classList.add('active');
  });
  setTimeout(()=>window.dispatchEvent(new Event('resize')),120);
  if(!rendered[name]&&renderers[name]){renderers[name]();rendered[name]=true;}
}
const rendered={overview:false};
const renderers={};

// ═══════════════════════════════════════════════════════════════════════════════
// KPIs
// ═══════════════════════════════════════════════════════════════════════════════
function ti(key){return (I18N[key]&&I18N[key][currentLang])||key;}
function renderKPIs(){
  const k=D.kpis;
  const cards=[
    {label:ti('kpi_pib_total'),value:'$'+k.pib_total+' '+(currentLang==='en'?'Bn':'Mrd'),cls:'teal',icon:'💰',icls:'teal',sub:'54 '+(currentLang==='en'?'countries':'pays')+' · 2024'},
    {label:ti('kpi_growth'),value:k.pib_growth_avg+'%',cls:'teal',icon:'📈',icls:'teal',sub:ti('kpi_sub_growth')},
    {label:ti('kpi_inflation'),value:k.inflation_avg+'%',cls:'gold',icon:'🔥',icls:'gold',sub:ti('kpi_sub_inflation')},
    {label:ti('kpi_banking'),value:k.bancarisation_avg+'%',cls:'blue',icon:'🏦',icls:'blue',sub:ti('kpi_sub_banking')},
    {label:ti('kpi_npl'),value:k.npl_avg+'%',cls:'red',icon:'⚠️',icls:'red',sub:ti('kpi_sub_npl')},
    {label:ti('kpi_car'),value:k.car_avg+'%',cls:'teal',icon:'🛡️',icls:'teal',sub:ti('kpi_sub_car')},
    {label:ti('kpi_roe'),value:k.roe_avg+'%',cls:'purple',icon:'💎',icls:'purple',sub:ti('kpi_sub_roe')},
    {label:ti('kpi_nim'),value:k.nim_avg+'%',cls:'gold',icon:'📊',icls:'gold',sub:ti('kpi_sub_nim')},
    {label:ti('kpi_mm_accounts'),value:k.mobile_money_accounts+'M',cls:'teal',icon:'📱',icls:'teal',sub:ti('kpi_sub_mm_accounts')},
    {label:ti('kpi_mm_transactions'),value:'$'+k.mm_transactions+' '+(currentLang==='en'?'Bn':'Mrd'),cls:'blue',icon:'💸',icls:'blue',sub:ti('kpi_sub_mm_transactions')},
    {label:ti('kpi_startups'),value:k.fintech_startups.toLocaleString(),cls:'purple',icon:'🚀',icls:'purple',sub:ti('kpi_sub_startups')},
    {label:ti('kpi_fdi'),value:'$'+k.fdi_total+' '+(currentLang==='en'?'Bn':'Mrd'),cls:'gold',icon:'🌐',icls:'gold',sub:ti('kpi_sub_fdi')},
    {label:ti('kpi_debt'),value:k.dette_avg+'% '+(currentLang==='en'?'GDP':'PIB'),cls:'red',icon:'📉',icls:'red',sub:ti('kpi_sub_debt')},
    {label:ti('kpi_credit'),value:k.credit_pib_avg+'%',cls:'blue',icon:'🏛️',icls:'blue',sub:ti('kpi_sub_credit')},
    {label:ti('kpi_inclusion'),value:k.score_inclusion_avg+'/10',cls:'teal',icon:'🎯',icls:'teal',sub:ti('kpi_sub_inclusion')},
    {label:ti('kpi_coverage'),value:k.nb_pays+' '+ti('kpi_sub_coverage_countries'),cls:'purple',icon:'🌍',icls:'purple',sub:k.nb_annees+' '+ti('kpi_sub_coverage_years')},
  ];
  document.getElementById('kpi-grid').innerHTML=cards.map(c=>`
    <div class="kpi-card">
      <div class="kpi-icon ${c.icls}">${c.icon}</div>
      <div class="kpi-label">${c.label}</div>
      <div class="kpi-value ${c.cls}">${c.value}</div>
      <div class="kpi-sub">${c.sub}</div>
    </div>`).join('');
}

// ═══════════════════════════════════════════════════════════════════════════════
// CHOROPLETH MAPS
// ═══════════════════════════════════════════════════════════════════════════════
const CHORO_SCALES={
  pib_hab:{title:{en:'GDP/cap ($)',fr:'PIB/hab ($)'},colorscale:[[0,'#0d1117'],[0.2,'#0a3d2e'],[0.5,'#0d6644'],[0.8,'#00b377'],[1,'#00e5a0']],range:[0,8000]},
  croissance:{title:{en:'GDP Growth (%)',fr:'Croissance PIB (%)'},colorscale:[[0,'#f85149'],[0.3,'#f59e0b'],[0.5,'#21262d'],[0.7,'#1a7d5a'],[1,'#00e5a0']],range:[-5,12]},
  inflation:{title:{en:'Inflation (%)',fr:'Inflation (%)'},colorscale:[[0,'#00e5a0'],[0.15,'#0d6644'],[0.4,'#f59e0b'],[0.7,'#f85149'],[1,'#7f1d1d']],range:[0,30]},
  dette:{title:{en:'Debt/GDP (%)',fr:'Dette/PIB (%)'},colorscale:[[0,'#00e5a0'],[0.3,'#f59e0b'],[0.6,'#f85149'],[1,'#7f1d1d']],range:[0,120]},
  bancarisation:{title:{en:'Banking Rate (%)',fr:'Bancarisation (%)'},colorscale:[[0,'#0d1117'],[0.25,'#1e1a3a'],[0.5,'#5b3cc4'],[0.75,'#8b5cf6'],[1,'#c084fc']],range:[0,100]},
  npl:{title:{en:'NPL (%)',fr:'NPL (%)'},colorscale:[[0,'#00e5a0'],[0.2,'#f59e0b'],[0.5,'#f85149'],[1,'#7f1d1d']],range:[0,25]},
  car:{title:{en:'CAR (%)',fr:'CAR (%)'},colorscale:[[0,'#f85149'],[0.3,'#f59e0b'],[0.5,'#00e5a0'],[1,'#00ffc8']],range:[5,25]},
  credit_pib:{title:{en:'Credit/GDP (%)',fr:'Crédit/PIB (%)'},colorscale:[[0,'#0d1117'],[0.3,'#1a3a5c'],[0.6,'#3b82f6'],[1,'#93c5fd']],range:[0,100]},
  pop_mm:{title:{en:'Mobile Money (% pop.)',fr:'Mobile Money (% pop.)'},colorscale:[[0,'#0d1117'],[0.3,'#2d1a4e'],[0.6,'#7c3aed'],[1,'#c084fc']],range:[0,90]},
  score_inclusion:{title:{en:'Inclusion Score (0-10)',fr:'Score Inclusion (0-10)'},colorscale:[[0,'#0d1117'],[0.3,'#0a3d2e'],[0.6,'#00b377'],[1,'#00e5a0']],range:[0,10]},
  fdi:{title:{en:'FDI ($Bn)',fr:'FDI ($Mrd)'},colorscale:[[0,'#0d1117'],[0.3,'#1a3a5c'],[0.6,'#3b82f6'],[1,'#93c5fd']],range:[0,15]},
  chomage:{title:{en:'Unemployment (%)',fr:'Chômage (%)'},colorscale:[[0,'#00e5a0'],[0.3,'#f59e0b'],[0.6,'#f85149'],[1,'#7f1d1d']],range:[0,35]},
  par30:{title:{en:'PAR30 (%)',fr:'PAR30 (%)'},colorscale:[[0,'#00e5a0'],[0.3,'#f59e0b'],[0.6,'#f85149'],[1,'#7f1d1d']],range:[0,20]},
};

function buildChoroTrace(indicator,year){
  const yr=String(year);
  const cd=D.choropleth[yr];
  if(!cd)return [];
  const cfg=CHORO_SCALES[indicator]||CHORO_SCALES.bancarisation;
  const isos=Object.keys(cd).filter(k=>cd[k][indicator]!=null);
  return [{
    type:'choropleth',
    locations:isos,
    z:isos.map(k=>cd[k][indicator]),
    text:isos.map(k=>cd[k].pays),
    customdata:isos.map(k=>{
      const d=cd[k];
      return currentLang==='en'
        ? `<b>${d.pays}</b><br>GDP/cap: $${(d.pib_hab||0).toFixed(0)}<br>Banking: ${(d.bancarisation||0).toFixed(1)}%<br>NPL: ${(d.npl||0).toFixed(1)}%<br>M-Money: ${(d.pop_mm||0).toFixed(1)}%`
        : `<b>${d.pays}</b><br>PIB/hab: $${(d.pib_hab||0).toFixed(0)}<br>Bancarisation: ${(d.bancarisation||0).toFixed(1)}%<br>NPL: ${(d.npl||0).toFixed(1)}%<br>M-Money: ${(d.pop_mm||0).toFixed(1)}%`;
    }),
    hovertemplate:'%{customdata}<br><b>${cfg.title}: %{z:.1f}</b><extra></extra>'.replace('${cfg.title}',cfg.title[currentLang]),
    colorscale:cfg.colorscale,
    zmin:cfg.range[0],zmax:cfg.range[1],
    colorbar:{title:{text:cfg.title[currentLang],font:{size:12,color:'#e6edf3'}},
      tickfont:{size:11,color:'#8b949e'},len:0.7,thickness:15,
      bgcolor:'rgba(0,0,0,0)',borderwidth:0,
      tickcolor:'#30363d'},
    marker:{line:{color:'#30363d',width:0.5}},
  }];
}

function choroLayout(title){
  return {
    paper_bgcolor:'rgba(0,0,0,0)',
    geo:{
      scope:'africa',
      bgcolor:'rgba(0,0,0,0)',
      showframe:false,showcoastlines:true,
      coastlinecolor:'#30363d',coastlinewidth:0.5,
      showland:true,landcolor:'#161b22',
      showocean:true,oceancolor:'#0d1117',
      showlakes:true,lakecolor:'#1c2128',
      showcountries:true,countrycolor:'#21262d',countrywidth:0.5,
      projection:{type:'natural earth'},
      lonaxis:{range:[-25,55]},lataxis:{range:[-38,40]},
    },
    font:{family:FONT,color:'#e6edf3',size:12},
    margin:{t:10,r:10,b:10,l:10},
    dragmode:'pan',
    hoverlabel:{bgcolor:'#161b22',bordercolor:'#00e5a0',font:{color:'#e6edf3',size:12,family:FONT}},
  };
}

function renderChoropleth(){
  const ind=document.getElementById('choro-indicator').value;
  const yr=document.getElementById('choro-year').value;
  const cfg=CHORO_SCALES[ind]||CHORO_SCALES.bancarisation;
  Plotly.react('chart-choropleth',buildChoroTrace(ind,yr),choroLayout(),CFG);
  // Histogram
  const cd=D.choropleth[String(yr)];
  if(cd){
    const vals=Object.values(cd).map(v=>v[ind]).filter(v=>v!=null);
    Plotly.react('chart-choro-hist',[{x:vals,type:'histogram',nbinsx:20,
      marker:{color:'rgba(0,229,160,0.5)',line:{color:'#00e5a0',width:1}},
      hovertemplate:'%{x:.1f}: %{y} '+(currentLang==='en'?'countries':'pays')+'<extra></extra>'
    }],L({xaxis:{title:cfg.title[currentLang]},yaxis:{title:currentLang==='en'?'Countries':'Nb pays'},bargap:0.05}),CFG);
  }
}
function renderChoropleth2(){
  const ind=document.getElementById('choro-indicator2').value;
  const yr=document.getElementById('choro-year').value;
  Plotly.react('chart-choropleth2',buildChoroTrace(ind,yr),choroLayout(),CFG);
}
function updateChoroYear(){
  const yr=document.getElementById('choro-year').value;
  document.getElementById('choro-year-display').textContent=yr;
  renderChoropleth();renderChoropleth2();
}
renderers.choropleth=function(){renderChoropleth();renderChoropleth2();};

// ═══════════════════════════════════════════════════════════════════════════════
// OVERVIEW
// ═══════════════════════════════════════════════════════════════════════════════
function renderOverview(){
  renderKPIs();
  const ts=D.ts_continental,tb=D.ts_banking,tf=D.ts_fintech;
  const years=ts.map(r=>r.Annee);

  // PIB Total — area chart
  Plotly.newPlot('chart-pib-total',[{
    x:years,y:ts.map(r=>r.PIB_total),type:'scatter',mode:'lines',
    fill:'tozeroy',fillcolor:'rgba(0,229,160,0.08)',fillgradient:{type:'vertical',colorscale:[['0','rgba(0,229,160,0.15)'],['1','rgba(0,229,160,0)']]},
    line:{color:'#00e5a0',width:3,shape:'spline'},
    hovertemplate:'<b>%{x}</b><br>PIB: $%{y:,.0f} Mrd<extra></extra>'
  }],L({yaxis:{title:'$Mrd',tickformat:','}}),CFG);

  // Growth + Inflation dual
  Plotly.newPlot('chart-growth',[
    {x:years,y:ts.map(r=>r.Croissance_moy),type:'bar',name:'Croissance (%)',
      marker:{color:ts.map(r=>r.Croissance_moy>=0?'rgba(0,229,160,0.7)':'rgba(248,81,73,0.7)'),
      line:{color:ts.map(r=>r.Croissance_moy>=0?'#00e5a0':'#f85149'),width:1}},
      hovertemplate:'%{x}: %{y:.1f}%<extra>Croissance</extra>'},
    {x:years,y:ts.map(r=>r.Inflation_moy),type:'scatter',mode:'lines+markers',name:'Inflation (%)',
      line:{color:'#f59e0b',width:2.5,dash:'dot'},marker:{size:4,color:'#f59e0b'},yaxis:'y2',
      hovertemplate:'%{x}: %{y:.1f}%<extra>Inflation</extra>'},
  ],L({yaxis:{title:'Croissance (%)',zeroline:true,zerolinecolor:'#f59e0b',zerolinewidth:1},
      yaxis2:{title:'Inflation (%)',overlaying:'y',side:'right',gridcolor:'transparent'}}),CFG);

  // Bancarisation & NPL
  Plotly.newPlot('chart-banc-npl',[
    {x:tb.map(r=>r.Annee),y:tb.map(r=>r.Bancarisation_moy),name:'Bancarisation',type:'scatter',mode:'lines',
      line:{color:'#00e5a0',width:3,shape:'spline'},fill:'tozeroy',fillcolor:'rgba(0,229,160,0.06)'},
    {x:tb.map(r=>r.Annee),y:tb.map(r=>r.NPL_moy),name:'NPL',type:'scatter',mode:'lines',
      line:{color:'#f85149',width:2.5,shape:'spline'},yaxis:'y2'},
  ],L({yaxis:{title:'Bancarisation (%)'},yaxis2:{title:'NPL (%)',overlaying:'y',side:'right',gridcolor:'transparent'}}),CFG);

  // Mobile Money
  Plotly.newPlot('chart-mm-overview',[
    {x:tf.map(r=>r.Annee),y:tf.map(r=>r.Comptes_MM_total),type:'scatter',mode:'lines',name:'Comptes (M)',
      fill:'tozeroy',fillcolor:'rgba(139,92,246,0.08)',line:{color:'#8b5cf6',width:3,shape:'spline'}},
    {x:tf.map(r=>r.Annee),y:tf.map(r=>r.Transactions_total),type:'scatter',mode:'lines',name:'Trans. ($Mrd)',
      line:{color:'#f59e0b',width:2.5,dash:'dot'},yaxis:'y2'},
  ],L({yaxis:{title:'Comptes (M)'},yaxis2:{title:'$Mrd',overlaying:'y',side:'right',gridcolor:'transparent'}}),CFG);

  // Scatter
  const sc=D.scatter;
  const regions=[...new Set(sc.map(s=>s.region))];
  Plotly.newPlot('chart-scatter-overview',regions.map((reg,i)=>{
    const pts=sc.filter(s=>s.region===reg);
    return {x:pts.map(p=>p.pib_hab),y:pts.map(p=>p.bancarisation),text:pts.map(p=>p.pays),
      mode:'markers+text',type:'scatter',name:reg,
      marker:{size:pts.map(p=>Math.max(10,Math.sqrt((p.pib||1))*2.2)),color:REGION_COLORS[reg]||COLORS[i],opacity:0.8,
        line:{color:'rgba(255,255,255,0.3)',width:1}},
      textposition:'top center',textfont:{size:9,color:'#8b949e'},
      hovertemplate:'<b>%{text}</b><br>PIB/hab: $%{x:,.0f}<br>Bancarisation: %{y:.1f}%<extra>'+reg+'</extra>'};
  }),L({xaxis:{title:'PIB par habitant ($)',type:'log'},yaxis:{title:'Bancarisation (%)'}}),CFG);

  // Treemap — add region parent nodes required by Plotly
  const tm=D.treemap.filter(t=>t.pib&&t.pib>0);
  const tmRegions=[...new Set(tm.map(t=>t.region))];
  const labels=[...tmRegions,...tm.map(t=>t.pays)];
  const parents=[...tmRegions.map(()=>''),...tm.map(t=>t.region)];
  const values=[...tmRegions.map(()=>0),...tm.map(t=>t.pib)];
  const colors=[...tmRegions.map(()=>3),...tm.map(t=>t.croissance||0)];
  const texts=[...tmRegions.map(r=>r),...tm.map(t=>'$'+t.pib.toFixed(1)+(currentLang==='en'?' Bn':' Mrd'))];
  Plotly.newPlot('chart-treemap',[{
    type:'treemap',
    labels:labels,
    parents:parents,
    values:values,
    text:texts,
    textinfo:'label+text',
    branchvalues:'total',
    marker:{colors:colors,colorscale:[[0,'#f85149'],[0.3,'#f59e0b'],[0.5,'#21262d'],[0.7,'#1a4d3e'],[1,'#00e5a0']],
      cmid:3,line:{width:1,color:'#21262d'},colorbar:{title:(currentLang==='en'?'Growth %':'Croissance %'),len:0.5}},
    hovertemplate:'<b>%{label}</b><br>'+(currentLang==='en'?'GDP':'PIB')+': $%{value:.1f} '+(currentLang==='en'?'Bn':'Mrd')+'<br>'+(currentLang==='en'?'Growth':'Croissance')+': %{color:.1f}%<extra></extra>',
    pathbar:{visible:true,textfont:{size:12,color:'#e6edf3'}},
    textfont:{size:12,color:'#e6edf3'},
  }],{paper_bgcolor:'rgba(0,0,0,0)',margin:{t:30,r:10,b:10,l:10},font:{family:FONT,color:'#e6edf3'}},CFG);
}

// ═══════════════════════════════════════════════════════════════════════════════
// MACRO
// ═══════════════════════════════════════════════════════════════════════════════
renderers.macro=function(){
  const ts=D.ts_continental;const years=ts.map(r=>r.Annee);
  Plotly.newPlot('chart-macro-pib',[
    {x:years,y:ts.map(r=>r.PIB_total),name:'PIB ($Mrd)',type:'bar',marker:{color:'rgba(0,229,160,0.5)',line:{color:'#00e5a0',width:1}}},
    {x:years,y:ts.map(r=>r.Croissance_moy),name:'Croissance (%)',type:'scatter',mode:'lines+markers',
      line:{color:'#f59e0b',width:3},marker:{size:5},yaxis:'y2'}
  ],L({yaxis:{title:'$Mrd'},yaxis2:{title:'%',overlaying:'y',side:'right',gridcolor:'transparent'}}),CFG);

  Plotly.newPlot('chart-macro-inflation',[
    {x:years,y:ts.map(r=>r.Inflation_moy),name:'Inflation (%)',type:'scatter',mode:'lines',
      line:{color:'#f85149',width:3,shape:'spline'},fill:'tozeroy',fillcolor:'rgba(248,81,73,0.06)'},
  ],L({yaxis:{title:'%'}}),CFG);

  Plotly.newPlot('chart-macro-fdi',[
    {x:years,y:ts.map(r=>r.FDI_total),name:'FDI',type:'bar',marker:{color:'rgba(59,130,246,0.6)'}},
    {x:years,y:ts.map(r=>r.Envois_fonds),name:'Remittances',type:'bar',marker:{color:'rgba(139,92,246,0.6)'}},
  ],L({barmode:'group',yaxis:{title:'$Mrd'}}),CFG);

  Plotly.newPlot('chart-macro-dette',[
    {x:years,y:ts.map(r=>r.Dette_moy),name:'Dette (%PIB)',type:'scatter',mode:'lines',
      line:{color:'#f59e0b',width:3,shape:'spline'},fill:'tozeroy',fillcolor:'rgba(245,158,11,0.06)'},
    {x:years,y:ts.map(r=>r.Chomage_moy),name:'Chômage (%)',type:'scatter',mode:'lines',
      line:{color:'#ec4899',width:2,dash:'dot'}},
  ],L({yaxis:{title:'%'}}),CFG);

  const rg=D.ts_region_growth;const regs=[...new Set(rg.map(r=>r.Region))];
  Plotly.newPlot('chart-macro-region-growth',regs.map((reg,i)=>{
    const pts=rg.filter(r=>r.Region===reg);
    return {x:pts.map(p=>p.Annee),y:pts.map(p=>p.Croissance_PIB),name:reg,type:'scatter',mode:'lines',
      line:{color:REGION_COLORS[reg]||COLORS[i],width:2.5,shape:'spline'}};
  }),L({yaxis:{title:'Croissance (%)',zeroline:true,zerolinecolor:'#f59e0b'}}),CFG);
};

// ═══════════════════════════════════════════════════════════════════════════════
// BANKING
// ═══════════════════════════════════════════════════════════════════════════════
renderers.banking=function(){
  const tb=D.ts_banking;const years=tb.map(r=>r.Annee);
  Plotly.newPlot('chart-bank-banc',[{x:years,y:tb.map(r=>r.Bancarisation_moy),type:'scatter',mode:'lines',
    fill:'tozeroy',fillcolor:'rgba(0,229,160,0.06)',line:{color:'#00e5a0',width:3,shape:'spline'}}],
    L({yaxis:{title:'%'}}),CFG);

  Plotly.newPlot('chart-bank-npl-car',[
    {x:years,y:tb.map(r=>r.NPL_moy),name:'NPL',type:'scatter',mode:'lines+markers',line:{color:'#f85149',width:3},marker:{size:5}},
    {x:years,y:tb.map(r=>r.CAR_moy),name:'CAR',type:'scatter',mode:'lines+markers',line:{color:'#00e5a0',width:3},marker:{size:5}},
  ],L({yaxis:{title:'%'},
    shapes:[{type:'line',y0:5,y1:5,x0:years[0],x1:years[years.length-1],line:{color:'#f59e0b',width:1,dash:'dash'}},
            {type:'line',y0:10.5,y1:10.5,x0:years[0],x1:years[years.length-1],line:{color:'#3b82f6',width:1,dash:'dash'}}],
    annotations:[{x:years[years.length-1],y:5,text:'Seuil NPL 5%',showarrow:false,font:{size:10,color:'#f59e0b'}},
                 {x:years[years.length-1],y:10.5,text:'Min Bâle III',showarrow:false,font:{size:10,color:'#3b82f6'}}]
  }),CFG);

  Plotly.newPlot('chart-bank-roe-nim',[
    {x:years,y:tb.map(r=>r.ROE_moy),name:'ROE',type:'scatter',mode:'lines',line:{color:'#8b5cf6',width:3,shape:'spline'}},
    {x:years,y:tb.map(r=>r.NIM_moy),name:'NIM',type:'scatter',mode:'lines',line:{color:'#f59e0b',width:3,shape:'spline'},yaxis:'y2'},
  ],L({yaxis:{title:'ROE (%)'},yaxis2:{title:'NIM (%)',overlaying:'y',side:'right',gridcolor:'transparent'}}),CFG);

  Plotly.newPlot('chart-bank-credit',[{x:years,y:tb.map(r=>r.Credit_PIB_moy),type:'scatter',mode:'lines',
    fill:'tozeroy',fillcolor:'rgba(59,130,246,0.06)',line:{color:'#3b82f6',width:3,shape:'spline'}}],
    L({yaxis:{title:'Crédit/PIB (%)'}}),CFG);

  const rb=D.ts_region_banc;const regs=[...new Set(rb.map(r=>r.Region))];
  Plotly.newPlot('chart-bank-region-banc',regs.map((reg,i)=>{
    const pts=rb.filter(r=>r.Region===reg);
    return {x:pts.map(p=>p.Annee),y:pts.map(p=>p.Bancarisation),name:reg,type:'scatter',mode:'lines',
      line:{color:REGION_COLORS[reg]||COLORS[i],width:2.5,shape:'spline'}};
  }),L({yaxis:{title:'Bancarisation (%)'}}),CFG);

  // Radar
  const rr=D.radar_regions;const rnames=Object.keys(rr);
  const cats=['Bancarisation','CAR','ROE','Crédit/PIB','Solidité (20-NPL)','Croissance','Mobile Money'];
  Plotly.newPlot('chart-radar-bank',rnames.map((reg,i)=>{
    const d=rr[reg];
    return {type:'scatterpolar',r:[d.bancarisation,d.car,d.roe,d.credit_pib,d.npl_inv,d.croissance,d.mm],
      theta:cats,fill:'toself',name:reg,
      fillcolor:(REGION_COLORS[reg]||COLORS[i]).replace(')',',0.1)').replace('rgb','rgba'),
      line:{color:REGION_COLORS[reg]||COLORS[i],width:2}};
  }),{paper_bgcolor:'rgba(0,0,0,0)',polar:{bgcolor:'rgba(0,0,0,0)',
    radialaxis:{visible:true,color:'#30363d',gridcolor:'#21262d'},
    angularaxis:{color:'#8b949e',gridcolor:'#21262d'}},
    font:{family:FONT,color:'#e6edf3',size:11},
    legend:{font:{size:11},bgcolor:'rgba(0,0,0,0)'},margin:{t:40,b:40,l:60,r:60},
    showlegend:true},CFG);
};

// ═══════════════════════════════════════════════════════════════════════════════
// FINTECH
// ═══════════════════════════════════════════════════════════════════════════════
renderers.fintech=function(){
  const tf=D.ts_fintech;const years=tf.map(r=>r.Annee);
  Plotly.newPlot('chart-ft-mm',[
    {x:years,y:tf.map(r=>r.Comptes_MM_total),name:'Comptes (M)',type:'bar',marker:{color:'rgba(0,229,160,0.5)'}},
    {x:years,y:tf.map(r=>r.Transactions_total),name:'Transactions ($Mrd)',type:'scatter',mode:'lines+markers',
      line:{color:'#f59e0b',width:3},yaxis:'y2'}
  ],L({yaxis:{title:'Comptes (M)'},yaxis2:{title:'$Mrd',overlaying:'y',side:'right',gridcolor:'transparent'}}),CFG);

  Plotly.newPlot('chart-ft-startups',[
    {x:years,y:tf.map(r=>r.Startups_total),name:'Startups',type:'bar',marker:{color:'rgba(139,92,246,0.5)'}},
    {x:years,y:tf.map(r=>r.Invest_total),name:'Invest ($M)',type:'scatter',mode:'lines+markers',
      line:{color:'#ec4899',width:3},yaxis:'y2'}
  ],L({yaxis:{title:'Startups'},yaxis2:{title:'$M',overlaying:'y',side:'right',gridcolor:'transparent'}}),CFG);

  const rm=D.ts_region_mm;const regs=[...new Set(rm.map(r=>r.Region))];
  Plotly.newPlot('chart-ft-region',regs.map((reg,i)=>{
    const pts=rm.filter(r=>r.Region===reg);
    return {x:pts.map(p=>p.Annee),y:pts.map(p=>p.Pop_MM),name:reg,type:'scatter',mode:'lines',
      line:{color:REGION_COLORS[reg]||COLORS[i],width:2.5,shape:'spline'}};
  }),L({yaxis:{title:'% pop. avec M-Money'}}),CFG);

  Plotly.newPlot('chart-ft-smartphone',[
    {x:years,y:tf.map(r=>r.Smartphone_moy),name:'Smartphone (%)',type:'scatter',mode:'lines',
      line:{color:'#3b82f6',width:3,shape:'spline'},fill:'tozeroy',fillcolor:'rgba(59,130,246,0.06)'},
    {x:years,y:tf.map(r=>r.Paiements_num_moy),name:'Paiements numériques (%)',type:'scatter',mode:'lines',
      line:{color:'#00e5a0',width:3,shape:'spline'}},
  ],L({yaxis:{title:'%'}}),CFG);
};

// ═══════════════════════════════════════════════════════════════════════════════
// MARKETS
// ═══════════════════════════════════════════════════════════════════════════════
renderers.markets=function(){
  const tm=D.ts_markets;const years=tm.map(r=>r.Annee);
  Plotly.newPlot('chart-mk-cap',[{x:years,y:tm.map(r=>r.Cap_totale),type:'scatter',mode:'lines',
    fill:'tozeroy',fillcolor:'rgba(59,130,246,0.06)',line:{color:'#3b82f6',width:3,shape:'spline'}}],
    L({yaxis:{title:'$Mrd'}}),CFG);

  Plotly.newPlot('chart-mk-spread',[{x:years,y:tm.map(r=>r.Spread_moy),type:'scatter',mode:'lines',
    fill:'tozeroy',fillcolor:'rgba(248,81,73,0.06)',line:{color:'#f85149',width:3,shape:'spline'},
    hovertemplate:'%{x}: %{y:.0f} pb<extra></extra>'}],
    L({yaxis:{title:'Points de base'},
      shapes:[{type:'line',y0:600,y1:600,x0:years[0],x1:years[years.length-1],line:{color:'#f59e0b',width:1,dash:'dash'}}],
      annotations:[{x:years[years.length-1],y:600,text:'Seuil risque élevé',showarrow:false,font:{size:10,color:'#f59e0b'}}]
    }),CFG);

  const mk=D.markets.filter(m=>m.Capitalisation_Mrd).sort((a,b)=>b.Capitalisation_Mrd-a.Capitalisation_Mrd);
  Plotly.newPlot('chart-mk-bourses',[{
    y:mk.map(m=>m.Bourse+' ('+m.Pays+')'),x:mk.map(m=>m.Capitalisation_Mrd),
    type:'bar',orientation:'h',
    marker:{color:mk.map((_,i)=>COLORS[i%COLORS.length]),line:{color:'rgba(255,255,255,0.1)',width:1}},
    text:mk.map(m=>'$'+m.Capitalisation_Mrd+' Mrd'),textposition:'outside',textfont:{size:11,color:'#e6edf3'},
    hovertemplate:'<b>%{y}</b><br>Cap: $%{x:.1f} Mrd<extra></extra>'
  }],L({margin:{l:200},yaxis:{autorange:'reversed'}}),CFG);
};

// ═══════════════════════════════════════════════════════════════════════════════
// MICROFINANCE
// ═══════════════════════════════════════════════════════════════════════════════
renderers.microfinance=function(){
  const tm=D.ts_mfi;const years=tm.map(r=>r.Annee);
  Plotly.newPlot('chart-mfi-par-oss',[
    {x:years,y:tm.map(r=>r.PAR30_moy),name:'PAR30 (%)',type:'scatter',mode:'lines',line:{color:'#f85149',width:3,shape:'spline'}},
    {x:years,y:tm.map(r=>r.OSS_moy),name:'OSS (%)',type:'scatter',mode:'lines',line:{color:'#00e5a0',width:3,shape:'spline'},yaxis:'y2'},
  ],L({yaxis:{title:'PAR30 (%)'},yaxis2:{title:'OSS (%)',overlaying:'y',side:'right',gridcolor:'transparent'},
    shapes:[{type:'line',y0:100,y1:100,x0:years[0],x1:years[years.length-1],yref:'y2',line:{color:'#f59e0b',width:1,dash:'dash'}}]}),CFG);

  Plotly.newPlot('chart-mfi-clients',[
    {x:years,y:tm.map(r=>r.Clients_total),name:'Clients (000)',type:'bar',marker:{color:'rgba(139,92,246,0.5)'}},
    {x:years,y:tm.map(r=>r.Pct_femmes_moy),name:'% Femmes',type:'scatter',mode:'lines+markers',
      line:{color:'#ec4899',width:3},yaxis:'y2'},
  ],L({yaxis:{title:'Clients (000)'},yaxis2:{title:'% Femmes',overlaying:'y',side:'right',gridcolor:'transparent'}}),CFG);

  Plotly.newPlot('chart-mfi-portf',[{x:years,y:tm.map(r=>r.Portefeuille_total),type:'scatter',mode:'lines',
    fill:'tozeroy',fillcolor:'rgba(245,158,11,0.06)',line:{color:'#f59e0b',width:3,shape:'spline'}}],L({yaxis:{title:'$M'}}),CFG);

  Plotly.newPlot('chart-mfi-inclusion',[{x:years,y:tm.map(r=>r.Score_inclusion_moy),type:'scatter',mode:'lines',
    fill:'tozeroy',fillcolor:'rgba(0,229,160,0.06)',line:{color:'#00e5a0',width:3,shape:'spline'}}],
    L({yaxis:{title:'Score (0-10)',range:[0,10]}}),CFG);
};

// ═══════════════════════════════════════════════════════════════════════════════
// CRISES
// ═══════════════════════════════════════════════════════════════════════════════
renderers.crises=function(){
  const cr=D.crises;
  document.getElementById('crises-count').textContent=cr.length+' ÉVÉNEMENTS';
  const byYear={};cr.forEach(c=>{if(c.Annee)byYear[c.Annee]=(byYear[c.Annee]||0)+1;});
  const yrs=Object.keys(byYear).sort();
  Plotly.newPlot('chart-crises-year',[{x:yrs,y:yrs.map(y=>byYear[y]),type:'bar',
    marker:{color:yrs.map(y=>byYear[y]>10?'#f85149':byYear[y]>5?'#f59e0b':'#00e5a0'),
      line:{width:1,color:'rgba(255,255,255,0.1)'}}}],L({yaxis:{title:'Nb crises'}}),CFG);

  Plotly.newPlot('chart-crises-impact',[{
    x:cr.map(c=>c.Severite),y:cr.map(c=>c.Impact_PIB),text:cr.map(c=>c.Pays+' ('+c.Annee+')'),
    mode:'markers',type:'scatter',
    marker:{size:cr.map(c=>Math.max(8,Math.abs(c.Impact_PIB||1)*1.8)),
      color:cr.map(c=>c.Severite),colorscale:[[0,'#f59e0b'],[0.5,'#f85149'],[1,'#7f1d1d']],
      opacity:0.75,line:{color:'rgba(255,255,255,0.2)',width:1}},
    hovertemplate:'<b>%{text}</b><br>Sévérité: %{x}<br>Impact PIB: %{y}%<extra></extra>'
  }],L({xaxis:{title:'Sévérité (1-5)'},yaxis:{title:'Impact PIB (%)'}}),CFG);

  let t='<table class="data-table"><thead><tr>';
  ['Pays','Année','Type de Crise','Sév.','Impact PIB','NPL+','Aide FMI','Durée'].forEach(h=>t+='<th>'+h+'</th>');
  t+='</tr></thead><tbody>';
  cr.sort((a,b)=>(b.Annee||0)-(a.Annee||0)).forEach(c=>{
    t+='<tr><td>'+c.Pays+'</td><td>'+c.Annee+'</td><td>'+c.Type_crise+'</td>';
    t+='<td><span class="sev-'+(c.Severite||1)+'">'+'★'.repeat(c.Severite||1)+'</span></td>';
    t+='<td style="color:'+(c.Impact_PIB<-5?'#f85149':c.Impact_PIB<0?'#f59e0b':'#00e5a0')+'">'+(c.Impact_PIB||'—')+'%</td>';
    t+='<td>'+(c.Hausse_NPL?'+'+c.Hausse_NPL+'pp':'—')+'</td>';
    t+='<td>'+(c.Aide_FMI?'$'+c.Aide_FMI+'Mrd':'—')+'</td>';
    t+='<td>'+(c.Duree_trim||'—')+' trim.</td></tr>';
  });
  t+='</tbody></table>';
  document.getElementById('crises-table-container').innerHTML=t;
};

// ═══════════════════════════════════════════════════════════════════════════════
// RANKINGS
// ═══════════════════════════════════════════════════════════════════════════════
renderers.rankings=function(){renderRanking();};
function renderRanking(){
  const key=document.getElementById('ranking-select').value;
  const r=D.rankings[key];if(!r)return;
  const vk=Object.keys(r.top[0]).find(k=>k!=='Pays');
  Plotly.newPlot('chart-ranking-top',[{
    y:r.top.map(t=>t.Pays).reverse(),x:r.top.map(t=>t[vk]).reverse(),type:'bar',orientation:'h',
    marker:{color:r.top.map((_,i)=>`rgba(0,229,160,${0.35+0.045*i})`).reverse(),line:{width:1,color:'rgba(255,255,255,0.1)'}},
    text:r.top.map(t=>t[vk]?.toFixed?.(1)??t[vk]).reverse(),textposition:'outside',textfont:{size:11,color:'#e6edf3'}
  }],L({margin:{l:160}}),CFG);
  Plotly.newPlot('chart-ranking-bottom',[{
    y:r.bottom.map(t=>t.Pays),x:r.bottom.map(t=>t[vk]),type:'bar',orientation:'h',
    marker:{color:r.bottom.map((_,i)=>`rgba(248,81,73,${0.25+0.045*i})`),line:{width:1,color:'rgba(255,255,255,0.1)'}},
    text:r.bottom.map(t=>t[vk]?.toFixed?.(1)??t[vk]),textposition:'outside',textfont:{size:11,color:'#e6edf3'}
  }],L({margin:{l:160}}),CFG);
}

// ═══════════════════════════════════════════════════════════════════════════════
// CORRELATIONS
// ═══════════════════════════════════════════════════════════════════════════════
renderers.correlations=function(){
  const c=D.correlations;if(!c.labels||!c.labels.length)return;
  Plotly.newPlot('chart-corr-heatmap',[{
    z:c.values,x:c.labels,y:c.labels,type:'heatmap',
    colorscale:[[0,'#f85149'],[0.25,'#21262d'],[0.5,'#161b22'],[0.75,'#1a4d3e'],[1,'#00e5a0']],
    zmin:-1,zmax:1,
    hovertemplate:'%{y} × %{x}: r = %{z:.3f}<extra></extra>',
    text:c.values.map(row=>row.map(v=>v!==null?v.toFixed(2):'')),
    texttemplate:'%{text}',textfont:{size:10,color:'#e6edf3'},
  }],L({margin:{t:30,l:130,b:130,r:30},xaxis:{tickangle:45},yaxis:{autorange:'reversed'}}),CFG);
};

// ═══════════════════════════════════════════════════════════════════════════════
// COUNTRY
// ═══════════════════════════════════════════════════════════════════════════════
renderers.country=function(){
  const sel=document.getElementById('country-select');
  sel.innerHTML=D.country_list.map(c=>'<option value="'+c+'">'+c+'</option>').join('');
  renderCountry();
};
function renderCountry(){
  const p=document.getElementById('country-select').value;if(!p)return;
  const cm=D.country_macro[p],cb=D.country_bank[p],cf=D.country_fintech[p];
  ['macro','bank','fintech','extra'].forEach(s=>document.getElementById('country-title-'+s).textContent=p+' — '+(
    {macro:'PIB & Croissance',bank:'Bancarisation & NPL',fintech:'Mobile Money',extra:'Inflation & Dette'}[s]));

  if(cm){
    Plotly.newPlot('chart-country-macro',[
      {x:cm.annees,y:cm.pib,name:'PIB ($Mrd)',type:'bar',marker:{color:'rgba(0,229,160,0.4)'}},
      {x:cm.annees,y:cm.croissance,name:'Croissance (%)',type:'scatter',mode:'lines+markers',
        line:{color:'#f59e0b',width:3},marker:{size:5},yaxis:'y2'},
    ],L({yaxis:{title:'$Mrd'},yaxis2:{title:'%',overlaying:'y',side:'right',gridcolor:'transparent'}}),CFG);
    Plotly.newPlot('chart-country-extra',[
      {x:cm.annees,y:cm.inflation,name:'Inflation',type:'scatter',mode:'lines',line:{color:'#f85149',width:2.5,shape:'spline'}},
      {x:cm.annees,y:cm.dette,name:'Dette (%PIB)',type:'scatter',mode:'lines',line:{color:'#f59e0b',width:2.5,shape:'spline'},yaxis:'y2'},
    ],L({yaxis:{title:'Inflation (%)'},yaxis2:{title:'Dette (%PIB)',overlaying:'y',side:'right',gridcolor:'transparent'}}),CFG);
  }
  if(cb){
    Plotly.newPlot('chart-country-bank',[
      {x:cb.annees,y:cb.bancarisation,name:'Bancarisation',type:'scatter',mode:'lines',
        line:{color:'#00e5a0',width:3,shape:'spline'},fill:'tozeroy',fillcolor:'rgba(0,229,160,0.06)'},
      {x:cb.annees,y:cb.npl,name:'NPL',type:'scatter',mode:'lines',line:{color:'#f85149',width:2.5,shape:'spline'},yaxis:'y2'},
    ],L({yaxis:{title:'Bancarisation (%)'},yaxis2:{title:'NPL (%)',overlaying:'y',side:'right',gridcolor:'transparent'}}),CFG);
  }
  if(cf){
    Plotly.newPlot('chart-country-fintech',[
      {x:cf.annees,y:cf.comptes_mm,name:'Comptes (M)',type:'bar',marker:{color:'rgba(139,92,246,0.4)'}},
      {x:cf.annees,y:cf.pop_mm,name:'% pop.',type:'scatter',mode:'lines+markers',
        line:{color:'#ec4899',width:3},yaxis:'y2'},
    ],L({yaxis:{title:'Millions'},yaxis2:{title:'%',overlaying:'y',side:'right',gridcolor:'transparent'}}),CFG);
  }
}

// ═══════════════════════════════════════════════════════════════════════════════
// REGIONS
// ═══════════════════════════════════════════════════════════════════════════════
renderers.regions=function(){
  const rm=D.regions_macro,rb=D.regions_bank,rf=D.regions_fintech;
  Plotly.newPlot('chart-reg-pib',[{
    x:rm.map(r=>r.Region),y:rm.map(r=>r.PIB_total),type:'bar',
    marker:{color:rm.map(r=>REGION_COLORS[r.Region]||'#00e5a0'),line:{width:1,color:'rgba(255,255,255,0.1)'}},
    text:rm.map(r=>'$'+r.PIB_total.toFixed(0)+' Mrd'),textposition:'outside',textfont:{size:11,color:'#e6edf3'}
  }],L({yaxis:{title:'$Mrd'}}),CFG);

  if(rb.length){
    Plotly.newPlot('chart-reg-bank',[
      {x:rb.map(r=>r.Region),y:rb.map(r=>r.Bancarisation_moy),name:'Bancarisation',type:'bar',marker:{color:'rgba(0,229,160,0.6)'}},
      {x:rb.map(r=>r.Region),y:rb.map(r=>r.NPL_moy),name:'NPL',type:'bar',marker:{color:'rgba(248,81,73,0.6)'}},
      {x:rb.map(r=>r.Region),y:rb.map(r=>r.CAR_moy),name:'CAR',type:'bar',marker:{color:'rgba(59,130,246,0.6)'}},
    ],L({barmode:'group',yaxis:{title:'%'}}),CFG);
  }
  if(rf.length){
    Plotly.newPlot('chart-reg-fintech',[{
      x:rf.map(r=>r.Region),y:rf.map(r=>r.Pop_MM_moy),type:'bar',
      marker:{color:rf.map(r=>REGION_COLORS[r.Region]||'#8b5cf6'),line:{width:1,color:'rgba(255,255,255,0.1)'}},
      text:rf.map(r=>r.Pop_MM_moy.toFixed(1)+'%'),textposition:'outside',textfont:{size:11,color:'#e6edf3'}
    }],L({yaxis:{title:'% pop.'}}),CFG);
  }
  const rn=D.ts_region_npl;const regs=[...new Set(rn.map(r=>r.Region))];
  Plotly.newPlot('chart-reg-npl-ts',regs.map((reg,i)=>{
    const pts=rn.filter(r=>r.Region===reg);
    return {x:pts.map(p=>p.Annee),y:pts.map(p=>p.NPL),name:reg,type:'scatter',mode:'lines',
      line:{color:REGION_COLORS[reg]||COLORS[i],width:2.5,shape:'spline'}};
  }),L({yaxis:{title:'NPL (%)'}}),CFG);
};

// ═══════════════════════════════════════════════════════════════════════════════
// STATISTIQUES AVANCÉES
// ═══════════════════════════════════════════════════════════════════════════════
renderers.statistics=function(){
  const S=D.advanced_stats;

  // ── Descriptive Stats Table ──
  const ds=S.descriptive;
  const dkeys=Object.keys(ds);
  let ht='<table class="data-table"><thead><tr><th>Variable</th><th>N</th><th>Moy.</th><th>Méd.</th><th>Éc-type</th><th>Min</th><th>Q1</th><th>Q3</th><th>Max</th><th>CV%</th><th>Skewness</th><th>Kurtosis</th></tr></thead><tbody>';
  dkeys.forEach(k=>{const d=ds[k];ht+='<tr><td style="font-weight:600;color:var(--accent)">'+k+'</td><td>'+d.n+'</td><td>'+d.mean+'</td><td>'+d.median+'</td><td>'+d.std+'</td><td>'+d.min+'</td><td>'+d.q1+'</td><td>'+d.q3+'</td><td>'+d.max+'</td><td>'+(d.cv||'—')+'</td><td style="color:'+(Math.abs(d.skew)>1?'var(--accent3)':'var(--text)')+'">'+d.skew+'</td><td style="color:'+(Math.abs(d.kurtosis)>3?'var(--accent3)':'var(--text)')+'">'+d.kurtosis+'</td></tr>';});
  ht+='</tbody></table>';
  document.getElementById('desc-stats-table').innerHTML=ht;

  // ── Normality Tests ──
  let nt='<table class="data-table"><thead><tr><th>Variable</th><th>N</th><th>W (Shapiro)</th><th>p-value</th><th>Résultat</th></tr></thead><tbody>';
  S.normality.forEach(t=>{
    const ok=t.normal;
    nt+='<tr><td style="font-weight:600">'+t.variable+'</td><td>'+t.n+'</td><td>'+t.W+'</td><td style="color:'+(ok?'var(--green)':'var(--red)')+'">'+t.p_value+'</td><td style="color:'+(ok?'var(--green)':'var(--red)')+';font-weight:600">'+(ok?'✓ Normale':'✗ Non-normale')+'</td></tr>';
  });
  nt+='</tbody></table>';
  document.getElementById('normality-table').innerHTML=nt;

  // ── Distribution selector ──
  const distSel=document.getElementById('dist-var-select');
  const distKeys=Object.keys(S.distributions);
  distSel.innerHTML=distKeys.map(k=>'<option value="'+k+'">'+k+'</option>').join('');
  renderDistribution();

  // ── Regression selector ──
  const regSel=document.getElementById('reg-select');
  regSel.innerHTML=S.regressions.map((r,i)=>'<option value="'+i+'">'+r.label+' (R²='+r.r2+')</option>').join('');
  renderRegression();

  // ── Regression summary table ──
  let rt='<table class="data-table"><thead><tr><th>Modèle</th><th>N</th><th>R²</th><th>r</th><th>Pente (β)</th><th>p-value</th><th>Significatif</th></tr></thead><tbody>';
  S.regressions.forEach(r=>{
    rt+='<tr><td style="font-weight:600">'+r.label+'</td><td>'+r.n+'</td><td style="color:var(--accent);font-weight:700">'+r.r2+'</td><td>'+r.r+'</td><td>'+r.slope+'</td>';
    rt+='<td style="color:'+(r.significant?'var(--green)':'var(--red)')+'">'+r.p_value+'</td>';
    rt+='<td style="color:'+(r.significant?'var(--green)':'var(--red)')+';font-weight:600">'+(r.significant?'✓ Oui (p<0.05)':'✗ Non')+'</td></tr>';
  });
  rt+='</tbody></table>';
  document.getElementById('reg-summary-table').innerHTML=rt;

  // ── Panel Regression ──
  const pr=S.panel_regression;
  if(pr){
    document.getElementById('panel-reg-info').innerHTML='<div style="background:var(--bg3);border-radius:var(--radius);padding:20px;"><p style="font-size:13px;color:var(--text2);margin-bottom:12px;">Modèle OLS poolé sur données panel ('+pr.n+' obs.)</p><p style="font-size:11px;color:var(--text2);margin-bottom:8px;">Variable dépendante: <strong style="color:var(--accent)">'+pr.dep_var+'</strong></p><div style="display:flex;gap:16px;margin-bottom:12px;"><div><span style="font-size:11px;color:var(--text3)">R²</span><div style="font-size:28px;font-weight:800;color:var(--accent)">'+pr.r2+'</div></div><div><span style="font-size:11px;color:var(--text3)">R² ajusté</span><div style="font-size:28px;font-weight:800;color:var(--accent2)">'+pr.r2_adj+'</div></div><div><span style="font-size:11px;color:var(--text3)">N obs.</span><div style="font-size:28px;font-weight:800;color:var(--accent5)">'+pr.n+'</div></div></div><p style="font-size:10px;color:var(--text3);">'+pr.k+' variables explicatives</p></div>';
    let pt='<table class="data-table"><thead><tr><th>Variable</th><th>Coeff. (β)</th><th>Std. Err.</th><th>t-stat</th><th>p-value</th><th>Sig.</th></tr></thead><tbody>';
    pr.coefficients.forEach(c=>{
      pt+='<tr><td style="font-weight:600">'+c.var+'</td><td style="font-family:JetBrains Mono,monospace;color:var(--accent)">'+c.coeff+'</td><td>'+c.se+'</td><td>'+c.t+'</td>';
      pt+='<td style="color:'+(c.sig?'var(--green)':'var(--text2)')+'">'+c.p+'</td>';
      pt+='<td>'+(c.sig?'<span style="color:var(--green);font-weight:700">★★★</span>':'<span style="color:var(--text3)">ns</span>')+'</td></tr>';
    });
    pt+='</tbody></table>';
    document.getElementById('panel-reg-table-container').innerHTML=pt;
  }

  // ── ANOVA selector ──
  const aSel=document.getElementById('anova-select');
  aSel.innerHTML=S.anova.map((a,i)=>'<option value="'+i+'">'+a.variable+' (F='+a.F+', p='+a.p_value+')</option>').join('');
  renderAnova();

  // ── ANOVA + Kruskal table ──
  let at='<table class="data-table"><thead><tr><th>Variable</th><th>F (ANOVA)</th><th>p ANOVA</th><th>H (Kruskal)</th><th>p Kruskal</th><th>Significatif</th></tr></thead><tbody>';
  S.anova.forEach(a=>{
    const kr=S.kruskal.find(k=>k.variable===a.variable);
    at+='<tr><td style="font-weight:600">'+a.variable+'</td><td>'+a.F+'</td><td style="color:'+(a.significant?'var(--green)':'var(--red)')+'">'+a.p_value+'</td>';
    at+='<td>'+(kr?kr.H:'—')+'</td><td style="color:'+(kr&&kr.significant?'var(--green)':'var(--red)')+'">'+(kr?kr.p_value:'—')+'</td>';
    at+='<td style="color:'+(a.significant?'var(--green)':'var(--red)')+';font-weight:600">'+(a.significant?'✓ Diff. significative':'✗ Non significatif')+'</td></tr>';
  });
  at+='</tbody></table>';
  document.getElementById('anova-table').innerHTML=at;

  // ── Spearman Heatmap ──
  const sp=S.spearman;
  if(sp.labels.length){
    Plotly.newPlot('chart-spearman',[{
      z:sp.rho,x:sp.labels,y:sp.labels,type:'heatmap',
      colorscale:[[0,'#f85149'],[0.25,'#21262d'],[0.5,'#161b22'],[0.75,'#1a4d3e'],[1,'#00e5a0']],
      zmin:-1,zmax:1,
      text:sp.rho.map(row=>row.map(v=>v!==null?v.toFixed(3):'')),texttemplate:'%{text}',textfont:{size:10,color:'#e6edf3'},
      hovertemplate:'%{y} × %{x}: ρ = %{z:.3f}<extra>Spearman</extra>',
    }],L({margin:{t:30,l:130,b:130,r:30},xaxis:{tickangle:45},yaxis:{autorange:'reversed'}}),CFG);
  }

  // ── Trends table ──
  const tSel=document.getElementById('trend-select');
  tSel.innerHTML=S.trends.map((t,i)=>'<option value="'+i+'">'+t.variable+' (ρ='+t.rho+')</option>').join('');
  renderTrend();

  let tt='<table class="data-table"><thead><tr><th>Variable</th><th>Direction</th><th>Spearman ρ</th><th>p-value</th><th>Années</th><th>Significatif</th></tr></thead><tbody>';
  S.trends.forEach(t=>{
    const up=t.direction==='hausse';
    tt+='<tr><td style="font-weight:600">'+t.variable+'</td><td style="color:'+(up?'var(--green)':'var(--red)')+'">'+( up?'↗ Hausse':'↘ Baisse')+'</td>';
    tt+='<td style="font-weight:700;color:'+(Math.abs(t.rho)>0.7?'var(--accent)':'var(--text)')+'">'+t.rho+'</td>';
    tt+='<td style="color:'+(t.significant?'var(--green)':'var(--text2)')+'">'+t.p_value+'</td>';
    tt+='<td>'+t.n_years+'</td>';
    tt+='<td style="color:'+(t.significant?'var(--green)':'var(--red)')+';font-weight:600">'+(t.significant?'✓ Oui':'✗ Non')+'</td></tr>';
  });
  tt+='</tbody></table>';
  document.getElementById('trend-table').innerHTML=tt;

  // ── Outliers table ──
  const ol=S.outliers;
  const okeys=Object.keys(ol);
  let ot='<table class="data-table"><thead><tr><th>Variable</th><th>Pays (Outlier)</th><th>Valeur</th></tr></thead><tbody>';
  okeys.forEach(k=>{
    ol[k].forEach((o,i)=>{
      ot+='<tr><td'+(i===0?' style="font-weight:600;color:var(--accent3)"':' style="color:transparent"')+'>'+k+'</td><td>'+o.pays+'</td><td style="color:var(--accent3);font-weight:600">'+o.value+'</td></tr>';
    });
  });
  ot+='</tbody></table>';
  document.getElementById('outliers-table').innerHTML=ot;
};

// ── Render helpers ──
function renderDistribution(){
  const S=D.advanced_stats;
  const v=document.getElementById('dist-var-select').value;
  const dd=S.distributions[v];if(!dd)return;
  const ds=S.descriptive[v];
  Plotly.react('chart-distribution',[
    {y:dd.values,type:'box',name:v,boxpoints:'all',jitter:0.4,pointpos:-1.8,
      marker:{color:'#00e5a0',size:5,opacity:0.6,line:{width:1,color:'rgba(255,255,255,0.2)'}},
      line:{color:'#00e5a0',width:2},fillcolor:'rgba(0,229,160,0.15)',
      text:dd.pays,hovertemplate:'<b>%{text}</b>: %{y:.2f}<extra></extra>'},
  ],L({yaxis:{title:v},
    shapes:ds?[{type:'line',y0:ds.mean,y1:ds.mean,x0:-0.5,x1:0.5,line:{color:'#f59e0b',width:2,dash:'dash'}},
               {type:'line',y0:ds.median,y1:ds.median,x0:-0.5,x1:0.5,line:{color:'#3b82f6',width:2,dash:'dot'}}]:[],
    annotations:ds?[{x:0.45,y:ds.mean,text:'μ='+ds.mean,showarrow:false,font:{size:10,color:'#f59e0b'}},
                    {x:0.45,y:ds.median,text:'Med='+ds.median,showarrow:false,font:{size:10,color:'#3b82f6'}}]:[],
  }),CFG);
}

function renderRegression(){
  const S=D.advanced_stats;
  const idx=parseInt(document.getElementById('reg-select').value);
  const r=S.regressions[idx];if(!r)return;
  const xmin=Math.min(...r.points.map(p=>p.x)),xmax=Math.max(...r.points.map(p=>p.x));
  const xrng=[xmin-(xmax-xmin)*0.05,xmax+(xmax-xmin)*0.05];
  const yline=[r.intercept+r.slope*xrng[0],r.intercept+r.slope*xrng[1]];
  document.getElementById('reg-equation').textContent=
    r.yvar+' = '+r.slope.toFixed(4)+'·'+r.xvar+' + '+r.intercept.toFixed(2)+'  |  R²='+r.r2+'  |  p='+r.p_value+(r.significant?' ★★★':' ns');
  Plotly.react('chart-regression',[
    {x:r.points.map(p=>p.x),y:r.points.map(p=>p.y),text:r.points.map(p=>p.pays),
      mode:'markers+text',type:'scatter',name:'Observations',textposition:'top center',textfont:{size:8,color:'#8b949e'},
      marker:{size:10,color:'#00e5a0',opacity:0.8,line:{color:'rgba(255,255,255,0.3)',width:1}},
      hovertemplate:'<b>%{text}</b><br>'+r.xvar+': %{x:.2f}<br>'+r.yvar+': %{y:.2f}<extra></extra>'},
    {x:xrng,y:yline,mode:'lines',type:'scatter',name:'Régression OLS',
      line:{color:'#f59e0b',width:3,dash:'dash'}},
  ],L({xaxis:{title:r.xvar},yaxis:{title:r.yvar},
    annotations:[{x:xrng[1],y:yline[1],text:'R²='+r.r2,showarrow:true,arrowcolor:'#f59e0b',font:{size:12,color:'#f59e0b'}}]}),CFG);
}

function renderAnova(){
  const S=D.advanced_stats;
  const idx=parseInt(document.getElementById('anova-select').value);
  const a=S.anova[idx];if(!a)return;
  Plotly.react('chart-anova',[{
    x:a.groups.map(g=>g.region),y:a.groups.map(g=>g.mean),type:'bar',
    error_y:{type:'data',array:a.groups.map(g=>g.std),visible:true,color:'#f59e0b',thickness:2},
    marker:{color:a.groups.map(g=>REGION_COLORS[g.region]||'#00e5a0'),line:{width:1,color:'rgba(255,255,255,0.15)'}},
    text:a.groups.map(g=>'μ='+g.mean+'±'+g.std+' (n='+g.n+')'),textposition:'outside',textfont:{size:10,color:'#e6edf3'},
    hovertemplate:'<b>%{x}</b><br>Moyenne: %{y:.2f}<br>N: '+a.groups.map(g=>g.n).join(',')+' <extra></extra>',
  }],L({yaxis:{title:a.variable},
    annotations:[{x:0.5,y:1.08,xref:'paper',yref:'paper',showarrow:false,
      text:'F='+a.F+' | p='+a.p_value+(a.significant?' → Différence significative ★★★':' → Non significatif'),
      font:{size:12,color:a.significant?'#00e5a0':'#f85149'}}]
  }),CFG);
}

function renderTrend(){
  const S=D.advanced_stats;
  const idx=parseInt(document.getElementById('trend-select').value);
  const t=S.trends[idx];if(!t)return;
  const x=t.ts.map(p=>p.year),y=t.ts.map(p=>p.value);
  // Linear fit on time series
  const n=x.length,sx=x.reduce((a,b)=>a+b,0),sy=y.reduce((a,b)=>a+b,0);
  const sxy=x.reduce((a,xi,i)=>a+xi*y[i],0),sx2=x.reduce((a,xi)=>a+xi*xi,0);
  const slope=(n*sxy-sx*sy)/(n*sx2-sx*sx),inter=(sy-slope*sx)/n;
  Plotly.react('chart-trend',[
    {x:x,y:y,type:'scatter',mode:'lines+markers',name:t.variable,
      line:{color:'#00e5a0',width:3,shape:'spline'},marker:{size:5}},
    {x:[x[0],x[x.length-1]],y:[inter+slope*x[0],inter+slope*x[x.length-1]],
      type:'scatter',mode:'lines',name:'Tendance linéaire',
      line:{color:'#f59e0b',width:2,dash:'dash'}},
  ],L({yaxis:{title:t.variable},
    annotations:[{x:0.5,y:1.08,xref:'paper',yref:'paper',showarrow:false,
      text:'Spearman ρ='+t.rho+' | p='+t.p_value+' | '+(t.direction==='hausse'?'↗ Tendance haussière':'↘ Tendance baissière'),
      font:{size:12,color:t.significant?'#00e5a0':'#f85149'}}]
  }),CFG);
}

function exportStatsCSV(){
  const ds=D.advanced_stats.descriptive;
  let csv='Variable,N,Moyenne,Mediane,Ecart-type,Min,Q1,Q3,Max,CV_pct,Skewness,Kurtosis\n';
  Object.keys(ds).forEach(k=>{const d=ds[k];csv+=k+','+d.n+','+d.mean+','+d.median+','+d.std+','+d.min+','+d.q1+','+d.q3+','+d.max+','+(d.cv||'')+','+d.skew+','+d.kurtosis+'\n';});
  const blob=new Blob([csv],{type:'text/csv;charset=utf-8;'});
  const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download='AfricaFinance_Stats_Descriptives.csv';a.click();
}

// ═══════════════════════════════════════════════════════════════════════════════
// I18N — ENGLISH / FRENCH TOGGLE
// ═══════════════════════════════════════════════════════════════════════════════
let currentLang = 'en';
const I18N = {
  header_sub: {en:'54 Countries · 25 Years · 12 Dimensions · 15,000+ Observations — Analytics Dashboard', fr:'54 Pays · 25 Ans · 12 Dimensions · 15 000+ Observations — Dashboard Analytique'},
  // Nav
  nav_overview: {en:'📊 Overview', fr:'📊 Synthèse'},
  nav_choropleth: {en:'🗺️ Choropleth Maps', fr:'🗺️ Cartes Choroplèthes'},
  nav_macro: {en:'💰 Macroeconomics', fr:'💰 Macroéconomie'},
  nav_banking: {en:'🏦 Banking Sector', fr:'🏦 Secteur Bancaire'},
  nav_fintech: {en:'📱 Fintech & M-Money', fr:'📱 Fintech & M-Money'},
  nav_markets: {en:'📈 Markets', fr:'📈 Marchés'},
  nav_microfinance: {en:'🏘️ Microfinance', fr:'🏘️ Microfinance'},
  nav_crises: {en:'⚠️ Crises', fr:'⚠️ Crises'},
  nav_rankings: {en:'🏆 Rankings', fr:'🏆 Rankings'},
  nav_correlations: {en:'🔗 Correlations', fr:'🔗 Corrélations'},
  nav_country: {en:'🔍 Country', fr:'🔍 Pays'},
  nav_regions: {en:'🌍 Regions', fr:'🌍 Régions'},
  nav_statistics: {en:'📐 Advanced Statistics', fr:'📐 Statistiques Avancées'},
  // Modal
  modal_title: {en:'⬇ Export Charts', fr:'⬇ Exporter les Graphiques'},
  modal_desc: {en:'Click the desired format. All visible charts will be exported.', fr:'Cliquez sur le format souhaité. Tous les graphiques visibles seront exportés.'},
  modal_close: {en:'Close', fr:'Fermer'},
  export_png: {en:'📸 PNG (high resolution)', fr:'📸 PNG (haute résolution)'},
  export_svg: {en:'🎨 SVG (vector)', fr:'🎨 SVG (vectoriel)'},
  export_csv: {en:'📊 CSV (data)', fr:'📊 CSV (données)'},
  export_json: {en:'🔧 JSON (data)', fr:'🔧 JSON (données)'},
  // Sections
  sec_overview: {en:'📊 Executive Summary — Africa Finance 2024', fr:'📊 Synthèse Exécutive — Africa Finance 2024'},
  tag_overview: {en:'ANALYTICS DASHBOARD', fr:'DASHBOARD ANALYTIQUE'},
  sec_choropleth: {en:'🗺️ Choropleth Maps — Financial Africa', fr:'🗺️ Cartes Choroplèthes — Afrique Financière'},
  tag_choropleth: {en:'GEOVISUALIZATION', fr:'GÉOVISUALISATION'},
  sec_macro: {en:'💰 Macroeconomic Analysis (2000-2024)', fr:'💰 Analyse Macroéconomique (2000-2024)'},
  sec_banking: {en:'🏦 African Banking Sector', fr:'🏦 Secteur Bancaire Africain'},
  sec_fintech: {en:'📱 Fintech & Mobile Money', fr:'📱 Fintech & Mobile Money'},
  tag_fintech: {en:'FINANCIAL INNOVATION', fr:'INNOVATION FINANCIÈRE'},
  sec_markets: {en:'📈 African Financial Markets', fr:'📈 Marchés Financiers Africains'},
  tag_markets: {en:'29 EXCHANGES · EUROBONDS', fr:'29 BOURSES · EUROBONDS'},
  sec_mfi: {en:'🏘️ Microfinance & Financial Inclusion', fr:'🏘️ Microfinance & Inclusion Financière'},
  sec_crises: {en:'⚠️ Financial Crises & Shocks', fr:'⚠️ Crises & Chocs Financiers'},
  sec_rankings: {en:'🏆 Rankings & Classifications 2024', fr:'🏆 Classements & Rankings 2024'},
  sec_correlations: {en:'🔗 Correlation Matrix', fr:'🔗 Matrice de Corrélations'},
  sec_country: {en:'🔍 Detailed Country Analysis', fr:'🔍 Analyse Détaillée par Pays'},
  sec_regions: {en:'🌍 Regional Comparative Analysis', fr:'🌍 Analyse Régionale Comparative'},
  tag_regions: {en:'5 REGIONS', fr:'5 RÉGIONS'},
  sec_statistics: {en:'📐 Advanced Statistics & Econometric Tests', fr:'📐 Statistiques Avancées & Tests Économétriques'},
  tag_statistics: {en:'REGRESSION · ANOVA · AUTOCORRELATION · DISTRIBUTIONS', fr:'RÉGRESSION · ANOVA · AUTOCORRÉLATION · DISTRIBUTIONS'},
  // Chart titles
  chart_pib_total: {en:'Total African GDP ($Bn) — 25-Year Evolution', fr:'PIB Africain Total ($Mrd) — Évolution 25 ans'},
  chart_growth_infl: {en:'Average GDP Growth vs Inflation', fr:'Croissance PIB Moyenne vs Inflation'},
  chart_banc_npl: {en:'Banking Rate & NPL — Continental Trajectory', fr:'Bancarisation & NPL — Trajectoire Continentale'},
  chart_mm_explosion: {en:'Mobile Money — Continental Explosion', fr:'Mobile Money — Explosion Continentale'},
  chart_scatter_gdp: {en:'GDP/capita vs Banking Rate (54 countries, 2024) — Analytical Scatter', fr:'PIB/habitant vs Bancarisation (54 pays, 2024) — Scatter analytique'},
  chart_treemap: {en:'Treemap — GDP by Country & Region', fr:'Treemap — PIB par Pays & Région'},
  chart_map2: {en:'Map 2 — Secondary Comparison', fr:'Carte 2 — Comparaison secondaire'},
  chart_distrib_indicator: {en:'Indicator Distribution', fr:"Distribution de l'indicateur"},
  chart_gdp_growth: {en:'Total GDP & Growth', fr:'PIB Total & Croissance'},
  chart_infl_rate: {en:'Inflation & Policy Rate', fr:'Inflation & Taux Directeur'},
  chart_fdi_remit: {en:'FDI vs Remittances ($Bn)', fr:'FDI vs Envois de Fonds ($Mrd)'},
  chart_debt_unemp: {en:'Public Debt & Unemployment (%)', fr:'Dette Publique & Chômage (%)'},
  chart_growth_region: {en:'GDP Growth by Region', fr:'Croissance PIB par Région'},
  chart_banking_rate: {en:'Continental Banking Rate (%)', fr:'Bancarisation Continentale (%)'},
  chart_npl_car: {en:'NPL vs CAR (%) — Basel III Thresholds', fr:'NPL vs CAR (%) — Seuils Bâle III'},
  chart_roe_nim: {en:'ROE & NIM (%)', fr:'ROE & NIM (%)'},
  chart_credit_priv: {en:'Private Sector Credit (% GDP)', fr:'Crédit au Secteur Privé (% PIB)'},
  chart_banking_region: {en:'Banking Rate by Region', fr:'Bancarisation par Région'},
  chart_radar_bank: {en:'Radar — Regional Banking Profile', fr:'Radar — Profil Régional Bancaire'},
  chart_mm_accounts: {en:'M-Money Accounts & Transactions', fr:'Comptes M-Money & Transactions'},
  chart_fintech_startups: {en:'Fintech Startups & Investments', fr:'Startups Fintech & Investissements'},
  chart_mm_region: {en:'M-Money Penetration by Region', fr:'Pénétration M-Money par Région'},
  chart_smartphone: {en:'Smartphone vs Digital Payments (%)', fr:'Smartphone vs Paiements Numériques (%)'},
  chart_mkt_cap: {en:'Total Market Capitalization ($Bn)', fr:'Capitalisation Boursière Totale ($Mrd)'},
  chart_spread: {en:'Average Sovereign Spread (bps)', fr:'Spread Souverain Moyen (pb)'},
  chart_exchanges: {en:'African Exchanges — Capitalization 2024', fr:'Bourses Africaines — Capitalisation 2024'},
  chart_par_oss: {en:'PAR30 & OSS (Quality Indicators)', fr:'PAR30 & OSS (Indicateurs qualité)'},
  chart_clients_women: {en:'Clients & Women Percentage', fr:'Clients & Pourcentage Femmes'},
  chart_portf: {en:'Total Microcredit Portfolio ($M)', fr:'Portefeuille Total Microcrédit ($M)'},
  chart_inclusion_score: {en:'Financial Inclusion Score (0-10)', fr:'Score Inclusion Financière (0-10)'},
  chart_crises_year: {en:'Crises by Year', fr:'Crises par Année'},
  chart_crises_impact: {en:'GDP Impact vs Severity', fr:'Impact PIB vs Sévérité'},
  chart_heatmap: {en:'Heatmap — Pearson Correlations (54 countries aggregated)', fr:'Heatmap — Corrélations de Pearson (54 pays agrégés)'},
  chart_reg_gdp: {en:'GDP by Region (2024)', fr:'PIB par Région (2024)'},
  chart_reg_bank: {en:'Banking Indicators by Region', fr:'Indicateurs Bancaires par Région'},
  chart_reg_mm: {en:'Mobile Money by Region', fr:'Mobile Money par Région'},
  chart_reg_npl: {en:'NPL by Region (2000-2024)', fr:'NPL par Région (2000-2024)'},
  chart_desc_stats: {en:'Descriptive Statistics (cross-section 2024)', fr:'Statistiques Descriptives (coupe transversale 2024)'},
  chart_normality: {en:'Normality Tests (Shapiro-Wilk)', fr:'Tests de Normalité (Shapiro-Wilk)'},
  chart_distributions: {en:'Distributions & Box Plots', fr:'Distributions & Box Plots'},
  chart_regressions: {en:'Linear Regressions (OLS) — Scatter + Regression Line', fr:'Régressions Linéaires (OLS) — Scatter + Droite de Régression'},
  chart_reg_summary: {en:'Summary — All Regressions', fr:'Synthèse — Toutes les Régressions'},
  chart_panel_reg: {en:'Panel Regression (Pooled OLS) — GDP Growth ~ Macro Factors', fr:'Régression Panel (Pooled OLS) — Croissance PIB ~ Facteurs Macro'},
  chart_anova: {en:'ANOVA — Regional Differences', fr:'ANOVA — Différences Régionales'},
  chart_anova_results: {en:'ANOVA & Kruskal-Wallis Results', fr:'Résultats ANOVA & Kruskal-Wallis'},
  chart_spearman: {en:'Spearman Correlation Matrix (ρ) — Non-parametric', fr:'Matrice de Corrélation de Spearman (ρ) — Non-paramétrique'},
  chart_trends: {en:'Trend Analysis (Spearman over Time)', fr:'Analyse de Tendance (Spearman sur le Temps)'},
  chart_trends_summary: {en:'Trend Summary 2000-2024', fr:'Synthèse des Tendances 2000-2024'},
  chart_outliers: {en:'Outlier Detection (IQR method)', fr:"Détection d'Outliers (méthode IQR)"},
  // Labels
  lbl_indicator: {en:'Indicator', fr:'Indicateur'},
  lbl_year: {en:'Year', fr:'Année'},
  lbl_country: {en:'Country', fr:'Pays'},
  lbl_model: {en:'Model', fr:'Modèle'},
  // Select options
  opt_gdp_cap: {en:'GDP per capita ($)', fr:'PIB par habitant ($)'},
  opt_growth: {en:'GDP Growth (%)', fr:'Croissance PIB (%)'},
  opt_inflation: {en:'Inflation (%)', fr:'Inflation (%)'},
  opt_debt: {en:'Public Debt (% GDP)', fr:'Dette publique (% PIB)'},
  opt_banking: {en:'Banking Rate (%)', fr:'Bancarisation (%)'},
  opt_npl: {en:'NPL — Non-Performing Loans (%)', fr:'NPL — Créances douteuses (%)'},
  opt_car: {en:'CAR — Capital Adequacy (%)', fr:'CAR — Adéquation capital (%)'},
  opt_credit_gdp: {en:'Credit/GDP (%)', fr:'Crédit/PIB (%)'},
  opt_mm_pop: {en:'Mobile Money (% pop.)', fr:'Mobile Money (% pop.)'},
  opt_inclusion: {en:'Inclusion Score (0-10)', fr:'Score Inclusion (0-10)'},
  opt_fdi: {en:'FDI Inflows ($Bn)', fr:'FDI Entrants ($Mrd)'},
  opt_unemp: {en:'Unemployment (%)', fr:'Chômage (%)'},
  opt_par30: {en:'PAR30 Microfinance (%)', fr:'PAR30 Microfinance (%)'},
  opt_gdp: {en:'GDP ($Bn)', fr:'PIB ($Mrd)'},
  opt_npl_short: {en:'NPL (%)', fr:'NPL (%)'},
  opt_inflation_short: {en:'Inflation (%)', fr:'Inflation (%)'},
  opt_fdi_short: {en:'FDI Inflows ($Bn)', fr:'FDI Entrants ($Mrd)'},
  opt_mm: {en:'Mobile Money (% pop)', fr:'Mobile Money (% pop)'},
  opt_debt_short: {en:'Public Debt (% GDP)', fr:'Dette Publique (% PIB)'},
  opt_credit: {en:'Credit/GDP (%)', fr:'Crédit/PIB (%)'},
  // Buttons
  btn_export_country: {en:'⬇ Export Country Sheet (PNG)', fr:'⬇ Export Fiche Pays (PNG)'},
  // Footer
  footer_role: {en:'Data Analyst & WebGIS Expert Report', fr:'Rapport Data Analyst & WebGIS Expert'},
  footer_date: {en:'April 2026', fr:'Avril 2026'},
  footer_desc: {en:'54 countries · 2000-2024 · 12 dimensions · IMF, WB, AfDB, GSMA, UNCTAD, BIS, MIX Market', fr:'54 pays · 2000-2024 · 12 dimensions · FMI, BM, BAfD, GSMA, CNUCED, BIS, MIX Market'},
  // KPI labels
  kpi_pib_total: {en:'TOTAL AFRICAN GDP', fr:'PIB AFRICAIN TOTAL'},
  kpi_growth: {en:'AVG GDP GROWTH', fr:'CROISSANCE PIB MOY.'},
  kpi_inflation: {en:'AVG INFLATION', fr:'INFLATION MOYENNE'},
  kpi_banking: {en:'BANKING RATE', fr:'TAUX BANCARISATION'},
  kpi_npl: {en:'AVG NPL RATIO', fr:'NPL RATIO MOYEN'},
  kpi_car: {en:'AVG CAR (BASEL III)', fr:'CAR MOYEN (BÂLE III)'},
  kpi_roe: {en:'AVG ROE', fr:'ROE MOYEN'},
  kpi_nim: {en:'AVG NIM', fr:'NIM MOYEN'},
  kpi_mm_accounts: {en:'M-MONEY ACCOUNTS', fr:'COMPTES M-MONEY'},
  kpi_mm_transactions: {en:'M-MONEY TRANSACTIONS', fr:'TRANSACTIONS M-MONEY'},
  kpi_startups: {en:'FINTECH STARTUPS', fr:'STARTUPS FINTECH'},
  kpi_fdi: {en:'FDI INFLOWS', fr:'FDI ENTRANTS'},
  kpi_debt: {en:'AVG PUBLIC DEBT', fr:'DETTE PUBLIQUE MOY.'},
  kpi_credit: {en:'AVG CREDIT/GDP', fr:'CRÉDIT/PIB MOYEN'},
  kpi_inclusion: {en:'INCLUSION SCORE', fr:'SCORE INCLUSION'},
  kpi_coverage: {en:'COVERAGE', fr:'COUVERTURE'},
  kpi_sub_growth: {en:'Real annual rate', fr:'Taux réel annuel'},
  kpi_sub_inflation: {en:'Continental CPI', fr:'IPC continental'},
  kpi_sub_banking: {en:'Banked adults', fr:'Adultes bancarisés'},
  kpi_sub_npl: {en:'Non-performing loans', fr:'Créances douteuses'},
  kpi_sub_car: {en:'Capital adequacy', fr:'Adéquation capital'},
  kpi_sub_roe: {en:'Bank profitability', fr:'Rentabilité bancaire'},
  kpi_sub_nim: {en:'Interest margin', fr:'Marge interméd.'},
  kpi_sub_mm_accounts: {en:'Active accounts', fr:'Comptes actifs'},
  kpi_sub_mm_transactions: {en:'Annual volume', fr:'Volume annuel'},
  kpi_sub_startups: {en:'Active ecosystem', fr:'Écosystème actif'},
  kpi_sub_fdi: {en:'Investments', fr:'Investissements'},
  kpi_sub_debt: {en:'Continental ratio', fr:'Ratio continental'},
  kpi_sub_credit: {en:'Financial depth', fr:'Profondeur financière'},
  kpi_sub_inclusion: {en:'Financial inclusion', fr:'Inclusion financière'},
  kpi_sub_coverage_countries: {en:'countries', fr:'pays'},
  kpi_sub_coverage_years: {en:'years of data', fr:'années de données'},
};

function applyI18n(){
  document.querySelectorAll('[data-i18n]').forEach(el=>{
    const key=el.getAttribute('data-i18n');
    if(I18N[key]&&I18N[key][currentLang]) el.textContent=I18N[key][currentLang];
  });
  const btn=document.getElementById('btn-lang');
  if(currentLang==='en'){
    btn.innerHTML='<span class="flag">🇫🇷</span> FR';
  } else {
    btn.innerHTML='<span class="flag">🇬🇧</span> EN';
  }
}

function toggleLang(){
  currentLang = currentLang==='en' ? 'fr' : 'en';
  applyI18n();
  renderKPIs();
}

// ═══════════════════════════════════════════════════════════════════════════════
// INIT
// ═══════════════════════════════════════════════════════════════════════════════
applyI18n();
renderOverview();
rendered.overview=true;

// Header shrink on scroll
window.addEventListener('scroll',()=>{
  document.querySelector('.header').classList.toggle('scrolled',window.scrollY>20);
},{passive:true});
</script>
</body>
</html>"""

with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    content = html_template.replace('__DATA_PLACEHOLDER__', data_json)
    f.write(content)

file_size = OUTPUT_FILE.stat().st_size / (1024*1024)
print(f"\n🎉 Dashboard generated: {OUTPUT_FILE}")
print(f"📦 File size: {file_size:.1f} MB")
print(f"📊 Data: {len(country_list)} pays, {len(ts_continental)} années, {len(crises_list)} crises")
print(f"🔗 Open in browser: file:///{str(OUTPUT_FILE).replace(chr(92),'/')}")
