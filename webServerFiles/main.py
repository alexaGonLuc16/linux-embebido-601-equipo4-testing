import os
import shutil
import socket
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse
from datetime import datetime

app = FastAPI()

# Lista para almacenar los registros de acceso
access_log = []

# Dirección y puerto del servidor de sockets
ADDRESS = 'localhost'
PORT = 3333

def send_message_to_server(message):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((ADDRESS, PORT))
        sock.sendall(message.encode())
        sock.close()
    except Exception as e:
        print(f"Failed to send message to server: {e}")

@app.get("/", response_class=HTMLResponse)
async def main():
    def formatear_fecha(fecha):
        meses = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
        dia = fecha.day
        mes = meses[fecha.month - 1]
        return f"{dia} de {mes}"

    fecha_actual = formatear_fecha(datetime.now())

    access_table = "<table><tr><th>Hora</th><th>Usuario</th><th>Estatus</th></tr>"
    for entry in access_log:
        access_table += f"<tr><td>{entry['time']}</td><td>{entry['user']}</td><td>{entry['status']}</td></tr>"
    access_table += "</table>"

    content = f"""
<!DOCTYPE html>
<html>
    <head>
        <title>Registro de Acceso</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                background-color: #f0f0f0;
            }}
            .container {{
                background-color: #ffffff;
                padding: 20px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                border-radius: 8px;
                width: 90%;
                max-width: 1200px;
                display: flex;
                flex-direction: column;
            }}
            h1 {{
                margin-bottom: 20px;
                text-align: center;
            }}
            .table-container {{
                flex: 1;
                overflow-y: auto;
                margin-bottom: 20px;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
            }}
            table, th, td {{
                border: 1px solid black;
            }}
            th, td {{
                padding: 10px;
                text-align: left;
                font-size: 1em;
            }}
            @media (max-width: 600px) {{
                th, td {{
                    font-size: 0.8em;
                    padding: 5px;
                }}
                .container {{
                    padding: 10px;
                }}
                h1 {{
                    font-size: 1.5em;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div>{fecha_actual}</div>
            <h1>Registro de Usuarios</h1>
            <div class="table-container">
                {access_table}
            </div>
        </div>
    </body>
</html>
    """
    return HTMLResponse(content=content)

@app.post("/receive_code/")
async def receive_code(request: Request):
    data = await request.form()
    code = data.get("code")
    status = data.get("status")
    if code:
        access_log.append({
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "user": code,
            "status": status
        })
        # Enviar un mensaje al servidor de sockets
        send_message_to_server(f"{code} - {status}")
        return JSONResponse(content={"message": "Code received successfully"})
    return JSONResponse(content={"message": "No code received"}, status_code=400)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8080)
