from telethon import TelegramClient, events
import asyncio
import re

# ==== TUS DATOS ====
api_id = 38616374
api_hash = "fc9e3d72e05c43f541caee55838d0c54"

canal_origen = -1001572222502      # CorretoraQuotex
canal_destino = -1003277843142     # Quotexplus
# ====================


client = TelegramClient('session_copybot', api_id, api_hash)

# 🔥 Función que elimina links
def limpiar_urls(texto):
    if not texto:
        return ""
    return re.sub(r'https?://\S+', '', texto).strip()


@client.on(events.NewMessage(chats=canal_origen))
async def copiar(event):

    try:
        # Eliminar URLs del texto
        texto = limpiar_urls(event.message.message)

        # 🟩 SI ES SOLO TEXTO
        if event.message.message and not event.message.media:
            await client.send_message(canal_destino, texto)

        # 🟦 SI CONTIENE FOTO/VIDEO/ARCHIVO
        elif event.message.media:
            await client.send_file(
                canal_destino,
                event.message.media,
                caption=texto
            )

        print("Mensaje copiado sin URLs.")

    except Exception as e:
        print("ERROR:", e)


async def main():
    print("BOT INICIADO — COPIANDO SEÑALES SIN LINKS...")
    await client.run_until_disconnected()


with client:
    client.loop.run_until_complete(main())
