import streamlit as st
import unicodedata
import pandas as pd
import datetime as dt
import login as login
from github import Github

hoy = dt.datetime.now().strftime("%d/%m/%Y")
fecha_hora_actual = dt.datetime.now().strftime("%d/%m/%Y %H:%M:%S")


login.generarLogin()


if 'usuario' in st.session_state and 'area' in st.session_state:
    # Configuración de Google Sheets
    opcion = ['Aprobar', 'No aprobar', 'Pendiente'
              ]

    url = 'https://raw.githubusercontent.com/BM1012/AsistenciasTV/main/PERMISOS.csv'

    df_filtered = pd.read_csv(url, encoding='latin-1')
    filtro1 = pd.DataFrame(df_filtered)
    filtro2 = pd.DataFrame(df_filtered)
    filtro3 = pd.DataFrame(df_filtered)

    if st.session_state['usuario'] in ['omoctezuma', 'molguin', 'jreyes', 'amendoza', 'aherrera']:
        filtro1 = filtro1[filtro1['AREA'] == st.session_state['area']]
    elif st.session_state['usuario'] in ['lfortunato', 'clopez', 'bsanabria']:
        filtro1 = filtro1
    else:
        filtro1 = filtro1[(filtro1['AREA'] == st.session_state['area']) & (
            filtro1['COLABORADOR'] == st.session_state['colab'])]

    filtro1['ID'] = filtro1['ID'].replace(
        0, 'EN ESPERA DE CONFIRMACIÓN DE GERENTE')
    filtro1['ID'] = filtro1['ID'].replace(
        1, 'EN ESPERA DE CONFIRMACIÓN DE DIRECCIÓN')
    filtro1['ID'] = filtro1['ID'].replace(2, 'APROBADO')
    filtro1['ID'] = filtro1['ID'].replace(3, 'NO AUTORIZADO')
    filtro1 = filtro1[['COLABORADOR',
                       'FECHA', 'CONCEPTO', 'DETALLE', 'ID']]
    if st.session_state['usuario'] not in ['lfortunato', 'clopez', 'bsanabria']:
        filtro2 = filtro2[filtro2['AREA'] == st.session_state['area']]
    filtro2 = filtro2[filtro2[
        'ID'] == 0]
    filtro2['ID'] = filtro2['ID'].replace(
        0, False)
    filtro2 = filtro2[['COLABORADOR',
                       'FECHA', 'CONCEPTO', 'DETALLE']]
    print(f'2.- este es el filtro 2: {filtro2}')
    filtro2['AUTORIZACION'] = 'Pendiente'

    filtro3 = filtro3[filtro3[
        'ID'] == 1]
    filtro3 = filtro3[['COLABORADOR',
                       'FECHA', 'CONCEPTO', 'DETALLE']]
    filtro3['AUTORIZACION'] = 'Pendiente'

    st.title("TRUST :orange[VALUE]")
    # Dataframe
    if st.session_state['usuario'] in ['lfortunato', 'clopez', 'bsanabria']:
        tab1, tab2, tab3, tab4 = st.tabs(
            ["Incidencias", "Estatus", 'Solicitudes Gerentes', 'Solicitudes a Dirección'])
    elif st.session_state['usuario'] in ['omoctezuma', 'molguin', 'jreyes', 'amendoza', 'aherrera']:
        tab1, tab2, tab3 = st.tabs(
            ["Incidencias", "Estatus", 'Solicitudes'])
    else:
        tab1, tab2 = st.tabs(
            ["Incidencias", "Estatus"])

    with tab1:
        st.subheader("Envío de incidencias")

        today = dt.datetime.now()
        next_year = today.year
        jan_1 = dt.date(today.year, today.month, today.day)
        dec_31 = dt.date(next_year, 12, 31)
        fecha_hora_actual = dt.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        d = st.date_input(
            "Elige el día de la incidencia", min_value=today,
            format="DD.MM.YYYY"
        )

        e = st.selectbox("Selecciona la opción deseada:", options=[
                         'ENFERMEDAD', 'FALLECIMIENTO DIRECTO', 'FALLECIMIENTO INDIRECTO', 'MATERNIDAD', 'PATERNIDAD', 'MOTIVOS PERSONALES', 'CASOS FORTUITOS'])

        c = st.text_input("Justifica tu solicitud: ")

        c = unicodedata.normalize('NFKD', c).encode(
            'ASCII', 'ignore').decode('ASCII')

        datos_dict = {
            # Guardar el nombre directamente
            "COLABORADOR": st.session_state['colab'],
            # Guardar la opción directamente
            "AREA": st.session_state['area'],
            # Guardar las fechas seleccionadas
            "FECHA": d.strftime(format="%d/%m/%Y"),
            "CONCEPTO": e,     # Guardar el concepto
            'DETALLE': c,
            "REGISTRO": fecha_hora_actual,  # Columna de fecha y hora
            'ID': 0
        }

        permi = pd.DataFrame([datos_dict])  # Corregido: envolver en una lista

        def show_warning():
            st.warning(
                body='Los datos guardados, se enviaron correctamente para su confirmación')

        df = pd.DataFrame([datos_dict])
        df_completo = pd.concat([df_filtered, df], ignore_index=True)
        print(datos_dict)

        if st.button("Guardar", key='Guardar-solicitud'):
            df_completo.to_csv("PERMISOS.csv", index=False, encoding='latin-1')

            try:
                token = "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"
                g = Github(token)
                repo = g.get_repo("BM1012/AsistenciasTV")

                with open('PERMISOS.csv', 'r', encoding='latin-1') as file:
                    content = file.read()
                    estatus = content

                repo.update_file(
                    path='PERMISOS.csv',
                    message='Actualización automatica del archivo',
                    content=content,
                    # Obtener el SHA del archivo actual
                    sha=repo.get_contents("PERMISOS.csv").sha

                )
                st.success("Datos guardados correctamente")
                df_filtered = pd.read_csv(url, encoding='latin-1')
                filtro1 = pd.DataFrame(df_filtered)
                df_filtered = df_filtered[df_filtered[
                    'COLABORADOR'] == st.session_state['colab']]
                filtro1 = df_filtered[df_filtered[
                    'COLABORADOR'] == st.session_state['colab']]
                filtro1['ID'] = filtro1['ID'].replace(
                    0, 'EN ESPERA DE CONFIRMACIÓN DE GERENTE')
                filtro1['ID'] = filtro1['ID'].replace(
                    1, 'EN ESPERA DE CONFIRMACIÓN DE DIRECCIÓN')
                filtro1['ID'] = filtro1['ID'].replace(2, 'APROBADO')
                filtro1 = filtro1[['COLABORADOR',
                                   'FECHA', 'CONCEPTO', 'DETALLE', 'ID']]

            except Exception as e:
                st.error(f"Error al subir el archivo: {e}")

    with tab2:
        st.subheader("Base de datos")
        st.dataframe(filtro1, use_container_width=True, hide_index=True)
    try:
        with tab3:
            st.subheader("Solicitudes pendientes")
            edited_df = st.data_editor(filtro2, column_config={
                "AUTORIZACION": st.column_config.SelectboxColumn("AUTORIZACION", options=opcion, help="Selecciona si autoriza la incidencia", default='Pendiente')}, disabled=["widgets"], hide_index=True)
            # Botón para guardar los cambios
            if st.button('Guardar', key='Guardar-ConfirmarG'):
                # Verificar si algún checkbox está seleccionado
                # Verifica si algún valor en la columna 'ID' es True
                if not (edited_df['AUTORIZACION'] == 'Pendiente').all():

                    try:
                        # Leer el archivo CSV desde GitHub
                        df_filtered = pd.read_csv(url, encoding='latin-1')

                        # Obtener los índices de las filas seleccionadas (donde el checkbox está activado)
                        filas_seleccionadas = edited_df[edited_df['AUTORIZACION']
                                                        == 'Aprobar'].index
                        filas_seleccionadas_2 = edited_df[edited_df['AUTORIZACION']
                                                          == 'No aprobar'].index
                        filas_seleccionadas_3 = edited_df[edited_df['AUTORIZACION']
                                                          == 'Pendiente'].index

                        # Actualizar los valores de 'ID' en df_filtered para las filas seleccionadas

                        df_filtered.loc[filas_seleccionadas, 'ID'] = 1
                        df_filtered.loc[filas_seleccionadas_2, 'ID'] = 3
                        df_filtered.loc[filas_seleccionadas_3, 'ID'] = 0

                        # Guardar el archivo localmente

                        df_filtered.to_csv(
                            "PERMISOS.csv", index=False, encoding='latin-1')

                        # Subir el archivo a GitHub

                        token = "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"
                        g = Github(token)
                        repo = g.get_repo("BM1012/AsistenciasTV")

                        with open('PERMISOS.csv', 'r', encoding='latin-1') as file:
                            content = file.read()

                        repo.update_file(
                            path='PERMISOS.csv',
                            message='Actualización automática del archivo',
                            content=content,
                            # Obtener el SHA del archivo actual
                            sha=repo.get_contents("PERMISOS.csv").sha)
                        st.success("Datos guardados correctamente")
                    except Exception as e:
                        st.error(f"Error al subir el archivo: {e}")
                else:
                    st.warning(
                        "No se seleccionó ninguna incidencia para autorizar.")
    except:
        print("No existe el bloque")

    try:
        with tab4:
            st.subheader("Solicitudes pendientes")
            edited_df = st.data_editor(filtro3,  column_config={
                "AUTORIZACION": st.column_config.SelectboxColumn("AUTORIZACION", options=opcion, help="Selecciona si autoriza la incidencia", default='Pendiente')}, disabled=["widgets"], hide_index=True, key='BaseDire')
            # Botón para guardar los cambios
            if st.button('Guardar', key='Guardar-ConfirmarDR'):
                # Verificar si algún checkbox está seleccionado
                if not (edited_df['AUTORIZACION'] == 'Pendiente').all():

                    try:
                        # Leer el archivo CSV desde GitHub
                        df_filtered = pd.read_csv(url, encoding='latin-1')

                        # Obtener los índices de las filas seleccionadas (donde el checkbox está activado)
                        filas_seleccionadas = edited_df[edited_df['AUTORIZACION']
                                                        == 'Aprobar'].index
                        filas_seleccionadas_2 = edited_df[edited_df['AUTORIZACION']
                                                          == 'No aprobar'].index
                        filas_seleccionadas_3 = edited_df[edited_df['AUTORIZACION']
                                                          == 'Pendiente'].index

                        # Actualizar los valores de 'ID' en df_filtered para las filas seleccionadas

                        df_filtered.loc[filas_seleccionadas, 'ID'] = 1
                        df_filtered.loc[filas_seleccionadas_2, 'ID'] = 3
                        df_filtered.loc[filas_seleccionadas_3, 'ID'] = 0

                        # Guardar el archivo localmente

                        df_filtered.to_csv(
                            "PERMISOS.csv", index=False, encoding='latin-1')

                        # Subir el archivo a GitHub

                        token = "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"
                        g = Github(token)
                        repo = g.get_repo("BM1012/AsistenciasTV")

                        with open('PERMISOS.csv', 'r', encoding='latin-1') as file:
                            content = file.read()

                        repo.update_file(
                            path='PERMISOS.csv',
                            message='Actualización automática del archivo',
                            content=content,
                            # Obtener el SHA del archivo actual
                            sha=repo.get_contents("PERMISOS.csv").sha)
                        st.success("Datos guardados correctamente")
                    except Exception as e:
                        st.error(f"Error al subir el archivo: {e}")
                else:
                    st.warning(
                        "No se seleccionó ninguna incidencia para autorizar.")
    except:
        print("No existe el bloque")
