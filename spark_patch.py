# spark_patch.py — Extensión mínima para declarar que la app "sigue a SPARK"
# -------------------------------------------------------------
# Requisitos: streamlit, sqlite3 (ya los usas). No dependencias extra.
# Integra 5 checkpoints con artefactos obligatorios + rúbrica y export.
# Cómo usar:
#   1) Coloca este archivo junto a tu app principal (app.py o Home.py).
#   2) En tu app, importa con: `from spark_patch import spark_ui, admin_panel, ensure_schema`.
#   3) Llama `ensure_schema(conn)` una vez al inicio (donde abres sqlite3).
#   4) En "Crear / Editar mi Gabinete", inserta `spark_ui(conn, email, nombre_equipo)` debajo de tus secciones.
#   5) En "Panel docente", inserta `admin_panel(conn)`.
#   6) En "Galería" puedes filtrar por `completion == 5` (SPARK completo).

import json
import sqlite3
from datetime import date
import streamlit as st

SDGS = [
    "No Poverty", "Zero Hunger", "Good Health and Well-being", "Quality Education",
    "Gender Equality", "Clean Water and Sanitation", "Affordable and Clean Energy",
    "Decent Work and Economic Growth", "Industry, Innovation and Infrastructure",
    "Reduced Inequalities", "Sustainable Cities and Communities", "Responsible Consumption and Production",
    "Climate Action", "Life Below Water", "Life on Land", "Peace, Justice and Strong Institutions",
    "Partnerships for the Goals"
]

# ---------- DB SCHEMA ----------

def ensure_schema(conn: sqlite3.Connection):
    cur = conn.cursor()
    # Tabla para entradas SPARK por estudiante (clave por email + team opcional)
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS spark_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            team TEXT,
            sensing_snapshot TEXT,
            sensing_valence TEXT,
            sensing_evidence_url TEXT,
            probing_hypothesis TEXT,
            probing_data_plan TEXT, -- JSON array of {data, source, owner, due}
            acting_decisions TEXT,  -- JSON list
            acting_learnings TEXT,  -- JSON list
            acting_changes TEXT,    -- JSON list
            reflecting_tension TEXT,
            reflecting_assumption TEXT,
            knowing_insights TEXT,  -- JSON list (2)
            knowing_sdg TEXT,       -- JSON list (≥1)
            knowing_next_action TEXT, -- JSON object {action, owner, due}
            updated_at TEXT
        )
        """
    )
    # Tabla de calificaciones por fase (0–4)
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS spark_scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            rubric JSON,            -- {sensing: int, probing: int, acting: int, reflecting: int, knowing: int}
            comments TEXT,
            updated_at TEXT
        )
        """
    )
    conn.commit()

# ---------- HELPERS ----------

def word_count(txt: str) -> int:
    return len((txt or "").strip().split())

def get_entry(conn, email: str):
    cur = conn.cursor()
    cur.execute("SELECT * FROM spark_entries WHERE email = ? ORDER BY id DESC LIMIT 1", (email,))
    row = cur.fetchone()
    if not row:
        return None
    cols = [d[0] for d in cur.description]
    return dict(zip(cols, row))

def upsert_entry(conn, email: str, team: str, payload: dict):
    existing = get_entry(conn, email)
    now = date.today().isoformat()
    fields = {
        "email": email,
        "team": team,
        "sensing_snapshot": payload.get("sensing_snapshot"),
        "sensing_valence": payload.get("sensing_valence"),
        "sensing_evidence_url": payload.get("sensing_evidence_url"),
        "probing_hypothesis": payload.get("probing_hypothesis"),
        "probing_data_plan": json.dumps(payload.get("probing_data_plan", [])),
        "acting_decisions": json.dumps(payload.get("acting_decisions", [])),
        "acting_learnings": json.dumps(payload.get("acting_learnings", [])),
        "acting_changes": json.dumps(payload.get("acting_changes", [])),
        "reflecting_tension": payload.get("reflecting_tension"),
        "reflecting_assumption": payload.get("reflecting_assumption"),
        "knowing_insights": json.dumps(payload.get("knowing_insights", [])),
        "knowing_sdg": json.dumps(payload.get("knowing_sdg", [])),
        "knowing_next_action": json.dumps(payload.get("knowing_next_action", {})),
        "updated_at": now,
    }
    cur = conn.cursor()
    if existing:
        sets = ", ".join([f"{k} = :{k}" for k in fields.keys() if k not in ("email",)])
        cur.execute(f"UPDATE spark_entries SET {sets} WHERE email = :email", fields)
    else:
        cols = ",".join(fields.keys())
        placeholders = ",".join([f":{k}" for k in fields.keys()])
        cur.execute(f"INSERT INTO spark_entries ({cols}) VALUES ({placeholders})", fields)
    conn.commit()

