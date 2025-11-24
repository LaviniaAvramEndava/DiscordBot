import json
from pathlib import Path

class Store:
    def __init__(self, filename: str = "data.json"):
        self.path = Path(filename)
        self.data = {"wins": {}}
        self.load()

    def load(self):
        if self.path.exists():
            try:
                self.data = json.loads(self.path.read_text(encoding="utf-8"))
            except Exception:
                self.data = {"wins": {}}

    def save(self):
        self.path.write_text(json.dumps(self.data, indent=2), encoding="utf-8")

    def add_win(self, user_id: int, username: str = None, amount: int = 1):
        uid = str(user_id)
        if "users" not in self.data:
            self.data["users"] = {}
        if username:
            self.data["users"][uid] = username
        self.data["wins"][uid] = self.data["wins"].get(uid, 0) + amount
        self.save()

    def get_username(self, user_id: int):
        uid = str(user_id)
        return self.data.get("users", {}).get(uid)

    def wins(self):
        return self.data.get("wins", {})

    def add_poll(self, poll_id: str, question: str, options: list):
        if "polls" not in self.data:
            self.data["polls"] = {}
        self.data["polls"][poll_id] = {
            "question": question,
            "options": options,
            "votes": [0] * len(options)
        }
        self.save()

    def vote_poll(self, poll_id: str, option_index: int):
        if "polls" in self.data and poll_id in self.data["polls"]:
            self.data["polls"][poll_id]["votes"][option_index] += 1
            self.save()

    def get_polls(self):
        return self.data.get("polls", {})
