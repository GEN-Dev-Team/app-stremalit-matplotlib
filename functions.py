import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import streamlit as st

# Calculo de reacciones por carga puntual
def ReaccionPuntual(Long, CP):
    # Reacciones en los extremos de la viga
    R1 = CP[0] * (Long - CP[1]) / Long
    R2 = CP[0] * CP[1] / Long
    return R1, R2

# Calculo del diagrama de momentos flectores para una carga puntual
def DMFPuntual(Long, CP, Paso=0.1):
    # Inicializa el diagrama
    DMF = []
    if CP[0] == 0:
        DMF = [0] * (int(Long / Paso) + 1)
        return DMF
    else:
        R1, R2 = ReaccionPuntual(Long, CP)
        # Calcula el momento flector en cada punto
        i = 0
        while i <= Long:
            if i < CP[1]:
                M = R1 * i
            else:
                M = R1 * i - CP[0] * (i - CP[1])
            DMF.append(M)
            i += Paso
        return DMF
    
# Calculo del diagrama de fuerzas cortantes para una carga puntual
def DFCPuntual(Long, CP, Paso=0.1):
    # Inicializa el diagrama
    DFC = []
    if CP[0] == 0:
        DFC = [0] * (int(Long / Paso) + 1)
        return DFC
    else:
        R1, R2 = ReaccionPuntual(Long, CP)
        # Calcula la fuerza cortante en cada punto
        i = 0
        while i <= Long:
            if i < CP[1]:
                F = R1
            else:
                F = R1 - CP[0]
            DFC.append(F)
            i += Paso
        return DFC

# Cálculo de reacciones por carga distribuida
def ReaccionDistribuida(Long, CD):
    # Reacciones en los extremos de la viga
    C = CD[0] * (Long - CD[1] - CD[2])
    X = CD[1] + (Long - CD[1] - CD[2])/2
    R1 = C * (Long - X) / Long
    R2 = C * X / Long
    return R1, R2

# Calculo del diagrama de momentos flectores para una carga distribuida
def DMFDistribuida(Long, CD, Paso=0.1):
    # Inicializa el diagrama
    DMF = []
    if CD[0] == 0:
        DMF = [0] * (int(Long / Paso) + 1)
        return DMF
    else:
        R1, R2 = ReaccionDistribuida(Long, CD)
        # Calcula el momento flector en cada punto
        i = 0
        while i <= Long:
            if i < CD[1]:
                M = R1 * i
            elif i < Long - CD[2]:
                M = R1 * i - CD[0] * (i - CD[1]) * (Long - i + (i - CD[1])/2)
            else:
                M = R1 * i - CD[0] * (Long - CD[1] - CD[2]) * (2*i + CD[2] - CD[1] - Long)/2
            DMF.append(M)
            i += Paso
        return DMF

# Calculo del diagrama de fuerzas cortantes para una carga puntual
def DFCDistribuida(Long, CD, Paso=0.1):
    # Inicializa el diagrama
    DFC = []
    if CD[0] == 0:
        DFC = [0] * (int(Long / Paso) + 1)
        return DFC
    else:
        R1, R2 = ReaccionDistribuida(Long, CD)
        # Calcula la fuerza cortante en cada punto
        i = 0
        while i <= Long:
            if i < CD[1]:
                F = R1
            elif i < Long - CD[2]:
                F = R1 - CD[0] * (i - CD[1])
            else:
                F = R1 - CD[0] * (Long - CD[1]- CD[2])
            DFC.append(F)
            i += Paso
        return DFC
    
def Grafica(long, posicion, momento, cortante):
    # Crear la figura con subgráficos (2 filas, 1 columna)
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                        vertical_spacing=0.2, 
                        subplot_titles=('Diagrama de Momento Flector (DMF)', 'Diagrama de Fuerza Cortante (DFC)'))

    # Colores modo dark
    bg_color = "#1e1e1e"  # Fondo oscuro
    grid_color = "#444"    # Color de la cuadrícula
    text_color = "#ffffff" # Color del texto
    
    # Gráfica del Momento Flector (DMF)
    fig.add_trace(go.Scatter(x=posicion, y=momento, mode='lines', fill='tozeroy',
                             line=dict(color='#00bfff'), name='Momento negativo'), row=1, col=1)
    fig.add_trace(go.Scatter(x=posicion, y=momento, mode='lines', fill='tozeroy',
                             line=dict(color='#ff4500'), name='Momento positivo'), row=1, col=1)
    fig.add_trace(go.Scatter(x=[0, long], y=[0, 0], mode='lines', 
                             line=dict(color='#800080', width=8), name='Viga'), row=1, col=1)
    
    # Gráfica de la Fuerza Cortante (DFC)
    fig.add_trace(go.Scatter(x=posicion, y=cortante, mode='lines', fill='tozeroy',
                             line=dict(color='#00bfff'), name='Cortante negativo'), row=2, col=1)
    fig.add_trace(go.Scatter(x=posicion, y=cortante, mode='lines', fill='tozeroy',
                             line=dict(color='#ff4500'), name='Cortante positivo'), row=2, col=1)
    fig.add_trace(go.Scatter(x=[0, long], y=[0, 0], mode='lines', 
                             line=dict(color='#800080', width=8), name='Viga'), row=2, col=1)
    
    # Configurar el diseño del gráfico
    fig.update_layout(height=600, width=800, showlegend=False,
                      xaxis_title='Longitud de la viga (m)',
                      xaxis2_title='Longitud de la viga (m)',
                      yaxis_title='Momento flector (Ton·m)',
                      yaxis2_title='Fuerza cortante (Ton)',
                      paper_bgcolor=bg_color,
                      plot_bgcolor=bg_color,
                      font=dict(color=text_color),
                      xaxis=dict(gridcolor=grid_color, zerolinecolor=grid_color),
                      xaxis2=dict(gridcolor=grid_color, zerolinecolor=grid_color),
                      yaxis=dict(gridcolor=grid_color, zerolinecolor=grid_color),
                      yaxis2=dict(gridcolor=grid_color, zerolinecolor=grid_color))
    
    # Mostrar el gráfico en Streamlit
    st.plotly_chart(fig)

# Funcion para calcular el diagrama de momentos y fuerzas cortantes globales
def Global(long, pas, esfuerzos):
    # Sumar los momentos y fuerzas por cada carga
    DMF = np.zeros(int(long / pas) + 1)
    DFC = np.zeros(int(long / pas) + 1)
    for mf in esfuerzos:
        DMF += mf[0]
        DFC += mf[1]
    return DMF, DFC