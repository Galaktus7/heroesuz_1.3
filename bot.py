# -*- coding: utf-8 -*-
import config
import telebot
import Main_classes
import Fighting
import Item_list
import utils
import special_abilities
import Weapon_list
import time
import os
import bot_handlers
import datahandler
import subprocess
#from loguru import logger
#import sys
import traceback
types = telebot.types
bot = telebot.TeleBot(config.token)


symbols=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',
           'а','б','в','г','д','е','ё','ж','з','и','й','к','л','м','н','о','п','р','с','т','у','ф','х','ц','ч','ш','щ','ъ','ы','ь','э','ю','я', ' ']



# Настройка логгера - пишем в файл
#logger.add("bot.log", rotation="10 MB", encoding="utf-8")

#def log_exception(exc_type, exc_value, exc_traceback):
#    if issubclass(exc_type, KeyboardInterrupt):
        # Чтобы ctrl+c не ломал
#        sys.__excepthook__(exc_type, exc_value, exc_traceback)
 #       return
#    logger.error("Unhandled exception caught!", exc_info=(exc_type, exc_value, exc_traceback))

#sys.excepthook = log_exception


# Инлайн тимчата
@bot.inline_handler(func=lambda query: len(query.query)>0)
def query_text(query):
    try:
        Game = utils.get_game_from_player(query.from_user.id)
        r_sum = types.InlineQueryResultArticle(
            id='11', title="Guruhga yuborish📩",
            # Описание отображается в подсказке,
            # message_text - то, что будет отправлено в виде сообщения
            description=query.query,
            input_message_content=types.InputTextMessageContent(
                message_text=utils.teamchat(query.query, Game.player_dict[query.from_user.id])))
        bot.answer_inline_query(query.id, [r_sum])
    except:
        r_sum = types.InlineQueryResultArticle(
            id='22', title="Xatolik!",
            description="0'yinda emassiz📭",
            input_message_content=types.InputTextMessageContent(
                message_text='Xatolik!'))
        bot.answer_inline_query(query.id, [r_sum])


@bot.chosen_inline_handler(func=lambda chosen_inline_result: True )
def test_chosen(chosen_inline_result):
    if chosen_inline_result.result_id == '11':
        Game = utils.get_game_from_player(chosen_inline_result.from_user.id)
        player = Game.player_dict[chosen_inline_result.from_user.id]
        for p in player.team.players:
            bot.send_message(p.chat_id, player.message)


@bot.message_handler(commands=["start"])
def start(message):
    datahandler.get_player(message.from_user.id, message.from_user.username, message.from_user.first_name)


@bot.message_handler(commands=["bugreport"])
def bugreport(message):
    Main_classes.reportid.append(message.from_user.id)
    bot.send_message(message.from_user.id, 'Xatolikni bitta xat bilan tushintiring.')

@bot.message_handler(commands=['fight_random'])
def handle_random_fight(message):
    game = get_current_game(message.chat.id)
    prepare_fight_random(game)

# Обычный режим
@bot.message_handler(commands=["game"])
def start_game(message):
    if message.chat.id in Main_classes.existing_games:
        pass
    else:
        bot_handlers.start_game(0, message.chat.id)
        bot.send_document(message.chat.id,config.gameid,caption="*⚔️Qo`shilish uchun* /join *knopkasini bosing. O`yin bekor qilinishiga 5 daqiqa qoldi.*", parse_mode='markdown')

# Обычный режим
@bot.message_handler(commands=["customgame"])
def start_game(message):
    if message.chat.id in Main_classes.existing_games:
        pass
    else:
        bot_handlers.start_game(3, message.chat.id)
        bot.send_photo(message.chat.id,config.cusid,caption="Qo`shilish uchun /join knopkasini bosing. O`yin bekor qilinishiga 5 daqiqa qoldi.")

# Сражение с носорогом
@bot.message_handler(commands=["rhinohunt"])
def start_game(message):
    if message.chat.id in Main_classes.existing_games:
        pass
    else:
        bot_handlers.start_game(1, message.chat.id)
        bot.send_photo(message.chat.id,config.rhinoid,caption="Qo`shilish uchun /join knopkasini bosing. O`yin bekor qilinishiga 5 daqiqa qoldi.")


# Сражение с волками
@bot.message_handler(commands=["doghunt"])
def start_game(message):
    if message.chat.id in Main_classes.existing_games:
        pass
    else:
        bot_handlers.start_game(2, message.chat.id)
        bot.send_photo(message.chat.id,config.dogid,caption="Qo`shilish uchun /join knopkasini bosing. O`yin bekor qilinishiga 5 daqiqa qoldi.")


@bot.message_handler(commands=["rathunt"])
def start_game(message):
    if message.chat.id in Main_classes.existing_games:
        pass
    else:
        bot_handlers.start_game(4, message.chat.id)
        bot.send_photo(message.chat.id,config.ratid,caption="Qo`shilish uchun /join knopkasini bosing. O`yin bekor qilinishiga 5 daqiqa qoldi.")


