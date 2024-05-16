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

st.set_page_config(page_title="🏎🏎🏎2024 F1 Quiniela🏎🏎🏎", page_icon="🏆", layout="wide")

st.image("https://www.formula1.com/etc/designs/fom-website/images/f1-tv-logo.svg", width=120) #https://www.formula1.com/etc/designs/fom-website/images/f1_logo.svg
st.header('2024 - F1 Fantasy')
st.subheader('4ta Temporada 🏎')
tab1, tab2 = st.tabs(["Resultados", "Pronosticos"])
usuarios = pd.DataFrame({'Usuario': ['Seleccionar', 'Alex', 'Gerry', 'Giorgio', 'Mike']})
usuario_activo = st.selectbox('Usuario', usuarios)

conn =  st.connection("gsheets", type=GSheetsConnection)
pronosticos = conn.read(worksheet="Forecast", usecols=list(range(9)))
drivers = conn.read(worksheet="Pilotos", usecols=list(range(2)))
piloto = drivers["Piloto"]

current_time = datetime.now()
year = '2024'
month = '5'
day = '17'
hora = '5'
minuto = '0'
hora_limite = datetime.strptime(str(year) + '-' + str(month) + '-' + str(day) + ' ' + hora + ':' + minuto, '%Y-%m-%d %H:%M')

if current_time <= hora_limite:
    st.write(current_time)
    pronosticos = pronosticos[((pronosticos['Race No'] == 9) | (pronosticos['Race No'] == 10))]

    st.dataframe(pronosticos)
    st.write(hora_mexico)

# if usuario_activo is not "Seleccionar":
#     pronosticos = pronosticos[pronosticos['User'] == usuario_activo]
#     edited_pronosticos = st.data_editor(pronosticos, column_config={"Forecast": st.column_config.SelectboxColumn(options=["Max Verstappen","Sergio Perez","Charles Leclerc","Carlos Sainz","George Russell","Lewis Hamilton","Esteban Ocon","Pierre Gasly","Oscar Piastri","Lando Norris","Valteri Bottas","Zhou Guanyu","Lance Stroll","Fernando Alonso","Kevin Magnusen","Nico Hulkenberg","Daniel Ricciardo","Yuki Tsunoda"])}, disabled=["Race No", "Race", "Place", "Fecha Carrera", "Fecha Limite", "Player", "Result"], hide_index=True)






# st.column_config.SelectboxColumn(label="Pronostico", *, width=None, help="Selecciona de la lista el piloto", width="medium", options=["Max", "Per"])

# st.dataframe(edited_pronosticos)







# url = 'https://uehrgoqjfbdbkkyumtpw.supabase.co'
# key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVlaHJnb3FqZmJkYmtreXVtdHB3Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTcwOTA3MDE1MywiZXhwIjoyMDI0NjQ2MTUzfQ.KIIsWOhJx7sPYYP6Wdvdq6S4vPJ8vrSrZbs-vG6kBWw'
# supabase_client = create_client(url, key)

# response_drivers = supabase_client.table('drivers').select("*").execute()
# drivers = pd.DataFrame(response_drivers.data)
# drivers = drivers.sort_values(by='driverId')

# # st.table(drivers)
# if usuario_activo is not 'Seleccionar':

#     # Consulta la base de datos para verificar los orderId existentes
#     response_pronosticos = supabase_client.table('Pronosticos').select("*").execute()
#     pronosticos = pd.DataFrame(response_pronosticos.data)
#     pronosticos = pronosticos.sort_values(by='id')
#     pronosticos = pronosticos[pronosticos['Usuario'] == usuario_activo]
#     # pronosticos = pronosticos[pronosticos['Carrera No'] == 3]


#     # st.dataframe(pronosticos, height=400)
