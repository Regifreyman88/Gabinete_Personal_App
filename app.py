import streamlit as st
import pandas as pd
import gspread
from google.oauth2 import service_account

# --- CONFIGURACIÓN Y TÍTULO ---
st.set_page_config(layout="wide")
st.title("🖼️ Galería de la Clase: Gabinetes Personales")
st.markdown("Explora los análisis y descubrimientos realizados por todos los participantes del curso.")

# --- AUTENTICACIÓN (CON EL PERMISO CORREGIDO) ---
def connect_to_google_sheets():
    try:
        creds_dict = {
            "type": st.secrets["gcp_type"],
            "project_id": st.secrets["gcp_project_id"],
            "private_key_id": st.secrets["gcp_private_key_id"],
            "private_key": st.secrets["gcp_private_key"],
            "client_email": st.secrets["gcp_client_email"],
            "client_id": st.secrets["gcp_client_id"],
            "auth_uri": st.secrets["gcp_auth_uri"],
            "token_uri": st.secrets["gcp_token_uri"],
            "auth_provider_x509_cert_url": st.secrets["gcp_auth_provider_x509_cert_url"],
            "client_x509_cert_url": st.secrets["gcp_client_x509_cert_url"],
        }
        
        # AQUÍ ESTÁ LA CORRECCIÓN: Se añadieron los permisos para Google Drive
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
        creds = service_account.Credentials.from_service_account_info(
            creds_dict,
            scopes=scopes,
        )
        client = gspread.authorize(creds)
        return client
    except Exception as e:
        st.error(f"Error de autenticación: {e}")
        st.info("Verifica que los 'Secrets' en GitHub sean correctos y que hayas compartido tu Hoja de Cálculo y la Carpeta de Drive con el 'client_email'.")
        return None

# --- CARGA DE DATOS ---
def load_data(client):
    try:
        sheet = client.open("Mi gabinete personal (Respuestas)").sheet1
        data = sheet.get_all_records()
        return pd.DataFrame(data)
    except gspread.exceptions.SpreadsheetNotFound:
        st.error("No se encontró la Hoja de Cálculo 'Mi gabinete personal (Respuestas)'. Revisa que el nombre sea exacto y los permisos de compartir.")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Ocurrió un error al cargar los datos: {e}")
        return pd.DataFrame()

# --- CONSTRUCCIÓN DE LA GALERÍA ---
client = connect_to_google_sheets()

if client:
    df = load_data(client)
    if not df.empty:
        df = df.iloc[::-1]
        for index, row in df.iterrows():
            st.divider()

            # --- Nombres de las columnas de tu Formulario ---
            col_carrera = "Carrera"
            col_artefacto = "El artefacto central: Describe el único objeto, real o imaginado, que está en el corazón de tu Gabinete."
            col_pitch = "El Pitch (La Revelación Controlada)\nEscribe aquí tu pitch (máximo 3 minutos de lectura). Responde: ¿Por qué este Gabinete merece existir y qué debería sentir alguien al visitarlo?"
            col_imagen = "Mi Gabinete"
            col_timestamp = "Marca temporal"

            # --- Diseño de cada entrada de la galería ---
            col1, col2 = st.columns([1, 2])
            
            with col1:
                if col_imagen in row and row[col_imagen]:
                    st.image(row[col_imagen], use_column_width=True)
                else:
                    st.warning("Imagen no disponible.")
            
            with col2:
                if col_carrera in row and row[col_carrera]:
                    st.subheader(f"Gabinete de: {row[col_carrera]}")
                if col_artefacto in row:
                    st.markdown(f"**Artefacto Central:** {row[col_artefacto]}")
                if col_pitch in row:
                    st.markdown(f"**El Pitch:** *\"{row[col_pitch]}\"*")
                if col_timestamp in row:
                    st.caption(f"Publicado el: {row[col_timestamp]}")
    else:
        st.info("Aún no hay respuestas en el formulario. ¡La galería aparecerá aquí cuando los alumnos empiecen a participar!")
