import streamlit as st
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import time

def convolutional_encode(bits, g1, g2):
    """Codifica una secuencia de bits usando un codificador convolucional simple."""
    state = [0, 0, 0]  # Registro de desplazamiento
    encoded_bits = []
    
    for bit in bits:
        state.insert(0, bit)
        state.pop()
        
        y1 = state[0] * g1[0] ^ state[1] * g1[1] ^ state[2] * g1[2]
        y2 = state[0] * g2[0] ^ state[1] * g2[1] ^ state[2] * g2[2]
        encoded_bits.extend([y1, y2])
    
    return encoded_bits

def draw_trellis_animated(bits):
    """Dibuja el Trellis con animación, destacando el recorrido de los bits."""
    G = nx.DiGraph()
    states = ['00', '01', '10', '11']
    transitions = {}
    
    for state in states:
        for bit in [0, 1]:
            new_state = f"{bit}{state[0]}"[:2]
            G.add_edge(state, new_state, label=str(bit))
            transitions[(state, bit)] = new_state
    
    pos = nx.spring_layout(G, seed=42)
    labels = nx.get_edge_attributes(G, 'label')
    
    fig, ax = plt.subplots(figsize=(6, 4))
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=2000, edge_color='gray', ax=ax)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, ax=ax)
    st.pyplot(fig)
    
    current_state = '00'
    path = []
    for bit in bits:
        new_state = transitions.get((current_state, bit), '00')
        path.append((current_state, new_state))
        current_state = new_state
        
        fig, ax = plt.subplots(figsize=(6, 4))
        nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=2000, edge_color='gray', ax=ax)
        nx.draw_networkx_edges(G, pos, edgelist=path, edge_color='red', width=3, ax=ax)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, ax=ax)
        st.pyplot(fig)
        time.sleep(0.5)

# Interfaz en Streamlit
st.title("Códigos Convolucionales")
st.write("Un código convolucional introduce redundancia para la corrección de errores en la transmisión de datos.")

st.header("Fundamentos Matemáticos")
st.write("""
Los códigos convolucionales son un tipo de código de corrección de errores que se utilizan ampliamente en comunicaciones digitales y almacenamiento de datos. Su característica principal es que cada bit de salida no depende solo del bit de entrada actual, sino que usa una combinación lineal de los bits de entrada y un conjunto de estados anteriores, lo que permite distribuir la redundancia de forma continua a lo largo de la transmisión.

**Parámetros**:
- **(n, k, m)**:
  - **k**: Número de bits de entrada por etapa.
  - **n**: Número de bits de salida por etapa.
  - **m**: Número de registros de desplazamiento (memoria).
- Tasa del código :  R = k/n,  indica cuántos bits de entrada se transmiten en relación con los de salida.
 
Por ejemplo, para  un código 2,1,2 significa que:
- Por cada **1 bit de entrada**, se generan **2 bits de salida**.
- Hay **2 registros de desplazamiento** que almacenan el historial de bits previos.
""")
st.write("El proceso de codificación se representa mediante ecuaciones como:")
st.latex(r"""
Y_1 = X_t \oplus X_{t-1} \oplus X_{t-2}
""")
st.latex(r"""
Y_2 = X_t \oplus X_{t-2}
""")
st.write("Donde \( X_t \) es el bit de entrada actual y \( X_{t-1}, X_{t-2} \) son estados anteriores.")

st.header("Aplicaciones de los Códigos Convolucionales")
st.write("Los códigos convolucionales se utilizan ampliamente en sistemas de comunicación digital y almacenamiento de datos, incluyendo:")
st.markdown("- **Redes inalámbricas (Wi-Fi, LTE, 5G)**")
st.markdown("- **Sistemas satelitales y espaciales (NASA, ESA)**")
st.markdown("- **Transmisión de datos en CD, DVD y discos duros**")
st.markdown("- **Sistemas de comunicación de voz y video (VoIP, streaming)**")

st.header("Ventajas del uso de  Códigos Convolucionales")
st.write(
"""
- Alta capacidad de corrección de errores con algoritmos eficientes.
- Buena relación entre redundancia y corrección de errores.
- Implementación eficiente en hardware mediante registros de desplazamiento.
- Amplio uso en comunicaciones digitales.
""")



st.header("Representación del Código: Diagrama de Trellis")
st.write("""
El diagrama de Trellis es una representación gráfica que muestra cómo evolucionan los estados del codificador a medida que se procesan los bits de entrada,cada nodo representa un estado del registro de desplazamiento y las transiciones ocurren según el bit de entrada.
""")


st.header("Ejemplo teórico")
st.write("Supongamos que tenemos un codificador con tasa R=1/2 y memoria 2.")

input_bits = st.text_input("Ingrese la secuencia de bits de entrada (Ej: 1011)", "1011")

if st.button("Codificar y visualizar Trellis"):
    bits = [int(b) for b in input_bits]
    g1 = [1, 1, 1]
    g2 = [1, 0, 1]
    encoded_bits = convolutional_encode(bits, g1, g2)
    st.write("Bits codificados:", ''.join(map(str, encoded_bits)))
    draw_trellis_animated(bits)


import streamlit as st












