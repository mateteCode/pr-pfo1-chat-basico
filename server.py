import socket
import threading
from datetime import datetime
import database
import errno

HOST = "127.0.0.1"
PORT = 5000


# Inicializa el servidor, creando el socket, vinculándolo al puerto y comenzando a escuchar conexiones
def init_server():
  try:
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind((HOST, PORT))
    server_sock.listen()
    print(f"Servidor corriendo y escuchando en {HOST}:{PORT}")
    return server_sock
  except OSError as e:
        if e.errno == errno.EADDRINUSE:
            print(f"(!) Error: El puerto {PORT} ya está siendo usado por otra aplicación.")
        else:
            print(f"(!) Ocurrió un error inesperado al abrir el socket: {e}")
        return None
  except socket.error as e:
    print(f"(!) Error de configuración del socket: {e}")
    server_sock.close()
    return None
 

# Atiende a un cliente específico, recibiendo mensajes, guardando en la base de datos y respondiendo con la hora de llegada
def handle_client(client_sock):
  ip, port = client_sock.getpeername()
  print(f"(+) Nuevo cliente conectado desde {ip}:{port}")
  with client_sock:
    while True:
      try:
        data = client_sock.recv(1024)
        if not data:
          print(f"(-) Cliente desconectado desde {ip}:{port}.")
          break
        message = data.decode('utf-8').strip()

        # Guardar el mensaje en la base de datos y obtener el timestamp
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
  print(f"(x) Conexión finalizada con el cliente {ip}:{port}")


# Aceptar clientes y genera un hilo para cada uno
def accept_clients(server_sock):
  # Ponemos un timeout de 1 segundo para detectar si se presiona ctrl+c
  server_sock.settimeout(1.0)   
  print("Presiona Ctrl+C para detener el servidor.")
  while True:
    try:
      client_sock, addr = server_sock.accept()
      t = threading.Thread(target=handle_client, args=(client_sock,), daemon=True).start()
    except socket.timeout:
      # Lapso de tiempo que permite capturar el ctrl+C
      continue


# Punto de entrada del programa
if __name__ == "__main__":
  database.init_db()
  server_sock = init_server()
  if(server_sock):
    try:
      accept_clients(server_sock)
    except KeyboardInterrupt:
      print("(!) Servidor detenido por el usuario.")
    except Exception as e:
      print(f"(!) Error al aceptar clientes: {e}")
    finally:
            # Este bloque se ejecuta SIEMPRE, ya sea por error o por Ctrl+C
      server_sock.close()
      print("(x) Socket cerrado. ¡Adiós!")
    