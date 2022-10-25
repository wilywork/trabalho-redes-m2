import socket, threading

socket_instance = ''
SERVER_PORT = 12000
CONEXOES = []

def main() -> None:
    coletarDados()
    startServer()

# Coleta os dados para iniciar o servidor
def coletarDados() -> None:
    try:
        SERVER_PORT = int(input('Insira a porta do servidor, exemplo(12000): '))
        if SERVER_PORT >= 1 & SERVER_PORT <= 65535:
            print(f'Ligando servidor na porta: {str(SERVER_PORT)}')
        else:
            raise Exception('Informe um número de 1-65535')
    except Exception as e:
        print(f'Porta inválida, {e}')

def handleUserConnection(connection: socket.socket, address: str) -> None:
    while True:
        try:
            msg = connection.recv(1024)
            if msg:
                broadcast(msg, connection)
            else:
                remove_connection(connection)
                break

        except Exception as e:
            print(f'Error to handle user connection: {e}')
            remove_connection(connection)
            break

# Transmitir mensagem para todos os usuários conectados ao servidor
def broadcast(message: str, connection: socket.socket) -> None:
    for cliente in CONEXOES:
        if cliente != connection:
            try:
                cliente.send(message)
            except Exception as e:
                print('Erro ao transmitir mensagem: {e}')
                remove_connection(cliente)

# Remova a conexão especificada da lista de conexões
def remove_connection(conn: socket.socket) -> None:
    if conn in CONEXOES:
        conn.close()
        CONEXOES.remove(conn)

# Processo principal que recebe as conexões do cliente e inicia uma nova thread para lidar com suas mensagens
def startServer() -> None:
    try:
        # Cria o servidor
        socket_instance = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_instance.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        socket_instance.bind(('', SERVER_PORT))
        socket_instance.listen(4)

        print('Servidor iniciado!')

        try:
            while True:
                # Aceitar conexão do cliente
                socket_connection, address = socket_instance.accept()
                # Adiciona na lista
                CONEXOES.append(socket_connection)
                # Iniciar um novo thread para lidar com a conexão do cliente e receber suas mensagens
                threading.Thread(target=handleUserConnection, args=[socket_connection, address]).start()
        except Exception as e:
            print(f'Ocorreu um erro ao instanciar o socket: {e}')
        
    except Exception as e:
        print(f'Erro ao inicializar servidor: {e}')


main()
