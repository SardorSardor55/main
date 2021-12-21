from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import CommandHandler, MessageHandler, Filters, Updater, CallbackQueryHandler

from servise import create_table, create_user, get_one

vil = ["🌇 Tashkent", "Andijon🌇", "🌇 Sirdaryo", "Samarqand🌇", "🌇 Namangan", "Xorazm🌇", "🌇 Farg'ona",
       "Jizzax🌇", "🌇 Surxondaryo", "Buxoro🌇", "🌇 Navoiy", "Qashqadaryo🌇"]


def btns(tip=None):
    bts = []
    if tip == "contact":
        bts.append([KeyboardButton("Raqamingizni kiritni", request_contact=True)])
    elif tip == "lang":
        bts = [
            [KeyboardButton("🇺🇿 Uzbek tili")],
            [KeyboardButton("🇷🇺 Руский язык")],
            [KeyboardButton("🇺🇸 English")],
        ]
    elif tip == "viloyat":
        bts = [
            [KeyboardButton("🌇 Tashkent"), KeyboardButton("🌇 Farg'ona")],
            [KeyboardButton("Andijon🌇"), KeyboardButton("Jizzax🌇")],
            [KeyboardButton("🌇 Sirdaryo"), KeyboardButton("🌇 Surxondaryo")],
            [KeyboardButton("Samarqand🌇"), KeyboardButton("Buxoro🌇")],
            [KeyboardButton("🌇 Namangan"), KeyboardButton("🌇 Navoiy")],
            [KeyboardButton("Xorazm🌇"), KeyboardButton("Qashqadaryo🌇")]
        ]
    elif tip == "menu":
        bts = [
            [KeyboardButton("🛒 Buyurtma qilish")],
            [KeyboardButton("🛍 Buyurtmalarim"), KeyboardButton("👪 EVOS Oilasi")],
            [KeyboardButton("✍️ Fikr bildirish"), KeyboardButton("⚙️ Sozlamalar")]
        ]
    return ReplyKeyboardMarkup(bts, resize_keyboard=True)


def inline_btns(tip=None, btn_type=None, ctg=None):
    if btn_type == "tur":
        btn = [
            [InlineKeyboardButton(f"🥩 Gushtli", callback_data=f"{ctg}_gusht"),
             InlineKeyboardButton(f"🍗 Tovuqli", callback_data=f"{ctg}_tovuq")]
        ]
    elif btn_type == "number":
        btn = []
        for i in range(1, 8, 3):
            btn.append([
                InlineKeyboardButton(f"{i}", callback_data=f"{ctg}_{tip}_{i}"),
                InlineKeyboardButton(f"{i + 1}", callback_data=f"{ctg}_{tip}_{i + 1}"),
                InlineKeyboardButton(f"{i + 2}", callback_data=f"{ctg}_{tip}_{i + 2}")
            ])
    elif btn_type == "ich":
        btn = [
            [InlineKeyboardButton(f"Cola1.5L ", callback_data=f"{ctg}_cola"),
             InlineKeyboardButton(f"Fanta1.5L", callback_data=f"{ctg}_fanta")]
        ]
    elif btn_type == "shirin":
        btn = [
            [InlineKeyboardButton("Desert", callback_data=f"{ctg}_desert")]
        ]
    else:
        btn = [
            [InlineKeyboardButton("🌯 Lavash", callback_data="lavash"),
             InlineKeyboardButton("🍔 Burger", callback_data="burger")],
            [InlineKeyboardButton("🍰 Desert", callback_data="desert"),
             InlineKeyboardButton("🥂 Ichimlik", callback_data="ichimlik")]
        ]
    return InlineKeyboardMarkup(btn)


try:
    create_table()
except Exception as e:
    pass


def start(update, context):
    user = update.message.from_user
    if get_one(user.id):
        print('royhatdan otgan faydalanuvchi')
    else:
        create_user(user_id=user.id, username=user.username)
    update.message.reply_text(f"Assalomu Alaykum. Botimizga xush kelibsiz.\n Tilni tanlang 👇👇👇👇",
                              reply_markup=btns("lang"))


