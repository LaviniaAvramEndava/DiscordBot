import random

#Rock-Paper-Scissors logic
RPS_CHOICES = ["rock", "paper", "scissors"]

def rps_outcome(user: str, bot_choice: str) -> str:
    if user == bot_choice:
        return "draw"
    wins = {"rock": "scissors", "paper": "rock", "scissors": "paper"}
    return "win" if wins[user] == bot_choice else "lose"

#Guess the Number logic
class GuessSessions:
    def __init__(self):
        self.sessions = {}  # user_id -> {"target": int, "attempts": int}

    def start(self, user_id: int):
        self.sessions[user_id] = {"target": random.randint(1, 100), "attempts": 0}

    def stop(self, user_id: int):
        self.sessions.pop(user_id, None)

    def active(self, user_id: int) -> bool:
        return user_id in self.sessions

    def guess(self, user_id: int, value: int):
        s = self.sessions[user_id]
        s["attempts"] += 1
        if value == s["target"]:
            tries = s["attempts"]
            self.stop(user_id)
            return ("correct", tries)
        return ("low", s["attempts"]) if value < s["target"] else ("high", s["attempts"])