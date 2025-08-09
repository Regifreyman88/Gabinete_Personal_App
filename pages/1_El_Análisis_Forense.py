import sys
from pathlib import Path
import streamlit as st

# --- Bootstrap para reutilizar backend y utilidades de app.py ---
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Reutilizamos las utilidades del hub principal
from app import DATA_DIR, save_media  # type: ignore

st.set_page_config(page_title="Fase 1: Análisis Forense", page_icon="🔎")

# ---------- Estado de borrador compartido ----------
if "draft" not in st.session_state:
    st.session_state.draft = {
        "image_urls": [],       # aquí iremos acumulando imágenes guardadas
        "reflection_q1": "",    # respuesta de esta fase
    }
draft = st.session_state.draft

# ---------- UI ----------
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

# --- Subida de imagen (no se guarda hasta que des clic en "G
