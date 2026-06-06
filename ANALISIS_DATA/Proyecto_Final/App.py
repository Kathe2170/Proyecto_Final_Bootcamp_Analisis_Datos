import streamlit as st
import pandas as pd
import plotly.express as px


# CONFIGURACIÓN DE LA PÁGINA

st.set_page_config(
    page_title="Accidentes de Tránsito Colombia",
    page_icon="🚗",
    layout="wide"
)

# CARGA DE DATOS

vehiculos = pd.read_csv(
    "VEHICULOS_INVOLUCRADOS_EN_UN_ACCIDENTE_DE_TRANSITO.csv"
)

victimas = pd.read_csv(
    "Homicidios_accidente_de_tránsito.csv"
)


def formato_col(numero):
    return f"{numero:,}".replace(",", ".")


# FILTROS

st.sidebar.header("🔎 Filtros")

departamentos_lista = sorted(
    vehiculos["DEPARTAMENTO_ACCIDENTE"]
    .dropna()
    .unique()
)

departamento_seleccionado = st.sidebar.selectbox(
    "Departamento",
    ["Todos"] + list(departamentos_lista)
)

tipos_lista = sorted(
    vehiculos["TIPO_VEHICULO"]
    .dropna()
    .unique()
)

tipo_seleccionado = st.sidebar.selectbox(
    "Tipo de vehículo",
    ["Todos"] + list(tipos_lista)
)

vehiculos_filtrado = vehiculos.copy()

if departamento_seleccionado != "Todos":
    vehiculos_filtrado = vehiculos_filtrado[
        vehiculos_filtrado["DEPARTAMENTO_ACCIDENTE"]
        == departamento_seleccionado
    ]

if tipo_seleccionado != "Todos":
    vehiculos_filtrado = vehiculos_filtrado[
        vehiculos_filtrado["TIPO_VEHICULO"]
        == tipo_seleccionado
    ]

if len(vehiculos_filtrado) == 0:
    st.warning(
        "No existen registros para la combinación de filtros seleccionada."
    )
    st.stop()

# TÍTULO

st.title("🚗 Análisis de Accidentes de Tránsito en Colombia")

st.write(
    "Dashboard interactivo creado por Katherine y Yenny"
)

st.markdown(
    f"""
    **Departamento:** {departamento_seleccionado}

    **Tipo de vehículo:** {tipo_seleccionado}
    """
)

# KPIs

total_vehiculos = len(vehiculos_filtrado)

accidentes_heridos = (
    vehiculos_filtrado["GRAVEDAD_ACCIDENTE"]
    == "CON HERIDOS"
).sum()

accidentes_muertos = (
    vehiculos_filtrado["GRAVEDAD_ACCIDENTE"]
    == "CON MUERTOS"
).sum()

edad_promedio = round(
    vehiculos_filtrado["EDAD_VEHICULO"].mean(),
    1
)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Vehículos involucrados",
    formato_col(total_vehiculos)
)

col2.metric(
    "Con heridos",
    formato_col(accidentes_heridos)
)

col3.metric(
    "Con muertos",
    formato_col(accidentes_muertos)
)

col4.metric(
    "Edad promedio vehículo",
    edad_promedio
)

# TIPOS DE VEHÍCULO

tipos_vehiculo = (
    vehiculos_filtrado["TIPO_VEHICULO"]
    .value_counts()
    .head(10)
    .reset_index()
)

tipos_vehiculo.columns = [
    "Tipo Vehiculo",
    "Cantidad"
]

fig_tipos = px.bar(
    tipos_vehiculo,
    x="Tipo Vehiculo",
    y="Cantidad",
    title="Top 10 tipos de vehículo involucrados"
)

# GRAVEDAD

gravedad = (
    vehiculos_filtrado["GRAVEDAD_ACCIDENTE"]
    .value_counts()
    .reset_index()
)

gravedad.columns = [
    "Gravedad",
    "Cantidad"
]

