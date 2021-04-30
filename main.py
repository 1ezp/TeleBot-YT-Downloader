import telebot
import time,json,requests
import youtube_dl

bot_token = "Bot token"
bot = telebot.TeleBot(token=bot_token)






@bot.message_handler(commands=["start"])
def send_welcome(message):
    try:
        members = bot.get_chat_member(chat_id='@h_ccz',user_id=str(message.chat.id))
        if "'status': 'member'" in str(members) or "'status': 'creator'" in str(members) or "'status': 'administrator'" in str(members):
            bot.send_message(message.chat.id,"أرسل رابط الفيديو لتحميله.")
        else:
            bot.reply_to(message,"أولاً يجب الأشترك في قناة البوت\n@h_ccz")
    except:
        pass


@bot.message_handler(func= lambda msg: msg.text is not None and "https://" in msg.text)
def send_media(message):
    try:
        members = bot.get_chat_member(chat_id='@h_ccz',user_id=str(message.chat.id))

        if "'status': 'member'" in str(members) or "'status': 'creator'" in str(members) or "'status': 'administrator'" in str(members):
            video_url = message.text
            bot.send_message(message.chat.id,"جاري تحميل الفيديو وتحويله ...")
            video_info = youtube_dl.YoutubeDL().extract_info(url=video_url, download=False)
            for f in video_info['formats']:
                if f['ext'] == 'm4a':

                    audi = requests.get(f['url']).content
                    break
            #print(audi)
            
            thum = requests.get(video_info['thumbnails'][0]['url']).content
            bot.send_audio(message.chat.id, audio = audi, performer = "@YTDOWONBOT", title = video_info['title'],thumb=thum,duration=video_info['duration'])


        else:
            bot.reply_to(message,"أولاً يجب الأشترك في قناة البوت\n@h_ccz")

    except:
        bot.reply_to(message,"هناك مشكلة في ارسال المقطع.")


while True:
    try:
        bot.polling(True)
    except Exception as e:
        print(e)
        time.sleep(2)
