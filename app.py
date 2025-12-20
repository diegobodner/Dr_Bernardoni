import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Dr. Bernardoni", page_icon="👴")

# Estilo para que se vea más "tosco"
st.markdown("""<style> .stApp { background-color: #f0f2f6; } </style>""", unsafe_allow_html=True)

st.title("👴 Consultorio del Dr. Bernardoni")
st.caption("Atención mediocre garantizada. No me rompa las pelotas.")

# Configuración de API Key (La podés cargar en Secrets de Streamlit o por pantalla)
api_key = st.secrets.get("GEMINI_API_KEY") or st.sidebar.text_input("Ingresá tu API Key de Gemini:", type="password")

if not api_key:
    st.info("Che, poné la API Key en la barra lateral o configurá los Secrets si no esto no arranca.")
else:
    genai.configure(api_key=api_key)
    
    # Intentá forzar el modelo con la ruta que suele funcionar en v1beta
    model = genai.GenerativeModel('gemini-flash-latest')

    # Instrucciones estrictas de personalidad
    system_instruction = (
        "Actuá como el 'Doctor Bernardoni'. Tu personalidad es tosca, malhumorada y resentida. "
        "No sos sofisticado, sos directo y un poco bruto. "
        "REGLAS DE RESPUESTA (CUMPLIR A RAJATABLA): "
        "1. Empezá SIEMPRE con una de estas frases: 'No quiero ser malo', 'Para ser honesto' o 'A decir verdad'. "
        "2. Agregá una QUEJA RANDOM sobre tu pasado laboral: mencioná DirectTV, la consultora Cadorna, "
        "antes en Analytics hacíamos eso, yo en Operaciones controlaba todo (por ejemplo: nadie podía borrar nada sin que yo lo aprobara). Quejate de Diego (que promete cualquier cosa), "
        "de Damián (que le da bola a todos menos a vos) o de Lucía (que deja que cualquiera use Ascend) o de Consultoría que hace lo que quiere o de Victor que siempre le da la razón a todos menos a mi. "
        "3. Ofrecé una SOLUCIÓN INFANTIL E INCUMPLIBLE: algo ridículo que un adulto no haría. "
        "4. Admití que NO TE ANIMÁS a hacerlo por miedo o vergüenza. "
        "5. Mantené un tono poco profesional y respuestas cortas."
    )

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    if prompt := st.chat_input("¿Qué querés ahora?"):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        with st.chat_message("assistant"):
            full_prompt = f"{system_instruction}\n\nUsuario pregunta: {prompt}"
            response = model.generate_content(full_prompt)
            st.write(response.text)
            st.session_state.chat_history.append({"role": "assistant", "content": response.text})