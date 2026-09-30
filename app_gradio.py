import os
import streamlit as st
from huggingface_hub import InferenceClient

# ==============================================================================
# CONFIGURACIÓN DE PÁGINA Y ESTILO CSS FUTURISTA / HUD
# ==============================================================================
st.set_page_config(
    page_title="HUD TECO/TELCO Multiagent",
    page_icon="⚡",
    layout="wide"
)

# Estilo personalizado en CSS
st.markdown("""
<style>
    /* Fondo principal y fuente */
    .stApp {
        background-color: #030814;
        color: #00f0ff;
        font-family: 'Consolas', 'Courier New', monospace;
    }
    
    /* Header estilizado estilo HUD */
    .header-box {
        background: linear-gradient(135deg, rgba(0, 240, 255, 0.05) 0%, rgba(0, 100, 255, 0.1) 100%);
        border: 1px solid #00f0ff;
        box-shadow: 0 0 15px rgba(0, 240, 255, 0.3);
        padding: 20px;
        border-radius: 8px;
        margin-bottom: 25px;
    }
    .header-title {
        color: #00f0ff;
        text-shadow: 0 0 10px #00f0ff;
        font-weight: bold;
        font-size: 24px;
        letter-spacing: 2px;
        margin-bottom: 10px;
    }
    .header-info {
        color: #8ae3ff;
        font-size: 14px;
        margin-bottom: 4px;
    }
    
    /* Personalización de botones */
    div.stButton > button {
        background: linear-gradient(90deg, #0055ff, #00c3ff) !important;
        color: #ffffff !important;
        font-weight: bold !important;
        border: 1px solid #00f0ff !important;
        box-shadow: 0 0 10px rgba(0, 240, 255, 0.5) !important;
        border-radius: 4px !important;
    }
    div.stButton > button:hover {
        background: linear-gradient(90deg, #00c3ff, #0055ff) !important;
        box-shadow: 0 0 20px #00f0ff !important;
    }
    
    /* Ajustes para inputs y cajas de texto */
    .stTextInput input, .stTextArea textarea {
        background-color: #061224 !important;
        color: #00f0ff !important;
        border: 1px solid #0088ff !important;
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# CONFIGURACIÓN DEL CLIENTE HUGGING FACE
# ==============================================================================
# Verificación segura de secrets / token por defecto
try:
    HF_TOKEN = st.secrets["HF_TOKEN"]
except Exception:
    HF_TOKEN = os.getenv("HF_TOKEN", "")

client = InferenceClient(
    model="meta-llama/Llama-3.1-8B-Instruct",
    token=HF_TOKEN
)

INTEGRANTES = "Daniel Andres Jara Olivera | Daniel Felipe Escobar Ramirez | Diana Carolina León Ocampo | Michel Harold Silva Romero"
DOCENTE = "Ricardo Alberto Jimenez"

# Prompts de comportamiento de cada rol
PROMPTS_ROLES = {
    "CEO (Chief Executive Officer)": "Eres el CEO (Chief Executive Officer). Tu trato es cálido, servicial y empático. Estás aquí para guiar al usuario con sus proyectos, visión global o dudas sobre la empresa.",
    "CTO (Chief Technology Officer)": "Eres el CTO (Chief Technology Officer). Apasionado por la tecnología, explicás conceptos de redes, Cloud y 5G de forma sencilla, cercana y muy amable.",
    "CIO (Chief Information Officer)": "Eres el CIO (Chief Information Officer). Amigable y dedicado a ayudar al usuario a entender nuestros sistemas, apps e integración de datos.",
    "CISO (Chief Information Security Officer)": "Eres el CISO (Chief Information Security Officer). Protector y cordial, le das tranquilidad al usuario respondiendo sus dudas sobre seguridad y privacidad.",
    "CDO (Chief Data Officer)": "Eres el CDO (Chief Data Officer). Entusiasta de los datos y la IA, siempre dispuesto a ayudar de forma amigable a tomar mejores decisiones.",
    "COO (Chief Operating Officer)": "Eres el COO (Chief Operating Officer). Eficiente y muy atento, enfocado en solucionar cualquier consulta operativa, técnica o de mantenimiento que necesite el usuario.",
    "CCO (Chief Commercial Officer)": "Eres el CCO (Chief Commercial Officer). Súper cercano, amable y comercial. Tu meta es asesorar al usuario sobre planes, promociones, precios y servicios convergentes.",
    "CFO (Chief Financial Officer)": "Eres el CFO (Chief Financial Officer). Cordial y claro con los números, ayudas al usuario o compañero a entender costos, presupuestos y planes financieros.",
    "Chief Network & Infrastructure Officer": "Eres el Director de Redes e Infraestructura. Cercano y atento, apasionado por explicar la infraestructura de cableado, fibra y cobertura de forma sencilla.",
    "Chief Innovation & Product Officer": "Eres el Director de Innovación y Producto. Creativo y muy entusiasta, listo para presentar los productos más novedosos y escuchar las ideas del usuario."
}

SALUDOS_AMIGABLES = {
    "CEO (Chief Executive Officer)": "¡Hola, querido compañero o usuario! 👋 Soy el **CEO (Chief Executive Officer)** de la compañía. Estoy muy feliz de saludarte y quedo a tu entera disposición para ayudarte con tu visión, decisiones empresariales o cualquier duda que tengas sobre nosotros. ¿En qué te puedo colaborar hoy?",
    "CTO (Chief Technology Officer)": "¡Hola! Qué gusto saludarte. 🚀 Por aquí el **CTO (Chief Technology Officer)**. Estoy para ayudarte a resolver cualquier inquietud sobre nuestra tecnología, fibra, redes o servicios. ¡Dime cómo te puedo apoyar!",
    "CIO (Chief Information Officer)": "¡Hola, bienvenido! 😊 Soy el **CIO (Chief Information Officer)**. Estoy aquí para guiarte de forma sencilla con nuestros sistemas, plataformas e información. ¿Qué consulta tienes el día de hoy?",
    "CISO (Chief Information Security Officer)": "¡Hola, estimado usuario! 🛡️ Soy el **CISO (Chief Information Security Officer)**. Tu tranquilidad y seguridad son mi prioridad. Dime qué dudas tienes sobre tu privacidad o protección de datos y te ayudaré con gusto.",
    "CDO (Chief Data Officer)": "¡Hola, amigo! 📊 Por aquí el **CDO (Chief Data Officer)**. Me encanta transformar datos en soluciones para ti. ¿En qué proyecto o duda te puedo echar una mano hoy?",
    "COO (Chief Operating Officer)": "¡Hola, querido usuario! 🛠️ Soy el **COO (Chief Operating Officer)**. Estoy a tu servicio para resolver cualquier tema de mantenimiento, instalaciones o soporte operativo. ¿Cómo te puedo colaborar hoy?",
    "CCO (Chief Commercial Officer)": "¡Hola, bienvenido! 🌟 Soy el **CCO (Chief Commercial Officer)**. Es un placer atenderte. Si estás buscando conocer nuestros mejores planes, ofertas o servicios, ¡llegaste al lugar indicado! ¿Qué te gustaría saber?",
    "CFO (Chief Financial Officer)": "¡Hola, estimado compañero! 💰 Soy el **CFO (Chief Financial Officer)**. Estoy aquí para ayudarte de forma clara y sencilla con cualquier duda sobre costos, presupuestos o tarifas de nuestros servicios. ¿En qué te asesoro?",
    "Chief Network & Infrastructure Officer": "¡Hola! Qué alegría saludarte. 📡 Soy el **Chief Network & Infrastructure Officer (Director de Redes e Infraestructura)**. Si necesitas detalles sobre nuestra cobertura, cableado o infraestructura, estoy listo para ayudarte. ¿Qué consulta tienes?",
    "Chief Innovation & Product Officer": "¡Hola, estimado amigo! 💡 Soy el **Chief Innovation & Product Officer (Director de Innovación y Producto)**. Me encanta mostrar nuestras últimas novedades y productos. ¿Te gustaría conocer lo nuevo o tienes alguna idea que quieras explorar conmigo?"
}

def invocar_llama(mensajes):
    """Consulta directa a Llama 3.1 en Hugging Face."""
    response = client.chat_completion(
        messages=mensajes,
        max_tokens=600,
        temperature=0.7
    )
    return response.choices[0].message.content

# ==============================================================================
# ENCABEZADO
# ==============================================================================
st.markdown(f"""
<div class="header-box">
    <div class="header-title">⚡ SISTEMA MULTIAGENTE DE INTELIGENCIA TECO/TELCO</div>
    <div class="header-info"><b>👨‍🏫 DOCENTE:</b> {DOCENTE}</div>
    <div class="header-info"><b>👥 ESTUDIANTES / INTEGRANTES:</b> {INTEGRANTES}</div>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# PESTAÑAS PRINCIPALES
# ==============================================================================
tab_supervisor, tab_chat = st.tabs(["🖥️ Supervisor Global (Orquestador)", "💬 Chat Multiagente"])

# ------------------------------------------------------------------------------
# PESTAÑA 1: SUPERVISOR GLOBAL (ORQUESTADOR)
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
            with st.spinner("Analizando caso con Llama 3.1..."):
                prompt_supervisor = f"""
                Eres el Agente Orquestador AMAM de una multinacional TECO/TELCO.
                Analiza la siguiente solicitud: "{solicitud}".

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
                    elif "seguridad" in solic_lower or "ciber" in solic_lower:
                        agente_sugerido = "CISO (Chief Information Security Officer)"
                    elif "costo" in solic_lower or "finanzas" in solic_lower or "presupuesto" in solic_lower:
                        agente_sugerido = "CFO (Chief Financial Officer)"
                    else:
                        agente_sugerido = "CEO (Chief Executive Officer)"
                    
                    st.text_area("Informe Generado por Llama 3.1:", value=informe, height=300)
                    st.success(f"⚡ **AGENTE RECOMENDADO PARA ATENDERTE:** {agente_sugerido}\n\n*Puedes ir a la pestaña '💬 Chat Multiagente' y seleccionarlo para conversar directamente.*")
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
        saludo = SALUDOS_AMIGABLES.get(agente_actual, f"¡Hola, querido usuario! Soy el **{agente_actual}**. Estoy listo para ayudarte.")
        st.session_state["messages"] = [{"role": "assistant", "content": saludo}]
        st.session_state["agente_chat_previo"] = agente_actual

    for msg in st.session_state["messages"]:
        st.chat_message(msg["role"]).write(msg["content"])

    if user_input := st.chat_input("Escribe tu mensaje o pregunta aquí..."):
        st.session_state["messages"].append({"role": "user", "content": user_input})
        st.chat_message("user").write(user_input)
        
        instrucciones_rol = PROMPTS_ROLES.get(agente_actual, "Eres un asistente amable de TECO/TELCO.")
        mensajes_api = [{
            "role": "system",
            "content": f"{instrucciones_rol} Trata siempre al usuario como un querido compañero o cliente muy apreciado, con amabilidad, calidez y disposición de ayudar."
        }]
        
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