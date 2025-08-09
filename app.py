# ===========================================
# Gabinete Personal — app.py (completo, bonito, sqlite3 + assets/)
# ===========================================
from __future__ import annotations
import io, csv, sqlite3
from zipfile import ZipFile, ZIP_DEFLATED
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

import streamlit as st
from PIL import Image

# ---------------- Config ----------------
APP_TITLE = "Gabinete Personal – Metodologías del Pensamiento Creativo"
APP_DESC  = "Captura tu arte-objeto, reflexiona, sube imágenes y audio/Suno y comparte tu gabinete en la galería."
st.set_page_config(page_title=APP_TITLE, page_icon="🗝️", layout="wide")

BASE_DIR   = Path(__file__).parent
DATA_DIR   = BASE_DIR / "data"
DB_PATH    = DATA_DIR / "gabinete.db"
UPLOADS    = DATA_DIR / "uploads"
IMG_DIR    = UPLOADS / "images"
AUDIO_DIR  = UPLOADS / "audio"
ASSETS_DIR = BASE_DIR / "assets"

for p in [DATA_DIR, UPLOADS, IMG_DIR, AUDIO_DIR]:
    p.mkdir(parents=True, exist_ok=True)

# Clave para el panel docente (puedes cambiarla en Secrets si quieres)
ADMIN_KEY = st.secrets.get("ADMIN_KEY", "regina-demo")

# ---------- util imágenes ----------
def img_asset(name: str):
    """Pinta una imagen de /assets si existe y no rompe si falta."""
    p = ASSETS_DIR / name
    if p.exists():
        st.image(str(p), use_container_width=True)
    else:
        st.warning(f"Falta assets/{name}")

def parse_tags(s: str) -> list[str]:
    return [t.strip() for t in (s or "").split(",") if t.strip()]

# ---------- DB sqlite3 ----------
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
            ),
        )
        con.commit()

def fetch_entries() -> List[sqlite3.Row]:
    with db() as con:
        return con.execute(
            "SELECT * FROM entries ORDER BY datetime(created_at) DESC"
        ).fetchall()

# ---------- guardar media ----------
def save_image(file) -> str:
    image = Image.open(file).convert("RGB")
    fname = f"img_{datetime.utcnow().strftime('%Y%m%d_%H%M%S_%f')}.jpg"
    out = IMG_DIR / fname
    image.save(out, "JPEG", quality=92)
    # devolvemos la ruta relativa a DATA_DIR (para servir localmente)
    return str(out.relative_to(DATA_DIR))

def save_audio(file) -> str:
    suffix = Path(file.name).suffix.lower() or ".mp3"
    fname = f"aud_{datetime.utcnow().strftime('%Y%m%d_%H%M%S_%f')}{suffix}"
    out = AUDIO_DIR / fname
    out.write_bytes(file.read())
    return str(out.relative_to(DATA_DIR))

# ---------- estilos (bonito) ----------
st.markdown("""
<style>
.block-container{padding-top:1rem}
h1,h2,h3{letter-spacing:.2px}
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
hr{margin:1.2rem 0}
</style>
""", unsafe_allow_html=True)

# ---------- sidebar/nav ----------
st.sidebar.title("Gabinete Personal")
st.sidebar.write(APP_DESC)
page = st.sidebar.radio(
    "Ir a",
    [
        "Inicio",
        "Fase 1 · Análisis Forense",
        "Fase 2 · Arquitectura Conceptual",
        "Fase 3 · Prototipo",
        "Fase 4 · Conspiración Curatorial",
        "Crear mi gabinete",
        "Galería",
        "Panel docente",
    ],
)

# ---------- páginas ----------
if page == "Inicio":
    img_asset("hero.jpg")
    st.title(APP_TITLE)
    st.write(APP_DESC)
    c1, c2 = st.columns([1,1])
    with c1:
        st.subheader("Flujo")
        st.markdown(
            "1) Completa tu perfil y describe tu arte-objeto.\n"
            "2) Sube imágenes (proceso y obra final).\n"
            "3) Responde 3 preguntas de reflexión.\n"
            "4) Agrega audio o tu enlace de Suno.\n"
            "5) Publica y aparece en la galería."
        )
    with c2:
        st.subheader("Tips")
        st.markdown(
            "- Usa etiquetas para agrupar.\n"
            "- Cuida iluminación y foco.\n"
            "- El audio puede ser voz o Suno."
        )
    st.markdown("---")

