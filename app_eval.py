# app_eval.py — Panel independiente para evaluar SPARK (versión simple)
from pathlib import Path
import sqlite3
import streamlit as st
# Importa directamente desde la carpeta donde están app.py y spark_patch.py
from Gabinete_Personal_App.spark_patch import ensure_schema, admin_panel

st.set_page_config(page_title="Evaluación SPARK", page_icon="✅", layout="wide")
st.title("Evaluación SPARK")

# Clave docente (la misma que tu app; por defecto 'regina-demo')
ADMIN_KEY = st.secrets.get("ADMIN_KEY", "regina-demo")
key = st.text_input("Clave docente", type="password")
if key != ADMIN_KEY:
    st.info("Introduce la clave docente para acceder.")
    st.stop()

# Usa la MISMA base que tu app principal
DB_PATH = Path("Gabinete_Personal_App") / "data" / "gabinete.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)
conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
ensure_schema(conn)

st.caption(f"Base de datos: {DB_PATH.as_posix()}")
st.markdown("---")

# Panel de evaluación SPARK
admin_panel(conn)

st.markdown("---")
st.caption("Panel independiente de evaluación SPARK · comparte la misma base de datos de la app principal.")
