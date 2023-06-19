import socket

# Função para enviar requisição ao servidor e receber a resposta
def enviar_requisicao(requisicao, endereco_servidor):
    # Criação do socket
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # Conexão com o servidor
        cliente.connect(endereco_servidor)

        # Envia a requisição ao servidor
        cliente.send(requisicao.encode())

        # Recebe a resposta do servidor
        resposta = cliente.recv(1024).decode()

        # Fecha a conexão com o servidor
        cliente.close()

        return resposta
    except:
        return "Não foi possível conectar ao servidor."

# Solicita o endereço IP e a porta do servidor
endereco_ip = input("Digite o endereço IP do servidor: ")
porta = int(input("Digite o número da porta do servidor: "))

# Cria a tupla de endereço do servidor
endereco_servidor = (endereco_ip, porta)
while True:

    # Exibe o menu de opções
    print("=== MENU ===")
    print("1. Criar diretório")
    print("2. Remover diretório")
    print("3. Listar conteúdo de diretório")
    print("4. Enviar arquivo")
    print("5. Remover arquivo")
    print("0. Sair")



    # Solicita a opção ao usuário
    opcao = input("Selecione uma opção: ")

    if opcao == "1":
        diretorio = input("Informe o nome do diretório a ser criado: ")
        requisicao = f"criar_diretorio {diretorio}"
        resposta = enviar_requisicao(requisicao, endereco_servidor)
        print(resposta)
    elif opcao == "2":
        diretorio = input("Informe o nome do diretório a ser removido: ")
        requisicao = f"remover_diretorio {diretorio}"
        resposta = enviar_requisicao(requisicao, endereco_servidor)
        print(resposta)
    elif opcao == "3":
        diretorio = input("Informe o nome do diretório a ser listado: ")
        requisicao = f"listar_conteudo {diretorio}"
        resposta = enviar_requisicao(requisicao, endereco_servidor)
        print(resposta)
    elif opcao == "4":
        arquivo = input("Informe o caminho do arquivo a ser enviado: ")
        diretorio_destino = input("Informe o diretório de destino: ")
        requisicao = f"enviar_arquivo {arquivo} {diretorio_destino}"
        resposta = enviar_requisicao(requisicao, endereco_servidor)
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