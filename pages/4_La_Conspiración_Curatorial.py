import streamlit as st

st.set_page_config(
    page_title="Fase 4: Conspiración Curatorial",
    page_icon="🌿"
)

st.title("Fase 4: La Conspiración Curatorial 🌿")

st.header("La Metáfora: EL RIZOMA")
st.info(
    """
    "Un rizoma no tiene un centro ni una jerarquía. Es una red subterránea que conecta 
    puntos dispares. Su misión hoy es dejar de pensar como árboles individuales y 
    empezar a pensar como un rizoma: ¿cómo se conectan sus Gabinetes por debajo de la 
    superficie? ¿Qué conversaciones inesperadas surgen entre ellos?"
    """
)
st.markdown("---")

st.header("Tu Misión Colectiva")
st.write(
    """
    **1. Actividad Manual:** En equipo, observen los prototipos físicos de cada miembro. 
    Usen post-its o hilos para mapear las "conexiones rizomáticas": temas comunes, 
    contrastes estéticos, diálogos narrativos.

    **2. Actividad Digital:** Usen la galería de abajo como referencia y trabajen 
    juntos para diseñar el concepto de su exposición final y la invitación.
    """
)

# --- Galería de Prototipos ---
st.subheader("Galería de Gabinetes Personales")

# --- NOTA IMPORTANTE PARA TI (LA DOCENTE) ---
# Para la exposición, aquí es donde añadirías manualmente la información de los
# prototipos de tus alumnos después de que ellos completen la Fase 3.
# Sube sus imágenes al repositorio y llena esta lista.

prototipos = [
    {
        "autor": "Agustín",
        "imagen": "prototipo_agustin.jpg", # Reemplazar con el nombre real del archivo
        "pitch": "Mi gabinete es un espejo que refleja la verdad cruda..."
    },
    {
        "autor": "Regina",
        "imagen": "prototipo_regina.jpg", # Reemplazar con el nombre real del archivo
        "pitch": "Este gabinete explora el secreto como un acto de revelación controlada..."
    },
    # Añade aquí más diccionarios para cada alumno del equipo
]

# Mostramos la galería en columnas
if prototipos:
    cols = st.columns(len(prototipos))
    for i, prototipo in enumerate(prototipos):
        with cols[i]:
            st.image(prototipo["imagen"], caption=f"Gabinete de {prototipo['autor']}")
            with st.expander("Ver Pitch"):
                st.write(prototipo["pitch"])
else:
    st.warning("Aún no se han añadido prototipos a la galería.")


st.markdown("---")

# --- Componentes Colaborativos ---
st.subheader("Diseño de la Exposición Final")

concepto_expo = st.text_area(
    "1. Escriban aquí el concepto y el plano de su exposición final (el diálogo entre sus proyectos):",
    height=300
)

texto_invitacion = st.text_area(
    "2. Escriban aquí el texto de la invitación que atraerá a los visitantes:",
    height=200
)

if st.button("Guardar Diseño Curatorial"):
    if concepto_expo and texto_invitacion:
        st.success("¡El diseño de la exposición ha sido guardado en la bitácora de esta sesión!")
    else:
        st.warning("Por favor, completen ambos campos.")
