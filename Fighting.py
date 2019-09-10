import utils
import config
import telebot
import threading
import time
import Weapon_list
import random
import special_abilities
import datahandler

bot = telebot.TeleBot(config.token)
types = telebot.types


# Собираем пул активных игроков
def get_playerpool(fight):
    fight.round += 1
    fight.fightstate = 'playerpool'
    for p in fight.activeplayers:
        if p.dodgecd > 0:
            p.dodgecd -= 1
        if p.Disabled:
            p.turn = 'disabled'
        elif p.Alive:
            fight.playerpool.append(p)
        elif 'Zombie' in p.passive:
            if p.zombiecounter > 0:
                fight.playerpool.append(p)
        elif special_abilities.Zombie in p.abilities:
            fight.playerpool.append(p)


# Рассылаем варианты действий
def send_actions(fight):
    for p in fight.actors:
        account_targets(p)
    for p in fight.playerpool:
        send_action(p, fight)
        print('Harakatlar jadvali jo`natildi - ' + p.name)


# Описание вариантов действий
def send_action(p, fight):
    keyboard = types.InlineKeyboardMarkup()
    if p.energy > 0:
        if not p.weapon.Melee:
            callback_button1 = types.InlineKeyboardButton(text="O`q uzish", callback_data=str('attack'
                                                                                            + str(fight.round)))
            callback_button2 = types.InlineKeyboardButton(text="Qayta o`qlash", callback_data=str('reload'
                                                                                                + str(fight.round)))
            keyboard.add(callback_button1, callback_button2)
        else:
            if p.Inmelee:
                callback_button1 = types.InlineKeyboardButton(text="Zarb",
                                                              callback_data=str('attack' + str(fight.round)))
                callback_button2 = types.InlineKeyboardButton(text="Dam olish",
                                                              callback_data=str('reload' + str(fight.round)))
                keyboard.add(callback_button1, callback_button2)
            else:
                if not p.targets:
                    callback_button1 = types.InlineKeyboardButton(text="Yaqinlashish",
                                                                  callback_data=str('move' + str(fight.round)))
                    callback_button2 = types.InlineKeyboardButton(text="Dam olish",
                                                                  callback_data=str('reload' + str(fight.round)))
                    keyboard.add(callback_button1, callback_button2)
                elif len(p.targets) < len(utils.get_other_team(p).actors):
                    callback_button1 = types.InlineKeyboardButton(text="Zarb",
                                                                  callback_data=str('attack' + str(fight.round)))
                    callback_button2 = types.InlineKeyboardButton(text="Dam olish",
                                                                  callback_data=str('reload' + str(fight.round)))
                    keyboard.add(callback_button1, callback_button2)
                    callback_button1 = types.InlineKeyboardButton(text="Yaqinlashish",
                                                                  callback_data=str('move' + str(fight.round)))
                    keyboard.add(callback_button1)
                else:
                    callback_button1 = types.InlineKeyboardButton(text="Zarb",
                                                                  callback_data=str('attack' + str(fight.round)))
                    callback_button2 = types.InlineKeyboardButton(text="Dam olish",
                                                                  callback_data=str('reload' + str(fight.round)))
                    keyboard.add(callback_button1, callback_button2)
    elif special_abilities.Zombie in p.abilities:
        if not p.targets:
            callback_button1 = types.InlineKeyboardButton(text="Yaqinlashish",
                                                          callback_data=str('move' + str(fight.round)))
            keyboard.add(callback_button1)
        elif len(p.targets) < len(utils.get_other_team(p).actors):
            callback_button1 = types.InlineKeyboardButton(text="Zarb",
                                                          callback_data=str('attack' + str(fight.round)))
            keyboard.add(callback_button1)
            callback_button1 = types.InlineKeyboardButton(text="Yaqinlashish",
                                                          callback_data=str('move' + str(fight.round)))
            keyboard.add(callback_button1)
        else:
            callback_button1 = types.InlineKeyboardButton(text="Zarb",
                                                          callback_data=str('attack' + str(fight.round)))
            keyboard.add(callback_button1)
    else:
        if not p.weapon.Melee:
            callback_button2 = types.InlineKeyboardButton(text="Qayta o`qlash",
                                                          callback_data=str('reload' + str(fight.round)))
            keyboard.add(callback_button2)
        else:
            callback_button2 = types.InlineKeyboardButton(text="Dam olish",
                                                          callback_data=str('reload' + str(fight.round)))

            keyboard.add(callback_button2)

    if p.dodgecd > 0:
        keyboard.add(types.InlineKeyboardButton(text='Info', callback_data=str('info')))
    else:
        keyboard.add(types.InlineKeyboardButton(text='Chetlashish', callback_data=str('evade' + str(fight.round))),
                     types.InlineKeyboardButton(text='Info', callback_data=str('info')))

    if not p.Armed:
        if len(p.itemlist) > 2:
            callback_button1 = types.InlineKeyboardButton(text="Qo`shimcha",
                                                          callback_data=str('inventory' + str(fight.round)))
            keyboard.add(callback_button1)
        else:
            for c in p.itemlist:
                if p.energy >= 2:
                    keyboard.add(types.InlineKeyboardButton(text=c.name, callback_data=str(c.id + str(fight.round))))
                elif c.energy is False:
                    keyboard.add(types.InlineKeyboardButton(text=c.name, callback_data=str(c.id + str(fight.round))))

    else:
        callback_button1 = types.InlineKeyboardButton(text="Bekor qilish",
                                                      callback_data=str('release' + str(fight.round)))
        keyboard.add(callback_button1)
    if p.lostweapon is not None:
        keyboard.add(types.InlineKeyboardButton(text='Qurolni olish', callback_data=str('take' + str(fight.round))))
    if p.firecounter > 0:
        keyboard.add(types.InlineKeyboardButton(text='O`tni o`chirish', callback_data=str('skip' + str(fight.round))))
    else:
        keyboard.add(types.InlineKeyboardButton(text='O`tkazib yuborish', callback_data=str('skip' + str(fight.round))))
    p.choicemessage = bot.send_message(p.chat_id, utils.player_turn_info(p).string, reply_markup=keyboard)
    p.info.clear()


