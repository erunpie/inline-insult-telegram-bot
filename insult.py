import logging
import random
from telegram import Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
    CallbackQueryHandler, 
    InlineQueryHandler,
)
from telegram import InlineKeyboardButton, InlineKeyboardMarkup,InlineQueryResultArticle
from uuid import uuid4
import mysql.connector
from telegram.inline.inputtextmessagecontent import InputTextMessageContent


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

#اطلاعات دیتابیس خود را وارد کونید
mydb = mysql.connector.connect(
    host="",
    user="",
    password="",
    database=""
)
mycursor = mydb.cursor()

# enter your channel token and 
TOKEN = ''
CHANNEL=100

TEXT,CONFIRMATION,TYPE, NAME =range(4)


reply_keyboard_1 = [
    [InlineKeyboardButton("📍 پیشنهاد دشنام ", callback_data='111')], # suggest insult
    [InlineKeyboardButton("📍 روش استفاده ", callback_data='222')], # how to use
    [InlineKeyboardButton("📍  حمایت مالی  ", callback_data='333')],
]
reply_keyboard_2 = [
    [
    InlineKeyboardButton("🔴", callback_data='0'),
    InlineKeyboardButton("🟢", callback_data='1'),
    ],
    [InlineKeyboardButton("لغو", callback_data='2')],
]
reply_keyboard_3 = [
    [
    InlineKeyboardButton("🔴ناموسی", callback_data='0'),
    InlineKeyboardButton("🔴ترکیبی🔴", callback_data='1'),
    ],
    [
    InlineKeyboardButton("🟡پدری", callback_data='2'),
    InlineKeyboardButton("🟢معمولی", callback_data='3'),
    ],
    [InlineKeyboardButton("بازگشت⮐", callback_data='22')],
]
reply_keyboard_4=[
   [InlineKeyboardButton('بازگشت⮐',callback_data='5')],
]

reply_keyboard_5=[ 
   [
    InlineKeyboardButton('🟢',callback_data='10'),
    InlineKeyboardButton('🔴',callback_data='11'),
   ],
]
reply_keyboard_6=[
   [InlineKeyboardButton('لغو',callback_data='6')],
]
reply_keyboard_7=[
   [InlineKeyboardButton('برای جستجو روی من کلیک کنید', switch_inline_query_current_chat ='')],
   [InlineKeyboardButton('بازگشت⮐',callback_data='5')],
]

thumb_url=[
    'https://i.imgflip.com/3r7v68.jpg',

]
doshnam_hadis_list=[
    'ناسزاگويى به مؤمن، فسق است و جنگيدن با او، كفر .\n | كنز العمّال : ۸۰۹۴',
   'آرام باش قنبر! دشنام گوىِ خود را خوار و سرشكسته بگذار، تا خداى رحمان را خشنود و شيطان را ناخشنود كرده و دشمنت را كيفر داده باشى .\n |  الأمالي للمفيد : ۱۱۸/۲'
]
def start(update: Update, context: CallbackContext) :
    context.bot.send_message(chat_id=update.effective_user.id , text = random.choice(doshnam_hadis_list))
    update.message.reply_text('-- انتخاب کن --',reply_markup=InlineKeyboardMarkup(reply_keyboard_1))

def keyboards_handler(update: Update, context: CallbackContext) : 
    query= update.callback_query
    query.answer()
    if query.data == '111' :
       query.delete_message()
       context.bot.send_message(chat_id=update.effective_user.id , text ='لطفا نام دشنام خویش را ارسال کنید',reply_markup=InlineKeyboardMarkup(reply_keyboard_6)) 
       return NAME
    if query.data == '222':
       help='دا برای استفاده باید رو دکمه زیر کلیک کنید و کوصشر خودرا بنویسید تا نتیجه را ببینید'
       query.edit_message_text(help,reply_markup=InlineKeyboardMarkup(reply_keyboard_7))   
  
    if query.data == '333':
       hemaiat = 'برای حمایت مالی از ما می توانید از روش های زیر استفاده کنید 👇' + '\n\nPayPing : https://payping.ir/RezFD' + '\n\n IDPay : https://idpay.ir/persianmeme'
       query.edit_message_text( hemaiat,reply_markup=InlineKeyboardMarkup(reply_keyboard_4))
    if query.data == '5' :
       query.edit_message_text('-- انتخاب کن --',reply_markup=InlineKeyboardMarkup(reply_keyboard_1))
    

    #channel verification -----
    if query.data =='10':
        message = update.effective_message.text
        sql = "SELECT id FROM insult WHERE text = '%s' "% message
        mycursor.execute(sql)
        myresult = mycursor.fetchone()
        try:
            sql = "UPDATE insult SET status = 'True' WHERE text = '%s'"% message
            mycursor.execute(sql)
            mydb.commit()
            query.edit_message_text(str(message+'\nverified!'))
            try :
                context.bot.send_message(chat_id=myresult[0], text='دا دشنامت تایید شد ✅ حالا می تونی ازش استفاده کنی')
            except:
                pass
        except:
            context.bot.send_message(chat_id=CHANNEL, text='failed to change status ')     
    if query.data =='11':
            not_verified_msg ='دا به دلیل اینکه کیرمون کلفته دشنامت تایید نشد حالا می تونی گریه کنی' 
            query.edit_message_text(str(message +'\n not verified'))
            try:
               context.bot.send_message(chat_id=myresult[0], text=not_verified_msg)
            except :
                pass
    # --------------------------
       
