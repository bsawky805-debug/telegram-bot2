import sqlite3
import random
import string
from datetime import datetime, timedelta

from telegram import (
        Update,
        InlineKeyboardButton,
        InlineKeyboardMarkup,
    )
from telegram.ext import (
        Application,
        CommandHandler,
        CallbackQueryHandler,
        MessageHandler,
        ContextTypes,
        filters,
    )

TOKEN = "8795829326:AAEcy8-ZTNxjN4sgyXBWAq7u3Kat51SPK-k"

    # =========================
    # Languages
    # =========================
LANGUAGES = {
        "en": {
            "flag": "🇺🇸",
            "name": "English",
            "welcome_private": "Welcome {name} 👋\nPlease choose your language:",
            "main_menu": "Main Menu:",
            "credits": "💳 Your Credits: {credits}",
            "profile": "👤 Name: {name}\n🔹 Username: {username}\n🆔 ID: {user_id}\n💳 Credits: {credits}\n💬 Messages: {messages}\n🌐 Language: {language}",
            "salary_need_msgs": "❌ You need at least 20 messages to claim salary.\n💬 Your messages: {count}/20",
            "salary_wait": "❌ You already claimed your salary.\n⏳ Try again after {hours}h {minutes}m",
            "salary_success": "✅ You received {amount} Credits\n💳 Your Credits: {credits}",
            "transfer_usage": "💸 To transfer Credits use:\n/transfer USER_ID AMOUNT",
            "transfer_self": "You cannot transfer Credits to yourself.",
            "transfer_receiver": "Receiver not found. Ask them to start the bot first.",
            "transfer_not_enough": "Not enough Credits.",
            "transfer_invalid_amount": "Amount must be greater than 0.",
            "transfer_captcha_prompt": "🔐 Verification required.\nType this code exactly:\n\n`{code}`",
            "transfer_captcha_wrong": "❌ Wrong code. Transfer cancelled.",
            "transfer_success": "✅ Transfer completed.\nSent {amount} Credits to {receiver_id}",
            "help_text": (
                "📖 MaxBot Help\n\n"
                "/start - Start the bot\n"
                "/help - Show help\n"
                "/transfer USER_ID AMOUNT - Send credits\n"
                "/addreply word|reply - Add auto reply in group\n"
                "/delreply word - Delete reply\n"
                "/replies - Show replies\n"
                "/addcommand name|response - Add custom command in group\n"
                "/delcommand name - Delete custom command\n"
                "/commandslist - Show custom commands\n"
                "/addbadword word - Add filtered word\n"
                "/delbadword word - Delete filtered word\n"
                "/badwords - Show filtered words\n"
                "/setwelcome message - Set group welcome message\n"
                "/settings - Show group settings\n\n"
                "Daily Salary:\n"
                "• Need 20 messages minimum\n"
                "• Once every 24 hours\n"
                "• Random amount from 10 to 50 Credits"
            ),
            "leaderboard_title": "🏆 Leaderboard\n\n",
            "no_users": "No users yet.",
            "language_saved": "✅ Your language has been saved.",
            "group_language_choose": "🌐 Group language is not set.\nAdmin, choose the group language:",
            "group_language_saved": "✅ Group language has been set.",
            "group_welcome_default": "Welcome {name} to the group! 👋",
            "welcome_set": "✅ Welcome message saved.",
            "settings_text": (
                "⚙️ Group Settings\n\n"
                "Language: {language}\n"
                "Welcome: {welcome}\n"
                "Filter enabled: {filter_enabled}\n"
            ),
            "admins_only": "Only admins can use this command.",
            "groups_only": "This command works in groups only.",
            "reply_added": "✅ Reply added:\n{trigger} → {response}",
            "reply_deleted": "✅ Reply deleted.",
            "reply_not_found": "❌ Reply not found.",
            "replies_title": "📋 Group Replies:\n\n",
            "no_replies": "No replies added in this group yet.",
            "command_added": "✅ Custom command added:\n/{name} → {response}",
            "command_deleted": "✅ Custom command deleted.",
            "command_not_found": "❌ Command not found.",
            "commands_title": "📋 Group Custom Commands:\n\n",
            "no_commands": "No custom commands in this group yet.",
            "badword_added": "✅ Filtered word added: {word}",
            "badword_deleted": "✅ Filtered word deleted.",
            "badword_not_found": "❌ Word not found.",
            "badwords_title": "🚫 Filtered Words:\n\n",
            "no_badwords": "No filtered words yet.",
            "filtered_message": "🚫 This word is not allowed here.",
            "choose_language": "🌐 Choose your language:",
            "choose_group_language": "🌐 Admin, choose the group language:",
            "back": "⬅️ Back",
            "credits_btn": "💳 Credits",
            "salary_btn": "🎁 Daily Salary",
            "transfer_btn": "💸 Transfer",
            "profile_btn": "👤 Profile",
            "leaderboard_btn": "🏆 Leaderboard",
            "help_btn": "📖 Help",
            "welcome_preview_none": "Default",
        },
        "ar": {
            "flag": "🇸🇦",
            "name": "العربية",
            "welcome_private": "أهلًا {name} 👋\nاختر لغتك:",
            "main_menu": "القائمة الرئيسية:",
            "credits": "💳 الكردت عندك: {credits}",
            "profile": "👤 الاسم: {name}\n🔹 اليوزر: {username}\n🆔 الآيدي: {user_id}\n💳 الكردت: {credits}\n💬 الرسائل: {messages}\n🌐 اللغة: {language}",
            "salary_need_msgs": "❌ تحتاج 20 رسالة على الأقل لاستلام الراتب.\n💬 رسائلك: {count}/20",
            "salary_wait": "❌ سبق واستلمت راتبك.\n⏳ حاول بعد {hours} ساعة و {minutes} دقيقة",
            "salary_success": "✅ استلمت {amount} كردت\n💳 الكردت عندك: {credits}",
            "transfer_usage": "💸 لتحويل الكردت استخدم:\n/transfer USER_ID AMOUNT",
            "transfer_self": "ما تقدر تحول لنفسك.",
            "transfer_receiver": "المستلم غير موجود. خله يبدأ البوت أولًا.",
            "transfer_not_enough": "ما عندك كردت كافي.",
            "transfer_invalid_amount": "المبلغ لازم يكون أكبر من 0.",
            "transfer_captcha_prompt": "🔐 مطلوب تحقق.\nاكتب هذا الرمز بالضبط:\n\n`{code}`",
            "transfer_captcha_wrong": "❌ رمز التحقق غلط. تم إلغاء التحويل.",
            "transfer_success": "✅ تم التحويل بنجاح.\nتم إرسال {amount} كردت إلى {receiver_id}",
            "help_text": (
                "📖 شرح MaxBot\n\n"
                "/start - تشغيل البوت\n"
                "/help - عرض الشرح\n"
                "/transfer USER_ID AMOUNT - تحويل كردت\n"
                "/addreply كلمة|رد - إضافة رد تلقائي في الكروب\n"
                "/delreply كلمة - حذف رد\n"
                "/replies - عرض الردود\n"
                "/addcommand اسم|رد - إضافة أمر مخصص في الكروب\n"
                "/delcommand اسم - حذف أمر مخصص\n"
                "/commandslist - عرض الأوامر المخصصة\n"
                "/addbadword كلمة - إضافة كلمة ممنوعة\n"
                "/delbadword كلمة - حذف كلمة ممنوعة\n"
                "/badwords - عرض الكلمات الممنوعة\n"
                "/setwelcome رسالة - تعيين ترحيب الكروب\n"
                "/settings - عرض إعدادات الكروب\n\n"
                "الراتب اليومي:\n"
                "• لازم 20 رسالة على الأقل\n"
                "• مرة كل 24 ساعة\n"
                "• عشوائي من 10 إلى 50 كردت"
            ),
            "leaderboard_title": "🏆 قائمة الأغنياء\n\n",
            "no_users": "ماكو مستخدمين بعد.",
            "language_saved": "✅ تم حفظ لغتك.",
            "group_language_choose": "🌐 لغة الكروب غير محددة.\nالأدمن يختار لغة الكروب:",
            "group_language_saved": "✅ تم حفظ لغة الكروب.",
            "group_welcome_default": "أهلًا {name} في الكروب 👋",
            "welcome_set": "✅ تم حفظ رسالة الترحيب.",
            "settings_text": (
                "⚙️ إعدادات الكروب\n\n"
                "اللغة: {language}\n"
                "الترحيب: {welcome}\n"
                "الفلترة مفعلة: {filter_enabled}\n"
            ),
            "admins_only": "هذا الأمر للأدمن فقط.",
            "groups_only": "هذا الأمر يشتغل في الكروبات فقط.",
            "reply_added": "✅ تم إضافة الرد:\n{trigger} → {response}",
            "reply_deleted": "✅ تم حذف الرد.",
            "reply_not_found": "❌ الرد غير موجود.",
            "replies_title": "📋 ردود الكروب:\n\n",
            "no_replies": "ماكو ردود مضافة لهذا الكروب.",
            "command_added": "✅ تم إضافة الأمر المخصص:\n/{name} → {response}",
            "command_deleted": "✅ تم حذف الأمر المخصص.",
            "command_not_found": "❌ الأمر غير موجود.",
            "commands_title": "📋 أوامر الكروب المخصصة:\n\n",
            "no_commands": "ماكو أوامر مخصصة في هذا الكروب.",
            "badword_added": "✅ تم إضافة كلمة ممنوعة: {word}",
            "badword_deleted": "✅ تم حذف الكلمة الممنوعة.",
            "badword_not_found": "❌ الكلمة غير موجودة.",
            "badwords_title": "🚫 الكلمات الممنوعة:\n\n",
            "no_badwords": "ماكو كلمات ممنوعة بعد.",
            "filtered_message": "🚫 هذه الكلمة ممنوعة هنا.",
            "choose_language": "🌐 اختر لغتك:",
            "choose_group_language": "🌐 أيها الأدمن، اختر لغة الكروب:",
            "back": "⬅️ رجوع",
            "credits_btn": "💳 الكردت",
            "salary_btn": "🎁 الراتب اليومي",
            "transfer_btn": "💸 تحويل",
            "profile_btn": "👤 ملفي",
            "leaderboard_btn": "🏆 المتصدرين",
            "help_btn": "📖 شرح",
            "welcome_preview_none": "الافتراضي",
        },
        "es": {
            "flag": "🇪🇸",
            "name": "Español",
            "welcome_private": "Bienvenido {name} 👋\nElige tu idioma:",
            "main_menu": "Menú principal:",
            "credits": "💳 Tus créditos: {credits}",
            "profile": "👤 Nombre: {name}\n🔹 Usuario: {username}\n🆔 ID: {user_id}\n💳 Créditos: {credits}\n💬 Mensajes: {messages}\n🌐 Idioma: {language}",
            "salary_need_msgs": "❌ Necesitas al menos 20 mensajes para reclamar el salario.\n💬 Tus mensajes: {count}/20",
            "salary_wait": "❌ Ya reclamaste tu salario.\n⏳ Intenta de nuevo en {hours}h {minutes}m",
            "salary_success": "✅ Recibiste {amount} Créditos\n💳 Tus créditos: {credits}",
            "transfer_usage": "💸 Para transferir créditos usa:\n/transfer USER_ID AMOUNT",
            "transfer_self": "No puedes transferirte a ti mismo.",
            "transfer_receiver": "Receptor no encontrado. Debe usar /start primero.",
            "transfer_not_enough": "No tienes suficientes créditos.",
            "transfer_invalid_amount": "La cantidad debe ser mayor que 0.",
            "transfer_captcha_prompt": "🔐 Verificación requerida.\nEscribe este código exactamente:\n\n`{code}`",
            "transfer_captcha_wrong": "❌ Código incorrecto. Transferencia cancelada.",
            "transfer_success": "✅ Transferencia completada.\nEnviaste {amount} Créditos a {receiver_id}",
            "help_text": "📖 Ayuda de MaxBot",
            "leaderboard_title": "🏆 Clasificación\n\n",
            "no_users": "Aún no hay usuarios.",
            "language_saved": "✅ Tu idioma ha sido guardado.",
            "group_language_choose": "🌐 El idioma del grupo no está configurado.\nAdmin, elige el idioma del grupo:",
            "group_language_saved": "✅ El idioma del grupo ha sido guardado.",
            "group_welcome_default": "¡Bienvenido {name} al grupo! 👋",
            "welcome_set": "✅ Mensaje de bienvenida guardado.",
            "settings_text": "⚙️ Ajustes del grupo\n\nIdioma: {language}\nBienvenida: {welcome}\nFiltro activo: {filter_enabled}\n",
            "admins_only": "Solo admins pueden usar este comando.",
            "groups_only": "Este comando solo funciona en grupos.",
            "reply_added": "✅ Respuesta añadida:\n{trigger} → {response}",
            "reply_deleted": "✅ Respuesta eliminada.",
            "reply_not_found": "❌ Respuesta no encontrada.",
            "replies_title": "📋 Respuestas del grupo:\n\n",
            "no_replies": "No hay respuestas en este grupo.",
            "command_added": "✅ Comando personalizado añadido:\n/{name} → {response}",
            "command_deleted": "✅ Comando personalizado eliminado.",
            "command_not_found": "❌ Comando no encontrado.",
            "commands_title": "📋 Comandos personalizados:\n\n",
            "no_commands": "No hay comandos personalizados.",
            "badword_added": "✅ Palabra filtrada añadida: {word}",
            "badword_deleted": "✅ Palabra filtrada eliminada.",
            "badword_not_found": "❌ Palabra no encontrada.",
            "badwords_title": "🚫 Palabras filtradas:\n\n",
            "no_badwords": "No hay palabras filtradas.",
            "filtered_message": "🚫 Esta palabra no está permitida aquí.",
            "choose_language": "🌐 Elige tu idioma:",
            "choose_group_language": "🌐 Admin, elige el idioma del grupo:",
            "back": "⬅️ Volver",
            "credits_btn": "💳 Créditos",
            "salary_btn": "🎁 Salario diario",
            "transfer_btn": "💸 Transferir",
            "profile_btn": "👤 Perfil",
            "leaderboard_btn": "🏆 Ranking",
            "help_btn": "📖 Ayuda",
            "welcome_preview_none": "Predeterminado",
        },
    }


    # =========================
    # Database
    # =========================