# ----- Fase 1
if page == "Fase 1 · Análisis Forense":
    st.title("Fase 1: El Análisis Forense 🔎")
    img_asset("banner_fase1.jpg")
    st.header("La Metáfora: La Caverna de Platón")
    st.info("Identifica las sombras que el museo proyecta y, sobre todo, imagina el ‘sol’ de la verdad fuera de la caverna.")
    st.markdown("---")
    st.header("Tu Misión Práctica")
    st.write(
        "**1. Manual:** Visita un museo (físico/virtual) y rescata **un solo objeto** como metáfora del arte. "
        "Tómale una foto.\n\n"
        "**2. Digital:** Sube la foto y responde la reflexión."
    )
    f = st.file_uploader("Sube tu artefacto (JPG/PNG):", type=["jpg","jpeg","png"])
    if f: st.image(f, caption="Previsualización — Artefacto", use_container_width=True)
    st.text_area("Reflexión: ¿cuál es ese ‘sol’ sugerido por tu artefacto?")

# ----- Fase 2
if page == "Fase 2 · Arquitectura Conceptual":
    st.title("Fase 2: La Arquitectura Conceptual 📐")
    img_asset("banner_fase2.jpg")
    st.header("La Metáfora: El Espejo")
    st.info("Giramos la lente hacia adentro: el gabinete no es ventana, es espejo.")
    st.markdown("---")
    st.subheader("Ficha arquitectónica")
    tipo = st.radio("Tipo de gabinete:", ["Verdad cruda","Embellece la realidad","Muestra el potencial"])
    meta = st.text_input("Metáfora central (nombre secreto):")
    salas = st.text_area("Salas principales (3–5):")
    arte = st.text_input("Artefacto central:")
    if st.button("Guardar (local) – Fase 2"):
        st.success("✓ Guardado en esta sesión.")
    st.markdown("---")
    st.subheader("Resumen")
    st.write(f"**Tipo:** {tipo or '—'}")
    st.write(f"**Metáfora:** {meta or '—'}")
    st.write("**Salas:**"); st.write(salas or "—")
    st.write(f"**Artefacto central:** {arte or '—'}")

# ----- Fase 3
if page == "Fase 3 · Prototipo":
    st.title("Fase 3: El Prototipo 📦")
    img_asset("banner_fase3.jpg")
    st.header("La Metáfora: El Secreto")
    st.info("Un pitch es revelación controlada: qué muestras y qué reservas.")
    st.markdown("---")
    fp = st.file_uploader("Foto del prototipo (JPG/PNG):", type=["jpg","jpeg","png"])
    if fp: st.image(fp, caption="Previsualización — Prototipo", use_container_width=True)
    st.text_area("Pitch (~3 min):")

# ----- Fase 4
if page == "Fase 4 · Conspiración Curatorial":
    st.title("Fase 4: La Conspiración Curatorial 🌿")
    img_asset("banner_fase4.jpg")
    st.header("La Metáfora: El Rizoma")
    st.info("Conecta tu gabinete con el de otros: temas, contrastes, diálogos.")
    st.markdown("---")
    team = st.text_input("Nombre del equipo/curaduría")
    concepto = st.text_area("Concepto curatorial (200–300 palabras):", height=180)
    invitacion = st.text_area("Invitación (corta y clara):", height=140)
    if st.button("Guardar (local) – Fase 4"):
        st.success("✓ Guardado en esta sesión.")
    st.markdown("---")
    st.subheader("Resumen")
    st.write(f"**Equipo:** {team or '—'}")
    st.caption(concepto or "—")
    st.caption(invitacion or "—")

