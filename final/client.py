import socket, threading
from datetime import datetime
from cryptography.fernet import Fernet

KEY_CRYPTO = '2#$C@#%V@VTGEGW$W$#¨B$%N&YSE%B&awaDQwfqwr&$%'
SERVER_ADDRESS = '127.0.0.1'
SERVER_PORT = 12000
NICK_NAME = 'Fulano'
FERNET = Fernet(KEY_CRYPTO)

# Inicializa o Chat
def main():
    try:
        coletarDados()
        connection()
        terminalInterativoDoChat()
    except Exception as e:
        print(f'Error {e}')

# Coleta os dados de acesso e nick do usuário
def coletarDados() -> None:
    try:
        SERVER_ADDRESS = input('Insira o endereço do servidor, exemplo(127.0.0.1): ')
        SERVER_PORT = int(input('Insira a porta do servidor, exemplo(12000): '))
        NICK_NAME = input('Insira seu nick: ')
        print('Aguarde um estante ' + NICK_NAME)
        print('Conectando ao servidor: ' + SERVER_ADDRESS + ':' + str(SERVER_PORT))
    except Exception as e:
        print(f'Dados informados inválidos: {e}')

# Finaliza a conexão com o servidor
def quitChat() -> None:
    socket_instance.close()

# Inicia a conexão com o servidor
def connection() -> None:
    try:
        # Instanciar socket
        socket_instance = socket.socket()
        # Iniciar conexão com servidor
        socket_instance.connect((SERVER_ADDRESS, SERVER_PORT))
        # Crie um thread(processo) para lidar com mensagens enviadas pelo servidor
        threading.Thread(target=handleMessages, args=[socket_instance]).start()
        socket_instance.send(NICK_NAME.encode())
        print('Conectado.')
    except Exception as e:
        print(f'Erro ao conectar ao servidor {e}')
        socket_instance.close()

# Mantem o terminal ativo e interativo para envio de novas mensagens
def terminalInterativoDoChat() -> None:
    try:
        # Matem o terminal ativo
        while True:
            msg = input('Digite sua mensagem: ')
            # Caso o cliente escreva quit e de enter o client fecha.
            if msg == 'quit':
                quitChat()
                break
            # Converte para utf-8
            socket_instance.send(do_encrypt(msg).encode())

    except Exception as e:
        print(f'Erro ao enviar mensagem {e}')

#Receber mensagens enviadas pelo servidor e exibi ao usuário
def handleMessages(connection: socket.socket, address: str):
    while True:
        try: 
            msg = connection.recv(1024)
            # Caso exista uma mensagem ela será processada, caso contrário será finalizada
            if msg:
                # Exibe a mensagem no terminal com hora e minuto
                print(f'{datetime.now().strftime("%H:%M")} {address[0]}:{address[1]} > {do_decrypt(msg).decode()}')
            else:
                connection.close()
                break
        except Exception as e:
            print(f'Erro ao tratar mensagem do servidor: {e}')
            connection.close()
            break

# Descryptografa a mensagem
def do_decrypt(message):
    return FERNET.decrypt(message)

# Criptografa a mensagem
def do_encrypt(message):
    return FERNET.encrypt(message)

main()
