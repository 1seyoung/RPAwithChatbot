import re
import os
import shutil
from pathlib import Path


from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, InputFile,Update, ForceReply, InlineKeyboardButton, InlineKeyboardMarkup
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

SELECT_TASK, SELECT_TASK_DETAIL = range(2)
class FileHandler():
    def __init__(self, gm, config):
        self.gm =gm
        self.config = config


        self.handler = ConversationHandler(
            entry_points = [CallbackQueryHandler(self.handle_start, pattern='^file$')],
            states ={
                SELECT_TASK : [CallbackQueryHandler(self.handle_get_task)], 
                SELECT_TASK_DETAIL: [CallbackQueryHandler(self.handle_send_zip)]
            },
            fallbacks=[CommandHandler('cancel', self.cancel)]
        )

    def get_help(self):
        return [InlineKeyboardButton("문서 양식", callback_data= "file")]
    
    def get_handler(self) :
        #Telegram Manager 36~37 line
        return self.handler
    
    async def cancel(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Display the gathered info and end the conversation."""
        await update.message.reply_text("취소 되었습니다.")
        return ConversationHandler.END
    
    async def handle_start(self,update: Update, context: ContextTypes.DEFAULT_TYPE) :
        context.user_data['telegramID'] = update.callback_query.from_user.id

        query = update.callback_query
        await query.answer()

        folder_list = next(os.walk(self.config.doc_path))[1]

        subfolders = {}

        for i, folder in enumerate(os.listdir(self.config.doc_path)):
            folder_path = os.path.join(self.config.doc_path, folder)
            if os.path.isdir(folder_path):
                subfolders[i] = folder
        

        context.user_data['folder_structure']= subfolders

        keyboard =[]
        for idx, folder in subfolders.items():
            keyboard.append([InlineKeyboardButton(folder, callback_data=idx)])

        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text("정보를 확인하고싶은 사업(과제)을 선택해주세요", reply_markup=reply_markup)

        return SELECT_TASK
    
    async def handle_get_task(self,update: Update, context: ContextTypes.DEFAULT_TYPE) :
        query = update.callback_query
        await query.answer()

        select_idx = query.data
        selected_folder = context.user_data['folder_structure'].get(int(select_idx))
        sub_path = os.path.join(self.config.doc_path, selected_folder)

        subfolder_list = next(os.walk(sub_path))[1]  # 선택한 폴더의 하위 폴더 목록 가져오기

        subfolder = {}
        for i, folder in enumerate(os.listdir(sub_path)):
            folder_path = os.path.join(sub_path, folder)
            if os.path.isdir(folder_path):
                subfolder[i] = folder


        keyboard =[]
        for idx, folder in subfolder.items():
            keyboard.append([InlineKeyboardButton(folder, callback_data=idx)])

        context.user_data['folder_structure']= subfolder
        context.user_data['last_path'] = sub_path


        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text("필요한 항목을 선택해주세요", reply_markup=reply_markup)

        return SELECT_TASK_DETAIL

    async def handle_send_zip(self,update: Update, context: ContextTypes.DEFAULT_TYPE) :
        query = update.callback_query
        await query.answer()

        select_idx = query.data
        selected_folder = context.user_data['folder_structure'].get(int(select_idx))
        sub_path = os.path.join(context.user_data['last_path'], selected_folder)

        last_token = os.path.basename(sub_path)

        zip_filename = f"{last_token}.zip"


        folder_path = sub_path  # 압축할 폴더의 경로로 대체하세요
        folder_path = os.path.normpath(folder_path)  # 경로를 표준화합니다
        folder_name = os.path.basename(folder_path)
        file_list = os.listdir(folder_path)

        # 압축 파일 경로
        zip_file_path = f"{folder_name}.zip"

        if os.path.exists(zip_file_path):
            # 이미 압축된 파일이 존재하는 경우, 파일을 전송하거나 처리하는 로직을 추가하세요
            print("exists zip file")
        else:
            # 압축 파일 생성
            shutil.make_archive(folder_name, "zip", folder_path)
            print("압축 파일이 생성되었습니다.")

        file_text = "\n".join(file_list)
        await query.edit_message_text(f"[양식 목록]\n{file_text}")

        with open(zip_filename, "rb") as file:
            await context.bot.send_document(chat_id=context.user_data['telegramID'], document=InputFile(file))

        return ConversationHandler.END
        