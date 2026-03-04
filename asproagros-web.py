import streamlit as st
from pathlib import Path
from docx import Document

# ---------------- CONFIG ---------------- #
st.set_page_config(page_title="ASPROAGROS", page_icon="🌱", layout="wide")

BASE_DIR = Path(__file__).parent
IMG_DIR = BASE_DIR / "images"
DATA_DIR = BASE_DIR / "data"

# ---------------- HELPERS ---------------- #
def list_files(dir_path: Path):
    if dir_path.exists():
        return sorted([p.name for p in dir_path.iterdir() if p.is_file()])
    return []

def show_image(original_name: str, caption: str | None = None):
    path = IMG_DIR / original_name
    if path.exists():
        st.image(str(path), caption=caption, use_container_width=True)
    else:
        st.warning(f"⚠️ No se encontró la imagen: `{original_name}`")
        st.caption(f"Ruta buscada: {path}")

def download_file(original_name: str, label: str, mime: str):
    path = DATA_DIR / original_name
    if path.exists():
        with open(path, "rb") as f:
            st.download_button(label=label, data=f, file_name=original_name, mime=mime)
    else:
        st.warning(f"⚠️ No se encontró: `{original_name}`")
        st.caption(f"Ruta buscada: {path}")

def read_docx_text(docx_name: str) -> str:
    """Lee un .docx desde data/ y devuelve texto (para mostrar planeación en web)."""
    path = DATA_DIR / docx_name
    if not path.exists():
        return ""
    doc = Document(str(path))
    lines = []
    for p in doc.paragraphs:
        t = (p.text or "").strip()
        if t:
            lines.append(t)
    return "\n".join(lines)

# ---------------- DEBUG (Sidebar) ---------------- #
st.sidebar.markdown("## 🔧 Diagnóstico (Streamlit Cloud)")
st.sidebar.write("📄 Carpeta app:", str(BASE_DIR))
st.sidebar.write("🖼️ images/:", str(IMG_DIR))
st.sidebar.write("📦 data/:", str(DATA_DIR))

imgs = list_files(IMG_DIR)
docs = list_files(DATA_DIR)

if IMG_DIR.exists():
    st.sidebar.success(f"✅ images/ existe ({len(imgs)} archivos)")
    st.sidebar.write(imgs)
else:
    st.sidebar.error("❌ Falta la carpeta images/ en el repo (debe estar commiteada).")

if DATA_DIR.exists():
    st.sidebar.success(f"✅ data/ existe ({len(docs)} archivos)")
    st.sidebar.write(docs)
else:
    st.sidebar.error("❌ Falta la carpeta data/ en el repo (debe estar commiteada).")

# ---------------- HEADER ---------------- #
st.title("🌱 Asociación de Productores Agrícolas de Santa Cruz")
st.subheader("ASPROAGROS")

# Identidad institucional (tomada de hoja de vida / informe)
st.markdown("""
**NIT:** 901.117.531-1  
**Ubicación:** Santa Cruz - Luruaco, Atlántico, Colombia  
**Contacto:** +57 3205822216  
""")

menu = st.sidebar.selectbox(
    "Menú",
    [
        "Inicio",
        "Identidad institucional",
        "Planeación estratégica 2025–2030",
        "Gestión 2024",
        "Soportes y documentos",
        "Galería"
    ]
)

# ---------------- PÁGINAS ---------------- #
if menu == "Inicio":
    col1, col2 = st.columns([1.2, 1])

    with col1:
        show_image("WhatsApp Image 2026-02-20 at 10.33.46 AM.jpeg", "Reunión comunitaria / trabajo asociativo")

    with col2:
        st.markdown("""
### Bienvenidos a ASPROAGROS
Somos una asociación campesina y productiva ubicada en **Santa Cruz – Luruaco**.

Trabajamos para:
- Fortalecer la organización de productores
- Mejorar productividad y acceso a mercados
- Impulsar proyectos y financiamiento
- Promover sostenibilidad ambiental
""")

    st.divider()
    st.markdown("### Actividad productiva (resumen)")
    st.write("Cultivos y líneas productivas: plátano, ñame, yuca, mango, limón, ají (según hoja de vida institucional).")

