import streamlit as st
import pandas as pd
import os
from supabase import create_client, Client
import json
from datetime import datetime
# import datetime
import time
import pytz
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="2024 F1 Fantasy", page_icon="🏆", layout="wide")

st.image("https://www.formula1.com/etc/designs/fom-website/images/f1-tv-logo.svg", width=120) #https://www.formula1.com/etc/designs/fom-website/images/f1_logo.svg
st.header('2024 - F1 Fantasy')
st.subheader('4ta Temporada 🏎')

current_time = datetime.now()
year = '2024'
month = '5'
day = '17'
hora = '5'
minuto = '0'
hora_limite = datetime.strptime(str(year) + '-' + str(month) + '-' + str(day) + ' ' + hora + ':' + minuto, '%Y-%m-%d %H:%M')

tab1, tab2 = st.tabs(["Resultados", "Pronosticos"])
usuarios = pd.DataFrame({'Usuario': ['Seleccionar', 'Alex', 'Gerry', 'Giorgio', 'Mike']})
usuario_activo = st.selectbox('Usuario', usuarios)

conn =  st.connection("gsheets", type=GSheetsConnection)
pronosticos = conn.read(worksheet="Forecast", usecols=list(range(6)))
drivers = conn.read(worksheet="Pilotos", usecols=list(range(2)))
players = conn.read(worksheet="Players", usecols=list(range(3)))

if usuario_activo is not "Seleccionar":
    clave_jugador = players.loc[players['User'] == usuario_activo, 'user_key'].values[0]
    st.write(clave_jugador)
    if clave_jugador is None:
        st.caption("Registra tu password")
        
    
    password = st.text_input("Ingresa tu password", type="password")
    if password == clave_jugador:
        st.write("La clave del jugador seleccionado es correcta")
        if current_time <= hora_limite:
            pronosticos = pronosticos[((pronosticos['Race No'] == 9) | (pronosticos['Race No'] == 10))]
            pronosticos =  pronosticos[['User', 'Race', 'Fecha Carrera', 'Place', 'Forecast']]
            pronosticos = pronosticos[pronosticos['User'] == usuario_activo]
            edited_pronosticos = st.data_editor(pronosticos, column_config={"Forecast": st.column_config.SelectboxColumn(options=["Max Verstappen","Sergio Perez","Charles Leclerc","Carlos Sainz","George Russell","Lewis Hamilton","Esteban Ocon","Pierre Gasly","Oscar Piastri","Lando Norris","Valteri Bottas","Zhou Guanyu","Lance Stroll","Fernando Alonso","Kevin Magnusen","Nico Hulkenberg","Daniel Ricciardo","Yuki Tsunoda"])}, disabled=["Race", "Place", "Fecha Carrera", "Player"], hide_index=True)
            conn.update(worksheet="Forecast", data=edited_pronosticos)











# # url = 'https://uehrgoqjfbdbkkyumtpw.supabase.co'
# # key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVlaHJnb3FqZmJkYmtreXVtdHB3Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTcwOTA3MDE1MywiZXhwIjoyMDI0NjQ2MTUzfQ.KIIsWOhJx7sPYYP6Wdvdq6S4vPJ8vrSrZbs-vG6kBWw'
# # supabase_client = create_client(url, key)

# # response_drivers = supabase_client.table('drivers').select("*").execute()
# # drivers = pd.DataFrame(response_drivers.data)
# # drivers = drivers.sort_values(by='driverId')

# # # st.table(drivers)
# # if usuario_activo is not 'Seleccionar':

# #     # Consulta la base de datos para verificar los orderId existentes
# #     response_pronosticos = supabase_client.table('Pronosticos').select("*").execute()
# #     pronosticos = pd.DataFrame(response_pronosticos.data)
# #     pronosticos = pronosticos.sort_values(by='id')
# #     pronosticos = pronosticos[pronosticos['Usuario'] == usuario_activo]
# #     # pronosticos = pronosticos[pronosticos['Carrera No'] == 3]


# #     # st.dataframe(pronosticos, height=400)
