import sys
from pathlib import Path
import streamlit as st

# --- Bootstrap para reutilizar backend/constantes del hub (app.py) ---
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app import DATA_DIR  # type: ignore  # (no usamos DB aquí, solo estado compartido)

st.set_page_config(page_title="Fase 2: Arquitectura Conceptual", page_icon="📐")

# ---------- Estado de borrador compartido ----------
if "draft" not in st.session_state:
    st.session_state.draft = {
        # Fase 1
        "image_urls": [],
        "reflection_q1": "",
        # Fase 2
        "tipo_espejo": "",
        "m
