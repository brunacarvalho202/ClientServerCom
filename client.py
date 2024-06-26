import random
import socket
import hashlib
import time
from classMsgAdd import classMsgAdd
from classMsgGet import classMsgGet

#Método de Envio de Requisição:
#1. método de pegar - get
def enviarMsg_pegar_telefone(socket, nome):
    #montar uma msg dessa requisição com o nome fornecido no método
    objetoMensagem = classMsgGet("Get", nome)
    #serializar antes de enviar
    msgSerializada = objetoMensagem.to_json()
    
    return msgSerializada


#1. método de adicionar - Add
def enviarMsg_add_telefone(nome, telefone):
    objetoMensagemAdd = classMsgAdd("Add", nome, telefone)
    msgAddSerializada = objetoMensagemAdd.to_json()

    return msgAddSerializada
    #enviar_dados_com_checksum(socket, msgAddSerializada)

# Definir o tempo limite do temporizador (em segundos)
TIMEOUT = 60

# Número de sequência inicial
sequence_number = 0

# Tamanho da janela 
WINDOW_SIZE = 5
     
def calcular_checksum(dados):
    # Calcular o hash MD5 dos dados
    hash_md5 = hashlib.md5()
    hash_md5.update(dados)
    return hash_md5.digest()

def enviar_dados_com_checksum(socket, dados):
    global sequence_number

    # Calcular o checksum dos dados
    checksum = calcular_checksum(dados)

    # Adicionar o número de sequência e checksum aos dados
    dados = str(sequence_number).encode() + b":" + checksum + b":" + dados
    sequence_number += 1
    
    # Enviar dados
    socket.sendall(dados)

def receber_dados_com_checksum(socket):
    # Receber dados
    dados = socket.recv(1024)  # Tamanho máximo dos dados, ajuste conforme necessário

    # Separar número de sequência e checksum dos dados
    partes = dados.split(b":", 2)
    numero_sequencia = int(partes[0])
    checksum_recebido = partes[1]
    dados_reais = partes[2]

    # Calcular o checksum dos dados recebidos
    checksum_calculado = calcular_checksum(dados_reais)

    # Verificar se os checksums coincidem
    if checksum_recebido == checksum_calculado:
        return dados_reais
    else:
        raise Exception("Erro de integridade: checksums não coincidem")

# Função para enviar dados confiavelmente (com soma de verificação)
def enviar_dados_confiavelmente(socket, dados):
    try:
        inicio_temporizador = time.time()
        while True:
            #chamar metodo da msg serialiada aqui e englobar o enviar dados com checksum dentro dele
            enviar_dados_com_checksum(socket, dados)
            # print("Dados enviados com sucesso")
            
            # Esperar pela resposta
            socket.settimeout(TIMEOUT)
            resposta = socket.recv(1024)
            if resposta:
                print("Resposta do servidor:", resposta.decode())
                break  # Saia do loop se receber uma resposta
            if time.time() - inicio_temporizador > TIMEOUT:
                raise Exception("Tempo limite excedido ao aguardar resposta do servidor")

    #except socket.timeout:
     #   print("Tempo limite atingido ao aguardar resposta do servidor")
    #except Exception as e:
     #   print(f"Erro ao enviar dados: {e}")
    except Exception as e:
        if type(e) == socket.timeout:
           print("Tempo limite atingido ao aguardar resposta do servidor")
        else:
           print(f"Erro ao enviar dados: {e}")

# Função para receber dados confiavelmente (com soma de verificação)
def receber_dados_confiavelmente(socket):
    try:
        inicio_temporizador = time.time()
        
        dados = socket.recv(1024)
        # print("Dados recebidos com sucesso")
        return dados
            
    #except socket.timeout:
     #   print("Tempo limite atingido ao aguardar dados do cliente")
    #except Exception as e:
     #   print(f"Erro ao receber dados: {e}")
    except Exception as e:
        if type(e) == socket.timeout:
           print("Tempo limite atingido ao aguardar resposta do servidor")
        else:
           print(f"Erro ao enviar dados: {e}")

        print(f"Erro ao enviar dados: {e}")
    # finally:
    #     # Fechar o socket
    #     socket.close()

# Exibir o menu de opções
def menu():
    print("1. Adicionar contato")
    print("2. Simular erro de integridade")
    print("3. Enviar vários pacotes ao mesmo tempo")
    print("4. Sair")
    
    opcao = input("Escolha uma opção: ")
    return opcao

def simulate_integrity_error(socket, dados):
    # Simular um erro de integridade
    dados_corrompidos = b"0:" + b"0" * len(dados) + b":" + dados
    socket.sendall(dados_corrompidos)
    

    

    
    
    