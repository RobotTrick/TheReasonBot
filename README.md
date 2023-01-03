<img src="https://telegra.ph/file/5616a5ec2d6a0a5303741.png" width="100" height="100">

# The Reason Bot

### Telegram bot that saves a blocking reason when kicking a user from the group

Every group admin occasionally encounters a user seeking to release his block from the group, but in the vast majority of cases, and especially in large groups with multiple admins, there is no way to remember the reason for the block. The following bot will solve this problem for you!

_You can check our bot [here](https://t.me/TheReasonBot) (in Hebrew)._

## configuration:
- Clone this reposetory:
```
git clone https://github.com/RobotTrick/TheReasonBot.git
```
- Install requirements:
```
pip3 install -r requirements.txt
```
- Edit and insert the folowing values into the [config](/config.ini) file:
```
[pyrogram]
api_id = XXXXXXXXXXX
api_hash = XXXXXXXXXXXXXXXXXXXXXXXXXX
bot_token = XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```
The ``api_id`` & ``api_hash`` You can get from [my.telegram.org](https://my.telegram.org). ``bot_token`` you can get by create new bot on [BotFather](https://t.me/BotFather).
- Edit bot strings:

You can change, if you like, the bot strings: start and help messages, buttons and more by editing the [Msg.py](/Msg.py) file.
- Run the bot:
```
python3 main.py
```
---
![]()
Created with ❤️ by [David Lev](https://davidlev.me) & [Yehuda By](https://yeudaby.com)
