from telegram.ext import CommandHandler, MessageHandler, Filters

from .models import Category, Region, User

from telegram.ext import (
    CommandHandler,
    Updater,
    Filters,
    CallbackContext,
    ConversationHandler,
    MessageHandler,
    CallbackQueryHandler
)
from telegram import(
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove, 
    Update,  
    InlineKeyboardButton, 
    InlineKeyboardMarkup,
    KeyboardButton
) 


import logging
logger = logging.getLogger(__name__)

# def start()
db = Category()

def start(update: Update, context: CallbackContext) -> None:
    tg_user = update.message.from_user
    try:
        user = User.objects.get(tg_id=tg_user.id)
    except Exception:
        user = None

    if not user:
        user = User(tg_id=tg_user.id, first_name=tg_user.first_name, last_name=tg_user.last_name)
        user.save()

    jobs = [
        [

            InlineKeyboardButton("Ish beruvchi", callback_data='1'),
            InlineKeyboardButton("Ish Oluvchi", callback_data='2'),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(jobs)

    update.message.reply_text('KIMSIZ UZI ? :', reply_markup=reply_markup)
    return 2

def employer(update: Update, context: CallbackContext):
    query = update.callback_query
    datas = query.from_user
    try:
        user = User.objects.get(tg_id=datas.id)
    except Exception:
        user = None
    user.type_work=query.data
    user.save()
    
    if query.data == '1':
        return get_phone_number(update, context)
    elif query.data == '2':
        return category_2(update, context)
        
def category_2(update: Update, context: CallbackContext):
    query = update.callback_query
    childs= Category.objects.all()
    buttons = generateButtons(childs)

    query.message.delete()
    query.message.reply_text(
        'Qanday ish qilish kere: ',
        reply_markup=InlineKeyboardMarkup(buttons)
    )
    return 9

def more_category(update: Update, context: CallbackContext):
    query = update.callback_query
    print(query.data)
    jobs = [
        [

            InlineKeyboardButton("yana ish tanliszmi ", callback_data='1'),
            InlineKeyboardButton("Keyingi qadam", callback_data='2'),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(jobs)
    query.message.delete()

    query.message.reply_text('birini tanlang ? :', reply_markup=reply_markup)
    return 10

def user_category(update: Update, context: CallbackContext):
    query = update.callback_query.data
    
    if query == '1':
        return category_2(update, context)
    elif query == '2':
        return region_2(update, context)

def get_phone_number(update: Update, context: CallbackContext):
    query = update.callback_query
    query.message.delete()
    text = 'Telefon nomeringizni kiriting: '
    query.message.reply_text(text)
    return 3

def category(update: Update, context: CallbackContext) :
    tg_user = update.message.from_user
    phone_user = update.message.text
    try:
        user = User.objects.get(tg_id=tg_user.id)
    except Exception:
        user = None


    user.phone=phone_user
    user.save()

    childs= Category.objects.all()
    buttons = generateButtons(childs)

    update.message.delete()
    update.message.reply_text(
        'Qanday ish qilish kere: ',
        reply_markup=InlineKeyboardMarkup(buttons)
    )
    return 4

def descriptions(update: Update, context: CallbackContext):
    query = update.callback_query
    datas = query.data.split('_')
    text = 'Ish xaqida qisqacha malumot yozing'
    query.message.reply_text(text)
    return 5

def region_2(update: Update, context: CallbackContext):
    query = update.callback_query
    regions = Region.objects.filter(parend_id=0)
    buttons= generateButtons(regions)
    
    query.message.reply_text(
        'Qaysi Viloyatdansz: ', 
        reply_markup=InlineKeyboardMarkup(buttons)
    )
    return 6

def region(update: Update, context: CallbackContext):
    regions = Region.objects.filter(parend_id=0)
    buttons= generateButtons(regions)
    
    update.message.reply_text(
        'Qaysi Viloyatdansz: ', 
        reply_markup=InlineKeyboardMarkup(buttons)
    )
    return 6

def district(update: Update, context: CallbackContext):

    query = update.callback_query
    datas = query.data.split('_')
    if datas[0] == 'category':
        cat_id = int(datas[1])
        disct = Region.objects.raw('SELECT * FROM bot_region where parend_id=%s',[cat_id])
        buttons= generateButtons(disct)
    query.message.delete()
    query.message.reply_text(
        'Qaysi tumandansz: ', 
        reply_markup=InlineKeyboardMarkup(buttons)
    )
    return 7

def locations(update, context):
    query = update.callback_query
    
    location_keyboard = KeyboardButton(text="send location",  request_location=True)
    query.message.reply_text('lacation tashlang!', reply_markup=ReplyKeyboardMarkup([[location_keyboard]]))
    return 8

def last(update, context):
    from_user = update.message
    print(from_user)
    update.message.reply_text('Biz sizni malumotlarizi olib qoydik siz bilan boglanamiz !')

def help_command(update, context):
    update.message.reply_text('hi !')

def generateButtons(categories):
    buttons = []
    tmp_buttons = []
    for category in categories:
        tmp_buttons.append(
            InlineKeyboardButton(category.title,
            callback_data=f'category_{category.id}')
        )
        if len(tmp_buttons) == 2:
            buttons.append(tmp_buttons)
            tmp_buttons = []
    if len(tmp_buttons) > 0:
        buttons.append(tmp_buttons)

    return buttons

def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


