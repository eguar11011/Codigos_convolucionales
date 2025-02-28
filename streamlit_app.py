import streamlit as st

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

##########################
# STREAMLIT APP
##########################
def main():
    st.set_page_config(page_title="Codificación Convolucional", layout="wide")
    st.title("Codificación Convolucional y Decodificación Viterbi")

    # Campos principales (tal como en la imagen)
    user_bits = st.text_input("Secuencia entrada", "11011")
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

if __name__ == "__main__":
    main()
