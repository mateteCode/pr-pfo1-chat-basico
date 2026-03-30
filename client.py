import socket

HOST = '127.0.0.1'
POST = 5000

# Cliente del chat que se conecta al servidor, envía mensajes y recibe confirmaciones con la hora de llegada
def start_client():
  client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  try:
    client_socket.connect((HOST, POST))
    print("Conectado al servidor. Podés enviar mensajes o escribir 'éxito' para salir.")

    while True:
        user_input = input("Escriba un mensaje: ").strip()
        if user_input.lower() in ("éxito", "exito"):
            print("Terminando la comunicación con el servidor.")
            break
        client_socket.sendall(user_input.encode('utf-8'))

        server_response = client_socket.recv(1024).decode('utf-8')
        if not server_response:
            print("El servidor ha cerrado la conexión.")
            break
        print(f"{server_response}")
  except BrokenPipeError:
      print("ERROR: El servidor ha cerrado la conexión.")
  except ConnectionRefusedError:
      print(f"ERROR: No se pudo conectar al servidor en {HOST}:{POST}. Asegúrate de que el servidor esté en ejecución.")
  except Exception as e:
      print(f"ERROR: Ocurrió un error en el cliente: {e}")
  finally:
      client_socket.close()
      print("Conexión cerrada y salida del cliente.")


if __name__ == "__main__":
    start_client()