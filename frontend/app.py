import streamlit as st
import requests

API_URL = "https://sistema-comanda.onrender.com"

st.set_page_config(
    page_title="Sistema de Comandas",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ======================
# SESSION
# ======================

if "logado" not in st.session_state:
    st.session_state.logado = False

if "tipo" not in st.session_state:
    st.session_state.tipo = None


# ======================
# ESCONDER SIDEBAR
# ======================

if not st.session_state.logado:

    st.markdown("""
    <style>
        section[data-testid="stSidebar"]{
            display:none;
        }
    </style>
    """, unsafe_allow_html=True)


# ======================
# LOGIN
# ======================

if not st.session_state.logado:

    st.title("🔐 Login")

    email = st.text_input(
        "Email"
    )

    senha = st.text_input(
        "Senha",
        type="password"
    )

    if st.button("Entrar"):

        try:

            resposta = requests.post(
                f"{API_URL}/login",
                json={
                    "email": email,
                    "senha": senha
                },
                timeout=10
            )

            # DEBUG
            st.write(
                "Status:",
                resposta.status_code
            )

            try:

                st.write(
                    "Resposta:",
                    resposta.json()
                )

            except:

                st.write(
                    "Resposta:",
                    resposta.text
                )

            # LOGIN OK

            if resposta.status_code == 200:

                dados = resposta.json()

                st.session_state.logado = True
                st.session_state.tipo = dados["tipo"]

                st.rerun()

            else:

                st.error(
                    "Falha no login"
                )

        except requests.exceptions.ConnectionError:

            st.error(
                "Não foi possível conectar ao backend"
            )

        except requests.exceptions.Timeout:

            st.error(
                "Servidor demorou para responder"
            )

        except Exception as e:

            st.error(
                f"Erro: {str(e)}"
            )


# ======================
# SISTEMA
# ======================

else:

    st.sidebar.title(
        "🍴 Sistema"
    )

    menu = []

    if st.session_state.tipo == "Admin":

        menu = [
            "Dashboard",
            "Produtos",
            "Comandas",
            "Relatórios"
        ]

    elif st.session_state.tipo == "Operador":

        menu = [
            "Dashboard",
            "Comandas"
        ]

    elif st.session_state.tipo == "Sistema":

        menu = [
            "Comandas",
            "Relatórios"
        ]

    pagina = st.sidebar.radio(
        "Menu",
        menu
    )

    if st.sidebar.button("Sair"):

        st.session_state.logado = False
        st.session_state.tipo = None

        st.rerun()

    # CARREGAR TELAS

    if pagina == "Dashboard":

        exec(
            open(
                "telas/dashboard.py",
                encoding="utf8"
            ).read()
        )

    elif pagina == "Produtos":

        exec(
            open(
                "telas/produtos.py",
                encoding="utf8"
            ).read()
        )

    elif pagina == "Comandas":

        exec(
            open(
                "telas/comandas.py",
                encoding="utf8"
            ).read()
        )

    elif pagina == "Relatórios":

        exec(
            open(
                "telas/relatorios.py",
                encoding="utf8"
            ).read()
        )