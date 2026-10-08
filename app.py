from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
import random
from collections import Counter

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///leaderboard.db")

NOOFDICE = 5


def rolldice(n):
    dice = []
    for i in range(n):
        dice.append(random.randint(1, 6))
    return dice


def evalhand(dice):
    hand = Counter(dice)
    handvalue = sorted(hand.values())
    dice.sort()

    if handvalue == [5]:
        return (8, "Five of a kind")

    elif handvalue == [1, 4]:
        return (7, "Four of a kind")

    elif handvalue == [2, 3]:
        return (6, "Full house")

    elif dice == [1, 2, 3, 4, 5] or dice == [2, 3, 4, 5, 6]:
        return (5, "Straight")

    elif handvalue == [1, 1, 3]:
        return (4, "Three of a kind")

    elif handvalue == [1, 2, 2]:
        return (3, "Two pair")

    elif handvalue == [1, 1, 1, 2]:
        return (2, "One pair")

    else:
        return (1, "High die")


def aiplay(dice):
    score, hand = evalhand(dice)
    counts = Counter(dice)

    if score == 1:
        return rolldice(NOOFDICE)

    elif score >= 5:
        reroll = []

    else:
        maxcount = max(counts.values())

        keep = []
        for value, count in counts.items():
            if count == maxcount:
                keep.append(value)

        for i in range(len(dice)):
            if dice[i] not in keep:
                dice[i] = random.randint(1, 6)
    return dice


def game(level):
    dice = rolldice(NOOFDICE)
    aidice = rolldice(NOOFDICE)
    score, hand = evalhand(dice)
    aiscore, aihand = evalhand(aidice)
    highlight = highlightdice(dice)
    aihighlight = highlightdice(aidice)

    session["dice"] = dice
    session["aidice"] = aidice
    session["level"] = level

    return render_template("index.html", dice=dice, aidice=aidice, hand=hand, aihand=aihand, result="", level=level, highlight=highlight, aihighlight=aihighlight)


def highlightdice(dice):
    hand = Counter(dice)
    highlight = [False] * len(dice)

    for i in range(len(dice)):
        value = dice[i]
        if hand[value] > 1:
            highlight[i] = True

    if dice == [1, 2, 3, 4, 5] or dice == [2, 3, 4, 5, 6]:
        highlight = [True] * len(dice)

    return highlight


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        action = request.form.get("action")

        if action == "start":
            session.clear()
            session["level"] = 1
            username = request.form.get("username")
            if username:
                session["username"] = username
            return game(level=1)

        elif action == "restart":
            level = session.get("level", 1)
            return game(level=1)

        elif action == "next":
            level = session.get("level", 1) + 1
            return game(level=level)

        elif action == "replay":
            level = session.get("level", 1)
            return game(level=level)

        else:
            dice = session.get("dice")
            aidice = session.get("aidice")
            level = session.get("level", 1)

            reroll = request.form.getlist("reroll")
            for i in range(len(reroll)):
                reroll[i] = int(reroll[i])

            for i in reroll:
                dice[i] = random.randint(1, 6)

            aidice = aiplay(aidice)

            session["dice"] = dice
            session["aidice"] = aidice

            score, hand = evalhand(dice)
            aiscore, aihand = evalhand(aidice)
            highlight = highlightdice(dice)
            aihighlight = highlightdice(aidice)

            if score > aiscore:
                result = "Player wins!"

            elif aiscore > score:
                result = "AI wins!"
                level = session.get("level", 1)
                if level > 1:
                    username = session.get("username", "Anonymous")
                    level = session["level"]
                    db.execute(
                        "INSERT INTO players (name, level, date) VALUES (?,?,CURRENT_DATE)", username, level)

            else:
                result = "It's a tie"

            return render_template("index.html", dice=dice, hand=hand, aidice=aidice, aihand=aihand, result=result, level=level, highlight=highlight, aihighlight=aihighlight)

    else:
        return render_template("index.html", dice=[], aidice=[], result="", level="")


@app.route("/howtoplay")
def howtoplay():

    return render_template("howtoplay.html")


@app.route("/leaderboard")
def leaderboard():

    players = db.execute("SELECT * FROM players ORDER BY LEVEL DESC LIMIT 10")
    return render_template("leaderboard.html", players=players)
