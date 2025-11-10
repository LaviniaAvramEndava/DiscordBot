from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from .store import Store
from .gamesLogic import GuessSessions

def create_app(store: Store, sessions: GuessSessions) -> FastAPI:
    app = FastAPI()

    @app.get("/", response_class=HTMLResponse)
    def home():
        return """
        <h1> Mini Games Bot API</h1>
        <ul>
          <li><a href="/leaderboard">/leaderboard</a></li>
          <li><a href="/stats">/stats</a></li>
        </ul>
        """

    @app.get("/leaderboard")
    def leaderboard():
        wins = store.wins()
        top = sorted(wins.items(), key=lambda kv: kv[1], reverse=True)
        leaderboard = []
        for uid, score in top:
            username = store.get_username(uid)
            leaderboard.append({
                "user_id": uid,
                "username": username,
                "wins": score
            })
        return {"leaderboard": leaderboard}

    @app.get("/stats")
    def stats():
        wins = store.wins()
        return {
            "total_users": len(wins),
            "total_wins": sum(wins.values()),
            "active_guess_games": len(sessions.sessions),
        }

    return app
