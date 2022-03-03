
# SubitoScalper2

This bot will check subito.it for new listings and send updates via Telegram


## Deployment

We are going to use Docker to deploy the bot

```bash
  docker run \
    -d \
    --name subito.it-bot \
    -e CHATID=<AUTHORIZED_USER_CHAT_ID_HERE> \
    -e APIKEY=<TELEGRAM_BOT_API_KEY_HERE> \
    --restart unless-stopped \
    almanni/subitotgbot
```


## How to build

First, we need to clone the repository
```bash
  git clone https://github.com/AlManni/SubitoScalper2
```
Then, cd into the repo we just cloned
```bash
  cd SubitoScalper2/
```
Now we are going to build the image
```bash
  docker build -t subitotgbot .
```

