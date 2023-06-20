import socket
import os
import shutil

def criar_diretorio(diretorio):
    if not os.path.exists(diretorio):
        os.makedirs(diretorio)
        return "Diretório criado com sucesso."
    return "O diretório já existe."

def remover_diretorio(diretorio):
    try:
        shutil.rmtree(diretorio)
        return f"Diretório '{diretorio}' removido com sucesso."
    except OSError as e:
        return f"Erro ao remover diretório '{diretorio}': {str(e)}"

def listar_conteudo(diretorio):
    if os.path.exists(diretorio):
        conteudo = os.listdir(diretorio)
        return "\n".join(conteudo)
    else:
        return "O diretório não existe."


def receber_arquivo(cliente_socket):
    try:
        # Recebe o nome do arquivo do cliente
        nome_arquivo = cliente_socket.recv(1024).decode()
        
        # Abre o arquivo em modo de escrita binária
        with open(nome_arquivo, 'wb') as arquivo:
            # Recebe os chunks do arquivo e escreve no arquivo local
            while True:
                dados = cliente_socket.recv(1024)
                if not dados:
                    break
                arquivo.write(dados)
        
        return f"Arquivo '{nome_arquivo}' recebido com sucesso."
    except Exception as e:
        return f"Erro ao receber arquivo: {str(e)}"

def remover_arquivo(arquivo):
    if os.path.exists(arquivo):
        os.remove(arquivo)
        return "Arquivo removido com sucesso."
    else:
        return "O arquivo não existe."


HOST = '10.6.80.122'  
PORT = 3007

# Criação do socket
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Seta o socket para reutilizar o endereço
servidor.bind((HOST, PORT))

servidor.listen()

print("Servidor aguardando conexões...")

while True:
    # Aceita uma nova conexão
    cliente, endereco = servidor.accept()
    print("Conexão estabelecida com", endereco)

    # Recebe a requisição do cliente
    requisicao = cliente.recv(1024).decode()

    # Separa a requisição em partes
    partes = requisicao.split()

    if len(partes) > 0:
        comando = partes[0]

        if comando == "criar_diretorio":
            resposta = criar_diretorio(partes[1])
        elif comando == "remover_diretorio":
            resposta = remover_diretorio(partes[1])
        elif comando == "listar_conteudo":
            resposta = listar_conteudo(partes[1])
        if requisicao.startswith("enviar_arquivo"):
            resposta = receber_arquivo(cliente)
            cliente.sendall(resposta.encode())
        elif comando == "remover_arquivo":
            resposta = remover_arquivo(partes[1])
        else:
            resposta = "Comando inválido."

        # Envia a resposta ao cliente
        cliente.send(resposta.encode())

    # Fecha a conexão 
    cliente.close()
