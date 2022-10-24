import socket, threading
from datetime import datetime
from datetime import datetime

CLIENT_ADDRESS = '192.168.0.116'
CLIENT_PORT = 4000
LISTENING_PORT = 5000

# Global variable that mantain client's connections
connections = ['192.168.0.116']

def handle_user_connection(connection: socket.socket, address: str) -> None:
    '''
        Get user connection in order to keep receiving their messages and
        sent to others users/connections.
    '''
    while True:
        try:
            # Get client message
            username = connection.recv(1024)
            msg = connection.recv(1024)
        
            # If no message is received, there is a chance that connection has ended
            # so in this case, we need to close connection and remove it from connections list.
            if msg:
                #horário mensagem
                horarioMSG = datetime.now()

                # Log message sent by user
                print(f'{address[0]}:{address[1]} - {username} - {msg.decode()} - {horarioMSG.strftime("%H:%M")}')
                
                # Build message format and broadcast to users connected on server
                msg_to_send = f'From {address[0]}:{address[1]} - {msg.decode()}'
                broadcast(msg_to_send, connection)

            # Close connection if no message was sent
            else:
                remove_connection(connection)
                break

        except Exception as e:
            print(f'Error to handle user connection: {e}')
            remove_connection(connection)
            break

def handle_messages(connection: socket.socket):
    '''
        Receive messages sent by the server and display them to user
    '''

    while True:
        try: 
            msg = connection.recv(1024)
            print(msg.decode())
        except Exception as e:
            print(f'Error handling message from server: {e}')
            connection.close()
            break

def client() -> None:
    '''
        Main process that start client connection to the server 
        and handle it's input messages
    '''

    try:
        # Instantiate socket and start connection with other client
        socket_instance = socket.socket()
        socket_instance.connect((CLIENT_ADDRESS, CLIENT_PORT))
        # Create a thread in order to handle messages sent by other client
        threading.Thread(target=handle_messages, args=[socket_instance]).start()

        print('Connected to chat!')

        # Read user's input until it quit from chat and close connection
        while True:
            print('Insira seu nome de usuário:')
            username = input()
            print(username + ' conectado!')
            print('Digite sua mensagem: ')
            msg = input()

            if msg == 'quit':
                break

            if username != '' :
                # Parse message to utf-8
                socket_instance.send(username.encode())
                socket_instance.send(msg.encode())

        # Close connection with the server
        # socket_instance.close()

    except Exception as e:
        print(f'Error connecting to server socket {e}')
        socket_instance.close()

def server() -> None:
    '''
        Main process that receive client's connections and start a new thread
        to handle their messages
    '''
    try:
        # Create server and specifying that it can only handle 4 connections by time!
        socket_instance = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        socket_instance.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        socket_instance.bind(('', LISTENING_PORT))
        socket_instance.listen(4)

        print('Chat running!')
        
        while True:

            # Accept client connection
            socket_connection, address = socket_instance.accept()
            # Add client connection to connections list
            connections.append(socket_connection)
            # Start a new thread to handle client connection and receive it's messages
            # in order to send to others connections
            threading.Thread(target=handle_user_connection, args=[socket_connection, address]).start()

    except Exception as e:
        print(f'An error has occurred when instancing socket: {e}')
    finally:
        # In case of any problem we clean all connections and close the server connection
        if len(connections) > 0:
            for conn in connections:
                remove_connection(conn)

        socket_instance.close()

if __name__ == "__main__":
    server()
    client()