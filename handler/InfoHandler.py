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

import pandas as pd

SELECT_TASK , SELECT_TASK_DETAIL, SELECT_TASK_DETAIL_2= range(3)

class InfoHandler():
    def __init__(self, gm):
        
        #GsheetsManager
        self.gm = gm


        self.handler = ConversationHandler(
            entry_points = [CallbackQueryHandler(self.handle_start, pattern='^info$')],
            states ={
                SELECT_TASK :[CallbackQueryHandler(self.handle_get_task)],
                SELECT_TASK_DETAIL:[CallbackQueryHandler(self.handle_get_task_detail)],
                SELECT_TASK_DETAIL_2 :[CallbackQueryHandler(self.get_info)]
            },
            fallbacks=[CommandHandler('cancel', self.cancel)]
        )

    def get_help(self):
        return [InlineKeyboardButton("행정 정보 확인", callback_data= "info")]
    
    def get_handler(self) :
        #Telegram Manager 36~37 line
        return self.handler
    
    async def cancel(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Display the gathered info and end the conversation."""
        context.user_data.clear()
        await update.message.reply_text("취소 되었습니다.")
        return ConversationHandler.END
    
    async def handle_start(self,update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()

        #context.user_data['telegramID'] = update.effective_chat.id

        keyboard=[]
        task_list = self.gm.get_df_to_list("administrative_task_code","list")
        for task in task_list:
            keyboard.append([InlineKeyboardButton(task[1], callback_data=task[0])])
        
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text("행정 정보를 확인하고싶은 사업(과제)을 선택해주세요", reply_markup=reply_markup)

        return SELECT_TASK
  


    async def handle_get_task(self,update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()

        info_df = self.gm.get_df_to_list("info_structure","df")
        filter_rows = info_df[info_df['code'] == query.data]

        context.user_data['filter_df'] = filter_rows

        detailed_task = filter_rows['비목'].tolist()
        unique_detailed_task = list(dict.fromkeys(detailed_task))

        keyboard=[]
        for item in unique_detailed_task:
            keyboard.append([InlineKeyboardButton(item, callback_data=item)])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        task_name =list(set(filter_rows['행정명']))
        
        await query.edit_message_text(f"{task_name[0]} 선택하셨습니다.\n관련 행정 중 확인할 비목을 선택해주세요",reply_markup=reply_markup)

        return SELECT_TASK_DETAIL
                             
    async def handle_get_task_detail(self,update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()

        filter_rows = context.user_data['filter_df']

        filter_rows = filter_rows[filter_rows['비목'] == query.data]
        context.user_data['filter_df'] = filter_rows

        detailed_task = filter_rows['비목상세'].tolist()
        
        keyboard=[]
        for item in detailed_task:
            keyboard.append([InlineKeyboardButton(item, callback_data=item)])
        
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(f"{query.data}를 선택하셨습니다.\n어떤 항목을 확인하시겠습니까?",reply_markup=reply_markup)
    
        return SELECT_TASK_DETAIL_2                       


    async def get_info(self,update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer() 

        filter_rows = context.user_data['filter_df']


        new_filter_rows = filter_rows.drop(columns =['code', '행정명', '비목', '비목상세'])

        text = self.convert_df_to_text(new_filter_rows)
        await query.edit_message_text(f"행정명 : {filter_rows['행정명'].iloc[0]}\n비목 : {filter_rows['비목'].iloc[0]}\n비목 상세 : {filter_rows['비목상세'].iloc[0]}\n\n"+text)

        return ConversationHandler.END

    def convert_df_to_text(self, df):
        text = ""
        for _, row in df.iterrows():
            for column, value in row.items():
                text += f"[{column}]\n{value}\n"
            text += "\n\n"
        return text
