import requests
import json
import pandas as pd
import time
inicio = time.perf_counter()

#API DummyJSON: Serviço que fornece dados falsos para teste e desenvolvimento (https://dummyjson.com/)
#1 endpoints usuarios: info pessoas, dados de contato, ender, info bancária, detalhes de empresa
#2 endpoints produtos: nome produto, descrição , preço, desconto, avaliaçao, estoque, marca, categoria, imagens

# ETL - Extract, Transform, load

# EXTRACT
def extract_data(endpoints):
    response = requests.get(endpoints)
    if response.status_code == 200:  # status_code 200 é ok.
        return response.json()
    else:
        print(f"Erro ao extrair dados da API: {response.status_code}")
        return none


def load_data(data, path):
    id = data["id"]
    with open(f"{path}/{id}.json", "w") as file:
        json.dump(data, file)


def loop_load_data(endpoint, path, n):
    # Extract and load data
    for i in range(1, n + 1):
        data_e = extract_data(endpoint + str(i))
        if data_e:
            if 'user' in endpoint:
                load_data(data_e, path + 'raw/users_json')
            elif 'products' in endpoint:
                load_data(data_e, path + 'raw/products_json')
            else:
                print(f"[AVISO] Endpoint não reconhecido: {endpoint}")
                break

        else:
            print(f"erro ao extrair dados da API:{data_e}")
            break


def transform_data_json_csv(endpoint, path, n):
    for i in range(1, n + 1):
        if 'user' in endpoint:
            with open(path + 'raw/users_json/' + str(i) + '.json', 'r') as file:
                data = json.load(file)
                # convertendo para csv
                df = pd.DataFrame(data)
                df.to_csv(path + 'processed/users/' + str(i) + '.csv', index=False)
        elif 'products' in endpoint:
            with open(path + 'raw/products_json/' + str(i) + '.json', 'r') as file:
                data = json.load(file)
                data = {k: v for k, v in data.items() if
                        k not in ['tags', 'reviews', 'images']}  # Remover chaves problematicas.
                df = pd.DataFrame(data)
                df.to_csv(path + 'processed/products/' + str(i) + '.csv', index=False)
        else:
            print("erro com endpoint")
            break


# variaveis input
path='/home/akel/PycharmProjects/Lessons/programação/data/'
endpoints_user="https://dummyjson.com/users/"
endpoints_product="https://dummyjson.com/products/"
N=100

# extract em save data raw
print('extração iniciada')
inicio_extracao = time.perf_counter()
loop_load_data(endpoints_user,path,N)
loop_load_data(endpoints_product,path,N)
print('extração finalizada')

fim_extracao = time.perf_counter()

 # Transform to CSV and save em data process
inicio_transformacao = time.perf_counter()

transform_data_json_csv(endpoints_user,path,N)
transform_data_json_csv(endpoints_product,path,N)
fim_transformacao = time.perf_counter()


print(f"Tempo de extração: {fim_extracao- inicio_extracao} segundos")
print(f"Tempo de transformacao: {fim_transformacao- inicio_transformacao } segundos")
print(f"Tempo Total: {fim_transformacao- inicio} segundos")