elif menu == "Identidad institucional":
    st.header("🏛️ Identidad institucional")

    # Resumen en base a la hoja de vida institucional e informe
    st.subheader("Misión (resumen)")
    st.write("Representar, fortalecer y organizar a los productores agrícolas de Santa Cruz, promoviendo desarrollo sostenible, competitividad, innovación y acceso a mercados justos.")

    st.subheader("Visión (5 años)")
    st.write("Ser una asociación líder regional, reconocida por eficiencia organizativa, producción sostenible y acceso a mercados nacionales e internacionales.")

    st.subheader("Valores")
    st.write("Solidaridad, transparencia, responsabilidad social, sostenibilidad ambiental, innovación y compromiso con el productor.")

    st.divider()
    st.subheader("Foto / contexto territorial")
    show_image("WhatsApp Image 2026-02-23 at 1.09.40 PM.jpeg", "Trabajo comunitario y organización")

elif menu == "Planeación estratégica 2025–2030":
    st.header("🧭 Planeación Estratégica 2025–2030")

    st.markdown("""
**Ejes estratégicos:**
1) Fortalecimiento organizacional  
2) Desarrollo productivo y tecnificación  
3) Comercialización y acceso a mercados  
4) Sostenibilidad ambiental y cambio climático  
5) Gestión de proyectos y financiamiento  
""")

    st.divider()
    st.subheader("Contenido del documento (DOCX)")
    texto = read_docx_text("PLANEACIÓN ESTRATÉGICA ASPROAGROS.docx")

    if texto:
        st.text_area("Planeación (extracto cargado desde el DOCX)", texto, height=420)
    else:
        st.warning("⚠️ No pude leer el DOCX. Verifica que esté en /data con el nombre original.")

    st.divider()
    download_file("PLANEACIÓN ESTRATÉGICA ASPROAGROS.docx", "⬇️ Descargar Planeación Estratégica (DOCX)", "application/vnd.openxmlformats-officedocument.wordprocessingml.document")

elif menu == "Gestión 2024":
    st.header("📌 Actividades de Gestión 2024")

    st.markdown("""
Este apartado reúne el soporte del **informe de actividades (enero–diciembre 2024)**, que incluye actividades como rifa, bingo, pasteles y carnes asadas, y sus egresos asociados.
""")

    st.divider()
    download_file("ACTIVIDADES DE INFORME DE GESTIÓN.pdf", "⬇️ Descargar Informe de Gestión 2024 (PDF)", "application/pdf")

elif menu == "Soportes y documentos":
    st.header("📄 Soportes y Documentos Oficiales")

    st.subheader("Resolución / Registro RESO (ANT)")
    st.markdown("Soporte de inclusión de la asociación en el **Registro de Sujetos de Ordenamiento (RESO)** como aspirante de acceso a tierra.")
    download_file(
        "RESOLUCION DE INCLUSION-1106-ASOCIACION DE PRODUCTORES AGRICOLAS DE SANTA CRUZ SIGLA.pdf",
        "⬇️ Descargar Resolución ANT (PDF)",
        "application/pdf",
    )

    st.divider()
    st.subheader("Estados financieros y RUT")
    download_file(
        "balance, estado de resultados y rut ASPROAGROS.pdf",
        "⬇️ Descargar Balance + Estado de Resultados + RUT (PDF)",
        "application/pdf",
    )

    st.divider()
    st.subheader("Certificación contador")
    download_file("CERTIFICACION ASPROAGROS.pdf", "⬇️ Descargar Certificación (PDF)", "application/pdf")

    st.divider()
    st.subheader("Hoja de vida institucional")
    download_file(
        "HOJA DE VIDA ASOCIACION DE PRODUCTORES AGRICOLAS DE SANTA CRUZ - ASPROAGROS.pdf",
        "⬇️ Descargar Hoja de Vida (PDF)",
        "application/pdf",
    )

elif menu == "Galería":
    st.header("🖼️ Galería")

    st.markdown("Fotos de trabajo comunitario, producción agrícola y actividades en territorio.")

    col1, col2 = st.columns(2)
    with col1:
        show_image("WhatsApp Image 2026-02-20 at 10.33.46 AM.jpeg", "Reunión / organización")
        show_image("WhatsApp Image 2026-02-23 at 1.09.39 PM.jpeg", "Producción agrícola")
    with col2:
        show_image("WhatsApp Image 2026-02-23 at 1.09.40 PM.jpeg", "Gestión comunitaria")
        show_image("WhatsApp Image 2026-02-23 at 1.09.40 PM (1).jpeg", "Soportes / documentos")

st.caption("✅ Si algo no carga, revisa el sidebar 'Diagnóstico' para ver qué archivos detectó Streamlit Cloud.")
