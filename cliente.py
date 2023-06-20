import socket

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


def enviar_arquivo(nome_arquivo, endereco_servidor, porta):
    try:
        with open(nome_arquivo, 'rb') as arquivo:
            # Cria o socket e se conecta ao servidor
            cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            cliente_socket.connect((endereco_servidor, porta))
            
            # Envia o nome do arquivo para o servidor
            cliente_socket.sendall(nome_arquivo.encode())

            # Envia o conteúdo do arquivo em chunks
            for dados in arquivo:
                cliente_socket.sendall(dados)

            # Finaliza a conexão
            cliente_socket.close()
            
            return f"Arquivo '{nome_arquivo}' enviado com sucesso."
    except Exception as e:
        return f"Erro ao enviar arquivo: {str(e)}"



endereco_ip = input("Digite o endereço IP do servidor: ")
porta = int(input("Digite o número da porta do servidor: "))


endereco_servidor = (endereco_ip, porta)
while True:

    print("=== MENU ===")
    print("1. Criar diretório")
    print("2. Remover diretório")
    print("3. Listar conteúdo de diretório")
    print("4. Enviar arquivo")
    print("5. Remover arquivo")
    print("0. Sair")



    opcao = input("Selecione uma opção: ")

    if opcao == "1":
        diretorio = input("Informe o nome do diretório a ser criado: ")
        requisicao = f"criar_diretorio {diretorio}"
        resposta = enviar_requisicao(requisicao, endereco_servidor)
        print(resposta)
    elif opcao == "2":
        diretorio = input("Informe o nome do diretório a ser removido: ")
        confirmacao = input(f"Tem certeza de que deseja remover o diretório '{diretorio}' e todos os arquivos? (s/n): ")
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
        resposta = enviar_arquivo(nome_arquivo, endereco_servidor, int(porta))
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