# Ожидание ответа
def wait_response(fight):
    fight.done = False
    fight.fightstate = 'waiting'
    print('Yurishni kutyabmiz: ')
    for n in fight.playerpool:
        print(n.name)
    timer = threading.Timer(120.0, timerd, [fight])
    timer.start()
    i = 1
    while fight.playerpool and fight.done is False:
        if len(fight.playerpool) == 1 and i == 1:
            i += 1
        time.sleep(5)
    if fight.done:
        for p in fight.playerpool:
            print('Yurishni o`chiryabmiz ' + p.name)
            p.turn = 'skip' + str(fight.round)
            p.Skipped = True
            p.skipcounter += 1
            if p.skipcounter >= 3:
                p.turn = 'suicide'
            try:
                bot.edit_message_text(chat_id=p.chat_id, message_id=p.choicemessage.message_id,
                                    text="Yurish " + str(fight.round) + ': ''Vaqt tugadi!')
            except:
                pass
        fight.playerpool = []
    timer.cancel()
    del timer


# Переключение счетчика
def timerd(fight):
    fight.done = True


# Осуществление действий
def manifest_actions(fight):

    fight.fightstate = 'action'
    for p in fight.aiplayers:
        p.get_turn(fight)
    manifest_used_q(fight)
    for p in fight.aiplayers:
        p.aiaction1q(fight)
    manifest_first_q(fight)
    for p in fight.aiplayers:
        p.aiaction2q(fight)
    manifest_second_q(fight)
    for p in fight.actors:
        p.weapon.special_second(p)
    fight.string.post(bot, 'Yurish ' + str(fight.round), fight=fight)

    print('Tugagan')
    apply_effects(fight)

    for p in fight.aiplayers:
        p.aiactionlastq(fight)
    manifest_last_q(fight)
    fight.string.post(bot, 'Effektlar ' + str(fight.round), fight=fight)


# Действия до хода
def manifest_used_q(fight):
    for p in fight.actors:
        if p.turn[0:4] == 'item':
            for i in p.itemlist:
                if p.turn[0:7] == i.id:
                    i.usebefore(p)
                    break
    for p in fight.actors:
        print(', '.join([x.name for x in p.useditems]))
        for i in p.useditems:
                i.used(p)
        p.useditems = []
        for a in p.abilities:
            a.special_used(a, p)