fig_gravedad = px.pie(
    gravedad,
    names="Gravedad",
    values="Cantidad",
    hole=0.5,
    title="Distribución de gravedad del accidente"
)

# FILA 1

st.subheader("🚗 Vehículos involucrados")

col_g1, col_g2 = st.columns(2)

with col_g1:
    st.plotly_chart(
        fig_tipos,
        use_container_width=True
    )

with col_g2:
    st.plotly_chart(
        fig_gravedad,
        use_container_width=True
    )

# DEPARTAMENTOS

departamentos = (
    vehiculos["DEPARTAMENTO_ACCIDENTE"]
    .value_counts()
    .head(10)
    .reset_index()
)

departamentos.columns = [
    "Departamento",
    "Cantidad"
]

fig_departamentos = px.bar(
    departamentos,
    x="Departamento",
    y="Cantidad",
    title="Top 10 departamentos con más accidentes"
)

# MUNICIPIOS

municipios = (
    vehiculos_filtrado["MUNICIPIO_ACCIDENTE"]
    .value_counts()
    .head(10)
    .reset_index()
)

municipios.columns = [
    "Municipio",
    "Cantidad"
]

fig_municipios = px.bar(
    municipios,
    x="Municipio",
    y="Cantidad",
    title="Top 10 municipios con más accidentes"
)

# FILA 2

st.subheader("📍 Distribución geográfica")

col_g3, col_g4 = st.columns(2)

with col_g3:
    st.plotly_chart(
        fig_departamentos,
        use_container_width=True
    )

with col_g4:
    st.plotly_chart(
        fig_municipios,
        use_container_width=True
    )

# GÉNERO

genero = (
    victimas.groupby("GENERO")["CANTIDAD"]
    .sum()
    .reset_index()
)

fig_genero = px.pie(
    genero,
    names="GENERO",
    values="CANTIDAD",
    hole=0.5,
    title="Víctimas por género"
)

# GRUPO ETARIO

grupo_etario = (
    victimas.groupby("GRUPO ETARÍO")["CANTIDAD"]
    .sum()
    .reset_index()
)

fig_grupo = px.bar(
    grupo_etario,
    x="GRUPO ETARÍO",
    y="CANTIDAD",
    title="Víctimas por grupo etario"
)

# FILA 3

st.subheader("👥 Perfil de las víctimas")

col_g5, col_g6 = st.columns(2)

with col_g5:
    st.plotly_chart(
        fig_genero,
        use_container_width=True
    )

with col_g6:
    st.plotly_chart(
        fig_grupo,
        use_container_width=True
    )

# EDAD VS GRAVEDAD

edad_gravedad = (
    vehiculos_filtrado
    .groupby("GRAVEDAD_ACCIDENTE")["EDAD_VEHICULO"]
    .mean()
    .reset_index()
)

fig_edad = px.bar(
    edad_gravedad,
    x="GRAVEDAD_ACCIDENTE",
    y="EDAD_VEHICULO",
    title="Edad promedio del vehículo según gravedad"
)

# FILA 4

st.subheader("⚠️ Severidad de los accidentes")

st.plotly_chart(
    fig_edad,
    use_container_width=True
)

# HALLAZGOS DINÁMICOS

porcentaje_heridos = round(
    accidentes_heridos / total_vehiculos * 100,
    1
)

porcentaje_muertos = round(
    accidentes_muertos / total_vehiculos * 100,
    1
)

st.subheader("📌 Principales Hallazgos")

st.markdown(f"""
- Se analizaron **{formato_col(total_vehiculos)}** vehículos involucrados en accidentes.

- El **{porcentaje_heridos}%** de los casos terminaron con heridos.

- El **{porcentaje_muertos}%** de los casos terminaron con víctimas fatales.

- La edad promedio de los vehículos involucrados es de **{edad_promedio} años**.

- Departamento analizado: **{departamento_seleccionado}**.

- Tipo de vehículo analizado: **{tipo_seleccionado}**.
""")