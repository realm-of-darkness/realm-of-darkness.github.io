#!/usr/bin/env python3
"""Generates the static HTML of realm-of-darkness.at into the given directory."""
import html
import json
import sys
from pathlib import Path

OUT = Path(sys.argv[1])

BAT = ('<svg viewBox="0 0 60 36" aria-hidden="true"><path d="M30 10c2-4 4-6 4-6l1 5c3-1 5 0 5 0 '
       '4-6 12-8 20-6-5 2-8 6-8 12-4-3-8-3-11 1-2-3-5-4-7-3-1 4-4 7-4 7s-3-3-4-7c-2-1-5 0-7 3-3-4-7-4-11-1 '
       '0-6-3-10-8-12 8-2 16 0 20 6 0 0 2-1 5 0l1-5s2 2 4 6z"/></svg>')

COBWEB = ('<svg class="cobweb" viewBox="0 0 150 150" aria-hidden="true" fill="none" stroke="#e9e2d0" stroke-width="1">'
          '<path d="M150 0 L0 150 M150 0 L40 150 M150 0 L90 150 M150 0 L0 60 M150 0 L0 110"/>'
          '<path d="M150 30 Q135 22 120 0 M150 60 Q125 45 115 30 Q100 18 90 0 M150 95 Q115 75 100 60 Q80 40 60 0 '
          'M150 130 Q105 105 85 90 Q60 65 30 0"/></svg>')

DIVIDER = ('<svg class="divider" viewBox="0 0 120 20" aria-hidden="true" fill="none" stroke="currentColor">'
           '<path d="M0 10h48M72 10h48"/><path d="M60 2v16M53 7h14" stroke-width="2"/></svg>')


def candle(size=84):
    return (f'<svg class="candle" width="{size}" height="{size}" viewBox="0 0 84 84" aria-hidden="true">'
            '<path class="flame" d="M42 10c6 9 8 14 8 18a8 8 0 0 1-16 0c0-4 2-9 8-18z" fill="#e0a040"/>'
            '<path class="flame" d="M42 20c3 5 4 7 4 9a4 4 0 0 1-8 0c0-2 1-4 4-9z" fill="#fff2c8"/>'
            '<path d="M42 36v4" stroke="#222" stroke-width="2"/>'
            '<path d="M32 40h20v34H32z" fill="#e9e2d0"/><path d="M32 40h20v4c-4 0-4 6-7 6s-2-6-6-6-4 3-7 2z" fill="#cfc6af"/>'
            '<path d="M22 74h40v5H22z" fill="#5e5b58"/></svg>')


def tombstone_icon():
    return ('<svg viewBox="0 0 84 84" aria-hidden="true"><path d="M20 76V36a22 22 0 0 1 44 0v40z" fill="#8d8a86"/>'
            '<path d="M42 28v24M33 36h18" stroke="#1b1a19" stroke-width="4"/>'
            '<path d="M8 78h68v4H8z" fill="#2d3d20"/></svg>')


def skull_icon():
    return ('<svg viewBox="0 0 84 84" aria-hidden="true"><path d="M42 10c-17 0-28 12-28 27 0 9 4 15 10 19v12h36V56'
            'c6-4 10-10 10-19 0-15-11-27-28-27z" fill="#e9e2d0"/><circle cx="31" cy="38" r="7" fill="#0b0a0c"/>'
            '<circle cx="53" cy="38" r="7" fill="#0b0a0c"/><path d="M42 46l-4 8h8z" fill="#0b0a0c"/>'
            '<path d="M32 62v6M39 62v6M45 62v6M52 62v6" stroke="#0b0a0c" stroke-width="2"/></svg>')


def page(path, title, body, *, desc, nav=None, scripts=(), body_attrs="", absolute=False):
    """Writes one page. `path` is relative to OUT; links are made relative unless absolute=True."""
    depth = len(Path(path).parts) - 1
    root = "/" if absolute else ("../" * depth or "./")
    def href(p):
        return root + p
    links = [("crypt/", "Escape the Crypt", "crypt"), ("epitaph/", "Epitaphs", "epitaph"), ("museum/", "Museum of Petty Curses", "museum")]
    nav_html = "".join(
        f'<a href="{href(u)}"{" aria-current=\"page\"" if nav == key else ""}>{label}</a>' for u, label, key in links)
    script_tags = "".join(f'<script src="{href(s) if not s.startswith("./") else s}" defer></script>' for s in ("main.js",) + tuple(scripts))
    doc = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<meta name="theme-color" content="#0b0a0c">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Ctext y='.9em' font-size='90'%3E%F0%9F%A6%87%3C/text%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,600;1,400&family=UnifrakturMaguntia&display=swap">
