# -*- coding: utf-8 -*-
"""
Created on Wed Aug 20 19:14:00 2025

@author: guret
"""

import streamlit as st
import pandas as pd
import pydeck as pdk

# Configuración inicial
st.set_page_config(page_title="Dashboard Territorial", layout="wide")

# Cargar datos
@st.cache_data
def load_data():
    df = pd.read_csv("Data2.csv", sep=",", encoding="utf-8")
    df = df.dropna(subset=["Latitud", "Longitud"])  # Asegura que haya coordenadas
    return df

df = load_data()

# Sidebar: filtros
st.sidebar.header("🎯 Filtros")
region = st.sidebar.selectbox("Selecciona Región", options=df["Region"].unique())
comuna = st.sidebar.selectbox("Selecciona Comuna", options=df[df["Region"] == region]["comuna"].unique())
etapa = st.sidebar.multiselect("Etapa", options=df["Etapa"].unique(), default=df["Etapa"].unique())

# Filtrar datos
filtered_df = df[
    (df["Region"] == region) &
    (df["comuna"] == comuna) &
    (df["Etapa"].isin(etapa))
]

# Título
st.title("📍 Dashboard Territorial - EconoDataAI")
st.markdown("Visualización de proyectos según ubicación, etapa y comuna.")

# Mapa
st.subheader("🗺️ Mapa de Proyectos")
st.pydeck_chart(pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v9",
    initial_view_state=pdk.ViewState(
        latitude=filtered_df["Latitud"].mean(),
        longitude=filtered_df["Longitud"].mean(),
        zoom=11,
        pitch=0,
    ),
    layers=[
        pdk.Layer(
            "ScatterplotLayer",
            data=filtered_df,
            get_position='[Longitud, Latitud]',
            get_color='[200, 30, 0, 160]',
            get_radius=80,
            pickable=True,
        )
    ],
    tooltip={"text": "{Nombre_Ini}\nCosto: ${Costo_Tota}\nEtapa: {Etapa}"}
))

# Métricas
st.subheader("📈 Estadísticas")
col1, col2, col3 = st.columns(3)
col1.metric("Proyectos Totales", len(filtered_df))
col2.metric("Costo Total", f"${filtered_df['Costo_Tota'].sum():,.0f}")
col3.metric("Instituciones", filtered_df["Institucio"].nunique())

# Tabla
st.subheader("📋 Detalle de Proyectos")
st.dataframe(filtered_df[[
    "Solicitud", "Nombre_Ini", "Codigo_Bip", "Etapa", "Costo_Tota", "Institucio", "Region", "comuna"
]])
