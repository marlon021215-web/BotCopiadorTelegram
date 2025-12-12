from telethon import TelegramClient, events
import re

# ======================
# CONFIGURACIÓN
# ======================

api_id = 38616374
api_hash = "fc9e3d72e05c43f541caee55838d0c54"

# Muy importante: NO usar el número aquí en Render.
# Render usará la sesión guardada automáticamente.
telefono_o_token = None

canal_origen = -1001572222502
canal_destino = -1003277843142

# ======================
# INICIO DEL CLIENTE
# ======================

client = TelegramClient("session", api_id, api_hash)

# Quitar URLs
def limpiar_texto(texto):
    if texto is None:
        return None
    return re.sub(r'https?://\S+|t\.me/\S+', '', texto).strip()

# ======================
# MANEJAR MENSAJES NUEVOS
# ======================

@client.on(events.NewMessage(chats=canal_origen))
async def handler(event):

    texto = limpiar_texto(event.text)

    if not texto:
        print("Mensaje ignorado (solo tenía links).")
        return

    await client.send_message(canal_destino, texto)
    print("Mensaje enviado al canal destino.")

# ======================
# EJECUCIÓN
# ======================

async def main():
    print("========== BOT INICIADO ==========")
    print("Copiando señales sin enlaces...")
    print(f"Canal origen : {canal_origen}")
    print(f"Canal destino: {canal_destino}")
    print("=================================\n")

client.start()   # ← SIN NÚMERO, USA session.session DIRECTO
client.loop.run_until_complete(main())
client.run_until_disconnected()
