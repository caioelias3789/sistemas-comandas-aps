import streamlit as st
import requests

API_URL = "https://sistema-comanda.onrender.com"

st.title("🔐 Login")

email = st.text_input("Email")

senha = st.text_input(
    "Senha",
    type="password"
)

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

        else:

            st.error(
                f"Erro {r.status_code}"
            )

            st.write(
                r.json()
            )

    except Exception as e:

        st.error(
            f"Erro conexão: {str(e)}"
        )