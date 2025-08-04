import streamlit as st

st.set_page_config(
    page_title="Fase 3: El Prototipo",
    page_icon="📦"
)

st.title("Fase 3: El Prototipo 📦")

st.header("La Metáfora: EL SECRETO")
st.info(
    """
    "Hasta ahora, su Gabinete ha sido un proyecto íntimo. Ahora deben decidir: ¿Qué parte de este mundo interior 
    revelamos al mundo exterior? ¿Y cómo lo hacemos sin que pierda su misterio y su poder? 
    Un pitch es un acto de revelación controlada."
    """
)
st.markdown("---")

st.header("Tu Misión de Prototipado")
st.write(
    """
    **1. Actividad Manual:** Construye una versión 'de baja fidelidad' de tu Gabinete. 
    Puede ser un diorama en una caja de zapatos, un collage detallado, o un objeto hecho con 
    materiales reciclados. Luego, tómale una fotografía.

    **2. Actividad Digital:** Sube la foto de tu prototipo y escribe tu 'pitch', revelando 
    la esencia de tu gabinete al mundo.
    """
)

# --- Componentes Interactivos ---

st.subheader("Documenta tu Prototipo")

# Componente para subir la foto del prototipo
foto_prototipo = st.file_uploader(
    "Sube aquí la foto de tu prototipo físico:", 
    type=['jpg', 'png', 'jpeg']
)

if foto_prototipo is not None:
    st.image(foto_prototipo, caption="Tu prototipo.", use_container_width=True)

# Componente para el pitch
st.subheader("El Pitch (La Revelación Controlada)")
pitch = st.text_area(
    "Escribe aquí tu pitch (máximo 3 minutos de lectura). Responde: ¿Por qué este Gabinete merece existir y qué debería sentir alguien al visitarlo?",
    height=250
)

if pitch:
    st.success("¡Tu pitch ha sido guardado en la bitácora de esta sesión!")
