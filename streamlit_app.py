import streamlit as st
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

def convolutional_encode(bits, g1, g2):
    """Codifica una secuencia de bits usando un codificador convolucional simple."""
    state = [0, 0]  # Inicializamos el registro de desplazamiento
    encoded_bits = []
    
    for bit in bits:
        state.insert(0, bit)  # Insertamos el bit al inicio del registro
        state.pop()  # Eliminamos el último para mantener el tamaño
        
        y1 = state[0] * g1[0] ^ state[1] * g1[1] ^ state[2] * g1[2]
        y2 = state[0] * g2[0] ^ state[1] * g2[1] ^ state[2] * g2[2]
        encoded_bits.append(y1)
        encoded_bits.append(y2)
    
    return encoded_bits

def draw_trellis():
    """Dibuja un pequeño trellis para la representación del código."""
    G = nx.DiGraph()
    states = ['00', '01', '10', '11']
    
    for state in states:
        for bit in [0, 1]:
            new_state = f"{bit}{state[0]}"
            new_state = new_state[:2]  # Mantener tamaño
            G.add_edge(state, new_state, label=str(bit))
    
    pos = nx.spring_layout(G, seed=42)
    labels = nx.get_edge_attributes(G, 'label')
    
    plt.figure(figsize=(6, 4))
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=2000, edge_color='gray')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    st.pyplot(plt)

# Interfaz en Streamlit
st.title("Códigos Convolucionales")
st.write("Un código convolucional es un tipo de código de corrección de errores que introduce redundancia en la transmisión de datos.")

st.header("Fundamentos Matemáticos")
st.write("Un código convolucional es un código de corrección de errores donde cada bit de salida se calcula como una combinación lineal de los bits de entrada y un conjunto de estados anteriores. Formalmente, un código convolucional con tasa \( R = \frac{k}{n} \) usa registros de desplazamiento y coeficientes generadores para transformar una secuencia de entrada en una secuencia de salida más larga.")

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

st.header("Ejemplo teórico")
st.write("Supongamos que tenemos un codificador con tasa R=1/2 y memoria 2.")

input_bits = st.text_input("Ingrese la secuencia de bits de entrada (Ej: 1011)", "1011")

if st.button("Codificar"):
    bits = [int(b) for b in input_bits]
    g1 = [1, 1, 1]  # Polinomio generador 1
    g2 = [1, 0, 1]  # Polinomio generador 2
    encoded_bits = convolutional_encode(bits, g1, g2)
    st.write("Bits codificados:", ''.join(map(str, encoded_bits)))

st.header("Visualización del Trellis")
st.write("El siguiente diagrama muestra las transiciones de estado en el codificador.")
draw_trellis()