#@bot.message_handler(commands=["thanos_hunt"])
#def start_game(message):
 #   if message.chat.id in Main_classes.existing_games:
  #      pass
   # else:
    #    bot_handlers.start_game(5, message.chat.id)
     #   bot.send_photo(message.chat.id,config.newid,caption="𝗦𝗲𝗻 𝗹𝗼𝘆𝗶𝗾 𝗷𝗮𝗻𝗴 𝗾𝗶𝗹𝗱𝗶𝗻𝗴. 𝗔𝗺𝗺𝗼 𝗺𝗲𝗻 𝗼'𝘁𝗮 𝗾𝘂𝗱𝗿𝗮𝘁𝗹𝗶𝗺𝗮𝗻. 𝗦𝗲𝗻 𝘁𝘂𝗳𝗮𝘆𝗹𝗶 𝘆𝗲𝗿𝗻𝗶𝗻𝗴 𝘆𝗮𝗿𝗺𝗶 𝘀𝗲𝗻 𝗵𝗮𝗾𝗶𝗻𝗴𝗱𝗮𝗴𝗶 𝘅𝗼𝘁𝗶𝗿𝗮 𝗸𝗮𝗯𝗶 𝗼'𝗹𝗺𝗮𝘆𝗱𝗶... \n\n🌎𝘿𝙪𝙣𝙮𝙤 𝙠𝙖𝙩𝙩𝙖 𝙭𝙖𝙫𝙛 𝙤𝙨𝙩𝙞𝙙𝙖. 𝙐𝙣𝙞 𝙦𝙪𝙩𝙦𝙖𝙧𝙞𝙗 𝙦𝙤𝙡𝙞𝙨𝙝 𝙪𝙘𝙝𝙪𝙣 /join 𝙠𝙣𝙤𝙥𝙠𝙖𝙨𝙞𝙣𝙞 𝙗𝙤𝙨𝙞𝙣𝙜!")

@bot.message_handler(commands=["thanos_hunt"])
def start_game(message):
    if message.chat.id in Main_classes.existing_games:
        pass
    else:
        bot_handlers.start_game(5, message.chat.id)
        bot.send_photo(message.chat.id,config.newid,caption="*-Mag'lubiyatlaringni qabul qila olmadilaringmi? \n-Va bu sizlarni qayerga olib keldi? \n-Yana meni oldimga. \n\n🌎Dunyoni qutqarib qolish uchun /join knopkasini bosing.*", parse_mode='markdown')

@bot.message_handler(commands=["terrorhunt"])
def start_game(message):
    if message.chat.id in Main_classes.existing_games:
        pass
    else:
        bot_handlers.start_game(6, message.chat.id)
        bot.send_photo(message.chat.id,config.terrorid,caption="🏙Shahar terroristlar qurshovida qoldi. 👨🏻‍✈️Ularni ovlash uchun /join knopkasini bosing.")

        
@bot.message_handler(commands=["masterhunt"])
def start_game(message):
    if message.chat.id in Main_classes.existing_games:
        pass
    else:
        bot_handlers.start_game(7, message.chat.id)
        bot.send_photo(message.chat.id,config.masterid,caption="⚜️Sen o`zingni eng kuchli deb hisoblaysanmi❓ Unday bo`lsa /join knopkasini bosib ☯️Masterga qarshi kurash va buni isbotla.")
      
         
@bot.message_handler(commands=["dragonhunt"])
def start_game(message):
    if message.chat.id in Main_classes.existing_games:
        pass
    else:
        bot_handlers.start_game(8, message.chat.id)
        bot.send_photo(message.chat.id,config.dragoid,caption="🌋Tog`lar orasidan qo`rqinchli nara eshitilyabdi. 🐉Drakonni ovlash uchun /join knopkasini bosing.")
            
@bot.message_handler(commands=["death_hunt"])
def start_game(message):
    if message.chat.id in Main_classes.existing_games:
        pass
    else:
        bot_handlers.start_game(9, message.chat.id)
        bot.send_photo(message.chat.id,config.supid,caption="☠️𝐒𝐞𝐧𝐢𝐧𝐠 𝐨`𝐥𝐢𝐦 𝐯𝐚𝐪𝐭𝐢𝐧𝐠 𝐤𝐞𝐥𝐝𝐢... 🚪𝐍𝐚𝐫𝐢𝐠𝐢 𝐝𝐮𝐧𝐲𝐨𝐠𝐚 𝐫𝐚𝐯𝐨𝐧𝐚 𝐛𝐨`𝐥𝐢𝐬𝐡𝐢𝐧𝐠 𝐮𝐜𝐡𝐮𝐧 /join 𝐤𝐧𝐨𝐩𝐤𝐚𝐬𝐢𝐧𝐢 𝐛𝐨𝐬.")
    
#@bot.message_handler(commands=["randomgame"])
#def start_game(message):
 #   if message.chat.id in Main_classes.existing_games:
  #      pass
   # else:
    #    bot_handlers.start_game(10, message.chat.id)  # Новый режим — 4
     #   bot.send_message(message.chat.id, "🎲 Random jangga qo‘shiling: /join")    
    
# ✅ Команда /top (удалили дубль, скрываем игроков с рейтингом 1000)
@bot.message_handler(commands=['reyting'])
def show_top(message):
    top_players = datahandler.get_top_ratings(limit=50)
    filtered = [p for p in top_players if p.get("rating", 1000) != 1000]
    if not filtered:
        bot.send_message(message.chat.id, "⛔️ Reytingda hali faollik yo‘q.")
        return

    text = "🏅 TOP Reytingdagilar:\n\n"
    for i, player in enumerate(filtered[:10], 1):  # максимум 10
        name = player.get("name") or player.get("username") or f"ID {player.get('id')}"
        rating = player.get("rating", 1000)
        text += f"{i}. {name} — {rating} Elo\n"
    bot.send_message(message.chat.id, text)


