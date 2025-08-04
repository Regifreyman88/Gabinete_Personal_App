import streamlit as st

st.set_page_config(
    page_title="Curadores del Futuro",
    page_icon="🏛️",
    layout="wide"
)

st.title("🏛️ Curadores del Futuro: El Juego")

# --- LÍNEA AÑADIDA PARA MOSTRAR LA PORTADA ---
# Asegúrate de que tu imagen se llame 'portada_gabinete.jpg' en tu repositorio.
st.image("portada_gabinete.jpg")

st.header("Tu Misión: De la Idea a la Exposición")

st.write(
    """
    Bienvenido/a a tu **Bitácora de Curador**. Este no es un juego pasivo, es un taller interactivo 
    que te guiará en un viaje creativo. Tu misión es diseñar, prototipar y, finalmente, 
    colaborar en una exposición colectiva,