# Действия первой очереди
def manifest_first_q(fight):
    for p in fight.actors:
        if p.turn == 'evade' + str(p.fight.round):
            p.fight.string.add(u'\U0001F4A8' + "|" + p.name + ' chetlashmoqda.')
            p.dodgecd += 5
            for n in utils.get_other_team(p).actors:
                if n.target == p:
                    n.tempaccuracy -= 5
        elif p.turn[0:4] == 'item':
            for i in p.itemlist:
                if p.turn[0:7] == i.id:
                    i.usefirst(p)
                    break
        for a in p.abilities:
            a.special_first(a, p)
        p.weapon.special_first(p)


# Основные действия
def manifest_second_q(fight):
    for p in fight.actors:
        # Перезарядка
        if p.turn == 'reload' + str(fight.round):
            print(p.name + str(1))
            p.energy = p.maxenergy
            if p.weapon.Melee or isinstance(p.weapon, Weapon_list.BowBleeding):
                fight.string.add(u'\U0001F624' + "|" +
                                 p.name + ' nafasini roslayabdi. Energiya maksimalgacha tiklandi! (' + str(
                                     p.energy) + ')')
            else:
                fight.string.add(
                                 u'\U0001F553' + "|" +
                                 str(p.name + ' qayta o`qlayabdi. Energiya maksimalgacha tiklandi! (' +
                                     str(p.energy) + ')'))

        # Стрельба; определение player.target
        elif p.turn == 'attack' + str(fight.round):
            p.action = str(p.attack())
            if p.target == p:
                p.action = p.action.replace('Raqib', 'o`zi').replace('O`yinchi', p.name).replace('Nishon', p.target.name)
            else:
                p.action = p.action.replace('Raqib', p.target.name).replace('O`yinchi', p.name)\
                    .replace('Nishon', p.target.name)
            fight.string.add(p.action)
        # Предмет
        elif p.turn[0:4] == 'item':
            for i in p.itemlist:
                if p.turn[0:7] == i.id:
                    p.action = i.use(p)
                    break
        # Пропуск хода\Тушение
        elif p.turn == 'skip' + str(fight.round):
            if p.firecounter == 0:
                fight.string.add(u'\U00002B07' + "|" + p.name + ' yurishni o`tkazib yuborayabdi.')
            else:
                fight.string.add(u'\U0001F4A8' + "|" + p.name + ' o`tni o`chirayabdi.')
            p.extinguish = True
        elif p.turn == 'draw':
            fight.string.add(u'\U0001F3F9' + "|" + p.name + ' Asgard kamonini cho`zayabdi.')
        elif p.turn == 'take' + str(fight.round):
            fight.string.add(u'\U0000270B' + "|" + p.name + ' yo`qolgan qurolni olayabdi.')
            p.weapon = p.lostweapon
            p.weapon.aquare(p)
            p.lostweapon = None
        # Целиться
        elif p.turn[0:4] == 'move':
            fight.string.add(u'\U0001F463' + "|" + p.name + ' dushmanga yaqinlashmoqda.')
            p.Inmelee = True
        # Ошибка
        elif p.turn == 'suicide':
            p.Suicide = True
            fight.string.add(u'\U00002620' + ' |' + p.name + ' hayotini joniga qasd qilib tugatayabdi.')
        elif p.turn is None:
            print('Yurishni aniqlashdagi xatolik' + p.name)
        print(p.name)

