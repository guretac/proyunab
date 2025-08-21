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

        # 1. Filtro por "Anio_Presu"
        years = sorted(df['Anio_Presu'].unique())
        selected_years = st.sidebar.multiselect('Año de Presupuesto', years, default=years)

        # 2. Filtro por "Etapa"
        stages = sorted(df['Etapa'].unique())
        selected_stages = st.sidebar.multiselect('Etapa', stages, default=stages)

        # 3. Filtro por "Institucio"
        institutions = sorted(df['Institucio'].unique())
        selected_institutions = st.sidebar.multiselect('Institución', institutions, default=institutions)

        # 4. Filtro por "Institucio_1"
        institutions_1 = sorted(df['Institucio_1'].unique())
        selected_institutions_1 = st.sidebar.multiselect('Institución_1', institutions_1, default=institutions_1)

        # 5. Filtro por "Tipo_Insti"
        insti_types = sorted(df['Tipo_Insti'].unique())
        selected_insti_types = st.sidebar.multiselect('Tipo de Institución', insti_types, default=insti_types)

        # 6. Filtro por "Tipo_Insti_1"
        insti_types_1 = sorted(df['Tipo_Insti_1'].unique())
        selected_insti_types_1 = st.sidebar.multiselect('Tipo de Institución_1', insti_types_1, default=insti_types_1)

        # Filtros adicionales
        dimensions = sorted(df['Dimensione'].unique())
        selected_dimensions = st.sidebar.multiselect('Dimensión', dimensions, default=dimensions)

        subdimensions = sorted(df['Subdimensi'].unique())
        selected_subdimensions = st.sidebar.multiselect('Subdimensión', subdimensions, default=subdimensions)

        states = sorted(df['Estado'].unique())
        selected_states = st.sidebar.multiselect('Estado', states, default=states)

        regions = sorted(df['Region'].unique())
        selected_regions = st.sidebar.multiselect('Región', regions, default=regions)

        comunas = sorted(df['comuna'].unique())
        selected_comunas = st.sidebar.multiselect('Comuna', comunas, default=comunas)

        rates = sorted(df['RATE'].unique())
        selected_rates = st.sidebar.multiselect('RATE', rates, default=rates)


        # Apply all filters
        filtered_df = df[
            (df['Anio_Presu'].isin(selected_years)) &
            (df['Etapa'].isin(selected_stages)) &
            (df['Institucio'].isin(selected_institutions)) &
            (df['Institucio_1'].isin(selected_institutions_1)) &
            (df['Tipo_Insti'].isin(selected_insti_types)) &
            (df['Tipo_Insti_1'].isin(selected_insti_types_1)) &
            (df['Dimensione'].isin(selected_dimensions)) &
            (df['Subdimensi'].isin(selected_subdimensions)) &
            (df['Estado'].isin(selected_states)) &
            (df['Region'].isin(selected_regions)) &
            (df['comuna'].isin(selected_comunas)) &
            (df['RATE'].isin(selected_rates))
        ]

        st.markdown('---')

        # Main content
        if not filtered_df.empty:
            
            # Display a map
            st.markdown(f'### Ubicación de Proyectos en el Mapa')
            st.map(filtered_df[['Latitud', 'Longitud']].rename(columns={'Latitud': 'lat', 'Longitud': 'lon'}))
            
            st.markdown('---')

            st.markdown(f'### Datos de Proyectos')
            st.dataframe(filtered_df[['Nombre_Ini', 'Anio_Presu', 'Etapa', 'Institucio', 'Costo_Tota', 'Region', 'comuna', 'Estado', 'Dimensione']])

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