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

# conn =  st.connection("gsheets", type=GSheetsConnection)
# pronosticos = conn.read(worksheet="9y10", usecols=list(range(5)), ttl=5)
# drivers = conn.read(worksheet="Pilotos", usecols=list(range(3)), ttl=5)
# users = conn.read(worksheet="Players", usecols=list(range(3)), ttl=5)

# if usuario_activo is not "Seleccionar":
#     clave_jugador = users.loc[users['User'] == usuario_activo, 'user_key'].values[0]
#     # st.write(clave_jugador)
    
#     # if pd.isna(clave_jugador):
#     #     st.caption("Registra tu password para ingresar tus pronosticos")
#     #     users = users[users['user'] == usuario_activo]
#     #     st.dataframe(users)
#     #     # players =  players[['user_key']]
#     #     # edited_players = st.data_editor(players, column_config={"user_key": st.column_config.TextColumn("Password", max_chars=10,)}, hide_index=True,)
#     #     # conn.update(worksheet="Players", data=edited_players)
        
#     password = st.text_input("Ingresa tu password", type="password")
#     if password == clave_jugador:
#         st.write("La clave del jugador seleccionado es correcta")
#         if current_time <= hora_limite:
#             pronosticos = pronosticos[pronosticos['User'] == usuario_activo]
#             edited_pronosticos = st.data_editor(pronosticos, column_config={"Forecast": st.column_config.SelectboxColumn(options=["Max Verstappen","Sergio Perez","Charles Leclerc","Carlos Sainz","George Russell","Lewis Hamilton","Esteban Ocon","Pierre Gasly","Oscar Piastri","Lando Norris","Valteri Bottas","Zhou Guanyu","Lance Stroll","Fernando Alonso","Kevin Magnusen","Nico Hulkenberg","Daniel Ricciardo","Yuki Tsunoda"])}, disabled=["Race", "Place", "Fecha Carrera", "User"], hide_index=True)
#             conn.update(worksheet="Forecast", data=edited_pronosticos)







# # st.dataframe(players)

# # if usuario_activo in players:
# #     st.write('Ok')
# # else:
# #     st.caption('Registra tu usuario y contraseña')
# #     with st.form(key="alta_usuario"):
# #         usuario = usuario_activo
# #         password = st.text_input("Ingresa tu contraseña")
# #         submit_button = st.form_submit_button(label="Registra tu Password")
# #         if submit_button:
# #             user_data = pd.DataFrame(
# #                 [
# #                     {
# #                         "User": usuario,
# #                         "Password": password,
# #                     }
# #                 ]
# #             )
# #             updated_players = pd.concat([players, user_data], ignore_index=True)
# #             conn.update(worksheet="Players", data=updated_players)
        





















url = 'https://uehrgoqjfbdbkkyumtpw.supabase.co'
key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVlaHJnb3FqZmJkYmtreXVtdHB3Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTcwOTA3MDE1MywiZXhwIjoyMDI0NjQ2MTUzfQ.KIIsWOhJx7sPYYP6Wdvdq6S4vPJ8vrSrZbs-vG6kBWw'
supabase_client = create_client(url, key)

drivers = supabase_client.table('drivers').select("*").execute()
drivers = pd.DataFrame(drivers.data)
drivers = drivers.sort_values(by='driverId')
drivers = drivers['driverName']
# st.table(drivers)

# pronosticos = supabase_client.table('Pronosticos').select("*").eq("Usuario", usuario_activo).execute()
# pronosticos = pd.DataFrame(pronosticos.data)
# st.dataframe(pronosticos)

users = supabase_client.table('users').select("*").eq("user", usuario_activo).execute()
users = users.data
usuario_nombres = {users['user']: usuario['id'] for user in users}

st.write(usuario_nombres)

pronosticos = supabase_client.table('Pronosticos').select("*").eq("User", usuario_activo).execute()
pronosticos = pd.DataFrame(pronosticos.data)

pronosticos = pronosticos[(pronosticos['Race No'] == 8) | (pronosticos['Race No'] == 9)]
st.dataframe(pronosticos)




# # Función para actualizar los datos en la tabla "Pronosticos"
# def actualizar_datos(df):
#     for index, row in df.iterrows():
#         response = supabase_client.table("Pronosticos").update({
#             "Pronostico": row["Piloto"],
#             }).eq("id", row["id"]).execute()
#     return response

# pronosticos = obtener_datos()
# st.dataframe(pronosticos)
# # Filtrar por usuario activo
# usuario_activo = st.text_input("Usuario Activo", "default_user")
# df_usuario_activo = df[df['usuario'] == usuario_activo]

# # Mostrar el DataFrame editable
# edited_df = st.experimental_data_editor(df_usuario_activo)

# # Botón para actualizar los datos
# if st.button("Actualizar Datos"):
#     response = actualizar_datos(edited_df)
#     if response.status_code == 200:
#         st.success("Datos actualizados correctamente")
#     else:
#         st.error("Hubo un error al actualizar los datos")
















# if usuario_activo is not 'Seleccionar':

#     # Consulta la base de datos para verificar los orderId existentes
#     response_pronosticos = supabase_client.table('Pronosticos').select("*").execute()
#     pronosticos = pd.DataFrame(response_pronosticos.data)
#     pronosticos = pronosticos.sort_values(by='id')
#     pronosticos = pronosticos[pronosticos['Usuario'] == usuario_activo]
#     # pronosticos = pronosticos[pronosticos['Carrera No'] == 3]


#     # st.dataframe(pronosticos, height=400)