# ---------- UI COMPONENTS (ESTUDIANTE) ----------

def spark_ui(conn, email: str, team: str):
    st.markdown("### SPARK — Checkpoints (5/5)")
    tabs = st.tabs([
        "Sensing (Caverna)", "Probing (Forense/Arquitectura)", "Acting (Prototipo)",
        "Reflecting (Espejo)", "Knowing (Rizoma)"
    ])
    payload = {}

    with tabs[0]:
        st.caption("Saliencia ético‑afectiva del reto y evidencia local.")
        sensing_snapshot = st.text_area(
            "Snapshot (150–200 palabras)",
            help="Describe qué resulta éticamente saliente del objeto/tema y por qué.",
            height=140,
        )
        sensing_valence = st.selectbox("Valencia emocional", ["Positiva", "Negativa", "Mixta"]) 
        sensing_evidence_url = st.text_input("Evidencia local (URL a imagen/enlace)")
        if st.button("Guardar Sensing"):
            if word_count(sensing_snapshot) < 150 or word_count(sensing_snapshot) > 220:
                st.error("El snapshot debe tener entre 150 y 200 palabras.")
            else:
                payload.update({
                    "sensing_snapshot": sensing_snapshot,
                    "sensing_valence": sensing_valence,
                    "sensing_evidence_url": sensing_evidence_url,
                })
                upsert_entry(conn, email, team, payload)
                st.success("Sensing guardado ✔")

    with tabs[1]:
        st.caption("Marco abductivo y plan de datos.")
        probing_hypothesis = st.text_input("Hipótesis abductiva (1–2 frases)",
                                           placeholder="Creemos que … porque observamos …")
        st.markdown("**Plan de datos (qué/fuente/quién/fecha)**")
        plan = []
        for i in range(1, 4):
            c1, c2, c3, c4 = st.columns([2,2,2,1])
            with c1:
                d = st.text_input(f"Dato #{i}")
            with c2:
                s = st.text_input(f"Fuente #{i}")
            with c3:
                o = st.text_input(f"Responsable #{i}")
            with c4:
                due = st.date_input(f"Fecha #{i}", value=date.today())
            if d or s or o:
                plan.append({"data": d, "source": s, "owner": o, "due": str(due)})
        if st.button("Guardar Probing"):
            if not probing_hypothesis:
                st.error("Incluye una hipótesis abductiva.")
            elif len(plan) == 0:
                st.error("Agrega al menos una fila al plan de datos.")
            else:
                payload.update({
                    "probing_hypothesis": probing_hypothesis,
                    "probing_data_plan": plan,
                })
                upsert_entry(conn, email, team, payload)
                st.success("Probing guardado ✔")

    with tabs[2]:
        st.caption("Decisiones basadas en evidencia + aprendizaje/cambio.")
        decisions = st.tags_input("Decisiones (3–5)") if hasattr(st, 'tags_input') else st.text_area("Decisiones (bullets)")
        learnings = st.text_area("Qué aprendimos (bullets)")
        changes = st.text_area("Qué cambiaremos (bullets)")
        if st.button("Guardar Acting"):
            payload.update({
                "acting_decisions": decisions.split("\n") if isinstance(decisions, str) else decisions,
                "acting_learnings": [x.strip() for x in learnings.split("\n") if x.strip()],
                "acting_changes": [x.strip() for x in changes.split("\n") if x.strip()],
            })
            upsert_entry(conn, email, team, payload)
            st.success("Acting guardado ✔")

    with tabs[3]:
        st.caption("Metacognición narrativa: tensión y replanteamiento.")
        reflecting_tension = st.text_area("Tensión vivida (concreta)")
        reflecting_assumption = st.text_area("Supuesto que cambió (y por qué)")
        if st.button("Guardar Reflecting"):
            if word_count(reflecting_tension) < 20 or word_count(reflecting_assumption) < 20:
                st.error("Amplía la tensión/supuesto (≥20 palabras cada uno).")
            else:
                payload.update({
                    "reflecting_tension": reflecting_tension,
                    "reflecting_assumption": reflecting_assumption,
                })
                upsert_entry(conn, email, team, payload)
                st.success("Reflecting guardado ✔")

    with tabs[4]:
        st.caption("Transferencia: insights, SDG y próxima acción.")
        c1, c2 = st.columns(2)
        with c1:
            ins1 = st.text_input("Insight #1 (generalizable)")
        with c2:
            ins2 = st.text_input("Insight #2 (generalizable)")
        sdg_sel = st.multiselect("SDG(s) relacionados", SDGS)
        c3, c4, c5 = st.columns([2,1,1])
        with c3:
            act = st.text_input("Próxima acción")
        with c4:
            owner = st.text_input("Responsable")
        with c5:
            due = st.date_input("Fecha", value=date.today())
        if st.button("Guardar Knowing"):
            if not ins1 or not ins2 or not sdg_sel or not act or not owner:
                st.error("Completa insights, SDG, acción y responsable.")
            else:
                payload.update({
                    "knowing_insights": [ins1, ins2],
                    "knowing_sdg": sdg_sel,
                    "knowing_next_action": {"action": act, "owner": owner, "due": str(due)}
                })
                upsert_entry(conn, email, team, payload)
                st.success("Knowing guardado ✔")

    st.divider()
    if st.button("Exportar portafolio SPARK (JSON)"):
        entry = get_entry(conn, email)
        if entry:
            fname = f"spark_{email.replace('@','_')}.json"
            st.download_button("Descargar JSON", data=json.dumps(entry, ensure_ascii=False, indent=2), file_name=fname, mime="application/json")
        else:
            st.warning("Completa y guarda al menos una fase antes de exportar.")

