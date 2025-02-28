import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

##########################
# Función de Codificación
##########################
def convolutional_encode(bits, poly1="111", poly2="101"):
    """
    Codifica una secuencia de bits usando un código convolucional
    de tasa 1/2, memoria = 2, polinomios en binario (string).
    No se aplica flushing.
    """
    g1 = [int(b) for b in poly1]
    g2 = [int(b) for b in poly2]
    R1, R2 = 0, 0
    output = []

    for b in bits:
        bit_actual = int(b)
        y1 = (bit_actual * g1[0]) ^ (R1 * g1[1]) ^ (R2 * g1[2])
        y2 = (bit_actual * g2[0]) ^ (R1 * g2[1]) ^ (R2 * g2[2])
        output.extend([str(y1), str(y2)])
        R2 = R1
        R1 = bit_actual

    return "".join(output)

##########################
# Decodificador Viterbi
##########################
def viterbi_decode(coded_bits, poly1="111", poly2="101"):
    """
    Decodifica los bits codificados usando Viterbi.
    Asumimos misma configuración: tasa 1/2, memoria=2.
    """
    g1 = [int(b) for b in poly1]
    g2 = [int(b) for b in poly2]
    states = ['00','01','10','11']

    def next_state_output(state, bit_in):
        R1 = int(state[0])
        R2 = int(state[1])
        y1 = (bit_in*g1[0]) ^ (R1*g1[1]) ^ (R2*g1[2])
        y2 = (bit_in*g2[0]) ^ (R1*g2[1]) ^ (R2*g2[2])
        new_state = f"{bit_in}{R1}"
        return new_state, f"{y1}{y2}"

    pairs = [coded_bits[i:i+2] for i in range(0,len(coded_bits),2)]
    INF = float('inf')
    metric_prev = {s: (0.0 if s == '00' else INF, []) for s in states}

    for received in pairs:
        metric_current = {s: (INF, []) for s in states}
        for s in states:
            current_metric, current_path = metric_prev[s]
            for bit_in in [0, 1]:
                new_s, out = next_state_output(s, bit_in)
                dist = sum(a != b for a, b in zip(out, received))
                candidate_metric = current_metric + dist
                if candidate_metric < metric_current[new_s][0]:
                    new_path = current_path + [bit_in]
                    metric_current[new_s] = (candidate_metric, new_path)
        metric_prev = metric_current

    best_state = min(metric_prev, key=lambda s: metric_prev[s][0])
    return "".join(map(str, metric_prev[best_state][1]))



def draw_trellis(bits, g1, g2):
    import matplotlib.pyplot as plt
    import streamlit as st
    
    encoded_bits = convolutional_encode(bits, g1, g2)

    fig, ax = plt.subplots(figsize=(12, 8))
    states = ['00', '01', '10', '11']
    n_steps = len(bits) + 1
    state_positions = {state: i for i, state in enumerate(states)}

    for step in range(n_steps):
        for state in states:
            ax.scatter(step, state_positions[state], color='black')
            ax.text(step, state_positions[state], state, fontsize=12, ha='center', va='bottom')

    current_state = '00'
    path = [(0, state_positions[current_state])]
    output_symbols = []

    for step, (bit, output) in enumerate(zip(bits, encoded_bits)):
        next_state_0 = f"0{current_state[0]}"[-2:]
        next_state_1 = f"1{current_state[0]}"[-2:]

        # Obtener las salidas para las transiciones (0 y 1)
        output_0 = convolutional_encode([0], g1, g2)[0]
        output_1 = convolutional_encode([1], g1, g2)[0]

        # Dibujar transiciones posibles
        ax.annotate(f"{output_0}", ((step + 0.5), (state_positions[next_state_0] + state_positions[current_state]) / 2), color='gray')
        ax.annotate(f"{output_1}", ((step + 0.5), (state_positions[next_state_1] + state_positions[current_state]) / 2), color='gray')

        ax.plot([step, step + 1], [state_positions[current_state], state_positions[next_state_0]], 'gray', linestyle='--')
        ax.plot([step, step + 1], [state_positions[current_state], state_positions[next_state_1]], 'gray', linestyle='--')

        next_state = next_state_0 if bit == 0 else next_state_1
        output_symbols.append(output)
        path.append((step + 1, state_positions[next_state]))
        current_state = next_state

    x_coords, y_coords = zip(*path)
    ax.plot(x_coords, y_coords, marker='o', color='blue', linewidth=2)

    ax.set_xticks(range(n_steps))
    ax.set_yticks(range(len(states)))
    ax.set_yticklabels(states)
    ax.set_xlabel('Pasos')
    ax.set_ylabel('Estados')
    ax.grid(True)
    st.pyplot(fig)
    

    
  
    
            




##########################
# STREAMLIT APP
##########################
def main():
    st.set_page_config(page_title="Codificación Convolucional", layout="wide")
    st.title("Codificación Convolucional y Decodificación Viterbi")

    # Campos principales (tal como en la imagen)
    user_bits = st.text_input("Secuencia entrada", "11011")
    bits = [int(b) for b in user_bits] + [0]
    poly1 = st.text_input("Polinomio G1", "111")
    poly2 = st.text_input("Polinomio G2", "101")

    error_sim = st.checkbox("Simular errores")
    error_pos = st.text_input("Posiciones de error (separadas por coma)", "0,2")

    if st.button("Codificar/Decodificar"):
        # Validación
        if not all(c in '01' for c in user_bits):
            st.error("¡Entrada inválida! Solo se permiten 0s y 1s.")
            return

        # Codificación
        coded = convolutional_encode(user_bits, poly1, poly2)
        original_coded = coded

        # Simular errores si se desea
        if error_sim:
            coded_list = list(coded)
            try:
                positions = [int(p) for p in error_pos.split(',')]
            except ValueError:
                positions = []
            for pos in positions:
                if 0 <= pos < len(coded_list):
                    coded_list[pos] = '1' if coded_list[pos] == '0' else '0'
            coded = "".join(coded_list)

        # Decodificación
        decoded = viterbi_decode(coded, poly1, poly2)

        # Muestra de resultados
        st.subheader("Resultados")
        col_res1, col_res2, col_res3 = st.columns(3)
        col_res1.metric("Secuencia codificada", coded)
        col_res2.metric("Secuencia decodificada", decoded)
        col_res3.metric("Entrada original", user_bits)

        # Mensaje final
        if decoded == user_bits:
            st.success("Decodificación correcta (coincide)!")
        else:
            st.warning("La decodificación no coincide con la entrada original.")

 
        draw_trellis(bits, poly1, poly2)
        st.metric("Secuencia codificada:" ,coded)

if __name__ == "__main__":
    main()
