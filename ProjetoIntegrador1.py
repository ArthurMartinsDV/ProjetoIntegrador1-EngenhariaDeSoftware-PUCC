# Coding: utf-8
"""
Created on Tue Mar 28 08:11:01 2023

@author:
Arthur Magalhâes Peixoto de Oliveira
Arthur Martins Parmeggiani
Isbella Maria Tressino Bruno
Jose Eduardo Cunha Roppa
Luan de Campos Ferreira
Luigi Mazzoni Targa
"""

# Importações usadas
import getpass
import pandas as pd
import msvcrt
import oracledb 
from time import sleep
from os import system

# Exclui as mensagens que estavam no terminal
system("CLS")
sleep(1)

# Apresenta o tema do software com uma mensagem de bem vindo
print("-" * 80)
print("{:^80}".format("Bem vindo ao nosso software sobre amostras de ar"))
print("-" * 80)
print("\n")

# Exclui as mensagens que estavam no terminal
sleep(3)
system("CLS")
sleep(1)

# Input do usuario da conta do oracle
print("-" * 80)
print("{:^80}".format("Conta Oracle"))
print("-" * 80, "\n")
us = input("\nUsuario: ")

# Exclui as mensagens que estavam no terminal
system("CLS")

# Input da senha da conta do oracle
print("-" * 80)
print("{:^80}".format("Conta Oracle"))
print("-" * 80, "\n")
print("\nUsuario:", us)
pw = input("Senha: ")

# Realiza a conexão do banco de dados
connection = oracledb.connect(
    user=us,
    password=pw,
    dsn="172.16.12.14/XE"
)

# Exclui as mensagens que estavam no terminal
system("CLS")
sleep(1)

# Imprime a mensagem de sucesso ao conectar o banco de dados
print("-" * 80)
print("{:^80}".format("Sucesso ao conectar ao Oracle Database"))
print("-" * 80)

# Exclui as mensagens que estavam no terminal
sleep(3)
system("CLS")
sleep(1)

# Cria uma variavel indicador/cursor
cursor = connection.cursor()

# Tenta criar uma tabela
try:

    # Executa o create table atraves do SQL
    cursor.execute("""
        CREATE TABLE parametros (
            id_parametros NUMBER,
            mp10 NUMBER,
            mp25 NUMBER,
            so2 NUMBER,
            no2 NUMBER,
            o3 NUMBER,
            co NUMBER,
            CONSTRAINT parametros_pk PRIMARY KEY (id_parametros)
        )
    """)

# Caso a tabela ja exista
except:
    sleep(0)


# Função que verifica os valores inseridos ao mp10, mp25, so2, no2 ,o3 e co *quando chamada*
def valorParametro(parametro):

    # Verifica a integridade do valor inserido
    while True:
        try:

            # Atribui a variavel valor o valor do parametro digitado
            valor = float(input(parametro))

            # Caso seja maior ou igual a 0, é permitido o uso
            if valor >= 0:
                return valor
            
            # Caso seja menor que 0, não é permitido o uso
            else:

                # Exclui as mensagens que estavam no terminal
                system("CLS")

                # Imprime mensagem de aviso sobre a integridade do valor
                print("O valor deve ser maior ou igual a zero.")
                
                # Exclui as mensagens que estavam no terminal
                sleep(3)
                system("CLS")
                sleep(1)
        
        # Caso o valor não seja numerico, não é permitido o uso
        except ValueError:

            # Exclui as mensagens que estavam no terminal
            system("CLS")

            # Imprime mensagem de aviso sobre a integridade do valor
            print("Valor inválido. Digite um número válido.")
            
            # Exclui as mensagens que estavam no terminal
            sleep(3)
            system("CLS")
            sleep(1)

