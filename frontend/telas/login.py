import streamlit as st
import requests

API_URL="http://localhost:8000"

email=st.text_input("Email")
senha=st.text_input(
"Senha",
type="password"
)

if st.button("Entrar"):

    dados={
        "email":email,
        "senha":senha
    }

    r=requests.post(
        f"{API_URL}/login",
        json=dados
    )

    if r.status_code==200:
        st.success("Logado")