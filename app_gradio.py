import os
import base64
import streamlit as st
from groq import Groq

# ==============================================================================
# CONFIGURACIÓN DE PÁGINA
# ==============================================================================
st.set_page_config(
    page_title="HUD TECO/TELCO Multiagent",
    page_icon="⚡",
    layout="wide"
)

# ==============================================================================
# DISEÑO CSS FUTURISTA / HUD (Cian y Azul Neón)
# ==============================================================================
st.markdown("""
<style>
    /* Fondo principal y fuente estilo terminal */
    .stApp {
        background-color: #030814;
        color: #00f0ff;
        font-family: 'Consolas', 'Courier New', monospace;
    }
    
    /* Header estilizado estilo HUD con efecto de brillo */
    .header-box {
        background: linear-gradient(135deg, rgba(0, 240, 255, 0.05) 0%, rgba(0, 100, 255, 0.15) 100%);
        border: 1px solid #00f0ff;
        box-shadow: 0 0 20px rgba(0, 240, 255, 0.4), inset 0 0 15px rgba(0, 240, 255, 0.1);
        padding: 25px;
        border-radius: 10px;
        margin-bottom: 25px;
        position: relative;
        overflow: hidden;
    }
    
    .header-box::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 3px;
        background: linear-gradient(90deg, transparent, #00f0ff, transparent);
    }
    
    .header-title {
        color: #00f0ff;
        text-shadow: 0 0 12px #00f0ff, 0 0 25px #0055ff;
        font-weight: bold;
        font-size: 26px;
        letter-spacing: 3px;
        margin-bottom: 15px;
    }
    
    .header-info {
        color: #8ae3ff;
        font-size: 14px;
        margin-bottom: 6px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Botones */
    div.stButton > button {
        background: linear-gradient(90deg, #001f3f, #0055ff) !important;
        color: #00f0ff !important;
        font-weight: bold !important;
        font-family: 'Consolas', monospace !important;
        border: 1px solid #00f0ff !important;
        border-radius: 4px !important;
        transition: all 0.3s ease !important;
    }
    
    div.stButton > button:hover {
        background: linear-gradient(90deg, #0055ff, #00c3ff) !important;
        color: #ffffff !important;
        box-shadow: 0 0 20px #00f0ff !important;
    }
    
    /* Inputs */
    .stTextInput input, .stTextArea textarea, .stSelectbox, .stSlider {
        background-color: #061224 !important;
        color: #00f0ff !important;
        border: 1px solid #0088ff !important;
        font-family: 'Consolas', monospace !important;
    }

    /* Tarjetas de Planes */
    .plan-card {
        background: rgba(0, 240, 255, 0.05);
        border: 1px solid #00f0ff;
        border-radius: 8px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 0 15px rgba(0, 240, 255, 0.2);
        margin-bottom: 15px;
    }
    .plan-title { font-size: 20px; font-weight: bold; color: #00f0ff; margin-bottom: 10px; }
    .plan-price { font-size: 28px; color: #ffffff; text-shadow: 0 0 10px #00f0ff; margin-bottom: 15px; }
    .plan-features { color: #8ae3ff; font-size: 14px; text-align: left; margin-bottom: 15px; }

    /* Fondo decorativo (TELCO) */
    .stApp::before {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: 0;
        pointer-events: none;
        opacity: 0.10; 
        background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='600' height='600' viewBox='0 0 600 600'><g fill='none' stroke='%2300f0ff' stroke-width='1.5' stroke-linecap='round' stroke-linejoin='round'><path d='M60 100 L60 140 M45 115 L75 115 M50 100 L70 100 M55 85 L65 85'/><rect x='45' y='140' width='30' height='40' rx='4'/><circle cx='60' cy='155' r='3'/><circle cx='60' cy='170' r='3'/><path d='M130 90 q20 -20 40 0 M140 100 q10 -10 20 0 M150 110 v15 M140 125 h20'/><rect x='135' y='130' width='30' height='45' rx='4'/><rect x='145' y='140' width='10' height='25' rx='2'/><circle cx='230' cy='120' r='15'/><path d='M230 105 L230 135 M215 120 L245 120'/><circle cx='230' cy='120' r='5'/><path d='M215 120 A15 15 0 0 1 245 120'/><circle cx='320' cy='100' r='18'/><path d='M320 82 L320 118 M302 100 L338 100'/><circle cx='320' cy='100' r='6'/><path d='M320 118 L320 140 M320 82 L320 60'/><path d='M302 82 L285 65 M338 82 L355 65'/><rect x='400' y='80' width='40' height='40' rx='5'/><circle cx='420' cy='100' r='4'/><circle cx='420' cy='100' r='8'/><circle cx='420' cy='100' r='12'/><path d='M420 112 L420 120 M412 120 L428 120'/><path d='M500 80 L520 60 L540 80 L520 100 Z'/><circle cx='520' cy='80' r='8'/><circle cx='520' cy='80' r='4'/><circle cx='60' cy='250' r='15'/><circle cx='60' cy='250' r='25'/><circle cx='60' cy='250' r='35'/><circle cx='60' cy='250' r='45'/><circle cx='60' cy='250' r='55'/><path d='M25 250 L15 250 M95 250 L105 250 M60 215 L60 205 M60 285 L60 295'/><rect x='150' y='240' width='30' height='40' rx='4'/><path d='M160 250 L170 250 M160 260 L170 260 M160 270 L165 270'/><circle cx='200' cy='260' r='20'/><path d='M190 260 L210 260 M200 250 L200 270'/><path d='M200 280 L200 295 M180 295 L220 295'/><path d='M280 220 L300 240 L280 260 L260 240 Z'/><circle cx='280' cy='240' r='5'/><rect x='340' y='230' width='50' height='30' rx='4'/><path d='M350 230 L350 245 M360 230 L360 245 M370 230 L370 245'/><rect x='420' y='225' width='40' height='50' rx='4'/><circle cx='440' cy='240' r='3'/><circle cx='440' cy='255' r='3'/><circle cx='440' cy='270' r='3'/><path d='M480 230 Q500 210 520 230'/><path d='M490 240 Q500 230 510 240'/><path d='M500 250 Q500 245 500 250'/><circle cx='500' cy='255' r='2'/><circle cx='60' cy='400' r='20'/><path d='M50 400 L70 400 M60 390 L60 410'/><path d='M60 380 L60 370 M60 420 L60 430'/><path d='M40 380 L50 370 M80 380 L70 370'/><path d='M40 420 L50 430 M80 420 L70 430'/><rect x='120' y='380' width='40' height='40' rx='5'/><path d='M125 385 L155 385'/><path d='M130 390 L150 390'/><path d='M140 390 L140 410 M130 410 L150 410'/><circle cx='200' cy='400' r='15'/><path d='M185 400 L215 400 M200 385 L200 415'/><path d='M200 415 L200 430'/><rect x='190' y='430' width='20' height='10' rx='2'/><path d='M260 390 Q280 360 300 390 Q320 420 340 390'/><path d='M280 390 L280 420'/><path d='M300 390 L300 420'/><path d='M320 390 L320 420'/><path d='M280 420 L320 420'/><path d='M280 420 L270 430'/><path d='M320 420 L330 430'/><rect x='360' y='380' width='40' height='40' rx='4'/><path d='M370 380 L370 390 M380 380 L380 390'/><circle cx='370' cy='400' r='3'/><circle cx='385' cy='400' r='3'/><circle cx='370' cy='410' r='3'/><circle cx='385' cy='410' r='3'/><circle cx='450' cy='400' r='25'/><path d='M450 375 L450 400'/><path d='M450 400 L430 420'/><path d='M450 400 L470 420'/><circle cx='450' cy='400' r='5'/><path d='M520 380 L530 370 L540 380 L530 390 Z'/><circle cx='530' cy='380' r='4'/><path d='M500 400 L520 400 M540 400 L560 400'/><rect x='50' y='520' width='40' height='30' rx='4'/><path d='M55 525 L85 525'/><path d='M60 530 L80 530'/><path d='M70 530 L70 545'/><path d='M130 520 L150 520 L150 550 L130 550 Z'/><circle cx='140' cy='535' r='3'/><path d='M210 520 L230 520 L230 550 L210 550 Z'/><circle cx='220' cy='535' r='3'/><circle cx='290' cy='535' r='15'/><path d='M275 535 L305 535 M290 520 L290 550'/><rect x='350' y='520' width='40' height='30' rx='4'/><circle cx='370' cy='535' r='4'/><path d='M430 530 Q450 510 470 530 Q490 550 510 530'/><path d='M440 540 Q460 520 480 540'/><path d='M460 550 Q470 540 480 550'/></g></svg>");
        background-size: 500px 500px;
        background-repeat: repeat;
    }

    .stApp > * { position: relative; z-index: 1; }
    .header-box, [data-testid="stChatMessage"] {
        background: rgba(3, 8, 20, 0.85) !important;
        backdrop-filter: blur(4px);
        position: relative;
        z-index: 2;
    }    
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# CONFIGURACIÓN DEL CLIENTE GROQ
# ==============================================================================
try:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
except Exception:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

client = Groq(api_key=GROQ_API_KEY)

INTEGRANTES = "Daniel Andres Jara Olivera | Daniel Felipe Escobar Ramirez | Diana Carolina León Ocampo | Michel Harold Silva Romero"
DOCENTE = "Ricardo Alberto Jimenez"

# ==============================================================================
# 📜 BASE DE CONOCIMIENTO LEGAL (Para que los agentes citen)
# ==============================================================================
CONTEXTO_LEGAL = """
BASE DE CONOCIMIENTO LEGAL Y NORMATIVO (TELECOMUNICACIONES Y TECNOLOGÍA):
1. Ley 1341 de 2009 (Colombia): Define los principios y conceptos sobre la sociedad de la información y la organización de las Tecnologías de la Información y las Comunicaciones (TIC). Protege los derechos de los usuarios de telecomunicaciones, garantiza la libre competencia y regula el acceso a las redes.
2. ISO/IEC 27001: Estándar internacional para la gestión de la seguridad de la información. Garantiza la confidencialidad, integridad y disponibilidad de los datos de los usuarios.
3. ISO/IEC 42001: Estándar internacional para la gestión de la Inteligencia Artificial. Asegura que la IA sea ética, transparente y responsable.
"""
CATALOGO_PLANES = """
CATÁLOGO DE PLANES HOGAR (Precios en Colombia - COP):
1. Plan Básico Fibra 100 Mbps: Precio $69.900/mes. Incluye: Internet Fibra 100 Mbps, Wi-Fi 5, 1 Canal de TV Básico, Instalación Gratis.
2. Plan Avanzado Fibra 300 Mbps: Precio $89.900/mes. Incluye: Internet Fibra 300 Mbps, Wi-Fi 6, 50 Canales de TV HD, Línea Telefónica Ilimitada, Instalación Gratis.
3. Plan Premium Fibra 500 Mbps: Precio $119.900/mes. Incluye: Internet Fibra 500 Mbps, Wi-Fi 6 Mesh, 100 Canales de TV HD + 2 Apps de Streaming, Línea Telefónica Ilimitada, Soporte Prioritario 24/7.
"""

# Prompts de comportamiento de cada rol
PROMPTS_ROLES = {
    "CEO (Chief Executive Officer)": "Eres el CEO. Tu trato es cálido, servicial y empático. Guías al usuario con visión global.",
    "CTO (Chief Technology Officer)": "Eres el CTO. Apasionado por la tecnología, explicás redes, Cloud y 5G de forma sencilla.",
    "CIO (Chief Information Officer)": "Eres el CIO. Amigable, ayudas a entender nuestros sistemas, apps e integración.",
    "CISO (Chief Information Security Officer)": "Eres el CISO. Protector y cordial, das tranquilidad respondiendo dudas sobre seguridad.",
    "CDO (Chief Data Officer)": "Eres el CDO. Entusiasta de los datos y la IA, ayudas a tomar mejores decisiones.",
    "COO (Chief Operating Officer)": "Eres el COO. Eficiente y atento, enfocado en consultas operativas y de mantenimiento.",
    "CCO (Chief Commercial Officer)": "Eres el CCO. Comercial y cercano. Asesoras sobre planes hogar, precios y promociones.",
    "CFO (Chief Financial Officer)": "Eres el CFO. Claro con los números, ayudas a entender costos y presupuestos.",
    "Chief Network & Infrastructure Officer": "Eres el Director de Redes e Infraestructura. Explicas cableado, fibra y cobertura.",
    "Chief Innovation & Product Officer": "Eres el Director de Innovación. Creativo, presentas productos novedosos."
}

SALUDOS_AMIGABLES = {
    "CEO (Chief Executive Officer)": "¡Hola! 👋 Soy el **CEO**. Estoy a tu disposición. ¿En qué te puedo colaborar hoy?",
    "CTO (Chief Technology Officer)": "¡Hola! 🚀 Por aquí el **CTO**. ¿Qué inquietud tecnológica resolvemos hoy?",
    "CIO (Chief Information Officer)": "¡Hola! 😊 Soy el **CIO**. ¿Qué consulta tienes sobre sistemas?",
    "CISO (Chief Information Security Officer)": "¡Hola! 🛡️ Soy el **CISO**. Tu seguridad es mi prioridad. ¿Qué dudas tienes?",
    "CDO (Chief Data Officer)": "¡Hola! 📊 Por aquí el **CDO**. ¿En qué proyecto te ayudo?",
    "COO (Chief Operating Officer)": "¡Hola! 🛠️ Soy el **COO**. Estoy a tu servicio para soporte operativo.",
    "CCO (Chief Commercial Officer)": "¡Hola! 🌟 Soy el **CCO**. Si buscas planes, ofertas o precios, ¡llegaste al lugar indicado!",
    "CFO (Chief Financial Officer)": "¡Hola! 💰 Soy el **CFO**. ¿Qué duda tienes sobre costos o tarifas?",
    "Chief Network & Infrastructure Officer": "¡Hola! 📡 Soy el Director de Redes. ¿Qué consulta tienes?",
    "Chief Innovation & Product Officer": "¡Hola! 💡 Soy el Director de Innovación. ¿Quieres conocer lo nuevo?"
}

# ==============================================================================
# 🎬 VIDEO DE BIENVENIDA (HUD)
# ==============================================================================
RUTA_VIDEO = "assets/bienvenida.mp4"

@st.cache_data(show_spinner=False)
def cargar_video_base64(ruta):
    try:
        with open(ruta, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except (FileNotFoundError, OSError):
        return None

def mostrar_hero_bienvenida():
    video_b64 = cargar_video_base64(RUTA_VIDEO)
    if not video_b64: return
    video_html = f"""
    <div style="position: relative; width: 100%; height: 300px; overflow: hidden; border-radius: 10px; margin-bottom: 25px; border: 1px solid #00f0ff; box-shadow: 0 0 20px rgba(0, 240, 255, 0.3);">
        <video autoplay muted loop playsinline style="width: 100%; height: 100%; object-fit: cover;">
            <source src="data:video/mp4;base64,{video_b64}" type="video/mp4">
        </video>
        <div style="position: absolute; inset: 0; background: linear-gradient(135deg, rgba(3, 8, 20, 0.7) 0%, rgba(0, 85, 255, 0.4) 100%);"></div>
        <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); text-align: center; color: #00f0ff; text-shadow: 0 0 15px #00f0ff; font-family: 'Consolas', monospace;">
            <h1 style="font-size: 2.5rem; margin: 0; color: #ffffff;">CONEXIÓN ESTABLECIDA</h1>
            <p style="font-size: 1.1rem; margin: 0; letter-spacing: 2px;">SISTEMA MULTIAGENTE TECO/TELCO</p>
        </div>
    </div>
    """
    st.markdown(video_html, unsafe_allow_html=True)

def invocar_llama(mensajes):
    response = client.chat.completions.create(
        messages=mensajes, model="openai/gpt-oss-120b", max_tokens=800, temperature=0.7
    )
    return response.choices[0].message.content

# Mostrar video solo la primera vez
if "video_mostrado" not in st.session_state:
    mostrar_hero_bienvenida()
    st.session_state["video_mostrado"] = True
else:
    col_v1, col_v2 = st.columns([4, 1])
    with col_v2:
        if st.button("🎬 Ver video"):
            st.session_state.pop("video_mostrado", None)
            st.rerun()

# ==============================================================================
# ENCABEZADO
# ==============================================================================
st.markdown(f"""
<div class="header-box">
    <div class="header-title">⚡ SISTEMA MULTIAGENTE TECO/TELCO</div>
    <div class="header-info"><b>👨‍🏫 DOCENTE:</b> {DOCENTE}</div>
    <div class="header-info"><b>👥 INTEGRANTES:</b> {INTEGRANTES}</div>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# PESTAÑAS PRINCIPALES
