import streamlit as st
from sqlmodel import SQLModel, Field, create_engine, Session, select
from PIL import Image
import pandas as pd
import os

# Configuración de la app
st.set_page_config(page_title="Gabinete de Maravillas", page_icon="🗝️", layout="wide")

# --- BASE DE DATOS ---
class Entry(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    description: str
    image_path: str = Field(default="")
    suno_link: str = Field(default="")

# Conexión SQLite
engine = create_engine("sqlite:///gabinete.db")
SQLModel.metadata.create_all(engine)

def get_session():
    return Session(engine)

# --- FUNCIONES ---
def save_entry(title, description, image_file, suno_link):
    image_path = ""
    if image_file:
        os.makedirs("assets", exist_ok=True)
        image_path = os.path.join("assets", image_file.name)
        with open(image_path, "wb") as f:
            f.write(image_file.getbuffer())

    entry = Entry(title=title, description=description, image_path=image_path, suno_link=suno_link)
    with get_session() as session:
        session.add(entry)
        session.commit()

def load_entries():
    with get_session() as session:
        return session.exec(select(Entry)).all()

# --- INTERFAZ ---
st.title("🗝️ Gabinete de Maravillas")
st.write("Tu bitácora de curiosidades y creación artística.")

# Portada
if os.path.exists("assets/hero.jpg"):
    st.image("assets/hero.jpg", use_column_width=True)

# Formulario para agregar entradas
with st.form("entry_form"):
    title = st.text_input("Título")
    description = st.text_area("Descripción")
    image_file = st.file_uploader("Sube una imagen", type=["jpg", "jpeg", "png"])
    suno_link = st.text_input("Enlace de Suno (opcional)")
    submitted = st.form_submit_button("Guardar")
    if submitted:
        save_entry(title, description, image_file, suno_link)
        st.success("Entrada guardada correctamente.")

# Mostrar entradas guardadas
entries = load_entries()
if entries:
    for e in entries:
        st.subheader(e.title)
        st.write(e.description)
        if e.image_path and os.path.exists(e.image_path):
            st.image(e.image_path, width=300)
        if e.suno_link:
            st.markdown(f"[🎵 Escuchar en Suno]({e.suno_link})")
else:
    st.info("Aún no hay entradas en tu gabinete.")
