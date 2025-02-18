import streamlit as st
import datetime as dt
import pandas as pd
import login as login

login.generarLogin()

if 'usuario' in st.session_state and 'area' in st.session_state:
    gsheet = '1DISw0wlrkcy76HPD7lGDrZ49yhK69jVJiIgF29tRFYo'
    sheetid = '1662268283'
    url = f'https://docs.google.com/spreadsheets/d/{gsheet}/export?format=csv&gid={sheetid}&format'
    # st.write(url)

    df = pd.read_csv(url)

    fecha_hora_actual = dt.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    df_filtered = df[df['ÁREA'] == st.session_state['area']]
    dfnew = df_filtered[['EJECUTIVO', 'FECHA',
                         'MES']]

    days = []

    datos_dict = {
        # Guardar el nombre directamente
        "EJECUTIVO": 'Karen Mendoza',
        # Guardar la opción directamente
        "AREA": st.session_state['area'],
        "FECHA": days,  # Guardar las fechas seleccionadas
        "CONCEPTO": "Vacaciones",     # Guardar el concepto
        "REGISTRO": fecha_hora_actual  # Columna de fecha y hora
    }

    # Encabezado
    st.title("TRUST :orange[VALUE]")

    # Dataframe
    tab1, tab2 = st.tabs(["Tablero", "Data"])
    with tab1:
        st.subheader("Solicitud de vacaciones")

        today = dt.datetime.now()
        next_year = today.year
        jan_1 = dt.date(today.year, today.month, today.day)
        dec_31 = dt.date(next_year, 12, 31)

        d = st.date_input(
            "Elige tus días que requieres de vacaciones",
            (jan_1, dt.date(next_year, today.month, today.day)),
            jan_1,
            dec_31,
            format="DD.MM.YYYY",
        )

        # Verificar que el rango de fechas esté correctamente seleccionado
        if len(d) == 2:  # El usuario selecciona un rango de fechas
            start_date, end_date = d
            # Crear un rango de fechas entre start_date y end_date
            date_range = pd.date_range(start=start_date, end=end_date)
            # Convertir las fechas al formato deseado y agregarlas a la lista 'days'
            days.extend(date_range.strftime("%d.%m.%Y").tolist())
        elif len(d) == 1:  # Si el usuario selecciona un solo día
            days.append(d[0].strftime("%d.%m.%Y"))

        st.write(f"Los días que seleccionaste son: {days}")

        def show_warning():
            st.warning(
                body='Los datos guardados, se enviaron correctamente para su confirmación')

        st.button('Guardar', on_click=show_warning)

        print(f'Este es el diccionario: {datos_dict}')

    with tab2:
        st.subheader("Base de datos")
        st.dataframe(dfnew, use_container_width=True, hide_index=True)
