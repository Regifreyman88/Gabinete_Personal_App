# ================================
# Gabinete Personal — app.py (sqlite3 + assets/)
# ================================
from __future__ import annotations
import io, csv, sqlite3
from zipfile import ZipFile, ZIP_DEFLATED
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

import streamlit as st
from PIL import Image
import pandas as pd

# ---------------- Config ----------------
APP_TITLE = "Gabinete Personal – Metodologías del Pensamiento Creativo"
APP_DESCRIPTION = (
    "Captura tu arte-objeto, reflexiona, sube imágenes y audio/Suno y comparte tu gabinete en la galería."
)
st.set_page_config(page_title=APP_TITLE, layout="wide")

BASE_DIR   = Path(__file__).parent
DATA_DIR   = BASE_DIR / "data"
DB_PATH    = DATA_DIR / "gabinete.db"
UPLOADS    = DATA_DIR / "uploads"
IMG_DIR    = UPLOADS / "images"
AUDIO_DIR  = UPLOADS / "audio"
ASSETS_DIR = BASE_DIR / "assets"   # <- coloca aquí hero y banners

for p in [DATA_DIR, UPLOADS, IMG_DIR, AUDIO_DIR]:
    p.mkdir(parents=True, exist_ok=True)

ADMIN_KEY = st.secrets.get("ADMIN_KEY", "regina-demo")

# --------------- Utilidades de imágenes ---------------
def img(path_rel: str):
    """Muestra una imagen de assets/ si existe, sin romper la app si falta."""
    p = ASSETS_DIR / path_rel
    if p.exists():
        st.image(str(p), use_container_width=True)
    else:
        st.warning(f"Falta la imagen: assets/{path_rel}")

# --------------- DB (sqlite3) ---------------
SCHEMA = """
CREATE TABLE IF NOT EXISTS entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TEXT NOT NULL,
    student_name TEXT NOT NULL,
    email TEXT NOT NULL,
    grp TEXT NOT NULL,
    artifact_title TEXT NOT NULL,
    artifact_desc TEXT NOT NULL,
    tags TEXT DEFAULT '',
    reflection_q1 TEXT DEFAULT '',
    reflection_q2 TEXT DEFAULT '',
    reflection_q3 TEXT DEFAULT '',
    image_urls TEXT DEFAULT '',
    audio_url TEXT DEFAULT '',
    suno_link TEXT DEFAULT ''
);
"""
def db():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    return con

with db() as con:
    con.executescript(SCHEMA)

