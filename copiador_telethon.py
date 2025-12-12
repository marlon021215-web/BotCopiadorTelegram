from telethon import TelegramClient, events
import requests
import os
import time

# =============================================
# CONFIGURACIÓN — RELLENAR EN TU PC
# =============================================
api_id = 0                # <-- PON AQUÍ TU API ID (my.telegram.org)
api_hash = ''             # <-- PON AQUÍ TU API HASH
BOT_TOKEN = ''            # <-- PON AQUÍ TU TOKEN DEL BOT
CANAL_ORIGEN = 'CorretoraQuotex'    # canal origen
CANAL_DESTINO = '@Quotexplus'       # canal destino
# =============================================

session_name = 'session_yair'
client = TelegramClient(session_name, api_id, api_hash)

def enviar_texto(texto):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CANAL_DESTINO,
        "text": texto
    }
    requests.post(url, data=data)

def enviar_archivo(path, caption=None):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
    files = {"document": open(path, "rb")}
    data = {"chat_id": CANAL_DESTINO}
    if caption:
        data["caption"] = caption
    requests.post(url, files=files, data=data)
    files["document"].close()

def enviar_foto(path, caption=None):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    files = {"photo": open(path, "rb")}
    data = {"chat_id": CANAL_DESTINO}
    if caption:
        data["caption"] = caption
    requests.post(url, files=files, data=data)
    files["photo"].close()

@client.on(events.NewMessage(chats=CANAL_ORIGEN))
async def handler(event):
    print("Nuevo mensaje detectado en canal origen")

    # Si es texto
    if event.text:
        enviar_texto(event.text)
        return

    # Si tiene media, descargar y enviar
    if event.media:
        fname = f"tmp_{int(time.time())}"
        path = await event.download_media(file=fname)

        if not path:
            return

        # foto
        if path.lower().endswith((".jpg", ".jpeg", ".png", ".gif", ".webp")):
            enviar_foto(path)
        else:
            enviar_archivo(path)

        os.remove(path)

async def main():
    print("Iniciando sesión…")
    await client.start()
    print("Copiador activo — escuchando nuevos mensajes...")
    await client.run_until_disconnected()

if __name__ == "__main__":
    with client:
        client.loop.run_until_complete(main())

