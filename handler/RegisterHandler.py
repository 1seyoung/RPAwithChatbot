import re


from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, ForceReply, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
    CallbackQueryHandler,
    CallbackContext
)

#conversationhandler state
NAME, CODE, TELEGRAM_ID, E_MAIL, CONFIRM= range(5)
class RegisterHandler():
    """
    This module defines the RegisterHandler class, which utilizes the ConversationHandler feature of the python-telegram-bot library.

    The RegisterHandler class is responsible for gathering user information such as gender, Telegram ID, name, and code.

    This Handler is managed by the TelegramManager.

    Each method in this module that starts with 'handle_' is activated at a specific state in the conversation.
    """
    def __init__(self, gm):

        #GsheetManager class define
        self.gm = gm
        


        self.handler = ConversationHandler(
            entry_points =[CommandHandler('register', self.handle_start)],
            states ={
                CODE : [MessageHandler(filters.TEXT & ~(filters.COMMAND), self.handle_get_code)],
                NAME : [MessageHandler(filters.TEXT & ~(filters.COMMAND), self.handle_get_name)],
                E_MAIL : [MessageHandler(filters.TEXT & ~(filters.COMMAND), self.handle_get_email)],
                CONFIRM : [CallbackQueryHandler(self.handle_get_confirm)]
            },
            fallbacks=[CommandHandler('cancel', self.cancel)]
        )

    def get_help(self):
        #explain the role of handler

        return "/register : 사용자 등록"
    
    def get_handler(self) :
        #Telegram Manager 36~37 line
        return self.handler
    
    async def cancel(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Display the gathered info and end the conversation."""
        context.user_data.clear()
        await update.message.reply_text("취소 되었습니다.")
        return ConversationHandler.END
    
    async def handle_start(self,update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.message.chat.type == "private":
            await update.message.reply_text('교번(학번)을 입력해주세요')   
            context.user_data['telegramID'] = update.effective_chat.id

            return CODE
        
        else:
            return ConversationHandler.END

    
    async def handle_get_code(self,update: Update, context: ContextTypes.DEFAULT_TYPE):
        code = int(update.message.text)
        context.user_data['EmployeeID'] = code
        await update.message.reply_text('성명을 입력해주세요')
        return NAME
    
    async def handle_get_name(self,update: Update, context: ContextTypes.DEFAULT_TYPE):
        name = update.message.text
        context.user_data['Name'] = name
        await update.message.reply_text('한밭대학교 이메일 주소를 입력해주세요')

        return E_MAIL

    async def handle_get_email(self,update: Update, context: ContextTypes.DEFAULT_TYPE):
        email = update.message.text

        if self.validate_email(email):
            context.user_data['E-mail'] = email

            await update.message.reply_text(f"[신청정보]\n성명 : {context.user_data['Name']}\n교번(학번) : {context.user_data['EmployeeID']}\n이메일 : {context.user_data['E-mail']}")

            keyboard = [
                    [
                        InlineKeyboardButton("예", callback_data= "yes"),
                        InlineKeyboardButton("아니오", callback_data= "no"),
                    ]
                ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            await update.message.reply_text('위 정보로 승인 신청을 진행하시겠습니까?\n수정을 원하시면 아니오를 클릭해주세요\n사용자 등록 종료를 원한다면 /cancel 입력', reply_markup=reply_markup)

            return CONFIRM

        else:
            await update.message.reply_text('이메일이 유효하지 않습니다. 다시 입력해주세요.')
            return E_MAIL
        
    async def handle_get_confirm(self,update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()

        admin_info_list = self.gm.get_admin_info()
        
        send_text=[]
        for admin in admin_info_list:
            appended_text = admin[0] + ": " + admin[3] + "\n"
            send_text.append(appended_text)

        # Join all the lines into a single string
        message = ''.join(send_text)


        if query.data =="yes":
            

            '''info =[Name, EmployeeID,	TelegramID, E-mail, Approval Status, Permission'''
            info = [context.user_data['Name'], context.user_data['EmployeeID'], context.user_data['telegramID'], context.user_data['E-mail'], "승인대기", "Guest"]
            self.gm.update_table("user", info)

            await query.edit_message_text(text="신청이 완료되었습니다\n문의 :"+message)
            
            for admin in admin_info_list:
                admin_telegram_id = admin[2]
                await context.bot.send_message(chat_id=admin_telegram_id, text= f"{context.user_data['Name']}님이 사용을 신청하였습니다.\n확인 후 승인 절차를 진행해주세요 ")

            return ConversationHandler.END
        elif query.data == "no":
            await query.edit_message_text('사용자 등록을 다시 시작합니다.') 
            await context.bot.send_message(chat_id=context.user_data['telegramID'], text= '교번(학번)을 입력해주세요')

            return CODE


    
    def validate_email(self,email):
        # 이메일 패턴 정의
        email_regex = r"[^@]+@[^@]*hanbat+\.[^@]+"

        # 패턴과 이메일이 일치하는지 확인
        if re.match(email_regex, email):
            return True
        else:
            return False