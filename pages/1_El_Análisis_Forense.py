import streamlit as st

st.set_page_config(
    page_title="Fase 1: Análisis Forense",
    page_icon="🔎"
)

st.title("Fase 1: El Análisis Forense 🔎")

st.header("La Metáfora: La Caverna de Platón")
st.info(
    """
    "Su misión en el 'análisis forense' de hoy es identificar las sombras que el museo proyecta. 
    Pero, sobre todo, intenten imaginar: ¿cuál es el 'sol' de la verdad que se encuentra 
    fuera de la caverna del museo y que no nos están dejando ver?".
    """
)
st.markdown("---")

st.header("Tu Misión Práctica")
st.write(
    """
    **1. Actividad Manual:** Visita (física o virtualmente) el museo asignado. 
    Tu misión es rescatar **un solo objeto** que funcione como una metáfora del arte. 
    Toma una única fotografía de tu "artefacto rescatado".
    
    **2. Actividad Digital:** Sube tu fotografía y responde la pregunta de reflexión.
    """
)

# Componente para subir la foto
foto_artefacto = st.file_uploader(
    "Sube aquí la foto de tu artefacto rescatado:", 
    type=['jpg', 'png', 'jpeg']
)

if foto_artefacto is not None:
    st.image(foto_artefacto, caption="Tu artefacto rescatado.", use_container_width=True)

# Componente para la reflexión
st.subheader("Reflexión del Curador")
reflexion = st.text_area(
    "Basado en la metáfora de la caverna, ¿cuál es el 'sol' de la verdad que tu artefacto te ayudó a imaginar?"
)

if reflexion:
    st.success("¡Tu reflexión ha sido guardada en la bitácora de esta sesión!")
