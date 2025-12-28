import streamlit as st
import mysql.connector
import pandas as pd

st.set_page_config(page_title="GTS", layout="wide")

st.title("Graduate Thesis System (GTS)")
st.write("Welcome to the Graduate Thesis System")

# MySQL Connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="MYSQL_SIFREN",
    database="gts_db"
)

query = "SELECT thesis_no, title, year FROM thesis"
df = pd.read_sql(query, conn)

st.subheader("Thesis List")
st.dataframe(df)
