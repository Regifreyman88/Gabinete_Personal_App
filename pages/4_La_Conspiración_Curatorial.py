import sys
from pathlib import Path
import streamlit as st

# --- Bootstrap para reutilizar backend/DB del hub (app.py) ---
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app import DATA_DIR, Entry, engine, Session, save_media  # type: ignore
from sqlmodel import select

st.set_page_config(page_title="Fase 4: Conspiración Curatorial", page_icon="🌿")

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
        "reflection_q2": "",
        # Fase 4
        "reflection_q3": "",         # concepto curatorial
        "invitation_copy": "",        # texto de invitación
        "hashtags": "",               # #etiquetas para redes
        "team_name": "",              # nombre del equipo/curaduría
        "team_image_urls": [],        # imagen del mapa rizomático u organización
    }
draft = st.session_state.draft

# ---------- UI ----------
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
    Usen post-its o hilos para mapear las *conexiones rizomáticas*: temas comunes, 
    contrastes estéticos, diálogos narrativos.

    **2. Actividad Digital:** Usen la galería de abajo como referencia y trabajen 
    juntos el **concepto curatorial**, la **invitación** y los **hashtags**.
    """
)

# =========================
# Galería de gabinetes (DB)
# =========================
st.subheader("Galería de Gabinetes (referencia)")
colf1, colf2 = st.columns([1, 1])
with colf1:
    filtro_grupo = st.selectbox("Filtrar por grupo", ["Todos", "Grupo A", "Grupo B", "Grupo C", "Otro"])
with colf2:
    buscar = st.text_input("Buscar (título/nombre/etiqueta)", "")

with Session(engine) as session:
    stmt = select(Entry).order_by(Entry.created_at.desc())
    entries = list(session.exec(stmt))

def match(e: Entry) -> bool:
    if filtro_grupo != "Todos" and e.group != filtro_grupo:
        return False
    if buscar:
        s = buscar.lower()
        blob = " ".join([
            e.student_name, e.email, e.group, e.artifact_ti
