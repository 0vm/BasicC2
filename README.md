# Command and Control (C2)

This is a simple command and control (cnc) that allows a control server to send commands to multiple target servers (slaves) simultaneously. The target servers will execute the received commands and send back the result to the control server.

At 75 stars I will make a UDP Version that is undetected on GCP, Azure, AWS, etc

## Features

- The control server listens for incoming connections from target servers.
- Target servers connect to the control server and wait for commands to execute.
- The control server can send commands to all connected target servers.
- Each command is executed on a separate thread, ensuring concurrent execution.
- Target servers automatically reconnect to the control server if the connection is lost.
- Basic error handling for improved stability.

## Getting Started

1. Clone the repository.
   ```bash
   git clone https://github.com/0vm/BasicC2.git
   cd BasicC2
   ```

2. Set up the control server:
   - Open `control_server.py` and replace `your_secret_key` with a secure secret key for authentication (line 7).
   - Open `control_server.py` and replace `host & port` with your desired host and port (line 55 & 56).
   - Run the control server:
   ```ruby
   python control_server.py
   ```

3. Set up the target server(s):
   - Open `target_server.py` and replace `'your_control_server_ip'` with the actual IP address or hostname of the control server (line 13).
   - Open `target_server.py` and replace `control_server_port` with the port from the control server (line 14).
   - Run the target server(s):
   ```ruby
   python target_server.py
   ```

4. Use the application:
   - Type commands in the control server's command line to send them to all connected target servers.
   - Target servers will execute the commands and print the results.

## Security Considerations

- This is a basic implementation for educational purposes and should not be used in a production environment without proper security enhancements.
- Implement robust authentication and authorisation mechanisms to prevent unauthorised access.
- Restrict the commands that can be executed by the target servers to avoid potential security risks.
- Ensure input validation and sanitization to avoid command injection vulnerabilities.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

This project is for educational purposes only and should not be used for any malicious activities. Use it responsibly and ethically. But who's going to stop you if you don't?