def db_connect():
        return sqlite3.connect("bot.db")


def init_db():
        conn = db_connect()
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                credits INTEGER DEFAULT 0,
                message_count INTEGER DEFAULT 0,
                last_salary TEXT,
                language TEXT DEFAULT 'en'
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS group_settings (
                chat_id INTEGER PRIMARY KEY,
                language TEXT,
                welcome_message TEXT,
                filter_enabled INTEGER DEFAULT 1,
                language_locked INTEGER DEFAULT 0
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS replies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id INTEGER NOT NULL,
                trigger TEXT NOT NULL,
                response TEXT NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS custom_commands (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                response TEXT NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS badwords (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id INTEGER NOT NULL,
                word TEXT NOT NULL
            )
        """)

        conn.commit()
        conn.close()


    # =========================
    # DB helpers
    # =========================
def ensure_user(user):
        conn = db_connect()
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (user.id,))
        exists = cursor.fetchone()

        if not exists:
            cursor.execute("""
                INSERT INTO users (user_id, username, first_name, credits, message_count, last_salary, language)
                VALUES (?, ?, ?, 0, 0, NULL, 'en')
            """, (user.id, user.username, user.first_name))
        else:
            cursor.execute("""
                UPDATE users
                SET username = ?, first_name = ?
                WHERE user_id = ?
            """, (user.username, user.first_name, user.id))

        conn.commit()
        conn.close()


def get_user(user_id):
        conn = db_connect()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT user_id, username, first_name, credits, message_count, last_salary, language
            FROM users WHERE user_id = ?
        """, (user_id,))
        row = cursor.fetchone()
        conn.close()
        return row


def set_user_language(user_id, lang):
        conn = db_connect()
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET language = ? WHERE user_id = ?", (lang, user_id))
        conn.commit()
        conn.close()


def get_user_language(user_id):
        user = get_user(user_id)
        return user[6] if user else "en"


def ensure_group(chat_id):
        conn = db_connect()
        cursor = conn.cursor()
        cursor.execute("SELECT chat_id FROM group_settings WHERE chat_id = ?", (chat_id,))
        row = cursor.fetchone()
        if not row:
            cursor.execute("""
                INSERT INTO group_settings (chat_id, language, welcome_message, filter_enabled, language_locked)
                VALUES (?, NULL, NULL, 1, 0)
            """, (chat_id,))
        conn.commit()
        conn.close()


def get_group_settings(chat_id):
        ensure_group(chat_id)
        conn = db_connect()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT chat_id, language, welcome_message, filter_enabled, language_locked
            FROM group_settings WHERE chat_id = ?
        """, (chat_id,))
        row = cursor.fetchone()
        conn.close()
        return row


def set_group_language(chat_id, lang):
        ensure_group(chat_id)
        conn = db_connect()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE group_settings
            SET language = ?, language_locked = 1
            WHERE chat_id = ?
        """, (lang, chat_id))
        conn.commit()
        conn.close()