# ✅ Команда /rating (от себя, по реплаю, по ID)
@bot.message_handler(commands=['reyt'])
def show_rating(message):
    chat_id = message.chat.id
    from_user = message.from_user  # ← чтобы получить ID игрока, даже если в группе

    # 1️⃣ — Реплай на чужое сообщение
    if message.reply_to_message:
        target = message.reply_to_message.from_user
        target_id = target.id
        player = datahandler.fetch_player(target_id)
        rating = player.get("rating", 1000) if player else 1000
        name = player.get("name") or player.get("username") or f"ID {target_id}" if player else f"ID {target_id}"
        if rating == 1000:
            bot.send_message(chat_id, f"{name} hali reyting janglarida ishtirok etmagan.")
        else:
            bot.send_message(chat_id, f"{name} reytingi: {rating} Elo")
        return

    # 2️⃣ — Введён ID через аргумент /rating 123456789
    args = message.text.split()
    if len(args) > 1 and args[1].isdigit():
        target_id = int(args[1])
        player = datahandler.fetch_player(target_id)
        rating = player.get("rating", 1000) if player else 1000
        name = player.get("name") or player.get("username") or f"ID {target_id}" if player else f"ID {target_id}"
        if rating == 1000:
            bot.send_message(chat_id, f"{name} hali reyting janglarida ishtirok etmagan.")
        else:
            bot.send_message(chat_id, f"{name} reytingi: {rating} Elo")
        return

    # 3️⃣ — Отправитель (работает и в группе, и в ЛС)
    player_id = from_user.id
    player = datahandler.fetch_player(player_id)
    rating = player.get("rating", 1000) if player else 1000
    name = player.get("name") or player.get("username") or f"ID {player_id}" if player else f"ID {player_id}"
    if rating == 1000:
        bot.send_message(chat_id, "Siz hali reyting janglarida ishtirok etmagansiz.")
    else:
        bot.send_message(chat_id, f"{name}, sizning reytingingiz: {rating} Elo")

#@bot.message_handler(commands=['qobiliyat'])
#def set_custom_ability_limit(message):
 #   user_id = message.from_user.id
  #  print("❗️DEBUG user_id =", user_id)
   # print("❗️DEBUG dict_players.keys() =", Main_classes.dict_players.keys())
    #player = Main_classes.dict_players.get(user_id)

  #  if not player or not hasattr(player, 'game'):
   #     bot.send_message(message.chat.id, "❗️Siz o'yinda emassiz.")
    #    return

   # game = player.game
    #if game.gametype != 'normal':
     #   bot.send_message(message.chat.id, "❗️Bu buyruq faqat oddiy /game rejimida ishlaydi.")
      #  return

  #  try:
  #      count = int(message.text.split(' ')[1])
  #      if count < 2 or count > 8:
   #         raise ValueError
    #except (IndexError, ValueError):
     #   bot.send_message(message.chat.id, "❗️Foydalanish: /qobiliyat [2-8]")
      #  return

    #game.ability_count = count
    #bot.send_message(message.chat.id, f"🧠 Endi barcha o'yinchilar {count} ta qobiliyat tanlashlari mumkin bo'ladi.")

@bot.message_handler(commands=["fight"])
def start_game(message):
    game = utils.get_game_from_chat(message.chat.id)
    if game is not None:
        if game.gamestate == game.gamestates[0]:
            if game.gametype == 'game':
                if not game.pending_team1 or not game.pending_team2:
                    bot.send_message(message.chat.id, "O'yinchilar soni yetarli emas...")
                elif len(game.pending_players) > len(game.pending_team1) + len(game.pending_team2):
                    bot.send_message(message.chat.id, "Bazi o'yinchilar guruh tanlashmadi.")
                elif len(game.pending_players) == len(game.pending_team1) + len(game.pending_team2):
                    game.gamestate = game.gamestates[1]
                    for actor in game.pending_team1:
                        game.players.append(actor)
                        game.team1.players.append(actor)
                        actor.team = game.team1
                    for actor in game.pending_team2:
                        game.players.append(actor)
                        game.team2.players.append(actor)
                        actor.team = game.team2
                    bot_handlers.start_fight(message.chat.id)
            elif game.gametype == 'custom':
                if not game.pending_team1 or not game.pending_team2:
                    bot.send_message(message.chat.id, "Boshlash uchun o'yinchilar soni yetarli emas...")
                elif len(game.pending_players) > len(game.pending_team1) + len(game.pending_team2):
                    bot.send_message(message.chat.id, "Bazi o`yinchilar guruh tanlashmadi.")
                elif len(game.pending_players) == len(game.pending_team1) + len(game.pending_team2):
                    game.gamestate = game.gamestates[1]
                    for actor in game.pending_team1:
                        game.players.append(actor)
                        game.team1.players.append(actor)
                        actor.team = game.team1
                    for actor in game.pending_team2:
                        game.players.append(actor)
                        game.team2.players.append(actor)
                        actor.team = game.team2
                    bot_handlers.start_custom_fight(message.chat.id)
            else:
                if len(game.pending_players) < 1:
                    bot.send_message(message.chat.id, "Boshlash uchun o`yinchilar soni yetarli emas...")
                else:
                    game.gamestate = game.gamestates[1]
                    for actor in game.pending_team1:
                        game.players.append(actor)
                        game.team1.players.append(actor)
                        actor.team = game.team1
                    bot_handlers.start_fight(message.chat.id)


