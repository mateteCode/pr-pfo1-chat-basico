# Chat Básico Cliente-Servidor con Persistencia en SQLite

Este proyecto implementa un sistema de chat básico utilizando **Sockets TCP/IP** en Python. El servidor es capaz de manejar múltiples conexiones simultáneas mediante hilos (_threading_) y almacena cada mensaje recibido en una base de datos **SQLite**.

## 🚀 Características

- **Servidor Multihilo:** Soporta múltiples clientes conectados al mismo tiempo.
- **Persistencia de Datos:** Registro automático de mensajes (contenido, fecha, IP) en base de datos.
- **Manejo de Errores:** Control de puertos ocupados, desconexiones inesperadas y errores de base de datos.
- **Arquitectura Modular:** Separación lógica entre la gestión de red (`server.py`), la lógica de datos (`database.py`) y el cliente (`client.py`).

## 🛠️ Tecnologías Utilizadas

- **Lenguaje:** Python 3.14.3
- **Librerías Estándar:** `socket`, `threading`, `sqlite3`, `datetime`.

## 📂 Estructura del Proyecto

```text
.
├── server.py        # Lógica del servidor y gestión de sockets.
├── client.py        # Interfaz de usuario para enviar mensajes.
├── database.py      # Módulo de persistencia y consultas SQL.
├── messages.db      # Base de datos SQLite (se genera al iniciar).
├── test_db.py       # Prueba de lectura de los mensajes almacenados.
└── README.md        # Documentación del proyecto.
```

## 🚀 Insalación y Ejecución

1. **Clona el repositorio:**

```bash
 git clone https://github.com/mateteCode/pr-pfo1-chat-basico.git
```

2. **Iniciar el Servidor:**
   Abre una terminal y ejecuta:

```bash
python server.py
```

El servidor quedará escuchando en localhost:5000.

3. **Iniciar el Cliente:**
   En otra terminal (o varias), ejecuta:

```bash
python client.py
```

Podes escribir varios mensajes y ver que respuestas se generan desde el servidor.

4. **Finalizar:**
   Para salir del cliente, escribe "éxito".
   Para detener el servidor, usa Ctrl + C.

## 🧪 Pruebas

Parar leer todos los mensajes guardados, abre una terminal y ejecuta:

```bash
python test_db.py
```
