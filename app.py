import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

@st.cache_data
def load_data(file_path):
    """Loads and caches the data."""
    try:
        data = pd.read_csv(file_path, sep=';')
        return data
    except FileNotFoundError:
        st.error(f"Error: The file '{file_path}' was not found. Please make sure it's in the same directory.")
        return None

def create_dashboard():
    """Creates the Streamlit dashboard."""
    st.title('Dashboard de Proyectos')
    st.markdown('### Análisis de proyectos basados en la Región Metropolitana de Santiago')

    df = load_data('Data2.csv')

    if df is not None:
        # Pre-process the data
        df['Costo_Tota'] = pd.to_numeric(df['Costo_Tota'].str.replace('.', '', regex=False), errors='coerce').fillna(0)
        df['Latitud'] = pd.to_numeric(df['Latitud'], errors='coerce')
        df['Longitud'] = pd.to_numeric(df['Longitud'], errors='coerce')
        
        # Drop rows with invalid coordinates
        df.dropna(subset=['Latitud', 'Longitud'], inplace=True)

        # Sidebar filters
        st.sidebar.header('Filtros')
        selected_region = st.sidebar.selectbox('Seleccionar Región', ['Todas'] + list(df['Region'].unique()))
        
        filtered_df = df.copy()
        if selected_region != 'Todas':
            filtered_df = filtered_df[filtered_df['Region'] == selected_region]
        
        selected_comuna = st.sidebar.selectbox('Seleccionar Comuna', ['Todas'] + list(filtered_df['comuna'].unique()))
        
        if selected_comuna != 'Todas':
            filtered_df = filtered_df[filtered_df['comuna'] == selected_comuna]

        st.markdown('---')

        # Main content
        if not filtered_df.empty:
            
            # Display a map
            st.markdown(f'### Ubicación de Proyectos en el Mapa para {selected_region} - {selected_comuna}')
            st.map(filtered_df[['Latitud', 'Longitud']].rename(columns={'Latitud': 'lat', 'Longitud': 'lon'}))
            
            st.markdown('---')

            st.markdown(f'### Datos de Proyectos')
            st.dataframe(filtered_df[['Nombre_Ini', 'Anio_Presu', 'Etapa', 'Institucio', 'Costo_Tota', 'Region', 'comuna', 'Estado', 'Dimensione']])

            st.markdown('---')

            # Display a bar chart
            st.markdown('### Costo Total por Comuna')
            cost_by_comuna = filtered_df.groupby('comuna')['Costo_Tota'].sum().sort_values(ascending=False)
            
            fig, ax = plt.subplots(figsize=(12, 6))
            cost_by_comuna.plot(kind='bar', ax=ax, color='skyblue')
            ax.set_title('Costo Total por Comuna')
            ax.set_xlabel('Comuna')
            ax.set_ylabel('Costo Total (CLP)')
            ax.ticklabel_format(style='plain', axis='y')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            st.pyplot(fig)

        else:
            st.warning('No hay datos para la combinación de filtros seleccionada.')

if __name__ == "__main__":
    create_dashboard()