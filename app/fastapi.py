from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from .store import Store
from .gamesLogic import GuessSessions

def create_app(store: Store, sessions: GuessSessions) -> FastAPI:

    app = FastAPI()

    @app.get("/polls")
    def polls():
        polls_data = store.get_polls()
        if not polls_data:
            return HTMLResponse(render_page("🗳️ Polls", "<p>No polls found.</p>"))
        html = ""
        for poll_id, poll in polls_data.items():
            html += f"<div style='margin-bottom:28px;'><b>{poll['question']}</b><ul>"
            for opt, votes in zip(poll['options'], poll['votes']):
                html += f"<li><span class='option'>{opt}</span> — <span class='votes'>{votes} votes</span></li>"
            html += "</ul></div>"
        return HTMLResponse(render_page("🗳️ Polls", html))

    @app.get("/", response_class=HTMLResponse)
    def home():
                return """
                <html>
                <head>
                <style>
                body { font-family: 'Segoe UI', Arial, sans-serif; background: #f7f7fa; color: #222; margin: 0; padding: 0; }
                .container { max-width: 600px; margin: 40px auto; background: #fff; border-radius: 12px; box-shadow: 0 2px 8px #0001; padding: 32px; }
                h1 { color: #2b6cb0; margin-top: 0; }
                ul { list-style: none; padding: 0; }
                li { margin: 18px 0; }
                a { color: #3182ce; text-decoration: none; font-size: 1.2em; }
                a:hover { text-decoration: underline; }
                </style>
                </head>
                <body>
                <div class="container">
                <h1>Mini Games Bot API</h1>
                <ul>
                    <li><a href="/leaderboard">🏆 Leaderboard</a></li>
                    <li><a href="/stats">📊 Stats</a></li>
                    <li><a href="/polls">🗳️ Polls</a></li>
                </ul>
                </div>
                </body>
                </html>
                """

    @app.get("/leaderboard")
    def leaderboard():
        wins = store.wins()
        top = sorted(wins.items(), key=lambda kv: kv[1], reverse=True)
        rows = []
        for i, (uid, score) in enumerate(top, start=1):
            username = store.get_username(uid) or f"User {uid}"
            rows.append(f"<tr><td>{i}</td><td>{username}</td><td>{score}</td></tr>")
        table = f"""
        <table>
          <tr><th>#</th><th>User</th><th>Wins</th></tr>
          {''.join(rows)}
        </table>
        """ if rows else "<p>No wins yet!</p>"
        return HTMLResponse(render_page("🏆 Leaderboard", table))

    @app.get("/stats")
    def stats():
        wins = store.wins()
        stats_html = f"""
        <table>
          <tr><th>Total Users</th><th>{len(wins)}</th></tr>
          <tr><th>Total Wins</th><th>{sum(wins.values())}</th></tr>
          <tr><th>Active Guess Games</th><th>{len(sessions.sessions)}</th></tr>
        </table>
        """
        return HTMLResponse(render_page("📊 Stats", stats_html))

    @app.get("/polls")
    def polls():
        polls_data = store.get_polls()
        # Format as a list for easier API consumption
        result = []
        for poll_id, poll in polls_data.items():
            result.append({
                "poll_id": poll_id,
                "question": poll["question"],
                "options": poll["options"],
                "votes": poll["votes"]
            })
        return {"polls": result}

    @app.get("/polls/<poll_id>")
    def poll_detail(poll_id):
        poll = store.get_poll(poll_id)
        if not poll:
            return {"error": "Poll not found"}
        html = f"""
        <html>
        <head>
        <style>
        body {{ font-family: 'Segoe UI', Arial, sans-serif; background: #f7f7fa; color: #222; margin: 0; padding: 0; }}
        .container {{ max-width: 600px; margin: 40px auto; background: #fff; border-radius: 12px; box-shadow: 0 2px 8px #0001; padding: 32px; }}
        h1 {{ color: #2b6cb0; margin-top: 0; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 18px; }}
        th, td {{ padding: 10px 8px; border-bottom: 1px solid #e2e8f0; text-align: left; }}
        th {{ background: #ebf8ff; color: #2b6cb0; }}
        tr:last-child td {{ border-bottom: none; }}
        .stat {{ font-size: 1.1em; margin: 8px 0; }}
        ul {{ list-style: none; padding: 0; }}
        li {{ margin: 10px 0; }}
        .option {{ font-weight: 500; }}
        .votes {{ color: #3182ce; font-weight: bold; }}
        </style>
        </head>
        <body><div class='container'>
        <h1>{poll["question"]}</h1>
        <ul>
            {"".join([f"<li>{option}</li>" for option in poll["options"]])}
        </ul>
        <p>{poll["votes"]}</p>
        </div></body></html>
        """
        return HTMLResponse(render_page("🗳️ Polls", html))

    return app

def render_page(title, content):
    return f"""
    <html>
    <head>
    <style>
    body {{ font-family: 'Segoe UI', Arial, sans-serif; background: #f7f7fa; color: #222; margin: 0; padding: 0; }}
    .container {{ max-width: 600px; margin: 40px auto; background: #fff; border-radius: 12px; box-shadow: 0 2px 8px #0001; padding: 32px; }}
    h1 {{ color: #2b6cb0; margin-top: 0; }}
    table {{ width: 100%; border-collapse: collapse; margin-top: 18px; }}
    th, td {{ padding: 10px 8px; border-bottom: 1px solid #e2e8f0; text-align: left; }}
    th {{ background: #ebf8ff; color: #2b6cb0; }}
    tr:last-child td {{ border-bottom: none; }}
    .stat {{ font-size: 1.1em; margin: 8px 0; }}
    ul {{ list-style: none; padding: 0; }}
    li {{ margin: 10px 0; }}
    .option {{ font-weight: 500; }}
    .votes {{ color: #3182ce; font-weight: bold; }}
    </style>
    </head>
    <body><div class='container'>
    <h1>{title}</h1>
    {content}
    </div></body></html>
    """
