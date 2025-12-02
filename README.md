Project Description
This project builds a Discord Bot that combines fun mini-games and useful utilities. Using the discord.py library, the bot allows users to play quick games like dice roll, rock-paper-scissors, and number guessing, while tracking player scores in a persistent leaderboard.
Alongside the bot, a FastAPI web service exposes simple endpoints (and optional HTML pages) for live stats, the leaderboard, and configuration.

The project extends a basic Discord command bot into a modular, production-ready system with a clear structure, persistent storage, and additional user-friendly features.

MVP
Connect to Discord using required intents.

Implement commands: $roll, $rps, $guess, $leaderboard, $help.

Persist scores to data.json.

Run a FastAPI side server for /leaderboard and /stats endpoints.