# Эффекты
def apply_effects(fight):
    for p in fight.actors:
        if p.bleedcounter > 0 and special_abilities.Sturdy.Sturdy in p.abilities:
            if p.bleedcounter >= 6:
                fight.string.add(u'\U00002763' + "| Qon yo`qotish " + p.name + ' dan jonni olib qo`ydi!')
                p.hp -= 1
                fight.string.add(u'\U00002665' * p.hp + ' |' + str(p.name) +
                                 " " + str(1) + " ta jonni yo`qotoyabdi. Qoldi " + str(p.hp) + " ta jon.")
                p.bleedcounter = 0
                p.bloodloss = True
            else:
                fight.string.add(u'\U00002763' + "|" + p.name + ' qon yo`qotaybdi!' + '(' + str(6-p.bleedcounter) + ')')
                p.bleedcounter += 1
        elif p.bleedcounter > 0:
            if p.bleedcounter >= 4:
                fight.string.add(u'\U00002763' + "| Qon yo`qotish " + p.name + ' dan jonni olib qo`ydi!')
                p.hp -= 1
                fight.string.add(u'\U00002665' * p.hp + ' |' + str(p.name) +
                                 " " + str(1) + " ta jonni yo`qotoyabdi. Qoldi " + str(p.hp) + " ta jon.")
                p.bleedcounter = 0
                p.bloodloss = True
            else:
                fight.string.add(u'\U00002763' + "|" + p.name + ' qon yo`qotaybdi!' + '(' + str(4-p.bleedcounter) + ')')
                p.bleedcounter += 1
        if p.firecounter > 0:
            if p.extinguish is True:
                p.firecounter = 0
                p.extinguish = False
            elif p.offfire == fight.round:
                fight.string.add(u'\U0001F525' + "| Olov " + p.name + ' dagi o`chdi!')
                p.firecounter = 0
            else:
                utils.damage(None, p, p.firecounter, 'fire')
                p.energy -= p.firecounter - 1
                if p.firecounter - 1 == 0:
                    fight.string.add(u'\U0001F525' + "|" + p.name
                                     + ' yonayabdi! U ' + str(p.firecounter) + " ta zarar ko`rdi.")
                else:
                    fight.string.add(u'\U0001F525' + "|" + p.name + ' yonayabdi! Yoqotdi '
                                     + str(p.firecounter - 1) + " ta energiya va oldi " + str(p.firecounter) + " ta zarar.")
        if p.stuncounter > 0:
            p.stuncounter -= 1
            if p.stuncounter == 0:
                fight.string.add(u'\U0001F300' + '|' + p.name + ' o`ziga keldi.')


# Действия последней очереди
def manifest_last_q(fight):
    for p in fight.actors:
        if p.turn[0:4] == 'item':
            for i in p.itemlist:
                if p.turn[0:7] == i.id:
                    i.uselast(p)
                    break
        for a in p.abilities:
            a.special_last(a, p)

        for i in p.weaponeffect:
            i.effect(p)
        if p.damagetaken > 0 and p.armor > 0:
            if random.randint(1, 100) <= p.armorchance:
                p.damagetaken -= p.armor
                fight.string.add(u'\U0001F6E1' + '| Sovut ' + p.name + 'ning ' + str(p.armor) + ' ta zarbini yo`qotayabdi!')
        if p.damagetaken < 0:
            p.damagetaken = 0


# Сброс переменных
def refresh_turn(fight):
    for p in fight.actors:
        p.turn = None
        p.target = None
        p.tempaccuracy = 0
        p.targets = []
        p.evasion = 0
        p.extinguish = False
        if p.accuracyfix > 0:
            p.accuracy -= p.accuracyfix
            p.accuracyfix = 0
        if p.damagefix > 0:
            p.bonusdamage -= p.damagefix
            p.damagefix = 0
        p.Hit = False
        p.Hitability = False
        if p.energy < 0:
            p.energy = 0
        if p.stuncounter > 0:
            p.Disabled = True
        else:
            p.Disabled = False
        if p.lostweapon == p.weapon:
            p.weapon = Weapon_list.fists
            p.lostweapon.lose(p)
        if p.energy > p.maxenergy:
            p.energy = p.maxenergy
            fight.string.add(p.name + ' ortiqcha energiyani yo`qotayabdi.')
    for p in fight.activeplayers:
        if not p.Skipped and p.skipcounter > 0:
            p.skipcounter = 0
        p.Skipped = False


