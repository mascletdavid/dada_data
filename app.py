 # -*- coding: utf-8 -*-

import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(page_title="Analyse Dés et Abattages", layout="wide")

# ==============================
# Titre et description
# ==============================
st.title("Analyse des Lancers de Des et Abattages")
st.markdown("""
Cette application présente des statistiques et visualisations
issues des fichiers **Lancers_des.csv** et **Abattages.csv**.
""")

# ==============================
# Chargement des données
# ==============================
try:
    df_lancers = pd.read_csv("./Lancers_des.csv")
    df_abattages = pd.read_csv("./Abattages.csv")
except FileNotFoundError:
    st.error("Fichiers CSV manquants. Veuillez vérifier que `Lancers_des.csv` et `Abattages.csv` sont dans le dossier.")
    st.stop()

st.subheader("Aperçu des données de lancers")
st.dataframe(df_lancers.head())

# ==============================
# 1. Moyenne pondérée par joueur
# ==============================
faces = ["Face_1", "Face_2", "Face_3", "Face_4", "Face_5", "Face_6"]
df_lancers["Moyenne"] = (
    df_lancers[faces]
    .mul([1, 2, 3, 4, 5, 6], axis=1)
    .sum(axis=1)
) / df_lancers["Nb_Total_Lancers"]

couleurs = {
    "Nelly": "#1f77b4",
    "Thibault": "#ffdd00",
    "Lucas": "#2ca02c",
    "David": "#d62728"
}

st.subheader("Moyenne des dés par joueur")
fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(
    x="Joueur",
    y="Moyenne",
    hue="Joueur",
    data=df_lancers,
    palette=couleurs,
    dodge=False,
    legend=False,
    ax=ax
)
ax.set_title("Moyenne des dés par joueur")
ax.set_ylim(1, 6)
ax.set_ylabel("Valeur moyenne")
ax.grid(axis='y')
st.pyplot(fig)

# ==============================
# 2. Fréquences normalisées à 100 lancers
# ==============================
for face in faces:
    df_lancers[f"{face}_norm_100"] = df_lancers[face] / df_lancers["Nb_Total_Lancers"] * 100

df_norm = df_lancers[["Joueur"] + [f"{face}_norm_100" for face in faces]]
df_melted = df_norm.melt(id_vars="Joueur", var_name="Face", value_name="Occurrences_pour_100_lancers")
df_melted["Face"] = df_melted["Face"].str.extract(r"(Face_\d)")

st.subheader("Fréquences des faces (normalisées à 100 lancers)")
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(
    x="Face",
    y="Occurrences_pour_100_lancers",
    hue="Joueur",
    data=df_melted,
    ax=ax
)
ax.set_title("Fréquences des faces (normalisées à 100 lancers)")
ax.set_ylabel("Occurrences pour 100 lancers")
ax.grid(axis='y')
ax.legend(title="Joueur", bbox_to_anchor=(1.05, 1), loc='upper left')
st.pyplot(fig)

# ==============================
# 3. Scatter interactif Plotly
# ==============================
df_lancers["Somme_des"] = (
    df_lancers[faces]
    .mul([1, 2, 3, 4, 5, 6], axis=1)
    .sum(axis=1)
)

couleurs_plotly = {
    "Nelly": "blue",
    "Thibault": "yellow",
    "Lucas": "green",
    "David": "red"
}

df_lancers["Taille_Point"] = 50

fig_plotly = px.scatter(
    df_lancers,
    x="Nb_Total_Lancers",
    y="Somme_des",
    text="Joueur",
    color="Joueur",
    size="Taille_Point",
    color_discrete_map=couleurs_plotly,
    labels={
        "Nb_Total_Lancers": "Nombre de lancers",
        "Somme_des": "Somme des dés"
    },
    title="Nombre de lancers vs score total"
)
fig_plotly.update_traces(textposition='top right')
fig_plotly.update_layout(width=940, height=600)
st.plotly_chart(fig_plotly)

# ==============================
# 4. Abattages par joueur
# ==============================
st.subheader("Abattages par joueur")
st.dataframe(df_abattages.head())

df_pivot = df_abattages.pivot_table(
    index="Abattant",
    columns="Abattu",
    values="Nb_fois",
    fill_value=0
)

couleurs_abattages = {
    "Nelly": "blue",
    "Thibault": "yellow",
    "Lucas": "green",
    "David": "red"
}
palette = [couleurs_abattages[abattu] for abattu in df_pivot.columns]

fig, ax = plt.subplots(figsize=(10, 6))
df_pivot.plot(
    kind='bar',
    stacked=True,
    color=palette,
    ax=ax
)
ax.set_title("Nombre d'abattages par joueur (détail des cibles)")
ax.set_xlabel("Abattant")
ax.set_ylabel("Nombre d'abattages")
ax.legend(title="Abattu")
ax.grid(axis='y')
st.pyplot(fig)