<link rel="stylesheet" href="{href('style.css')}">
{script_tags}
</head>
<body{body_attrs}>
{COBWEB}
<header class="site-header"><div class="wrap">
<a class="brand" href="{href('')}">{BAT}Realm of Darkness</a>
<nav class="site-nav" aria-label="Main">{nav_html}</nav>
</div></header>
<main><div class="wrap">
{body}
</div></main>
<footer class="site-footer"><div class="wrap">
<span>&copy; The Void. All souls reserved.</span>
<span><a href="{href('impressum.html')}">Impressum</a> &middot; Best viewed by candlelight</span>
</div></footer>
</body>
</html>
"""
    target = OUT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(doc, encoding="utf-8")


# ---------------------------------------------------------------- hub
page("index.html", "Realm of Darkness",
     desc="A small, gloomy corner of the internet: escape a crypt, carve your epitaph, visit the Museum of Petty Curses.",
     body=f"""
<section class="center" style="margin-top:2.5rem">
{candle(96)}
<h1>Welcome, Mortal.</h1>
<p class="lede" style="margin:0 auto">The Realm used to be busier. Now it is quiet, dusty and slightly damp, the way we like it.
Wipe your feet, mind the cobwebs, and choose a door. All of them creak.</p>
</section>
<div class="doors">
  <a class="door" href="crypt/">{tombstone_icon()}<h2>The Crypt</h2><p>You wake up in a coffin. Escape, or die trying. Mostly die trying.</p></a>
  <a class="door" href="epitaph/">{candle()}<h2>The Graveyard</h2><p>Carve your own epitaph. Last words, written in advance, for your convenience.</p></a>
  <a class="door" href="museum/">{skull_icon()}<h2>The Museum</h2><p>A collection of petty curses. Admission free. Your phone charger is still too short.</p></a>
</div>
{DIVIDER}
<p class="center muted small">Notice from the management: visitors are kindly requested not to feed the bats, wake the dead, or lick anything.</p>
""")

# ---------------------------------------------------------------- crypt
DEATHS = {
    "knock": ("Knocked politely.", "The gravedigger heard knocking, assumed it was the neighbours, and added three more shovels of earth. Manners are lovely. Oxygen is lovelier."),
    "sleep": ("Overslept eternity.", "You closed your eyes for &lsquo;just five more minutes&rsquo;. That was in 1847. Your alarm is still ringing somewhere."),
    "rat": ("Petted the rat.", "The rat was in charge. The rat has always been in charge. The rat accepted your tribute and summoned its 4,000 cousins."),
    "hat": ("Wore a skull as a hat.", "It looked fantastic. Its previous owner disagreed and wanted it back, along with yours, as compensation."),
    "swim": ("Went for a swim.", "You forgot you can't swim. Or breathe underwater. Or see in the dark. The eels gave you a 2/10 for technique."),
    "drink": ("Drank the glowing water.", "You glowed beautifully for about eleven seconds. Then you glowed not at all. Hydration is important, within reason."),
    "form": ("Filled out Form 7B.", "Form 7B (Application to Leave the Crypt) requires an attached death certificate. You obligingly produced one."),
    "coffee": ("Drank the sexton's coffee.", "It had been brewing since the Habsburgs. It was stronger than you. It was stronger than most empires."),
    "shout": ("Shouted &ldquo;Hello?&rdquo;", "Three thousand bats answered at once. Echolocation is lovely in theory. In practice it is mostly teeth."),
    "organ": ("Played the organ.", "You found the Lost Chord. It had been lost on purpose. The chapel ceiling applauded by falling on you."),
    "candle": ("Blew out the last candle.", "You made a wish. The darkness granted it, technically. Be careful what you wish for in a crypt."),
    "lick": ("Licked the iron gate.", "It was a dare. Nobody dared you. You are now a permanent fixture, attached at the tongue, waiting for spring."),
}
TOTAL = len(DEATHS)

ROOMS = {
    "index.html": ("The Coffin", "Chapter I",
        """<p>You wake up. It is dark. It is cramped. It smells of pine, damp earth and somebody else's grandmother.</p>
