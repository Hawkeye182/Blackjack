import asyncio
import websockets
import json

# Diccionario para manejar las partidas y los jugadores conectados
salas = {}

async def manejar_conexion(websocket, path):
    async for mensaje in websocket:
        data = json.loads(mensaje)
        accion = data["accion"]
        
        if accion == "crear_sala":
            sala_id = data["sala_id"]
            salas[sala_id] = {"jugadores": [websocket], "estado": "esperando"}
            await websocket.send(json.dumps({"mensaje": f"Sala {sala_id} creada."}))
        
        elif accion == "unirse_sala":
            sala_id = data["sala_id"]
            if sala_id in salas:
                salas[sala_id]["jugadores"].append(websocket)
                await websocket.send(json.dumps({"mensaje": "Te uniste a la sala."}))
            else:
                await websocket.send(json.dumps({"error": "Sala no encontrada."}))

# Iniciar servidor WebSocket
start_server = websockets.serve(manejar_conexion, "localhost", 8080)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
