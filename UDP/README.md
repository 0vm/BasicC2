# UDP Version

## Overview
This is the **UDP-based** version, which uses UDP for communication instead of TCP. It is lightweight, simple and does not require persistent connections.

## Key Differences from TCP Version
- **No persistent connection** – UDP sends data without maintaining a session.
- **Unreliable** – No guarantee that commands will be received.
- **Stealthier** – Harder to detect since it doesn’t keep open connections.
- **IP Handling** – Targets must periodically resolve the control server's IP if using DDNS.

## Usage
### Start the Control Server
```bash
python server.py
```

### Deploy the Target Bot
1. Change the `control_server_host` value in `target_server.py` to your host.
2. Change the XOR `SECRET_KEY` value in `target_server.py` and `control_server.py`.
3. Start the server:
```bash
python control_server.py
```
4. Start the clients:
```bash
python target_server.py
```

## Notes
- UDP does not guarantee message delivery.
- Ensure the correct UDP ports are open.
- Encryption uses XOR – update the secret key in all scripts.
