# ================================
# Gabinete Personal – app.py (completo)
# ================================
# Autor: para Regina A. Freyman
# App todo-en-uno: captura, curaduría y exhibición (texto, imágenes y audio)
# Backend local: SQLite + sistema de archivos. En Cloud, migrar media a un bucket.
# ================================

from __future__ import annotations
import io
import os
from pathlib import Path
from datetime import datetime
from typing import List, Optional

import streamlit as st
from PIL import Image
from sqlmodel import Field, SQLModel, Session, create_engine, select

# ----------------
# Config general
# ----------------
APP_TITLE = "Gabinete Personal – Metodologías del Pensamiento Creativo"
APP_DESCRIPTION = (
    "Captura tu arte-objeto, reflexiona, sube imágenes y audio/Suno y comparte tu gabinete en la galería."
)
st.set_page_config(page_title=APP_TITLE, layout="wide")

# ----------------
# Rutas y assets
# ----------------
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "gabinete.db"
UPLOADS_DIR = DATA_DIR / "uploads"
IMG_DIR = UPLOADS_DIR / "images"
AUDIO_DIR = UPLOADS_DIR / "audio"
ASSETS_DIR = BASE_DIR / "assets"  # <- tus banners/hero

for p in [DATA_DIR, UPLOADS_DIR, IMG_DIR, AUDIO_DIR]:
    p.mkdir(parents=True, exist_ok=True)

def show_img(rel_path: str):
    """Muestra una imagen desde /assets si existe (sin crashear si falta)."""
    p = ASSETS_DIR / rel_path
    if p.exists():
        st.image(str(p), use_container_width=True)

# ----------------
# Media backend
# ----------------
MEDIA_BACKEND = st.secrets.get("MEDIA_BACKEND", "local")  # "local" o "external"
ADMIN_KEY = st.secrets.get("ADMIN_KEY", "regina-demo")

# ----------------
# Modelo de datos
# ----------------
class Entry(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Perfil
    student_name: str
    email: str
    group: str = Field(default="Grupo A")

    # Obra y metadatos
    artifact_title: str
    artifact_desc: str
    tags: str = Field(default="")  # coma separada

    # Reflexiones
    reflection_q1: str = Field(default="")
    reflection_q2: str = Field(default="")
    reflection_q3: str = Field(default="")

    # Media
    image_urls: str = Field(default="")  # separadas por "||"
    audio_url: str = Field(default="")
    suno_link: str = Field(default="")

engine = create_engine(f"sqlite:///{DB_PATH}")
SQLModel.metadata.create_all(engine)

# ----------------
# Utilidades media
# ----------------
def save_image_locally(file) -> str:
    img = Image.open(file).convert("RGB")
    fname = f"img_{datetime.utcnow().strftime('%Y%m%d_%H%M%S_%f')}.jpg"
    out_path = IMG_DIR / fname
    img.save(out_path, format="JPEG", quality=92)
    return str(out_path.relative_to(DATA_DIR))

def save_audio_locally(file) -> str:
    suffix = Path(file.name).suffix.lower() or ".mp3"
    fname = f"aud_{datetime.utcnow().strftime('%Y%m%d_%H%M%S_%f')}{suffix}"
    out_path = AUDIO_DIR / fname
    with open(out_path, "wb") as f:
        f.write(file.read())
    return str(out_path.relative_to(DATA_DIR))

def upload_external(file, kind: str) -> str:
    raise NotImplementedError("Configura un bucket (Supabase/S3/Cloudinary) si usas MEDIA_BACKEND='external'.")

def save_media(files: List, kind: str) -> List[str]:
    """Guarda imágenes o audio y devuelve lista de rutas/URLs."""
    urls = []
    if not files:
        return urls
    for f in files:
        if MEDIA_BACKEND == "local":
            rel = save_image_locally(f) if kind == "image" else save_audio_locally(f)
            urls.append(rel)  # ruta relativa dentro de DATA_DIR
        else:
            urls.append(upload_external(f, kind))
    return urls

def parse_tags(tags_str: str) -> List[str]:
    return [t.strip() for t in tags_str.split(",") if t.strip()]

# ----------------
# Estilos (CSS)
# ----------------
CUSTOM_CSS = """
<style>
.block-container {padding-top: 1.2rem;}
.card {
  border-radius: 18px; padding: 14px;
  box-shadow: 0 10px 24px rgba(0,0,0,0.08);
  transition: transform .15s ease, box-shadow .15s ease;
  background: #fff;
}
.card:hover { transform: translateY(-2px); box-shadow: 0 16px 28px rgba(0,0,0,0.12); }
.card h3 { margin: 6px 0 4px 0; }
.badge {display:inline-block; padding:.25rem .6rem; border-radius:999px; background:#EFEAFF; margin-right:.35rem; font-size:.8rem; color:#5531ff}
.meta {opacity:.8; font-size:.9rem}
.grid {display:grid; gap:1rem}
.grid.cols-3 {grid-template-columns: repeat(3, minmax(0, 1fr));}
.grid.cols-4 {grid-template-columns: repeat(4, minmax(0, 1fr));}
.thumb {border-radius: 14px; overflow:hidden; margin-bottom:10px; aspect-ratio: 16/10; width:100%; object-fit:cover;}
@media (max-width: 1100px){ .grid.cols-4 {grid-template-columns: repeat(2, minmax(0,1fr));}}
@media (max-width: 800px){ .grid.cols-3, .grid.cols-4 {grid-template-columns: 1fr;}}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ----------------
# Sidebar / Nav
# ----------------
st.sidebar.title("Gabinete Personal")
st.sidebar.write(APP_DESCRIPTION)
page = st.sidebar.radio("Ir a", ["Inicio", "Crear mi gabinete", "Galería", "Panel docente"])

# ----------------
# Página: Inicio
# ----------------
if page == "Inicio":
    show_img("hero.jpg")
    st.title(APP_TITLE)
    st.write(APP_DESCRIPTION)

    c1, c2 = st.columns([1, 1])
    with c1:
        st.markdown(
            "**Flujo**\n"
            "1) Completa tu perfil y describe tu arte-objeto.\n"
            "2) Sube imágenes (proceso y obra final).\n"
            "3) Responde 3 preguntas de reflexión.\n"
            "4) Agrega audio o tu enlace de Suno.\n"
            "5) Publica y aparece en la galería."
        )
    with c2:
        st.markdown("**Tips**\n- Usa etiquetas para agrupar.\n- Cuida iluminación y foco.\n- El audio puede ser voz o Suno.")

# --------------------------
# Página: Crear mi gabinete
# --------------------------
if page == "Crear mi gabinete":
    st.title("Crear / Editar mi Gabinete")
    with st.form("gabinete_form", clear_on_submit=False):
        # Perfil
        st.subheader("1) Perfil del estudiante")
        cols = st.columns(3)
        student_name = cols[0].text_input("