@bot.message_handler(commands=["flee"])
def flee(message):
    game = utils.get_game_from_chat(message.chat.id)
    if game is not None:
        if message.from_user.id in game.marked_id and game.gamestate == game.gamestates[0]:
            for x in game.pending_players:
                if x.chat_id == message.from_user.id:
                    game.pending_players.remove(x)
            for x in game.marked_id:
                if x == message.from_user.id:
                    game.marked_id.remove(x)
            for x in game.pending_team1:
                if x.chat_id == message.from_user.id:
                    game.pending_team1.remove(x)
            for x in game.pending_team2:
                if x.chat_id == message.from_user.id:
                    game.pending_team2.remove(x)
            del Main_classes.dict_players[message.from_user.id]
            game.gamers = game.gamers - 1
            bot.send_message(game.cid, message.from_user.first_name + ' qochib ketdi! Qolgan o`yinchilar: ' + str(game.gamers))



@bot.message_handler(commands=["cancel"])
def cancel_game(message):
    try:
        game = Main_classes.existing_games[message.chat.id]
    except:
        game = None
    if game is not None:
        if game.gamestate == game.gamestates[0]:
            game.waitingtimer.cancel()
            bot_handlers.cancel_game(game)


@bot.message_handler(commands=["suicide"])
def suicide(message):
    game = utils.get_game_from_chat(message.chat.id)
    if game != None:
        print("O`yin topildi.")
        found = True
        actor = None
        try:
            actor = game.player_dict[message.from_user.id]
        except:
            print('xatolik')
            found = False

        if game.gamestate == 'fight' and found and actor in actor.team.players:
            actor.turn = 'suicide'
            try:
                game.fight.playerpool.remove(actor)
            except:
                pass
            try:
                bot.delete_message(chat_id=actor.chat_id, message_id=actor.choicemessage)
            except:
                pass

@bot.message_handler(commands=["join"])
def add_player(message):
    game = utils.get_game_from_chat(message.chat.id)

    if message.from_user.id in Main_classes.dict_players:
        return

    if game is not None:
        try:
            no = 0
            for ids in message.from_user.first_name:
                if ids.lower() not in symbols:
                    no = 1

            if no == 0:
                name = message.from_user.first_name.split(' ')[0][:12]
            else:
                name = message.from_user.username

            username = message.from_user.username or "no_username"

            # ✅ Создаём игрока с нужными параметрами
            player = Main_classes.Player(message.from_user.id, name, game, username=username)
            Main_classes.dict_players[message.from_user.id] = player
            game.players.append(player)

            bot.send_message(message.from_user.id, "*Siz o'yinga omadli qo'shildingiz!*", parse_mode='markdown')

        except Exception as e:
            bot.send_message(message.chat.id, f"Xatolik yuz berdi: {e}")
            if game.gametype == game.gametypes[0] and message.from_user.id not in game.marked_id \
                    and message.chat.id == game.cid and game.gamestate == game.gamestates[0]:
                player = Main_classes.Player(message.from_user.id, name, Weapon_list.fists,
                                         game, message.from_user.username)
                game.pending_players.append(player)
                game.marked_id.append(player.chat_id)
                Main_classes.dict_players[player.chat_id] = game
                game.gamers = game.gamers + 1
                bot.send_message(game.cid, name + " o'yinga qo'shildi. O'yinchilar soni: " + str(game.gamers))
                if not game.pending_team1:
                    game.pending_team1.append(player)
                    datahandler.get_player(message.from_user.id, message.from_user.username, name)
                elif not game.pending_team2:
                    game.pending_team2.append(player)
                    datahandler.get_player(message.from_user.id, message.from_user.username, name)
                elif len(game.pending_players) >= 3:
                    keyboard = types.InlineKeyboardMarkup()
                    callback_button1 = types.InlineKeyboardButton(
                        text=str(len(game.pending_team1)) + ' - ' + game.pending_team1[0].name, callback_data='team1')
                    callback_button2 = types.InlineKeyboardButton(
                        text=str(len(game.pending_team2)) + ' - ' + game.pending_team2[0].name, callback_data='team2')
                    keyboard.add(callback_button1, callback_button2)
                    bot.send_message(message.from_user.id,
                                 name + ' Kimga yordam berishingizni '
                                                                'tanlang.', reply_markup=keyboard)
                    datahandler.get_player(message.from_user.id, message.from_user.username, name)
            elif game.gametype == game.gametypes[3] and message.from_user.id not in game.marked_id \
                    and message.chat.id == game.cid and game.gamestate == game.gamestates[0]:
                datahandler.get_player(message.from_user.id, message.from_user.username, name)
                data = datahandler.get_current(message.from_user.id)
                bot.send_message(game.cid, name + ' sozlangan janga omadli qo`shildi.')
                if data[0] is not None and data[1] is not None and data[2] is not None:
                    player = Main_classes.Player(message.from_user.id, name.split(' ')[0][:12],
                                                 Weapon_list.fists, game, message.from_user.username)
                    game.pending_players.append(player)
                    game.marked_id.append(player.chat_id)
                    Main_classes.dict_players[player.chat_id] = game
                    if not game.pending_team1:
                        game.pending_team1.append(player)
                        datahandler.get_player(message.from_user.id, message.from_user.username, name)
                    elif not game.pending_team2:
                        game.pending_team2.append(player)
                        datahandler.get_player(message.from_user.id, message.from_user.username, name)
                    elif len(game.pending_players) >= 3:
                        keyboard = types.InlineKeyboardMarkup()
                        callback_button1 = types.InlineKeyboardButton(
                            text=str(len(game.pending_team1)) + ' - ' + game.pending_team1[0].name, callback_data='team1')
                        callback_button2 = types.InlineKeyboardButton(
                            text=str(len(game.pending_team2)) + ' - ' + game.pending_team2[0].name, callback_data='team2')
                        keyboard.add(callback_button1, callback_button2)
                        bot.send_message(message.from_user.id,
                                 message.from_user.first_name + ' Kimga yordam berishingizni '
                                                                'tanlang.', reply_markup=keyboard)
                else:
                    bot.send_message(message.chat.id, '/player jadvalini to`ldiring')

            elif message.from_user.id not in game.marked_id and message.chat.id == game.cid and \
                            game.gamestate == game.gamestates[0]:
                if game.gametype == game.gametypes[1] and len(game.pending_players) > 2:
                    pass
                else:
                    game.gamers = game.gamers + 1
                    bot.send_message(game.cid, name + " o'yinga qo'shildi. O'yinchilar soni: " + str(game.gamers))
                    datahandler.get_player(message.from_user.id, message.from_user.username, name)
                    player = Main_classes.Player(message.from_user.id, name.split(' ')[0][:12],
                                                 None, game, message.from_user.username)
                    game.pending_players.append(player)
                    game.pending_team1.append(player)

                    Main_classes.dict_players[player.chat_id] = game
                    game.marked_id.append(player.chat_id)
            elif game.gamestate != game.gamestates[0]:
                bot.send_message(message.chat.id, 'O`yin boshlanmagan yoki allaqachon bo`layabdi.')
        except:
            bot.send_message(message.chat.id, 'O`yinga qo`shilish uchun @HuntUzBot bilan bog`laning.')

    time.sleep(3)



       # except:
      #      bot.send_message(message.chat.id, 'O`yinga qo`shilish uchun @HuntUzBot bilan bog`laning.')

    time.sleep(3)


