import streamlit as st
import numpy as np
import functions as f
import matplotlib.pyplot as plt
import pandas as pd

# Configuración de Streamlit
st.title("Diagramas de Momentos y Fuerzas Cortantes")
st.header("Datos")

# Entrada de datos
Long = st.slider("Longitud de la viga (m)", 1, 50, 1, 1)
Paso = st.slider("Paso para los cálculos (m)", 0.1, 1.0, 0.1, 0.1)

# Inicializar la lista de cargas puntuales si no existe en el estado de sesión
if 'cargas_puntuales' not in st.session_state:
    st.session_state.cargas_puntuales = []

# Función para agregar una nueva carga puntual
def agregar_carga_puntual():
    st.session_state.cargas_puntuales.append({'peso_cp': 1, 'posicion_cp': 0})

# Función para eliminar una carga puntual
def eliminar_carga_puntual(idx):
    del st.session_state.cargas_puntuales[idx]

# Título
st.header("Cargas puntuales")

# Botón para agregar una nueva carga puntual
if st.button("Agregar carga puntual"):
    agregar_carga_puntual()

# Mostrar las cargas puntuales existentes en filas
for idx, carga in enumerate(st.session_state.cargas_puntuales):
    cols = st.columns([1, 4, 4, 2])  # Definir las columnas para cada fila
    with cols[0]:
        st.write(f"P{idx + 1}:")
    with cols[1]:
        carga['peso_cp'] = st.number_input(f'Peso {idx + 1} (Ton)', min_value=1, step=1, key=f'peso_cp_{idx + 1}')
    with cols[2]:
        carga['posicion_cp'] = st.selectbox(f'Posición {idx + 1} (m)', options=[i for i in range(0, 51)], key=f'posicion_cp_{idx + 1}')
    with cols[3]:
        if st.button(f"Eliminar", key=f"eliminar_cp_{idx + 1}"):
            eliminar_carga_puntual(idx)

# Inicializar la lista de cargas distribuidas si no existe en el estado de sesión
if 'cargas_distribuidas' not in st.session_state:
    st.session_state.cargas_distribuidas = []

# Función para agregar una nueva carga distribuida
def agregar_carga_distribuida():
    st.session_state.cargas_distribuidas.append({'peso_cd': 1, 'posicion_inicial_cd': 0, 'posicion_final_cd': 0})

# Función para eliminar una carga distribuida
def eliminar_carga_distribuida(idx):
    del st.session_state.cargas_distribuidas[idx]

# Título
st.header("Cargas distribuidas")

# Botón para agregar una nueva carga distribuida
if st.button("Agregar carga distribuida"):
    agregar_carga_distribuida()

# Mostrar las cargas distribuidas existentes en filas
for idx, carga in enumerate(st.session_state.cargas_distribuidas):
    cols = st.columns([1, 4, 4, 4, 3])  # Definir las columnas para cada fila
    with cols[0]:
        st.write(f"P{idx + 1}:")
    with cols[1]:
        carga['peso_cd'] = st.number_input(f'Peso {idx + 1} (Ton)', min_value=1, step=1, key=f'peso_cd_{idx + 1}')
    with cols[2]:
        carga['posicion_inicial_cd'] = st.selectbox(f'Posición inicial {idx + 1} (m)', options=[i for i in range(0, 51)], key=f'posicion_inicial_cd_{idx + 1}')
    with cols[3]:
        carga['posicion_final_cd'] = st.selectbox(f'Posición final {idx + 1} (m)', options=[i for i in range(0, 51)], key=f'posicion_final_cd_{idx + 1}')
    with cols[4]:
        if st.button(f"Eliminar", key=f"eliminar_cd_{idx + 1}"):
            eliminar_carga_distribuida(idx)

# Sección de resultados
st.markdown("<hr>", unsafe_allow_html=True)
st.title("Resultados")

# Selección de carga para mostrar el gráfico
opciones_carga = ['Selecciona carga', 'Cargas puntuales', 'Cargas distribuidas']
carga_seleccionada = st.selectbox("Selecciona el tipo de carga para graficar", opciones_carga)

# Mostrar el gráfico de la carga seleccionada
if carga_seleccionada == 'Cargas puntuales':
    # Crear una lista de etiquetas como "Peso 1", "Peso 2", etc.
    opciones_puntuales = [f"Peso {idx + 1}" for idx in range(len(st.session_state.cargas_puntuales))]
    
    if opciones_puntuales:
        carga_puntual = st.selectbox("Selecciona una carga puntual", opciones_puntuales)
        
        if carga_puntual:
            idx_carga = opciones_puntuales.index(carga_puntual)  # Obtener el índice de la carga seleccionada
            carga = st.session_state.cargas_puntuales[idx_carga]
            # Calcular DMF y DFC para carga puntual
            CP = [carga['peso_cp'], carga['posicion_cp']]
            dmf1 = f.DMFPuntual(Long, CP, Paso)
            dfc1 = f.DFCPuntual(Long, CP, Paso)
            
            # Selección de gráfico
            opcion_grafico = st.radio("Selecciona el gráfico", ["Mostrar gráfico completo", "Ver Momentos Flectores y Fuerzas Cortantes"])
            
            if opcion_grafico == "Mostrar gráfico completo":
                # Mostrar gráfico completo con la función Grafica
                f.Grafica(Long, np.linspace(0, Long, int(Long / Paso) + 1), dmf1, dfc1)
            
            elif opcion_grafico == "Ver Momentos Flectores y Fuerzas Cortantes":
                # Mostrar los gráficos de DMF y DFC por separado
                fig, ax = plt.subplots(2, 1, figsize=(10, 8))
                
                ax[0].plot(np.linspace(0, Long, int(Long / Paso) + 1), dmf1, label="Diagrama de Momentos Flectores")
                ax[0].set_title("Diagrama de Momentos Flectores (Carga Puntual)")
                ax[0].set_xlabel("Longitud (m)")
                ax[0].set_ylabel("Momento Flector (Ton·m)")
                
                ax[1].plot(np.linspace(0, Long, int(Long / Paso) + 1), dfc1, label="Diagrama de Fuerzas Cortantes", color='r')
                ax[1].set_title("Diagrama de Fuerzas Cortantes (Carga Puntual)")
                ax[1].set_xlabel("Longitud (m)")
                ax[1].set_ylabel("Fuerza Cortante (Ton)")
                
                st.pyplot(fig)

