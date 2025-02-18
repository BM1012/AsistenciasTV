# import gdown
import streamlit as st
import pandas as pd
# from PIL import Image
# import io
import datetime

dfusuarios = pd.read_csv('PASS-ST.csv')


usuarios_permitidos = ['lfortunato', 'clopez', 'bsanabria',
                       'omoctezuma', 'molguin', 'jreyes', 'amendoza', 'aherrera']

# tv = "https://drive.google.com/uc?export=view&id=1OVkp45Xs0PDDI174eMz8ytfWhsWF5dHN"
hoy = datetime.datetime.now()


def validar_usuario(usuario, clave):

    if len(dfusuarios[(dfusuarios['User'] == usuario) & (dfusuarios['Password'] == clave)]) > 0:
        return True
    else:
        return False


def generarMenu(usuario):
    url = 'https://raw.githubusercontent.com/BM1012/AsistenciasTV/main/PERMISOS.csv'

    df_filtered = pd.read_csv(url, encoding='latin-1')
    if st.session_state['usuario'] in ['omoctezuma', 'molguin', 'jreyes', 'amendoza', 'aherrera']:
        df_filtered = df_filtered[df_filtered['AREA']
                                  == st.session_state['area']]
    num_coincidenciasG = (df_filtered['ID'] == 0).sum()
    num_coincidenciasD = (df_filtered['ID'] == 1).sum()
    with st.sidebar:
        st.image(
            "C:/Users/Bruno Sanabria/Pictures/Screenshots/Captura de pantalla 2025-02-14 171552.png", use_container_width=True)
        usuario_df = dfusuarios[(dfusuarios['User'] == usuario)]
        nombre = usuario_df['Ejecutivo'].iloc[0]
        st.write(f'Usuario: **:blue-background[{nombre}]** ')
        st.write(f"Fecha: **:blue-background[{hoy.strftime('%d/%m/%Y')}]** ")
        if st.session_state['usuario'] in usuarios_permitidos:
            st.page_link('Inicio.py', label='Inicio', icon="🏠")
        st.subheader("Asistencia")
        st.page_link('pages/1_Asistencia.py', label="Dashboard", icon="📊")
        st.page_link('pages/4_AsistenciaINC.py', label="DEMO", icon="💻")
        st.page_link('pages/3_AsistenciaVC.py', label="Vacaciones", icon="🏖️")

        if st.session_state['usuario'] in ['lfortunato', 'clopez', 'bsanabria']:
            comercial = df_filtered[((df_filtered['AREA']) == 'Comercial') & (
                (df_filtered['ID']).any() == '0')]
            rrhh = df_filtered[((df_filtered['AREA']) ==
                               'Recursos humanos') & ((df_filtered['ID']).any() == '0')]

            print(f'Este es el df comercial: {comercial}')
            print(f'Este es el df RRHH: {rrhh}')

            if len(comercial) > 0 or len(rrhh) > 0:
                if (df_filtered['ID'] == 0).any():
                    st.page_link('pages/5_AsistenciaDemo.py',
                                 label=f":red[Incidencias ({num_coincidenciasG})]", icon="❗")
                else:
                    st.page_link('pages/5_AsistenciaDemo.py',
                                 label="Incidencias", icon="😷")
            else:
                if (df_filtered['ID'] == 1).any():
                    st.page_link('pages/5_AsistenciaDemo.py',
                                 label=f":red[Incidencias ({num_coincidenciasD})]", icon="❗")
                else:
                    st.page_link('pages/5_AsistenciaDemo.py',
                                 label="Incidencias", icon="😷")
        else:
            if st.session_state['usuario'] in ['omoctezuma', 'molguin', 'jreyes', 'amendoza', 'aherrera']:
                if (df_filtered['ID'] == 0).any():
                    st.page_link('pages/5_AsistenciaDemo.py',
                                 label=f":red[Incidencias ({num_coincidenciasG})]", icon="❗")
                else:
                    st.page_link('pages/5_AsistenciaDemo.py',
                                 label="Incidencias", icon="😷")
            else:
                st.page_link('pages/5_AsistenciaDemo.py',
                             label="Incidencias", icon="😷")
        # st.subheader("Evaluaciones")
        btn_salir = st.button("Salir")
        if btn_salir:
            st.session_state.clear()
            st.rerun()


def generarLogin():

    if 'usuario' in st.session_state:
        generarMenu(st.session_state['usuario'])
    else:
        with st.form('frmLogin'):
            st.title("TRUST :grey[VALUE]")
            parUsuario = st.text_input('Usuario')
            parPassword = st.text_input('Password', type="password")
            btnLogin = st.form_submit_button('Ingresar', type="primary")
            if btnLogin:
                usuario_df = dfusuarios[dfusuarios['User'] == parUsuario]
                if usuario_df.empty:
                    st.error('Usuario no encontrado',
                             icon=':material/gpp_maybe:')
                else:
                    usuario_df = dfusuarios[(dfusuarios['User'] == parUsuario)]
                    area = usuario_df['Area'].iloc[0]
                    colab = usuario_df['Ejecutivo'].iloc[0]
                    nombre = usuario_df['Ejecutivo'].iloc[0]
                    if validar_usuario(parUsuario, parPassword):
                        st.session_state['usuario'] = parUsuario
                        st.session_state['colab'] = colab
                        st.session_state['area'] = area
                        st.session_state['Nombre'] = nombre
                        if parUsuario not in usuarios_permitidos:
                            st.switch_page("pages/1_Asistencia.py")
                        else:
                            st.switch_page("Inicio.py")
                    else:
                        st.error('Usuario o clave incorrecto',
                                 icon=':material/gpp_maybe:')
