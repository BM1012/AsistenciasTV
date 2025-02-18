import streamlit as st
import utils
import login as login  # Importar el módulo completo
import pandas as pd
import plotly.graph_objects as go
import plotly_express as px
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="TrustValue",  # Titulo de la pagina
    layout="wide",  # Forma de layout ancho o compacto
    initial_sidebar_state="expanded")  # Definimos si el sidebar aparece expandido o colapsado

# Colores del fondo
backgroundColor = st.get_option('theme.secondaryBackgroundColor')
textColor = st.get_option('theme.textColor')

# Aplicando colores CSS
utils.local_css('estilos.css', backgroundColor)

# Definir paletas


login.generarLogin()  # Usar la función con el prefijo del módulo

if 'usuario' in st.session_state:
    st.title("TRUST :grey[VALUE]")
    st.subheader('Tablero de control')

    gsheet = '1DISw0wlrkcy76HPD7lGDrZ49yhK69jVJiIgF29tRFYo'
    sheetid = '0'
    urlasis = f'https://docs.google.com/spreadsheets/d/{gsheet}/export?format=csv&gid={sheetid}&format'

    sheetid = '583896735'
    urlho = f'https://docs.google.com/spreadsheets/d/{gsheet}/export?format=csv&gid={sheetid}&format'

    sheetid = '1662268283'
    urlvc = f'https://docs.google.com/spreadsheets/d/{gsheet}/export?format=csv&gid={sheetid}&format'

    df = pd.read_csv(urlasis)
    df2 = pd.read_csv(urlho)
    df3 = pd.read_csv(urlvc)

    days = {
        'Monday': 'LUNES',
        'Tuesday': 'MARTES',
        'Wednesday': 'MIÉRCOLES',
        'Thursday': 'JUEVES',
        'Friday': 'VIERNES'
    }

    # FECHA a datetime
    df['FECHA'] = pd.to_datetime(df['FECHA'])
    df['HORA REGISTRO EN…'] = pd.to_datetime(
        df['HORA REGISTRO EN…'], errors='coerce').dt.strftime("%H:%M:%S")
    df['R. EXCEDIDO'] = pd.to_numeric(
        df['R. EXCEDIDO'], errors='coerce')
    df['RETARDOS'] = pd.to_numeric(
        df['RETARDOS'], errors='coerce')
    df2['MES'] = pd.to_datetime(df2['MES FECHA'])
    df3['FECHA'] = pd.to_datetime(df3['FECHA'])

    mes_actual = datetime.now().month
    hoy = datetime.now()
    if mes_actual == 1:
        mes_anterior = 12
    else:
        if hoy.day > 17:
            mes_anterior = mes_actual - 1
        else:
            mes_anterior = mes_actual - 2 if mes_actual > 2 else 12
    dia_semana = days[hoy.strftime('%A')]

    # Filtro de asistencia
    df_anterior = df[(df['ÁREA'] == st.session_state['area'])
                     & (df['FECHA'].dt.month == (mes_anterior))]
    df_adminACT = df[df['FECHA'].dt.month == mes_actual]
    df_adminANT = df[df['FECHA'].dt.month == (mes_anterior)]

    if st.session_state['usuario'] not in ['lfortunato', 'clopez', 'bsanabria']:
        df_actual = df[(df['ÁREA'] == st.session_state['area'])
                       & (df['FECHA'].dt.month == mes_actual)]
        if len(df_actual) == 0:
            df_actual = df[(df['ÁREA'] == st.session_state['area']) & (
                df['FECHA'].dt.month == (12 if mes_actual > 2 else (mes_actual - 1)))]
    else:
        df_actual = df_adminACT
        if len(df_actual) == 0:
            df_actual = df[df['FECHA'].dt.month ==
                           (12 if mes_actual > 2 else (mes_actual - 1))]

    excedente = df_actual[['NOMBRE', 'R. EXCEDIDO']]
    excedente = excedente.groupby('NOMBRE', as_index=False)[
        'R. EXCEDIDO'].mean()
    excedente['ExcedenteRange'] = pd.cut(excedente['R. EXCEDIDO'], bins=[-0.01, 0.00, 5.99, 10.99, 100.99], labels=[
                                         'SIN RETARDO', '0 - 5 MINUTOS', '6 - 10 MINUTOS', 'MÁS DE 11 MINUTOS'], right=True, ordered=False)
    excedente = pd.DataFrame({
        'NOMBRE': excedente['NOMBRE'],
        'R. EXCEDENTE': excedente['R. EXCEDIDO'],
        'RANGOS': excedente['ExcedenteRange']
    })
    df_excedente = excedente[['NOMBRE', 'RANGOS']]
    excedente = excedente.groupby('RANGOS', as_index=False)[
        'NOMBRE'].count().sort_values(by='NOMBRE', ascending=True)

    if st.session_state['usuario'] not in ['lfortunato', 'clopez']:
        excedenteAnt = df_anterior
    else:
        excedenteAnt = df_adminANT

    mes_anterior = mes_actual - 2 if mes_actual > 2 else 12

    excedenteAnt = excedenteAnt.groupby('NOMBRE', as_index=False)[
        'R. EXCEDIDO'].mean()
    excedenteAnt['ExcedenteRange'] = pd.cut(excedenteAnt['R. EXCEDIDO'], bins=[-0.01, 0.00, 5.99, 10.99, 100.99], labels=[
        'SIN RETARDO', '0 - 5 MINUTOS', '6 - 10 MINUTOS', 'MÁS DE 11 MINUTOS'], right=True, ordered=False)
    excedenteAnt = pd.DataFrame({
        'NOMBRE': excedenteAnt['NOMBRE'],
        'R. EXCEDENTE': excedenteAnt['R. EXCEDIDO'],
        'RANGOS': excedenteAnt['ExcedenteRange']
    })

    excedenteAnt = excedenteAnt.groupby('RANGOS', as_index=False)[
        'NOMBRE'].count().sort_values(by='NOMBRE', ascending=True)

    excedente = pd.merge(excedente, excedenteAnt[['NOMBRE', 'RANGOS']],
                         on='RANGOS', how='left', suffixes=('', '_ANT'))

    # DATA FRAME GRUPOS
    df_delays = pd.DataFrame(data=excedente.items(), columns=[
                             "NOMBRE", "ExcedenteRange"])
    df_delays = df_delays.dropna()  # Eliminar filas con NaN

    # Crear un nuevo DataFrame con el conteo de ejecutivos por grupo
    df_delays = df_delays.groupby('ExcedenteRange')[
        'NOMBRE']  # .reset_index()

    # DAY_MAX == PICOS RETARDOS
    day_max = df_actual[['FECHA',
                         'NOMBRE', 'HORA REGISTRO EN…', 'R. EXCEDIDO']]
    day_max['FECHA'] = day_max['FECHA'].dt.date
    day_max = day_max.groupby('FECHA', as_index=False)[
        'R. EXCEDIDO'].max()
    day_max = day_max[day_max['R. EXCEDIDO'] > 0]
    day_max = pd.merge(day_max, df_actual[['NOMBRE',  'R. EXCEDIDO', 'HORA REGISTRO EN…']],
                       on='R. EXCEDIDO', how='left')  # Agregar columna R. EXCEDIDO
    day_max['MINUTOS OUT'] = day_max['R. EXCEDIDO'].astype(str) + \
        ' Minutos'

    # Filtro de home office
    dfho = df2[(df2['MES FECHA'] == mes_actual)]

    print(f'AQUI ESTA EL DF HOME DESPUES DE FILTRAR{dfho}')
    # Filtro de vacaciones
    # if st.session_state['usuario'] not in ['lfortunato', 'clopez']:
    #    dfvc = df3[(df3['ÁREA'] == st.session_state['area'])]
    # else:
    dfvc = df3
    dfvc = dfvc[dfvc['FECHA'] > (hoy - timedelta(days=1))]
    # Reinicio de formato para quitar la hora
    dfvc['FECHA'] = dfvc['FECHA'].dt.date
    # Filtrar columnas dfho
    dfho = dfho[
        (dfho['DÍA 1'] == dia_semana) |
        (dfho['DÍA 2'] == dia_semana)
    ]
    dfho = dfho[['EJECUTIVO', 'ÁREA']]
    # Filtrar columnas dfvc
    dfvc = dfvc[['EJECUTIVO', 'ÁREA', 'FECHA']]
    dfvc = dfvc.sort_values(by='FECHA', ascending=True)
    TOPasis = df_actual.groupby('NOMBRE', as_index=False)[
        'RETARDOS'].sum().sort_values(by='RETARDOS', ascending=False)
    TOPasis = TOPasis[TOPasis['RETARDOS'] > 0]

    fig = px.pie(TOPasis,
                 values='RETARDOS',  # Columna con los valores
                 names='NOMBRE',     # Columna con los nombres
                 title='Retardos - Colaborador',
                 width=800,  # Ajusta el ancho de la gráfica
                 height=550)  # Ajusta la altura de la gráfica
    fig.update_traces(textposition='outside',
                      textinfo='percent+label')

    dfeje = df_actual.groupby('NOMBRE', as_index=False)[
        'RETARDOS'].sum().sort_values(by='RETARDOS', ascending=False)
    dfeje = dfeje[dfeje['RETARDOS'] > 0]

    fig2 = px.bar(dfeje,
                  x='NOMBRE',
                  y='RETARDOS',
                  title='Reporte de retardos',
                  width=800,  # Ajusta el ancho de la gráfica
                  height=600)  # Ajusta la altura de la gráfica
    fig2.update_traces(textposition='outside')
    limite = 4
    fig2.add_shape(type='line',
                   # Ajustar x1 al último elemento
                   x0=-0.5, x1=len(dfeje['NOMBRE'].unique())-0.5,
                   y0=limite, y1=limite,  # Usa la suma de retardos como límite
                   line=dict(color='red', width=3, dash='dash'))

    # RETARDOS POR ÁREA // ADMINISTRADOR

    df_suma_retardos = df_actual[['ÁREA', 'RETARDOS']]
    mes_anterior = mes_actual - 2 if mes_actual > 2 else 12
    dfneww = df[df['FECHA'].dt.month == (mes_anterior)]
    dfneww = dfneww[['ÁREA', 'RETARDOS']]
    df_suma1 = dfneww.groupby('ÁREA', as_index=False)[
        'RETARDOS'].sum()
    df_suma_retardos = df_suma_retardos.groupby('ÁREA', as_index=False)[
        'RETARDOS'].sum()
    df_suma_retardos = pd.merge(
        df_suma_retardos, df_suma1[['ÁREA', 'RETARDOS']], on='ÁREA', how='left', suffixes=('', '_ANT'))
    limite = df_actual.groupby('ÁREA', as_index=False)[
        'NOMBRE'].nunique()
    limite['A_LIMITE'] = limite['NOMBRE'] * 4
    df_suma_retardos = pd.merge(
        df_suma_retardos, limite[['ÁREA', 'A_LIMITE']], on='ÁREA', how='left')

    fig3 = px.bar(df_suma_retardos,
                  x='ÁREA',
                  y=['RETARDOS', 'RETARDOS_ANT'],
                  title='Retardos por Área',
                  labels={'value': 'Cantidad de Retardos',
                          'variable': 'Tipo de Retardo'},
                  barmode='group',
                  width=800,  # Ajusta el ancho de la gráfica
                  height=600)  # Ajusta la altura de la gráfica
    fig3.update_traces(textposition='outside',
                       textfont=dict(size=16))

    for _, row in df_suma_retardos.iterrows():
        fig3.add_trace(
            go.Scatter(
                x=[row['ÁREA']],  # Posición en el eje x (área)
                y=[row['A_LIMITE']],  # Posición en el eje y (límite)
                mode='markers',  # Modo de marcador (puntos)
                showlegend=True,

                # Personalización del marcador
                marker=dict(color='black', size=8),
                name=f'Límite {row["ÁREA"]}'  # Nombre del punto (opcional)
            )
        )

    fig4 = px.bar(excedente,
                  y='RANGOS',
                  x=['NOMBRE', 'NOMBRE_ANT'],
                  title='Minutos Excedentes',
                  orientation='h',
                  labels={'value': 'Cantidad de Colaboradores',
                          'variable': 'Grupos',
                          'NOMBRE': 'ACTUAL',  # Cambia 'NOMBRE' por 'ACTUAL'
                          'NOMBRE_ANT': 'ANTERIOR'},  # Cambia 'NOMBRE_ANT' por 'ANTERIOR',
                  barmode='group',
                  width=600,  # Ajusta el ancho de la gráfica
                  height=400)  # Ajusta la altura de la gráfica
    fig4.update_layout(legend_title_text='Grupos',
                       legend=dict(traceorder='normal',
                                   itemsizing='constant',
                                   title_font=dict(size=12),
                                   font=dict(size=12)))

    # Cambiar los nombres de las etiquetas en la leyenda
    fig4.for_each_trace(lambda t: t.update(name='ACTUAL')
                        if t.name == 'NOMBRE' else t.update(name='ANTERIOR'))

    fig4.update_traces(textposition='inside',
                       textfont=dict(size=16, color='black', weight='bold'))

    columnas = st.columns(4)
    with st.container(key='container-indicadores'):
        with columnas[0]:
            retardos = ((df_actual['RETARDOS'].sum()) *
                        (100)/(df_actual['NOMBRE'].count()))
            puntualidad = 100 - retardos
            puntualidad = f'{puntualidad:.2f}%'
            st.metric(label='Porcentaje de puntualidad', value=puntualidad)
        with columnas[1]:
            h_efectivas = round(df_actual['HORAS EFECTIVAS'].mean(), 2)
            st.metric(label='Horas efectivas', value=h_efectivas)
        with columnas[2]:
            if st.session_state['usuario'] not in ['lfortunato', 'clopez']:
                st.metric(label='Área', value=st.session_state['area'])
            else:
                st.metric(label='Área', value='TV')
        with columnas[3]:
            if hoy.day < 16:
                mes_actual = (mes_actual - 2)
            else:
                mes_actual = (mes_actual - 1)
            meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
                     "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
            st.metric(label='Mes calculado', value=meses[mes_actual])

    # SE BUSCA COINCIDENCIAS EN DFHO Y DFVC
    dfho_filtrado = dfho[~dfho['EJECUTIVO'].isin(dfvc['EJECUTIVO'])]

    col1, col2 = st.columns(2)
    with col1:
        if len(dfvc) > 0:
            st.subheader("Próximas vacaciones")
            st.dataframe(dfvc, use_container_width=True,
                         key='data-vc', hide_index=True)
        else:
            st.metric(label='Próximas vacaciones', value="0")
    with col2:
        if hoy.day in [14, 15, 16, 30, 31, 1]:
            dfho_filtrado.dropna()
        st.subheader('Home Office')
        st.dataframe(dfho_filtrado, use_container_width=True,
                     key='data-ho', hide_index=True)
    # col3, col4 = st.columns([6, 4])
    # with col3:
    #     st.plotly_chart(
    #         utils.aplicarformatoChart(
    #             fig,
    #             backgroundColor=backgroundColor,
    #             textcolor=textColor
    #         ),
    #         key='chart-pie'
    #     )
    # with col4:
    #     st.subheader('Detalle / Retardos - Colaborador')
    #     st.dataframe(TOPasis, use_container_width=True,
    #                  key='tabla-top', hide_index=True, height=430)
    if st.session_state['usuario'] not in ['lfortunato', 'clopez']:
        col7, col8 = st.columns([6, 4])
        with col7:
            st.plotly_chart(utils.aplicarformatoChart(fig2, backgroundColor=backgroundColor,
                                                      textcolor=textColor), use_container_width=True, key='chart-bar')
        with col8:
            def color_puntuacion(val):
                if val > 4:
                    color = 'red'  # Rojo para puntuaciones bajas
                else:
                    color = textColor
                return f'color: {color}'
            TOPasis['RETARDOS'] = pd.to_numeric(
                TOPasis['RETARDOS'], errors='coerce').round(0).astype(int)
            styled_df = TOPasis.style.applymap(
                color_puntuacion, subset=['RETARDOS'])

            st.subheader('Detalle / Retardos - Colaborador')
            st.dataframe(styled_df, use_container_width=True,
                         key='tabla-top', hide_index=True, height=430)

    else:
        t1, t2 = st.tabs(['Áreas', 'Detalle'])
        with t1:
            st.plotly_chart(utils.aplicarformatoChart(fig3, backgroundColor=backgroundColor,
                            textcolor=textColor), use_container_width=True, key='chart-bar2')
        with t2:
            col7, col8 = st.columns([6, 4])
            with col7:
                st.plotly_chart(utils.aplicarformatoChart(fig2, backgroundColor=backgroundColor,
                                                          textcolor=textColor), use_container_width=True, key='chart-bar')
            with col8:
                def color_puntuacion(val):
                    if val > 4:
                        color = 'red'  # Rojo para puntuaciones bajas
                    else:
                        color = textColor
                    return f'color: {color}'
                TOPasis['RETARDOS'] = pd.to_numeric(
                    TOPasis['RETARDOS'], errors='coerce').round(0).astype(int)
                styled_df = TOPasis.style.applymap(
                    color_puntuacion, subset=['RETARDOS'])

                st.subheader('Detalle / Retardos - Colaborador')
                st.dataframe(styled_df, use_container_width=True,
                             key='tabla-top', hide_index=True, height=430)

    col5, col6 = st.columns([6, 4])
    with col5:
        st.plotly_chart(utils.aplicarformatoChart(fig4, backgroundColor=backgroundColor,
                                                  textcolor=textColor), use_container_width=True, key='chart-barnew')
        # st.plotly_chart(utils.aplicarformatoChart(fig5, backgroundColor=backgroundColor,
        #   textcolor=textColor), use_container_width=True, key='chart-barnew2')
    with col6:
        st.subheader('Detalle / Minutos Excedentes')
        st.dataframe(df_excedente, hide_index=True,
                     use_container_width=True, height=305)
