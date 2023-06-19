import socket
import os

# Função para criar diretório
def criar_diretorio(diretorio):
    if not os.path.exists(diretorio):
        os.makedirs(diretorio)
        return "Diretório criado com sucesso."
    else:
        return "O diretório já existe."

# Função para remover diretório
def remover_diretorio(diretorio):
    if os.path.exists(diretorio):
        os.rmdir(diretorio)
        return "Diretório removido com sucesso."
    else:
        return "O diretório não existe."

# Função para listar conteúdo de diretório
def listar_conteudo(diretorio):
    if os.path.exists(diretorio):
        conteudo = os.listdir(diretorio)
        return "\n".join(conteudo)
    else:
        return "O diretório não existe."

# Função para enviar arquivo
def enviar_arquivo(arquivo, diretorio_destino):
    if os.path.exists(arquivo):
        with open(arquivo, "rb") as file:
            conteudo = file.read()

        caminho_destino = os.path.join(diretorio_destino, os.path.basename(arquivo))
        with open(caminho_destino, "wb") as file_destino:
            file_destino.write(conteudo)
        return "Arquivo enviado com sucesso."
    else:
        return "O arquivo não existe."

# Função para remover arquivo
def remover_arquivo(arquivo):
    if os.path.exists(arquivo):
        os.remove(arquivo)
        return "Arquivo removido com sucesso."
    else:
        return "O arquivo não existe."

# Configurações do servidor
HOST = '127.0.0.1'  # Endereço IP do servidor
PORT = 12345  # Porta de conexão

# Criação do socket
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Vincula o socket com o endereço e porta
servidor.bind((HOST, PORT))

# Aguarda uma conexão
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
        elif comando == "enviar_arquivo":
            resposta = enviar_arquivo(partes[1], partes[2])
        elif comando == "remover_arquivo":
            resposta = remover_arquivo(partes[1])
        else:
            resposta = "Comando inválido."

        # Envia a resposta ao cliente
        cliente.send(resposta.encode())

    # Fecha a conexão com o cliente
    cliente.close()
