import json
from telegram import ReplyKeyboardRemove
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
)
from database.db import SessionLocal
from sqlalchemy.orm import Session
from database.models import User
import logging
from config.logging_config import setup_logging


logger = logging.getLogger(__name__)

# Define a state for the ConversationHandler
REMOVE_PREFERENCE = 19

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ContextTypes, ConversationHandler
import json
from database.models import User
from database.db import SessionLocal

async def handle_check_preferences(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Обрабатывает команду "Check preferences".
    Извлекает предпочтения пользователя и отображает их с кнопками "Remove".
    """
    setup_logging()

    user = update.effective_user
    if not user:
        await update.message.reply_text("Не удалось определить пользователя.")
        return ConversationHandler.END

    with SessionLocal() as session:
        existing_user = session.query(User).filter(User.telegram_id == user.id).first()

        if not existing_user:
            await update.message.reply_text("Пользователь не найден в базе данных.")
            return ConversationHandler.END

        preferences_text = existing_user.preferences

    try:
        preferences = json.loads(preferences_text) if preferences_text else []
        if not isinstance(preferences, list):
            raise ValueError
    except (json.JSONDecodeError, ValueError):
        await update.message.reply_text(
            "Данные ваших предпочтений повреждены или имеют неправильный формат."
        )
        return ConversationHandler.END

    if not preferences:
        await update.message.reply_text("У вас нет установленных предпочтений.")
        return ConversationHandler.END

    # Удаляем клавиатуру
    await update.message.reply_text(
        "Ищу хуйню:",
        reply_markup=ReplyKeyboardRemove()  # Удаляет клавиатуру
    )

    # Создаём инлайн-кнопки для каждого предпочтения
    keyboard = []
    for idx, preference in enumerate(preferences, start=1):
        button = InlineKeyboardButton(
            text=f"Remove '{preference}'",
            callback_data=f"remove_pref:{idx - 1}",  # Используем индекс для идентификации
        )
        keyboard.append([button])

    reply_markup = InlineKeyboardMarkup(keyboard)

    # Отправляем сообщение с предпочтениями и инлайн-кнопками
    await update.message.reply_text(
        "Here are your preferences. Click 'Remove' to delete any preference:",
        reply_markup=reply_markup
    )

    return ConversationHandler.END  # Завершаем разговор; коллбэки обрабатываются отдельно

async def remove_preference_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Обрабатывает коллбэк при нажатии пользователем на кнопку "Remove" для предпочтения.
    Удаляет выбранное предпочтение из базы данных и обновляет сообщение.
    """
    query = update.callback_query
    await query.answer()  # Подтверждаем коллбэк, чтобы убрать индикатор загрузки

    user = query.from_user
    if not user:
        await query.edit_message_text("Не удалось определить пользователя.")
        return

    data = query.data
    if not data.startswith("remove_pref:"):
        await query.edit_message_text("Неверное действие.")
        return

    try:
        pref_index = int(data.split(":")[1])
        logger.info(f"Индекс предпочтения для удаления: {pref_index}")
    except (IndexError, ValueError):
        await query.edit_message_text("Неверный выбор предпочтения.")
        return

    with SessionLocal() as session:
        existing_user = session.query(User).filter(User.telegram_id == user.id).first()

        if not existing_user:
            await query.edit_message_text("Пользователь не найден в базе данных.")
            return

        preferences_text = existing_user.preferences

        try:
            preferences = json.loads(preferences_text) if preferences_text else []
            if not isinstance(preferences, list):
                raise ValueError
            logger.info(f"Текущие предпочтения пользователя: {preferences}")
        except (json.JSONDecodeError, ValueError):
            await query.edit_message_text(
                "Данные ваших предпочтений повреждены или имеют неправильный формат."
            )
            return

        if pref_index < 0 or pref_index >= len(preferences):
            await query.edit_message_text("Выбранное предпочтение не существует.")
            return

        removed_pref = preferences.pop(pref_index)
        logger.info(f"Удалено предпочтение: {removed_pref}")

        # Сохраняем обновленные предпочтения обратно в базу данных
        existing_user.preferences = json.dumps(preferences)
        session.commit()
        logger.info(f"Обновленные предпочтения сохранены: {existing_user.preferences}")

    if preferences:
        # Воссоздаём инлайн-клавиатуру с оставшимися предпочтениями
        keyboard = []
        for idx, preference in enumerate(preferences, start=1):
            button = InlineKeyboardButton(
                text=f"Remove '{preference}'",
                callback_data=f"remove_pref:{idx - 1}",
            )
            keyboard.append([button])

        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            text=f"Удалено '{removed_pref}'. Вот ваши обновленные предпочтения:",
            reply_markup=reply_markup,
        )
    else:
        await query.edit_message_text(
            text=f"Удалено '{removed_pref}'. У вас больше нет предпочтений."
        )

    return

