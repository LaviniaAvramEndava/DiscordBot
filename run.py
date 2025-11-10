import threading
import uvicorn
from app.config import TOKEN
from app.store import Store
from app.gamesLogic import GuessSessions
from app.fastapi import create_app
from app.botApp import create_bot

def _run_api(app):
    uvicorn.run(app, host="127.0.0.1", port=8000)

def main():
    if not TOKEN:
        raise RuntimeError("DISCORD_TOKEN not found in .env")

    store = Store()
    sessions = GuessSessions()

    app = create_app(store, sessions)
    bot = create_bot(store, sessions)

    threading.Thread(target=_run_api, args=(app,), daemon=True).start()
    bot.run(TOKEN)

if __name__ == "__main__":
    main()
