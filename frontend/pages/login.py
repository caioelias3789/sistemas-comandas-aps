import streamlit as st
import requests

API_URL = "https://sistema-comanda.onrender.com"

st.title("🔐 Login")

email = st.text_input(
    "Email"
).strip()

senha = st.text_input(
    "Senha",
    type="password"
).strip()

if st.button("Entrar"):

    dados = {
        "email": email,
        "senha": senha
    }

    try:

        r = requests.post(
            f"{API_URL}/login",
            json=dados
        )

        if r.status_code == 200:

            usuario = r.json()

            st.success(
                f"Bem-vindo {usuario['nome']}"
            )

            st.session_state["logado"] = True
            st.session_state["usuario"] = usuario

        else:

            st.error(
                f"Erro: {r.text}"
            )

    except Exception as e:

        st.error(
            f"Falha conexão: {str(e)}"
        )