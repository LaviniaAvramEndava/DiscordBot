import random
import discord
from discord.ext import commands
from .gamesLogic import RPS_CHOICES, rps_outcome, GuessSessions
from .store import Store


def create_bot(store: Store, sessions: GuessSessions) -> commands.Bot:

    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix="$", intents=intents, help_command=None)

    @bot.command()
    async def poll(ctx, question: str, *options: str):
        if len(options) < 2:
            await ctx.send("You must provide at least 2 options for the poll.")
            return
        if len(options) > 10:
            await ctx.send("You can provide at most 10 options.")
            return
        emojis = [
            "1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣",
            "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"
        ]
        description = "\n".join(f"{emojis[i]} {opt}" for i, opt in enumerate(options))
        embed = discord.Embed(title=question, description=description, color=0x00ff00)
        poll_message = await ctx.send(embed=embed)
        for i in range(len(options)):
            await poll_message.add_reaction(emojis[i])
        # Store poll in persistent storage
        poll_id = str(poll_message.id)
        store.add_poll(poll_id, question, list(options))
        await ctx.send(f"Poll created! Vote by reacting below.")

    @bot.event
    async def on_message(message):
        if message.author.bot:
            return
        greetings = ["hello", "hi", "hey", "salut", "hola"]
        if any(message.content.lower().startswith(greet) for greet in greetings):
            responses = [
                f"Hello, {message.author.display_name}!",
                f"Hi there, {message.author.display_name}!",
                f"Hey, {message.author.display_name}!",
                f"Salut, {message.author.display_name}!",
                f"Hola, {message.author.display_name}!"
            ]
            await message.channel.send(random.choice(responses))
        await bot.process_commands(message)

    @bot.event
    async def on_ready():
        print(f"✅ Logged in as {bot.user} (id={bot.user.id})")

    @bot.command()
    async def help(ctx):
        await ctx.send(
            "**Mini Games Bot**\n"
            "• `$roll` – Roll a die\n"
            "• `$rps <rock|paper|scissors>` – Rock–Paper–Scissors\n"
            "• `$guess start` / `$guess <number>` / `$guess stop`\n"
            "• `$leaderboard` – Show top winners\n"
            "• `$poll \"Your question?\" \"Option 1\" \"Option 2\" ...` – Create a poll (up to 10 options)"
        )

    @bot.command()
    async def roll(ctx):
        n = random.randint(1, 6)
        if n == 6:
            store.add_win(ctx.author.id, ctx.author.display_name)
            await ctx.send(f"🎲 You rolled **{n}**! (+1 win)")
        else:
            await ctx.send(f"🎲 You rolled **{n}**")

    @bot.command()
    async def rps(ctx, choice: str = None):
        if not choice or choice.lower() not in RPS_CHOICES:
            return await ctx.send("Use `$rps rock`, `$rps paper`, or `$rps scissors`.")
        choice = choice.lower()
        bot_choice = random.choice(RPS_CHOICES)
        outcome = rps_outcome(choice, bot_choice)
        if outcome == "win":
            store.add_win(ctx.author.id, ctx.author.display_name)
            await ctx.send(f"I chose **{bot_choice}**. You **win!** (+1 win)")
        elif outcome == "lose":
            await ctx.send(f"I chose **{bot_choice}**. You lose!")
        else:
            await ctx.send(f"We both chose **{bot_choice}**. Draw!")

    @bot.group(invoke_without_command=True)
    async def guess(ctx, arg: str = None):
        uid = ctx.author.id
        if arg is None:
            return await ctx.send("Use `$guess start`, `$guess <number>`, or `$guess stop`.")

        if arg.lower() == "start":
            sessions.start(uid)
            return await ctx.send("🎯 Number is between 1–100. Guess with `$guess <number>`!")

        if arg.lower() == "stop":
            if sessions.active(uid):
                sessions.stop(uid)
                await ctx.send(f"🛑 {ctx.author.display_name}, your round has been stopped. Others can continue their own games.")
            else:
                await ctx.send(f"{ctx.author.display_name}, you don't have an active round.")
            return

        if not arg.isdigit():
            return await ctx.send("Enter a valid number.")
        if not sessions.active(uid):
            return await ctx.send("Start a round with `$guess start` first.")

        value = int(arg)
        result, tries = sessions.guess(uid, value)
        if result == "correct":
            store.add_win(uid, ctx.author.display_name, amount=2)
            return await ctx.send(f"✅ Correct! It was **{value}**. Attempts: **{tries}** (+2 wins)")
        await ctx.send("📉 Too low!" if result == "low" else "📈 Too high!")

    @bot.command()
    async def leaderboard(ctx, top: int = 10):
        wins = store.wins()
        if not wins:
            return await ctx.send("No wins yet. Play a game!")
        top_items = sorted(wins.items(), key=lambda kv: kv[1], reverse=True)[:top]
        lines = []
        for i, (uid, score) in enumerate(top_items, start=1):
            member = ctx.guild.get_member(int(uid))
            if member:
                name = member.display_name
            else:
                try:
                    user = await ctx.bot.fetch_user(int(uid))
                    name = user.name
                except Exception:
                    name = f"User {uid}"
            lines.append(f"{i}. **{name}** — {score} wins")
        await ctx.send("🏆 **Leaderboard**\n" + "\n".join(lines))

    return bot
