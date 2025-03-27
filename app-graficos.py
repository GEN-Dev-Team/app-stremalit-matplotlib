import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Funciones
def ReaccionPuntual(Long, CP):
    R1 = CP[0] * (Long - CP[1]) / Long
    R2 = CP[0] * CP[1] / Long
    return R1, R2

def DMFPuntual(Long, CP, Paso=0.1):
    DMF = []
    R1, R2 = ReaccionPuntual(Long, CP)
    x = np.linspace(0, Long, int(Long / Paso) + 1)  # Usamos linspace para garantizar que x y y tengan la misma longitud
    for i in x:
        if i < CP[1]:
            M = R1 * i
        else:
            M = R1 * i - CP[0] * (i - CP[1])
        DMF.append(M)
    return x, DMF

def DFCPuntual(Long, CP, Paso=0.1):
    DFC = []
    R1, R2 = ReaccionPuntual(Long, CP)
    x = np.linspace(0, Long, int(Long / Paso) + 1)
    for i in x:
        if i < CP[1]:
            F = R1
        else:
            F = R1 - CP[0]
        DFC.append(F)
    return x, DFC

def ReaccionDistribuida(Long, CD):
    C = CD[0] * (Long - CD[1] - CD[2])
    X = CD[1] + (Long - CD[1] - CD[2])/2
    R1 = C * (Long - X) / Long
    R2 = C * X / Long
    return R1, R2

def DMFDistribuida(Long, CD, Paso=0.1):
    DMF = []
    R1, R2 = ReaccionDistribuida(Long, CD)
    x = np.linspace(0, Long, int(Long / Paso) + 1)
    for i in x:
        if i < CD[1]:
            M = R1 * i
        elif i < Long - CD[2]:
            M = R1 * i - CD[0] * (i - CD[1]) * (Long - i + (i - CD[1])/2)
        else:
            M = R1 * i - CD[0] * (Long - CD[1] - CD[2]) * (2*i + CD[2] - CD[1] - Long)/2
        DMF.append(M)
    return x, DMF

def DFCDistribuida(Long, CD, Paso=0.1):
    DFC = []
    R1, R2 = ReaccionPuntual(Long, CD)
    x = np.linspace(0, Long, int(Long / Paso) + 1)
    for i in x:
        if i < CD[1]:
            F = R1
        elif i < Long - CD[2]:
            F = R1 - CD[0] * (i - CD[1])
        else:
            F = R1 - CD[0] * (Long - CD[1] - CD[2])
        DFC.append(F)
    return x, DFC

# Configuración de Streamlit
st.title("Diagrama de Momentos y Fuerzas Cortantes")

# Entrada de datos
Long = st.slider("Longitud de la viga (m)", 1, 100, 50)
Paso = st.slider("Paso para los cálculos (m)", 0.1, 1.0, 0.66)

CPuntual = st.text_input("Carga Puntual (Ton, Posición)", "10, 5")
CPuntual = list(map(float, CPuntual.split(",")))

CDistribuida = st.text_input("Carga Distribuida (Intensidad, Inicio, Fin)", "4, 8, 12")
CDistribuida = list(map(float, CDistribuida.split(",")))

# Cálculos
x_Puntual, DMF_Puntual = DMFPuntual(Long, CPuntual, Paso)
x_Puntual, DFC_Puntual = DFCPuntual(Long, CPuntual, Paso)
x_Distribuida, DMF_Distribuida = DMFDistribuida(Long, CDistribuida, Paso)
x_Distribuida, DFC_Distribuida = DFCDistribuida(Long, CDistribuida, Paso)

# Mostrar gráficos
fig, ax = plt.subplots(2, 1, figsize=(10, 8))
plt.subplots_adjust(hspace=0.5)  # Ajuste del espacio entre los gráficos

# Diagrama de momentos flectores para carga puntual
ax[0].plot(x_Puntual, DMF_Puntual, label="DMF Carga Puntual")
ax[0].set_title("Diagrama de Momentos Flectores (Carga Puntual)")
ax[0].set_xlabel("Longitud (m)")
ax[0].set_ylabel("Momento Flector (Ton·m)")

# Diagrama de fuerzas cortantes para carga puntual
ax[1].plot(x_Puntual, DFC_Puntual, label="DFC Carga Puntual", color='r')
ax[1].set_title("Diagrama de Fuerzas Cortantes (Carga Puntual)")
ax[1].set_xlabel("Longitud (m)")
ax[1].set_ylabel("Fuerza Cortante (Ton)")

# Mostrar gráficos de carga distribuida
fig2, ax2 = plt.subplots(2, 1, figsize=(10, 8))
plt.subplots_adjust(hspace=0.5)

# Diagrama de momentos flectores para carga distribuida
ax2[0].plot(x_Distribuida, DMF_Distribuida, label="DMF Carga Distribuida")
ax2[0].set_title("Diagrama de Momentos Flectores (Carga Distribuida)")
ax2[0].set_xlabel("Longitud (m)")
ax2[0].set_ylabel("Momento Flector (Ton·m)")

# Diagrama de fuerzas cortantes para carga distribuida
ax2[1].plot(x_Distribuida, DFC_Distribuida, label="DFC Carga Distribuida", color='g')
ax2[1].set_title("Diagrama de Fuerzas Cortantes (Carga Distribuida)")
ax2[1].set_xlabel("Longitud (m)")
ax2[1].set_ylabel("Fuerza Cortante (Ton)")

# Mostrar gráficos
st.pyplot(fig)
st.pyplot(fig2)
