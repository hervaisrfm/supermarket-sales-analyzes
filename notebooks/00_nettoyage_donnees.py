# ============================================
# NETTOYAGE DES DONNÉES - SUPERMARCHÉ
# ============================================
# Objectif : Préparer les données pour l'analyse
# Exécution : python 00_nettoyage_donnees.py
# ============================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os
import warnings
warnings.filterwarnings('ignore')

# Configuration d'affichage
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 50)
pd.set_option('display.width', 1000)
pd.set_option('display.float_format', '{:.2f}'.format)

# Style des graphiques
sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

print("=" * 60)
print("🧹 NETTOYAGE DES DONNÉES - SUPERMARCHÉ")
print("=" * 60)

# ============================================
# 1. CHARGEMENT DES DONNÉES
# ============================================
print("\n📂 1. CHARGEMENT DES DONNÉES")
print("-" * 40)

# Créer le dossier outputs s'il n'existe pas
if not os.path.exists('../outputs'):
    os.makedirs('../outputs')

df = pd.read_csv('../data/supermarket_sales.csv')

print(f"✅ Données chargées : {df.shape[0]} lignes × {df.shape[1]} colonnes")
print(f"Colonnes : {df.columns.tolist()}")
print("\n5 premières lignes :")
print(df.head())

# ============================================
# 2. RENOMMER LES COLONNES
# ============================================
print("\n🔄 2. RENOMMAGE DES COLONNES")
print("-" * 40)

anciens_noms = df.columns.tolist()
df.columns = df.columns.str.replace(' ', '_').str.replace('/', '_')
nouveaux_noms = df.columns.tolist()

for ancien, nouveau in zip(anciens_noms, nouveaux_noms):
    if ancien != nouveau:
        print(f"  {ancien:30s} → {nouveau}")
    else:
        print(f"  {ancien:30s}   (inchangé)")

print(f"\n✅ {len(nouveaux_noms)} colonnes renommées")

# ============================================
# 3. TYPES DE DONNÉES
# ============================================
print("\n📋 3. TYPES DE DONNÉES")
print("-" * 40)
print(df.dtypes.to_string())

# ============================================
# 4. VALEURS MANQUANTES
# ============================================
print("\n🔍 4. DÉTECTION DES VALEURS MANQUANTES")
print("-" * 40)

missing = df.isnull().sum()
missing_pct = (missing / len(df)) * 100

missing_df = pd.DataFrame({
    'Colonne': missing.index,
    'Nombre_NaN': missing.values,
    'Pourcentage_%': missing_pct.values
})
missing_df = missing_df[missing_df['Nombre_NaN'] > 0].sort_values('Nombre_NaN', ascending=False)

if len(missing_df) == 0:
    print("✅ Aucune valeur manquante détectée !")
else:
    print(missing_df.to_string(index=False))

# ============================================
# 5. DOUBLONS
# ============================================
print("\n🔍 5. DÉTECTION DES DOUBLONS")
print("-" * 40)

nb_duplicates_exact = df.duplicated().sum()
print(f"Doublons exacts : {nb_duplicates_exact}")

nb_duplicates_subset = df.duplicated(subset=['Order_ID', 'Product_ID']).sum()
print(f"Doublons (Order_ID + Product_ID) : {nb_duplicates_subset}")

if nb_duplicates_exact > 0:
    before = len(df)
    df = df.drop_duplicates()
    after = len(df)
    print(f"✅ {before - after} doublons exacts supprimés")
else:
    print("✅ Aucun doublon à supprimer")

# ============================================
# 6. PARSING DES DATES
# ============================================
print("\n📅 6. PARSING DES DATES")
print("-" * 40)