# Função para mostrar a tabela  de amostras usando a biblioteca pandas *quando chamada*
def mostrarTabela():

    # Verifica se a tabela contem algo
    cursor.execute("SELECT COUNT(*) FROM parametros")
    resultado = cursor.fetchone()[0]

    # Caso não tenha
    if resultado == 0:

        # Imprime a mensagem de que não foi encontrada nenhuma tabela
        print("Nenhuma tabela encontrada.\n")
    
    # Caso tenha
    else:

        # Executa o select atraves do SQL e imprime a tabela
        cursor.execute("SELECT id_parametros, mp10, mp25, so2, no2, o3, co FROM parametros ORDER BY id_parametros")
        colunas = [descricao[0] for descricao in cursor.description]
        valores = cursor.fetchall()
        nomeColunas = pd.DataFrame(valores, columns=colunas)
        print(nomeColunas)


# While para possibilitar que o menu seja processado mais de uma vez
while True:

    # Prints mostrando as funções do menu
    print("-" * 80)
    print("{:^80}".format("Menu"))
    print("-" * 80, "\n")
    print("\n1 - Cadastrar Amostras")
    print("2 - Alterar Amostras")
    print("3 - Excluir Amostras")
    print("4 - Consultar Amostras")
    print("5 - Classificar Amostras")
    print("0 - Sair do Software") 
    print("\n")

    # While para receber um caractere numérico (0 a 5) à variavel "escolha"
    while True:
            try:

                # Atribui à variavel qual funçao do menu foi escolhida
                escolha = int(msvcrt.getch())       
                break
            except:

                # Exclui mensagens que estavam no terminal
                system("CLS")
                sleep(1)

                # Imprime um aviso caso seja atribuido um valor invalido
                print("-" * 80)
                print("{:^80}".format("Digite um valor numérico"))
                print("-" * 80)

                # Exclui mensagens que estavam no terminal
                sleep(3)
                system("CLS")

    # Função para inserir amostras
    if escolha == 1:

        # Exclui mensagens que estavam no terminal
        system("CLS")
        sleep(1)

        # Imprime mensagem que explica como usar a função de inserir uma amostra
        print("-" * 80)
        print("{:^80}".format("Insira as amostras de cada parametro que deseja cadastrar"))
        print("-" * 80)
        print("\n")

        # Chamando a função para inserir os valores
        mp10 = valorParametro("Digite a quantidade de partículas inaláveis: ")
        mp25 = valorParametro("Digite a quantidade de partículas inaláveis finas: ")
        so2 = valorParametro("Digite a quantidade de dióxido de enxofre: ")
        no2 = valorParametro("Digite a quantidade de dióxido de nitrogênio: ")
        o3 = valorParametro("Digite a quantidade de ozônio: ")
        co = valorParametro("Digite a quantidade de monóxido de carbono: ")

        # Pega o maior valor do id_parametros e soma 1 caso tenha alguma tabela, senão é 0
        cursor.execute("select max(id_parametros) from parametros")
        id_registro = cursor.fetchone()[0]
        id_registro = id_registro + 1 if id_registro is not None else 0

        # Insere os dados na tabela
        cursor.execute(f"""insert into parametros (id_parametros, mp10, mp25, so2, no2, o3, co) values({id_registro}, {mp10},{mp25},{so2},{no2},{o3},{co}) """)

        # Exclui mensagens que estavam no terminal
        sleep(1)
        system("CLS")

        # Notificação de confirmação de atualização
        print("-" * 80)
        print("{:^80}".format("Registro cadastrado com sucesso!"))
        print("-" * 80)

        # Exclui mensagens que estavam no terminal
        sleep(3)
        system("CLS")

    # Função para alterar amostras
    if escolha == 2:

        # Exclui mensagens que estavam no terminal
        system("CLS")
        sleep(1)

        # Imprime mensagem que explica como usar a função de alterar uma amostra cadastrada
        print("-" * 80)
        print("{:^80}".format("Consulte a tabela de amostras para ver o ID de qual deseja alterar."))
        print("-" * 80)
        print("\n")

        # Mostra a tabela de amostras cadastradas
        mostrarTabela()
        print("\n")

        # Input para definir o ID da amostra que sera alterada
        id_registro = int(input("Digite o ID da amostra que deseja alterar: "))

        # Chama a função para alterar os valores
        mp10 = valorParametro("\nDigite a nova quantidade de partículas inaláveis: ")
        mp25 = valorParametro("Digite a nova quantidade de partículas inaláveis finas: ")
        so2 = valorParametro("Digite a nova quantidade de dióxido de enxofre: ")
        no2 = valorParametro("Digite a nova quantidade de dióxido de nitrogênio: ")
        o3 = valorParametro("Digite a nova quantidade de ozônio: ")
        co = valorParametro("Digite a nova quantidade de monóxido de carbono: ")

        # Executa o SQL com os valores substituídos
        cursor.execute(f""" UPDATE parametros 
            SET mp10 = {mp10}, 
            mp25 = {mp25}, 
            so2 = {so2}, 
            no2 = {no2}, 
            o3 = {o3}, 
            co = {co}
            WHERE id_parametros = {id_registro}""")

        # Exclui mensagens que estavam no terminal
        sleep(1)
        system("CLS")

        # Notificação de confirmação de atualização
        print("-" * 80)
        print("{:^80}".format("Registro alterado com sucesso!"))
        print("-" * 80)

        # Exclui mensagens que estavam no terminal
        sleep(3)
        system("CLS")

    # Função para excluir amostras
    if escolha == 3:

        # Exclui mensagens que estavam no terminal
        sleep(1)
        system("CLS")

        # Imprime mensagem que explica como usar a função de excluir uma amostra cadastrada
        print("-" * 80)
        print("{:^80}".format("Consulte a tabela de amostras para ver o ID de qual amostra deseja excluir."))
        print("-" * 80)
        print("\n")

        # Mostra a tabela de amostras cadastradas
        mostrarTabela()
        print("\n")

        # Executa o SQL para excluir a amostra desejada
        id_registro = int(input("Digite o ID da amostra que deseja excluir: "))
        cursor.execute(f"DELETE FROM parametros WHERE id_parametros = {id_registro}")

        # Exclui mensagens que estavam no terminal
        sleep(1)
        system("CLS")

        # Imprime a mensagem de confirmação que a amostra foi excluida
        print("-" * 80)
        print("{:^80}".format("Registro excluido com sucesso!"))
        print("-" * 80)
        
        # Exclui mensagens que estavam no terminal
        sleep(3)
        system("CLS")

    # Função para consultar as amostras cadastradas
    if escolha == 4:

        # Exclui mensagens que estavam no terminal
        sleep(1)
        system("CLS")

        while True:
            # Imprime mensagem que explica como voltar para o menu
            print("-" * 80)
            print("{:^80}".format("Para voltar ao menu pressione qualquer tecla!"))
            print("-" * 80)
            print("\n")

            # Mostra a tabela de amostras cadastradas
            mostrarTabela()
            print("\n")

            # Função para voltar ao menu apertando qualquer tecla
            try:
                sair = int(msvcrt.getch())       
                break
            except: 
                break
    
    # Função para classificar o uma amostra cadastrada
    if escolha == 5:
        
        # Exclui mensagens que estavam no terminal
        system("CLS")
        sleep(1)

        # Imprime mensagem que explica como usar a função de classificar uma amostra cadastrada
        print("-" * 80)
        print("{:^80}".format("Consulte a tabela de amostras para ver o id de qual amostra deseja classificar"))
        print("-" * 80)
        print("\n")

        # Mostra a tabela de amostras cadastradas
        mostrarTabela()
        print("\n")

        # Input para selecionar qual amostra sera consultada sua classificaçao
        id_amostra = int(input("Digite o ID da amostra que deseja classificar: "))

        # Exclui mensagens que estavam no terminal
        sleep(1)
        system("CLS")
        sleep(1)

        # Imprime mensagem que explica como voltar para o menu
        print("-" * 80)
        print("{:^80}".format("Para voltar ao menu pressione qualquer tecla!"))
        print("-" * 80)
        print("\n")

        # Define cada parametro como zero para puxar os reais valores por meio de select do SQL
        vmp10 = 0
        vmp25 = 0
        vso2 = 0
        vno2 = 0
        vo3 = 0
        vco = 0

        # Executa o SQL com o valor atribuido ao id_amostra para que mostre apenas a amostra consultada
        cursor.execute(f"SELECT id_parametros, mp10, mp25, so2, no2, o3, co FROM parametros WHERE id_parametros = {id_amostra}")
        colunas = [descricao[0] for descricao in cursor.description]
        valores = cursor.fetchall()
        nomeColunas = pd.DataFrame(valores, columns=colunas)

        # Imprime a amostra consultada
        print(nomeColunas)
        print("\n")

        # Imprime os resultados de acordo com a amostra inserida
        print("A média da qualidade do ar está", end=" ")

        # Executa o SQL com o valor atribuido ao id_amostra para atribuir os valores a cada variavel de cada parametro para
        # a classificaçao de acordo com o 'if'
        cursor.execute(f"SELECT id_parametros, mp10, mp25, so2, no2, o3, co FROM parametros WHERE id_parametros = {id_amostra}")
        for row in cursor: 
            vmp10 = int(row[1])
            vmp25 = int(row[2])
            vso2 = int(row[3])
            vno2 = int(row[4])
            vo3 = int(row[5])
            vco = int(row[6])

        # Compara os parametros para definir a classificaçao da amostra
        if vmp10 <= 50 and vmp25 <= 25 and vso2 <= 20 and vno2 <= 200 and vo3 <= 100 and vco <= 9:
            print("boa.")
        elif vmp10 <= 120 and vmp25 <= 60 and vso2 <= 60 and vno2 <= 240 and vo3 <= 140 and vco <= 11:
            print("moderada.\n"
                "Pessoas de grupos sensíveis (crianças, idosos e pessoas com doenças respiratórias e cardíacas)"
                "podem apresentar sintomas como tosse seca e cansaço. \nA população, em geral, não é afetada.")
        elif vmp10 <= 150 and vmp25 <= 125 and vso2 <= 365 and vno2 <= 320 and vo3 <= 160 and vco <= 13:
            print("ruim.\n"
                "Toda a população pode apresentar sintomas como tosse seca, cansaço, ardor nos olhos, nariz e garganta."
                "\nPessoas de grupos sensíveis (crianças, idosos e pessoas com doenças respiratórias e cardíacas)"
                "podem apresentar efeitos mais sérios na saúde.")
        elif vmp10 <= 250 and vmp25 <= 210 and vso2 <= 800 and vno2 <= 1130 and vo3 <= 200 and vco <= 15:
            print("muito ruim.\n"
                "Toda a população pode apresentar agravamento dos sintomas como tosse seca, cansaço, ardor nos olhos,"
                "nariz e garganta e ainda falta de ar e respiração ofegante. \nEfeitos ainda mais graves à saúde de grupos sensíveis"
                "(crianças, idosos e pessoas com doenças respiratórias e cardíacas).")
        else:
            print("péssima.\n"
                "Toda a população pode apresentar sérios riscos de manifestações de doenças respiratórias, cardiovasculares e \n"
                "aumento de mortes prematuras em pessoas de grupos sensíveis.")
        print("\n")
        
        # Função para voltar ao menu apertando qualquer tecla
        while True:
            try:
                sair = int(msvcrt.getch())       
                break
            except: 
                break
    
    # Função para sair do sistema
    if escolha == 0:
        system("CLS")
        break

    # Confirma que todas mensagens sejam apagadas para mostar o menu novamente
    sleep(1)
    system("CLS")

    # Faz commit em todas transições de dados para o database
    connection.commit()

# Fecha a conexão
connection.close()