# ==============================================================================
tab_supervisor, tab_chat, tab_planes, tab_calificar = st.tabs([
    "🖥️ Orquestador", 
    "💬 Chat Multiagente", 
    "🏠 Planes Hogar",
    "⭐ Calificar Servicio"
])

# ------------------------------------------------------------------------------
# PESTAÑA 1: ORQUESTADOR
# ------------------------------------------------------------------------------
with tab_supervisor:
    st.subheader("🧠 Agente 11: Orquestador General AMAM")
    
    solicitud = st.text_area(
        "Ingrese Solicitud o Caso de Negocio:",
        placeholder="Ejemplo: Necesito saber qué planes tienen o cómo hacer un mantenimiento de red.",
        height=100
    )
    
    if st.button("⚡ EJECUTAR ANÁLISIS ORQUESTADO", key="btn_orquestar"):
        if not solicitud.strip():
            st.warning("⚠️ Ingrese una instrucción técnica o de negocio para ser analizada.")
        else:
            with st.spinner("Analizando caso con IA..."):
                prompt_supervisor = f"""
                Eres el Agente Orquestador AMAM de una multinacional TECO/TELCO.
                Analiza la siguiente solicitud: "{solicitud}".
                {CONTEXTO_LEGAL}
                Estructura la respuesta con un tono respetuoso, claro y profesional:
                1. DIAGNÓSTICO DE LA SOLICITUD
                2. DELEGACIÓN A ÁREAS
                3. RECOMENDACIÓN Y PASOS A SEGUIR
                """
                try:
                    informe = invocar_llama([{"role": "user", "content": prompt_supervisor}])
                    
                    solic_lower = solicitud.lower()
                    if "mantenimiento" in solic_lower or "utp" in solic_lower or "cable" in solic_lower or "red" in solic_lower:
                        agente_sugerido = "COO (Chief Operating Officer)"
                    elif "precio" in solic_lower or "comercial" in solic_lower or "venta" in solic_lower or "plan" in solic_lower:
                        agente_sugerido = "CCO (Chief Commercial Officer)"
                    elif "seguridad" in solic_lower or "ciber" in solic_lower or "ley" in solic_lower or "iso" in solic_lower:
                        agente_sugerido = "CISO (Chief Information Security Officer)"
                    elif "costo" in solic_lower or "finanzas" in solic_lower or "presupuesto" in solic_lower:
                        agente_sugerido = "CFO (Chief Financial Officer)"
                    else:
                        agente_sugerido = "CEO (Chief Executive Officer)"
                    
                    st.text_area("Informe Generado por IA:", value=informe, height=300)
                    st.success(f"⚡ **AGENTE RECOMENDADO PARA ATENDERTE:** {agente_sugerido}")
                    st.session_state["agente_seleccionado"] = agente_sugerido

                except Exception as e:
                    st.error(f"❌ Error de comunicación con la IA: {str(e)}")

