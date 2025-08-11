import pandas as pd
import random

from faker import Faker

'''
#https://www.youtube.com/watch?v=VuizzwyjEU4&t=69s
Criar lista falsa de usuarios com email correlacionados com os nomes.
Utilização de banco de ceps para ter correspondecias reais e aleatórias.
'''


import warnings
df = pd.read_csv('CEP_unid_correios.csv')
cep=df['CEP']
fake = Faker('pt_BR')

def fake_name_email():
    #fake = Faker('pt_BR')
    # Lista de gêneros possíveis
    generos = ['M', 'F']
    # Escolhe um gênero aleatório
    genero = random.choice(generos)
    # Gera o primeiro nome conforme o gênero escolhido
    if genero == 'M':
        primeiro_nome = fake.first_name_male()
    else:
        primeiro_nome = fake.first_name_female()

    sobrenome = fake.last_name()

    nome = f"{primeiro_nome} {sobrenome}"
    # nome = fake.name()
    titulos = ['sra.', 'srta.', 'sr.', 'dr.', 'dra.', 'dom']

    nomes = nome.lower().split()
    email_base = ''
    nome_base = ''
    if nomes[0] in titulos:
        if len(nomes) >= 3:
            email_base = f"{nomes[1]}.{nomes[-1]}"
            nome_base = nomes[1] + ' ' + nomes[-1]
        else:
            email_base = '.'.join(nomes[1:])
            nome_base = f"{nomes[1]}"
    else:
        if len(nomes) >= 2:
            email_base = f"{nomes[0]}.{nomes[-1]}"
            nome_base = nomes[0] + ' ' + nomes[-1]
        else:
            email_base = nomes[0]
            nome_base = f"{nomes[1]}"

    return nome_base, email_base + '@email.com', genero


dados = []
for i in range(1, 200):
    nome_base, email_base, genero = fake_name_email()
    data_nascimento = fake.date_of_birth(minimum_age=18, maximum_age=90)

    U = {'id': i,
         'nome': nome_base,
         'email': email_base,
         'telefone': fake.cellphone_number(),
         'cep': cep.sample(n=1).values[0],
         'data_nascimento': data_nascimento.strftime("%d-%m-%Y"),
         'genero': genero}
    dados.append(U)

df = pd.DataFrame(dados)
print(df)