# app_eval.py — Panel independiente para evaluar SPARK (funciona donde esté)
import sys, sqlite3
from pathlib import Path
import streamlit as st

# --- encontrar y cargar spark_patch estén donde estén los archivos
BASE = Path(__file__).resolve().parent
CANDIDATE_DIRS = [
    BASE,  # mismo nivel
    BASE / "Gabinete_Personal_App",  # subcarpeta común
    BASE.parent / "Gabinete_Personal_App",  # padre/Gabinete_Personal_App
]
loaded = False
for d in CANDIDATE_DIRS:
    sp = d / "spark_patch.py"
    if sp.exists():
        if str(d) not in sys.path:
            sys.path.insert(0, str(d))
        loaded = True
        break
if not loaded:
    st.error("No encuentro spark_patch.py. Pon este archivo (app_eval.py) en la misma carpeta que spark_patch.py o dentro de Gabinete_Personal_App/.")
    st.stop()

from spark_patch import ensure_schema, admin_panel  # ahora sí

st.set_page_config(page_title="Evaluación SPARK", page_icon="✅", layout="wide")
st.title("Evaluación SPARK")

# --- clave docente (misma que tu app principal; por defecto 'regina-demo')
ADMIN_KEY = st.secrets.get("ADMIN_KEY", "regina-demo")
key = st.text_input("Clave docente", type="password")
if key != ADMIN_KEY:
    st.info("Introduce la clave docente para acceder.")
    st.stop()

# --- localizar la MISMA base de datos (gabinete.db)
DB_CANDIDATES = [
    BASE / "data" / "gabinete.db",
    BASE / "Gabinete_Personal_App" / "data" / "gabinete.db",
    BASE.parent / "Gabinete_Personal_App" / "data" / "gabinete.db",
]
db_path = None
for p in DB_CANDIDATES:
    if p.exists():
        db_path = p
        break
if db_path is None:
    # si no existe, creamos en BASE/Gabinete_Personal_App/data para compartir con la app principal
    db_path = BASE / "Gabinete_Personal_App" / "data" / "gabinete.db"
    db_path.parent.mkdir(parents=True, exist_ok=True)

conn = sqlite3.connect(str(db_path), check_same_thread=False)
ensure_schema(conn)

st.caption(f"Base de datos: {db_path.as_posix()}")
st.markdown("---")

# --- panel de evaluación SPARK
admin_panel(conn)

st.markdown("---")
st.caption("Panel independiente de evaluación SPARK · comparte la misma base de datos de la app principal si existe.")
