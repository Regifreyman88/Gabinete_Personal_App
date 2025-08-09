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
        student_name = cols[0].text_input("Nombre completo *")
        email = cols[1].text_input("Email *")
        group = cols[2].selectbox("Grupo", ["Grupo A", "Grupo B", "Grupo C", "Otro"])

        st.markdown("---")
        # Obra
        st.subheader("2) Obra / Arte-objeto")
        artifact_title = st.text_input("Título de la obra *")
        artifact_desc = st.text_area("Descripción breve *", help="Materiales, intención, metáfora central, salas…")
        tags = st.text_input("Etiquetas (separadas por coma)", placeholder="identidad, memoria, ecofeminismo")

        st.markdown("---")
        # Imágenes
        st.subheader("3) Imágenes")
        images = st.file_uploader(
            "Sube 1-6 imágenes (JPG/PNG)", type=["jpg", "jpeg", "png"], accept_multiple_files=True
        )
        if images and len(images) > 6:
            st.warning("El límite recomendado es 6 imágenes; se guardarán solo las 6 primeras.")
            images = images[:6]

        st.markdown("---")
        # Reflexiones (puedes mapear con lo guardado en pages/)
        st.subheader("4) Reflexiones")
        # prefill desde borrador si existe
        draft = st.session_state.get("draft", {})
        reflection_q1 = st.text_area(
            "Q1 · ¿Qué representa tu arte-objeto de ti que no se ve a simple vista?",
            value=draft.get("reflection_q1", "")
        )
        reflection_q2 = st.text_area(
            "Q2 · Pitch/Prototipo: ¿por qué merece existir y qué debería sentir el visitante?",
            value=draft.get("reflection_q2", "")
        )
        reflection_q3 = st.text_area(
            "Q3 · Concepto curatorial (hilo común/rizoma con otros):",
            value=draft.get("reflection_q3", "")
        )

        st.markdown("---")
        # Audio / Suno
        st.subheader("5) Audio / Canción")
        audio_file = st.file_uploader(
            "Sube tu audio (MP3/WAV/M4A)", type=["mp3", "wav", "m4a"], accept_multiple_files=False
        )
        suno_link = st.text_input("o pega el enlace público de tu pista en Suno (opcional)")

        submitted = st.form_submit_button("Publicar mi gabinete")

    if submitted:
        missing = [("Nombre", student_name), ("Email", email), ("Título", artifact_title), ("Descripción", artifact_desc)]
        missing_fields = [m for m, v in missing if not v]
        if missing_fields:
            st.error("Faltan campos obligatorios: " + ", ".join(missing_fields))
        else:
            # Guardar media
            img_urls = save_media(images, kind="image") if images else []
            aud_urls = save_media([audio_file], kind="audio") if audio_file else []

            with Session(engine) as session:
                entry = Entry(
                    student_name=student_name.strip(),
                    email=email.strip(),
                    group=group,
                    artifact_title=artifact_title.strip(),
                    artifact_desc=artifact_desc.strip(),
                    tags=tags.strip(),
                    reflection_q1=(reflection_q1 or "").strip(),
                    reflection_q2=(reflection_q2 or "").strip(),
                    reflection_q3=(reflection_q3 or "").strip(),
                    image_urls="||".join(img_urls),
                    audio_url=aud_urls[0] if aud_urls else "",
                    suno_link=(suno_link or "").strip(),
                )
                session.add(entry)
                session.commit()
            st.success("¡Tu gabinete ha sido publicado!")

