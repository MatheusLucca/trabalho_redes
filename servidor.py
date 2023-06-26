# -*- coding: utf-8 -*-
import socket
import os
import shutil



BUFFER_SIZE = 4096
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


def receber_arquivo(cliente_socket, partes):
    try:

        mensagem = partes
        pathArq = mensagem[1]
        filesize = mensagem[2]
        pathDest= mensagem[3]
        filename = os.path.basename(pathArq)
        filesize = int(filesize)
        if not pathDest:
            pathDest = filename
        else:
            pathDest = pathDest +'\\'+ filename
        f = open(pathDest, "wb")
        progress=0
        pack = 0

        while True:
            bytes_read = cliente_socket.recv(BUFFER_SIZE)
            pack = pack + 1
        
            if len(bytes_read) < BUFFER_SIZE:
                f.write(bytes_read)
                progress = progress + len(bytes_read)
                break
            
            progress = progress + len(bytes_read)
            f.write(bytes_read)
        return "Arquivo enviado!"
    except Exception:
        return "Houve um erro!"


def remover_arquivo(arquivo):
    if os.path.exists(arquivo):
        os.remove(arquivo)
        return "Arquivo removido com sucesso."
    else:
        return "O arquivo não existe."


HOST = '127.0.0.1'  
PORT = 3005

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
    
    requisicao = cliente.recv(BUFFER_SIZE).decode(errors='ignore')

    partes = requisicao.split(' ')

    if len(partes) > 0:
        comando = partes[0]
        print("Comando recebido:", comando)
        if comando == "criar_diretorio":
            resposta = criar_diretorio(partes[1])
        elif comando == "remover_diretorio":
            resposta = remover_diretorio(partes[1])
        elif comando == "listar_conteudo":
            resposta = listar_conteudo(partes[1])
        elif requisicao.startswith("enviar_arquivo"):
            print('aa')
            resposta = receber_arquivo(cliente, partes)
            print(resposta)
        elif comando == "remover_arquivo":
            resposta = remover_arquivo(partes[1])
        else:
            resposta = "Comando inválido."

        # Envia a resposta ao cliente
        cliente.send(resposta.encode())

    # Fecha a conexão 
    cliente.close()
