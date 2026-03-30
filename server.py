import socket
import threading
from datetime import datetime
import database

HOST = "127.0.0.1"
PORT = 5000


def init_server():
  try:
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind((HOST, PORT))
    server_sock.listen()
    print(f"Server started on {HOST}:{PORT}")
    return server_sock
  except socket.error as e:
    print(f"Socket configuration error: {e}")
    server_sock.close()
    return None
 

# Atiende a un cliente específico, recibiendo mensajes y respondiendo con la hora de llegada
def handle_client(client_sock):
  ip, port = client_sock.getpeername()
  print(f"(+) Nuevo cliente conectado desde {ip}:{port}")
  with client_sock:
    while True:
      try:
        data = client_sock.recv(1024)
        if not data:
          print(f"(-) Cliente desde {ip}:{port} desconectado.")
          break
        message = data.decode('utf-8').strip()
        if message.lower() in ("éxito", "exito"):
          print(f"Cliente desde {ip}:{port} ha terminado la comunicación.")
          break
        ts = database.save_message(message, ip)
        if ts:
          respuesta = f"(✔) Mensaje recibido: {ts}\n"
        else:
          ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
          respuesta = f"(✘) Mensaje recibido: {ts} pero no se pudo guardar el mensaje en la base de datos.\n"
        client_sock.sendall(respuesta.encode('utf-8'))
      except ConnectionResetError:
        print(f"(!) Conexión perdida con el cliente {ip}:{port}")
        break
      except Exception as e:
        print(f"(!) Error al manejar el cliente {ip}:{port}: {e}")
        break
  print(f"[x] Conexión finalizada con el cliente {ip}:{port}")


# Aceptar clientes y genera un hilo para cada uno
def accept_clients(server_sock):
  try:
    while True:
      client_sock, addr = server_sock.accept()
      threading.Thread(target=handle_client, args=(client_sock,)).start()
  except KeyboardInterrupt:
    print("(!) Servidor detenido por el usuario.")
  except Exception as e:
    print(f"(!) Error al aceptar clientes: {e}")
  finally:
    server_sock.close()


if __name__ == "__main__":
  database.init_db()
  server_sock = init_server()
  if(server_sock):
    accept_clients(server_sock)