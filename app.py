import streamlit as st

st.set_page_config(
    page_title="Curadores del Futuro",
    page_icon="🏛️",
    layout="wide"
)

st.title("🏛️ Curadores del Futuro: El Juego")

st.markdown("---")
try:
    st.image("portada_gabinete.jpg")
except Exception:
    st.warning("Asegúrate de haber subido la imagen de portada 'portada_gabinete.jpg' a tu repositorio.")
st.markdown("---")


st.header("Tu Misión: De la Idea a la Exposición")

st.markdown(
    """
    Bienvenido/a a tu **Bitácora de Curador**. Este no es un juego pasivo, es un taller interactivo 
    que te guiará en un viaje creativo. Tu misión es diseñar, prototipar y, finalmente, 
    colaborar en una exposición colectiva, partiendo de una sola idea: tu propio 'Gabinete de Maravillas'.
    """
)

st.subheader("La Mecánica de Creación")
st.markdown("El juego combina dos mundos: el físico y el digital. En cada fase del viaje:")

col1, col2 = st.columns(2)

with col1:
    st.success(
        """
        **1. Creación Manual 👐**\n
        Primero, trabajarás con tus manos. Dibujarás, construirás y conectarás ideas 
        usando materiales reales. Aquí es donde ocurre la magia de la arteterapia.
        """
    )

with col2:
    st.info(
        """
        **2. Registro Digital 📲**\n
        Luego, volverás a esta aplicación para documentar tu creación, reflexionar 
        sobre el proceso y recibir tu siguiente misión. Esta bitácora guardará y 
        potenciará tu trabajo manual.
        """
    )

st.subheader("Las 4 Fases de tu Viaje")
st.markdown(
    """
    - **Fase 1: El Análisis Forense:** Rescatarás un artefacto y descubrirás su historia oculta.
    - **Fase 2: La Arquitectura Conceptual:** Diseñarás el 'plano' de tu gabinete personal.
    - **Fase 3: El Prototipo:** Construirás un modelo físico de tu gabinete y le darás voz.
    - **Fase 4: La Conspiración Curatorial:** Colaborarás en equipo para diseñar una exposición colectiva.
    """
)

st.header("¿Estás listo/a? Comienza tu viaje en el menú de la izquierda, en la Fase 1.")

# --- Módulo de Apoyo en la Barra Lateral ---
st.sidebar.markdown("---")
st.sidebar.header("Apoya este Proyecto")
st.sidebar.markdown(
    """
    Si te gustan estas herramientas, considera apoyar su creación y mantenimiento. 
    ¡Cada contribución ayuda a mantener vivos estos espacios creativos!
    """
)
st.sidebar.link_button("Invítame un café ☕", "https://coff.ee/regifreyman8")