# ---------- ADMIN PANEL (DOCENTE) ----------

def admin_panel(conn):
    st.header("Panel Docente — Rúbrica SPARK (0–4)")
    email = st.text_input("Email del estudiante para evaluar")
    if not email:
        st.info("Ingresa un email para cargar la última entrada SPARK.")
        return
    entry = get_entry(conn, email)
    if not entry:
        st.warning("Sin registro SPARK para este email.")
        return

    st.subheader("Vista rápida")
    st.json(entry, expanded=False)

    st.subheader("Rúbrica (0–4 por fase)")
    cols = st.columns(5)
    sensing = cols[0].number_input("Sensing", 0, 4, value=0)
    probing = cols[1].number_input("Probing", 0, 4, value=0)
    acting = cols[2].number_input("Acting", 0, 4, value=0)
    reflecting = cols[3].number_input("Reflecting", 0, 4, value=0)
    knowing = cols[4].number_input("Knowing", 0, 4, value=0)
    comments = st.text_area("Comentarios")

    if st.button("Guardar evaluación"):
        cur = conn.cursor()
        payload = {
            "email": email,
            "rubric": json.dumps({
                "sensing": int(sensing), "probing": int(probing), "acting": int(acting),
                "reflecting": int(reflecting), "knowing": int(knowing)
            }),
            "comments": comments,
            "updated_at": date.today().isoformat(),
        }
        cur.execute("SELECT id FROM spark_scores WHERE email = ?", (email,))
        row = cur.fetchone()
        if row:
            cur.execute("UPDATE spark_scores SET rubric=:rubric, comments=:comments, updated_at=:updated_at WHERE email=:email", payload)
        else:
            cur.execute("INSERT INTO spark_scores (email, rubric, comments, updated_at) VALUES (:email, :rubric, :comments, :updated_at)", payload)
        conn.commit()
        st.success("Evaluación guardada ✔")

    st.subheader("Exportar CSV")
    if st.button("Descargar calificaciones CSV"):
        cur = conn.cursor()
        cur.execute("SELECT email, rubric, comments, updated_at FROM spark_scores")
        rows = cur.fetchall()
        import csv, io
        buf = io.StringIO()
        writer = csv.writer(buf)
        writer.writerow(["email","sensing","probing","acting","reflecting","knowing","comments","updated_at"])
        for e, rjson, c, u in rows:
            r = json.loads(rjson)
            writer.writerow([e, r.get("sensing"), r.get("probing"), r.get("acting"), r.get("reflecting"), r.get("knowing"), c, u])
        st.download_button("Descargar CSV", data=buf.getvalue(), file_name="spark_scores.csv", mime="text/csv")

# ---------- USO DE EJEMPLO ----------
# En tu app principal:
# import sqlite3, streamlit as st
# from spark_patch import spark_ui, admin_panel, ensure_schema
# conn = sqlite3.connect("gabinete.db", check_same_thread=False)
# ensure_schema(conn)
# ... obtener email/nombre_equipo del formulario Perfil ...
# spark_ui(conn, email, nombre_equipo)
# ... en página Panel Docente ...
# admin_panel(conn)
