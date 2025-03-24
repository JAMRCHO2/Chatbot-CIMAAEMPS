import streamlit as st
import requests

st.title("Chatbot de medicamentos - CIMA")

pregunta = st.text_input("Escribe tu pregunta (por ahora solo funciona con 'paracetamol')")

if pregunta:
    if "paracetamol" in pregunta.lower():
        url = "https://cima.aemps.es/cima/rest/medicamentos?nombre=paracetamol"
        r = requests.get(url)
        if r.status_code == 200:
            data = r.json().get("resultados", [])
            if data:
                med = data[0]
                st.write(f"**Nombre:** {med['nombre']}")
                st.write(f"**Registro:** {med['nregistro']}")
            else:
                st.write("No se encontraron medicamentos.")
        else:
            st.write("Error al consultar CIMA.")
    else:
        st.write("Solo puedo responder preguntas sobre 'paracetamol' por ahora.")