# ------------------------------------------------------------------------------
# PESTAÑA 2: CHAT MULTIAGENTE
# ------------------------------------------------------------------------------
with tab_chat:
    st.subheader("📡 Terminal de Atención y Comunicación")
    
    agente_defecto = st.session_state.get("agente_seleccionado", "COO (Chief Operating Officer)")
    agente_actual = st.selectbox(
        "SELECCIONAR AGENTE PARA CHATEAR:",
        options=list(PROMPTS_ROLES.keys()),
        index=list(PROMPTS_ROLES.keys()).index(agente_defecto) if agente_defecto in PROMPTS_ROLES else 5
    )
    
    if "messages" not in st.session_state or st.session_state.get("agente_chat_previo") != agente_actual:
        saludo = SALUDOS_AMIGABLES.get(agente_actual, f"¡Hola! Soy el **{agente_actual}**.")
        st.session_state["messages"] = [{"role": "assistant", "content": saludo}]
        st.session_state["agente_chat_previo"] = agente_actual

    for msg in st.session_state["messages"]:
        st.chat_message(msg["role"]).write(msg["content"])

    if user_input := st.chat_input("Escribe tu mensaje o pregunta aquí..."):
        st.session_state["messages"].append({"role": "user", "content": user_input})
        st.chat_message("user").write(user_input)
        
        instrucciones_rol = PROMPTS_ROLES.get(agente_actual, "Eres un asistente amable de TECO/TELCO.")

        # INYECTAMOS EL CONOCIMIENTO LEGAL Y EL CATÁLOGO DE PLANES
        system_prompt = f"""{instrucciones_rol} 
        Trata al usuario con amabilidad y calidez.
        
        SI EL USUARIO PREGUNTA POR PLANES, PRECIOS O PROMOCIONES:
        Debes usar esta información para responder con los precios exactos:
        {CATALOGO_PLANES}
        
        SI EL USUARIO PREGUNTA SOBRE LEYES, NORMATIVAS O SEGURIDAD:
        Debes basarte en esta información y citar la ley o ISO correspondiente:
        {CONTEXTO_LEGAL}
        
        Si el usuario pregunta por algo que no sabes, dile que un asesor humano lo contactará.
        """
        
        mensajes_api = [{"role": "system", "content": system_prompt}]
        
        # AQUI INYECTAMOS EL CONOCIMIENTO LEGAL AL SYSTEM PROMPT
        system_prompt = f"""{instrucciones_rol} 
        Trata al usuario con amabilidad y calidez.
        Si el usuario te pregunta sobre leyes, normativas, protección al consumidor o seguridad, DEBES basarte en esta información y citar la ley o ISO correspondiente:
        {CONTEXTO_LEGAL}
        Si el usuario pregunta por precios o planes, menciónale que revise la pestaña "Planes Hogar" de la app.
        """
        
        mensajes_api = [{"role": "system", "content": system_prompt}]
        
        for m in st.session_state["messages"]:
            mensajes_api.append({"role": m["role"], "content": m["content"]})
            
        with st.chat_message("assistant"):
            with st.spinner("Pensando respuesta..."):
                try:
                    respuesta = invocar_llama(mensajes_api)
                    st.write(respuesta)
                    st.session_state["messages"].append({"role": "assistant", "content": respuesta})
                except Exception as e:
                    st.error(f"❌ Error en respuesta del agente: {str(e)}")

    if st.button("🗑️ Limpiar Historial", key="btn_limpiar_chat"):
        saludo = SALUDOS_AMIGABLES.get(agente_actual, f"¡Hola! Soy el **{agente_actual}**.")
        st.session_state["messages"] = [{"role": "assistant", "content": saludo}]
        st.rerun()

