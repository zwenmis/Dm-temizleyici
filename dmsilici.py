import discord
import asyncio
import threading
import tkinter as tk
from tkinter import messagebox

class DiscordClient(discord.Client):
    def __init__(self, user_id, limit, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_id = user_id
        self.limit = limit

    async def on_ready(self):
        print(f"Bot giriş yaptı: {self.user}")
        print("Panel: zwen tarafından geliştirildi.")
        user = await self.fetch_user(int(self.user_id))
        channel = await user.create_dm()

        async for msg in channel.history(limit=int(self.limit)):
            if msg.author == self.user:
                try:
                    await msg.delete()
                    print(f"Silindi: {msg.content}")
                    await asyncio.sleep(1)
                except Exception as e:
                    print(f"Hata oluştu: {e}")
        print("Silme işlemi tamamlandı.")
        await self.close()

def run_bot(token, user_id, limit):
    intents = discord.Intents.default()
    intents.messages = True
    intents.dm_messages = True

    client = DiscordClient(user_id, limit, intents=intents)
    asyncio.run(client.start(token))

def start_bot_thread(token, user_id, limit):
    threading.Thread(target=run_bot, args=(token, user_id, limit)).start()

def main():
    root = tk.Tk()
    root.title("Discord DM Temizleyici (zwen)")

    tk.Label(root, text="Bot Token:").grid(row=0, column=0)
    tk.Label(root, text="Kullanıcı ID:").grid(row=1, column=0)
    tk.Label(root, text="Mesaj Sayısı (limit):").grid(row=2, column=0)

    token_entry = tk.Entry(root, width=50)
    user_id_entry = tk.Entry(root)
    limit_entry = tk.Entry(root)

    token_entry.grid(row=0, column=1)
    user_id_entry.grid(row=1, column=1)
    limit_entry.grid(row=2, column=1)

    def on_run():
        token = token_entry.get()
        user_id = user_id_entry.get()
        limit = limit_entry.get()
        if not token or not user_id or not limit:
            messagebox.showerror("Hata", "Tüm alanları doldurun!")
            return
        start_bot_thread(token, user_id, limit)
        messagebox.showinfo("Bilgi", "Bot çalışmaya başladı. Konsol ekranını kontrol edin.")

    run_button = tk.Button(root, text="Başlat", command=on_run)
    run_button.grid(row=3, column=0, columnspan=2, pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
