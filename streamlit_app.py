import pandas as pd
import streamlit as st
#from pulp import *

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='Activity Distribuciones',
    page_icon=':sunglasses:', # This is an emoji shortcode. Could be a URL too.
)


st.title("DESPACHADOR")

st.write(
    "Despachar"
)

####
stock_minimo_codigo = 0
peso_venta = 3
peso_stock_alto = 1.5

Ruta = 'Base_Estandar_Cupo.xlsx'
Pestaña_Excel_1 = 'cupo'
Pestaña_Excel_2 = 'cod'
Pestaña_Excel_3 = 'venta_cod'
Pestaña_Excel_4 = 'venta_agr'
Pestaña_Excel_5 = 'inv_cod'

#Importar Excel
df_cupo = pd.read_excel(Ruta,sheet_name=Pestaña_Excel_1,header=0)
#df_cod = pd.read_excel(Ruta,sheet_name=Pestaña_Excel_2,header=0)
#df_venta_cod = pd.read_excel(Ruta,sheet_name=Pestaña_Excel_3,header=0)
#df_venta_agr = pd.read_excel(Ruta,sheet_name=Pestaña_Excel_4,header=0)
#df_inv_cod = pd.read_excel(Ruta,sheet_name=Pestaña_Excel_5,header=0)


####
st.write(df_cupo)


st.write(
    "Now I want to evaluate the responses from my model. "
    "One way to achieve this is to use the very powerful `st.data_editor` feature. "
    "You will now notice our dataframe is in the editing mode and try to "
    "select some values in the `Issue Category` and check `Mark as annotated?` once finished 👇"
)

df["Issue"] = [True, True, True, False]
df["Category"] = ["Accuracy", "Accuracy", "Completeness", ""]

new_df = st.data_editor(
    df,
    column_config={
        "Questions": st.column_config.TextColumn(width="medium", disabled=True),
        "Answers": st.column_config.TextColumn(width="medium", disabled=True),
        "Issue": st.column_config.CheckboxColumn("Mark as annotated?", default=False),
        "Category": st.column_config.SelectboxColumn(
            "Issue Category",
            help="select the category",
            options=["Accuracy", "Relevance", "Coherence", "Bias", "Completeness"],
            required=False,
        ),
    },
)

st.write(
    "You will notice that we changed our dataframe and added new data. "
    "Now it is time to visualize what we have annotated!"
)

st.divider()

st.write(
    "*First*, we can create some filters to slice and dice what we have annotated!"
)

col1, col2 = st.columns([1, 1])
with col1:
    issue_filter = st.selectbox("Issues or Non-issues", options=new_df.Issue.unique())
with col2:
    category_filter = st.selectbox(
        "Choose a category",
        options=new_df[new_df["Issue"] == issue_filter].Category.unique(),
    )

st.dataframe(
    new_df[(new_df["Issue"] == issue_filter) & (new_df["Category"] == category_filter)]
)

st.markdown("")
st.write(
    "*Next*, we can visualize our data quickly using `st.metrics` and `st.bar_plot`"
)

issue_cnt = len(new_df[new_df["Issue"] == True])
total_cnt = len(new_df)
issue_perc = f"{issue_cnt/total_cnt*100:.0f}%"

col1, col2 = st.columns([1, 1])
with col1:
    st.metric("Number of responses", issue_cnt)
with col2:
    st.metric("Annotation Progress", issue_perc)

df_plot = new_df[new_df["Category"] != ""].Category.value_counts().reset_index()

st.bar_chart(df_plot, x="Category", y="count")

st.write(
    "Here we are at the end of getting started with streamlit! Happy Streamlit-ing! :balloon:"
)