# Результаты
def get_results(fight):
    print('1-Guruhning zarari- ' + str(fight.team1.getteamdamage()))
    print('2-Guruhning zarari - ' + str(fight.team2.getteamdamage()))
    fight.team1.losthp = 0
    fight.team2.losthp = 0
    if fight.team1.damagetaken < fight.team2.damagetaken:
        fight.string.add(u'\U00002757' + "|" + 'Guruh ' + fight.team1.actors[0].name + ' ko`proq zarar yetkazdi!')
        utils.apply_damage(fight.team2.actors)

    elif fight.team1.damagetaken == fight.team2.damagetaken == 0:
        fight.string.add(u'\U00002757' + "|" + 'Raundda zarb yetkazilmadi!')

    elif fight.team1.damagetaken == fight.team2.damagetaken:
        fight.string.add(u'\U00002757' + "|" + 'Barcha guruhlarda yo`qotishlar bo`ldi.')
        utils.apply_damage(fight.activeplayers)
        utils.apply_damage(fight.aiplayers)
    else:
        fight.string.add(u'\U00002757' + "|" + 'Guruh ' + fight.team2.actors[0].name + ' ko`proq zarar yetkazdi!')
        utils.apply_damage(fight.team1.actors)
    for p in fight.actors:
        p.weapon.special_end(p)
        for a in p.enditems:
            a.used(p)
        for a in p.abilities:
            a.special_end(a, p)
    for p in fight.aiplayers:
        p.aiactionend(fight)


def kill_players(fight):
    fight.team1.damagetaken = 0
    fight.team2.damagetaken = 0
    for p in fight.game.players:
        p.damagetaken = 0
        p.hploss = 1
        p.Drugged = False
        p.attackers = []
        if p.hp < 0:
            p.hp = 0
        p.Losthp = False
        for a in p.tempabilities:
            p.abilities.remove(a)
        p.tempabilities = []
    for p in fight.game.players:
            if special_abilities.Zombie in p.abilities:
                pass
            elif p.Suicide:
                p.Suicide = False
                p.Alive = False
                fight.string.add(u'\U00002620' + ' |' + p.name + ' hayotini joniga qasd qilib tugatayabdi.')
                p.team.actors.remove(p)
                p.team.players.remove(p)
                p.team.deadplayers.append(p)
                fight.activeplayers.remove(p)
                fight.actors.remove(p)
            elif not p.Alive and 'Zombie' in p.passive:
                if p.zombiecounter > 0:
                    p.zombiecounter -= 1
                    if p.zombiecounter == 0:
                        fight.string.add(u'\U00002620' + ' |' + p.name + ' hushini yo`qotdi.')
                        p.team.actors.remove(p)
                        p.team.players.remove(p)
                        p.team.deadplayers.append(p)
                        fight.activeplayers.remove(p)
                        fight.actors.remove(p)
            elif p.hp <= 0 and p.Alive:
                p.Alive = False
                if 'Zombie' in p.passive:
                    p.zombiecounter = 2
                    fight.string.add(u'\U0001F62C' + ' |' + p.name + ' qon ketayotgan holda jangni davom ettirayabdi!')
                else:
                    fight.string.add(u'\U00002620' + ' |' + p.name + ' hushini yo`qotaybdi.')
                    p.team.actors.remove(p)
                    p.team.players.remove(p)
                    p.team.deadplayers.append(p)
                    fight.activeplayers.remove(p)
                    fight.actors.remove(p)
    for p in fight.game.aiplayers:
        p.damagetaken = 0
        p.hploss = 1
        if p.hp < 0:
            p.hp = 0
        p.Losthp = False
    for p in fight.game.aiplayers:
        if p.hp <= 0 and p.Alive:
            p.Alive = False
            fight.string.add(u'\U00002620' + ' |' + p.name + ' o`lmoqda.')
            p.team.deadplayers.append(p)
            p.team.actors.remove(p)
            fight.aiplayers.remove(p)
            fight.deadai.append(p)
            fight.actors.remove(p)
        elif p.Suicide:
            p.Suicide = False
            p.Alive = False
            fight.string.add(u'\U00002620' + ' |' + p.name + ' hayotini joniga qasd qilib tugatayabdi.')
            p.team.deadplayers.append(p)
            p.team.actors.remove(p)
            fight.aiplayers.remove(p)
            fight.actors.remove(p)


