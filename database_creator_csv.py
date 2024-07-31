import pandas as pd
from faker import Faker
import random

fake = Faker('pt_BR')  # Configurar o Faker para o português do Brasil

# Configuração dos tamanhos
num_clientes = 50000
num_pedidos = 100000
num_produtos = 5000
num_categorias = 100
num_detalhes_pedidos = 100000  # Total de detalhes de pedidos

# Gerar dados de clientes (incluindo endereços)
def gerar_clientes(num):
    clientes = []
    for _ in range(num):
        clientes.append([
            fake.uuid4(),
            fake.name(),
            fake.email(),
            fake.phone_number(),
            fake.date_of_birth(minimum_age=18, maximum_age=90).isoformat(),
            fake.date_this_decade().isoformat(),
            fake.cpf(),  # Adicionar CPF
            fake.street_address(),
            fake.building_number(),
            fake.bairro(),
            fake.city(),
            fake.estado_sigla(),  # Estado abreviado (UF)
            fake.postcode()  # CEP
        ])
    return clientes

# Gerar dados de pedidos
def gerar_pedidos(num, clientes):
    pedidos = []
    cliente_ids = [cliente[0] for cliente in clientes]
    for _ in range(num):
        pedidos.append([
            fake.uuid4(),
            random.choice(cliente_ids),
            fake.date_this_year().isoformat(),
            random.choice(['Pendente', 'Concluído', 'Cancelado']),
            round(random.uniform(10, 500), 2),
            random.choice(['Cartão de Crédito', 'Boleto', 'Transferência'])
        ])
    return pedidos

# Gerar dados de produtos (incluindo categorias)
def gerar_produtos(num, num_categorias):
    categorias = [fake.word() for _ in range(num_categorias)]
    produtos = []
    for i in range(num):
        produtos.append([
            f'produto_{i+1}',
            fake.word(),
            fake.text(max_nb_chars=200),
            round(random.uniform(5, 100), 2),
            random.choice(categorias),
            random.randint(0, 1000)
        ])
    return produtos

# Gerar dados de detalhes de pedidos
def gerar_detalhes_pedidos(num, pedidos, produtos):
    detalhes_pedidos = []
    pedido_ids = [pedido[0] for pedido in pedidos]
    produto_ids = [produto[0] for produto in produtos]
    for _ in range(num):
        detalhes_pedidos.append([
            fake.uuid4(),
            random.choice(pedido_ids),
            random.choice(produto_ids),
            random.randint(1, 5),
            round(random.uniform(5, 100), 2)
        ])
    return detalhes_pedidos

# Gerar os dados
clientes = gerar_clientes(num_clientes)
pedidos = gerar_pedidos(num_pedidos, clientes)
produtos = gerar_produtos(num_produtos, num_categorias)
detalhes_pedidos = gerar_detalhes_pedidos(num_detalhes_pedidos, pedidos, produtos)

# Função para salvar em arquivos CSV
def salvar_csv(dados, colunas, nome_arquivo):
    df = pd.DataFrame(dados, columns=colunas)
    df.to_csv(nome_arquivo, index=False, sep=',', encoding='utf-8')

# Definir colunas para cada tabela
colunas_clientes = [
    'cliente_id', 'nome', 'email', 'telefone', 'data_nascimento', 'data_cadastro', 'cpf',
    'rua', 'numero', 'bairro', 'cidade', 'estado', 'cep'
]
colunas_pedidos = ['pedido_id', 'cliente_id', 'data_pedido', 'status_pedido', 'total', 'metodo_pagamento']
colunas_produtos = ['produto_id', 'nome', 'descricao', 'preco', 'categoria', 'estoque']
colunas_detalhes_pedidos = ['detalhe_id', 'pedido_id', 'produto_id', 'quantidade', 'preco_unitario']

# Salvar os dados em arquivos CSV
salvar_csv(clientes, colunas_clientes, 'clientes.csv')
salvar_csv(pedidos, colunas_pedidos, 'pedidos.csv')
salvar_csv(produtos, colunas_produtos, 'produtos.csv')
salvar_csv(detalhes_pedidos, colunas_detalhes_pedidos, 'detalhes_pedidos.csv')

print("Dados gerados e salvos com sucesso em formato CSV!")
