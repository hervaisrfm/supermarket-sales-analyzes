# ============================================
# OBJECTIF 4 : TOP 10 PRODUITS
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
print("🏆 OBJECTIF 4 : TOP 10 PRODUITS")
print("=" * 60)

# Charger les données nettoyées
df = pd.read_csv('../data/supermarket_sales_cleaned.csv')

# ============================================
# AGRÉGATION PAR PRODUIT
# ============================================
print("\n📦 AGRÉGATION PAR PRODUIT")
print("-" * 40)

product_stats = df.groupby('Product_Name').agg(
    CA=('Sales', 'sum'),
    Profit=('Profit', 'sum'),
    Quantité=('Quantity', 'sum'),
    Commandes=('Order_ID', 'nunique'),
    Remise_Moy=('Discount', 'mean')
).reset_index()

product_stats['Marge_%'] = (product_stats['Profit'] / product_stats['CA']) * 100
product_stats['Prix_Moyen'] = product_stats['CA'] / product_stats['Quantité']

print(f"Nombre total de produits : {len(product_stats)}")
print(f"CA moyen par produit : ${product_stats['CA'].mean():,.2f}")
print(f"Profit moyen par produit : ${product_stats['Profit'].mean():,.2f}")

# ============================================
# TOP 10 PAR CHIFFRE D'AFFAIRES
# ============================================
print("\n🏆 TOP 10 PRODUITS LES PLUS VENDUS (CA)")
print("-" * 40)

top10_sales = product_stats.nlargest(10, 'CA')[['Product_Name', 'CA', 'Profit', 'Quantité', 'Marge_%']]
print(top10_sales.to_string(index=False))

# ============================================
# TOP 10 PAR PROFIT
# ============================================
print("\n💰 TOP 10 PRODUITS LES PLUS RENTABLES (PROFIT)")
print("-" * 40)

top10_profit = product_stats.nlargest(10, 'Profit')[['Product_Name', 'CA', 'Profit', 'Quantité', 'Marge_%']]
print(top10_profit.to_string(index=False))

# ============================================
# TOP 10 PRODUITS DÉFICITAIRES
# ============================================
print("\n📉 TOP 10 PRODUITS LES MOINS RENTABLES (PERTE)")
print("-" * 40)

bottom10_profit = product_stats.nsmallest(10, 'Profit')[['Product_Name', 'CA', 'Profit', 'Quantité', 'Marge_%']]
print(bottom10_profit.to_string(index=False))

# ============================================
# PRODUITS PRÉSENTS DANS LES 2 TOPS
# ============================================
top10_sales_names = set(top10_sales['Product_Name'])
top10_profit_names = set(top10_profit['Product_Name'])
stars = top10_sales_names.intersection(top10_profit_names)

print(f"\n⭐ Produits STARS (dans le top 10 CA ET top 10 Profit) : {len(stars)}")
for p in stars:
    print(f"   • {p}")

# ============================================
# GRAPHIQUES
# ============================================
fig, axes = plt.subplots(1, 3, figsize=(18, 8))

# Top 10 CA
top10_sales_plot = top10_sales.sort_values('CA', ascending=True)
axes[0].barh(top10_sales_plot['Product_Name'], top10_sales_plot['CA'], color='#3498db', alpha=0.8)
axes[0].set_title('Top 10 Produits - Chiffre d\'Affaires', fontsize=14, fontweight='bold')
axes[0].set_xlabel('CA ($)')

# Top 10 Profit
top10_profit_plot = top10_profit.sort_values('Profit', ascending=True)
axes[1].barh(top10_profit_plot['Product_Name'], top10_profit_plot['Profit'], color='#2ecc71', alpha=0.8)
axes[1].set_title('Top 10 Produits - Profit', fontsize=14, fontweight='bold')
axes[1].set_xlabel('Profit ($)')

# Bottom 10
bottom10_plot = bottom10_profit.sort_values('Profit', ascending=False)
axes[2].barh(bottom10_plot['Product_Name'], bottom10_plot['Profit'], color='#e74c3c', alpha=0.8)
axes[2].set_title('Top 10 Produits - Moins Rentables', fontsize=14, fontweight='bold')
axes[2].set_xlabel('Profit ($)')
axes[2].axvline(x=0, color='black', linestyle='-', linewidth=1)

plt.tight_layout()
plt.savefig('../outputs/04_top_produits.png', dpi=150, bbox_inches='tight')
plt.show()

# ============================================
# SCATTER : CA vs PROFIT PAR PRODUIT
# ============================================
plt.figure(figsize=(12, 8))
plt.scatter(product_stats['CA'], product_stats['Profit'], alpha=0.5, c=product_stats['Marge_%'], cmap='RdYlGn')
plt.colorbar(label='Marge %')
plt.axhline(y=0, color='red', linestyle='--', alpha=0.5)
plt.xlabel('Chiffre d\'Affaires ($)')
plt.ylabel('Profit ($)')
plt.title('Positionnement des Produits : CA vs Profit', fontsize=14, fontweight='bold')

# Annoter les produits stars
for name in stars:
    produit = product_stats[product_stats['Product_Name'] == name].iloc[0]
    plt.annotate(name[:30]+'...', (produit['CA'], produit['Profit']),
                 fontsize=8, alpha=0.8)

plt.tight_layout()
plt.savefig('../outputs/04_scatter_produits.png', dpi=150, bbox_inches='tight')
plt.show()

# ============================================
# INSIGHT
# ============================================
print("\n💡 INSIGHTS :")
print(f"   - {len(stars)} produits sont à la fois dans le top CA et le top Profit")
print(f"   - Le produit le plus vendu génère ${top10_sales['CA'].iloc[0]:,.0f}")
print(f"   - Le produit le plus rentable génère ${top10_profit['Profit'].iloc[0]:,.0f}")
print(f"   - Le produit le plus déficitaire perd ${bottom10_profit['Profit'].iloc[0]:,.0f}")
print(f"   - {len(bottom10_profit[bottom10_profit['Profit'] < 0])} des 10 pires produits sont déficitaires")

print("\n✅ Analyse des produits terminée !")