import pandas as pd
import random
import streamlit as st
import time

# Variables de estado para mantener los datos a través de las ejecuciones
if 'experiment_no' not in st.session_state:
    st.session_state['experiment_no'] = 0
if 'df_experiment_results' not in st.session_state:
    st.session_state['df_experiment_results'] = pd.DataFrame(columns=['no', 'iteraciones', 'suma_deseada', 'probabilidad_observada'])

st.header('Lanzar dos dados 🎲🎲')
st.markdown('¡Vamos a explorar la probabilidad de obtener una suma específica al lanzar dos dados!')

# -----------------
# Función de simulación
# -----------------
def roll_dice(n, target_sum):
    """
    Simula el lanzamiento de dos dados 'n' veces y visualiza la probabilidad de
    obtener una 'target_sum'.
    """
    roll_outcomes = []
    for _ in range(n):
        roll1 = random.randint(1, 6)
        roll2 = random.randint(1, 6)
        roll_outcomes.append(roll1 + roll2)

    target_sum_count = 0
    
    # Prepara el DataFrame inicial para el gráfico
    # El gráfico tendrá 11 puntos, uno para cada suma posible (del 2 al 12)
    chart_data = pd.DataFrame(data=[0.0] * 11, index=range(2, 13), columns=['Probabilidad'])
    chart = st.line_chart(chart_data)

    for i, r in enumerate(roll_outcomes):
        if r == target_sum:
            target_sum_count += 1
        
        prob = target_sum_count / (i + 1)
        
        # Actualiza solo la probabilidad de la suma deseada
        chart_data.loc[target_sum] = prob
        
        # Usa add_rows para actualizar el gráfico
        chart.add_rows(chart_data)
        
        # Pausa la ejecución para ver la animación
        time.sleep(0.05)

    return prob

# -----------------
# Interfaz de usuario
# -----------------
number_of_trials = st.slider('¿Número de lanzamientos?', 1, 1000, 10)
target_sum = st.selectbox('¿Qué suma quieres buscar?', options=range(2, 13))
start_button = st.button('Ejecutar simulación')

if start_button:
    st.write(f'Simulando {number_of_trials} lanzamientos, buscando la suma {target_sum}.')
    st.session_state['experiment_no'] += 1
    
    final_prob = roll_dice(number_of_trials, target_sum)
    
    # Crea un nuevo DataFrame para la fila del experimento actual
    new_experiment_row = pd.DataFrame(
        data=[[
            st.session_state['experiment_no'],
            number_of_trials,
            target_sum,
            final_prob
        ]],
        columns=['no', 'iteraciones', 'suma_deseada', 'probabilidad_observada']
    )
    
    # Concatena el nuevo DataFrame con el historial de resultados
    st.session_state['df_experiment_results'] = pd.concat(
        [st.session_state['df_experiment_results'], new_experiment_row],
        ignore_index=True
    )

st.write("### Historial de experimentos")
st.dataframe(st.session_state['df_experiment_results'])