def set_welcome(chat_id, message):
        ensure_group(chat_id)
        conn = db_connect()
        cursor = conn.cursor()
        cursor.execute("UPDATE group_settings SET welcome_message = ? WHERE chat_id = ?", (message, chat_id))
        conn.commit()
        conn.close()


def toggle_filter(chat_id, enabled):
        ensure_group(chat_id)
        conn = db_connect()
        cursor = conn.cursor()
        cursor.execute("UPDATE group_settings SET filter_enabled = ? WHERE chat_id = ?", (1 if enabled else 0, chat_id))
        conn.commit()
        conn.close()


def add_message(user_id):
        conn = db_connect()
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET message_count = message_count + 1 WHERE user_id = ?", (user_id,))
        conn.commit()
        conn.close()


def add_credits(user_id, amount):
        conn = db_connect()
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET credits = credits + ? WHERE user_id = ?", (amount, user_id))
        conn.commit()
        conn.close()


def transfer_credits_db(sender_id, receiver_id, amount):
        conn = db_connect()
        cursor = conn.cursor()

        cursor.execute("SELECT credits FROM users WHERE user_id = ?", (sender_id,))
        sender = cursor.fetchone()
        cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (receiver_id,))
        receiver = cursor.fetchone()

        if not receiver:
            conn.close()
            return False, "receiver_not_found"
        if amount <= 0:
            conn.close()
            return False, "invalid_amount"
        if sender[0] < amount:
            conn.close()
            return False, "not_enough"

        cursor.execute("UPDATE users SET credits = credits - ? WHERE user_id = ?", (amount, sender_id))
        cursor.execute("UPDATE users SET credits = credits + ? WHERE user_id = ?", (amount, receiver_id))
        conn.commit()
        conn.close()
        return True, "ok"


