import logging
from django.conf import settings
from django.core.management.base import BaseCommand
from telegram import Update
from telegram.ext import (
    CommandHandler,
    Updater,
    Filters,
    CallbackContext,
    ConversationHandler,
    MessageHandler,
    CallbackQueryHandler
)

from ...telegrambot import *


class Command(BaseCommand):
    help = "Run telegram bot in polling mode"
    can_import_settings = True

    
    def handle(self, *args, **options):
        updater = Updater(settings.TOKEN_KEY, use_context=True)

        # updater.dispatcher.add_handler(CommandHandler('start', start))
        # updater.dispatcher.add_handler(CallbackQueryHandler(category))
        # updater.dispatcher.add_handler(CommandHandler('help', help_command))
        # updater.start_polling()
        # updater.idle()
        dispatcher = updater.dispatcher
        conv_handler = ConversationHandler(
            entry_points=[CommandHandler('start', start)],
            states={
                2:[CallbackQueryHandler(employer), CommandHandler('start', start)],
                3:[MessageHandler(Filters.text & ~Filters.command, category), CommandHandler('start', start)],
                4:[CallbackQueryHandler(descriptions), CommandHandler('start', start)],
                5: [MessageHandler(Filters.text & ~Filters.command, region), CommandHandler('start', start)],
                6: [CallbackQueryHandler(district)],
                7:[CallbackQueryHandler(locations)],
                8:[MessageHandler(Filters.contact, last)],
                9:[CallbackQueryHandler(more_category)],
                10:[CallbackQueryHandler(user_category)],
                11: [CallbackQueryHandler(get_phone_number)],
                12: [CallbackQueryHandler(category_2)],
                13: [MessageHandler(Filters.location, check_phone)],
                14: [CallbackQueryHandler(district_2)],
                15: [CallbackQueryHandler(check_phone_2)],
                16: [CallbackQueryHandler(get_phone_number_2)],

            },
            fallbacks=[CommandHandler('help', help)],
        )
        dispatcher.add_handler(conv_handler)
        updater.start_polling()
        updater.idle()