async def fallback_remove_preference(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Fallback handler if inline buttons do not work.
    Presents a numbered list of preferences and asks the user to select one to remove.
    """
    user = update.effective_user
    if not user:
        await update.message.reply_text("Unable to identify the user.")
        return ConversationHandler.END

    with SessionLocal() as session:
        existing_user = session.query(User).filter(User.telegram_id == user.id).first()

        if not existing_user:
            await update.message.reply_text("User not found in the database.")
            return ConversationHandler.END

        preferences_text = existing_user.preferences

    try:
        preferences = json.loads(preferences_text) if preferences_text else []
        if not isinstance(preferences, list):
            raise ValueError
    except (json.JSONDecodeError, ValueError):
        await update.message.reply_text(
            "Your preferences data is corrupted or not in the correct format."
        )
        return ConversationHandler.END

    if not preferences:
        await update.message.reply_text("You have no preferences to remove.")
        return ConversationHandler.END

    # Create a numbered list of preferences
    message = "Select the number of the preference you want to remove:\n"
    for idx, preference in enumerate(preferences, start=1):
        message += f"{idx}. {preference}\n"

    # Create keyboard buttons with numbers
    keyboard = [
        [KeyboardButton(str(idx)) for idx in range(1, len(preferences) + 1)]
    ]
    reply_markup = ReplyKeyboardMarkup(
        keyboard, one_time_keyboard=True, resize_keyboard=True
    )

    await update.message.reply_text(message, reply_markup=reply_markup)

    return REMOVE_PREFERENCE

async def handle_remove_preference_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles the user's selection when using the fallback method to remove a preference.
    """
    user = update.effective_user
    if not user:
        await update.message.reply_text("Unable to identify the user.")
        return ConversationHandler.END

    selection = update.message.text.strip()

    if not selection.isdigit():
        await update.message.reply_text("Please enter a valid number.")
        return REMOVE_PREFERENCE

    selection = int(selection) - 1  # Convert to zero-based index

    with SessionLocal() as session:
        existing_user = session.query(User).filter(User.telegram_id == user.id).first()

        if not existing_user:
            await update.message.reply_text("User not found in the database.")
            return ConversationHandler.END

        preferences_text = existing_user.preferences

        try:
            preferences = json.loads(preferences_text) if preferences_text else []
            if not isinstance(preferences, list):
                raise ValueError
        except (json.JSONDecodeError, ValueError):
            await update.message.reply_text(
                "Your preferences data is corrupted or not in the correct format."
            )
            return ConversationHandler.END

        if selection < 0 or selection >= len(preferences):
            await update.message.reply_text("Selected number is out of range.")
            return REMOVE_PREFERENCE

        removed_pref = preferences.pop(selection)

        # Save the updated preferences back to the database
        existing_user.preferences = json.dumps(preferences)
        session.commit()

    if preferences:
        # Create a numbered list of remaining preferences
        message = "Preference removed successfully. Here are your updated preferences:\n"
        for idx, preference in enumerate(preferences, start=1):
            message += f"{idx}. {preference}\n"
    else:
        message = f"Preference '{removed_pref}' removed. You have no more preferences."

    await update.message.reply_text(message, reply_markup=ReplyKeyboardMarkup(
        [[]], resize_keyboard=True
    ))  # Remove the custom keyboard

    return ConversationHandler.END