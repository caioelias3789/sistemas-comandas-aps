import streamlit as st
import requests
import pandas as pd

API_URL = "https://sistemas-comandas-aps.onrender.com"

st.title("🍽️ Comandas")

# ==========================
# CARREGAR COMANDAS
# ==========================

try:

    r = requests.get(
        f"{API_URL}/comandas",
        timeout=10
    )

    comandas=[]

    if r.status_code==200:
        comandas=r.json()

except:

    comandas=[]


# ==========================
# LISTAR COMANDAS
# ==========================

if len(comandas)>0:

    tabela=[]

    for c in comandas:

        tabela.append({

            "ID":c["id"],
            "Mesa":c["mesa"],
            "Status":c["status"],
            "Total":c["total"]

        })

    st.dataframe(
        pd.DataFrame(tabela),
        use_container_width=True
    )

else:

    st.info(
        "Nenhuma comanda cadastrada"
    )


st.divider()


# ==========================
# NOVA COMANDA
# ==========================

st.subheader(
    "Nova comanda"
)

mesa=st.number_input(
    "Mesa",
    min_value=1
)

if st.button(
    "Criar"
):

    resposta=requests.post(
        f"{API_URL}/comandas",
        json={
            "mesa":mesa
        }
    )

    if resposta.status_code==200:

        st.success(
            "Comanda criada"
        )

        st.rerun()

    else:

        st.error(
            "Erro ao criar"
        )


st.divider()


# ==========================
# ADICIONAR PRODUTOS
# ==========================

st.subheader(
    "Adicionar produto na comanda"
)

try:

    r=requests.get(
        f"{API_URL}/produtos"
    )

    produtos=[]

    if r.status_code==200:
        produtos=r.json()

except:

    produtos=[]


if len(comandas)>0 and len(produtos)>0:

    lista_comandas={

        f"Mesa {c['mesa']}":
        c["id"]

        for c in comandas

    }

    lista_produtos={

        p["nome"]:
        p["id"]

        for p in produtos

    }

    comanda=st.selectbox(
        "Escolha a comanda",
        list(lista_comandas.keys())
    )

    produto=st.selectbox(
        "Produto",
        list(lista_produtos.keys())
    )

    quantidade=st.number_input(
        "Quantidade",
        min_value=1,
        value=1
    )

    if st.button(
        "Adicionar"
    ):

        resposta=requests.post(
            f"{API_URL}/itens",
            json={

                "comanda_id":
                lista_comandas[comanda],

                "produto_id":
                lista_produtos[produto],

                "quantidade":
                quantidade
            }
        )

        if resposta.status_code==200:

            st.success(
                "Produto adicionado"
            )

            st.rerun()

        else:

            st.error(
                f"Erro: {resposta.text}"
            )

else:

    st.warning(
        "Cadastre produtos e comandas primeiro"
    )