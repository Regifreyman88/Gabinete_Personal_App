import streamlit as st

st.set_page_config(
    page_title="Fase 2: Arquitectura Conceptual",
    page_icon="📐"
)

st.title("Fase 2: La Arquitectura Conceptual 📐")

st.header("La Metáfora: EL ESPEJO")
st.info(
    """
    "Hasta ahora, hemos usado nuestras herramientas para analizar el mundo exterior. 
    Ahora, damos la vuelta a la lente y la enfocamos hacia adentro. Un gabinete personal 
    no es una ventana para ver el mundo, es un espejo para verse a uno mismo."
    """
)
st.markdown("---")

st.header("Tu Misión de Diseño")
st.write(
    """
    **1. Actividad Manual:** En una hoja de papel o en tu bitácora, dibuja el "plano" de tu 
    Gabinete de Maravillas personal. No tiene que ser técnico, puede ser un mapa conceptual, 
    un collage o un dibujo simbólico.

    **2. Actividad Digital:** Usa las siguientes herramientas para definir la esencia de tu gabinete.
    """
)

# --- Componentes Interactivos ---

st.subheader("La Ficha Arquitectónica de tu Gabinete")

# Pregunta Activa
tipo_espejo = st.radio(
    "La Pregunta Activa: ¿Qué tipo de gabinete será el tuyo?",
    [
        "Uno que refleje la verdad cruda.",
        "Uno que embellezca la realidad.",
        "Uno que muestre el potencial."
    ],
    key="tipo_espejo"
)

# Metáfora Central
metafora_central = st.text_input(
    "1. La Metáfora Central (El Nombre Secreto): Elige una metáfora que defina el alma de tu Gabinete.",
    placeholder="Ej: Mi mente es un faro en la niebla, un jardín amurallado..."
)

# Salas Principales
salas_principales = st.text_area(
    "2. Las 'Salas' Principales: Define de 3 a 5 'salas' o 'exhibiciones' dentro de tu Gabinete.",
    placeholder="Ej: La Sala de los Miedos Heredados, La Galería de las Esperanzas Ruidosas..."
)

# Artefacto Central
artefacto_central = st.text_input(
    "3. El Artefacto Central: Describe el único objeto, real o imaginado, que está en el corazón de tu Gabinete.",
    placeholder="Ej: Una brújula rota, una semilla que brilla en la oscuridad..."
)

# --- Guardar y Mostrar Resumen ---
if st.button("Guardar Arquitectura en la Bitácora"):
    if tipo_espejo and metafora_central and salas_principales and artefacto_central:
        st.success("¡Arquitectura guardada con éxito!")
        
        st.markdown("---")
        st.subheader("Resumen de tu Gabinete:")
        st.write(f"**Tipo de Espejo:** {tipo_espejo}")
        st.write(f"**Metáfora Central:** {metafora_central}")
        st.write(f"**Salas Principales:**")
        st.write(salas_principales)
        st.write(f"**Artefacto Central:** {artefacto_central}")
    else:
        st.warning("Por favor, completa todos los campos para guardar tu arquitectura.")
