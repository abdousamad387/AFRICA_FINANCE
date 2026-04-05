# AFRICA FINANCE OBSERVATORY

**Tableau de bord analytique interactif de la finance africaine (2000-2024)**

*Auteur : Abdou Samad Faye -- Fullstack Geo Data Scientist*

---

> [English version available here](README_EN.md)

---

## Table des matieres

1. [Introduction](#1-introduction)
2. [Contexte](#2-contexte)
3. [Justification](#3-justification)
4. [Objectifs](#4-objectifs)
5. [Donnees et sources](#5-donnees-et-sources)
6. [Methodologie](#6-methodologie)
7. [Architecture technique](#7-architecture-technique)
8. [Resultats](#8-resultats)
9. [Discussion](#9-discussion)
10. [Conclusion](#10-conclusion)
11. [Installation et utilisation](#11-installation-et-utilisation)
12. [Structure du projet](#12-structure-du-projet)

---

## 1. Introduction

Le projet **Africa Finance Observatory** est un systeme d'analyse et de visualisation complet, couvrant 54 pays africains sur la periode 2000-2024. Il rassemble plus de 15 000 observations structurees en 12 dimensions thematiques (macroeconomie, secteur bancaire, fintech, microfinance, marches financiers, crises, etc.) et produit un tableau de bord HTML interactif entierement autonome, accompagne d'un orchestrateur CLI bilingue (francais/anglais).

L'objectif est de fournir un outil de decision et de recherche qui combine rigueur statistique (tests parametriques et non parametriques, regressions, analyses panel) et visualisation de qualite professionnelle (plus de 35 graphiques interactifs, cartes choroplethes animees, treemaps, radars).

---

## 2. Contexte

Le continent africain reunit 54 economies aux trajectoires de developpement heterogenes. Malgre une croissance moyenne superieure a la moyenne mondiale depuis deux decennies, les systemes financiers africains restent fragmentes : taux de bancarisation inegaux (de moins de 10 % a plus de 80 % selon les pays), profondeur creditrice limitee, vulnerabilite aux chocs exterieurs et reliance croissante sur le mobile money comme vecteur d'inclusion financiere.

Les donnees existent -- dispersees entre les bases du FMI, de la Banque Mondiale, de la BAD, du GSMA, de la CNUCED, de la BRI et du MIX Market -- mais aucun outil public ne les synthetise dans un cadre analytique unifie, interactif et statistiquement rigoureux couvrant l'ensemble du continent sur un quart de siecle.

---

## 3. Justification

| Constat | Reponse du projet |
|---|---|
| Les donnees financieres africaines sont eparpillees dans des bases heterogenes | Base unifiee de 15 000+ observations, 12 dimensions, format Excel standardise |
| Les tableaux de bord existants sont statiques ou limites a un sous-ensemble de pays | Dashboard HTML interactif couvrant 54 pays, 25 annees, 13 onglets thematiques |
| Les analyses restent souvent descriptives | 10 methodes statistiques implementees (ANOVA, Kruskal-Wallis, Shapiro-Wilk, Spearman, regression panel OLS) |
| La barriere linguistique limite l'audience | Systeme i18n complet francais/anglais (130+ cles de traduction) |
| La reproductibilite est rarement assuree | Pipeline entierement scriptable, CLI avec 11 commandes, generation deterministe du dashboard |

---

## 4. Objectifs

**Objectif general** : Concevoir un observatoire numerique interactif de la finance africaine combinant collecte, traitement, analyse statistique avancee et visualisation des donnees financieres de 54 pays sur 25 ans.

**Objectifs specifiques** :

| # | Objectif |
|---|---|
| 1 | Consolider les donnees de 7 sources internationales en une base structuree de 12 dimensions |
| 2 | Calculer 18 indicateurs cles de performance (KPI) par annee et par region |
| 3 | Appliquer 10 methodes statistiques (descriptive, inferentielle, panel) sur les donnees financieres |
| 4 | Generer un tableau de bord HTML autonome avec plus de 35 graphiques interactifs |
| 5 | Produire 13 cartes choroplethes interactives avec curseur temporel 2000-2024 |
| 6 | Permettre l'analyse comparative par region (5 regions) et par pays (54 fiches) |
| 7 | Offrir un outil CLI bilingue pour l'automatisation du pipeline analytique |

---

## 5. Donnees et sources

### 5.1 Sources de donnees

| Source | Sigle | Donnees fournies |
|---|---|---|
| Fonds Monetaire International | FMI | PIB, inflation, dette publique, balance courante, reserves |
| Banque Mondiale | BM | Bancarisation, credit/PIB, IDH, chomage, urbanisation |
| Banque Africaine de Developpement | BAD | Indicateurs sectoriels regionaux, profils pays |
| GSMA | GSMA | Mobile money (comptes, transactions, penetration) |
| Conference des Nations Unies sur le Commerce et le Developpement | CNUCED | FDI entrants/sortants, envois de fonds |
| Banque des Reglements Internationaux | BRI | Spreads souverains, taux directeurs, obligations |
| MIX Market | MIX | Microfinance (clients, portefeuille, PAR30, OSS) |

### 5.2 Structure de la base de donnees

La base `AfricaFinance_Database_2000_2024.xlsx` comprend 11 feuilles :

| # | Feuille | Observations | Variables | Description |
|---|---|---|---|---|
| 1 | Macroeconomie | 1 274 | 25 | PIB, croissance, inflation, dette, chomage, FDI, IDH |
| 2 | Secteur Bancaire | 1 274 | 26 | Bancarisation, NPL, CAR, ROE, NIM, credit, assurance |
| 3 | Fintech et Mobile Money | 1 274 | 23 | Comptes MM, transactions, startups, investissements |
| 4 | Marches Financiers | 849 | 21 | Capitalisation, indices, spreads, obligations |
| 5 | Microfinance | 1 274 | 21 | IMF, portefeuille, PAR30, OSS, clients, inclusion |
| 6 | Trimestrielles | 5 099 | 18 | Donnees infra-annuelles (PIB, credit, reserves) |
| 7 | Profil Pays | 50 | 21 | Metadonnees (monnaie, banque centrale, coordonnees) |
| 8 | Correlations | -- | -- | Matrice de correlation pre-calculee |
| 9 | Crises | 173 | 14 | Evenements de crise (type, severite, impact PIB) |
| 10 | Classements | -- | -- | Rankings par indicateur |
| 11 | Statistiques | -- | 12 | Statistiques descriptives regionales |

### 5.3 Couverture geographique

54 pays africains, regroupes en 5 regions :

| Region | Pays (exemples) |
|---|---|
| Afrique Australe | Afrique du Sud, Botswana, Mozambique, Zambie, Zimbabwe |
| Afrique Centrale | Cameroun, RDC, Gabon, Congo, Tchad |
| Afrique du Nord | Maroc, Egypte, Tunisie, Algerie, Libye |
| Afrique Occidentale | Nigeria, Ghana, Senegal, Cote d'Ivoire, Mali |
| Afrique Orientale | Kenya, Ethiopie, Tanzanie, Ouganda, Rwanda |

---

## 6. Methodologie

### 6.1 Pipeline de traitement des donnees

| Etape | Operation | Detail |
|---|---|---|
| 1 | Chargement | Lecture des 11 feuilles Excel via `pandas.read_excel()` avec moteur `openpyxl` |
| 2 | Nettoyage | Suppression des sous-en-tetes, renommage des colonnes, conversion numerique (`pd.to_numeric(..., errors='coerce')`), suppression des lignes sans pays/annee |
| 3 | Agregation temporelle | Series continentales (4 DataFrames), series regionales (4 DataFrames), classements top/bottom 15 pour 10 indicateurs |
| 4 | Agregation transversale | 18 KPI pour l'annee 2024, profils regionaux (3 DataFrames) |
| 5 | Donnees par pays | Series temporelles individuelles (macro : 6 variables, banque : 6, fintech : 4) pour chaque pays |
| 6 | Donnees choroplethes | 25 annees x 54 pays x 13 indicateurs, codes ISO-3 |
| 7 | Donnees radar | 5 regions x 7 dimensions normalisees |
| 8 | Donnees treemap | 54 pays : PIB, croissance, region (hierarchie) |
| 9 | Statistiques avancees | 10 methodes (cf. section 6.2) |
| 10 | Serialisation | Payload JSON (732 Ko), injection dans template HTML |

### 6.2 Methodes statistiques

#### 6.2.1 Statistiques descriptives

14 variables analysees sur la coupe transversale 2024.

| Metrique | Formule |
|---|---|
| Moyenne | $\bar{x} = \frac{1}{n}\sum_{i=1}^{n} x_i$ |
| Mediane | Valeur centrale de la distribution ordonnee |
| Ecart-type | $s = \sqrt{\frac{1}{n-1}\sum_{i=1}^{n}(x_i - \bar{x})^2}$ |
| Coefficient de variation | $CV = \frac{s}{\bar{x}} \times 100$ |
| Asymetrie (Skewness) | $g_1 = \frac{n}{(n-1)(n-2)} \sum \left(\frac{x_i - \bar{x}}{s}\right)^3$ |
| Aplatissement (Kurtosis) | $g_2 = \frac{n(n+1)}{(n-1)(n-2)(n-3)} \sum \left(\frac{x_i - \bar{x}}{s}\right)^4 - \frac{3(n-1)^2}{(n-2)(n-3)}$ |
| Quartiles | $Q_1$ (25e percentile), $Q_3$ (75e percentile) |

**Variables analysees** : PIB_Mrd, Croissance_PIB, PIB_hab, Inflation, Dette_publique, Chomage, Bancarisation, NPL, CAR, ROE, Credit_PIB, Pop_MM, Score_inclusion, FDI_entrants.

#### 6.2.2 Regression lineaire simple (MCO)

Implementation via `scipy.stats.linregress()`.

$$\hat{y} = \beta_0 + \beta_1 x$$

$$R^2 = 1 - \frac{SS_{res}}{SS_{tot}} = 1 - \frac{\sum(y_i - \hat{y}_i)^2}{\sum(y_i - \bar{y})^2}$$

| # | Variable dependante | Variable independante | Hypothese testee |
|---|---|---|---|
| 1 | Bancarisation | PIB par habitant | Le revenu favorise l'acces bancaire |
| 2 | Credit/PIB | PIB par habitant | Le revenu stimule le credit |
| 3 | Score inclusion | Bancarisation | La bancarisation ameliore l'inclusion |
| 4 | Bancarisation | Mobile Money (% pop.) | Le mobile money complement la banque |
| 5 | Croissance | Inflation | L'inflation freine la croissance |
| 6 | Croissance | NPL | Les creances douteuses penalisent la croissance |
| 7 | Croissance | Dette publique | L'endettement affecte la croissance |
| 8 | Croissance | FDI entrants | Les IDE stimulent la croissance |
| 9 | Bancarisation | Urbanisation | L'urbanisation facilite l'acces bancaire |
| 10 | Bancarisation | IDH | Le developpement humain favorise la bancarisation |

Seuil de significativite : $p < 0.05$.

#### 6.2.3 ANOVA a un facteur

Test de comparaison des moyennes entre les 5 regions africaines.

$$F = \frac{MS_{entre}}{MS_{intra}} = \frac{\sum n_j(\bar{x}_j - \bar{x})^2 / (k-1)}{\sum\sum(x_{ij} - \bar{x}_j)^2 / (N-k)}$$

Implementation via `scipy.stats.f_oneway()`.

| Variable testee | Description |
|---|---|
| Croissance_PIB | Les taux de croissance different-ils entre regions ? |
| Bancarisation | Les niveaux de bancarisation different-ils entre regions ? |
| NPL | Les ratios de creances douteuses different-ils entre regions ? |
| Inflation | Les niveaux d'inflation different-ils entre regions ? |
| Credit_PIB | La profondeur creditrice differe-t-elle entre regions ? |
| Pop_MM | La penetration du mobile money differe-t-elle entre regions ? |
| Score_inclusion | L'inclusion financiere differe-t-elle entre regions ? |
| PIB_hab | Les niveaux de revenu par habitant different-ils entre regions ? |

#### 6.2.4 Test de Shapiro-Wilk

Test de normalite applique aux 14 variables de la coupe transversale.

$$W = \frac{\left(\sum a_i x_{(i)}\right)^2}{\sum (x_i - \bar{x})^2}$$

Implementation via `scipy.stats.shapiro()`. Hypothese nulle : la distribution suit une loi normale ($p > 0.05$).

#### 6.2.5 Test de Kruskal-Wallis

Alternative non parametrique a l'ANOVA, appliquee aux memes 8 variables.

$$H = \frac{12}{N(N+1)} \sum_{j=1}^{k} \frac{R_j^2}{n_j} - 3(N+1)$$

Implementation via `scipy.stats.kruskal()`.

#### 6.2.6 Correlation de Spearman

Matrice de correlation des rangs pour 9 variables.

$$\rho = 1 - \frac{6\sum d_i^2}{n(n^2-1)}$$

Implementation via `scipy.stats.spearmanr()`. Variables : PIB_hab, Bancarisation, NPL, Inflation, Credit_PIB, Pop_MM, Croissance_PIB, IDH, Score_inclusion.

#### 6.2.7 Analyse de tendance temporelle

Correlation de Spearman entre les annees et les valeurs moyennes continentales, pour 8 variables :

| Variable | Type de tendance attendue |
|---|---|
| PIB_Mrd | Hausse structurelle |
| Croissance_PIB | Fluctuante avec tendance |
| Inflation | Baisse tendancielle |
| Dette_publique | Hausse post-2010 |
| Bancarisation | Hausse progressive |
| NPL | Baisse attendue |
| Pop_MM | Forte hausse |
| Score_inclusion | Hausse progressive |

#### 6.2.8 Detection des valeurs aberrantes (methode IQR)

$$\text{Borne inf.} = Q_1 - 1.5 \times IQR \quad ; \quad \text{Borne sup.} = Q_3 + 1.5 \times IQR$$

$$IQR = Q_3 - Q_1$$

Appliquee sur les 14 variables descriptives. Chaque outlier est identifie avec le pays et la valeur correspondante.

#### 6.2.9 Regression panel (MCO poolee)

Variable dependante : Croissance du PIB.

Variables independantes (6 regresseurs) :

| Variable | Justification |
|---|---|
| Inflation | Effet potentiellement negatif sur la croissance |
| Dette_publique | Hypothese de surendettement |
| FDI_entrants | Effet catalyseur attendu |
| Chomage | Dysfonctionnement du marche du travail |
| Bancarisation | Inclusion financiere comme moteur |
| Credit_PIB | Profondeur financiere |

Estimation par moindres carres :

$$\hat{\beta} = (X^T X)^{-1} X^T y$$

Erreurs standard :

$$SE(\hat{\beta}_j) = \sqrt{MSE \cdot [(X^T X)^{-1}]_{jj}}$$

Statistique t :

$$t_j = \frac{\hat{\beta}_j}{SE(\hat{\beta}_j)}$$

p-values calculees via `scipy.stats.t.cdf()`.

$R^2$ et $R^2$ ajuste :

$$R^2_{adj} = 1 - \frac{(1-R^2)(n-1)}{n-k-1}$$

Implementation via `numpy.linalg.lstsq()`.

#### 6.2.10 Matrice de correlation de Pearson

Extraite de la feuille pre-calculee du fichier Excel. 11 variables.

$$r = \frac{\sum(x_i - \bar{x})(y_i - \bar{y})}{\sqrt{\sum(x_i - \bar{x})^2 \sum(y_i - \bar{y})^2}}$$

### 6.3 Outils et technologies

| Composant | Technologie | Version | Role |
|---|---|---|---|
| Langage principal | Python | 3.14 | Traitement, statistiques, generation |
| Manipulation de donnees | pandas | -- | Chargement, nettoyage, agregation |
| Calcul numerique | NumPy | -- | Algebre matricielle, panel OLS |
| Tests statistiques | SciPy (scipy.stats) | -- | Regressions, ANOVA, Shapiro-Wilk, Kruskal-Wallis, Spearman |
| Lecture Excel | openpyxl | -- | Moteur de lecture du fichier .xlsx |
| Export Excel | xlsxwriter | -- | Export des analyses en .xlsx multi-feuilles |
| Visualisation | Plotly.js | 2.35.0 | 35+ graphiques interactifs cote client |
| Typographie | Google Fonts | -- | Inter (UI), JetBrains Mono (monospace) |
| Mise en page | CSS3 | -- | Glassmorphism, CSS Grid, animations, responsive |
| Theme | Dark mode | -- | 30+ variables CSS personnalisees |
| Internationalisation | JavaScript (client) | -- | 130+ cles, basculement FR/EN |
| Serveur local | http.server (Python) | -- | Port 8888, lancement automatique du navigateur |

---

## 7. Architecture technique

### 7.1 Structure du projet

| Fichier | Lignes | Taille | Description |
|---|---|---|---|
| `build_dashboard.py` | ~2 830 | ~130 Ko | ETL + statistiques + generation HTML |
| `main.py` | ~830 | ~38 Ko | Orchestrateur CLI bilingue |
| `AfricaFinance_Dashboard.html` | -- | ~0.8 Mo | Dashboard genere (autonome, donnees JSON integrees) |
| `AfricaFinance_Database_2000_2024.xlsx` | -- | ~1.2 Mo | Base de donnees source |
| `.gitignore` | 4 | -- | Exclusions (.venv, __pycache__, fichiers temporaires) |

### 7.2 Pipeline de generation

```
Excel (.xlsx)
    |
    v
[build_dashboard.py]
    |-- 1. Lecture des 11 feuilles
    |-- 2. Nettoyage et typage
    |-- 3. Calcul des agregats (KPI, series temporelles, classements)
    |-- 4. Construction des donnees cartographiques (choroplethes, treemap, radar)
    |-- 5. Calcul des statistiques avancees (10 methodes)
    |-- 6. Serialisation JSON (732 Ko)
    |-- 7. Injection dans le template HTML
    v
Dashboard HTML autonome (0.8 Mo)
    |-- CSS : theme sombre, glassmorphism, 5 breakpoints responsive
    |-- JS : Plotly.js 2.35.0, i18n FR/EN, 13 renderers
    |-- Donnees : JSON integre (aucune requete externe)
```

### 7.3 Onglets du tableau de bord

| # | Onglet | Contenu | Nb graphiques |
|---|---|---|---|
| 1 | Vue d'ensemble | KPI, scatter PIB/bancarisation, treemap PIB, histogramme | 4 |
| 2 | Cartes choroplethes | 2 cartes + curseur annee + histogramme de distribution | 3 |
| 3 | Macroeconomie | PIB total, croissance/inflation, FDI/remittances, dette/chomage, croissance regionale | 5 |
| 4 | Secteur bancaire | Bancarisation, NPL/CAR, ROE/NIM, credit/PIB, evolution regionale, radar 5 regions | 6 |
| 5 | Fintech et Mobile Money | Comptes/transactions, startups/investissements, evolution regionale, smartphone/paiements num. | 4 |
| 6 | Marches financiers | Capitalisation, spreads souverains, classement bourses | 3 |
| 7 | Microfinance | PAR30/OSS, clients/femmes, portefeuille, score inclusion | 4 |
| 8 | Crises | Chronologie, impact (scatter), tableau detaille | 3 |
| 9 | Classements | Top 15 / Bottom 15 pour 10 indicateurs (selecteur) | 2 |
| 10 | Correlations | Matrice de correlation de Pearson (heatmap) | 1 |
| 11 | Detail pays | 4 graphiques par pays (selecteur : 54 pays) | 4 |
| 12 | Regions comparees | PIB regional, indicateurs bancaires, fintech, NPL temporel | 4 |
| 13 | Statistiques avancees | Descriptives, normalite, distributions, regressions, panel OLS, ANOVA, Spearman, tendances, outliers | 9+ |

### 7.4 KPI calcules (annee 2024)

| # | KPI | Unite |
|---|---|---|
| 1 | PIB total africain | Milliards USD |
| 2 | Croissance moyenne du PIB | % |
| 3 | Inflation moyenne | % |
| 4 | Taux de bancarisation moyen | % |
| 5 | Ratio NPL moyen | % |
| 6 | Ratio CAR moyen (Bale III) | % |
| 7 | ROE moyen | % |
| 8 | NIM moyen | % |
| 9 | Comptes Mobile Money (total) | Millions |
| 10 | Nombre de startups fintech | Unites |
| 11 | FDI total entrant | Milliards USD |
| 12 | Dette publique moyenne | % PIB |
| 13 | Nombre de pays couverts | -- |
| 14 | Nombre d'annees | -- |
| 15 | Credit/PIB moyen | % |
| 16 | Score d'inclusion moyen | 0-10 |
| 17 | Transactions Mobile Money (total) | Milliards USD |
| 18 | Population avec Mobile Money | % |

### 7.5 Indicateurs cartographiques (choroplethes)

| # | Indicateur | Echelle de couleurs | Plage |
|---|---|---|---|
| 1 | PIB par habitant ($) | Vert progressif | 0 -- 8 000 |
| 2 | Croissance PIB (%) | Rouge-jaune-vert | -5 -- 12 |
| 3 | Inflation (%) | Vert-jaune-rouge | 0 -- 30 |
| 4 | Dette/PIB (%) | Vert-jaune-rouge | 0 -- 120 |
| 5 | Bancarisation (%) | Violet progressif | 0 -- 100 |
| 6 | NPL (%) | Vert-jaune-rouge | 0 -- 25 |
| 7 | CAR (%) | Rouge-jaune-vert | 5 -- 25 |
| 8 | Credit/PIB (%) | Bleu progressif | 0 -- 100 |
| 9 | Mobile Money (% pop.) | Violet progressif | 0 -- 90 |
| 10 | Score inclusion (0-10) | Vert progressif | 0 -- 10 |
| 11 | FDI ($Mrd) | Bleu progressif | 0 -- 15 |
| 12 | Chomage (%) | Vert-jaune-rouge | 0 -- 35 |
| 13 | PAR30 (%) | Vert-jaune-rouge | 0 -- 20 |

---

## 8. Resultats

### 8.1 Couverture et completude

| Metrique | Valeur |
|---|---|
| Pays couverts | 54 |
| Periode | 2000-2024 (25 ans) |
| Observations totales | 15 000+ |
| Dimensions thematiques | 12 |
| Variables analysees | 170+ |
| Graphiques interactifs generes | 35+ |
| Cartes choroplethes | 13 indicateurs x 25 annees |
| Tests statistiques effectues | 10 methodes, 50+ tests individuels |

### 8.2 Indicateurs synthetiques (typiques, annee 2024)

| Indicateur | Valeur typique | Observation |
|---|---|---|
| PIB total africain | ~3 000 Mrd USD | Croissance soutenue depuis 2000 |
| Bancarisation moyenne | ~35-45 % | Forte heterogeneite regionale |
| Penetration Mobile Money | ~30-40 % | Croissance exponentielle post-2010 |
| NPL moyen | ~8-12 % | Superieur aux standards internationaux (5 %) |
| CAR moyen | ~15-18 % | Conforme au minimum Bale III (10.5 %) |
| Score d'inclusion moyen | ~4-5 / 10 | Progres mais reste insuffisant |

### 8.3 Regressions significatives (exemples typiques)

| Modele | R2 attendu | Significativite | Interpretation |
|---|---|---|---|
| PIB/hab -> Bancarisation | Eleve | p < 0.05 | Le revenu est un determinant majeur de la bancarisation |
| Mobile Money -> Bancarisation | Moyen | p < 0.05 | Complementarite mobile money / banque |
| IDH -> Bancarisation | Eleve | p < 0.05 | Le developpement humain favorise l'acces financier |
| Dette -> Croissance | Faible a moyen | Variable | Relation non lineaire, effet seuil possible |

### 8.4 Comparaisons regionales (ANOVA)

Les tests ANOVA et Kruskal-Wallis revelent des differences significatives entre les 5 regions africaines pour la majorite des indicateurs financiers, confirmant l'heterogeneite structurelle du continent.

---

## 9. Discussion

### 9.1 Apports du projet

| Apport | Detail |
|---|---|
| Unicite | Premier observatoire interactif couvrant 54 pays, 25 ans, 12 dimensions en un seul fichier HTML |
| Rigueur statistique | 10 methodes complementaires (parametriques et non parametriques) |
| Reproductibilite | Pipeline entierement automatise via CLI |
| Accessibilite | Interface bilingue, responsive, exportable (PNG, SVG, CSV, JSON) |
| Autonomie | Aucune dependance serveur : le dashboard est un fichier HTML de 0.8 Mo |

### 9.2 Limites

| Limite | Explication |
|---|---|
| Donnees manquantes | Certains pays/annees presentent des lacunes dans les sources originales |
| Regression panel simplifiee | MCO poolee sans effets fixes ni effets aleatoires |
| Pas de tests post-hoc | L'ANOVA ne precise pas quelles paires de regions different |
| Causalite | Les regressions mesurent des associations, non des relations causales |
| Actualisation | Les donnees necessitent une mise a jour manuelle annuelle |

### 9.3 Perspectives

| Perspective | Description |
|---|---|
| Effets fixes panel | Integration de modeles a effets fixes et aleatoires (Hausman) |
| Tests post-hoc | Ajout de tests de Tukey HSD apres ANOVA significative |
| Machine Learning | Clustering (K-Means), prediction de la bancarisation |
| Donnees temps reel | Connexion a des API (FMI, Banque Mondiale) pour actualisation automatique |
| Publication web | Deploiement sur GitHub Pages ou serveur cloud |

---

## 10. Conclusion

Le projet **Africa Finance Observatory** demontre qu'il est possible de synthetiser un quart de siecle de donnees financieres africaines en un outil analytique unique, rigoureux et accessible. En combinant 12 dimensions thematiques, 10 methodes statistiques et plus de 35 visualisations interactives dans un fichier HTML autonome de 0.8 Mo, cet observatoire offre aux chercheurs, decideurs et praticiens un instrument de comprehension de la finance africaine sans precedent dans sa couverture et son interactivite.

L'architecture choisie -- un pipeline Python generant un dashboard statique avec donnees embarquees -- garantit la reproductibilite, la portabilite et l'independance vis-a-vis de toute infrastructure serveur.

---

## 11. Installation et utilisation

### 11.1 Pre-requis

| Composant | Version minimale |
|---|---|
| Python | 3.9+ |
| pip | 20+ |

### 11.2 Installation des dependances

```bash
pip install pandas openpyxl numpy scipy xlsxwriter
```

### 11.3 Commandes CLI

```bash
# Generer le dashboard
python main.py --build

# Generer et lancer le serveur local
python main.py --serve

# Afficher les statistiques en console
python main.py --stats

# Exporter en CSV
python main.py --export-csv

# Exporter en Excel
python main.py --export-excel

# Pipeline complet
python main.py --all

# Verifier les dependances
python main.py --check

# Installer les packages manquants
python main.py --install

# Choisir la langue (en/fr)
python main.py --lang fr --build

# Menu interactif
python main.py
```

### 11.4 Generation directe du dashboard

```bash
python build_dashboard.py
```

Le fichier `AfricaFinance_Dashboard.html` est genere dans le repertoire courant. Ouvrir dans un navigateur moderne (Chrome, Firefox, Edge).

---

## 12. Structure du projet

```
AFRICA_FINANCE/
|-- build_dashboard.py          # ETL + statistiques + generation HTML (~2 830 lignes)
|-- main.py                     # Orchestrateur CLI bilingue (~830 lignes)
|-- AfricaFinance_Dashboard.html        # Dashboard genere (autonome, ~0.8 Mo)
|-- AfricaFinance_Database_2000_2024.xlsx   # Base de donnees source (~1.2 Mo)
|-- AfricaFinance_Senior_Report.docx    # Rapport detaille (Word)
|-- AfricaFinance_Senior_Report.pdf     # Rapport detaille (PDF)
|-- README.md                   # Documentation (francais)
|-- README_EN.md                # Documentation (anglais)
|-- .gitignore                  # Exclusions Git
```

---

*Abdou Samad Faye -- Fullstack Geo Data Scientist*