<p>You stretch out a hand and touch wood. Above you. Beside you. Everywhere. Ah. A <em>coffin</em>.
On the bright side, the craftsmanship is excellent, and somebody tucked a little pillow under your head.</p>""",
        [("Push the lid with all your might", "ossuary.html"),
         ("Knock politely and wait", "death-knock.html"),
         ("This is fine. Go back to sleep", "death-sleep.html")]),
    "ossuary.html": ("The Ossuary", "Chapter II",
        """<p>The lid gives way with a groan that sounds like a cello falling down stairs. You climb out into a long, low vault.
The walls are made of skulls, stacked neatly, thousands of them, all grinning as if they know something you don't. They do.</p>
<p>A fat rat sits on a femur, watching you with the calm of an accountant. Somewhere to the left, water drips.
To the right, a narrow staircase climbs towards a flickering light.</p>""",
        [("Talk to the skulls", "skulls.html"),
         ("Pet the rat. Look at him. He's so round", "death-rat.html"),
         ("Borrow a skull and wear it as a hat", "death-hat.html"),
         ("Follow the dripping sound", "tunnel.html"),
         ("Climb the staircase towards the light", "office.html")]),
    "skulls.html": ("The Skulls Speak", "Chapter II &frac12;",
        """<p>You clear your throat. &ldquo;Excuse me&hellip;&rdquo;</p>
<p>A skull in the third row sighs. &ldquo;Finally, someone with manners. I'm Yorick. No, not <em>that</em> Yorick, everyone asks.
Listen, we've watched a lot of people try to get out. Mostly they didn't. Some advice:&rdquo;</p>
<ul>
<li>&ldquo;Never trust the rat. The rat runs this place.&rdquo;</li>
<li>&ldquo;The sexton upstairs locks the gate and keeps the key on a hook. He also keeps <em>coffee</em>. Don't.&rdquo;</li>
<li>&ldquo;The bats in the chapel know the way out. Be quiet around them. Very quiet.&rdquo;</li>
<li>&ldquo;And the old organ has a pedal nobody ever plays. Nobody knows why. Spooky, eh?&rdquo;</li>
</ul>
<p>&ldquo;Now off you go. And if you die, the third row has a vacancy. Lovely view.&rdquo;</p>""",
        [("Thank Yorick and go back", "ossuary.html")]),
    "tunnel.html": ("The Flooded Tunnel", "Chapter III",
        """<p>The dripping leads you into a tunnel half-full of black water. Something in it glows a cheerful, radioactive green.
Something else in it moves. You decide not to think about the something else.</p>
<p>A slimy ledge runs along the wall. It looks treacherous, but in a responsible, adult sort of way.</p>""",
        [("Swim across. How hard can it be?", "death-swim.html"),
         ("You're thirsty. Drink the glowing water", "death-drink.html"),
         ("Edge carefully along the ledge", "chapel.html"),
         ("Retreat to the ossuary", "ossuary.html")]),
    "office.html": ("The Sexton's Office", "Chapter IV",
        """<p>At the top of the stairs is a cramped office lit by a single oil lamp. Ledgers are piled to the ceiling.
A sign reads: <em>&ldquo;Office hours: Midnight to 00:01. Complaints: none received since 1312.&rdquo;</em></p>
<p>The sexton himself is asleep in his chair, snoring like a cathedral door. On his desk: a stack of forms, and a pot of coffee
of truly geological darkness. Behind him, on a hook, hangs a large iron key. A small door beside it is marked <em>&ldquo;Gate&rdquo;</em>.</p>""",
        [("Fill out a form. Do things properly", "death-form.html"),
         ("Pour yourself a cup of that coffee", "death-coffee.html"),
         ("Tiptoe past, take the key, and slip through the little door", "gate-key.html"),
         ("Go back down to the ossuary", "ossuary.html")]),
    "chapel.html": ("The Bat Chapel", "Chapter V",
        """<p>The ledge ends in a tiny chapel. The ceiling is alive: thousands of bats hang there like a velvet curtain, breathing softly.