def insert_entry(row: Dict[str, Any]) -> None:
    with db() as con:
        con.execute(
            """INSERT INTO entries
            (created_at, student_name, email, grp, artifact_title, artifact_desc, tags,
             reflection_q1, reflection_q2, reflection_q3, image_urls, audio_url, suno_link)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                datetime.utcnow().isoformat(),
                row["student_name"], row["email"], row["group"],
                row["artifact_title"], row["artifact_desc"], row.get("tags",""),
                row.get("reflection_q1",""), row.get("reflection_q2",""), row.get("reflection_q3",""),
                row.get("image_urls",""), row.get("audio_url",""), row.get("suno_link",""),
            )
        )
        con.commit()

def fetch_entries() -> List[sqlite3.Row]:
    with db() as con:
        cur = con.execute("SELECT * FROM entries ORDER BY datetime(created_at) DESC")
        return cur.fetchall()

# --------------- Guardado de media ---------------
def save_image(file) -> str:
    img = Image.open(file).convert("RGB")
    fname = f"img_{datetime.utcnow().strftime('%Y%m%d_%H%M%S_%f')}.jpg"
    out = IMG_DIR / fname
    img.save(out, "JPEG", quality=92)
    return str(out.relative_to(DATA_DIR))

def save_audio(file) -> str:
    suffix = Path(file.name).suffix.lower() or ".mp3"
    fname = f"aud_{datetime.utcnow().strftime('%Y%m%d_%H%M%S_%f')}{suffix}"
    out = AUDIO_DIR / fname
    out.write_bytes(file.read())
    return str(out.relative_to(DATA_DIR))

def parse_tags(s: str) -> List[str]:
    return [t.strip() for t in (s or "").split(",") if t.strip()]

# --------------- Estilos ---------------
st.markdown("""
<style>
.block-container{padding-top:1.1rem}
.card{border-radius:18px;padding:14px;background:#fff;
      box-shadow:0 10px 24px rgba(0,0,0,.08);transition:.15s}
.card:hover{transform:translateY(-2px);box-shadow:0 16px 28px rgba(0,0,0,.12)}
.badge{display:inline-block;padding:.25rem .6rem;border-radius:999px;background:#EFEAFF;margin-right:.35rem;font-size:.8rem;color:#5531ff}
.meta{opacity:.8;font-size:.9rem}
.grid{display:grid;gap:1rem}
.grid.cols-3{grid-template-columns:repeat(3,minmax(0,1fr))}
.thumb{border-radius:14px;overflow:hidden;margin-bottom:10px;aspect-ratio:16/10;width:100%;object-fit:cover}
@media (max-width:1100px){.grid.cols-3{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:800px){.grid.cols-3{grid-template-columns:1fr}}
</style>
""", unsafe_allow_html=True)

# --------------- Navegación ---------------
st.sidebar.title("Gabinete Personal")
st.sidebar.write(APP_DESCRIPTION)
page = st.sidebar.radio(
    "Ir a",
    ["Inicio",
     "Fase 1 · Análisis Forense",
     "Fase 2 · Arquitectura Conceptual",
     "Fase 3 · Prototipo",
     "Fase 4 · Conspiración Curatorial",
     "Crear mi gabinete",
     "Galería",
     "Panel docente"]
)

# --------------- Páginas ---------------
if page == "Inicio":
    img("hero.jpg")  # assets/hero.jpg
    st.title(APP_TITLE)
    st.write(APP_DESCRIPTION)
    c1, c2 = st.columns(2)
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
        st.markdown(
            "**Tips**\n"
            "- Usa etiquetas para agrupar.\n"
            "- Cuida iluminación y foco.\n"
            "- El audio puede ser voz o Suno."
        )

if page == "Fase 1 · Análisis Forense":
    st.title("Fase 1: El Análisis Forense 🔎")
    img("banner_fase1.jpg")
    st.header("La Metáfora: La Caverna de Platón")
    st.info(
        "“Su misión en el análisis forense de hoy es identificar las sombras que el museo proyecta. "
        "Pero, sobre todo, intenten imaginar: ¿cuál es el ‘sol’ de la verdad que se encuentra fuera de la caverna del museo y que no nos están dejando ver?”"
    )
    st.markdown("---")
    st.header("Tu Misión Práctica")
    st.write(
        "**1. Actividad Manual:** Visita el museo (físico o virtual) y rescata **un solo objeto** como metáfora del arte. "
        "Toma una fotografía de tu artefacto.\n\n"
        "**2. Actividad Digital:** Sube tu fotografía y responde la pregunta de reflexión."
    )
    foto = st.file_uploader("Sube tu artefacto rescatado (JPG/PNG):", type=["jpg","jpeg","png"])
    if foto: st.image(foto, caption="Previsualización — Artefacto", use_container_width=True)
    st.subheader("Reflexión")
    st.text_area("¿Cuál es ese ‘sol’ de la verdad que tu artefacto te sugiere?")

if page == "Fase 2 · Arquitectura Conceptual":
    st.title("Fase 2: La Arquitectura Conceptual 📐")
    img("banner_fase2.jpg")
    st.header("La Metáfora: EL ESPEJO")
    st.info(
        "Giramos la lente hacia adentro: el gabinete no es ventana, es espejo."
    )
    st.markdown("---")
    st.subheader("Ficha arquitectónica")
    tipo = st.radio("¿Qué tipo de gabinete será el tuyo?",
                    ["Verdad cruda", "Embellece la realidad", "Muestra el potencial"])
    meta = st.text_input("Metáfora central (nombre secreto):")
    salas = st.text_area("Salas principales (3–5):")
    arte = st.text_input("Artefacto central:")
    if st.button("Guardar (local) – Fase 2"):
        st.success("Guardado en esta sesión.")

if page == "Fase 3 · Prototipo":
    st.title("Fase 3: El Prototipo 📦")
    img("banner_fase3.jpg")
    st.header("La Metáfora: EL SECRETO")
    st.info("Un pitch es revelación controlada: qué muestras y qué reservas.")
    st.markdown("---")
    foto_p = st.file_uploader("Foto del prototipo (JPG/PNG):", type=["jpg","jpeg","png"])
    if foto_p: st.image(foto_p, caption="Previsualización — Prototipo", use_container_width=True)
    st.text_area("Pitch (máx. ~3 min de lectura):")

if page == "Fase 4 · Conspiración Curatorial":
    st.title("Fase 4: La Conspiración Curatorial 🌿")
    img("banner_fase4.jpg")
    st.header("La Metáfora: EL RIZOMA")
    st.info("Conecta tu gabinete con el de otros: temas, contrastes, diálogos.")
    st.markdown("---")
    team = st.text_input("Nombre del equipo/curaduría")
    concepto = st.text_area("Concepto curatorial (200–300 palabras):", height=180)
    invitacion = st.text_area("Invitación (corta y clara):", height=140)
    if st.button("Guardar (local) – Fase 4"):
        st.success("Guardado en esta sesión.")

if page == "Crear mi gabinete":
    st.title("Crear / Editar mi Gabinete")
    with st.form("gabinete_form", clear_on_submit=False):
        st.subheader("1) Perfil del estudiante")
        c = st.columns(3)
        student_name = c[0].text_input("Nombre completo *")
        email        = c[1].text_input("Email *")
        group        = c[2].selectbox("Grupo", ["Grupo A","Grupo B","Grupo C","Otro"])

        st.markdown("---")
        st.subheader("2) Obra / Arte-objeto")
        artifact_title = st.text_input("Título de la obra *")
        artifact_desc  = st.text_area("Descripción breve *",
            help="Materiales, intención, metáfora central, salas…")
        tags = st.text_input("Etiquetas (coma)", placeholder="identidad, memoria, ecofeminismo")

        st.markdown("---")
        st.subheader("3) Imágenes")
        imgs = st.file_uploader("Sube 1–6 imágenes", type=["jpg","jpeg","png"], accept_multiple_files=True)
        if imgs and len(imgs) > 6:
            st.warning("Se guardarán solo las 6 primeras."); imgs = imgs[:6]

        st.markdown("---")
        st.subheader("4) Reflexiones")
        q1 = st.text_area("Q1 · ¿Qué de ti representa tu arte-objeto?")
        q2 = st.text_area("Q2 · ¿Por qué merece existir y qué debería sentir el visitante?")
        q3 = st.text_area("Q3 · Concepto curatorial / rizoma:")

        st.markdown("---")
        st.subheader("5) Audio / Canción")
        aud = st.file_uploader("Audio (MP3/WAV/M4A)", type=["mp3","wav","m4a"])
        suno = st.text_input("o enlace público de Suno (opcional)")

        submit = st.form_submit_button("Publicar mi gabinete")

    if submit:
        faltan = [("Nombre", student_name), ("Email", email), ("Título", artifact_title), ("Descripción", artifact_desc)]
        miss = [n for n,v in faltan if not v]
        if miss:
            st.error("Faltan: " + ", ".join(miss))
        else:
            img_urls = [save_image(f) for f in (imgs or [])]
            aud_url  = save_audio(aud) if aud else ""
            row = {
                "student_name": student_name.strip(),
                "email": email.strip(),
                "group": group,
                "artifact_title": artifact_title.strip(),
                "artifact_desc": artifact_desc.strip(),
                "tags": (tags or "").strip(),
                "reflection_q1": (q1 or "").strip(),
                "reflection_q2": (q2 or "").strip(),
                "reflection_q3": (q3 or "").strip(),
                "image_urls": "||".join(img_urls),
                "audio_url": aud_url,
                "suno_link": (suno or "").strip(),
            }
            insert_entry(row)
            st.success("¡Tu gabinete ha sido publicado!")

if page == "Galería":
    st.title("Galería de Gabinetes")
    c0 = st.columns([1,1,2])
    f_group = c0[0].selectbox("Grupo", ["Todos","Grupo A","Grupo B","Grupo C","Otro"])
    f_search= c0[1].text_input("Buscar", placeholder="título, nombre, etiqueta…")
    f_tag   = c0[2].text_input("Etiqueta exacta")

    entries = fetch_entries()

    def match(e: sqlite3.Row) -> bool:
        if f_group != "Todos" and e["grp"] != f_group: return False
        if f_search:
            s = f_search.lower()
            blob = " ".join([
                e["student_name"], e["email"], e["grp"], e["artifact_title"],
                e["artifact_desc"], e["tags"], e["reflection_q1"], e["reflection_q2"], e["reflection_q3"]
            ]).lower()
            if s not in blob: return False
        if f_tag and f_tag.strip() not in parse_tags(e["tags"]): return False
        return True

    filt = [e for e in entries if match(e)]
    st.caption(f"Mostrando {len(filt)} de {len(entries)} gabinetes")

    st.markdown('<div class="grid cols-3">', unsafe_allow_html=True)
    for e in filt:
        st.markdown('<div class="card">', unsafe_allow_html=True)

        imgs = [u for u in (e["image_urls"] or "").split("||") if u]
        if imgs:
            first = DATA_DIR / imgs[0]
            if first.exists():
                st.markdown(f"<img class='thumb' src='{first.as_posix()}' />", unsafe_allow_html=True)

        st.markdown(f"<h3>{e['artifact_title']}</h3>", unsafe_allow_html=True)
        st.markdown(f"<div class='meta'>Por {e['student_name']} — {e['grp']}</div>", unsafe_allow_html=True)
        st.write(e["artifact_desc"])

        tags = parse_tags(e["tags"])
        if tags:
            st.markdown(" ".join([f"<span class='badge'>{t}</span>" for t in tags]), unsafe_allow_html=True)

        if e["audio_url"]:
            ap = DATA_DIR / e["audio_url"]
            if ap.exists(): st.audio(ap.read_bytes())
        if e["suno_link"]:
            st.link_button("Escuchar en Suno", e["suno_link"])

        with st.expander("Reflexiones"):
            st.markdown(f"**Q1** {e['reflection_q1'] or '—'}")
            st.markdown(f"**Q2** {e['reflection_q2'] or '—'}")
            st.markdown(f"**Q3** {e['reflection_q3'] or '—'}")

        st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

if page == "Panel docente":
    st.title("Panel docente")
    key = st.text_input("Clave docente", type="password")
    if key != ADMIN_KEY:
        st.info("Introduce la clave docente para ver y exportar datos.")
        st.stop()

    entries = fetch_entries()
    c = st.columns(4)
    c[0].metric("Total gabinetes", len(entries))
    c[1].metric("Con audio", sum(1 for e in entries if (e["audio_url"] or e["suno_link"])))
    c[2].metric(">2 imágenes", sum(1 for e in entries if len([u for u in (e["image_urls"] or '').split('||') if u]) > 2))
    grupos = {}
    for e in entries: grupos[e["grp"]] = grupos.get(e["grp"], 0) + 1
    c[3].metric("Grupos", len(grupos))

    st.markdown("---")
    st.subheader("Exportar")

    # CSV
    csv_buf = io.StringIO()
    w = csv.writer(csv_buf)
    w.writerow(["id","created_at","student_name","email","group","artifact_title","artifact_desc",
                "tags","reflection_q1","reflection_q2","reflection_q3","image_urls","audio_url","suno_link"])
    for e in entries:
        w.writerow([e["id"], e["created_at"], e["student_name"], e["email"], e["grp"], e["artifact_title"],
                    e["artifact_desc"], e["tags"], e["reflection_q1"], e["reflection_q2"], e["reflection_q3"],
                    e["image_urls"], e["audio_url"], e["suno_link"]])
    st.download_button("Descargar CSV", data=csv_buf.getvalue().encode("utf-8"),
                       file_name="gabinetes.csv", mime="text/csv")

    # ZIP (CSV + media)
    zip_buf = io.BytesIO()
    with ZipFile(zip_buf, "w", ZIP_DEFLATED) as zf:
        zf.writestr("gabinetes.csv", csv_buf.getvalue().encode("utf-8"))
        for e in entries:
            for u in [u for u in (e["image_urls"] or "").split("||") if u]:
                p = DATA_DIR / u
                if p.exists(): zf.write(p, arcname=str(Path("media") / u))
            if e["audio_url"]:
                ap = DATA_DIR / e["audio_url"]
                if ap.exists(): zf.write(ap, arcname=str(Path("media") / e["audio_url"]))
    st.download_button("Descargar ZIP (CSV + media)", data=zip_buf.getvalue(),
                       file_name="gabinetes_media.zip", mime="application/zip")

# --------------- Pie ---------------
st.markdown("---")
st.caption("Hecho con ❤️ por el Gabinete del Asombro · Streamlit + SQLite (sqlite3)")
