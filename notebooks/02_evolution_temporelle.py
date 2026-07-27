# ============================================
# OBJECTIF 2 : ÉVOLUTION DES VENTES PAR MOIS
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
print("📈 OBJECTIF 2 : ÉVOLUTION DES VENTES DANS LE TEMPS")
print("=" * 60)

# Charger les données nettoyées
df = pd.read_csv('../data/supermarket_sales_cleaned.csv')

# ============================================
# AGRÉGATION PAR MOIS
# ============================================
print("\n📅 AGRÉGATION MENSUELLE")
print("-" * 40)

monthly = df.groupby('Order_YearMonth').agg(
    CA=('Sales', 'sum'),
    Profit=('Profit', 'sum'),
    Commandes=('Order_ID', 'nunique'),
    Quantité=('Quantity', 'sum')
).reset_index()

print(monthly.to_string(index=False))

# ============================================
# MEILLEUR ET PIRE MOIS
# ============================================
best_sales = monthly.loc[monthly['CA'].idxmax()]
best_profit = monthly.loc[monthly['Profit'].idxmax()]
worst_sales = monthly.loc[monthly['CA'].idxmin()]

print(f"\n🏆 Meilleur mois (CA)    : {best_sales['Order_YearMonth']} - ${best_sales['CA']:,.0f}")
print(f"🏆 Meilleur mois (Profit) : {best_profit['Order_YearMonth']} - ${best_profit['Profit']:,.0f}")
print(f"📉 Pire mois (CA)         : {worst_sales['Order_YearMonth']} - ${worst_sales['CA']:,.0f}")

# ============================================
# GRAPHIQUE : CA ET PROFIT PAR MOIS
# ============================================
fig, axes = plt.subplots(3, 1, figsize=(14, 14))

# CA mensuel
axes[0].plot(monthly['Order_YearMonth'], monthly['CA'], marker='o', linewidth=2, color='#3498db', markersize=8)
axes[0].fill_between(range(len(monthly)), monthly['CA'], alpha=0.3, color='#3498db')
axes[0].set_title('Évolution du Chiffre d\'Affaires Mensuel', fontsize=14, fontweight='bold')
axes[0].set_ylabel('Chiffre d\'Affaires ($)')
axes[0].tick_params(axis='x', rotation=45)
# Ajouter les valeurs sur les points
for i, (x, y) in enumerate(zip(monthly['Order_YearMonth'], monthly['CA'])):
    axes[0].annotate(f'${y:,.0f}', (x, y), textcoords="offset points", xytext=(0,10), ha='center', fontsize=8)

# Profit mensuel
axes[1].plot(monthly['Order_YearMonth'], monthly['Profit'], marker='s', linewidth=2, color='#2ecc71', markersize=8)
axes[1].fill_between(range(len(monthly)), monthly['Profit'], alpha=0.3, color='#2ecc71')
axes[1].set_title('Évolution du Profit Mensuel', fontsize=14, fontweight='bold')
axes[1].set_ylabel('Profit ($)')
axes[1].tick_params(axis='x', rotation=45)
axes[1].axhline(y=0, color='red', linestyle='--', alpha=0.5)

# Nombre de commandes
axes[2].bar(monthly['Order_YearMonth'], monthly['Commandes'], color='#e74c3c', alpha=0.7)
axes[2].set_title('Nombre de Commandes par Mois', fontsize=14, fontweight='bold')
axes[2].set_ylabel('Nombre de Commandes')
axes[2].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig('../outputs/02_evolution_temporelle.png', dpi=150, bbox_inches='tight')
plt.show()

# ============================================
# SAISONNALITÉ
# ============================================
# Regrouper par mois (toutes années confondues)
monthly_season = df.groupby('Order_Month').agg(
    CA=('Sales', 'sum'),
    Profit=('Profit', 'sum')
).reset_index()

# Nom des mois
mois_noms = ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin',
             'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre']
monthly_season['Mois'] = monthly_season['Order_Month'].apply(lambda x: mois_noms[int(x)-1])

plt.figure(figsize=(14, 6))
plt.bar(monthly_season['Mois'], monthly_season['CA'], color='#9b59b6', alpha=0.7)
plt.title('Saisonnalité : CA Total par Mois (toutes années)', fontsize=14, fontweight='bold')
plt.ylabel('Chiffre d\'Affaires ($)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('../outputs/02_saisonnalite.png', dpi=150, bbox_inches='tight')
plt.show()

# ============================================
# INSIGHT
# ============================================
print("\n💡 INSIGHTS :")
print(f"   - Le meilleur mois est {best_sales['Order_YearMonth']} avec un CA de ${best_sales['CA']:,.0f}")
print(f"   - Le mois le plus rentable est {best_profit['Order_YearMonth']} avec ${best_profit['Profit']:,.0f}")
print(f"   - La tendance est {'haussière' if monthly['CA'].iloc[-1] > monthly['CA'].iloc[0] else 'baissière'} sur la période")

print("\n✅ Analyse temporelle terminée !")