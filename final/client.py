import socket, threading
from datetime import datetime
from cryptography.fernet import Fernet

KEY_CRYPTO = 'TyLTOB9m2EjFLEbyWZK1pr7zU1ZmSN25gFIpXb2LjnY='
FERNET = Fernet(KEY_CRYPTO)

# Inicializa o Chat
def main():
    try:
        dados = coletarDados()
        socket_instance = connection(dados[0], dados[1])
        terminalInterativoDoChat(socket_instance)
    except Exception as e:
        print(f'Error {e}')

# Coleta os dados de acesso e nick do usuário
def coletarDados():
    try:
        SERVER_ADDRESS = input('Insira o endereço do servidor, exemplo(127.0.0.1): ')
        SERVER_PORT = int(input('Insira a porta do servidor, exemplo(12000): '))
    except Exception as e:
        print(f'Dados informados inválidos: {e}')
    return [SERVER_ADDRESS, SERVER_PORT]

# Finaliza a conexão com o servidor
def quitChat(socket_instance) -> None:
    socket_instance.close()

# Inicia a conexão com o servidor
def connection(SERVER_ADDRESS, SERVER_PORT):
    try:
        # Instanciar socket
        socket_instance = socket.socket()
        print('Conectando ao servidor: ' + SERVER_ADDRESS + ':' + str(SERVER_PORT))
        # Iniciar conexão com servidor
        socket_instance.connect((SERVER_ADDRESS, SERVER_PORT))
        # Crie um thread(processo) para lidar com mensagens enviadas pelo servidor
        threading.Thread(target=handleMessages, args=[socket_instance]).start()
        print('Conectado.')
        print('Digite a mensagem e de enter para enviar\n')
    except Exception as e:
        print(f'Erro ao conectar ao servidor {e}')
        socket_instance.close()

    return socket_instance

# Mantem o terminal ativo e interativo para envio de novas mensagens
def terminalInterativoDoChat(socket_instance) -> None:
    try:
        # Matem o terminal ativo
        while True:
            msg = input()
            # Caso o cliente escreva quit e de enter o client fecha.
            if msg == 'quit':
                quitChat(socket_instance)
                break
            # Converte para utf-8
            socket_instance.send(do_encrypt(msg.encode()))

    except Exception as e:
        print(f'Erro ao enviar mensagem {e}')

#Receber mensagens enviadas pelo servidor e exibi ao usuário
def handleMessages(connection: socket.socket):
    while True:
        try: 
            msg = connection.recv(1024)
            # Caso exista uma mensagem ela será processada, caso contrário será finalizada
            if msg:
                # Exibe a mensagem no terminal com hora e minuto
                print(f'\nMensagem recebida de {connection.getsockname()} - {datetime.now().strftime("%H:%M")} > {do_decrypt(msg).decode()}')
            else:
                connection.close()
                break
        except Exception as e:
            print(f'Erro ao tratar mensagem do servidor: {e}')
            connection.close()
            break

# Descryptografa a mensagem
def do_decrypt(message):
    # return message
    return FERNET.decrypt(message)

# Criptografa a mensagem
def do_encrypt(message):
    # return message
    return FERNET.encrypt(message)

main()
