# Put the bot online — free, 24/7, no credit card

The bot will run **every hour by itself**, on GitHub's computers, forever, for
free. Your PC can be off.

There is no payment step anywhere in this. GitHub Actions is free and unlimited
on public repositories, and it does not ask for a card.

**Your part takes about 5 minutes.** I cannot make the account for you — that is
the one thing I am not allowed to do — so those steps are yours. Everything else
is already built.

---

## Step 1 — GitHub account

Go to <https://github.com/signup>. Email, password, username. No card.

If you already have one, skip this.

## Step 2 — Make an empty repository

1. Go to <https://github.com/new>
2. **Repository name:** `hourly-bot`
3. **Set it to PUBLIC.** This matters — public repos get unlimited free
   minutes, private ones get 2,000/month and the bot would stop about
   three weeks in.
4. Do **not** tick "Add a README"
5. Click **Create repository**

Copy the address it shows you. It looks like:
`https://github.com/YOURNAME/hourly-bot.git`

## Step 3 — Send the bot up

Double-click **`push-to-github.bat`** in this folder.

It asks for that address, then uploads everything. GitHub will ask you to sign
in the first time — a browser window opens, you approve, done.

## Step 4 — Switch it on

1. Open your repository on GitHub
2. Click the **Actions** tab
3. If it asks, click **"I understand my workflows, go ahead and enable them"**
4. Click **hourly-bot** on the left, then **Run workflow** to start the first
   one immediately instead of waiting for the hour

From then on it runs at 7 minutes past every hour, on its own.

## Step 5 (optional) — get it on your phone

If you want a Telegram message on every trade:

1. In your repo: **Settings → Secrets and variables → Actions → New repository secret**
2. Add `TELEGRAM_TOKEN` — the token from @BotFather
3. Add `TELEGRAM_CHAT_ID` — your numeric id

The bot picks them up automatically. Without them it just runs quietly.

### What you can do from Telegram

Buttons appear above the text box. Most of them only report:

| | |
|---|---|
| **Status** | equity, and every open trade with its live profit |
| **Charts** | one price chart per open trade — entry, stop, where it is now |
| **P&L** | live profit, and how much room is left before each stop |
| **Closest** | which coin is nearest to triggering, and what is blocking it |
| **Trades** | recent finished trades |

**Close** is the one that changes something. It lists the open trades; tapping
one exits it at market straight away, instead of waiting for the trailing stop.

**Or just double-tap a chart.** Any reaction added to a position chart closes
that position. It is built for the moment you look at the picture and decide
you want out, so it acts immediately with no confirmation step. Taking a
reaction off does nothing — undoing a mis-tap cannot close a second trade, but
the first one has already gone.

Both routes go through freqtrade's own API rather than touching the database,
so the bot places the exit order itself and stays in step with its own records.
That API listens only on 127.0.0.1 inside GitHub's runner and its password is
minted fresh every run — there is nothing extra to configure and **no new
secret to add**.

Between runs the bot is not there to close anything, and it says so rather than
failing silently.

---

## How to check on it

**Actions tab → click any run → "Show what happened"**

That prints the last log lines and every trade, like this:

```
#3   CLOSED SHORT SOL/USDT:USDT    pnl -0.0421 (stop_loss)
#4   OPEN   LONG  LINK/USDT:USDT   entry 11.84

closed trades: 3   realised P/L: -0.0912 USDT
```

Green tick = it ran. Red X = something broke, and the log says what.

## Things worth knowing

- **It is paper money.** $20 simulated, real Bybit prices. There are no API keys
  in this repository and it cannot place a real order. That is also why it is
  safe for the repo to be public — there is nothing secret in it.
- **A run taking ~6 minutes then stopping is normal.** The bot is designed to
  never exit; the workflow gives it six minutes to do the hour's work and then
  ends it. The log line saying `timeout` is expected, not an error.
- **Its memory lives in the repo.** After each run it commits
  `user_data/live_cloud.sqlite`, which is how it remembers open trades between
  hours. You will see an hourly commit from "hourly-bot" — that is correct.
- **GitHub switches off schedules in repos with 60 days of no activity.** The
  bot's own hourly commits normally prevent this, but if it ever goes quiet,
  press **Run workflow** once and it resumes.
- **Cron can run late.** GitHub queues scheduled jobs; a run may start 5-20
  minutes after the hour when their servers are busy. On an hourly strategy this
  costs almost nothing.