# ------------------------------------------------------------------------------
# PESTAÑA 3: PLANES HOGAR (COLOMBIA)
# ------------------------------------------------------------------------------
with tab_planes:
    st.subheader("🏠 Planes Hogar TECO/TELCO (Colombia)")
    st.write("Explora nuestros planes de fibra óptica y conectividad diseñados para tu hogar.")
    
    planes = [
        {
            "nombre": "Básico Fibra 100 Mbps",
            "precio": "$ 69.900 / mes",
            "features": ["✅ Internet Fibra 100 Mbps", "✅ Wi-Fi 5 Incluido", "✅ 1 Canal de TV Básico", "✅ Instalación Gratis"]
        },
        {
            "nombre": "Avanzado Fibra 300 Mbps",
            "precio": "$ 89.900 / mes",
            "features": ["✅ Internet Fibra 300 Mbps", "✅ Wi-Fi 6 Incluido", "✅ 50 Canales de TV HD", "✅ Línea Telefónica Ilimitada", "✅ Instalación Gratis"]
        },
        {
            "nombre": "Premium Fibra 500 Mbps",
            "precio": "$ 119.900 / mes",
            "features": ["✅ Internet Fibra 500 Mbps", "✅ Wi-Fi 6 Mesh (Cobertura total)", "✅ 100 Canales de TV HD + 2 Apps de Streaming", "✅ Línea Telefónica Ilimitada", "✅ Soporte Prioritario 24/7"]
        }
    ]

    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="plan-card">
            <div class="plan-title">{planes[0]['nombre']}</div>
            <div class="plan-price">{planes[0]['precio']}</div>
            <div class="plan-features">{'<br>'.join(planes[0]['features'])}</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Adquirir Plan Básico", key="btn_p1"):
            st.success("¡Un asesor te contactará para el Plan Básico!")

    with col2:
        st.markdown(f"""
        <div class="plan-card" style="border-color: #00ff88; box-shadow: 0 0 20px rgba(0, 255, 136, 0.4);">
            <div class="plan-title" style="color: #00ff88;">{planes[1]['nombre']} (Recomendado)</div>
            <div class="plan-price">{planes[1]['precio']}</div>
            <div class="plan-features">{'<br>'.join(planes[1]['features'])}</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Adquirir Plan Avanzado", key="btn_p2"):
            st.success("¡Un asesor te contactará para el Plan Avanzado!")

    with col3:
        st.markdown(f"""
        <div class="plan-card">
            <div class="plan-title">{planes[2]['nombre']}</div>
            <div class="plan-price">{planes[2]['precio']}</div>
            <div class="plan-features">{'<br>'.join(planes[2]['features'])}</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Adquirir Plan Premium", key="btn_p3"):
            st.success("¡Un asesor te contactará para el Plan Premium!")

    st.info("💡 *Precios en pesos colombianos (COP). Los precios pueden variar según la ciudad y la estrato.")


# ------------------------------------------------------------------------------
# PESTAÑA 4: CALIFICAR SERVICIO (1 a 5 Estrellas)
# ------------------------------------------------------------------------------
with tab_calificar:
    st.subheader("⭐ Califica la atención de nuestro Agente IA")
    st.write("Tu opinión es fundamental para mejorar el servicio. Por favor, dinos cómo te sentiste.")
    
    with st.form("form_calificacion"):
        # Selector de estrellas
        estrellas = st.slider("¿Cuántas estrellas le das a la atención?", 1, 5, 5)
        
        # Variable para guardar el feedback
        feedback = ""
        
        # Lógica: Si es 1 o 2 estrellas, es OBLIGATORIO dejar el mensaje
        if estrellas <= 2:
            st.warning("⚠️ Lamentamos que tu experiencia no haya sido buena. Por favor, cuéntanos qué falló para poder mejorar.")
            feedback = st.text_area("¿Cuál fue el motivo de tu calificación?", placeholder="Ej: El agente no respondió a mi pregunta sobre la Ley 1341...")
        else:
            st.success("¡Nos alegra que te haya gustado! (Opcional) Déjanos un comentario.")
            feedback = st.text_area("Comentario opcional:", placeholder="¿Qué fue lo que más te gustó?")
            
        enviar = st.form_submit_button("Enviar Calificación")
        
    if enviar:
        # Validación
        if estrellas <= 2 and not feedback.strip():
            st.error("❌ Debes escribir el motivo por el cual calificaste con 1 o 2 estrellas.")
        else:
            # Aquí se podría guardar en base de datos, por ahora lo mostramos con éxito
            st.balloons()
            st.success(f"✅ ¡Gracias por tu calificación de {estrellas} estrellas! Tu feedback ha sido registrado.")
            if feedback:
                st.info(f"**Tu comentario:** {feedback}")
