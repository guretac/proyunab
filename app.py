import streamlit as st
import pandas as pd
import pydeck as pdk

# Configuración inicial
st.set_page_config(page_title="Dashboard Territorial", layout="wide")

# Función robusta para cargar datos
def load_data():
    try:
        df = pd.read_csv("Data2.csv", sep=",", encoding="utf-8", engine="python", on_bad_lines="skip")
        df = df.dropna(subset=["Latitud", "Longitud"])
        return df
    except Exception as e:
        st.warning("⚠️ No se pudo cargar 'Data2.csv'. Puedes subirlo manualmente:")
        uploaded_file = st.file_uploader("Sube tu archivo CSV", type=["csv"])
        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file, sep=",", encoding="utf-8", engine="python", on_bad_lines="skip")
                df = df.dropna(subset=["Latitud", "Longitud"])
                return df
            except Exception as e2:
                st.error(f"❌ Error al leer el archivo subido: {e2}")
                st.stop()
        else:
            st.stop()

# Cargar datos
df = load_data()

# Sidebar: filtros
st.sidebar.header("🎯 Filtros")
region = st.sidebar.selectbox("Selecciona Región", options=df["Region"].dropna().unique())
comuna = st.sidebar.selectbox("Selecciona Comuna", options=df[df["Region"] == region]["comuna"].dropna().unique())
etapa = st.sidebar.multiselect("Etapa", options=df["Etapa"].dropna().unique(), default=df["Etapa"].dropna().unique())

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