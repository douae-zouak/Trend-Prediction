# Time Series Forecasting – Sales Prediction Platform

### 🔮 Prévision des ventes avec ARIMA, SARIMA, TBATS et Prophet + Interface Streamlit

Ce projet consiste à développer une **plateforme complète de prévision des ventes** à partir de données transactionnelles d'une entreprise. Après une analyse exploratoire approfondie, plusieurs modèles de séries temporelles ont été testés (AR, MA, ARMA, ARIMA, SARIMA, TBATS, Prophet). Le modèle *Prophet* a finalement été retenu pour sa capacité à gérer les fortes tendances, les multi-saisonnalités et les jours spéciaux.

L'application finale permet à l'utilisateur de **prédire les ventes futures via une interface Streamlit**.

---

##  1. Dataset

Le dataset provenant du service commercial contient les colonnes suivantes :

* `Customer ID`
* `Customer Status`
* `Date Order was placed`
* `Delivery Date`
* `Order ID`
* `Product ID`
* `Quantity Ordered`
* `Total Retail Price for This Order`
* `Cost Price Per Unit`

Un second dataset lié aux produits a également été intégré :

* `Product ID`
* `Product Line`
* `Product Category`
* `Product Group`
* `Product Name`
* `Supplier Country`
* `Supplier Name`
* `Supplier ID`

Les deux datasets ont été **fusionnés** pour permettre une analyse complète des ventes par produit, catégorie, groupe et fournisseur.

---

##  2. Data Cleaning & Preprocessing

Les principales étapes du nettoyage :

* Normalisation des catégories (`GOLD → Gold`, `PLATINUM → Platinum`, `SILVER → Silver`)
* Suppression des valeurs manquantes ou incohérentes
* Conversion des dates en format datetime
* Création de la série temporelle des ventes journalières
* Agrégation : `daily_sales = sum(Quantity Ordered)`
* Fusion orders + products pour enrichir l'analyse
* Gestion des outliers quand nécessaire

---

## 🔎 3. Exploratory Data Analysis

Les analyses exploratoires ont mis en évidence :

* Une **tendance haussière** claire des ventes
* Une **forte saisonnalité multiple** : hebdomadaire, mensuelle et annuelle
* Des variations notables sur certains événements :
  * Black Friday
  * Rentrée scolaire
* Analyse par statut client (Silver, Gold, Platinum)
* Analyse des produits les plus vendus, des catégories dominantes, et des fournisseurs clés

Des visualisations ont été produites :

* Courbe des ventes journalières
* Histogrammes par product category / customer status
* Heatmap saisonnière
* ACF / PACF

---

##  4. Feature Engineering

Pour améliorer les modèles, plusieurs features ont été ajoutées :

### 4.1. Features temporelles

* `day` : jour du mois
* `month` : mois
* `year` : année
* `day_of_week` : jour de la semaine
* `is_weekend` : indicateur de week-end

*Utilité : capturer les patterns récurrents dans les cycles de vente.*

### 4.2. Features de retard (Lags)

* `lag_1`, `lag_7`, `lag_30`

*Ces variables représentent les ventes passées ; elles améliorent les modèles AR/ARMA.*

### 4.3. Jours spéciaux

* Black Friday
* Rentrée scolaire

*Aident Prophet et TBATS à expliquer les pics anormaux.*

---

##  5. Modélisation

Plusieurs modèles ont été testés de manière rigoureuse :

### 5.1. ARMA / ARIMA

* Analyse ACF & PACF
* Différenciation (d) testée avec plusieurs ordres
* Limite constatée : **ACF et PACF ne décroissent pas**, signe de forte saisonnalité → modèle inefficace.

### 5.2. SARIMA

* Test de SARIMA(p,d,q)(P,D,Q)s
* Problème : présence de **multi-saisonnalités** → SARIMA ne gère qu'UNE seule saisonnalité → performances faibles.

### 5.3. TBATS

* Modèle capable de capturer plusieurs périodes saisonnières
* Performances correctes mais instables sur les longues prédictions
* Sensible aux outliers

### 5.4. Prophet (Best Model)

* Gestion de :
  * tendance non linéaire
  * multi-saisonnalités
  * jours fériés & événements
* Ajout de jours spéciaux → nette amélioration du RMSE et du MAPE

**Prophet a été retenu comme modèle final.**

---

## 6. Comparaison des Performances

| Modèle      | MAPE       | RMSE       | Observations                                             |
| ----------- | ---------- | ---------- | -------------------------------------------------------- |
| SARIMA      | 84.23%     | 8384.0106   | Ne gère qu'une seule saisonnalité                        |
| TBATS       | 24.28%         | 7127.64      | Gère bien la multi-saisonnalité mais manque de stabilité |
| **Prophet** | 24.0% | faible     | 6706.68                        |

---

## 7. Interface Utilisateur (Streamlit)

Une application Streamlit a été développée pour :

* Charger le modèle Prophet entraîné (pickle)
* Générer des prévisions sur n jours
* Visualiser la tendance, saisonnalité et les intervalles de confiance
* Exporter les résultats

Fonctionnalités de l'interface :

* Sélection de la plage de dates futures
* Affichage des prédictions
* Graphiques interactifs (Plotly / Matplotlib)
* Décomposition de la série (`trend`, `yearly`, `weekly`)

---

## 8. Installation

### 1. Cloner le projet
git clone [https://github.com/your-username/sales-forecasting](https://github.com/douae-zouak/Trend-Prediction)

### 2. Installer les dépendances
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000

cd frontend
pip install -r requirements.txt
streamlit run app.py




