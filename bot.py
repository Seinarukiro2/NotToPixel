import io
import os
from dotenv import load_dotenv
from PIL import Image
from telegram import Update, InputFile
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from settings import DEFAULT_PIXEL_SIZE, DEFAULT_COLORS

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")


def process_image(image: Image.Image, pixel_size: int, colors: int) -> io.BytesIO:
    hsv_image = image.convert("HSV")
    hue, saturation, value = hsv_image.split()
    threshold = 180
    saturation = saturation.point(lambda x: 255 if x > threshold else x)
    hsv_image = Image.merge("HSV", (hue, saturation, value))
    img = hsv_image.convert("RGB")
    size = img.size

    new_size = (size[0] * pixel_size // max(size), size[1] * pixel_size // max(size))

    img = img.convert("RGB").convert("P", palette=Image.ADAPTIVE, colors=colors)
    img = img.resize(new_size, resample=Image.NEAREST).quantize(
        colors=256, dither=Image.Dither.FLOYDSTEINBERG
    )

    img = img.resize(size, resample=Image.NEAREST)

    output = io.BytesIO()
    img.convert("RGB").save(output, format="PNG")
    output.seek(0)
    return output


async def start(update: Update, context) -> None:
    message = (
        "*Hello!*\n\n"
        "Send me an image with the command `!pix` and I will turn it into pixel art.\n\n"
        "*Default Settings:*\n"
        "- Pixel grid size: 64px\n"
        "- Number of colors: 32\n\n"
        "For more info, visit our [Support Channel](https://t.me/+2puk8tnjWRA4NmQy).\n\n"
        "*Dev - @tondirt*"
    )
    await update.message.reply_text(
        message, parse_mode="Markdown", disable_web_page_preview=True
    )


# Обработчик изображений с командой !pix
async def handle_image(update: Update, context) -> None:
    if update.message.caption and update.message.caption.lower().startswith("!pix"):
        file = await update.message.photo[-1].get_file()
        image_stream = io.BytesIO()
        await file.download_to_memory(image_stream)
        image_stream.seek(0)

        img_raw = Image.open(image_stream)
        processed_image = process_image(img_raw, DEFAULT_PIXEL_SIZE, DEFAULT_COLORS)

        await update.message.reply_photo(
            photo=InputFile(processed_image, filename="pixel_art.png")
        )


def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(
        MessageHandler(filters.PHOTO & filters.Caption(), handle_image)
    )

    application.run_polling()


if __name__ == "__main__":
    main()
