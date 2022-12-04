<h1 align="center">
  Polus Discord Bot
  <br>
</h1>

<p align="center">
  <a href="https://www.python.org/downloads/">
    <img src="https://img.shields.io/pypi/pyversions/py-cord" alt="python version">
  </a>
  <a href="https://pypi.org/project/py-cord/">
     <img alt="py-cord" src="https://img.shields.io/badge/py-cord-blue.svg">
  </a>
  <a href="https://paypal.me/nostorian">
    <img alt="paypal" src="https://img.shields.io/badge/support-me!-red.svg">
  </a>

<p align="center">
  <a href="#overview">Overview</a>
  •
  <a href="#self-hosting">Self Hosting</a>
  •
  <a href="#original-project">Original Project</a>
</p>

# Overview
Polus is a really cool bot which has got amazing moderation features and much more. The bot is completely coded in Python utilizing the py-cord API. This is a *self-hosted bot* meaning you will need to host and maintain your own instance, instructions for self-hosting are given below. You can contact me at my [telegram](https://t.me/nostorian) or open an [issue](https://github.com/Nostorian/Polus-Discord-Bot/issues) if you face any problems with self-hosting.

# Self Hosting
**Currently only Windows Installation or deploying the project on [Railway](https://railway.app) is supported.**
## Windows Installation
1. Download the [source code](https://github.com/Nostorian/Polus-Discord-Bot/archive/refs/heads/main.zip) and [python](https://www.python.org/downloads/)
2. Unzip the file with either [WinRAR](https://www.win-rar.com/) or [7-Zip](https://www.7-zip.org/download.html)
3. Rename env.text to .env and fill all the values of the .env file and config.json as well.
5. Install all required modules with `pip install -r requirements.txt`
6. Execute the bot with `python main.py`
❗ NOTE: If you face an error like `Microsoft Visual C++ 14.0 or greater is required`, install the build tools from [here](https://visualstudio.microsoft.com/visual-cpp-build-tools).
### All .env and config.json values explained...

1. TOKEN, to get your discord bot token follow this [guide](https://www.writebots.com/discord-bot-token/), **also enable the `message content` intent from the bot tab in your developer portal as it will be required for certain features of the bot.**
2. POSTGRESQL_URL, to get this you need install [postgresql](https://www.postgresql.org/) in your computer or check out postgresql online hosting methods on your own.
3. WEBHOOK LOGGER, create a private server since most of the owner command loggings will be sent via this webhook and its suggested to keep it private for security reasons, to get your webhook url check out this [guide](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks)
4. owner id, to get this check out this [guide](https://www.remote.tools/remote-work/how-to-find-discord-id)
5. success emoji and error emoji, really man? just download emojis from emojis folder and upload to ur guild get their syntax and paste it in the respective fields.
## Railway Installation
coming soon...

# Original Project
This bot is a recreation of https://nukebot.org and I thank the developer for giving permission to remake his project without any fuss. Do checkout the original project as well. If you dont like to self host your own version, you can invite the [public bot](https://discord.com/oauth2/authorize?client_id=1003543331919376504&permissions=285698135&scope=bot%20applications.commands)

