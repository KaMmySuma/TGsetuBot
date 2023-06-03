# -*- coding: UTF-8 -*-
import telebot
import setu
import time
import os
import pixiv
import html2text
from pprint import pprint


def main():
    global bot
    if os.path.exists("token.txt"):
        with open("token.txt", "r") as f:
            TOKEN = f.read()
    else:
        print("缺少token.txt")
        exit()
    bot = telebot.TeleBot(TOKEN)
    print("\n=============Start============")

    @bot.message_handler(commands=['start'])
    def start(message):
        bot.reply_to(message, "要...h的事吗？\n /setu -抽取一张随机涩图~。\n /setu_r18 -不够涩！抽取一张r18涩图。\n /pixiv_ranking -获取p站排行榜前5名的作品；私聊中可添加参数num=？自定义数量：例：/pixiv_ranking num=3。\n /pixiv_ranking_r18 -获取p站r18排行榜前5名的作品；私聊中可添加参数num=？自定义数量：例：/pixiv_ranking_r18 num=3。")
        bot.send_message(message.chat.id, "为避免刷屏，以下命令私聊可用（注意空格）：\n /pixiv_id 插画ID -获取指定pid的全部插画。\n /pixiv_search 关键词 -进行关键词搜索，默认获取前5个结果，可添加参数num=？自定义数量：例：/pixiv_search 猫娘 num=3。")

    @bot.message_handler(commands=['fetch_tg_user_by_id'])
    def fetch_tg_user_by_id(message):
        user_id = message.text.split(" ")[1]
        user = bot.get_chat(user_id)
        if user.type == "private":
            button = telebot.types.InlineKeyboardButton(text="查看用户详情", url='tg://user?id={0}'.format(user_id))
            if user.username:
                bot.send_message(message.chat.id, "@" + user.username,
                                 reply_markup=telebot.types.InlineKeyboardMarkup(keyboard=[[button]]))
            else:
                bot.send_message(message.chat.id, "用户未设置用户名",
                                 reply_markup=telebot.types.InlineKeyboardMarkup(keyboard=[[button]]))
        elif user.type == "group":
            if user.invite_link:
                button = telebot.types.InlineKeyboardButton(text="查看群详情", url=user.invite_link)
                bot.send_message(message.chat.id, "这是一个群组：" + user.title,
                                 reply_markup=telebot.types.InlineKeyboardMarkup(keyboard=[[button]]))
            else:
                bot.send_message(message.chat.id, "群组未设置或无权限访问邀请链接，群组：" + user.title)
        elif user.type == "supergroup":
            bot.send_message(message.chat.id, "@" + user.username)

    @bot.message_handler(commands=['setu'])
    def send_setu(message):
        r18 = 2  # 1:r18，2:全部
        '''if 'r18' in message.text:
            r18 = 1'''
        bot.reply_to(message, "小咪啪祈祷中......")
        print(time.time(), "，chat_id：", message.chat.id, "，开始获取色图...")
        data = setu.fetch_setu(r18)
        photo = data['data'][0]['urls']['original']
        try:
            bot.send_photo(message.chat.id, photo)
            '''if r18 == 1:
                bot.send_message(message.chat.id, "你选择了只发送r18色图，如果想要发送全部色图，请使用 /setu")
            else:
                bot.send_message(message.chat.id, "你选择了发送全部色图，如果想要只发送r18色图，请使用 /setu_r18")'''
        except Exception as e:
            print(e)
            bot.reply_to(message, "小咪啪抽风啦，再试一次叭QAQ")
            print(time.time(), "，chat_id：", message.chat.id, "，获取失败！")

    @bot.message_handler(commands=['setu_r18'])
    def send_setu(message):
        r18 = 1  # 1:r18，2:全部
        '''if 'r18' in message.text:
            r18 = 1'''
        bot.reply_to(message, "小咪啪祈祷中......")
        print(time.time(), "，chat_id：", message.chat.id, "，开始获取色图...")
        data = setu.fetch_setu(r18)
        photo = data['data'][0]['urls']['original']
        try:
            bot.send_photo(message.chat.id, photo)
            '''if r18 == 1:
                bot.send_message(message.chat.id, "你选择了只发送r18色图，如果想要发送全部色图，请使用 /setu")
            else:
                bot.send_message(message.chat.id, "你选择了发送全部色图，如果想要只发送r18色图，请使用 /setu_r18")'''
        except Exception as e:
            print(e)
            bot.reply_to(message, "小咪啪抽风啦，再试一次叭QAQ")
            print(time.time(), "，chat_id：", message.chat.id, "，获取失败！")
            
    @bot.message_handler(commands=['pixiv_ranking'])
    def send_pixiv_ranking(message):
        # 提取请求参数
        num = 5  # 默认10条
        r18 = False  # 默认不发送r18
        if 'num=' in message.text:
            num = int(message.text.split('num=')[1])
        '''if 'r18' in message.text:
            r18 = True'''

        bot.reply_to(message, "小咪啪祈祷中...正在获取pixiv排行榜...")
        print(time.time(), "，chat_id：", message.chat.id, "，开始获取pixiv...")
        try:
            api = pixiv.pixiv_login()
            mode = "day"
                
            for now_item in range(0, num):
                # item_cover_img 存储的是图片的url
                # item_pixiv_id 存储的是插画的id
                item_cover_img = pixiv.deal_ranking(api.illust_ranking(mode), now_item)
                item_pixiv_id = api.illust_ranking(mode)['illusts'][now_item]['id']

                bot.send_message(message.chat.id, "正在发送pixiv排行榜第" + str(now_item + 1) + "张...")
                button = telebot.types.InlineKeyboardButton(text="查看详情", callback_data="pixiv_" + str(item_pixiv_id))

                message_sent = bot.send_photo(message.chat.id, pixiv.download_illust(item_cover_img),
                                              reply_markup=telebot.types.InlineKeyboardMarkup(keyboard=[[button]]))

        except Exception as e:
            print(e)
            bot.reply_to(message, "小咪啪抽风啦，再试一次叭QAQ")
            print(time.time(), "，chat_id：", message.chat.id, "，获取失败！")

    @bot.message_handler(commands=['pixiv_ranking_r18'])
    def send_pixiv_ranking(message):
        # 提取请求参数
        num = 5  # 默认10条
        r18 = True  # 默认发送r18
        if 'num=' in message.text:
            num = int(message.text.split('num=')[1])
        '''if 'r18' in message.text:
            r18 = True'''

        bot.reply_to(message, "小咪啪祈祷中...正在获取pixiv排行榜...你选择了r18模式！")
        print(time.time(), "，chat_id：", message.chat.id, "，开始获取pixiv...")
        try:
            api = pixiv.pixiv_login()
            mode = "day_r18"
            for now_item in range(0, num):
                # item_cover_img 存储的是图片的url
                # item_pixiv_id 存储的是插画的id
                item_cover_img = pixiv.deal_ranking(api.illust_ranking(mode), now_item)
                item_pixiv_id = api.illust_ranking(mode)['illusts'][now_item]['id']

                bot.send_message(message.chat.id, "正在发送pixiv排行榜第" + str(now_item + 1) + "张...")
                button = telebot.types.InlineKeyboardButton(text="查看详情", callback_data="pixiv_" + str(item_pixiv_id))

                message_sent = bot.send_photo(message.chat.id, pixiv.download_illust(item_cover_img),
                                              reply_markup=telebot.types.InlineKeyboardMarkup(keyboard=[[button]]))

        except Exception as e:
            print(e)
            bot.reply_to(message, "小咪啪抽风啦，再试一次叭QAQ")
            print(time.time(), "，chat_id：", message.chat.id, "，获取失败！")

    @bot.message_handler(commands=['pixiv_id'])
    def get_detail_by_id(message):
        bot.reply_to(message, "小咪啪祈祷中......")
        api = pixiv.pixiv_login()
        detail = pixiv.get_pixiv_detail(api, message.text.split(' ')[1])
        p, caption, caption_not_empty, original_image_urls = pixiv.handle_pixiv_detail(detail)
        # 发送消息
        if caption_not_empty:
            bot.send_message(message.chat.id, caption, parse_mode="Markdown")
        bot.send_message(message.chat.id, p)
        j = 1  # 图片序号
        for i in original_image_urls:
            bot.send_message(message.chat.id, "正在发送第" + str(j) + "张...")
            bot.send_photo(message.chat.id, pixiv.download_illust(i))
            j += 1
        bot.send_message(message.chat.id, "获取详情完成！")
        print(time.time(), "，chat_id：", message.chat.id, "，获取详情完成！")

    @bot.message_handler(commands=['pixiv_search'])
    def pixiv_search(message):
        word = message.text.split(' ')[1]
        num = 5  # 默认5条
        if 'num=' in message.text:
            num = int(message.text.split('num=')[1])
        api = pixiv.pixiv_login()
        search_data = api.search_illust(word)

        index = 0
        if num > 15:
            num = 15
            bot.send_message(message.chat.id, "搜索结果超过15条，只显示前15条~")

        for id in pixiv.handle_search_illust(search_data):
            # 检测是否超过num
            index += 1
            if index > num:
                break

            bot.send_message(message.chat.id, "小咪啪祈祷中......")
            detail = pixiv.get_pixiv_detail(api, id)
            # 封面图片
            cover_img = detail['illust']['image_urls']['large']
            # 发送消息
            button = telebot.types.InlineKeyboardButton(text="查看详情", callback_data="pixiv_" + str(id))
            bot.send_photo(message.chat.id, pixiv.download_illust(cover_img),
                           reply_markup=telebot.types.InlineKeyboardMarkup(keyboard=[[button]]))

    @bot.callback_query_handler(func=lambda call: True)
    def handle_callback(call):
        bot.send_message(call.message.chat.id, "正在获取详情...请勿重复点击")
        api = pixiv.pixiv_login()

        # 提取插画id
        pixiv_id = call.data.split("_")[1]
        detail = pixiv.get_pixiv_detail(api, pixiv_id)
        p, caption, caption_not_empty, original_image_urls = pixiv.handle_pixiv_detail(detail)

        # 发送消息
        if caption_not_empty:
            bot.send_message(call.message.chat.id, caption, parse_mode="Markdown")
        bot.send_message(call.message.chat.id, p + "\n——————\n私聊小咪啪发送 “/pixiv_id 插画ID” 以获取指定作品下全部插画")
        
    bot.polling()