elif carga_seleccionada == 'Cargas distribuidas':
    # Crear una lista de etiquetas como "Peso 1", "Peso 2", etc.
    opciones_distribuidas = [f"Peso {idx + 1}" for idx in range(len(st.session_state.cargas_distribuidas))]
    
    if opciones_distribuidas:
        carga_distribuida = st.selectbox("Selecciona una carga distribuida", opciones_distribuidas)
        
        if carga_distribuida:
            idx_carga = opciones_distribuidas.index(carga_distribuida)  # Obtener el índice de la carga seleccionada
            carga = st.session_state.cargas_distribuidas[idx_carga]
            # Calcular DMF y DFC para carga distribuida
            CD = [carga['peso_cd'], carga['posicion_inicial_cd'], carga['posicion_final_cd']]
            dmf3 = f.DMFDistribuida(Long, CD, Paso)
            dfc3 = f.DFCDistribuida(Long, CD, Paso)
            
            # Selección de gráfico
            opcion_grafico = st.radio("Selecciona el gráfico", ["Mostrar gráfico completo", "Ver Momentos Flectores y Fuerzas Cortantes"])
            
            if opcion_grafico == "Mostrar gráfico completo":
                # Mostrar gráfico completo con la función Grafica
                f.Grafica(Long, np.linspace(0, Long, int(Long / Paso) + 1), dmf3, dfc3)
            
            elif opcion_grafico == "Ver Momentos Flectores y Fuerzas Cortantes":
                # Mostrar los gráficos de DMF y DFC por separado
                fig, ax = plt.subplots(2, 1, figsize=(10, 8))
                
                ax[0].plot(np.linspace(0, Long, int(Long / Paso) + 1), dmf3, label="Diagrama de Momentos Flectores")
                ax[0].set_title("Diagrama de Momentos Flectores (Carga Distribuida)")
                ax[0].set_xlabel("Longitud (m)")
                ax[0].set_ylabel("Momento Flector (Ton·m)")
                
                ax[1].plot(np.linspace(0, Long, int(Long / Paso) + 1), dfc3, label="Diagrama de Fuerzas Cortantes", color='r')
                ax[1].set_title("Diagrama de Fuerzas Cortantes (Carga Distribuida)")
                ax[1].set_xlabel("Longitud (m)")
                ax[1].set_ylabel("Fuerza Cortante (Ton)")
                
                st.pyplot(fig)


# Botón para generar gráfico general y tabla
if st.button("Generar gráfico general y tabla"):
    # Listas para almacenar los resultados de los diagramas de cada carga
    esfuerzos = []
    
    # Cálculo de DMF y DFC para cada carga puntual
    for carga in st.session_state.cargas_puntuales:
        CP = [carga['peso_cp'], carga['posicion_cp']]
        dmf1 = f.DMFPuntual(Long, CP, Paso)
        dfc1 = f.DFCPuntual(Long, CP, Paso)
        esfuerzos.append([dmf1, dfc1])
    
    # Cálculo de DMF y DFC para cada carga distribuida
    for carga in st.session_state.cargas_distribuidas:
        CD = [carga['peso_cd'], carga['posicion_inicial_cd'], carga['posicion_final_cd']]
        dmf3 = f.DMFDistribuida(Long, CD, Paso)
        dfc3 = f.DFCDistribuida(Long, CD, Paso)
        esfuerzos.append([dmf3, dfc3])
    
    # Calcular los diagramas globales sumados
    DMF, DFC = f.Global(Long, Paso, esfuerzos)
    
    # Crear un array para las posiciones (x)
    x = np.linspace(0, Long, int(Long / Paso) + 1)
    
    # Crear el DataFrame para mostrar los resultados
    df = pd.DataFrame({
        'x': x,
        'DMF-Global': DMF,
        'DFC-Global': DFC
    })
    
    # Añadir las columnas para los diagramas individuales
    for i, carga in enumerate(st.session_state.cargas_puntuales):
        CP = [carga['peso_cp'], carga['posicion_cp']]
        dmf = f.DMFPuntual(Long, CP, Paso)
        dfc = f.DFCPuntual(Long, CP, Paso)
        df[f'DMF{i+1}'] = dmf
        df[f'DFC{i+1}'] = dfc
    
    for i, carga in enumerate(st.session_state.cargas_distribuidas):
        CD = [carga['peso_cd'], carga['posicion_inicial_cd'], carga['posicion_final_cd']]
        dmf = f.DMFDistribuida(Long, CD, Paso)
        dfc = f.DFCDistribuida(Long, CD, Paso)
        df[f'DMF{len(st.session_state.cargas_puntuales)+i+1}'] = dmf
        df[f'DFC{len(st.session_state.cargas_puntuales)+i+1}'] = dfc
    
    # Mostrar la tabla en Streamlit
    st.write(df)
    
    # Generar el gráfico general usando la función Grafica
    f.Grafica(Long, x, DMF, DFC)