def end(fight, game):
    if not fight.Withbots:
        for p in game.players:
            datahandler.add_played_games(p.chat_id)
        if not fight.team1.actors and not fight.team2.actors:
            bot.send_message(game.cid, "Ikkala guruh ham mag`lub bo`ldi!")
        elif not fight.team1.actors:
            for p in game.pending_team2:
                datahandler.add_won_games(p.chat_id)
            bot.send_message(game.cid, "Guruh " + fight.team1.leader.name + " mag`lubiyatga uchradi!")
            try:
                pic = bot.get_user_profile_photos(fight.team2.leader.chat_id).photos[0][0].file_id
                bot.send_photo(game.cid, pic, "Guruh " + fight.team2.leader.name + " g`alaba qozondi!")
            except:
                bot.send_message(game.cid, "Guruh " + fight.team2.leader.name + " g`alaba qozondi!")
        elif not fight.team2.actors:
            bot.send_message(game.cid, "Guruh " + fight.team2.leader.name + " mag`lubiyatga uchradi!")
            for p in game.pending_team1:
                datahandler.add_won_games(p.chat_id)
            try:
                pic = bot.get_user_profile_photos(fight.team1.leader.chat_id).photos[0][0].file_id
                bot.send_photo(game.cid, pic, "Guruh " + fight.team1.leader.name + " g`alaba qildi!")
            except:
                bot.send_message(game.cid, "Guruh " + fight.team1.leader.name + " g`alaba qildi!")
    else:
        if not fight.team1.actors and not fight.team2.actors:
            bot.send_message(game.cid, "Ikkala guruh ham mag`lub bo`ldi!")
        elif not fight.team1.actors:
            bot.send_message(game.cid, "Guruh " + fight.team1.leader.name + " mag`lubiyatga uchradi!")
            try:
                pic = fight.team2.leader.wonpic
                bot.send_document(game.cid, pic, caption="Guruh " + fight.team2.leader.name + " g`alaba qozondi!")
            except:
                bot.send_message(game.cid, "Guruh " + fight.team2.leader.name + " g`alaba qozondi!")
        elif not fight.team2.actors:
            bot.send_message(game.cid, "Guruh " + fight.team2.leader.name + " mag`lubiyatga uchradi!")
            try:
                pic = bot.get_user_profile_photos(fight.team1.leader.chat_id).photos[0][0].file_id
                bot.send_photo(game.cid, pic, "Guruh " + fight.team1.leader.name + " g`alaba qozondi!")
            except:
                bot.send_message(game.cid, "Guruh " + fight.Team1.leader.name + " g`alaba qozondi!")
            for ai in fight.deadai:
                if ai.dropweapons:
                    for weapon in ai.dropweapons:
                        for player in fight.team1.players:
                            if player.username is not None:
                                if datahandler.add_unique_weapon(player.username, weapon.name):
                                    bot.send_message(player.chat_id,'Siz olayabsiz ' + weapon.name + '!')


def fight_loop(game, fight):

    fight.team1 = game.team1
    fight.team2 = game.team2
    fight.team1.leader = game.team1.actors[0]
    fight.team2.leader = game.team2.actors[0]
    fight.actors = fight.aiplayers + fight.activeplayers
    for p in game.players:
        if p.chat_id == 379168159:
            p.abilities.append(special_abilities.Isaev)
            special_abilities.Isaev.aquare(p.abilities, p)
        p.hp = p.maxhp
        p.energy = p.maxenergy
        p.Alive = True
        p.team.participators.append(p)
    while fight.team1.actors != [] and fight.team2.actors != [] and fight.round != 50:
        fight.string.add('1-Guruh - ' + ', '.join([p.name for p in game.team1.actors]))
        fight.string.add('2-Guruh - ' + ', '.join([p.name for p in game.team2.actors]))
        get_playerpool(fight)
        send_actions(fight)
        wait_response(fight)
        manifest_actions(fight)
        get_results(fight)
        refresh_turn(fight)
        kill_players(fight)
        fight.string.post(bot, 'Yurish natijalari ' + str(fight.round), fight=fight)
    end(fight, game)
    utils.delete_game(game)


def account_targets(player):
    if not player.weapon.Melee:
        player.targets = utils.get_other_team(player).actors
    else:
        if player.Inmelee:
            player.targets = utils.get_other_team(player).actors
        else:
            for p in utils.get_other_team(player).actors:
                if p.weapon.Melee and p.Inmelee:
                    player.targets.append(p)
        blockers = []
        for p in player.targets:
            if special_abilities.Blocker in p.abilities:
                blockers.append(p)
        if blockers:
            player.targets = blockers
