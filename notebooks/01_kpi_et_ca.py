# ============================================
# OBJECTIF 1 : KPI - CHIFFRE D'AFFAIRES, PROFIT, VENTES
# ============================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

print("=" * 60)
print("📊 OBJECTIF 1 : INDICATEURS CLÉS DE PERFORMANCE (KPI)")
print("=" * 60)

# Charger les données nettoyées
df = pd.read_csv('../data/supermarket_sales_cleaned.csv')

# ============================================
# CALCUL DES KPI
# ============================================
print("\n🧮 CALCUL DES KPI")
print("-" * 40)

total_sales = df['Sales'].sum()
total_profit = df['Profit'].sum()
total_orders = df['Order_ID'].nunique()
total_customers = df['Customer_ID'].nunique()
total_quantity = df['Quantity'].sum()
avg_discount = df['Discount'].mean()
avg_basket = total_sales / total_orders
avg_profit_per_order = total_profit / total_orders
margin_rate = (total_profit / total_sales) * 100

print(f"Chiffre d'affaires total       : ${total_sales:,.2f}")
print(f"Profit total                   : ${total_profit:,.2f}")
print(f"Nombre total de commandes      : {total_orders:,}")
print(f"Nombre de clients              : {total_customers:,}")
print(f"Quantité totale vendue         : {total_quantity:,}")
print(f"Remise moyenne                 : {avg_discount:.2%}")
print(f"Panier moyen                   : ${avg_basket:,.2f}")
print(f"Profit moyen par commande      : ${avg_profit_per_order:,.2f}")
print(f"Taux de marge                  : {margin_rate:.1f}%")

# ============================================
# TABLEAU RÉCAPITULATIF
# ============================================
kpi_data = {
    'Indicateur': [
        '💰 Chiffre d\'affaires total',
        '📈 Profit total',
        '🛒 Nombre de commandes',
        '👥 Nombre de clients',
        '📦 Quantité vendue',
        '💸 Remise moyenne',
        '🧺 Panier moyen',
        '💵 Profit/commande',
        '📊 Taux de marge'
    ],
    'Valeur': [
        f"${total_sales:,.2f}",
        f"${total_profit:,.2f}",
        f"{total_orders:,}",
        f"{total_customers:,}",
        f"{total_quantity:,}",
        f"{avg_discount:.2%}",
        f"${avg_basket:,.2f}",
        f"${avg_profit_per_order:,.2f}",
        f"{margin_rate:.1f}%"
    ]
}

kpi_df = pd.DataFrame(kpi_data)
print("\n📋 TABLEAU DE BORD - KPI")
print("=" * 60)
print(kpi_df.to_string(index=False))

# ============================================
# VISUALISATION
# ============================================
fig, axes = plt.subplots(1, 4, figsize=(16, 5))

# CA
axes[0].bar(['CA'], [total_sales], color='#3498db')
axes[0].set_title('💰 Chiffre d\'Affaires', fontweight='bold')
axes[0].set_ylabel('$')
axes[0].text(0, total_sales/2, f'${total_sales:,.0f}', ha='center', fontsize=14, fontweight='bold', color='white')

# Profit
axes[1].bar(['Profit'], [total_profit], color='#2ecc71')
axes[1].set_title('📈 Profit', fontweight='bold')
axes[1].set_ylabel('$')
axes[1].text(0, total_profit/2, f'${total_profit:,.0f}', ha='center', fontsize=14, fontweight='bold', color='white')

# Commandes
axes[2].bar(['Commandes'], [total_orders], color='#e74c3c')
axes[2].set_title('🛒 Commandes', fontweight='bold')
axes[2].text(0, total_orders/2, f'{total_orders:,}', ha='center', fontsize=14, fontweight='bold', color='white')

# Clients
axes[3].bar(['Clients'], [total_customers], color='#f39c12')
axes[3].set_title('👥 Clients', fontweight='bold')
axes[3].text(0, total_customers/2, f'{total_customers:,}', ha='center', fontsize=14, fontweight='bold', color='white')

plt.suptitle('Tableau de Bord - Indicateurs Clés', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig('../outputs/01_kpi_dashboard.png', dpi=150, bbox_inches='tight')
plt.show()

# ============================================
# INSIGHT
# ============================================
print("\n💡 INSIGHT :")
print(f"   Le supermarché a généré {total_orders:,} commandes pour un CA de ${total_sales:,.0f}.")
print(f"   Le taux de marge est de {margin_rate:.1f}%, ce qui est {'bon' if margin_rate > 10 else 'faible'}.")
print(f"   Le panier moyen est de ${avg_basket:,.2f}.")

print("\n✅ Analyse KPI terminée !")