def name(update: Update , context: CallbackContext):
    context.user_data['insult_name']=update.message.text
    context.bot.send_message(chat_id = update.effective_user.id ,text='دشنام مورد نظر را ارسال کون و کمتر از 4095 کاراکتر باشد',reply_markup=InlineKeyboardMarkup(reply_keyboard_6))
    return TEXT
def text(update: Update , context: CallbackContext): 
    if len (update.message.text) > 4095 : 
        update.message.reply_text('متن دشنامی که دادی بلنده دوباره امتحان کن')
        return TEXT
    if len(update.message.text) <= 4095 :
        #insult len and insult itself 
        context.user_data['insult'] =  update.message.text
        context.user_data['insult_len']  = str(len(update.message.text))
        reply_markup =InlineKeyboardMarkup(reply_keyboard_3)
        update.message.reply_text('مدل دشنام خویش را گزینش کنید ...',reply_markup=reply_markup)
        return TYPE
#insult type
def type(update: Update , context : CallbackContext):
    query = update.callback_query
    query.answer()
    reply_markup =InlineKeyboardMarkup(reply_keyboard_2)
    if query.data == '0':
        context.user_data['insult_type']='ناموسی'
        query.edit_message_text('نوع دشنام  : --:: %s ::-- \n آیا تمام اطلاعات دشنامت درست بود ؟'%(context.user_data['insult_type']),reply_markup=reply_markup)
        return CONFIRMATION
    if query.data == '1':
        context.user_data['insult_type']='ترکیبی'
        query.edit_message_text('نوع دشنام  : --:: %s ::-- \n آیا تمام اطلاعات دشنامت درست بود ؟'%(context.user_data['insult_type']),reply_markup=reply_markup)
        return CONFIRMATION
    if query.data == '2':
        context.user_data['insult_type']='پدری'
        query.edit_message_text('نوع دشنام  : --:: %s ::-- \n آیا تمام اطلاعات دشنامت درست بود ؟'%(context.user_data['insult_type']),reply_markup=reply_markup)
        return CONFIRMATION
    if query.data == '3':
        context.user_data['insult_type']='معمولی'
        query.edit_message_text('نوع دشنام  : --:: %s ::-- \n آیا تمام اطلاعات دشنامت درست بود ؟'%(context.user_data['insult_type']),reply_markup=reply_markup)
        return CONFIRMATION
    #RETURN STATE ...
    if query.data == '22':
      query.edit_message_text('نام دشنام را ارسال کون',reply_markup=InlineKeyboardMarkup(reply_keyboard_6))
      context.user_data.clear()
      return NAME