# ----- Crear / publicar
if page == "Crear mi gabinete":
    st.title("Crear / Editar mi Gabinete")
    with st.form("gabinete_form", clear_on_submit=False):
        st.subheader("1) Perfil")
        c = st.columns(3)
        student_name = c[0].text_input("Nombre completo *")
        email        = c[1].text_input("Email *")
        group        = c[2].selectbox("Grupo", ["Grupo A","Grupo B","Grupo C","Otro"])

        st.markdown("---")
        st.subheader("2) Obra")
        artifact_title = st.text_input("Título de la obra *")
        artifact_desc  = st.text_area("Descripción breve *", help="Materiales, intención, metáfora, salas…")
        tags           = st.text_input("Etiquetas (coma) — ej: identidad, memoria, ecofeminismo")

        st.markdown("---")
        st.subheader("3) Imágenes (1–6)")
        imgs = st.file_uploader("JPG/PNG", type=["jpg","jpeg","png"], accept_multiple_files=True)
        if imgs and len(imgs) > 6:
            st.warning("Se guardarán solo las 6 primeras."); imgs = imgs[:6]

        st.markdown("---")
        st.subheader("4) Reflexiones")
        q1 = st.text_area("Q1 · ¿Qué de ti representa tu arte-objeto?")
        q2 = st.text_area("Q2 · ¿Por qué merece existir y qué debería sentir el visitante?")
        q3 = st.text_area("Q3 · Concepto curatorial / rizoma:")

        st.markdown("---")
        st.subheader("5) Audio / Canción")
        aud  = st.file_uploader("Audio (MP3/WAV/M4A)", type=["mp3","wav","m4a"])
        suno = st.text_input("o enlace público de Suno (opcional)")

        submit = st.form_submit_button("Publicar mi gabinete")

    if submit:
        faltan = [("Nombre", student_name), ("Email", email), ("Título", artifact_title), ("Descripción", artifact_desc)]
        miss = [n for n,v in faltan if not v]
        if miss:
            st.error("Faltan: " + ", ".join(miss))
        else:
            img_urls = []
            for f in (imgs or []):
                try:
                    img_urls.append(save_image(f))
                except Exception as ex:
                    st.warning(f"No se pudo guardar una imagen: {ex}")
            aud_url = ""
            if aud:
                try:
                    aud_url = save_audio(aud)
                except Exception as ex:
                    st.warning(f"No se pudo guardar audio: {ex}")
            insert_entry({
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
            })
            st.success("¡Tu gabinete ha sido publicado!")

# ----- Galería
if page == "Galería":
    st.title("Galería de Gabinetes")
    colf = st.columns([1,1,2])
    g = colf[0].selectbox("Grupo", ["Todos","Grupo A","Grupo B","Grupo C","Otro"])
    s = colf[1].text_input("Buscar", placeholder="título, nombre, etiqueta…")
    t = colf[2].text_input("Etiqueta exacta")

    entries = fetch_entries()

    def match(e: sqlite3.Row) -> bool:
        if g != "Todos" and e["grp"] != g: return False
        if s:
            blob = " ".join([
                e["student_name"], e["email"], e["grp"], e["artifact_title"],
                e["artifact_desc"], e["tags"], e["reflection_q1"], e["reflection_q2"], e["reflection_q3"]
            ]).lower()
            if s.lower() not in blob: return False
        if t and t.strip() not in parse_tags(e["tags"]): return False
        return True

    flt = [e for e in entries if match(e)]
    st.caption(f"Mostrando {len(flt)} de {len(entries)} gabinetes")

    st.markdown('<div class="grid cols-3">', unsafe_allow_html=True)
    for e in flt:
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
            st.markdown(" ".join([f"<span class='badge'>{x}</span>" for x in tags]), unsafe_allow_html=True)

        if e["audio_url"]:
            ap = DATA_DIR / e["audio_url"]
            if ap.exists():
                st.audio(ap.read_bytes())
        if e["suno_link"]:
            st.link_button("Escuchar en Suno", e["suno_link"])

        with st.expander("Reflexiones"):
            st.markdown(f"**Q1** {e['reflection_q1'] or '—'}")
            st.markdown(f"**Q2** {e['reflection_q2'] or '—'}")
            st.markdown(f"**Q3** {e['reflection_q3'] or '—'}")

        st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ----- Panel docente
if page == "Panel docente":
    st.title("Panel docente")
    key = st.text_input("Clave docente", type="password")
    if key != ADMIN_KEY:
        st.info("Introduce la clave docente para ver/exportar datos.")
        st.stop()

    entries = fetch_entries()
    c = st.columns(4)
    c[0].metric("Total", len(entries))
    c[1].metric("Con audio", sum(1 for e in entries if (e["audio_url"] or e["suno_link"])))
    c[2].metric(">2 imágenes", sum(1 for e in entries if len([u for u in (e["image_urls"] or '').split('||') if u]) > 2))
    grupos = {}
    for e in entries: grupos[e["grp"]] = grupos.get(e["grp"], 0) + 1
    c[3].metric("Grupos", len(grupos))

    st.markdown("---")
    st.subheader("Exportar datos")

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
                if p.exists():
                    zf.write(p, arcname=str(Path("media") / u))
            if e["audio_url"]:
                ap = DATA_DIR / e["audio_url"]
                if ap.exists():
                    zf.write(ap, arcname=str(Path("media") / e["audio_url"]))
    st.download_button("Descargar ZIP (CSV + media)", data=zip_buf.getvalue(),
                       file_name="gabinetes_media.zip", mime="application/zip")

# ----- Pie
st.markdown("---")
st.caption("Hecho con ❤️ por el Gabinete del Asombro · Streamlit + SQLite (sqlite3)")
