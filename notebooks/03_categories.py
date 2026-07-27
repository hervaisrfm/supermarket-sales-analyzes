# ============================================
# OBJECTIF 3 : CATÉGORIES ET SOUS-CATÉGORIES
# ============================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (14, 6)

print("=" * 60)
print("📦 OBJECTIF 3 : CATÉGORIES ET SOUS-CATÉGORIES")
print("=" * 60)

# Charger les données nettoyées
df = pd.read_csv('../data/supermarket_sales_cleaned.csv')

print(f"✅ Données chargées : {len(df)} lignes")
print(f"Colonnes : {df.columns.tolist()}")

# ============================================
# ANALYSE PAR CATÉGORIE
# ============================================
print("\n📂 ANALYSE PAR CATÉGORIE")
print("-" * 40)

cat_stats = df.groupby('Category').agg(
    CA=('Sales', 'sum'),
    Profit=('Profit', 'sum'),
    Commandes=('Order_ID', 'nunique'),
    Quantité=('Quantity', 'sum')
).sort_values('CA', ascending=False)

cat_stats['Marge_%'] = (cat_stats['Profit'] / cat_stats['CA']) * 100
cat_stats['Panier_Moyen'] = cat_stats['CA'] / cat_stats['Commandes']

print(cat_stats.to_string())

# ============================================
# GRAPHIQUE CATÉGORIES
# ============================================
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# CA par catégorie
cat_sorted_ca = cat_stats.sort_values('CA', ascending=True)
axes[0].barh(cat_sorted_ca.index, cat_sorted_ca['CA'], color=['#3498db', '#2ecc71', '#e74c3c'])
axes[0].set_title('Chiffre d\'Affaires par Catégorie', fontsize=14, fontweight='bold')
axes[0].set_xlabel('CA ($)')
for i, v in enumerate(cat_sorted_ca['CA']):
    axes[0].text(v + 10000, i, f'${v:,.0f}', va='center', fontweight='bold')

# Profit par catégorie
cat_sorted_profit = cat_stats.sort_values('Profit', ascending=True)
axes[1].barh(cat_sorted_profit.index, cat_sorted_profit['Profit'], color=['#3498db', '#2ecc71', '#e74c3c'])
axes[1].set_title('Profit par Catégorie', fontsize=14, fontweight='bold')
axes[1].set_xlabel('Profit ($)')
for i, v in enumerate(cat_sorted_profit['Profit']):
    axes[1].text(v + 5000, i, f'${v:,.0f}', va='center', fontweight='bold')

plt.tight_layout()
plt.savefig('../outputs/03_categories.png', dpi=150, bbox_inches='tight')
plt.show()

# ============================================
# ANALYSE PAR SOUS-CATÉGORIE
# ============================================
print("\n📁 TOP 10 SOUS-CATÉGORIES PAR CA")
print("-" * 40)

# ⚠️ Utiliser le nom exact : 'Sub-Category' (avec tiret)
subcat_stats = df.groupby('Sub-Category').agg(
    CA=('Sales', 'sum'),
    Profit=('Profit', 'sum'),
    Commandes=('Order_ID', 'nunique')
).sort_values('CA', ascending=False)

subcat_stats['Marge_%'] = (subcat_stats['Profit'] / subcat_stats['CA']) * 100
print(subcat_stats.head(10).to_string())

print("\n📁 TOP 10 SOUS-CATÉGORIES PAR PROFIT")
print("-" * 40)
top_profit_subcat = subcat_stats.sort_values('Profit', ascending=False).head(10)
print(top_profit_subcat.to_string())

# ============================================
# GRAPHIQUE SOUS-CATÉGORIES
# ============================================
fig, axes = plt.subplots(1, 2, figsize=(16, 8))

# Top 10 CA
top10_ca = subcat_stats.head(10).sort_values('CA', ascending=True)
axes[0].barh(top10_ca.index, top10_ca['CA'], color='#3498db', alpha=0.8)
axes[0].set_title('Top 10 Sous-Catégories - Chiffre d\'Affaires', fontsize=14, fontweight='bold')
axes[0].set_xlabel('CA ($)')

# Top 10 Profit
top10_profit = subcat_stats.sort_values('Profit', ascending=False).head(10).sort_values('Profit', ascending=True)
axes[1].barh(top10_profit.index, top10_profit['Profit'], color='#2ecc71', alpha=0.8)
axes[1].set_title('Top 10 Sous-Catégories - Profit', fontsize=14, fontweight='bold')
axes[1].set_xlabel('Profit ($)')

plt.tight_layout()
plt.savefig('../outputs/03_sous_categories.png', dpi=150, bbox_inches='tight')
plt.show()

# ============================================
# INSIGHT
# ============================================
best_cat_ca = cat_stats['CA'].idxmax()
best_cat_profit = cat_stats['Profit'].idxmax()

print(f"\n💡 INSIGHTS :")
print(f"   - Catégorie plus vendue : {best_cat_ca} (${cat_stats.loc[best_cat_ca, 'CA']:,.0f})")
print(f"   - Catégorie plus rentable : {best_cat_profit} (${cat_stats.loc[best_cat_profit, 'Profit']:,.0f})")
print(f"   - Marges par catégorie :")
for cat in cat_stats.index:
    print(f"     • {cat:20s} : {cat_stats.loc[cat, 'Marge_%']:.1f}%")

print("\n✅ Analyse des catégories terminée !")