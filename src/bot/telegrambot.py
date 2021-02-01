from telegram.ext import CommandHandler, MessageHandler, Filters

from .models import Category, Region, User, District, Order, UserCategory

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
    print('user: ', tg_user.id)
    print('user: ', user)
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
        return category(update, context)
    elif query.data == '2':
        return category_2(update, context)

def get_phone_number(update: Update, context: CallbackContext):

    text = 'Telefon nomeringizni kiriting: '
    contact_number = KeyboardButton(text="Contact", request_contact=True)
    update.message.reply_text(text, reply_markup=ReplyKeyboardMarkup([[contact_number]]))


    return 8
# need change

def get_phone_number_2(update: Update, context: CallbackContext):
    query = update.callback_query
    text = 'Telefon nomeringizni kiriting: '
    contact_number = KeyboardButton(text="Contact", request_contact=True)
    query.delete_message()
    context.bot.send_message(query.from_user.id, text, reply_markup=ReplyKeyboardMarkup([[contact_number]], resize_keyboard=True))
    print('get_phone_number_2')

    return 8
        
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
    datas= query.data.split('_')
    tg_user = query.from_user
    if datas[0] == 'category':
        cat_id = int(datas[1])
        context.user_data['category_id_2 :'] = cat_id
    try:
        user = User.objects.get(tg_id=tg_user.id)
    except Exception:
        user = None

    user_category = UserCategory(user_id_id=user.id, cat_id_id=context.user_data['category_id_2 :'])
    user_category.save()
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


def category(update: Update, context: CallbackContext) :

    query = update.callback_query
    context.user_data['type']= query.data
    datas = query.data.split('_')
    childs = Category.objects.all()
    buttons = generateButtons(childs)
    # info = f"type:{context.user_data['type']}"
    query.message.delete()
    query.message.reply_text(
    'birortasini tanlang:', reply_markup=InlineKeyboardMarkup(buttons)
    )
    return 4

def descriptions(update: Update, context: CallbackContext):
    query = update.callback_query
    datas = query.data.split('_')
    if datas[0] == 'category':
        cat_id = int(datas[1])
        context.user_data['category_id :'] = cat_id
        print(context.user_data['category_id :'])
    
    text = 'Ish xaqida qisqacha malumot yozing'
    query.message.reply_text(text)
    return 5

def region_2(update: Update, context: CallbackContext):
    query = update.callback_query
    regions = Region.objects.all()
    buttons= generateButtons(regions)
    
    query.message.reply_text(
        'Qaysi Viloyatdansz: ', 
        reply_markup=InlineKeyboardMarkup(buttons)
    )
    print('region 2')
    return 14

def region(update: Update, context: CallbackContext):
    user = update.message
    context.user_data['description :'] = user.text
    regions = Region.objects.all()
    buttons= generateButtons(regions)
    
    update.message.reply_text(
        'Qaysi Viloyatdansz: ', 
        reply_markup=InlineKeyboardMarkup(buttons)
    )
    print('region 1')
    return 6

def district(update: Update, context: CallbackContext):

    query = update.callback_query
    context.user_data['region_id :'] = query.data
    tg_user = query.from_user
    datas = query.data.split('_')
    if datas[0] == 'category':
        cat_id = int(datas[1])
        context.user_data['region_id :'] = cat_id
        disct = District.objects.raw('SELECT * FROM bot_district where region_id=%s',[cat_id])
        buttons= generateButtons(disct)
    query.message.delete()
    query.message.reply_text(
        'Qaysi tumandansz: ', 
        reply_markup=InlineKeyboardMarkup(buttons)
    )

    return 7

def district_2(update: Update, context: CallbackContext):

    query = update.callback_query
    tg_user = query.from_user
    datas = query.data.split('_')
    if datas[0] == 'category':
        cat_id = int(datas[1])
        disct = District.objects.raw('SELECT * FROM bot_district where region_id=%s',[cat_id])
        buttons= generateButtons(disct)
    query.message.delete()
    print(buttons)
    query.message.reply_text(
        'Qaysi tumandansz: ',
        reply_markup=InlineKeyboardMarkup(buttons)
    )
    return 15

def check_phone(update: Update, context: CallbackContext):
    print('check_phone')
    query = update.message
    
    context.user_data['location :']= query.location
    tg_user = query.from_user
    try:
        user = User.objects.get(tg_id=tg_user.id)
    except Exception:
        user = None


    if user.phone:
        return last(update, context)
    else:
        return get_phone_number(update, context)

def check_phone_2(update: Update, context: CallbackContext):
    query = update.callback_query
    tg_user = query.from_user
    try:
        user = User.objects.get(tg_id=tg_user.id)
    except Exception:
        user = None


    if user.phone:
        query.edit_message_text('Biz sizni malumotlarizi olib qoydik siz bilan boglanamiz !')
    else:
        return get_phone_number_2(update, context)

def locations(update, context):
    query = update.callback_query
    datas = query.data.split('_')
    if datas[0] == 'category':
        cat_id = int(datas[1])
        context.user_data['distcrit_id :'] = cat_id

    location_keyboard = KeyboardButton(text="send location",  request_location=True)
    query.message.reply_text('lacation tashlang!', reply_markup=ReplyKeyboardMarkup([[location_keyboard]]))
    
    return 13

def last(update, context):
    # tg_user = update.message.from_user
    # phone_user = update.message
    query = update.message
    # tg_user = query.data
    try:
        user = User.objects.get(tg_id=query.from_user.id)
    except Exception:
        user = None

    if not user.phone:
        user.phone=phone_user.contact.phone_number
        user.save()

    print('saving....')
    order = Order(user_id=user.id , 
            cat_id=context.user_data['category_id :'], 
            description=context.user_data['description :'], 
            location=context.user_data['location :'], 
            Region_id=context.user_data['region_id :'], 
            district_id=context.user_data['distcrit_id :'])
    order.save()
    ordering = Order.objects.filter(cat_id=context.user_data['category_id :'])
    context.bot.send_message(ordering, f'oka ish bor...\n{order.description}')
    context.bot.send_message(1304604274, f'oka ish bor...\n{order.description}')
    print('saved')

    info = f"category_id{context.user_data['category_id :']}\n description{context.user_data['description :']}\n region{context.user_data['region_id :']}\n district{context.user_data['distcrit_id :']}\n location{context.user_data['location :']}"
    update.message.reply_text(info)

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


