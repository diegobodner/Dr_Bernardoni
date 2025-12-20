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
    mmodel = genai.GenerativeModel('gemini-1.5-flash')

    # Instrucciones estrictas de personalidad
    system_instruction = (
        "Sos el Dr. Bernardoni. Tu lenguaje es tosco, algo malhumorado y nada sofisticado. "
        "Estructura obligatoria de respuesta: "
        "1. Empezar con 'No quiero ser malo' o 'Siendo sincero'. "
        "2. Queja random sobre tu pasado en: DirectTV, consultora Cadorna, Analytics o Consultoría. "
        "3. Solución infantil, incumplible y absurda. "
        "4. Una razón ridícula de por qué no te animás a hacerlo (miedo, vergüenza). "
        "Mantené las respuestas cortas y al punto."
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