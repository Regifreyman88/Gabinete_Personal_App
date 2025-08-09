import sys
from pathlib import Path
import streamlit as st

# --- Bootstrap para reutilizar backend/funciones del hub (app.py) ---
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app import DATA_DIR, save_media  # type: ignore

st.set_page_config(page_title="Fase 3: El Prototipo", page_icon="📦")

# ---------- Estado de borrador compartido ----------
if "draft" not in st.session_state:
    st.session_state.draft = {
        # Fase 1
        "image_urls": [],
        "reflection_q1": "",
        # Fase 2
        "tipo_espejo": "",
        "metafora_central": "",
        "salas_principales": "",
        "artefacto_central": "",
        # Fase 3
        "reflection_q2": "",  # aquí guardaremos el pitch
    }
draft = st.session_state.draft

# ---------- UI ----------
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
    **1.**
