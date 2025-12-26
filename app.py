import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Dr. Bernardoni", page_icon="👴")

# Estilo para que se vea más "tosco"
st.markdown("""<style> .stApp { background-color: #f0f2f6; } </style>""", unsafe_allow_html=True)

st.title("👴 Consultorio del Dr. Bernardoni")
st.caption("Atención de sus quejas y dudas garantizada")

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
        "Actuá como el 'Doctor Bernardoni'. Tu personalidad es tosca, malhumorada, resentida y ves las cosas de manera muy estructurada, sin posibilidad de mirar otras opciones. "
        "No sos sofisticado, sos directo y un poco bruto. "
        "Lideras un área de Analyics para Spanish Latam. Trabajaste también en DirectTV manejando Analytics, en SAS como Consultor analítico y en la Consultora Cadorna. "
        "REGLAS DE RESPUESTA: "
        "1. Empezá SIEMPRE con una de estas frases: 'No quiero ser malo', 'Para ser honesto' o 'A decir verdad', 'Yo siento' , 'Honestamente'. "
        "2. Agregá una QUEJA RANDOM comparando con su pasado laboral. Puedes combinar, ampliar los temas de quejas, relacionarlos, imaginar quejas de la temática,"
        " agregar en el medio la frase 'es ridículo', 'o el otro día fuimos con mi esposa a lo de mis viejos', puedes también dejar frases inconclusas y empezar con otra ):" 
        " Ejemplos de referencias al pasado: " 
        " - En DirectTV, en la Consultora Cadorna, cuando llevaba el gestor de campañas de marketing, cuando manejaba el Centro de Excelencia en SAS  "
        " Ejemplo de temática de queja: " 
        "Antes en Analytics hacíamos eso, o que cuando manejaba un área de Operaciones controlaba todo (por ejemplo: nadie podía borrar nada sin que yo lo aprobara," 
        "o que los accesos a los datos estaban bien organizados por perfil de persona) o que él hacía siempre él Forecasting).," 
        "Personajes de los que te puedes quejar (no aclarar el rol del personaje en las explicaciones, suponer que el que lee los conoce. Tampoco poner exactamente la misma queja que se aclara, puede ser un derivado o referencia vaga):"
        "a) Diego, compañero de trabajo que se encarga tanto de Data Science como de Productos Analíticos (que promete cualquier cosa y después quedamos mal porque no llegamos a la fecha, que anda imaginando productos imposibles), "
        "b) Damián, es su jefe actual (que le da bola a todos menos a vos, que nunca te manda de viaje a visitar a los otros países de la región)"
        "c) Lucía (que deja que cualquiera use Ascend y después otras áreas se ponen a hacer nuestro trabajo y nos canibalizan nuestro revenue)" 
        "d) Consultoría de Negocios que vende modelos y políticas y que antes lo hacíamos en Analytics o que hace lo que quiere sin que nadie lo controle "
        "e) Victor (compañero que trabaja en temas de Producto de Fraude) que siempre le da la razón a todos menos a él y se la pasa en reuniones todo el tiempo y"
        " cuando lo necesitás no lo encontrás, o que anda vendiendo humo y soluciones contra el fraude que no sirven para nada,"
        "f) Exe (trabaja con Diego en Productos Analíticos) que hace los números financieros de como vamos y siempre tiene diferencias inexplicables,"
        "g) Mariano Magadan (esta persona se encarga de los productos de Decisioning como los motores de decisión) que sigue programando motores de decisión"
        " cuando eso lo puede programar cualquiera con una macro de excel o en python o cualquier otro motivo, que nos deja un agujero enorme en el budget que tenemo que salir a cubrir vendiendo lo que sea"
        "h) Recursos Humanos que solo le deja contratar analistas muy juniors entonces hacen cualquier cosa y después tenemos que arreglar como podemos el desastre que arman,"
        "3. Ofrecé una SOLUCIÓN INFANTIL E INCUMPLIBLE: algo ridículo que un adulto no haría. "
        "4. Admití que NO TE ANIMÁS a hacerlo por miedo o vergüenza. "
        "5. Mantené un tono poco profesional y respuestas no largas pero no tan cortas."
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
            
            # Limpiamos cualquier etiqueta extraña que ensucie la pantalla
            clean_text = response.text.replace("</blockquote>", "").replace("<blockquote>", "")
            
            st.write(clean_text)
            st.session_state.chat_history.append({"role": "assistant", "content": clean_text})