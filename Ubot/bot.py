import asyncio

from telethon.tl.functions.account import UpdateProfileRequest
from telethon import TelegramClient, events
from gtts import gTTS
from telethon.tl.types import PeerChannel, PeerChat, PeerUser

ADMIN = 5193095802
API_KEY = "21627484"  # API ID
API_HASH = "45ace3d738494add4dee68a680c1b2cf"  # API HASH
SESSION_NAME = "userbot.session"  # Nome del file di sessione
ubot = TelegramClient("ubot", API_KEY, API_HASH)
ubot.parse_mode = "html"


@ubot.on(events.NewMessage(outgoing=True))
async def RaspaManager(e):
    global ADMIN
    if ADMIN is None:
        me = await ubot.get_me()
        ADMIN = me.id
        print("admin is " + str(me.id))
    if e.sender_id == ADMIN:
        if e.text == ".info":
            if e.is_reply:
                reply = await e.get_reply_message()
                if e.is_private:
                    friend = await ubot.get_entity(reply.peer_id.user_id)
                else:
                    friend = await ubot.get_entity(reply.from_id.user_id)

                await e.edit("Bot 🤖: "+ str(friend.bot)+"\nUsername: @"+ str(friend.username)+ "\nDC📳 :" + str(friend.photo.dc_id) + "\nFirst_name✊🏿:" + str(
                    friend.first_name) + "\nLast name✋🏿: " + str(
                    friend.last_name) + "\n Chat id🔬: <a href=\"tg://user?id=" + str(friend.id) + "\">" + str(
                    friend.id) + "</a>")
            else:
                await e.edit("<b>Non è un reply❌\nusalo replicando un messaggio</b>")
        elif e.text == ".on":
            await ubot(UpdateProfileRequest(
                last_name="ON🟢️"
            ))
            await e.edit("<b>sono ON🟢️</b>")
        elif e.text == ".off":
            await ubot(UpdateProfileRequest(
                last_name="OFF🔴"
            ))
            await e.edit("<b>sono OFF🔴</b>")
        elif e.text == ".a":
            await e.edit("ª")
        elif e.text.startswith(".type "):
            s1 = e.text.replace(".type ", "")
            s2 = list(s1)
            msg = "💬->"
            for c1 in s2:
                if c1 == " ":
                    c1 = "_"
                if c1 == "\n":
                    c1= "\n."
                msg = msg + c1
                await e.edit(msg)
                await asyncio.sleep(0.17)


        elif e.text.startswith(".tts"):
            s1 = e.text.replace(".tts ", "")
            tts = gTTS(s1, lang="it")
            tts.save("tts.mp3")
            id = None
            if isinstance(e.peer_id, PeerChannel):
                id = e.peer_id.channel_id
            elif isinstance(e.peer_id, PeerChat):
                id = e.peer_id.chat_id
            elif isinstance(e.peer_id, PeerUser):
                id = e.peer_id.user_id
            ent = await ubot.get_entity(id)
            await ubot.send_file(ent, file="tts.mp3",voice_note=True)
            await e.delete()



ubot.start()

ubot.run_until_disconnected()