A single candle burns on the altar, the only light left in the whole crypt.</p>
<p>In the corner stands an ancient organ, its keys yellow as old teeth. Down by your feet, one dusty
<a class="secret" href="secret.html">pedal</a> looks as if nobody has touched it in centuries.
A cool draught flows from a passage on the far side. A few bats flutter quietly in that direction.</p>""",
        [("Shout &ldquo;Hello? Anyone?&rdquo;", "death-shout.html"),
         ("Play something on the organ", "death-organ.html"),
         ("Blow out the candle and make a wish", "death-candle.html"),
         ("Follow the bats, very quietly", "gate.html"),
         ("Go back along the ledge", "tunnel.html")]),
    "gate.html": ("The Gate", "Chapter VI",
        """<p>The bats lead you to a heavy iron gate. Beyond it: moonlight, fresh air, the faint sound of people laughing.
It is locked, of course. A small enamel sign reads: <em>&ldquo;EXIT. Keys at the sexton's office. No loitering.&rdquo;</em></p>
<p>The bars glisten with frost. They look oddly&hellip; lickable.</p>""",
        [("Lick the gate. For science", "death-lick.html"),
         ("Trudge all the way back to the ossuary", "ossuary.html")]),
    "gate-key.html": ("The Gate, With a Key", "Chapter VI",
        """<p>The little door opens onto a short corridor, and at its end: a heavy iron gate. Beyond it, moonlight and fresh air.
The key in your hand is cold and heavy and wonderful.</p>
<p>The bars glisten with frost. They still look oddly&hellip; lickable.</p>""",
        [("Unlock the gate", "escape.html"),
         ("Lick the gate first. You've come this far", "death-lick.html")]),
}

ENDINGS = {
    "escape.html": ("Freedom!", "The End",
        """<p>The key turns with a satisfying <em>clunk</em>. The gate swings open. You stagger out into the night, covered in dust,
cobwebs and a light dusting of somebody else.</p>
<p>It is the 31st of October. The street is full of people dressed as ghosts, zombies and vampires.
&ldquo;Amazing costume!&rdquo; someone shouts. &ldquo;So realistic! How did you get the grave smell?&rdquo;
You win the costume contest. The prize is a pumpkin. You have never been happier.</p>
<p class="muted">You escaped the crypt. The skulls are mildly impressed.</p>"""),
    "secret.html": ("The Secret Ending", "The Other End",
        """<p>You press the dusty pedal. Somewhere deep in the walls, a great mechanism wheezes. The organ slides aside,
revealing a warm, candlelit lounge. There are armchairs. There is a fireplace. There is <em>tea</em>.</p>
<p>A dozen ghosts look up from their card game. &ldquo;Oh, finally,&rdquo; says one. &ldquo;We've needed a fourth for bridge since 1703.&rdquo;
The rat brings you a biscuit. He is, it turns out, a gracious host.</p>
<p>You never leave the crypt. You never want to. You are appointed the new Keeper of the Realm, with a lovely
pension and dental, although you no longer strictly have teeth.</p>
<p class="muted">You found the secret ending. Tell no one. (Tell everyone.)</p>"""),
}


def choices_html(choices):
    return '<ul class="choices">' + "".join(f'<li><a href="{h}">{t}</a></li>' for t, h in choices) + "</ul>"


COUNTER = f'<p class="counter" data-death-counter data-total="{TOTAL}" hidden></p>'

for fname, (title, kicker, text, choices) in ROOMS.items():
    extra = ""
    if fname == "index.html":
        extra = '<p class="muted small">A tiny text adventure. No saving, no inventory, no mercy. Choose wisely, or at least entertainingly.</p>'
    page(f"crypt/{fname}", f"{html.unescape(title)}: Escape the Crypt" if fname != "index.html" else "Escape the Crypt",
         desc="Escape the Crypt: a small, dark, silly text adventure.", nav="crypt",
         body=f"""<article class="room">
<p class="room-kicker">{kicker}</p>
<h1>{title}</h1>
{extra}
{text}
{choices_html(choices)}
{COUNTER if fname == 'index.html' else ''}
</article>""")

for fname, (title, kicker, text) in ENDINGS.items():
    page(f"crypt/{fname}", f"{title}: Escape the Crypt", desc="Escape the Crypt: an ending.", nav="crypt",
         body=f"""<article class="room center">
