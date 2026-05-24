import streamlit as st
import requests

API_URL = "https://sistemas-comandas-aps.onrender.com"

st.title("🍽️ Comandas")

# ==========================
# BUSCAR COMANDAS
# ==========================

try:

    r = requests.get(
        f"{API_URL}/comandas",
        timeout=10
    )

    if r.status_code == 200:

        comandas = r.json()

    else:

        comandas = []

except:

    comandas = []


# ==========================
# LISTAR COMANDAS
# ==========================

if not comandas:

    st.info(
        "Nenhuma comanda cadastrada"
    )

else:

    st.subheader(
        "Comandas abertas"
    )

    for c in comandas:

        with st.container():

            col1, col2, col3 = st.columns(3)

            with col1:

                st.metric(
                    "Mesa",
                    c["mesa"]
                )

            with col2:

                st.metric(
                    "Status",
                    c["status"]
                )

            with col3:

                st.metric(
                    "Total",
                    f'R$ {c["total"]:.2f}'
                )

            st.divider()


# ==========================
# NOVA COMANDA
# ==========================

st.subheader(
    "Nova comanda"
)

mesa = st.number_input(
    "Mesa",
    min_value=1,
    value=1
)

if st.button(
    "Criar comanda"
):

    try:

        resposta = requests.post(
            f"{API_URL}/comandas",
            json={
                "mesa": mesa
            },
            timeout=10
        )

        if resposta.status_code in [200,201]:

            st.success(
                "Comanda criada"
            )

            st.rerun()

        else:

            st.error(
                f"Erro: {resposta.text}"
            )

    except Exception as e:

        st.error(
            str(e)
        )


st.divider()


# ==========================
# ADICIONAR PRODUTO
# ==========================

st.subheader(
    "Adicionar produto na comanda"
)

try:

    r_prod = requests.get(
        f"{API_URL}/produtos",
        timeout=10
    )

    produtos = r_prod.json()

except:

    produtos=[]


if comandas and produtos:

    lista_comandas = {

        f"Mesa {c['mesa']}":
        c["id"]

        for c in comandas
    }

    lista_produtos = {

        p["nome"]:
        p["id"]

        for p in produtos
    }

    comanda = st.selectbox(
        "Comanda",
        list(
            lista_comandas.keys()
        )
    )

    produto = st.selectbox(
        "Produto",
        list(
            lista_produtos.keys()
        )
    )

    quantidade = st.number_input(
        "Quantidade",
        min_value=1,
        value=1
    )

    if st.button(
        "Adicionar produto"
    ):

        try:

            resposta = requests.post(
                f"{API_URL}/itens",
                json={

                    "comanda_id":
                    lista_comandas[
                        comanda
                    ],

                    "produto_id":
                    lista_produtos[
                        produto
                    ],

                    "quantidade":
                    quantidade
                },
                timeout=10
            )

            if resposta.status_code in [200,201]:

                st.success(
                    "Produto adicionado"
                )

                st.rerun()

            else:

                st.error(
                    resposta.text
                )

        except Exception as e:

            st.error(
                str(e)
            )

else:

    st.warning(
        "Cadastre produtos e comandas primeiro"
    )