def message_handler(update, context):
    msg = update.message.text
    if msg == "🇺🇿 Uzbek tili" or msg == "🇷🇺 Руский язык" or msg == "🇺🇸 English":
        update.message.reply_text(
            f"🇺🇿 Qaysi viloyatda yashaysiz \n🇷🇺 В какой провинции вы живете в \n🇺🇸 Which province you from",
            reply_markup=btns("viloyat"))

    elif msg in vil:
        update.message.reply_text("🇺🇿 Raqamingizni yuboring \n🇷🇺 Введите свой номер \n 🇺🇸 Send you number",
                                  reply_markup=btns("contact"))

    elif msg == "🛒 Buyurtma qilish":
        update.message.reply_text("Taomni tanlang<a href='https://telegra.ph/EVOS-MENU-04-05-2'>.</a>",
                                  reply_markup=inline_btns("tur"), parse_mode="HTML")


def recieved_contact(update, context):
    update.message.reply_text("Meyulardan birini tanlang", reply_markup=btns("menu"))


def inline_handler(update, context):
    query = update.callback_query
    data_sp = query.data.split("_")
    print(data_sp)
    if data_sp[0] == "lavash":
        if len(data_sp) > 1 and data_sp[1] == "gusht":
            if len(data_sp) > 2:
                context.bot.send_photo(photo=open("go'sht.png", "rb"),
                                       caption=f"Umumiy narh:{23000 * int(data_sp[2])}",
                                       reply_markup=inline_btns(
                                           btn_type="number",
                                           ctg=data_sp[0],
                                           tip=data_sp[1]
                                       ),
                                       chat_id=query.message.chat_id)

            else:
                context.bot.send_photo(photo=open("go'sht.png", "rb"),
                                       caption="Narhi:23000 \nNechta kerak ekanligini kiriting",
                                       reply_markup=inline_btns(
                                           btn_type="number",
                                           ctg=data_sp[0],
                                           tip=data_sp[1]
                                       ),
                                       chat_id=query.message.chat_id)
        elif len(data_sp) > 1 and data_sp[1] == "tovuq":
            if len(data_sp) > 2:
                context.bot.send_photo(photo=open("word.png", "rb"),
                                       caption=f"Umumiy narh:{24000 * int(data_sp[2])}",
                                       reply_markup=inline_btns(
                                           btn_type="number",
                                           ctg=data_sp[0],
                                           tip=data_sp[1]
                                       ),
                                       chat_id=query.message.chat_id)

            else:
                context.bot.send_photo(photo=open("word.png", "rb"),
                                       caption="Narhi:24000 \nNechta kerak ekanligini kiriting",
                                       reply_markup=inline_btns(
                                           btn_type="number",
                                           ctg=data_sp[0],
                                           tip=data_sp[1]
                                       ),
                                       chat_id=query.message.chat_id)

        else:
            query.message.edit_text("Lavash turini tanlang<a href='https://telegra.ph/EVOS-MENU-04-05-2'>.</a>",
                                    reply_markup=inline_btns(btn_type='tur', ctg=data_sp[0]), parse_mode="HTML"
                                    )

    elif data_sp[0] == "burger":
        if len(data_sp) > 1 and data_sp[1] == "gusht":
            if len(data_sp) > 2:
                context.bot.send_photo(photo=open("burgergusht.png", "rb"),
                                       caption=f"Umumiy narh:{30000 * int(data_sp[2])}",
                                       reply_markup=inline_btns(
                                           btn_type="number",
                                           ctg=data_sp[0],
                                           tip=data_sp[1]
                                       ),
                                       chat_id=query.message.chat_id)
            else:
                context.bot.send_photo(photo=open("burgergusht.png", "rb"),
                                       caption="Narhi:30000 \nNechta kerak ekanligini kiriting",
                                       reply_markup=inline_btns(
                                           btn_type="number",
                                           ctg=data_sp[0],
                                           tip=data_sp[1]
                                       ),
                                       chat_id=query.message.chat_id)
        else:
            query.message.edit_text("Burger turini <a href='https://telegra.ph/EVOS-MENU-04-05-2'>.</a>",
                                    reply_markup=inline_btns(btn_type='tur', ctg=data_sp[0]), parse_mode="HTML"
                                    )

            if data_sp[0] == "burger":
                if len(data_sp) > 1 and data_sp[1] == "tovuq":
                    if len(data_sp) > 2:
                        context.bot.send_photo(photo=open("burgertovuq.png", "rb"),
                                               caption=f"Umumiy narh:{25000 * int(data_sp[2])}",
                                               reply_markup=inline_btns(
                                                   btn_type="number",
                                                   ctg=data_sp[0],
                                                   tip=data_sp[1]
                                               ),
                                               chat_id=query.message.chat_id)
                    else:
                        context.bot.send_photo(photo=open("burgertovuq.png", "rb"),
                                               caption="Narhi:25000 \nNechta kerak ekanligini kiriting",
                                               reply_markup=inline_btns(
                                                   btn_type="number",
                                                   ctg=data_sp[0],
                                                   tip=data_sp[1]
                                               ),
                                               chat_id=query.message.chat_id)
                else:
                    query.message.edit_text(
                        "Tovuqli burger turini tanlang<a href='https://telegra.ph/EVOS-MENU-04-05-2'>.</a>",
                        reply_markup=inline_btns(btn_type='tur', ctg=data_sp[0]), parse_mode="HTML"
                    )

    elif data_sp[0] == "desert":
        if len(data_sp) > 1 and data_sp[1] == "desert":
            if len(data_sp) > 2:
                context.bot.send_photo(photo=open("shirinlik.png", "rb"),
                                       caption=f"Umumiy narh:{60000 * int(data_sp[2])}",
                                       reply_markup=inline_btns(
                                           btn_type="number",
                                           ctg=data_sp[0],
                                           tip=data_sp[1]
                                       ),
                                       chat_id=query.message.chat_id)
            else:
                context.bot.send_photo(photo=open("shirinlik.png", "rb"),
                                       caption="Narhi:60000 \nNechta kerak ekanligini kiriting",
                                       reply_markup=inline_btns(
                                           btn_type="number",
                                           ctg=data_sp[0],
                                           tip=data_sp[1]
                                       ),
                                       chat_id=query.message.chat_id)
        else:
            query.message.edit_text("Desert turini tanlang<a href='https://telegra.ph/EVOS-MENU-04-05-2'>.</a>",
                                    reply_markup=inline_btns(btn_type='shirin', ctg=data_sp[0]), parse_mode="HTML"
                                    )

    elif data_sp[0] == "ichimlik":
        if len(data_sp) > 1 and data_sp[1] == "cola":
            if len(data_sp) > 2:
                context.bot.send_photo(photo=open("cola.png", "rb"),
                                       caption=f"Umumiy narh:{11000 * int(data_sp[2])}",
                                       reply_markup=inline_btns(
                                           btn_type="number",
                                           ctg=data_sp[0],
                                           tip=data_sp[1]
                                       ),
                                       chat_id=query.message.chat_id)
            else:
                context.bot.send_photo(photo=open("cola.png", "rb"),
                                       caption="Narhi:11000 \nNechta kerak ekanligini kiriting",
                                       reply_markup=inline_btns(
                                           btn_type="number",
                                           ctg=data_sp[0],
                                           tip=data_sp[1]
                                       ),
                                       chat_id=query.message.chat_id)

        elif len(data_sp) > 1 and data_sp[1] == "fanta":
            if len(data_sp) > 2:
                context.bot.send_photo(photo=open("fanta.png", "rb"),
                                       caption=f"Umumiy narh:{11000 * int(data_sp[2])}",
                                       reply_markup=inline_btns(
                                           btn_type="number",
                                           ctg=data_sp[0],
                                           tip=data_sp[1]
                                       ),
                                       chat_id=query.message.chat_id)
            else:
                context.bot.send_photo(photo=open("fanta.png", "rb"),
                                       caption="Narhi:11000 \nNechta kerak ekanligini kiriting",
                                       reply_markup=inline_btns(
                                           btn_type="number",
                                           ctg=data_sp[0],
                                           tip=data_sp[1]
                                       ),
                                       chat_id=query.message.chat_id)
        else:
            query.message.edit_text("Ichimlik turini tanlang<a href='https://telegra.ph/EVOS-MENU-04-05-2'>.</a>",
                                    reply_markup=inline_btns(btn_type='ich', ctg=data_sp[0]), parse_mode="HTML")


def main():
    Token = "2102288184:AAH_CH6Ls97PbPEV0mvLX4Xxz_T1IKs78jM"
    updater = Updater(Token)

    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, message_handler))
    updater.dispatcher.add_handler(MessageHandler(Filters.contact, recieved_contact))
    updater.dispatcher.add_handler(CallbackQueryHandler(inline_handler))
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