@bot.message_handler(commands=["sendall"])
def start(message):
    Main_classes.ruporready = True

@bot.message_handler(commands=["stats"])
def stats_handler(message):
    # Определение целевого пользователя
    target_id = message.from_user.id
    target_name = message.from_user.first_name

    # Проверка на реплай
    if message.reply_to_message:
        target_id = message.reply_to_message.from_user.id
        target_name = message.reply_to_message.from_user.first_name

    # Проверка на ID в тексте команды
    elif len(message.text.split()) > 1:
        try:
            arg = message.text.split()[1]
            target_id = int(arg)
            # Если бот знает имя по id, можно заменить
            target_name = f"ID: {target_id}"
        except ValueError:
            bot.send_message(message.chat.id, "Noto‘g‘ri ID format.")
            return

    data = datahandler.get_games(target_id)
    if data is None:
        bot.send_message(message.chat.id, f"{target_name} jadvalda yo‘q.")
    elif data[0] == 0:
        bot.send_message(message.chat.id, f"{target_name}\n0 ta o‘yin o‘ynalgan.")
    else:
        winrate = int(data[1] / data[0] * 100)
        bot.send_message(message.chat.id, f"{target_name}:\n{data[0]} ta o‘yin o‘ynalgan.\n"
                                          f"{data[1]} ta o‘yin yutgan.\n{winrate}% yutuq.")
                                                                                   
@bot.message_handler(commands=["top"])
def reyting(message):
    stats = datahandler.get_all_stats()  # Ожидается список словарей [{'id': ..., 'wins': ..., 'games': ..., 'name': ...}, ...]
    if not stats:
        bot.send_message(message.chat.id, "Hozircha hech qanday ma'lumot yo'q.")
        return

    def format_player(p):
        winrate = int(p['wins'] / p['games'] * 100) if p['games'] > 0 else 0
        return f"- {p['name']} ({p['games']} o‘yin, {p['wins']} yutuq, {winrate}%)"

    def sort_and_limit(stats, min_games, max_games=None, limit=3):
        filtered = [s for s in stats if s['games'] >= min_games and (max_games is None or s['games'] < max_games)]
        sorted_list = sorted(filtered, key=lambda x: x['wins']/x['games'] if x['games'] > 0 else 0, reverse=True)
        return sorted_list[:limit]

    part1 = sort_and_limit(stats, 1000)
    part2 = sort_and_limit(stats, 500, 1000)
    part3 = sort_and_limit(stats, 100, 500)
    top_games = sorted(stats, key=lambda x: x['games'], reverse=True)[:5]

    text = "🏆 Reyting:\n\n"
    text += "1. 🥇 Top 3 Eng statistikasi baland o'yinchilar (1000+ o‘yin):\n" + "\n".join([format_player(p) for p in part1]) + "\n\n"
    text += "2. 🥈 Top 3 Eng statistikasi baland o'yinchilar (500–999 o‘yin):\n" + "\n".join([format_player(p) for p in part2]) + "\n\n"
    text += "3. 🥉 Top 3 Eng statistikasi baland o'yinchilar (100–499 o‘yin):\n" + "\n".join([format_player(p) for p in part3]) + "\n\n"
    text += "4. 🎮 Eng ko‘p o‘ynaganlar:\n" + "\n".join([f"- {p['name']} ({p['games']} o‘yin)" for p in top_games])

    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['test'])
def find_file_ids(message):
    for file in os.listdir('gif/'):
        if file.split('.')[-1] == 'gif' or file.split('.')[-1] == 'jpg' or file.split('.')[-1] == 'mp4':
            f = open('gif/'+file,'rb')
            msg = bot.send_photo(message.chat.id, f, None)
            # А теперь отправим вслед за файлом его file_id
            bot.send_message(message.chat.id, msg.photo[0].file_id, reply_to_message_id=msg.message_id)
        time.sleep(3)