<p class="room-kicker">{kicker}</p>
<h1>{title}</h1>
{candle(96)}
<div style="text-align:left">{text}</div>
{COUNTER}
<p class="row" style="justify-content:center;margin-top:1.5rem"><a class="btn" href="index.html">Play again</a> <a class="btn ghost" href="../">Back to the Realm</a></p>
</article>""")

for key, (cause, text) in DEATHS.items():
    page(f"crypt/death-{key}.html", f"You Died: Escape the Crypt", desc="Escape the Crypt: you died.", nav="crypt",
         body_attrs=f' data-death="{key}"',
         body=f"""<article class="room center">
<p class="room-kicker">You died</p>
<div class="stone"><p class="rip">R.I.P.</p><p class="cause">{cause}</p><p class="dates">BORN: YES &middot; DIED: JUST NOW</p></div>
<div class="grass"></div>
<p>{text}</p>
{COUNTER}
<p class="row" style="justify-content:center;margin-top:1.5rem"><a class="btn" href="index.html">Rise again</a> <a class="btn ghost" href="../">Stay dead (go home)</a></p>
</article>""")

# ---------------------------------------------------------------- museum
CURSES = [
    ("The Short Charger Cable", "c. 2007", 3, "Always exactly 20&nbsp;cm too short to reach the bed. Scientists have tried longer cables. The curse adapts."),
    ("The Wobbly Shopping Cart", "Medieval period", 2, "Of all the carts in the row, you will choose the one with the haunted wheel. It wants to go left. It always wants to go left."),
    ("Eternal 1% Battery", "2011", 4, "Your phone reaches 1% at the precise moment you need the map. It then lasts exactly long enough to show you how lost you are."),
    ("The Song Stuck in Your Head", "Prehistoric", 3, "Not a good song. Never a good song. Usually a jingle for a furniture store that closed in 1998."),
    ("The Sock Abyss", "Since the invention of socks", 3, "Two socks enter the washing machine. One sock leaves. Where the other goes, no living mortal knows."),
    ("The USB Stick, Upside Down", "1996", 2, "Inserted wrong. Flipped. Still wrong. Flipped again. Correct. This exhibit has been rotated three times by the curator."),
    ("The Slowest Queue", "Ancient Egypt", 3, "Whichever queue you join becomes the slowest. Switching queues transfers the curse with you, like a loyal, terrible dog."),
    ("The Elevator Goodbye", "1890s", 2, "You say goodbye to a colleague. You both walk the same direction. You meet again at the lift. Nobody knows what to say. Forever."),
    ("The Phantom Vibration", "2009", 1, "Your phone buzzed in your pocket. It did not. It never does. The phone is in the other room."),
    ("The Lego Underfoot", "1958", 4, "Laid by unseen hands at the exact spot your bare foot will land at 3&nbsp;a.m. Exhibit behind glass for visitor safety."),
    ("The Unopenable Packet", "Industrial Revolution", 2, "&lsquo;Tear here.&rsquo; You tear there. Nothing tears. You resort to teeth, scissors and, eventually, prayer."),
    ("The Reply-All", "1971", 4, "One person replies all. Twelve people reply all asking to be removed. The curse feeds on every message."),
    ("The Name You Forgot", "Since names", 3, "They remember yours. They use it warmly. It is far too late to ask theirs. You will pretend for the next eleven years."),
    ("The Hot Side of the Pillow", "Classical antiquity", 2, "You flip the pillow to the cool side. Within seconds it, too, becomes the hot side. There is no cool side. There never was."),
    ("The Bus That Leaves", "1830s", 3, "Departs the very moment you arrive at the stop, close enough to see the driver's face. The driver smiles. The driver knows."),
    ("The Tangled Earphones", "1979", 2, "Placed neatly in a pocket. Removed as a single cursed knot of Gordian complexity. Wireless earphones replaced this with Curse No.&nbsp;19."),
    ("The Restaurant Order Envy", "Roman era", 1, "Your food arrives. It is fine. Then their food arrives, and you understand you have chosen wrong. You always will."),
    ("The Update Required", "1995", 3, "Your device must update right now. It will take 47 minutes. It will change one icon, slightly, for the worse."),
    ("The Lost Single Earbud", "2016", 3, "One earbud, gone. Possibly in the sofa. Possibly in the Sock Abyss (see No.&nbsp;5). Possibly ascended."),
    ("The Spoon in the Disposal", "1940s", 2, "Something is in the sink. It is always a spoon. It is always there. The spoon is the true owner of your kitchen."),
    ("The Cold Coffee", "17th century", 2, "Made with love. Set down for just a second. Discovered stone cold 40 minutes later. The second cup will suffer the same fate."),
    ("The Inconvenient Sneeze", "Since noses", 1, "Arrives only during silence: at funerals, exams, job interviews and the quiet bit of a film."),
    ("The Password Requirements", "2003", 4, "Must contain a capital, a number, a symbol, a rune and a drop of blood. Must not resemble any password you can remember."),
    ("The Stair That Isn't There", "Gothic period", 3, "In the dark, your foot finds a stair that does not exist. Your heart leaves your body briefly. It returns, but changed."),
    ("The Gift of Socks", "Victorian era", 1, "Not technically a curse. Just a lifelong, gentle disappointment. Kept in the museum for its dark sentimental value."),
]


def skulls(n):
    return ('<span class="skulls" aria-label="Severity ' + str(n) + ' of 5">' +
            "&#9760;" * n + '<span class="off">' + "&#9760;" * (5 - n) + "</span></span>")


cards = "".join(
    f'<article class="exhibit" id="no-{i}"><div class="no">Exhibit No. {i}</div><h3>{t}</h3>'
    f'<p class="meta">Discovered: {d} &middot; <span style="white-space:nowrap">Severity {skulls(s)}</span></p><p>{n}</p></article>'
    for i, (t, d, s, n) in enumerate(CURSES, 1))

options = "".join(f'<option value="{i}">{t}</option>' for i, (t, _, _, _) in enumerate(CURSES, 1))

page("museum/index.html", "Museum of Petty Curses", nav="museum", scripts=("museum/curses.js", "museum/museum.js"),
     desc="A museum of small, everyday curses: the short charger cable, the sock abyss, the eternal 1% battery and more.",
     body=f"""<section style="margin-top:1.5rem">
