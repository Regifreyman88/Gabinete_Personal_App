# app_eval.py — Evaluación SPARK independiente
from pathlib import Path
import sqlite3
import streamlit as st
from spark_patch import ensure_schema, admin_panel

st.set_page_config(page_title="Evaluación SPARK", page_icon="✅", layout="wide")
st.title("Evaluación SPARK")

# Clave docente (usa la misma que tu app; si no hay, queda 'regina-demo')
ADMIN_KEY = st.secrets.get("ADMIN_KEY", "regina-demo")
key = st.text_input("Clave docente", type="password")
if key != ADMIN_KEY:
    st.info("Introduce la clave docente para acceder.")
    st.stop()

# MISMA base de datos que tu app: ./data/gabinete.db
BASE_DIR = Path(__file__).parent
DB_PATH  = BASE_DIR / "data" / "gabinete.db"
conn = sqlite3.connect(DB_PATH, check_same_thread=False)
ensure_schema(conn)

st.markdown("---")
admin_panel(conn)

st.markdown("---")
st.caption("Panel independiente de evaluación SPARK · comparte la misma base de datos de la app principal.")
