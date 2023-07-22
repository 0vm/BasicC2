# control_server.py

import socket
import threading

# Replace this with a secure shared secret key (passphrase) for encryption/decryption
SECRET_KEY = b'your_shared_secret_key'

def xor_encrypt_decrypt(data):
    # Perform XOR encryption/decryption with the shared secret key
    return bytes([data[i] ^ SECRET_KEY[i % len(SECRET_KEY)] for i in range(len(data))])

def send_command_to_all(command):
    encrypted_command = xor_encrypt_decrypt(command.encode())
    for target_socket in target_sockets.values():
        try:
            target_socket.send(encrypted_command)
        except Exception as e:
            print(f"Error sending command to target server: {e}")



def handle_target_connection(target_socket, address):
    # Perform any authentication or security checks here


    # Add the target socket to the list of connected target servers
    target_sockets[address] = target_socket

    print(f"New target server connected: {address}")

    while True:
        data = target_socket.recv(1024)
        if not data:
            # Target server disconnected
            del target_sockets[address]
            print(f"Target server disconnected: {address}")
            break
        else:
            # Process data received from the target server (if needed)
            print(f"Received from {address}: {data.decode()}")

def user_input():
    # Get user input and send commands to target servers
    while True:
        command = input("Enter command to send to all devices: ")
        send_command_to_all(command)

if __name__ == '__main__':
    target_sockets = {}

    control_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    control_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    host = '0.0.0.0'
    port = 5000

    control_socket.bind((host, port))
    control_socket.listen(5)

    print("Control Server is listening for connections...")

    # Start a separate thread to handle user input
    threading.Thread(target=user_input, daemon=True).start()

    try:
        while True:
            target_socket, target_address = control_socket.accept()
            threading.Thread(target=handle_target_connection, args=(target_socket, target_address), daemon=True).start()

    except KeyboardInterrupt:
        print("Control Server shutting down...")
        control_socket.close()