# -------------
# Página: Galería
# -------------
if page == "Galería":
    st.title("Galería de Gabinetes")

    colf = st.columns([1, 1, 2])
    group_f = colf[0].selectbox("Grupo", ["Todos", "Grupo A", "Grupo B", "Grupo C", "Otro"])
    search = colf[1].text_input("Buscar", placeholder="título, nombre, etiqueta…")
    tag_f = colf[2].text_input("Filtrar por etiqueta específica (exacta)")

    with Session(engine) as session:
        stmt = select(Entry).order_by(Entry.created_at.desc())
        entries = list(session.exec(stmt))

    def match(e: Entry) -> bool:
        if group_f != "Todos" and e.group != group_f:
            return False
        if search:
            s = search.lower()
            blob = " ".join([
                e.student_name, e.email, e.group, e.artifact_title, e.artifact_desc, e.tags,
                e.reflection_q1, e.reflection_q2, e.reflection_q3
            ]).lower()
            if s not in blob:
                return False
        if tag_f:
            tags_list = parse_tags(e.tags)
            if tag_f.strip() not in tags_list:
                return False
        return True

    filtered = [e for e in entries if match(e)]
    st.caption(f"Mostrando {len(filtered)} de {len(entries)} gabinetes")

    # Grid de tarjetas
    st.markdown('<div class="grid cols-3">', unsafe_allow_html=True)
    for e in filtered:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        # portada: primera imagen
        img_urls = [u for u in e.image_urls.split("||") if u]
        if img_urls:
            first = DATA_DIR / img_urls[0]
            if first.exists():
                st.markdown(f"<img class='thumb' src='{first.as_posix()}' />", unsafe_allow_html=True)

        st.markdown(f"<h3>{e.artifact_title}</h3>", unsafe_allow_html=True)
        st.markdown(f"<div class='meta'>Por {e.student_name} — {e.group}</div>", unsafe_allow_html=True)
        st.write(e.artifact_desc)

        tags_list = parse_tags(e.tags)
        if tags_list:
            st.markdown(" ".join([f"<span class='badge'>{t}</span>" for t in tags_list]), unsafe_allow_html=True)

        # Audio/Suno
        if e.audio_url:
            ap = DATA_DIR / e.audio_url
            if ap.exists():
                with open(ap, "rb") as f:
                    st.audio(f.read())
        if e.suno_link:
            st.link_button("Escuchar en Suno", e.suno_link)

        with st.expander("Reflexiones"):
            st.markdown(f"**Q1** {e.reflection_q1 or '—'}")
            st.markdown(f"**Q2** {e.reflection_q2 or '—'}")
            st.markdown(f"**Q3** {e.reflection_q3 or '—'}")

        st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ----------------
# Página: Docente
# ----------------
if page == "Panel docente":
    st.title("Panel docente")
    key = st.text_input("Clave docente", type="password")
    if key != ADMIN_KEY:
        st.info("Introduce la clave docente para ver y exportar datos.")
        st.stop()

    from zipfile import ZipFile, ZIP_DEFLATED
    import csv
    import pandas as pd

    with Session(engine) as session:
        entries = list(session.exec(select(Entry).order_by(Entry.created_at.desc())))

    st.subheader("Resumen")
    cols = st.columns(4)
    cols[0].metric("Total gabinetes", len(entries))
    cols[1].metric("Con audio", sum(1 for e in entries if e.audio_url or e.suno_link))
    cols[2].metric(">2 imágenes", sum(1 for e in entries if len([u for u in e.image_urls.split('||') if u]) > 2))
    groups = {}
    for e in entries:
        groups[e.group] = groups.get(e.group, 0) + 1
    cols[3].metric("Grupos", len(groups))

    st.markdown("---")
    st.subheader("Exportar datos")

    # CSV
    csv_buf = io.StringIO()
    writer = csv.writer(csv_buf)
    writer.writerow([
        "id","created_at","student_name","email","group","artifact_title","artifact_desc",
        "tags","reflection_q1","reflection_q2","reflection_q3","image_urls","audio_url","suno_link",
    ])
    for e in entries:
        writer.writerow([
            e.id, e.created_at.isoformat(), e.student_name, e.email, e.group, e.artifact_title, e.artifact_desc,
            e.tags, e.reflection_q1, e.reflection_q2, e.reflection_q3, e.image_urls, e.audio_url, e.suno_link,
        ])
    csv_bytes = csv_buf.getvalue().encode("utf-8")
    st.download_button("Descargar CSV", data=csv_bytes, file_name="gabinetes.csv", mime="text/csv")

    # ZIP (CSV + media)
    zip_buf = io.BytesIO()
    with ZipFile(zip_buf, "w", ZIP_DEFLATED) as zf:
        zf.writestr("gabinetes.csv", csv_bytes)
        for e in entries:
            for u in [u for u in e.image_urls.split("||") if u]:
                p = DATA_DIR / u
                if p.exists():
                    zf.write(p, arcname=str(Path("media") / u))
            if e.audio_url:
                ap = DATA_DIR / e.audio_url
                if ap.exists():
                    zf.write(ap, arcname=str(Path("media") / e.audio_url))
    st.download_button("Descargar ZIP (CSV + media)", data=zip_buf.getvalue(),
                       file_name="gabinetes_media.zip", mime="application/zip")

    st.markdown("---")
    st.subheader("Vista de tabla")
    df = pd.DataFrame([
        {
            "ID": e.id,
            "Creado": e.created_at.strftime("%Y-%m-%d %H:%M"),
            "Nombre": e.student_name,
            "Email": e.email,
            "Grupo": e.group,
            "Título": e.artifact_title,
            "Etiquetas": e.tags,
            "#Imágenes": len([u for u in e.image_urls.split("||") if u]),
            "Audio?": bool(e.audio_url or e.suno_link),
        }
        for e in entries
    ])
    st.dataframe(df, use_container_width=True)

# -------------
# Pie
# -------------
st.markdown("---")
st.caption("Hecho con ❤️ por el Gabinete del Asombro · Streamlit + SQLite")