@bot.message_handler(commands=['player'])
def find_file_ids(message):
    data = bot_handlers.player_menu(message.from_user.first_name, message.from_user.id)
    bot.send_message(message.from_user.id, data[0], reply_markup=data[1])


@bot.message_handler(commands=['try'])
def find_file_ids(message):
    try:
        bot.send_message(message.chat.id, '@' + message.from_user.username)
    except:
        pass


# Разрешенные пользователи (помимо админов)
allowed_users = [5153916046,1968791248,7281641346,1036373229]  # сюда впиши нужные Telegram ID

@bot.message_handler(commands=['restart'])
def restart_bot(message):
    user_id = message.from_user.id

    if user_id not in config.admins and user_id not in allowed_users:
        bot.reply_to(message, "🚫 Sizda ruxsat yo'q.")
        return

    try:
        bot.reply_to(message, "✅ Huntuzbot qayta ishga tushirildi.")
        subprocess.run(['sudo', 'systemctl', 'restart', 'huntuzbot.service'], check=True)
    except subprocess.CalledProcessError as e:
        bot.reply_to(message, f"❌ Xatolik: {e}")
        
@bot.message_handler(commands=['grouplist'])
def find_file_ids(message):
        Keyboard=types.InlineKeyboardMarkup()
        Keyboard.add(types.InlineKeyboardButton(text='⚔️Qaxramonlar🛡', url='telegram.me/huntuz'))
        Keyboard.add(types.InlineKeyboardButton(text='🌀Janglar Olami🌀', url='telegram.me/raunduz'))   
        Keyboard.add(types.InlineKeyboardButton(text='🦠Qasoskorlar🧬', url='telegram.me/qasosuz'))  
        bot.send_message(message.from_user.id, "📊Guruhlar ro'yxati:", reply_markup=Keyboard)



# === Обновлённая функция action с удалением старой логики выбора способностей ===
@bot.callback_query_handler(func=lambda call: True)
def action(call):
    if call.message:
        print("Получено.")
        if call.data == '1':
            bot.send_message(call.from_user.id, call.message.text)

    game = utils.get_game_from_player(call.from_user.id)

    if game is not None:
        print("Игра найдена.")
        found = True
        actor = None
        try:
            actor = game.player_dict[call.from_user.id]
        except:
            print('xatolik')
            found = False

        if game.gamestate == game.gamestates[0]:
            print('Guruh jamlanishi.')
            for p in game.pending_players:
                if call.from_user.id == p.chat_id:
                    print('O`yinchi topildi')
                    if call.data == 'team1':
                        print('Guruh-1')
                        game.pending_team1.append(p)
                        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                              text="Siz guruhga qo`shildingiz " + game.pending_team1[0].name)
                        bot.send_message(game.cid, p.name + ' quyidagi tomonda jang qiladi: ' + game.pending_team1[0].name)
                    if call.data == 'team2':
                        print('Guruh-2')
                        game.pending_team2.append(p)
                        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                              text="Siz guruhga qo`shildingiz " + game.pending_team2[0].name)
                        bot.send_message(game.cid, p.name + ' quyidagi tomonda jang qiladi: ' + game.pending_team2[0].name)

        elif game.gamestate == 'weapon' and found:
            if call.data[0] == 'a' and call.data[0:1] != 'at':
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text="Qurollar tanlandi: " + (call.data[1:]))
                for w in Weapon_list.fullweaponlist:
                    if w.name == call.data[1:]:
                        actor.weapon = w
                        break
                game.weaponcounter -= 1
                print(actor.name + ' qurol tanladi.')

        elif game.gamestate == 'ability' and found:
            if call.data.startswith('i') and len(call.data) < 4:
                bot.send_message(call.from_user.id, special_abilities.abilities[int(call.data[1:])].info)

            elif call.data.startswith('unique_i'):
                bot.send_message(call.from_user.id, special_abilities.unique_abilities[int(call.data[8:])].info)

            elif call.data.startswith('a') and len(call.data) < 4:
                if len(actor.abilities) >= actor.maxabilities:
                    bot.answer_callback_query(call.id, text=f"❗️Siz {actor.maxabilities} ta qobiliyatni tanladingiz")
                    return
                ability = special_abilities.abilities[int(call.data[1:])]
                if ability not in actor.abilities:
                    actor.abilities.append(ability)
                    if hasattr(ability, 'aquare'):
                        ability.aquare(ability, actor)
                    if hasattr(ability, 'aquareonce'):
                        ability.aquareonce(ability, actor)
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text="Qobiliyat tanlandi: " + ability.name)
                if len(actor.abilities) < actor.maxabilities:
                    utils.get_ability(actor)
                else:
                    try:
                        game.abilitycounter -= 1
                    except:
                        pass

            elif call.data.startswith('unique_a'):
                if len(actor.abilities) >= actor.maxabilities:
                    bot.answer_callback_query(call.id, text=f"❗️Siz {actor.maxabilities} ta qobiliyatni tanladingiz")
                    return
                ability = special_abilities.unique_abilities[int(call.data[8:])]
                if ability not in actor.abilities:
                    actor.abilities.append(ability)
                    if hasattr(ability, 'aquare'):
                        ability.aquare(ability, actor)
                    if hasattr(ability, 'aquareonce'):
                        ability.aquareonce(ability, actor)
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text="Qobiliyat tanlandi: " + ability.name)
                if len(actor.abilities) < actor.maxabilities:
                    utils.get_ability(actor)
                else:
                    try:
                        game.abilitycounter -= 1
                    except:
                        pass

        elif game.gamestate == game.gamestates[3] and found:
            pass  # [оставшийся боевой код обработки item, skills, moves и т.д.]

    else:
        if call.data == 'change_weapon':
            data = bot_handlers.weapon_menu(call.from_user.id)
            bot.edit_message_text(data[0], chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=data[1])
        elif call.data == 'change_items':
            data = bot_handlers.items_menu(call.from_user.id)
            bot.edit_message_text(data[0], chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  reply_markup=data[1])
        elif call.data == 'change_skills':
            data = bot_handlers.skills_menu(call.from_user.id)
            bot.edit_message_text(data[0], chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  reply_markup=data[1])
        elif call.data == 'change_string':
            bot_handlers.change_string(call.from_user.id)
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            data = bot_handlers.player_menu(call.from_user.first_name, call.from_user.id)
            bot.send_message(call.from_user.id, data[0], reply_markup=data[1])
        elif call.data[:10] == 'new_weapon':
            weapon = call.data[10:]
            datahandler.change_weapon(call.message.chat.id, weapon)
            data = bot_handlers.player_menu(call.from_user.first_name, call.from_user.id)
            bot.edit_message_text(data[0], chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  reply_markup=data[1])
        elif call.data[:8] == 'add_item':
            item_id = call.data[8:]
            changed = datahandler.add_item(call.message.chat.id, item_id)
            data = bot_handlers.items_menu(call.from_user.id)
            if changed:
                bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Invertor o`zgardi!")
                bot.edit_message_text(data[0], chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      reply_markup=data[1])
            else:
                bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="Oldin hozirgi narsalarni o`zgartiring.")
        elif call.data[:11] == 'delete_item':
            item_id = call.data[11:]
            true = datahandler.delete_item(call.message.chat.id, item_id)
            data = bot_handlers.items_menu(call.from_user.id)
            if true:
                bot.edit_message_text(data[0], chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      reply_markup=data[1])
        elif call.data[:9] == 'add_skill':
            skill_name = call.data[9:]
            changed = datahandler.add_skill(call.message.chat.id, skill_name)
            data = bot_handlers.skills_menu(call.from_user.id)
            if changed:
                bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Qobiliyatlar o`zgartirildi!")
                bot.edit_message_text(data[0], chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      reply_markup=data[1])
            else:
                bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="Oldin hozirgi qobiliyatlarni o`zgartiring.")
        elif call.data[:12] == 'delete_skill':
            skill_name = call.data[12:]
            true = datahandler.delete_skill(call.message.chat.id, skill_name)
            data = bot_handlers.skills_menu(call.from_user.id)
            if true:
                bot.edit_message_text(data[0], chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      reply_markup=data[1])
        elif call.data == 'accept_player':
            data = bot_handlers.player_menu(call.from_user.first_name, call.from_user.id)
            bot.edit_message_text(data[0], chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  reply_markup=data[1])