<h1>The Museum of Petty Curses</h1>
<p class="lede">Not every curse is dramatic. Most don't involve pharaohs or cursed rings. Most are small, petty and
unbearably persistent. Here we collect, catalogue and display them, so that you may know your enemy.</p>
</section>
<section class="panel cotd" id="cotd" hidden>
<h2>Curse of the Day</h2>
<p class="muted small" id="cotd-date"></p>
<h3 id="cotd-title"></h3>
<p id="cotd-note"></p>
</section>
<h2>The Collection</h2>
<p class="muted">Please do not touch the exhibits. Several of them are already touching you.</p>
<div class="exhibits">{cards}</div>
<h2 id="curse-a-friend">Curse a Friend (Mildly)</h2>
<div class="panel">
<p>Bestow an official certificate of mild cursing upon someone deserving. Completely harmless. Mostly.</p>
<form id="curse-form" action="certificate.html" method="get">
<div class="field"><label for="to">Name of the cursed</label><input type="text" id="to" name="to" maxlength="40" required placeholder="e.g. Klaus from accounting"></div>
<div class="field"><label for="curse">Curse</label><select id="curse" name="curse">{options}</select></div>
<div class="row"><button type="submit">Issue certificate</button> <button type="button" class="ghost" id="curse-random">Let fate decide</button></div>
</form>
</div>
<p class="giftshop">Thank you for visiting. Please exit through the crypt. The gift shop sells charger cables, 20&nbsp;cm too short.</p>
""")

page("museum/certificate.html", "Certificate of Mild Cursing", nav="museum", scripts=("museum/curses.js", "museum/museum.js"),
     desc="An official certificate of mild cursing from the Museum of Petty Curses.",
     body="""<div class="certificate" id="certificate">
