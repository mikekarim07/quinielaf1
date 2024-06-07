import streamlit as st
import pandas as pd
from supabase import create_client, Client
from datetime import datetime

st.set_page_config(page_title="2024 F1 Fantasy", page_icon="🏆", layout="wide")

st.image("https://www.formula1.com/etc/designs/fom-website/images/f1-tv-logo.svg", width=120)  # https://www.formula1.com/etc/designs/fom-website/images/f1_logo.svg
st.header('2024 - F1 Fantasy')
st.subheader('4ta Temporada 🏎')

current_time = datetime.now()
year = '2024'
month = '6'
day = '6'
hora = '22'
minuto = '48'
hora_limite = datetime.strptime(f"{year}-{month}-{day} {hora}:{minuto}", '%Y-%m-%d %H:%M')

st.write(current_time)
if current_time < hora_limite:
    st.write('ok')


tab1, tab2 = st.tabs(["Pronosticos", "Resultados"])
usuarios = pd.DataFrame({'Usuario': ['Seleccionar', 'Alex', 'Gerry', 'Giorgio', 'Mike']})
usuario_activo = st.sidebar.selectbox('Usuario', usuarios['Usuario'])

# Credenciales de Supabase
url = 'https://uehrgoqjfbdbkkyumtpw.supabase.co'
key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVlaHJnb3FqZmJkYmtreXVtdHB3Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTcwOTA3MDE1MywiZXhwIjoyMDI0NjQ2MTUzfQ.KIIsWOhJx7sPYYP6Wdvdq6S4vPJ8vrSrZbs-vG6kBWw'
supabase_client = create_client(url, key)

# Extraer la tabla de drivers
drivers = supabase_client.table('drivers').select("*").execute()
drivers = pd.DataFrame(drivers.data)
drivers = drivers.sort_values(by='driverId')
drivers = drivers['driverName']

admin = supabase_client.table('admin_control').select("*").execute()
race_inicial = admin.data[0]['RaceNo']
race_final = admin.data[1]['RaceNo']
st.write(race_inicial)
st.write(race_final)
admin_tbl = pd.DataFrame(admin.data)

resultados = supabase_client.table('Resultados').select("id,Race No,Race,Place,Result").execute()
resultados = pd.DataFrame(resultados.data)
resultados_all = resultados.copy()

pronosticos_all = supabase_client.table('Pronosticos').select("id,Race No,Race,Place,User,Forecast,Result").execute()
pronosticos_all = pd.DataFrame(pronosticos_all.data)

#función para actualizar data en supabase
def upload_forecast(dataframe: pd.DataFrame):
    data = dataframe.to_dict(orient="records")
    try:
        # Inserta o actualiza los datos en Supabase
        response = supabase_client.table('Pronosticos').upsert(data).execute()
        return response
    except Exception as e:
        return e

def upload_results(dataframe: pd.DataFrame):
    data = dataframe.to_dict(orient="records")
    try:
        # Inserta o actualiza los datos en Supabase
        response = supabase_client.table('Resultados').upsert(data).execute()
        return response
    except Exception as e:
        return e

# Extraer la tabla de users