from telebot.types import Message
from config import admins

@bot.message_handler(commands=["add_group_weapons"])
def add_group_weapons(message):
    if message.from_user.id not in config.admins:
        return

    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        bot.reply_to(message, "Формат: /add_group_weapons <оружие1>, <оружие2>, ...")
        return

    weapon_names = [w.strip() for w in parts[1].split(',')]
    all_weapon_names = [w.name for w in Weapon_list.fullweaponlist]
    invalid = [w for w in weapon_names if w not in all_weapon_names]

    if invalid:
        bot.reply_to(message, f"Следующие оружия не найдены: {', '.join(invalid)}")
        return

    all_players = datahandler.getallplayers()
    count = 0
    for pid in all_players:
        for weapon in weapon_names:
            datahandler.add_unique_weapon(pid, weapon)
        count += 1

    bot.reply_to(message, f"Оружия добавлены {count} игрокам.")

# Команда: /add_weapon <weapon_name> <player_id>
@bot.message_handler(commands=["add_weapon"])
def add_weapon(message):
    if message.from_user.id not in config.admins:
        return

    parts = message.text.split()
    if len(parts) < 3:
        bot.reply_to(message, "Формат: /add_weapon <weapon_name> <player_id>")
        return

    try:
        player_id = int(parts[-1])
        weapon_name = " ".join(parts[1:-1])
    except ValueError:
        bot.reply_to(message, "ID игрока должен быть числом.")
        return

    all_weapon_names = [w.name for w in Weapon_list.fullweaponlist]
    if weapon_name not in all_weapon_names:
        bot.reply_to(message, "Оружие не найдено.")
        return

    success = datahandler.add_unique_weapon(player_id, weapon_name)
    if success:
        bot.reply_to(message, "Успешно добавлено.")
    else:
        bot.reply_to(message, "У игрока уже есть это оружие.")
        
