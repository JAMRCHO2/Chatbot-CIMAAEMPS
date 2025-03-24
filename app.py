import requests
import streamlit as st

st.set_page_config(page_title="Chatbot Medicamentos CIMA", layout="centered")
st.title("💊 Chatbot de Medicamentos - CIMA")
st.write("Escribe el nombre de un medicamento autorizado en España y obtendrás información oficial del CIMA.")

nombre = st.text_input("🔎 ¿Qué medicamento quieres consultar?")

def buscar_medicamento(nombre):
    url = f"https://cima.aemps.es/cima/rest/medicamentos?nombre={nombre}"
    response = requests.get(url)
    if response.status_code == 200:
        resultados = response.json().get("resultados", [])
        if resultados:
            med = resultados[0]
            nregistro = med.get("nregistro")
            detalle_url = f"https://cima.aemps.es/cima/rest/medicamento/{nregistro}"
            detalle_resp = requests.get(detalle_url)
            if detalle_resp.status_code == 200:
                detalle = detalle_resp.json()
                return f"""
**💊 Nombre:** {med.get('nombre')}
**🔢 Registro:** {med.get('nregistro')}
**🏭 Laboratorio:** {detalle.get('titular')}
**🧬 Principio activo:** {detalle.get('principiosActivos')}
**💉 Vía de administración:** {detalle.get('viaAdministracion')}
**📄 Estado de autorización:** {detalle.get('estado_autorizacion')}

[📘 Ficha técnica]({"https://cima.aemps.es/cima/dochtml/" + detalle["docs"][0]["nombreArchivo"] if detalle.get("docs") else "No disponible"})
"""
        else:
            return "No se encontraron medicamentos con ese nombre."
    return "❌ Error al consultar la API del CIMA."

if nombre:
    respuesta = buscar_medicamento(nombre)
    st.markdown(respuesta)
