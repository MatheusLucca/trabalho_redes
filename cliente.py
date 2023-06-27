# -*- coding: utf-8 -*-
import socket
import os

def enviar_requisicao(requisicao, endereco_servidor):
    # Criação do socket
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        cliente.connect(endereco_servidor)

        cliente.send(requisicao.encode())

        resposta = cliente.recv(1024).decode()

        cliente.close()

        return resposta
    except:
        return "Não foi possível conectar ao servidor."


def enviar_arquivo(nome_arquivo, caminho_arquivo, endereco_servidor):
    SEPARATOR = " "
    BUFFER_SIZE = 4096
    filesize = os.path.getsize(nome_arquivo)
    cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente_socket.connect(endereco_servidor)
    cliente_socket.send(f"enviar_arquivo{SEPARATOR}{nome_arquivo}{SEPARATOR}{filesize}{SEPARATOR}{caminho_arquivo} ".encode())
    f = open(nome_arquivo, "rb")
    while True:
        bytes_read = f.read(BUFFER_SIZE)
        cliente_socket.sendall(bytes_read)
        if not bytes_read:
            print('Envio finalizado!')
            break
endereco_ip = input("Digite o endereço IP do servidor: ")
porta = int(input("Digite o número da porta do servidor: "))


endereco_servidor = (endereco_ip, porta)
while True:

    print("=== MENU ===")
    print("1. Criar diretorio")
    print("2. Remover diretorio")
    print("3. Listar conteúdo de diretorio")
    print("4. Enviar arquivo")
    print("5. Remover arquivo")
    print("0. Sair")



    opcao = input("Selecione uma opcao: ")

    if opcao == "1":
        diretorio = input("Informe o nome do diretorio a ser criado: ")
        requisicao = f"criar_diretorio {diretorio}"
        resposta = enviar_requisicao(requisicao, endereco_servidor)
        print(resposta)
    elif opcao == "2":
        diretorio = input("Informe o nome do diretorio a ser removido: ")
        confirmacao = input(f"Tem certeza de que deseja remover o diretorio '{diretorio}' e todos os arquivos? (s/n): ")
        if confirmacao.lower() == 's':
            requisicao = f"remover_diretorio {diretorio}"
            resposta = enviar_requisicao(requisicao, endereco_servidor)
            print(resposta)
        else:
            print("Remoção cancelada.")
    elif opcao == "3":
        diretorio = input("Informe o nome do diretório a ser listado: ")
        requisicao = f"listar_conteudo {diretorio}"
        resposta = enviar_requisicao(requisicao, endereco_servidor)
        print(resposta)
    elif opcao == "4":
        nome_arquivo = input("Informe o nome do arquivo a ser enviado: ")
        caminho_arquivo = input("Informe o caminho onde o arquivo será salvo:")
        resposta = enviar_arquivo(nome_arquivo, caminho_arquivo, endereco_servidor)
        print(resposta)
    elif opcao == "5":
        arquivo = input("Informe o caminho do arquivo a ser removido: ")
        requisicao = f"remover_arquivo {arquivo}"
        resposta = enviar_requisicao(requisicao, endereco_servidor)
        print(resposta)
    elif opcao == "0":
        break
    else:
        print("Opção inválida. Por favor, tente novamente.")

print("Programa encerrado.")