# Команда: /delete_weapon <weapon_name> <player_id>
@bot.message_handler(commands=["delete_weapon"])
def remove_weapon(message):
    if message.from_user.id not in config.admins:
        return

    parts = message.text.split()
    if len(parts) < 3:
        bot.reply_to(message, "Формат: /remove_weapon <weapon_name> <player_id>")
        return

    try:
        player_id = int(parts[-1])
        weapon_name = " ".join(parts[1:-1])
    except ValueError:
        bot.reply_to(message, "ID игрока должен быть числом.")
        return

    all_weapon_names = [w.name for w in Weapon_list.fullweaponlist]
    if weapon_name not in all_weapon_names:
        bot.reply_to(message, "Оружие не найдено.")
        return

    success = datahandler.delete_unique_weapon(player_id, weapon_name)
    if success:
        bot.reply_to(message, "Оружие удалено.")
    else:
        bot.reply_to(message, "У игрока нет такого оружия.")

# Команда: /inventory <player_id>
@bot.message_handler(commands=["weapons"])
def get_player_weapons(message):
    # Определяем ID цели
    target_id = message.from_user.id
    target_name = message.from_user.first_name

    # Если есть реплай
    if message.reply_to_message:
        target_id = message.reply_to_message.from_user.id
        target_name = message.reply_to_message.from_user.first_name

    # Если указан ID через аргумент
    parts = message.text.strip().split()
    if len(parts) == 2:
        try:
            target_id = int(parts[1])
        except ValueError:
            bot.reply_to(message, "ID игрока должен быть числом.")
            return

    # Проверка на существование игрока
    if not datahandler.player_exists(target_id):
        bot.reply_to(message, "Игрок не найден.")
        return

    # Получение оружия
    weapons = datahandler.get_unique_weapon(target_id)
    if weapons:
        weapon_list = "\n".join(f"- {w}" for w in weapons)
        bot.reply_to(message, f" {target_name}ning unikal qurollari ro`yxati:\n{weapon_list}")
    else:
        bot.reply_to(message, f"У игрока {target_name} нет уникального оружия.")
        
# Команда: /delete_dungeon_weapons
@bot.message_handler(commands=['delete_dungeon_weapons'])
def delete_dungeon_weapons(message: Message):
    if message.chat.id not in admins:
        return
    datahandler.delete_dungeon_weapons()
    bot.send_message(message.chat.id, "Данжевое оружие удалено у всех игроков.")

# Команда: /delete_all_players
@bot.message_handler(commands=['delete_all_players'])
def delete_all_players(message: Message):
    if message.chat.id not in admins:
        return
    datahandler.delete_all_players()
    bot.send_message(message.chat.id, "Все данные игроков удалены.")

@bot.message_handler(commands=['weapon_list'])
def show_weapon_list(message):
    if message.chat.id not in config.admins:
        return

    weapon_names = [w.name for w in Weapon_list.fullweaponlist]
    weapon_text = '\n'.join(f"- {name}" for name in weapon_names)

    # Ограничим длину сообщения (Telegram max ~4096)
    if len(weapon_text) > 4000:
        bot.send_message(message.chat.id, "Слишком много оружия для вывода.")
    else:
        bot.send_message(message.chat.id, f"Список всех оружий:\n{weapon_text}")

@bot.message_handler(commands=['adminpanel'])
def admin_panel(message):
    if message.from_user.id not in config.admins:
        return

    help_text = (
        "Админ-панель команд:\n\n"
        "/add_weapon <weapon_name> <player_id> — Добавить оружие игроку\n"
        "/delete_weapon <weapon_name> <player_id> — Удалить оружие у игрока\n"
        "/weapons <player_id> — Показать уникальные оружия игрока\n"
        "/delete_dungeon_weapons — Удалить данжевые оружия у всех игроков\n"
        "/clear_players — Удалить весь player_database\n"
        "/weapon_list — Список всех доступных оружий\n"
        "/ad_group_weapon - hammaga qurol qowiw\n"
        "/adminpanel — Показать эту справку"
    )
    bot.send_message(message.chat.id, help_text)

# Обработчик inline-кнопок с ограничением по количеству выбранных способностей

@bot.callback_query_handler(func=lambda call: call.data.startswith(('a', 'i', 'unique_a', 'unique_i')))
def handle_ability_choice(call):
    chat_id = call.message.chat.id
    player = Main_classes.dict_players.get(chat_id)
    if not player:
        return

    max_ab = getattr(player, 'maxabilities', 2)

    # Проверка количества уже выбранных
    if call.data.startswith('a') or call.data.startswith('unique_a'):
        if len(player.abilities) >= max_ab:
            bot.answer_callback_query(call.id, text=f"❗️Siz {max_ab} ta qobiliyatni tanladingiz")
            return

        if call.data.startswith('unique_a'):
            index = int(call.data[len('unique_a'):])
            ability = special_abilities.unique_abilities[index]
        else:
            index = int(call.data[1:])
            ability = special_abilities.abilities[index]

        if ability not in player.abilities:
            player.abilities.append(ability)
            ability.aquare(ability, player)
            ability.aquareonce(ability, player)
            bot.answer_callback_query(call.id, text=f"✅ Qobiliyat tanlandi: {ability.name}")
            bot.edit_message_reply_markup(chat_id, call.message.message_id)
    
    elif call.data.startswith('i') or call.data.startswith('unique_i'):
        if call.data.startswith('unique_i'):
            index = int(call.data[len('unique_i'):])
            ability = special_abilities.unique_abilities[index]
        else:
            index = int(call.data[1:])
            ability = special_abilities.abilities[index]

        bot.answer_callback_query(call.id)
        bot.send_message(chat_id, f"🧠 <b>{ability.name}</b>\n{ability.desc}", parse_mode='HTML')

bot.skip_pending = True
if __name__ == '__main__':
     time.sleep(1)
     bot.polling(none_stop=True)     