def confirmation(update : Update, context : CallbackContext):
    query = update.callback_query 
    query.answer()
    content = context.user_data['insult'] 
    type = context.user_data['insult_type']
    name = context.user_data['insult_name']
    if query.data == '0':
        query.edit_message_text('متنی جدید ارسال نما',reply_markup=InlineKeyboardMarkup(reply_keyboard_6))
        return TEXT
    if query.data == '1':
        sql = "SELECT text FROM insult "
        mycursor.execute(sql)
        myresult = mycursor.fetchall() 
        if content in myresult :
            query.edit_message_text('در حال حاضر این فوش موجود است لطفا کرم نریزید ')

        else:

            user_id = update.effective_user.id
            try:
                sql = "INSERT INTO insult (id, name, text, len, type ,status ) VALUES (%s, %s, %s, %s, %s, %s)"
                val = (user_id ,context.user_data['insult_name'], context.user_data['insult'],context.user_data['insult_len'], context.user_data['insult_type'],'False' )
                mycursor.execute(sql, val)
                mydb.commit()
                query.edit_message_text('برای تایید باید صبرکنید')
                context.bot.send_message(chat_id = CHANNEL , text = '〰〰〰〰〰〰〰〰〰〰〰')
                context.bot.send_message(chat_id = CHANNEL , text = type)
                context.bot.send_message(chat_id = CHANNEL , text = name)
                context.bot.send_message(chat_id=CHANNEL, text = content ,reply_markup =InlineKeyboardMarkup(reply_keyboard_5))
                
            except:
                context.bot.send_message(chat_id = update.effective_user.id ,text ='دا به مشکل بر خورد کردیم نشد دوباره امتحان کن ')

        context.bot.send_message(chat_id=update.effective_user.id , text = random.choice(doshnam_hadis_list))
        context.bot.send_message(chat_id=update.effective_user.id ,text='-- انتخاب کن --',reply_markup=InlineKeyboardMarkup(reply_keyboard_1))
        return ConversationHandler.END

    if query.data == '2':
       query.delete_message()
       context.bot.send_message(chat_id=update.effective_user.id , text = random.choice(doshnam_hadis_list))
       context.bot.send_message(chat_id=update.effective_user.id , text = '-- انتخاب کن --' ,reply_markup=InlineKeyboardMarkup(reply_keyboard_1 ))
    
       context.user_data.clear()
       return ConversationHandler.END   




def cancel (update: Update, context: CallbackContext):
    query=update.callback_query
    query.answer()
    if query.data == '6':
       query.delete_message()
       context.bot.send_message(chat_id=update.effective_user.id , text = random.choice(doshnam_hadis_list))
       context.bot.send_message(chat_id=update.effective_user.id , text = '-- انتخاب کن --' ,reply_markup=InlineKeyboardMarkup(reply_keyboard_1 ))
    
    return ConversationHandler.END




def search_engine(query): 
    search_dic={}
    query_string = str(query)
    mycursor.execute("SELECT text,type,name FROM insult WHERE status ='True'")
    myresult = mycursor.fetchall()
    # -- i -- in down is equal by text in database
    # --- i [0] = text and i [1] = type
    # -----i [1] = name
    # {text : (type , name)}
    for i in myresult :
        if query_string in i[0] :
            search_dic.update({i[0] : i[1:3]})
        else :
            pass
    return search_dic

def inlinequery(update:Update, context:CallbackContext):
    query=update.inline_query.query
    inline_results = list()
    # {text : (type , name)}
    results = search_engine(query)
    
    for i in results :
        string =' '
        preview_lst=i.split()
        preview_txt = string.join(preview_lst[0:9])
        descreption ='type :'+results[i][0]+'  length :'+str(len(i))+'char\npreview : %s'% preview_txt
        inline_results.append(InlineQueryResultArticle(id=uuid4(),
                                                       title= results[i][1] ,
                                                       input_message_content=InputTextMessageContent(i),
                                                       thumb_url=random.choice(thumb_url),
                                                       description=descreption)
                                                       )

    update.inline_query.answer(inline_results[:40])



def main() :
   
    updater = Updater(TOKEN)

   
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start',start,run_async=True))
  

    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(keyboards_handler ,run_async=True)],
        states={
            NAME:[MessageHandler(Filters.text , name , run_async=True)],
            TEXT: [MessageHandler(Filters.text , text, run_async=True)],
            TYPE: [CallbackQueryHandler(type, run_async=True)],
            CONFIRMATION:[CallbackQueryHandler(confirmation, run_async=True)] 
        },
        fallbacks=[CallbackQueryHandler(cancel ,run_async=True)],  
    )

    dispatcher.add_handler(conv_handler)
  
    dispatcher.add_handler(InlineQueryHandler(inlinequery ,run_async=True))
    
    #updater.start_webhook(listen='0.0.0.0',port=443,url_path='token')
    #updater.start_webhook('domain'+'token')
    updater.start_polling()
    

    updater.idle()


if __name__ == '__main__':
    main()


 