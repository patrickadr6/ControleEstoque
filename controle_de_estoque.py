import sys
from datetime import datetime, date
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


df = pd.DataFrame(columns=['Nome', 'Quantidade', 'Validade'])
today = date.today()

def dias(x):
    if type(x) != str:
        if x > today:
            return f"{datetime.strptime(str(x), '%Y-%m-%d').strftime('%d/%m/%Y')} - Vencimento em {(x-today).days} dia(s)"
        elif x == today:
            return "Vence hoje"
        return f"{datetime.strptime(str(x), '%Y-%m-%d').strftime('%d/%m/%Y')} - Venceu há {(today-x).days} dia(s)"
    else:
        return x
    return ""


def alterar():
    def to_quit(x):
        if x == 'q': return
    if df.empty:
        return print("A tabela está vazia!\n")
    print("\nDigite 'q' a qualquer momento para cancelar")
    
    while True:
        m_col = input("Digite a coluna desejada: \n").capitalize()
        to_quit(m_col)
        if m_col not in df.columns:
            print("Nome de coluna inválido, tente novamente!")
            continue

        m_lin = input("Linha da coluna a ser alterada: \n")
        to_quit(m_lin)

        m_lin2 = input("Novo valor: \n")
        to_quit(m_lin2)
    
        if m_col == "Validade":
            df.at[int(m_lin), m_col] = datetime.strptime(m_lin2, "%d/%m/%Y").date()
            df['Validade'] = df['Validade'].apply(dias)
            break
        
        else: 
            df.at[int(m_lin), m_col] = m_lin2
            break


def excluir():
    if df.empty:
        print("A tabela está vazia!")
        return
    try:
        linha = int(input("Número da linha a ser apagada (ou digite 'q' para cancelar): "))
        df.drop(
            labels=linha,
            axis=0,
            inplace=True
        )
        df.index = pd.RangeIndex(len(df.index))
    except Error as err:
        print(err)

def criar_pdf():
    if df.empty:
        print("A tabela está vazia!")
        return
    nome_pdf = input("Digite o nome desejado do arquivo, incluindo a extensão .pdf (exemplo: controle de estoque.pdf)\nDigite 'q' para cancelar\n")
    fig, ax = plt.subplots(figsize=(12,4))
    ax.axis('tight')
    ax.axis('off')
    the_table = ax.table(cellText=df.values,colLabels=df.columns,loc='center')
    pp = PdfPages(nome_pdf)
    pp.savefig(fig, bbox_inches='tight')
    pp.close()
    print("PDF criado!\n")

        
def cadastro():
    while True:
        pegar_nome = input("Digite o nome do produto (ou digite 'q' para voltar ao menu): ")
        if pegar_nome == "q": break
            
        pegar_quant = input(f"Digite a quantidade de {pegar_nome}: ")
        while True:
            try:
                pegar_data = input('Qual a data de validade (no formato "dd/mm/aaaa")? Deixe vazio caso não tenha: ')
                if pegar_data: 
                    pegar_data = datetime.strptime(pegar_data, "%d/%m/%Y").date()
            except ValueError as err:
                print("Data Inválida!")
                continue
            else:
                df.loc[len(df.index)] = [pegar_nome, pegar_quant, pegar_data]
                break
        print(f"Produto '{pegar_nome}' adicionado!\n\n")

                
while True:
    print("*******************  Controle de estoque  *******************")
    df['Validade'] = df['Validade'].apply(dias)
    print(df)
    acao = input("Digite o que quer fazer:\n1 - Adicionar produto\n2 - Alterar algum dado\n3 - Excluir linha\n4 - Fazer PDF\n5 - Sair\n")
    
    if acao == '1':
        cadastro()
    elif acao == '2':
        alterar()
    elif acao == '3':
        excluir()
    elif acao == '4':
        criar_pdf()
    elif acao == '5':
        sys.exit()
    else: continue

    
    