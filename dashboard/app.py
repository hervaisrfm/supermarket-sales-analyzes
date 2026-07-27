# ============================================
# DASHBOARD FINAL - ANALYSE DES VENTES SUPERMARCHÉ
# ============================================
# Lancer : streamlit run dashboard/app.py
# ============================================

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# Configuration de la page
st.set_page_config(
    page_title="Dashboard - Ventes Supermarché",
    page_icon="🛒",
    layout="wide"
)

# Titre
st.title("🛒 Analyse des Ventes - Supermarché")
st.markdown("---")

# Charger les données
@st.cache_data
def load_data():
    df = pd.read_csv('../data/supermarket_sales_cleaned.csv')
    df['Order_Date'] = pd.to_datetime(df['Order_Date'])
    return df

df = load_data()

# ============================================
# FILTRES (SIDEBAR)
# ============================================
st.sidebar.header("🎯 Filtres")

# Filtre Année
years = df['Order_Year'].dropna().unique()
selected_year = st.sidebar.selectbox("Année", sorted(years), index=len(years)-1)

# Filtre Région
regions = df['Region'].unique()
selected_regions = st.sidebar.multiselect("Région", regions, default=regions)

# Filtre Catégorie
categories = df['Category'].unique()
selected_categories = st.sidebar.multiselect("Catégorie", categories, default=categories)

# Appliquer les filtres
filtered_df = df[
    (df['Order_Year'] == selected_year) &
    (df['Region'].isin(selected_regions)) &
    (df['Category'].isin(selected_categories))
]

# ============================================
# KPI (LIGNE 1)
# ============================================
st.subheader("📊 Indicateurs Clés de Performance")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    ca = filtered_df['Sales'].sum()
    st.metric("💰 Chiffre d'Affaires", f"${ca:,.0f}")

with col2:
    profit = filtered_df['Profit'].sum()
    st.metric("📈 Profit", f"${profit:,.0f}", delta_color="normal")

with col3:
    commandes = filtered_df['Order_ID'].nunique()
    st.metric("🛒 Commandes", f"{commandes:,}")

with col4:
    clients = filtered_df['Customer_ID'].nunique()
    st.metric("👥 Clients", f"{clients:,}")

with col5:
    panier = ca / commandes if commandes > 0 else 0
    st.metric("🧺 Panier Moyen", f"${panier:,.0f}")

st.markdown("---")

# ============================================
# GRAPHIQUES (LIGNE 2)
# ============================================
col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 CA par Catégorie")
    cat_ca = filtered_df.groupby('Category')['Sales'].sum().sort_values(ascending=True)
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(cat_ca.index, cat_ca.values, color=['#3498db', '#2ecc71', '#e74c3c'])
    for i, v in enumerate(cat_ca.values):
        ax.text(v + 5000, i, f'${v:,.0f}', va='center')
    st.pyplot(fig)

with col2:
    st.subheader("🌍 CA par Région")
    region_ca = filtered_df.groupby('Region')['Sales'].sum().sort_values(ascending=True)
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(region_ca.index, region_ca.values, color=['#e74c3c', '#3498db', '#2ecc71', '#f39c12'])
    for i, v in enumerate(region_ca.values):
        ax.text(v + 5000, i, f'${v:,.0f}', va='center')
    st.pyplot(fig)

st.markdown("---")

# ============================================
# GRAPHIQUES (LIGNE 3)
# ============================================
col1, col2 = st.columns(2)

with col1:
    st.subheader("💸 Impact des Remises sur le Profit")
    fig, ax = plt.subplots(figsize=(8, 5))
    scatter = ax.scatter(filtered_df['Discount'], filtered_df['Profit'], 
                         alpha=0.5, c=filtered_df['Profit'], cmap='RdYlGn')
    ax.axhline(y=0, color='red', linestyle='--', alpha=0.5)
    ax.set_xlabel('Taux de Remise')
    ax.set_ylabel('Profit ($)')
    st.pyplot(fig)

with col2:
    st.subheader("👥 CA par Segment Client")
    segment_ca = filtered_df.groupby('Segment')['Sales'].sum()
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.pie(segment_ca.values, labels=segment_ca.index, autopct='%1.1f%%',
           colors=['#3498db', '#2ecc71', '#f39c12'], startangle=90)
    st.pyplot(fig)

st.markdown("---")

# ============================================
# TOP 10 PRODUITS
# ============================================
st.subheader("🏆 Top 10 Produits les Plus Vendus")

top10 = filtered_df.groupby('Product_Name')['Sales'].sum().sort_values(ascending=False).head(10)
fig, ax = plt.subplots(figsize=(12, 6))
ax.barh(top10.index[::-1], top10.values[::-1], color='#3498db', alpha=0.8)
ax.set_xlabel('CA ($)')
st.pyplot(fig)

# ============================================
# TABLEAU DES DONNÉES
# ============================================
st.markdown("---")
st.subheader("📋 Données Brutes (filtrées)")

if st.checkbox("Afficher les données"):
    st.dataframe(filtered_df.head(100))

# Pied de page
st.markdown("---")
st.caption("📊 Projet Data Science - Analyse des Ventes Supermarché | 2024")