def set_last_salary(user_id, when_text):
        conn = db_connect()
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET last_salary = ? WHERE user_id = ?", (when_text, user_id))
        conn.commit()
        conn.close()


def get_top_users(limit=10):
        conn = db_connect()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT first_name, username, credits
            FROM users
            ORDER BY credits DESC
            LIMIT ?
        """, (limit,))
        rows = cursor.fetchall()
        conn.close()
        return rows


    # Replies
def add_reply_db(chat_id, trigger, response):
        conn = db_connect()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO replies (chat_id, trigger, response)
            VALUES (?, ?, ?)
        """, (chat_id, trigger.lower().strip(), response.strip()))
        conn.commit()
        conn.close()


def delete_reply_db(chat_id, trigger):
        conn = db_connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM replies WHERE chat_id = ? AND trigger = ?", (chat_id, trigger.lower().strip()))
        deleted = cursor.rowcount
        conn.commit()
        conn.close()
        return deleted > 0


def get_reply_db(chat_id, text):
        conn = db_connect()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT response FROM replies
            WHERE chat_id = ? AND trigger = ?
            LIMIT 1
        """, (chat_id, text.lower().strip()))
        row = cursor.fetchone()
        conn.close()
        return row[0] if row else None


def list_replies_db(chat_id):
        conn = db_connect()
        cursor = conn.cursor()
        cursor.execute("SELECT trigger, response FROM replies WHERE chat_id = ? ORDER BY id DESC", (chat_id,))
        rows = cursor.fetchall()
        conn.close()
        return rows


    # Commands
def add_custom_command_db(chat_id, name, response):
        conn = db_connect()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO custom_commands (chat_id, name, response)
            VALUES (?, ?, ?)
        """, (chat_id, name.lower().strip(), response.strip()))
        conn.commit()
        conn.close()


