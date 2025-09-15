import pandas as pd
import random
import streamlit as st
import time

if 'experiment_no' not in st.session_state:
    st.session_state['experiment_no'] = 0
if 'df_experiment_results' not in st.session_state:
    st.session_state['df_experiment_results'] = pd.DataFrame(columns=['no', 'iteraciones', 'suma_deseada', 'probabilidad'])

st.header('Lanzar dos dados 🎲🎲')
st.markdown('¡Vamos a explorar la probabilidad de obtener una suma específica al lanzar dos dados!')

def roll_dice(n, target_sum):
    roll_outcomes = []
    for _ in range(n):
        roll1 = random.randint(1, 6)
        roll2 = random.randint(1, 6)
        roll_outcomes.append(roll1 + roll2)

    mean = None
    outcome_no = 0
    target_sum_count = 0
    
    # Preparamos el gráfico con los valores posibles (del 2 al 12)
    chart = st.line_chart([0.0] * 11)

    for r in roll_outcomes:
        outcome_no += 1
        if r == target_sum:
            target_sum_count += 1
        
        prob = target_sum_count / outcome_no
        
        # Actualizamos solo el punto correspondiente a la suma deseada
        data = [0.0] * 11
        data[target_sum - 2] = prob
        chart.add_rows([data])
        
        time.sleep(0.01)

    return prob

number_of_trials = st.slider('¿Número de lanzamientos?', 1, 1000, 10)
target_sum = st.selectbox('¿Qué suma quieres buscar?', options=range(2, 13))
start_button = st.button('Ejecutar simulación')

if start_button:
    st.write(f'Simulando {number_of_trials} lanzamientos, buscando la suma {target_sum}.')
    st.session_state['experiment_no'] += 1
    
    final_prob = roll_dice(number_of_trials, target_sum)

    st.session_state['df_experiment_results'] = pd.concat([
        st.session_state['df_experiment_results'],
        pd.DataFrame(data=[[st.session_state['experiment_no'],
                            number_of_trials,
                            target_sum,
                            final_prob]],
                     columns=['no', 'iteraciones', 'suma_deseada', 'probabilidad'])
    ], axis=0)
    st.session_state['df_experiment_results'] = st.session_state['df_experiment_results'].reset_index(drop=True)

st.write("### Resultados del experimento")
st.dataframe(st.session_state['df_experiment_results'])
