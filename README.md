
# subito-tracker-telegram

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