def delete_custom_command_db(chat_id, name):
        conn = db_connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM custom_commands WHERE chat_id = ? AND name = ?", (chat_id, name.lower().strip()))
        deleted = cursor.rowcount
        conn.commit()
        conn.close()
        return deleted > 0


def get_custom_command_db(chat_id, name):
        conn = db_connect()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT response FROM custom_commands
            WHERE chat_id = ? AND name = ?
            LIMIT 1
        """, (chat_id, name.lower().strip()))
        row = cursor.fetchone()
        conn.close()
        return row[0] if row else None


def list_custom_commands_db(chat_id):
        conn = db_connect()
        cursor = conn.cursor()
        cursor.execute("SELECT name, response FROM custom_commands WHERE chat_id = ? ORDER BY id DESC", (chat_id,))
        rows = cursor.fetchall()
        conn.close()
        return rows


    # Badwords
def add_badword_db(chat_id, word):
        conn = db_connect()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO badwords (chat_id, word) VALUES (?, ?)", (chat_id, word.lower().strip()))
        conn.commit()
        conn.close()


def delete_badword_db(chat_id, word):
        conn = db_connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM badwords WHERE chat_id = ? AND word = ?", (chat_id, word.lower().strip()))
        deleted = cursor.rowcount
        conn.commit()
        conn.close()
        return deleted > 0


def list_badwords_db(chat_id):
        conn = db_connect()
        cursor = conn.cursor()
        cursor.execute("SELECT word FROM badwords WHERE chat_id = ? ORDER BY id DESC", (chat_id,))
        rows = cursor.fetchall()
        conn.close()
        return [r[0] for r in rows]


def contains_badword(chat_id, text):
        words = list_badwords_db(chat_id)
        low = text.lower()
        return any(w in low for w in words)


    # =========================
    # Text helpers
    # =========================
def tr(lang, key, **kwargs):
        data = LANGUAGES.get(lang, LANGUAGES["en"])
        text = data.get(key, LANGUAGES["en"].get(key, key))
        return text.format(**kwargs)


def user_lang(user_id):
        return get_user_language(user_id)


def group_lang(chat_id):
        settings = get_group_settings(chat_id)
        lang = settings[1]
        return lang if lang else "en"


def language_name(lang):
        data = LANGUAGES.get(lang, LANGUAGES["en"])
        return f"{data['flag']} {data['name']}"


def main_menu(lang):
        keyboard = [
            [InlineKeyboardButton(tr(lang, "credits_btn"), callback_data="credits")],
            [InlineKeyboardButton(tr(lang, "salary_btn"), callback_data="salary")],
            [InlineKeyboardButton(tr(lang, "transfer_btn"), callback_data="transfer")],
            [InlineKeyboardButton(tr(lang, "profile_btn"), callback_data="profile")],
            [InlineKeyboardButton(tr(lang, "leaderboard_btn"), callback_data="leaderboard")],
            [InlineKeyboardButton(tr(lang, "help_btn"), callback_data="help")],
        ]
        return InlineKeyboardMarkup(keyboard)


def back_menu(lang):
        return InlineKeyboardMarkup([[InlineKeyboardButton(tr(lang, "back"), callback_data="back")]])


def user_language_keyboard():
        keyboard = []
        row = []
        for code in ["ar", "en", "es"]:
            label = f"{LANGUAGES[code]['flag']} {LANGUAGES[code]['name']}"
            row.append(InlineKeyboardButton(label, callback_data=f"setlang_user_{code}"))
        keyboard.append(row)
        return InlineKeyboardMarkup(keyboard)


def group_language_keyboard():
        keyboard = []
        row = []
        for code in ["ar", "en", "es"]:
            label = f"{LANGUAGES[code]['flag']} {LANGUAGES[code]['name']}"
            row.append(InlineKeyboardButton(label, callback_data=f"setlang_group_{code}"))
        keyboard.append(row)
        return InlineKeyboardMarkup(keyboard)


def random_captcha_code(length=5):
        chars = string.ascii_uppercase + string.digits
        return "".join(random.choice(chars) for _ in range(length))


    # =========================
    # Permissions
    # =========================
async def is_admin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
        if update.effective_chat.type not in ["group", "supergroup"]:
            return True
        member = await context.bot.get_chat_member(update.effective_chat.id, update.effective_user.id)
        return member.status in ["administrator", "creator"]


    # =========================
    # Commands
    # =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        ensure_user(user)
        lang = user_lang(user.id)

        if update.effective_chat.type == "private":
            await update.message.reply_text(
                tr(lang, "welcome_private", name=user.first_name),
                reply_markup=user_language_keyboard()
            )
        else:
            ensure_group(update.effective_chat.id)
            gsettings = get_group_settings(update.effective_chat.id)
            if not gsettings[1] and await is_admin(update, context):
                await update.message.reply_text(
                    tr("en", "choose_group_language"),
                    reply_markup=group_language_keyboard()
                )
            else:
                glang = group_lang(update.effective_chat.id)
                await update.message.reply_text(tr(glang, "main_menu"), reply_markup=main_menu(glang))


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        lang = user_lang(update.effective_user.id) if update.effective_chat.type == "private" else group_lang(update.effective_chat.id)
        await update.message.reply_text(tr(lang, "help_text"), reply_markup=main_menu(lang) if update.effective_chat.type == "private" else None)


async def transfer_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        ensure_user(user)
        lang = user_lang(user.id)

        if len(context.args) != 2:
            await update.message.reply_text(tr(lang, "transfer_usage"), reply_markup=main_menu(lang))
            return

        try:
            receiver_id = int(context.args[0])
            amount = int(context.args[1])
        except ValueError:
            await update.message.reply_text(tr(lang, "transfer_usage"), reply_markup=main_menu(lang))
            return

        if receiver_id == user.id:
            await update.message.reply_text(tr(lang, "transfer_self"), reply_markup=main_menu(lang))
            return

        code = random_captcha_code()
        context.user_data["pending_transfer"] = {
            "receiver_id": receiver_id,
            "amount": amount,
            "captcha": code,
        }

        await update.message.reply_text(
            tr(lang, "transfer_captcha_prompt", code=code),
            parse_mode="Markdown",
            reply_markup=main_menu(lang)
        )


async def addreply_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        chat = update.effective_chat
        lang = group_lang(chat.id)

        if chat.type not in ["group", "supergroup"]:
            await update.message.reply_text(tr(lang, "groups_only"))
            return

        if not await is_admin(update, context):
            await update.message.reply_text(tr(lang, "admins_only"))
            return

        if not context.args:
            await update.message.reply_text("/addreply word|reply")
            return

        full_text = " ".join(context.args)
        if "|" not in full_text:
            await update.message.reply_text("/addreply word|reply")
            return

        trigger, response = full_text.split("|", 1)
        trigger = trigger.strip()
        response = response.strip()

        if not trigger or not response:
            await update.message.reply_text("/addreply word|reply")
            return

        add_reply_db(chat.id, trigger, response)
        await update.message.reply_text(tr(lang, "reply_added", trigger=trigger, response=response))


async def delreply_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        chat = update.effective_chat
        lang = group_lang(chat.id)

        if chat.type not in ["group", "supergroup"]:
            await update.message.reply_text(tr(lang, "groups_only"))
            return

        if not await is_admin(update, context):
            await update.message.reply_text(tr(lang, "admins_only"))
            return

        if not context.args:
            await update.message.reply_text("/delreply word")
            return

        trigger = " ".join(context.args).strip()
        deleted = delete_reply_db(chat.id, trigger)

        if deleted:
            await update.message.reply_text(tr(lang, "reply_deleted"))
        else:
            await update.message.reply_text(tr(lang, "reply_not_found"))


async def replies_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        chat = update.effective_chat
        lang = group_lang(chat.id)

        if chat.type not in ["group", "supergroup"]:
            await update.message.reply_text(tr(lang, "groups_only"))
            return

        rows = list_replies_db(chat.id)
        if not rows:
            await update.message.reply_text(tr(lang, "no_replies"))
            return

        text = tr(lang, "replies_title")
        for i, (trigger, response) in enumerate(rows[:20], start=1):
            text += f"{i}. {trigger} → {response}\n"
        await update.message.reply_text(text)


async def addcommand_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        chat = update.effective_chat
        lang = group_lang(chat.id)

        if chat.type not in ["group", "supergroup"]:
            await update.message.reply_text(tr(lang, "groups_only"))
            return

        if not await is_admin(update, context):
            await update.message.reply_text(tr(lang, "admins_only"))
            return

        if not context.args:
            await update.message.reply_text("/addcommand name|response")
            return

        full_text = " ".join(context.args)
        if "|" not in full_text:
            await update.message.reply_text("/addcommand name|response")
            return

        name, response = full_text.split("|", 1)
        name = name.strip().lstrip("/")
        response = response.strip()

        if not name or not response:
            await update.message.reply_text("/addcommand name|response")
            return

        add_custom_command_db(chat.id, name, response)
        await update.message.reply_text(tr(lang, "command_added", name=name, response=response))


async def delcommand_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        chat = update.effective_chat
        lang = group_lang(chat.id)

        if chat.type not in ["group", "supergroup"]:
            await update.message.reply_text(tr(lang, "groups_only"))
            return

        if not await is_admin(update, context):
            await update.message.reply_text(tr(lang, "admins_only"))
            return

        if not context.args:
            await update.message.reply_text("/delcommand name")
            return

        name = " ".join(context.args).strip().lstrip("/")
        deleted = delete_custom_command_db(chat.id, name)

        if deleted:
            await update.message.reply_text(tr(lang, "command_deleted"))
        else:
            await update.message.reply_text(tr(lang, "command_not_found"))


async def commandslist_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        chat = update.effective_chat
        lang = group_lang(chat.id)

        if chat.type not in ["group", "supergroup"]:
            await update.message.reply_text(tr(lang, "groups_only"))
            return

        rows = list_custom_commands_db(chat.id)
        if not rows:
            await update.message.reply_text(tr(lang, "no_commands"))
            return

        text = tr(lang, "commands_title")
        for i, (name, response) in enumerate(rows[:20], start=1):
            text += f"{i}. /{name} → {response}\n"
        await update.message.reply_text(text)


async def addbadword_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        chat = update.effective_chat
        lang = group_lang(chat.id)

        if chat.type not in ["group", "supergroup"]:
            await update.message.reply_text(tr(lang, "groups_only"))
            return

        if not await is_admin(update, context):
            await update.message.reply_text(tr(lang, "admins_only"))
            return

        if not context.args:
            await update.message.reply_text("/addbadword word")
            return

        word = " ".join(context.args).strip().lower()
        add_badword_db(chat.id, word)
        await update.message.reply_text(tr(lang, "badword_added", word=word))


async def delbadword_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        chat = update.effective_chat
        lang = group_lang(chat.id)

        if chat.type not in ["group", "supergroup"]:
            await update.message.reply_text(tr(lang, "groups_only"))
            return

        if not await is_admin(update, context):
            await update.message.reply_text(tr(lang, "admins_only"))
            return

        if not context.args:
            await update.message.reply_text("/delbadword word")
            return

        word = " ".join(context.args).strip().lower()
        deleted = delete_badword_db(chat.id, word)

        if deleted:
            await update.message.reply_text(tr(lang, "badword_deleted"))
        else:
            await update.message.reply_text(tr(lang, "badword_not_found"))


async def badwords_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        chat = update.effective_chat
        lang = group_lang(chat.id)

        if chat.type not in ["group", "supergroup"]:
            await update.message.reply_text(tr(lang, "groups_only"))
            return

        words = list_badwords_db(chat.id)
        if not words:
            await update.message.reply_text(tr(lang, "no_badwords"))
            return

        text = tr(lang, "badwords_title")
        for i, word in enumerate(words[:30], start=1):
            text += f"{i}. {word}\n"
        await update.message.reply_text(text)


async def setwelcome_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        chat = update.effective_chat
        lang = group_lang(chat.id)

        if chat.type not in ["group", "supergroup"]:
            await update.message.reply_text(tr(lang, "groups_only"))
            return

        if not await is_admin(update, context):
            await update.message.reply_text(tr(lang, "admins_only"))
            return

        if not context.args:
            await update.message.reply_text("/setwelcome your message here")
            return

        message = " ".join(context.args).strip()
        set_welcome(chat.id, message)
        await update.message.reply_text(tr(lang, "welcome_set"))


async def settings_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        chat = update.effective_chat
        ensure_group(chat.id)
        lang = group_lang(chat.id)
        settings = get_group_settings(chat.id)

        welcome = settings[2] if settings[2] else tr(lang, "welcome_preview_none")
        filter_enabled = "Yes" if settings[3] == 1 else "No"
        if lang == "ar":
            filter_enabled = "نعم" if settings[3] == 1 else "لا"

        await update.message.reply_text(
            tr(
                lang,
                "settings_text",
                language=language_name(lang),
                welcome=welcome,
                filter_enabled=filter_enabled,
            )
        )


    # =========================
    # Buttons
    # =========================
async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        user = update.effective_user
        ensure_user(user)

        data = query.data

        if data.startswith("setlang_user_"):
            lang = data.split("_")[-1]
            set_user_language(user.id, lang)
            await query.edit_message_text(tr(lang, "language_saved"), reply_markup=main_menu(lang))
            return

        if data.startswith("setlang_group_"):
            if update.effective_chat.type not in ["group", "supergroup"]:
                return
            if not await is_admin(update, context):
                lang = group_lang(update.effective_chat.id)
                await query.edit_message_text(tr(lang, "admins_only"))
                return

            settings = get_group_settings(update.effective_chat.id)
            if settings[4] == 1:
                lang = settings[1] or "en"
                await query.edit_message_text(f"{language_name(lang)}")
                return

            lang = data.split("_")[-1]
            set_group_language(update.effective_chat.id, lang)
            await query.edit_message_text(tr(lang, "group_language_saved"))
            return

        lang = user_lang(user.id) if update.effective_chat.type == "private" else group_lang(update.effective_chat.id)
        user_data = get_user(user.id)

        if data == "credits":
            await query.edit_message_text(
                tr(lang, "credits", credits=user_data[3]),
                reply_markup=back_menu(lang)
            )

        elif data == "profile":
            username = user_data[1] if user_data[1] else "No username"
            await query.edit_message_text(
                tr(
                    lang,
                    "profile",
                    name=user_data[2],
                    username=username,
                    user_id=user.id,
                    credits=user_data[3],
                    messages=user_data[4],
                    language=language_name(user_data[6]),
                ),
                reply_markup=back_menu(lang)
            )

        elif data == "salary":
            message_count = user_data[4]
            last_salary = user_data[5]

            if message_count < 20:
                await query.edit_message_text(
                    tr(lang, "salary_need_msgs", count=message_count),
                    reply_markup=back_menu(lang)
                )
                return

            now = datetime.now()

            if last_salary:
                last_salary_time = datetime.fromisoformat(last_salary)
                next_time = last_salary_time + timedelta(hours=24)
                if now < next_time:
                    remaining = next_time - now
                    total_seconds = int(remaining.total_seconds())
                    hours = total_seconds // 3600
                    minutes = (total_seconds % 3600) // 60
                    await query.edit_message_text(
                        tr(lang, "salary_wait", hours=hours, minutes=minutes),
                        reply_markup=back_menu(lang)
                    )
                    return

            amount = random.randint(10, 50)
            add_credits(user.id, amount)
            set_last_salary(user.id, now.isoformat())
            new_user = get_user(user.id)

            await query.edit_message_text(
                tr(lang, "salary_success", amount=amount, credits=new_user[3]),
                reply_markup=back_menu(lang)
            )

        elif data == "transfer":
            await query.edit_message_text(
                tr(lang, "transfer_usage"),
                reply_markup=back_menu(lang)
            )

        elif data == "leaderboard":
            top = get_top_users(10)
            if not top:
                text = tr(lang, "no_users")
            else:
                text = tr(lang, "leaderboard_title")
                for i, row in enumerate(top, start=1):
                    first_name, username, credits = row
                    display_name = first_name or username or "Unknown"
                    text += f"{i}. {display_name} — {credits}\n"

            await query.edit_message_text(text, reply_markup=back_menu(lang))

        elif data == "help":
            await query.edit_message_text(tr(lang, "help_text"), reply_markup=back_menu(lang))

        elif data == "back":
            await query.edit_message_text(tr(lang, "main_menu"), reply_markup=main_menu(lang))


    # =========================
    # Group welcome
    # =========================
async def welcome_new_members(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not update.message or not update.message.new_chat_members:
            return

        chat = update.effective_chat
        ensure_group(chat.id)
        lang = group_lang(chat.id)
        settings = get_group_settings(chat.id)
        welcome_msg = settings[2]

        for member in update.message.new_chat_members:
            if member.is_bot:
                continue
            ensure_user(member)
            text = welcome_msg if welcome_msg else tr(lang, "group_welcome_default", name=member.first_name)
            text = text.replace("{name}", member.first_name)
            await update.message.reply_text(text)


    # =========================
    # Text messages
    # =========================
async def count_messages_and_features(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not update.message:
            return

        user = update.effective_user
        if user.is_bot:
            return

        ensure_user(user)

        text = update.message.text or ""
        if not text:
            return

        # pending captcha transfer in private
        if update.effective_chat.type == "private":
            lang = user_lang(user.id)
            pending = context.user_data.get("pending_transfer")
            if pending:
                if text.strip() == pending["captcha"]:
                    success, code = transfer_credits_db(user.id, pending["receiver_id"], pending["amount"])
                    context.user_data.pop("pending_transfer", None)

                    if not success:
                        if code == "receiver_not_found":
                            await update.message.reply_text(tr(lang, "transfer_receiver"), reply_markup=main_menu(lang))
                        elif code == "invalid_amount":
                            await update.message.reply_text(tr(lang, "transfer_invalid_amount"), reply_markup=main_menu(lang))
                        elif code == "not_enough":
                            await update.message.reply_text(tr(lang, "transfer_not_enough"), reply_markup=main_menu(lang))
                        else:
                            await update.message.reply_text("Error", reply_markup=main_menu(lang))
                        return

                    await update.message.reply_text(
                        tr(lang, "transfer_success", amount=pending["amount"], receiver_id=pending["receiver_id"]),
                        reply_markup=main_menu(lang)
                    )
                    return
                else:
                    context.user_data.pop("pending_transfer", None)
                    await update.message.reply_text(tr(lang, "transfer_captcha_wrong"), reply_markup=main_menu(lang))
                    return

        chat = update.effective_chat
        if chat.type in ["group", "supergroup"]:
            ensure_group(chat.id)
            glang = group_lang(chat.id)
            add_message(user.id)

            # If group language not chosen and admin sends /start, handled in start.
            # Badwords
            settings = get_group_settings(chat.id)
            filter_enabled = settings[3] == 1

            if filter_enabled and contains_badword(chat.id, text):
                try:
                    await update.message.delete()
                except Exception:
                    pass
                await update.message.reply_text(tr(glang, "filtered_message"))
                return

            # Replies
            if not text.startswith("/"):
                reply = get_reply_db(chat.id, text)
                if reply:
                    await update.message.reply_text(reply)
                    return

            # Custom commands in DB
            if text.startswith("/"):
                cmd = text.split()[0].lstrip("/").split("@")[0].lower()
                custom = get_custom_command_db(chat.id, cmd)
                if custom:
                    await update.message.reply_text(custom)
                    return


    # =========================
    # Main
    # =========================
def main():
        init_db()

        app = Application.builder().token(TOKEN).build()

        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("help", help_command))
        app.add_handler(CommandHandler("transfer", transfer_command))

        app.add_handler(CommandHandler("addreply", addreply_command))
        app.add_handler(CommandHandler("delreply", delreply_command))
        app.add_handler(CommandHandler("replies", replies_command))

        app.add_handler(CommandHandler("addcommand", addcommand_command))
        app.add_handler(CommandHandler("delcommand", delcommand_command))
        app.add_handler(CommandHandler("commandslist", commandslist_command))

        app.add_handler(CommandHandler("addbadword", addbadword_command))
        app.add_handler(CommandHandler("delbadword", delbadword_command))
        app.add_handler(CommandHandler("badwords", badwords_command))

        app.add_handler(CommandHandler("setwelcome", setwelcome_command))
        app.add_handler(CommandHandler("settings", settings_command))

        app.add_handler(CallbackQueryHandler(buttons))
        app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome_new_members))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, count_messages_and_features))
        app.add_handler(MessageHandler(filters.TEXT & filters.COMMAND, count_messages_and_features))

        print("Bot is running...")
        app.run_polling()


if __name__ == "__main__":
        main()