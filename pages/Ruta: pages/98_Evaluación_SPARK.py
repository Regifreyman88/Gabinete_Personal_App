import sqlite3
from pathlib import Path
import streamlit as st
from spark_patch import ensure_schema, admin_panel

st.title("Evaluación SPARK")

# misma clave que tu app principal (o 'regina-demo' si no hay secret)
ADMIN_KEY = st.secrets.get("ADMIN_KEY", "regina-demo")
key = st.text_input("Clave docente", type="password")
if key != ADMIN_KEY:
    st.info("Introduce la clave docente para acceder.")
    st.stop()

# usa la MISMA base de datos que app.py: data/gabinete.db
DB_PATH = Path(__file__).resolve().parent.parent / "data" / "gabinete.db"
conn = sqlite3.connect(DB_PATH, check_same_thread=False)
ensure_schema(conn)

st.markdown("---")
admin_panel(conn)