if usuario_activo != "Seleccionar":
    users = supabase_client.table('users').select("*").eq("user", usuario_activo).execute()
    if users.data:
        user_id = str(users.data[0]['id'])
        none_pswd = users.data[0]['password']
        user_pswd = str(users.data[0]['password'])
        # st.write(user_id)
        # st.write(user_pswd)

        if none_pswd is None:
            st.sidebar.caption("Registra tu password para ingresar tus pronosticos")
            new_password = st.sidebar.text_input("Password", type="password")
            if st.sidebar.button("Registrar Password"):
                supabase_client.table('users').update({"password": new_password}).eq("id", user_id).execute()
                st.sidebar.write("Tu password ha sido registrado, para continuar selecciona un usuario diferente y posteriormente vuelve a seleccionar tu usuario para que se actualice la información")

        

        else:
            current_password = st.sidebar.text_input("Ingresa tu Password", type="password")
            if current_password == user_pswd and current_time < hora_limite:
                pronosticos = supabase_client.table('Pronosticos').select("id,Race No,Race,Place,User,Forecast").eq("User", usuario_activo).neq("Place", "Top 3").neq("Place", "Top 5").order('id', desc=False).execute()
                pronosticos = pd.DataFrame(pronosticos.data)
                pronosticos = pronosticos.sort_values(by='id')
                pronosticos = pronosticos[(pronosticos['Race No'] >= race_inicial) & (pronosticos['Race No'] <= race_final)]
                edited_pronosticos = st.data_editor(pronosticos, column_config={
                    "Forecast": st.column_config.SelectboxColumn(options=drivers)
                }, disabled=["Race No", "Race", "Place", "Fecha Carrera", "User", "Result", "id"], hide_index=True)
                if st.button('Cargar pronosticos'):
                    # response = upload_to_supabase(edited_pronosticos)
                    upload_forecast(edited_pronosticos)
                    st.write(f'Tus pronosticos han sido actualizados correctamente, recuerda que los puedes editar hasta el : {hora_limite}')
            if usuario_activo == "Mike" and current_password == user_pswd:
                race_inicial_update = st.sidebar.number_input("Ingresa la carrera inicial", step=1)
                race_final_update = st.sidebar.number_input("Ingresa la carrera Final", step=1)
                if st.sidebar.button('Actualizar Race Filter'):
                    data, count = supabase_client.table('admin_control').update({'RaceNo': race_inicial_update}).eq('id', 1).execute()
                    data, count = supabase_client.table('admin_control').update({'RaceNo': race_final_update}).eq('id', 2).execute()
                    st.sidebar.write('La configuración de las carreras ha sido cargado')

                # st.write('resultados')
                resultados = resultados[(resultados['Race No'] >= race_inicial) & (resultados['Race No'] <= race_final)]
                st.write('resultados')
                edited_resultados = st.data_editor(resultados, column_config={
                    "Result": st.column_config.SelectboxColumn(options=drivers)
                }, disabled=["Race No", "Race", "Place", "id"], hide_index=True)
    
                if st.button('Cargar resultados'):
                    # response = upload_to_supabase(edited_pronosticos)
                    upload_results(edited_resultados)
                    st.write('Los resultados han sido cargados con exito')
                
                

    
    else:
        st.error("Usuario no encontrado.")


pronosticos_all['key1'] = pronosticos_all['Race'] + pronosticos_all['Place']
# st.dataframe(pronosticos_all)
resultados_all['key1'] = resultados_all['Race'] + resultados_all['Place']
pronosticos_all = pronosticos_all.merge(resultados_all, left_on="key1", right_on='key1', how='left', suffixes=('', '_Results'))
def puntos(row):
        if row['Place'].startswith("1st") and (row['Forecast'] == row['Result']):
            return 5
        elif row['Place'].startswith("2nd") and (row['Forecast'] == row['Result']):
            return 4
        elif row['Place'].startswith("3rd") and (row['Forecast'] == row['Result']):
            return 3
        elif row['Place'].startswith("4th") and (row['Forecast'] == row['Result']):
            return 2
        elif row['Place'].startswith("5th") and (row['Forecast'] == row['Result']):
            return 1
        else:
            return 0

pronosticos_all['Puntos'] = pronosticos_all.apply(puntos, axis=1)

# st.dataframe(pronosticos_all)







# fin prueba codigo gpt
    
    
    # if usuario_activo is not "Seleccionar" and user_pswd is not None:
    # user_id = users.data[0]['id']
    # user_pswd = users.data[0]['password']
    # if pd.isna(clave_jugador):
    # #     st.caption("Registra tu password para ingresar tus pronosticos")
    #     users = users[users['user'] == usuario_activo]
    #     st.dataframe(users)
    #     # players =  players[['user_key']]
    #     # edited_players = st.data_editor(players, column_config={"user_key": st.column_config.TextColumn("Password", max_chars=10,)}, hide_index=True,)
    #     # conn.update(worksheet="Players", data=edited_players)



# st.write(users)





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



