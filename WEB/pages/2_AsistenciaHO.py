import streamlit as st
import pandas as pd
import login as login

login.generarLogin()

if 'usuario' in st.session_state and 'area' in st.session_state:
    gsheet = '1DISw0wlrkcy76HPD7lGDrZ49yhK69jVJiIgF29tRFYo'
    # sheetid = '0'
    # url = f'https://docs.google.com/spreadsheets/d/{gsheet}/export?format=csv&gid={sheetid}&format'
    # st.write(url)
    sheetid = '583896735'
    url2 = f'https://docs.google.com/spreadsheets/d/{gsheet}/export?format=csv&gid={sheetid}&format'
    # st.write(url2)#

    # df = pd.read_csv(url)
    dfho = pd.read_csv(url2)

    df_filtered = dfho[dfho['ÁREA'] == st.session_state['area']]
    dfnew = df_filtered[['EJECUTIVO', 'MES',
                         'DÍA 1', 'DÍA 2']]

    # Encabezado
    st.title("TRUST :orange[VALUE]")
    # Dataframe
    tab1, tab2 = st.tabs(["Tablero", "Data"])
    with tab1:
        st.subheader("Tablero Home Office")

    with tab2:
        st.subheader("Base de datos")
        st.dataframe(dfnew, use_container_width=True, hide_index=True)
