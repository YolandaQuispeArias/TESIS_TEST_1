import streamlit as st
import geopandas as gpd
from shapely.geometry import shape
import os

# Título de la aplicación
st.title("Calculadora de Áreas y Perímetros Geoespaciales")

# Instrucción para subir un archivo
st.write("Sube tu archivo Shapefile (como archivo .zip) o KML para calcular áreas y perímetros.")

# Carga de archivos
uploaded_file = st.file_uploader("Sube tu archivo (Shapefile como ZIP o KML)", type=["zip", "kml"])

# Verificar si se subió un archivo
if uploaded_file is not None:
    st.success("¡Archivo cargado exitosamente!")
else:
    st.warning("Esperando archivo...")

def process_shapefile(zip_file):
    import tempfile
    import zipfile

    with tempfile.TemporaryDirectory() as tmpdir:
        # Extraer los archivos del ZIP
        with zipfile.ZipFile(zip_file, 'r') as z:
            z.extractall(tmpdir)

        # Buscar el archivo .shp dentro del ZIP extraído
        shapefile_path = [os.path.join(tmpdir, f) for f in os.listdir(tmpdir) if f.endswith(".shp")]
        if not shapefile_path:
            st.error("No se encontró un archivo .shp en el ZIP.")
            return None

        # Leer el archivo shapefile con GeoPandas
        gdf = gpd.read_file(shapefile_path[0])
        return gdf

def process_kml(kml_file):
    # Leer archivo KML con GeoPandas
    gdf = gpd.read_file(kml_file)
    return gdf



if uploaded_file is not None:
    if uploaded_file.name.endswith(".zip"):
        gdf = process_shapefile(uploaded_file)
    elif uploaded_file.name.endswith(".kml"):
        gdf = process_kml(uploaded_file)
    else:
        st.error("Formato no compatible.")
        gdf = None


if gdf is not None:
    st.write("Visualización de datos geoespaciales cargados:")
    st.write(gdf)

    # Asegúrate de que el GeoDataFrame tenga una proyección adecuada
    if gdf.crs is None or gdf.crs.is_geographic:
        st.warning("El sistema de coordenadas está en latitud/longitud. Reproyectando a UTM para cálculos precisos.")
        gdf = gdf.to_crs(gdf.estimate_utm_crs())

    # Calcular área y perímetro
    gdf['Área (m²)'] = gdf.geometry.area
    gdf['Perímetro (m)'] = gdf.geometry.length

    st.write("Resultados con área y perímetro:")
    st.write(gdf[['Área (m²)', 'Perímetro (m)']])

streamlit run app.py