def parse_date_flexible(date_str):
    """Parse une date avec plusieurs formats possibles."""
    if pd.isna(date_str):
        return pd.NaT
    
    date_str = str(date_str).strip()
    
    formats = [
        '%m/%d/%Y',      # 3/1/2021
        '%d-%m-%Y',      # 13-01-2021
        '%d/%m/%Y',      # 13/01/2021
        '%Y-%m-%d',      # 2021-01-13
        '%m-%d-%Y',      # 01-13-2021
        '%d.%m.%Y',      # 13.01.2021
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except (ValueError, TypeError):
            continue
    
    print(f"⚠️ Format non reconnu : {date_str}")
    return pd.NaT

print("Parsing de Order_Date...")
df['Order_Date'] = df['Order_Date'].apply(parse_date_flexible)

print("Parsing de Ship_Date...")
df['Ship_Date'] = df['Ship_Date'].apply(parse_date_flexible)

nb_order_na = df['Order_Date'].isna().sum()
nb_ship_na = df['Ship_Date'].isna().sum()

print(f"Order_Date non parsées : {nb_order_na}")
print(f"Ship_Date non parsées  : {nb_ship_na}")

if nb_order_na == 0 and nb_ship_na == 0:
    print("✅ Toutes les dates parsées avec succès !")

# ============================================
# 7. CRÉER COLONNES TEMPORELLES
# ============================================
print("\n📅 7. CRÉATION DES COLONNES TEMPORELLES")
print("-" * 40)

df['Order_Year'] = df['Order_Date'].dt.year
df['Order_Month'] = df['Order_Date'].dt.month
df['Order_Month_Name'] = df['Order_Date'].dt.month_name()
df['Order_Day'] = df['Order_Date'].dt.day
df['Order_DayOfWeek'] = df['Order_Date'].dt.day_name()
df['Order_YearMonth'] = df['Order_Date'].dt.to_period('M').astype(str)
df['Shipping_Days'] = (df['Ship_Date'] - df['Order_Date']).dt.days

nouvelles_colonnes = ['Order_Year', 'Order_Month', 'Order_Month_Name', 'Order_Day', 
                       'Order_DayOfWeek', 'Order_YearMonth', 'Shipping_Days']
for col in nouvelles_colonnes:
    print(f"  ✅ {col}")

print("\nÉchantillon :")
print(df[nouvelles_colonnes].head(10))

# ============================================
# 8. ANALYSE COUNTRY_REGION
# ============================================
print("\n🌍 8. ANALYSE DE LA COLONNE Country_Region")
print("-" * 40)

pays = df['Country_Region'].value_counts()
print(f"Nombre de pays différents : {len(pays)}")
print(pays)

if len(pays) == 1:
    print(f"💡 Un seul pays détecté ({pays.index[0]}). Colonne non utilisée pour l'analyse.")

# ============================================
# 9. STATISTIQUES NUMÉRIQUES
# ============================================
print("\n📊 9. STATISTIQUES DES COLONNES NUMÉRIQUES")
print("-" * 40)

colonnes_numeriques = ['Sales', 'Quantity', 'Discount', 'Profit']
print(df[colonnes_numeriques].describe())

# ============================================
# 10. BOXPLOTS
# ============================================
print("\n📦 10. GÉNÉRATION DES BOXPLOTS")
print("-" * 40)

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

colonnes = ['Sales', 'Quantity', 'Discount', 'Profit']
couleurs = ['#3498db', '#2ecc71', '#e74c3c', '#f39c12']
titres = ['Chiffre d\'Affaires (Sales)', 'Quantité (Quantity)', 
          'Remise (Discount)', 'Profit']

for i, (col, couleur, titre) in enumerate(zip(colonnes, couleurs, titres)):
    ax = axes[i//2, i%2]
    sns.boxplot(data=df, y=col, ax=ax, color=couleur)
    ax.set_title(titre, fontsize=14, fontweight='bold')
    ax.set_ylabel('')

plt.suptitle('Distribution des Variables Numériques', fontsize=16, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('../outputs/boxplots_nettoyage.png', dpi=150, bbox_inches='tight')
plt.show()
print("✅ Boxplots sauvegardés dans outputs/boxplots_nettoyage.png")

# ============================================
# 11. ANALYSE DES REMISES
# ============================================
print("\n💸 11. ANALYSE DES REMISES")
print("-" * 40)

print("Distribution des taux de remise :")
discount_dist = df['Discount'].value_counts().sort_index()
for taux, nb in discount_dist.items():
    barre = '█' * int(nb / len(df) * 100)
    print(f"  {taux:.0%} : {nb:5d} transactions  {barre}")

df['Discount_Category'] = pd.cut(
    df['Discount'],
    bins=[-0.01, 0, 0.2, 0.5, 1.0],
    labels=['0%', '0-20%', '20-50%', '>50%']
)

print("\nRépartition par catégorie :")
print(df['Discount_Category'].value_counts().sort_index())

print("\nProfit moyen par catégorie de remise :")
print(df.groupby('Discount_Category', observed=False)['Profit'].mean().to_string())

# ============================================
# 12. ANALYSE DES PERTES
# ============================================
print("\n📉 12. ANALYSE DES VENTES À PERTE")
print("-" * 40)

nb_perte = (df['Profit'] < 0).sum()
nb_total = len(df)
pct_perte = (nb_perte / nb_total) * 100

print(f"Transactions avec perte : {nb_perte} sur {nb_total} ({pct_perte:.1f}%)")

ventes_normales = df[df['Profit'] >= 0]
ventes_perte = df[df['Profit'] < 0]

print(f"\n{'Caractéristique':30s} {'Ventes normales':>15s} {'Ventes à perte':>15s}")
print("-" * 60)
print(f"{'Remise moyenne':30s} {ventes_normales['Discount'].mean():>15.2%} {ventes_perte['Discount'].mean():>15.2%}")
print(f"{'Quantité moyenne':30s} {ventes_normales['Quantity'].mean():>15.1f} {ventes_perte['Quantity'].mean():>15.1f}")
print(f"{'Profit moyen':30s} {ventes_normales['Profit'].mean():>15.2f}€ {ventes_perte['Profit'].mean():>15.2f}€")

# ============================================
# 13. COHÉRENCE DES DATES
# ============================================
print("\n📅 13. VÉRIFICATION COHÉRENCE DES DATES")
print("-" * 40)

dates_incoherentes = df[df['Ship_Date'] < df['Order_Date']]
nb_incoherent = len(dates_incoherentes)

if nb_incoherent > 0:
    print(f"⚠️ {nb_incoherent} lignes avec Ship_Date < Order_Date")
else:
    print("✅ Toutes les dates cohérentes")

print(f"\nDélai de livraison moyen : {df['Shipping_Days'].mean():.1f} jours")
print(f"Délai de livraison médian : {df['Shipping_Days'].median():.1f} jours")
print(f"Délai min : {df['Shipping_Days'].min():.0f} jours")
print(f"Délai max : {df['Shipping_Days'].max():.0f} jours")

# ============================================
# 14. RÉSUMÉ
# ============================================
print("\n" + "=" * 60)
print("📋 14. RÉSUMÉ DU NETTOYAGE")
print("=" * 60)

print(f"""
✅ Colonnes renommées (espaces → underscores)
✅ Dates parsées (formats US et FR)
✅ 7 nouvelles colonnes temporelles créées
✅ {nb_duplicates_exact} doublons supprimés
✅ Colonne Discount_Category créée

Dimensions initiales : {nb_total} lignes × {len(anciens_noms)} colonnes
Dimensions finales   : {len(df)} lignes × {len(df.columns)} colonnes

Colonnes finales ({len(df.columns)}) :
""")

for i, col in enumerate(df.columns, 1):
    print(f"  {i:2d}. {col}")

# ============================================
# 15. SAUVEGARDE
# ============================================
print("\n💾 15. SAUVEGARDE DES DONNÉES")
print("-" * 40)

output_path = '../data/supermarket_sales_cleaned.csv'
df.to_csv(output_path, index=False)

print(f"✅ Fichier sauvegardé : {output_path}")
print(f"   {len(df)} lignes × {len(df.columns)} colonnes")

print("\n" + "=" * 60)
print("🎉 NETTOYAGE TERMINÉ AVEC SUCCÈS !")
print("=" * 60)