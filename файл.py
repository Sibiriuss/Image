from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from PIL import Image
import io
import logging

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Привет! Отправь мне изображение, и я изменю его размер до 512x512.')

def process_image(update: Update, context: CallbackContext) -> None:
    # Получаем файл изображения
    file = update.message.photo[-1].get_file() if update.message.photo else update.message.document.get_file()
    
    # Загружаем изображение в память
    img_data = io.BytesIO()
    file.download(out=img_data)
    img_data.seek(0)
    
    # Открываем изображение с помощью Pillow
    img = Image.open(img_data)
    
    # Изменяем размер до 512x512 (без сжатия, если исходное меньше)
    img.thumbnail((512, 512))
    
    # Сохраняем изображение в буфер
    output = io.BytesIO()
    img.save(output, format='PNG')  # Можно изменить на 'JPEG' и т.д.
    output.seek(0)
    
    # Отправляем обратно
    update.message.reply_photo(photo=output, caption="Готово! Размер изменен до 512x512.")

def error_handler(update: Update, context: CallbackContext) -> None:
    logger.error(f'Ошибка при обработке сообщения: {context.error}')
    update.message.reply_text('Произошла ошибка при обработке изображения.')

def main() -> None:
    # Замените 'YOUR_BOT_TOKEN' на токен вашего бота
    updater = Updater("7660847934:AAH16PT0ECVOCVzTSTkdXT4ucEhD8L1u6Ck", use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.photo | Filters.document.image, process_image))
    dp.add_error_handler(error_handler)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()