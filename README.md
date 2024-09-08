
# NotToPixel - Convert your images to pixel art for NotPixel 

This Telegram bot converts images into pixel art. It uses customizable settings for pixel grid size and color count.
Features

    Convert Images: Send an image with the command !pix, and the bot will transform it into pixel art.
    Customizable Settings: The default pixel grid size is 64 pixels, and the number of colors is 32. These can be adjusted in the code if needed.
    Image Processing: The bot processes the image by adjusting saturation, resizing it to a pixelated version, and converting it back to the original size.

Commands

    /start: Sends a welcome message with instructions on how to use the bot.

How to Use

    Start the Bot: Type /start to receive a welcome message.
    Send an Image: Send an image with the caption !pix. The bot will respond with the pixelated version of the image.

Setup

    Install dependencies:
    pip install python-dotenv pillow python-telegram-bot

    



Create a .env file in the project root with the following content:



TELEGRAM_TOKEN=your_bot_token_here

Run the bot:



    python bot.py



