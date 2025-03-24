import streamlit as st
import requests

st.title("Chatbot de medicamentos - AEMPS CIMA")
st.write("Consulta cualquier medicamento autorizado en España.")

nombre = st.text_input("🔎 Escribe el nombre del medicamento")

def buscar_medicamento(nombre):
    url = f"https://cima.aemps.es/cima/rest/medicamentos?nombre={nombre}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get("resultados", [])
    return []

def obtener_info_detallada(nregistro):
    url = f"https://cima.aemps.es/cima/rest/medicamento/{nregistro}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return {}

if nombre:
    resultados = buscar_medicamento(nombre)
    
    if resultados:
        st.success(f"Se encontraron {len(resultados)} resultados. Mostrando el primero:")
        medicamento = resultados[0]
        detalle = obtener_info_detallada(medicamento["nregistro"])

        st.subheader(medicamento["nombre"])
        st.write(f"**Registro:** {medicamento['nregistro']}")
        st.write(f"**Código Nacional (CN):** {medicamento.get('cn')}")
        st.write(f"**Laboratorio:** {detalle.get('titular')}")
        st.write(f"**Estado de autorización:** {detalle.get('estado_autorizacion')}")
        st.write(f"**Vía de administración:** {detalle.get('viaAdministracion')}")
        st.write(f"**Principio activo:** {detalle.get('principiosActivos')}")
        
        if detalle.get("docs"):
            doc_links = detalle["docs"]
            for doc in doc_links:
                tipo = doc.get("tipoDocumento")
                enlace = f"https://cima.aemps.es/cima/dochtml/{doc.get('nombreArchivo')}"
                st.write(f"[{tipo}]({enlace})")
    else:
        st.warning("No se encontraron medicamentos con ese nombre.")
