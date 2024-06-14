import socket
ADDRESS= 'localhost'
PORT = 3333

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((ADDRESS, PORT))

try:
    while True:
        to_send = input("Message to send->")
        sock.send(to_send.encode())
except KeyboardInterrupt:
    print("Exitin app..")
except Exception as e:
    print(f"Something happened {e}")
finally:
    sock.close()