import tabula
import pandas as pd
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

def juntar_df_tables(df_list):
    """
    Organiza N tabelas estruturadas extraídas de um PDF em um único DataFrame.
    Estrutura fixa: mesmo número de colunas e ordem.
    """
    N = len(df_list)

    for i in range(1, N):
        valores_primeira_linha = df_list[i].columns.tolist()

        # Conversão para int nas posições fixas
        for j in [0, 2, 5, 11]:
            try:
                valores_primeira_linha[j] = int(str(valores_primeira_linha[j]).strip())
            except (ValueError, TypeError):
                pass

        # Remover os dois últimos caracteres nas colunas 9 e 10
        valores_primeira_linha[9] = valores_primeira_linha[9][:-2]
        valores_primeira_linha[10] = valores_primeira_linha[10][:-2]

        # Unificar colunas
        df_list[i].columns = df_list[0].columns

        # Inserir primeira linha original como dado
        nova_linha = pd.DataFrame([valores_primeira_linha], columns=df_list[0].columns)
        df_list[i] = pd.concat([nova_linha, df_list[i]], ignore_index=True)

    # Concatena todas as tabelas de uma vez
    df = pd.concat(df_list, ignore_index=True)

    # Converter coluna NUMERO para inteiro (tratando 'SN' como nulo)
    df['NUMERO'] = pd.to_numeric(df['NUMERO'].replace('SN', None), errors='coerce').astype('Int64')

    return df


# # Extraia TODAS as tabelas do PDF (modifique o caminho para o seu arquivo)
df_list = tabula.read_pdf("unidades_correios_atestmed.pdf", pages='all', lattice=True, multiple_tables=True)

df = juntar_df_tables(df_list)
df.to_csv('CEP_unid_correios.csv', index=False, encoding='utf-8')
# # Salva em CSV para uso posterior
# df_ceps.to_csv('ceps_200.csv', index=False, encoding='utf-8')
print(df.head())