from Crypto.Cipher import AES
import socket, threading

LISTENING_PORT = 12000
KEY_MASTER = 'y/B?E(H+MbQeShVmYq3t6w9z$C&F)J@N'.encode('utf-8')
KEY_IV = '\xc6o\x00t\xc7u5\x14\xf3R\xe2C\xf3U\xc1\xd0'
# Global variable that mantain client's connections
connections = []

def do_decrypt(ciphertext):
    obj2 = AES.new(KEY_MASTER, AES.MODE_CBC,IV=KEY_MASTER)
    message = obj2.decrypt(ciphertext)
    return message

def handle_user_connection(connection: socket.socket, address: str) -> None:
    '''
        Get user connection in order to keep receiving their messages and
        sent to others users/connections.
    '''
    while True:
        try:
            # Get client message
            msg = connection.recv(1024)

            # If no message is received, there is a chance that connection has ended
            # so in this case, we need to close connection and remove it from connections list.
            if msg:
                # Log message sent by user
                print(f'{address[0]}:{address[1]} - {do_decrypt(msg.decode())}')
                
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


def broadcast(message: str, connection: socket.socket) -> None:
    '''
        Broadcast message to all users connected to the server
    '''

    # Iterate on connections in order to send message to all client's connected
    for client_conn in connections:
        # Check if isn't the connection of who's send
        if client_conn != connection:
            try:
                # Sending message to client connection
                client_conn.send(message.encode())

            # if it fails, there is a chance of socket has died
            except Exception as e:
                print('Error broadcasting message: {e}')
                remove_connection(client_conn)


def remove_connection(conn: socket.socket) -> None:
    '''
        Remove specified connection from connections list
    '''

    # Check if connection exists on connections list
    if conn in connections:
        # Close socket connection and remove connection from connections list
        conn.close()
        connections.remove(conn)


def server() -> None:
    '''
        Main process that receive client's connections and start a new thread
        to handle their messages
    '''
    try:
        # Create server and specifying that it can only handle 4 connections by time!
        socket_instance = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


        socket_instance.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        # if platform.system() == "Darwin":
        #     socket_instance.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        # socket_instance.bind(("", LISTENING_PORT))
        # socket_instance.settimeout(0)
        # socket_instance.setblocking(0)


        # self._read_notifier = QSocketNotifier(
        #     self._socket.fileno(), QSocketNotifier.Read, self
        # )
        # self._read_notifier.activated.connect(self._notify_read)
        # self._read_notifier.setEnabled(True)
        # self._started = True 


        socket_instance.bind(('', LISTENING_PORT))
        socket_instance.listen(4)

        print('Server running!')
        
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