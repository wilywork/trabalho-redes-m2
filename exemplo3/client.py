from Crypto.Cipher import AES
import socket, threading

SERVER_ADDRESS = '127.0.0.1'
SERVER_PORT = 12000
KEY_MASTER = 'y/B?E(H+MbQeShVmYq3t6w9z$C&F)J@N'.encode('utf-8')
KEY_IV = '\xc6o\x00t\xc7u5\x14\xf3R\xe2C\xf3U\xc1\xd0'

def do_decrypt(ciphertext):
    obj2 = AES.new(KEY_MASTER, AES.MODE_CBC,IV=KEY_MASTER)
    message = obj2.decrypt(ciphertext)
    return message

def do_encrypt(message):
    obj = AES.new(KEY_MASTER, AES.MODE_CBC, KEY_IV)
    ciphertext = obj.encrypt(message)
    return ciphertext

def handle_messages(connection: socket.socket):
    '''
        Receive messages sent by the server and display them to user
    '''

    while True:
        try:
            msg = connection.recv(1024)

            # If there is no message, there is a chance that connection has closed
            # so the connection will be closed and an error will be displayed.
            # If not, it will try to decode message in order to show to user.
            if msg:
                print(msg.decode())
            else:
                connection.close()
                break

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
        # Instantiate socket and start connection with server
        socket_instance = socket.socket()
        socket_instance.connect((SERVER_ADDRESS, SERVER_PORT))
        # Create a thread in order to handle messages sent by server
        threading.Thread(target=handle_messages, args=[socket_instance]).start()

        print('Connected to chat!')

        # Read user's input until it quit from chat and close connection
        while True:
            msg = input()

            if msg == 'quit':
                break

            # Parse message to utf-8
            socket_instance.send(do_encrypt(msg.encode()))

        # Close connection with the server
        socket_instance.close()

    except Exception as e:
        print(f'Error connecting to server socket {e}')
        socket_instance.close()


if __name__ == "__main__":
    client()