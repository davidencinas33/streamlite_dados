import pandas as pd
import random
import streamlit as st
import time

# ... (código anterior) ...

def roll_dice(n, target_sum):
    roll_outcomes = []
    for _ in range(n):
        roll1 = random.randint(1, 6)
        roll2 = random.randint(1, 6)
        roll_outcomes.append(roll1 + roll2)

    target_sum_count = 0
    
    # Crea un DataFrame inicial para el gráfico
    initial_data = pd.DataFrame({'probabilidad': [0.0] * 11})
    chart = st.line_chart(initial_data)

    for r in roll_outcomes:
        target_sum_count += 1 if r == target_sum else 0
        
        prob = target_sum_count / (roll_outcomes.index(r) + 1)
        
        # Crea un nuevo DataFrame para la fila a agregar
        new_row = pd.DataFrame({'probabilidad': [0.0] * 11})
        new_row.loc[target_sum - 2, 'probabilidad'] = prob
        
        # Usa add_rows con el DataFrame
        chart.add_rows(new_row)
        
        time.sleep(0.01)

    return prob

# ... (resto del código) ...
