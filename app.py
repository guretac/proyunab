import streamlit as st
import pandas as pd
import plotly.express as px

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
        df['Costo_Tota'] = df['Costo_Tota'].astype(str).str.replace('.', '', regex=False)
        df['Costo_Tota'] = pd.to_numeric(df['Costo_Tota'], errors='coerce').fillna(0)
        df['Latitud'] = pd.to_numeric(df['Latitud'], errors='coerce')
        df['Longitud'] = pd.to_numeric(df['Longitud'], errors='coerce')
        
        # Drop rows with invalid coordinates
        df.dropna(subset=['Latitud', 'Longitud'], inplace=True)

        # Sidebar filters
        st.sidebar.header('Filtros')

        # Filtro de Comuna
        comunas = ['Todas'] + sorted(df['Dimensione'].unique())
        selected_comuna = st.sidebar.selectbox('Seleccionar Dimensiones', comunas)

        # Aplicar el filtro al DataFrame
        filtered_df = df.copy()
        if selected_comuna != 'Todas':
            filtered_df = filtered_df[filtered_df['Dimensione'] == selected_comuna]
            
        st.markdown('---')

        # Main content
        if not filtered_df.empty:
            
            # Display a map
            st.markdown(f'### Ubicación de Proyectos en el Mapa para la comuna de {selected_comuna}')
            st.map(filtered_df[['Latitud', 'Longitud']].rename(columns={'Latitud': 'lat', 'Longitud': 'lon'}))
            
            st.markdown('---')

            st.markdown(f'### Datos de Proyectos')
            st.dataframe(filtered_df[['Nombre_Ini', 'Anio_Presu', 'Etapa', 'Institucio', 'Costo_Tota', 'comuna', 'Estado', 'Dimensione']])

            st.markdown('---')

            # Display a bar chart using plotly
            st.markdown('### Costo Total por Comuna')
            cost_by_comuna = filtered_df.groupby('comuna')['Costo_Tota'].sum().reset_index()
            fig = px.bar(cost_by_comuna, 
                         x='comuna', 
                         y='Costo_Tota', 
                         title='Costo Total por Comuna', 
                         labels={'Costo_Tota': 'Costo Total (CLP)', 'comuna': 'Comuna'})
            fig.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)

        else:
            st.warning('No hay datos para la combinación de filtros seleccionada.')

if __name__ == "__main__":
    create_dashboard()