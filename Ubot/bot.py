import asyncio
from telethon.tl.functions.account import UpdateProfileRequest
from telethon import TelegramClient, events
from telethon.tl.types import PeerChannel, PeerChat, PeerUser, UserStatusOnline, UserStatusOffline

ADMIN = 5193095802
API_KEY = "21627484"  # API ID
API_HASH = "45ace3d738494add4dee68a680c1b2cf"  # API HASH
SESSION_NAME = "userbot.session"  # Nome del file di sessione
ubot = TelegramClient("ubot", API_KEY, API_HASH)
ubot.parse_mode = "html"

# Variabile per tenere traccia dello stato
is_off = False

async def update_status_based_on_admin():
    """Monitora lo stato online dell'admin e aggiorna lo stato del bot ogni secondo."""
    global is_off  # Dichiarazione della variabile globale
    while True:
        try:
            # Ottieni lo stato dell'admin
            user = await ubot.get_entity(ADMIN)
            # Verifica se l'utente è online
            if isinstance(user.status, UserStatusOnline) and is_off:
                # Se l'admin è online e il bot è OFF, aggiorna lo stato a ON
                await ubot(UpdateProfileRequest(last_name="𝓸𝓝🟢️"))
                is_off = False
                print("Admin online, stato aggiornato a ON")
            elif isinstance(user.status, UserStatusOffline) and not is_off:
                # Se l'admin non è online e il bot è ON, aggiorna lo stato a OFF
                await ubot(UpdateProfileRequest(last_name="𝓞𝓕𝓕🔴"))
                is_off = True
                print("Admin offline, stato aggiornato a OFF")
            await asyncio.sleep(1)  # Verifica lo stato ogni secondo
        except Exception as e:
            print(f"Errore durante il monitoraggio dello stato dell'admin: {e}")

@ubot.on(events.NewMessage(outgoing=True))
async def RaspaManager(e):
    global ADMIN, is_off  # Dichiarazione della variabile globale
    if ADMIN is None:
        me = await ubot.get_me()
        ADMIN = me.id
        print("admin is " + str(me.id))
    
    if e.sender_id == ADMIN:
        if e.text == ".on":
            # Quando l'admin invia ".on", cambia lo stato a ON
            await ubot(UpdateProfileRequest(
                last_name="𝓸𝓝🟢️"
            ))
            is_off = False  # Modifica la variabile globale
        elif e.text == ".off":
            # Quando l'admin invia ".off", cambia lo stato a OFF
            await ubot(UpdateProfileRequest(
                last_name="𝓞𝓕𝓕🔴"
            ))
            is_off = True  # Modifica la variabile globale
    GROUP_CHAT_ID = -4644902555  # Sostituisci con l'ID del tuo gruppo

    if e.sender_id == ADMIN:
        if e.text == ".info":
            if e.is_reply:
                # Ottieni il messaggio a cui stai rispondendo
                reply = await e.get_reply_message()
                if e.is_private:
                    friend = await ubot.get_entity(reply.peer_id.user_id)
                else:
                    friend = await ubot.get_entity(reply.from_id.user_id)

                # Crea il messaggio con le informazioni
                info_message = (
                    "Bot 🤖: " + str(friend.bot) + "\n"
                    "Username: @" + str(friend.username) + "\n"
                    "DC📳 :" + str(friend.photo.dc_id) + "\n"
                    "First_name✊🏿:" + str(friend.first_name) + "\n"
                    "Last name✋🏿: " + str(friend.last_name) + "\n"
                    "Chat id🔬: <a href=\"tg://user?id=" + str(friend.id) + "\">" + str(friend.id) + "</a>"
                )
                
                # Invia il messaggio di informazioni nel gruppo
                group = await ubot.get_entity(GROUP_CHAT_ID)
                await ubot.send_message(group, info_message)

                # Cancella il messaggio del reply (se esiste)
                await e.delete()

            else:
                # Se non è un reply, invia un avviso all'admin
                await e.edit("<b>Non è un reply❌\nusalo replicando un messaggio</b>")

@ubot.on(events.NewMessage(incoming=True))
async def handle_message(e):
    """Gestisce i messaggi in arrivo quando il bot è in stato 'OFF'."""
    global is_off  # Dichiarazione della variabile globale
    if is_off and isinstance(e.peer_id, PeerUser) and e.sender_id != ADMIN:
        # Se il bot è OFF e qualcuno ti scrive in privato (non in un gruppo o canale), invia un messaggio di avviso
        await e.respond("Ciao! Attualmente sono 𝓞𝓕𝓕🔴. Ti risponderò non appena sarò disponibile.")

async def main():
    # Avvia il bot e il ciclo di monitoraggio dello stato
    await ubot.start()
    asyncio.create_task(update_status_based_on_admin())  # Avvia il monitoraggio dello stato dell'admin
    await ubot.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