<p class="small" style="margin:0;letter-spacing:.15em">THE MUSEUM OF PETTY CURSES</p>
<h1>Certificate of Mild Cursing</h1>
<p>Be it known throughout the Realm that</p>
<p class="to" id="cert-to">Somebody</p>
<p>has been officially and irrevocably afflicted with</p>
<p class="curse-name" id="cert-curse">The Short Charger Cable</p>
<p class="small" id="cert-note"></p>
<p class="small" id="cert-date"></p>
<div class="seal" aria-hidden="true">RoD</div>
<p class="small" style="margin-top:1.4rem">This curse is petty, harmless, and non-refundable.<br>
<a href="index.html#curse-a-friend">Curse someone else</a> &middot; <a href="index.html">Visit the museum</a></p>
</div>""")

(OUT / "museum").mkdir(parents=True, exist_ok=True)
(OUT / "museum/curses.js").write_text(
    "/* Generated: the museum's catalogue. Index 0 = Exhibit No. 1. */\nwindow.ROD_CURSES = " +
    json.dumps([{"title": html.unescape(t), "found": d, "severity": s, "note": html.unescape(n)} for t, d, s, n in CURSES],
               ensure_ascii=False, indent=1) + ";\n", encoding="utf-8")

# ---------------------------------------------------------------- epitaph
TAGS = [("coffee", "coffee"), ("cats", "cats"), ("beer", "&ldquo;hold my beer&rdquo;"), ("gym", "the gym"),
        ("plants", "houseplants"), ("tv", "one more episode"), ("work", "spreadsheets"), ("phone", "the phone")]
tag_html = "".join(f'<label><input type="checkbox" name="tags" value="{v}"> {l}</label>' for v, l in TAGS)

page("epitaph/index.html", "Epitaph Generator", nav="epitaph", scripts=("epitaph/epitaph.js",),
     desc="Carve your own funny epitaph on a tombstone and download it as an image.",
     body=f"""<section style="margin-top:1.5rem">
<h1>The Epitaph Generator</h1>
<p class="lede">Why leave your last words to chance, or worse, to your relatives? Carve them now, while you still have fingers.</p>
</section>
<div class="epitaph-grid">
<form id="epitaph-form" class="panel" action="./" method="get">
<div class="field"><label for="name">Name of the departed</label><input type="text" id="name" name="name" maxlength="28" required placeholder="Your name, or someone else's"></div>
<fieldset class="tags"><legend>Known weaknesses (optional)</legend>{tag_html}</fieldset>
<div class="row"><button type="submit">Carve it</button> <button type="button" class="ghost" id="reroll" disabled>Reroll</button></div>
<noscript><p class="muted small">The stonemason needs JavaScript. He is old-fashioned in every other way.</p></noscript>
</form>
<div>
<svg id="stone-svg" viewBox="0 0 400 480" role="img" aria-labelledby="stone-title"><title id="stone-title">A tombstone</title></svg>
<div class="row" style="justify-content:center;margin-top:1rem">
<button type="button" id="download" disabled>Download PNG</button>
<button type="button" class="ghost" id="share" disabled>Copy link</button>
</div>
<p class="share-out center" id="share-out" aria-live="polite"></p>
</div>
</div>
""")

# ---------------------------------------------------------------- 404 & impressum
page("404.html", "Page Not Found", absolute=True,
     desc="This page has passed on.",
     body=f"""<section class="center" style="margin-top:2rem">
<div class="stone"><p class="rip">404</p><p class="cause">This page has passed on.</p><p class="dates">IT WAS LOVED &middot; BRIEFLY</p></div>
<div class="grass"></div>
<p class="lede" style="margin:0 auto">We have searched the crypt, the ossuary and the sock abyss. It is gone.
No flowers, please. It would have wanted you to <a href="/">go back to the start</a>.</p>
</section>""")

page("impressum.html", "Impressum",
     desc="Impressum for realm-of-darkness.at.",
     body="""<section style="margin-top:1.5rem">
<h1>Impressum</h1>
<div class="panel">
<p><strong>Contact:</strong> <a href="mailto:office@realm-of-darkness.at">office@realm-of-darkness.at</a></p>
<p>Private, non-commercial website. All content is fiction and satire.</p>
<p>No cookies, no tracking. Hosted on GitHub Pages; fonts from Google Fonts.</p>
</div>
<p class="muted small">The management accepts no responsibility for curses, hauntings, or charger cables that are too short.</p>
</section>""")

print("built", sum(1 for _ in OUT.rglob("*.html")), "pages")
