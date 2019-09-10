import random
import telebot
import config
import utils
import Item_list
types = telebot.types
bot = telebot.TeleBot(config.token)
weaponlist = []
fullweaponlist = []


class Weapon(object):
    def __init__(self, dice, damage, energy, bonus, fixed, Melee, TwoHanded, Concealable, name, damagestring, standart=True, pellets=False, natural=False):
        self.dice = dice
        self.damage = damage
        self.energy = energy
        self.fixed = fixed
        self.bonus = bonus
        self.Melee = Melee
        self.TwoHanded = TwoHanded
        self.Concealable = Concealable
        self.name = name
        self.damagestring = damagestring
        self.standart = standart
        self.pellets = pellets
        self.natural = natural
        if self.standart == True:
            weaponlist.append(self)
        fullweaponlist.append(self)

    # Выстрел
    def hit(self,user):
        n = 0
        d = 0
        dmax = self.dice
        print(user.name + " otayabdi " + str(self.name) + 'dan. Uning energiyasi - ' + str(
            user.energy) + '. Uning aniqligi va qurolning bonus aniqligi - '
              + str(user.accuracy) + ' ' + str(self.bonus) + ' ' +
              '. Tegish ehtimolligi - ' + str(10 - user.energy - self.bonus - user.accuracy - user.tempaccuracy) + "+!")
        while d != dmax:
            x = random.randint(1, 10)
            print(user.name + ' Tushib qoldi ' + str(x))
            if x > 10 - user.energy - self.bonus - user.accuracy - user.tempaccuracy + user.target.evasion:

                n += 1
                print('+1 summar zarba.')
            else:
                print('qiyshiq.')
            d += 1
        print('Umumuy zarbi ' + str(n))

        # бонусный урон персонажа
        if n != 0:
            n += user.bonusdamage + self.damage - 1
            if self.pellets and user.target.weapon.Melee and user.target.Inmelee:
                n += 1
        for a in user.abilities:
            n = a.onhit(a,n, user)
        # уходит энергия
        if self.fixed > 0 and n > 0:
            n = self.fixed
        user.energy -= self.energy
        # энергия загоняется в 0
        if user.energy < 0: user.energy = 0

        utils.damage(user, user.target, n, 'hit')
        return n

    # При экипировке
    def aquare(self,user):
        pass

    # Создание описания
    def getDesc(self, damagetaken,user):
        if damagetaken != 0:
            if not self.Melee:
                d = str(u'\U0001F4A5' + "|" + getattr(self,str('desc' + str(random.randint(1, 3)))) + " Yetkazildi " + str(damagetaken) + ' zarb.')
            else:
                d = str(u'\U0001F44A' + "|" + getattr(self,str('desc' + str(random.randint(1, 3)))) + " Yetkazildi " + str(damagetaken) + ' zarb.')
                for a in user.abilities:
                    d = a.onhitdesc(a,d,user)
        else:
            d = str(u'\U0001F4A8' + "|" + getattr(self,str('desc' + str(random.randint(4, 6)))))
        return d

    # Отправка вариантов
    def get_action(self, p, call):
        keyboard1 = types.InlineKeyboardMarkup()
        targets = p.targets
        p.turn = call.data
        if p.Blocked:
            for c in targets:
                keyboard1.add(types.InlineKeyboardButton(text=c.name, callback_data=str('op' + str(c.chat_id))))
            keyboard1.add(types.InlineKeyboardButton(text='Bekor qilish', callback_data=str('opcancel')))
            bot.send_message(p.chat_id, targets[0].name +' raqibga yaqinlashishizga yo`l qo`ymayabdi.', reply_markup=keyboard1)

        elif len(targets) == 1:
            p.target = targets[0]
            try:
                p.fight.playerpool.remove(p)
            except:
                print('Oyy.')
        else:
            for c in targets:
                keyboard1.add(types.InlineKeyboardButton(text=c.name, callback_data=str('op' + str(c.chat_id))))
            keyboard1.add(types.InlineKeyboardButton(text='Bekor qilish', callback_data=str('opcancel')))
            bot.send_message(p.chat_id, 'Raqibni tanlang.', reply_markup=keyboard1)

    # Особое действие
    def special(self, user, call):
        pass

    #На конец хода
    def special_end(self, user):
        pass

    def special_second(self, user):
        pass

    def special_first(self, user):
        pass

    def lose(self,user):
        pass

    def effect(self, user):
        pass


class Tazer(Weapon):
    def effect(self, user):
        user.target.energy -= 1
        user.weaponeffect.remove(self)

    def getDesc(self, damagetaken, user):
        if damagetaken != 0:
            user.weaponeffect.append(self)
            d = str(u'\U0001F44A' + u'\U000026A1'+ "|" + getattr(self,str('desc' + str(random.randint(1, 3)))) + " Yetkazildi " + str(damagetaken) + ' zarb. ' + user.target.name + ' 1 Energiya yo`qotayabdi.')
            for a in user.abilities:
                d = a.onhitdesc(a,d,user)
        else:
            d = str(u'\U0001F4A8' + "|" + getattr(self,str('desc' + str(random.randint(4, 6)))))
        return d

    desc1 = 'O`yinchi urayabdi Raqibini Militsiya Dubinkasi bilan.'
    desc2 = 'O`yinchi urayabdi Raqibini Militsiya Dubinkasi bilan.'
    desc3 = 'O`yinchi urayabdi Raqibini Militsiya Dubinkasi bilan.'
    desc4 = 'O`yinchi urayabdi Raqibini Militsiya Dubinkasi bilan, lekin tekkiza olmayabdi.'
    desc5 = 'O`yinchi urayabdi Raqibini Militsiya Dubinkasi bilan, lekin tekkiza olmayabdi.'
    desc6 = 'O`yinchi urayabdi Raqibini Militsiya Dubinkasi bilan, lekin tekkiza olmayabdi.'


class Sniper(Weapon):
    def hit(self,user):
        if user.aimtarget is not None:
            if user.target.chat_id != int(user.aimtarget):
                print('tiklash')
                user.bonusaccuracy = 0
        n = 0
        d = 0
        dmax = self.dice
        print(user.name + " otayabdi " + str(self.name) + 'dan. Uning energiyasi - ' + str(
            user.energy) + '. Uning aniqligi va qurolning bonus aniqligi - ' + ' '
              + str(user.accuracy) + ' ' + str(user.bonusaccuracy) + ' ' + str(self.bonus) +
              '. Tegish ehtimolligi - ' + str(11 - user.energy - self.bonus - user.accuracy - user.bonusaccuracy - user.tempaccuracy) + "+!")
        while d != dmax:
            x = random.randint(1, 10)
            print(user.name + ' Tushib qoldi ' + str(x))
            if x > 10 - user.energy - self.bonus - user.accuracy - user.bonusaccuracy - user.tempaccuracy + user.target.evasion:
                n += 1
            d += 1
        user.bonusaccuracy = 0
        user.aimtarget = None

        # бонусный урон персонажа
        if n != 0:
            n += user.bonusdamage + self.damage - 1
        # уходит энергия
        if self.Melee:
            user.energy -= random.randint(1, 2)
        else:
            user.energy -= self.energy
        # энергия загоняется в 0
        if self.fixed > 0 and n > 0:
            n = self.fixed
        if user.energy < 0: user.energy = 0
        utils.damage(user, user.target, n, 'firearm')
        return n

    def aquare(self,user):
        user.aimtarget = None
        user.bonusaccuracy = 0

    def lose(self,user):
        del user.aimtarget
        del user.bonusaccuracy

    def get_action(self, p, call):
        keyboard1 = types.InlineKeyboardMarkup()
        enemyteam = p.targets
        p.turn = call.data
        for c in enemyteam:
            if p.energy + self.bonus + p.accuracy + p.bonusaccuracy >= 10:
                keyboard1.add(types.InlineKeyboardButton(text=c.name, callback_data=str('op' + str(c.chat_id))))
            else:
                keyboard1.add(types.InlineKeyboardButton(text=c.name, callback_data=str('op' + str(c.chat_id))),
                              types.InlineKeyboardButton(text="Nishonga olish", callback_data=str('aim' + str(c.chat_id))))

        keyboard1.add(types.InlineKeyboardButton(text='Bekor qilish', callback_data=str('opcancel')))
        bot.send_message(p.chat_id, 'Raqibni tanlang.', reply_markup=keyboard1)

    def special(self, user, call):
        if user.aimtarget != call.data[3:]:
            user.aimtarget = call.data[3:]
            user.bonusaccuracy = 5
        else:
            user.bonusaccuracy +=5
        if user.energy + self.bonus + user.accuracy + user.bonusaccuracy >= 10:
            bot.send_message(user.chat_id, 'Aniqlik maksimal!')
        user.fight.string.add(u'\U0001F3AF' + "|" + user.name + ' nishonga olish.')
        print('scheck')


    desc1 = 'O`yinchi Raqibiga Snayper Vintovkasi bilan otayabdi.'
    desc2 = 'O`yinchi Raqibiga Snayper Vintovkasi bilan otayabdi.'
    desc3 = 'O`yinchi Raqibiga Snayper Vintovkasi bilan otayabdi.'
    desc4 = 'O`yinchi Raqibiga Snayper Vintovkasi bilan otayabdi, lekin tekkiza olmayabdi.'
    desc5 = 'O`yinchi Raqibiga Snayper Vintovkasi bilan otayabdi, lekin tekkiza olmayabdi.'
    desc6 = 'O`yinchi Raqibiga Snayper Vintovkasi bilan otayabdi, lekin tekkiza olmayabdi.'

##########################New weapon#########################################


class Kalashnikov(Weapon):
    def hit(self,user):
        n = 0
        d = 0
        dmax = self.dice
        print(user.name + " otayabdi " + str(self.name) + 'dan. Uning energiyasi - ' + str(
            user.energy) + '. Uning aniqligi va qurolning bonus aniqligi - ' + ' '
              + str(user.accuracy) + ' ' + str(self.bonus) +
              '. Tegish ehtimolligi - ' + str(11 - user.energy - self.bonus - user.accuracy - user.tempaccuracy) + "+!")
        while d != dmax:
            x = random.randint(1, 10)
            print(user.name + ' Tushib qoldi ' + str(x))
            if x > 10 - user.energy - self.bonus - user.accuracy - user.tempaccuracy + user.target.evasion:
                n += 1
            d += 1
        if n != 0:
            user.target.firecounter += 1
            user.target.offfire = user.fight.round + 2
            n += user.bonusdamage + self.damage - 1
        else:
            pass
        n += user.truedamage
        # энергия загоняется в 0
        if self.Melee:
            user.energy -= random.randint(1, 2)
        else:
            user.energy -= self.energy
        if user.energy < 0 :
            user.energy = 0
        if self.fixed > 0 and n > 0:
            n = self.fixed
        utils.damage(user, user.target, n, 'fire')
        return n

    def get_action(self, p, call):
        keyboard1 = types.InlineKeyboardMarkup()
        enemyteam = p.targets
        p.turn = call.data
        for c in enemyteam:
            if p.energy < 3:
                keyboard1.add(types.InlineKeyboardButton(text=c.name, callback_data=str('op' + str(c.chat_id))))
            else:
                keyboard1.add(types.InlineKeyboardButton(text=c.name, callback_data=str('op' + str(c.chat_id))),
                              types.InlineKeyboardButton(text="Olovli o'q", callback_data=str('weaponspecial'
                                                                                                 + str(c.chat_id))))

        keyboard1.add(types.InlineKeyboardButton(text='Bekor qilish', callback_data=str('opcancel')))
        bot.send_message(p.chat_id, 'Raqibni tanlang.', reply_markup=keyboard1)

    def special(self, user, call):
        user.target = utils.actor_from_id(call, user.game)

    def special_second(self, user):
        if user.turn == 'weaponspecial':
            damagetaken = 0
            combo = 0
            while user.energy > 0 and combo < 3:
                damagetaken += self.hit(user)
                combo += 1
            if damagetaken != 0:
                d = str(
                    u'\U0001F91C' + "|" + user.name + ' Kalashnikovdan ' + str(combo) + " ta olovli o'q orqali "
                    + user.target.name + "ga zarb berayabdi! Yetkazildi " + str(damagetaken) + ' zarb.')
            else:
                d = str(
                    u'\U0001F4A8' + "|" + user.name + ' bitta ham o`q ota olmadi ' + user.target.name + "ga!")
            for a in user.abilities:
                d = a.onhitdesc(a, d, user)
            user.fight.string.add(d)

    def getDesc(self, damagetaken,user):
        if damagetaken != 0:
            d = str(u'\U0001F4A5' + "|"
                           + getattr(self,str('desc' + str(random.randint(1, 3)))) + " Yetkazildi "
                                              + str(damagetaken) + ' zarb.')
            if user.target.firecounter == 1:
                d += u'\U0001F525' + "|" + user.target.name + ' yonayabdi!'
            return d
        else:
            return str(u'\U0001F4A8' + "|" + getattr(self, str('desc' + str(random.randint(4, 6)))))


    desc1 = 'O`yinchi Raqibiga Kalashnikovdan otayabdi!'
    desc2 = 'O`yinchi Raqibiga Kalashnikovdan otayabdi!'
    desc3 = 'O`yinchi Raqibiga Kalashnikovdan otayabdi!'
    desc4 = 'O`yinchi Raqibiga Kalashnikovdan otayabdi, lekin tekkiza olmayabdi.'
    desc5 = 'O`yinchi Raqibiga Kalashnikovdan otayabdi, lekin tekkiza olmayabdi.'
    desc6 = 'O`yinchi Raqibiga Kalashnikovdan otayabdi, lekin tekkiza olmayabdi.'

    ####################################################################################
    
##########################New weapon#########################################


class Vintovka(Weapon):
    def __init__(self, dice, damage, energy, bonus, fixed, Melee, TwoHanded, Concealable, name, damagestring, chance,
                 standart=True,natural=False):
        Weapon.__init__(self, dice, damage, energy, bonus, fixed, Melee, TwoHanded, Concealable, name, damagestring,
                        standart=standart,natural=natural)
        self.chance = chance
        
    def hit(self,user):
        n = 0
        d = 0
        dmax = self.dice
        print(user.name + " otayabdi " + str(self.name) + 'dan. Uning energiyasi - ' + str(
            user.energy) + '. Uning aniqligi va qurolning bonus aniqligi - ' + ' '
              + str(user.accuracy) + ' ' + str(self.bonus) +
              '. Tegish ehtimolligi - ' + str(11 - user.energy - self.bonus - user.accuracy - user.tempaccuracy) + "+!")
        while d != dmax:
            x = random.randint(1, 10)
            print(user.name + ' Tushib qoldi ' + str(x))
            if x > 10 - user.energy - self.bonus - user.accuracy - user.tempaccuracy + user.target.evasion:
                n += 1
            d += 1


            # бонусный урон персонажа
        # уходит энергия
        user.energy -= self.energy
        if n!=0:
            n += user.bonusdamage + self.damage - 1
            for a in user.abilities:
                n = a.onhit(a,n, user)
        else:
            pass
        n += user.truedamage
        # применяется урон
        # энергия загоняется в 0

        if user.energy < 0: user.energy = 0

        utils.damage(user, user.target, n, 'melee')
        return n

    def effect(self, user):
        if random.randint(1,5)< self.chance:
            if user.target.stuncounter < 1:
                user.target.stuncounter = 1
            user.fight.string.add(u'\U0001F300' + '|' + user.target.name + ' karaxtlandi!')
        user.weaponeffect.remove(self)

    def get_action(self, p, call):
        keyboard1 = types.InlineKeyboardMarkup()
        enemyteam = p.targets
        p.turn = call.data
        for c in enemyteam:
            if p.energy < 3:
                keyboard1.add(types.InlineKeyboardButton(text=c.name, callback_data=str('op' + str(c.chat_id))))
            else:
                keyboard1.add(types.InlineKeyboardButton(text=c.name, callback_data=str('op' + str(c.chat_id))),
                              types.InlineKeyboardButton(text="Kalibrli o'q", callback_data=str('weaponspecial'
                                                                                                 + str(c.chat_id))))

        keyboard1.add(types.InlineKeyboardButton(text='Bekor qilish', callback_data=str('opcancel')))
        bot.send_message(p.chat_id, 'Raqibni tanlang.', reply_markup=keyboard1)

    def special(self, user, call):
        user.target = utils.actor_from_id(call, user.game)

    def special_second(self, user):
        if user.turn == 'weaponspecial':
            damagetaken = 0
            combo = 0
            while user.energy > 0 and combo < 3:
                damagetaken += self.hit(user)
                combo += 1
            if damagetaken != 0:
                d = str(
                    u'\U0001F91C' + "|" + user.name + ' M4A1 Vintovkadan ' + str(combo) + " kalibrli o'q orqali "
                    + user.target.name + "ga zarb berayabdi! Yetkazildi " + str(damagetaken) + ' zarb.')
            else:
                d = str(
                    u'\U0001F4A8' + "|" + user.name + ' bitta ham o`q ota olmadi ' + user.target.name + "ga!")
            for a in user.abilities:
                d = a.onhitdesc(a, d, user)
            user.fight.string.add(d)

    def getDesc(self, damagetaken,user):
        if damagetaken != 0:
            user.weaponeffect.append(self)
            if not self.Melee:
                d = str(u'\U0001F4A5' + "|" + getattr(self,str('desc' + str(random.randint(1, 3)))) + " Yetkazildi " + str(damagetaken) + ' zarba.')
            else:
                d = str(u'\U0001F44A' + "|" + getattr(self,str('desc' + str(random.randint(1, 3)))) + " Yetkazildi " + str(damagetaken) + ' zarba.')
            for a in user.abilities:
                d = a.onhitdesc(a, d, user)
            return d
        else:
            return str(u'\U0001F4A8' + "|" + getattr(self,str('desc' + str(random.randint(4, 6)))))


    desc1 = 'O`yinchi Raqibiga Vintovkadan otayabdi!'
    desc2 = 'O`yinchi Raqibiga Vintovkadan otayabdi!'
    desc3 = 'O`yinchi Raqibiga Vintovkadan otayabdi!'
    desc4 = 'O`yinchi Raqibiga Vintovkadan otayabdi, lekin tekkiza olmayabdi.'
    desc5 = 'O`yinchi Raqibiga Vintovkadan otayabdi, lekin tekkiza olmayabdi.'
    desc6 = 'O`yinchi Raqibiga Vintovkadan otayabdi, lekin tekkiza olmayabdi.'

    ####################################################################################    
    
##########################New weapon#########################################


class Drago(Weapon):
    def hit(self,user):
        n = 0
        d = 0
        dmax = self.dice
        print(user.name + " otayabdi " + str(self.name) + 'dan. Uning Energiyasi - ' + str(
            user.energy) + '. Uning aniqligi va qurolning bonus aniqligi - ' + ' '
              + str(user.accuracy) + ' ' + str(self.bonus) +
              '. Tegish ehtimolligi - ' + str(11 - user.energy - self.bonus - user.accuracy - user.tempaccuracy) + "+!")
        while d != dmax:
            x = random.randint(1, 10)
            print(user.name + ' Tushib qoldi ' + str(x))
            if x > 10 - user.energy - self.bonus - user.accuracy - user.tempaccuracy + user.target.evasion:
                n += 1
            d += 1
        for a in user.abilities:
            n = a.onhit(a,n, user)
        if n != 0:
            user.target.firecounter += 1
            user.target.offfire = user.fight.round + 2
            n += user.bonusdamage + self.damage - 1
        else:
            pass
        n += user.truedamage
        # бонусный урон персонажа
        if n != 0:
            n += user.bonusdamage + self.damage - 1
        # уходит энергия
        user.energy -= self.energy
        # энергия загоняется в 0
        if self.Melee:
            user.energy -= random.randint(1, 2)
        else:
            user.energy -= self.energy
        if user.energy < 0 :
            user.energy = 0
        if self.fixed > 0 and n > 0:
            n = self.fixed
        utils.damage(user, user.target, n, 'fire')
        return n
    
    def aquare(self,user):
        user.countercd = 0
        user.counterhit = 2
        if user.fight.round > 1:
            user.throwcd = 3
        else:
            user.itemlist.append(Item_list.throwspear)
            user.throwcd = 0


    def lose(self, user):
        del user.countercd
        del user.counterhit

    def get_action(self, user, call):
        keyboard1 = types.InlineKeyboardMarkup()
        targets = user.targets
        user.turn = call.data
        for c in targets:
            keyboard1.add(types.InlineKeyboardButton(text=c.name, callback_data=str('op' + str(c.chat_id))))
        if user.countercd == 0 and user.energy > 1:
            keyboard1.add(types.InlineKeyboardButton(text="Qizil Ajdar", callback_data=str('aim')))
        keyboard1.add(types.InlineKeyboardButton(text='Bekor qilish', callback_data=str('opcancel')))
        bot.send_message(user.chat_id, 'Raqibni tanlang.', reply_markup=keyboard1)

    def special(self, user, call):

        user.fight.string.add('🐉' + "|" + user.name + ' butun maydonni🌋 qizil alanga bilan to`ldirmoqda. Alanga🏜 ichidan tanasi olovda🌫 yonib turgan Qizil Ajdarlar👹 chiqib kelishdi.')

    def special_second(self, user):
        if user.turn == 'aim':
            user.bonusdamage += 1
            for player in user.targets:
                if player.turn == 'attack' + str(user.fight.round) and user.counterhit > 0 or player.turn == 'weaponspecial' and user.counterhit > 0:
                    user.target = player
                    user.action = str(user.attack())
                    if user.target == user:
                        user.action = user.action.replace('Raqibi', 'o`zizni').\
                            replace('O`yinchi', user.name).replace('Nishon', user.target.name).\
                            replace(u'\U0001F44A',u'\U00002694')
                    else:
                        user.action = user.action.replace('Raqibi', user.target.name). \
                            replace('O`yinchi', user.name).replace('Nishon', user.target.name). \
                            replace(u'\U0001F44A', u'\U00002694')
                    user.fight.string.add(user.action)
                    user.energy += 3
                    user.counterhit -= 1
                    user.target = None
            user.energy -= 3
            user.counterhit = 2
            user.countercd = 3

    def special_end(self, user):
        if user.countercd > 0:
            user.countercd -= 1
        if user.throwcd > 0:
            user.throwcd -= 1
        elif user.throwcd == 0 and Item_list.throwspear not in user.itemlist and user.weapon == self:
            user.itemlist.append(Item_list.throwspear)
 

    def getDesc(self, damagetaken,user):
        if damagetaken != 0:
            d = str(u'\U0001F4A5' + "|"
                           + getattr(self,str('desc' + str(random.randint(1, 3)))) + " Yetkazildi "
                                              + str(damagetaken) + ' zarb.')
            if user.target.firecounter == 1:
                d += u'\U0001F525' + "|" + user.target.name + ' yonayabdi!'
            return d
        else:
            return str(u'\U0001F4A8' + "|" + getattr(self, str('desc' + str(random.randint(4, 6)))))


    desc1 = '👹 O`yinchi Raqibiga olov purkayabdi☄️!'
    desc2 = '👹 O`yinchi Raqibiga olov purkayabdi☄️!'
    desc3 = '👹 O`yinchi Raqibiga olov purkayabdi☄️!'
    desc4 = '👹 O`yinchi Raqibiga olov purkayabdi☄️, lekin tekkiza olmayabdi.'
    desc5 = '👹 O`yinchi Raqibiga olov purkayabdi☄️, lekin tekkiza olmayabdi.'
    desc6 = '👹 O`yinchi Raqibiga olov purkayabdi☄️, lekin tekkiza olmayabdi.'

    ####################################################################################
     
class Spear(Weapon):
    def hit(self,user):
        n = 0
        d = 0
        dmax = self.dice
        print(user.name + " otayabdi " + str(self.name) + 'dan. Uning energiyasi - ' + str(
            user.energy) + '. Uning aniqligi va qurolning bonus aniqligi - ' + ' '
              + str(user.accuracy) + ' ' + str(self.bonus) +
              '. Tegish ehtimolligi - ' + str(11 - user.energy - self.bonus - user.accuracy - user.tempaccuracy) + "+!")
        while d != dmax:
            x = random.randint(1, 10)
            print(user.name + ' Tushib qoldi ' + str(x))
            if x > 10 - user.energy - self.bonus - user.accuracy - user.tempaccuracy + user.target.evasion:
                n += 1
            d += 1
        for a in user.abilities:
            n = a.onhit(a,n, user)

        # бонусный урон персонажа
        if n != 0:
            n += user.bonusdamage + self.damage - 1
        # уходит энергия
        user.energy -= self.energy
        # энергия загоняется в 0
        utils.damage(user, user.target, n, 'melee')
        return n

    def aquare(self,user):
        user.Counter = False
        user.countercd = 0
        user.counterhit = 2

    def lose(self,user):
        del user.Counter
        del user.countercd
        del user.counterhit

    def get_action(self, user, call):
        keyboard1 = types.InlineKeyboardMarkup()
        targets = user.targets
        user.turn = call.data
        for c in targets:
            keyboard1.add(types.InlineKeyboardButton(text=c.name, callback_data=str('op' + str(c.chat_id))))
        if user.countercd == 0 and user.energy > 1:
            keyboard1.add(types.InlineKeyboardButton(text="Kontrxujum", callback_data=str('aim')))
        keyboard1.add(types.InlineKeyboardButton(text='Bekor qilish', callback_data=str('opcancel')))
        bot.send_message(user.chat_id, 'Raqibni tanlang.', reply_markup=keyboard1)

    def special(self, user, call):
        user.Counter = True
        user.countercd = 2
        user.fight.string.add(u'\U00002694' + "|" + user.name + ' kontrxujumga tayorlanayabdi.')

    def special_second(self, user):
        if user.Counter:
            for player in user.targets:
                if player.turn == 'attack' + str(user.fight.round) and user.counterhit > 0 or player.turn == 'weaponspecial' and user.counterhit > 0:
                    user.target = player
                    user.action = str(user.attack())
                    if user.target == user:
                        user.action = user.action.replace('Raqib', 'o`zizni').\
                            replace('O`yinchi', user.name).replace('Nishon', user.target.name).\
                            replace(u'\U0001F44A',u'\U00002694')
                    else:
                        user.action = user.action.replace('Raqib', user.target.name). \
                            replace('O`yinchi', user.name).replace('Nishon', user.target.name). \
                            replace(u'\U0001F44A', u'\U00002694')
                    user.fight.string.add(user.action)
                    user.energy += 3
                    user.counterhit -= 1
                    user.target = None
            user.counterhit = 2
            user.Counter = False
            user.energy -= 2

    def special_end(self, user):
        if user.countercd > 0:
            user.countercd -= 1
    desc1 = 'O`yinchi Raqibiga Nayza otayabdi.'
    desc2 = 'O`yinchi Raqibiga Nayza otayabdi.'
    desc3 = 'O`yinchi Raqibiga Nayza otayabdi.'
    desc4 = 'O`yinchi Raqibiga Nayza otayabdi, lekin tekkiza olmayabdi.'
    desc5 = 'O`yinchi Raqibiga Nayza otayabdi, lekin tekkiza olmayabdi.'
    desc6 = 'O`yinchi Raqibiga Nayza otayabdi, lekin tekkiza olmayabdi.'


class SpearEternal(Weapon):    
    def hit(self,user):
        n = 0
        d = 0
        dmax = self.dice
        print(user.name + " otayabdi " + str(self.name) + 'dan. Uning Energiyasi - ' + str(
            user.energy) + '. Uning aniqligi va qurolning bonus aniqligi - ' + ' '
              + str(user.accuracy) + ' ' + str(self.bonus) +
              '. Tegish ehtimolligi - ' + str(11 - user.energy - self.bonus - user.accuracy - user.tempaccuracy) + "+!")
        while d != dmax:
            x = random.randint(1, 10)
            print(user.name + ' Tushib qoldi ' + str(x))
            if x > 10 - user.energy - self.bonus - user.accuracy - user.tempaccuracy + user.target.evasion:
                n += 1
            d += 1
        for a in user.abilities:
            n = a.onhit(a,n, user)

        # бонусный урон персонажа
        if n != 0:
            n += user.bonusdamage + self.damage - 1
        # уходит энергия
        user.energy -= self.energy
        # энергия загоняется в 0
        utils.damage(user, user.target, n, 'melee')
        return n

    def aquare(self,user):
        user.countercd = 0
        user.counterhit = 2
        if user.fight.round > 1:
            user.throwcd = 1
        else:
            user.itemlist.append(Item_list.throw)
            user.throwcd = 0


    def lose(self, user):
        del user.countercd
        del user.counterhit

    def get_action(self, user, call):
        keyboard1 = types.InlineKeyboardMarkup()
        targets = user.targets
        user.turn = call.data
        for c in targets:
            keyboard1.add(types.InlineKeyboardButton(text=c.name, callback_data=str('op' + str(c.chat_id))))
        if user.countercd == 0 and user.energy > 1:
            keyboard1.add(types.InlineKeyboardButton(text="Sekira kuchi", callback_data=str('aim')))
        keyboard1.add(types.InlineKeyboardButton(text='Bekor qilish', callback_data=str('opcancel')))
        bot.send_message(user.chat_id, 'Raqibni tanlang.', reply_markup=keyboard1)

    def special(self, user, call):
        user.fight.string.add('🌩' + "|" + user.name + ' 𝐨𝐲𝐛𝐨𝐥𝐭𝐚𝐧𝐢 𝐲𝐞𝐫𝐠𝐚 𝐮𝐫𝐝𝐢 𝐯𝐚 𝐛𝐮𝐭𝐮𝐧 𝐣𝐚𝐧𝐠 𝐦𝐚𝐲𝐝𝐨𝐧𝐢𝐠𝐚 𝐨𝐬𝐦𝐨𝐧𝐝𝐚𝐧 𝐜𝐡𝐚𝐪𝐦𝐨𝐪⚡️ 𝐭𝐮𝐬𝐡𝐚 𝐛𝐨𝐬𝐡𝐥𝐚𝐝𝐢.')

    def special_second(self, user):
        if user.turn == 'aim':
            user.bonusdamage += 4
            for player in user.targets:
                if player.turn == 'attack' + str(user.fight.round) and user.counterhit > 0 or player.turn == 'weaponspecial' and user.counterhit > 0:
                    user.target = player
                    user.action = str(user.attack())
                    if user.target == user:
                        user.action = user.action.replace('Raqib', 'o`zizni').\
                            replace('O`yinchi', user.name).replace('Nishon', user.target.name).\
                            replace(u'\U0001F44A',u'\U00002694')
                    else:
                        user.action = user.action.replace('Raqib', user.target.name). \
                            replace('O`yinchi', user.name).replace('Nishon', user.target.name). \
                            replace(u'\U0001F44A', u'\U00002694')
                    user.fight.string.add(user.action)
                    user.energy += 3
                    user.counterhit -= 1
                    user.target = None
            user.energy -= 3
            user.counterhit = 2
            user.countercd = 3

    def special_end(self, user):
        if user.countercd > 0:
            user.countercd -= 1
        if user.throwcd > 0:
            user.throwcd -= 1
        elif user.throwcd == 0 and Item_list.throw not in user.itemlist and user.weapon == self:
            user.itemlist.append(Item_list.throw)  
            
    desc1 = 'O`yinchi oyboltani⛏ otayabdi va Raqibini chaqmoq🌩 urayabdi.'
    desc2 = 'O`yinchi oyboltani⛏ otayabdi va Raqibini chaqmoq🌩 urayabdi.'
    desc3 = 'O`yinchi oyboltani⛏ otayabdi va Raqibini chaqmoq🌩 urayabdi.'
    desc4 = 'O`yinchi oyboltani⛏ otayabdi va Raqibini chaqmoq🌩 urayabdi, lekin zarb yetkaza olmadi.'
    desc5 = 'O`yinchi oyboltani⛏ otayabdi va Raqibini chaqmoq🌩 urayabdi, lekin zarb yetkaza olmadi.'
    desc6 = 'O`yinchi oyboltani⛏ otayabdi va Raqibini chaqmoq🌩 urayabdi, lekin zarb yetkaza olmadi.'

################################################################################################


class Iceman(Weapon):
    def hit(self,user):
        n = 0
        d = 0
        dmax = self.dice
        print(user.name + " otayabdi " + str(self.name) + 'dan. Uning Energiyasi - ' + str(
            user.energy) + '. Uning aniqligi va qurolning bonus aniqligi - ' + ' '
              + str(user.accuracy) + ' ' + str(self.bonus) +
              '. Tegish ehtimolligi - ' + str(11 - user.energy - self.bonus - user.accuracy - user.tempaccuracy) + "+!")
        while d != dmax:
            x = random.randint(1, 10)
            print(user.name + ' Tushib qoldi ' + str(x))
            if x > 10 - user.energy - self.bonus - user.accuracy - user.tempaccuracy + user.target.evasion:
                n += 1
            d += 1
        for a in user.abilities:
            n = a.onhit(a,n, user)

        # бонусный урон персонажа
        if n != 0:
            n += user.bonusdamage + self.damage - 1
        # уходит энергия
        user.energy -= self.energy
        # энергия загоняется в 0
        utils.damage(user, user.target, n, 'melee')
        return n

    def aquare(self,user):
        user.countercd = 0
        user.counterhit = 2
        if user.fight.round > 1:
            user.throwcd = 3
        else:
            user.itemlist.append(Item_list.throwspear)
            user.throwcd = 0


    def lose(self, user):
        del user.countercd
        del user.counterhit

    def get_action(self, user, call):
        keyboard1 = types.InlineKeyboardMarkup()
        targets = user.targets
        user.turn = call.data
        for c in targets:
            keyboard1.add(types.InlineKeyboardButton(text=c.name, callback_data=str('op' + str(c.chat_id))))
        if user.countercd == 0 and user.energy > 1:
            keyboard1.add(types.InlineKeyboardButton(text="Muzli halqa", callback_data=str('aim')))
        keyboard1.add(types.InlineKeyboardButton(text='Bekor qilish', callback_data=str('opcancel')))
        bot.send_message(user.chat_id, 'Raqibni tanlang.', reply_markup=keyboard1)

    def special(self, user, call):

        user.fight.string.add(u'\U00002694' + "|" + user.name + ' atrofiga muzli halqa🍥 hosil qildi.')

    def special_second(self, user):
        if user.turn == 'aim':
            user.bonusdamage += 1
            for player in user.targets:
                if player.turn == 'attack' + str(user.fight.round) and user.counterhit > 0 or player.turn == 'weaponspecial' and user.counterhit > 0:
                    user.target = player
                    user.action = str(user.attack())
                    if user.target == user:
                        user.action = user.action.replace('Raqibi', 'o`zizni').\
                            replace('O`yinchi', user.name).replace('Nishon', user.target.name).\
                            replace(u'\U0001F44A',u'\U00002694')
                    else:
                        user.action = user.action.replace('Raqibi', user.target.name). \
                            replace('O`yinchi', user.name).replace('Nishon', user.target.name). \
                            replace(u'\U0001F44A', u'\U00002694')
                    user.fight.string.add(user.action)
                    user.energy += 3
                    user.counterhit -= 1
                    user.target = None
            user.energy -= 3
            user.counterhit = 2
            user.countercd = 3

    def special_end(self, user):
        if user.countercd > 0:
            user.countercd -= 1
        if user.throwcd > 0:
            user.throwcd -= 1
        elif user.throwcd == 0 and Item_list.throwspear not in user.itemlist and user.weapon == self:
            user.itemlist.append(Item_list.throwspear)
  
    def special_end(self, user):
        if user.turn == 'attack' + str(user.fight.round):
            if user.target.turn == 'reload' + str(user.fight.round) or 'dog_rest' + str(user.fight.round):
                user.target.energy -= 3
                user.fight.string.add('❄️' + user.target.name + ' 3 energiyasi muzlamoqda.')
        
    desc1 = 'O`yinchi Raqibini Muzli Kristal❄️ bilan sexrlayabdi.'
    desc2 = 'O`yinchi Raqibini Muzli Kristal❄️ bilan sexrlayabdi.'
    desc3 = 'O`yinchi Raqibini Muzli Kristal❄️ bilan sexrlayabdi.'
    desc4 = 'O`yinchi Raqibini Muzli Kristal❄️ bilan sexrlayabdi, lekin tekkiza olmayabdi.'
    desc5 = 'O`yinchi Raqibini Muzli Kristal❄️ bilan sexrlayabdi, lekin tekkiza olmayabdi.'
    desc6 = 'O`yinchi Raqibini Muzli Kristal❄️ bilan sexrlayabdi, lekin tekkiza olmayabdi.'


#########################################################################################
class Flamethrower(Weapon):
    def hit(self,user):
        n = 0
        d = 0
        dmax = self.dice
        print(user.name + " otayabdi " + str(self.name) + 'dan. Uning energiyasi - ' + str(
            user.energy) + '. Uning aniqligi va qurolning bonus aniqligi - ' + ' '
              + str(user.accuracy) + ' ' + str(self.bonus) +
              '. Tegish ehtimolligi - ' + str(11 - user.energy - self.bonus - user.accuracy - user.tempaccuracy) + "+!")
        while d != dmax:
            x = random.randint(1, 10)
            print(user.name + ' Tushib qoldi ' + str(x))
            if x > 10 - user.energy - self.bonus - user.accuracy - user.tempaccuracy + user.target.evasion:
                n += 1
            d += 1
        if n != 0:
            user.target.firecounter += 1
            user.target.offfire = user.fight.round + 2
            n += user.bonusdamage + self.damage - 1
        else:
            pass
        n += user.truedamage
        # энергия загоняется в 0
        if self.Melee:
            user.energy -= random.randint(1, 2)
        else:
            user.energy -= self.energy
        if user.energy < 0 :
            user.energy = 0
        if self.fixed > 0 and n > 0:
            n = self.fixed
        utils.damage(user, user.target, n, 'fire')
        return n

    def getDesc(self, damagetaken,user):
        if damagetaken != 0:
            d = str(u'\U0001F4A5' + "|"
                           + getattr(self,str('desc' + str(random.randint(1, 3)))) + " Yetkazildi "
                                              + str(damagetaken) + ' zarb.')
            if user.target.firecounter == 1:
                d += u'\U0001F525' + "|" + user.target.name + ' yonayabdi!'
            return d
        else:
            return str(u'\U0001F4A8' + "|" + getattr(self, str('desc' + str(random.randint(4, 6)))))


    desc1 = 'O`yinchi Raqibiga Ognemyotdan otayabdi!'
    desc2 = 'O`yinchi Raqibiga Ognemyotdan otayabdi!'
    desc3 = 'O`yinchi Raqibiga Ognemyotdan otayabdi!'
    desc4 = 'O`yinchi Raqibiga Ognemyotdan otayabdi, lekin tekkiza olmayabdi.'
    desc5 = 'O`yinchi Raqibiga Ognemyotdan otayabdi, lekin tekkiza olmayabdi.'
    desc6 = 'O`yinchi Raqibiga Ognemyotdan otayabdi, lekin tekkiza olmayabdi.'


class Bleeding(Weapon):
    def __init__(self, dice, damage, energy, bonus, fixed, Melee, TwoHanded, Concealable, name, damagestring, chance,
                 standart=True,natural=False):
        Weapon.__init__(self, dice, damage, energy, bonus, fixed, Melee, TwoHanded, Concealable, name, damagestring,standart=standart,natural=natural)
        self.chance = chance

    def hit(self,user):
        n = 0
        d = 0
        dmax = self.dice
        print(user.name + " otayabdi " + str(self.name) + 'dan. Uning energiyasi - ' + str(
            user.energy) + '. Uning aniqligi va qurolning bonus aniqligi - ' + ' '
              + str(user.accuracy) + ' ' + str(self.bonus) +
              '. Tegish ehtimolligi - ' + str(11 - user.energy - self.bonus - user.accuracy - user.tempaccuracy) + "+!")
        while d != dmax:
            x = random.randint(1, 10)
            print(user.name + ' Tushib qoldi ' + str(x))
            if x > 10 - user.energy - self.bonus - user.accuracy - user.tempaccuracy + user.target.evasion:
                n += 1
            d += 1
        if n != 0 and random.randint(1,10)< self.chance:
            user.target.bleedcounter += 1
            user.target.bloodloss = False
            user.Hitability = True

            # бонусный урон персонажа
        # уходит энергия
        user.energy -= self.energy
        if n!=0:
            n += user.bonusdamage + self.damage - 1

        for a in user.abilities:
            n = a.onhit(a, n, user)
        else:
            pass
        n += user.truedamage
        # энергия загоняется в 0

        if user.energy < 0: user.energy = 0
        utils.damage(user, user.target, n, 'melee')
        print('bleed')
        return n

    def getDesc(self, damagetaken,user):
        if damagetaken != 0:
            if not self.Melee:
                d =  str(u'\U0001F4A5' + "|" + getattr(self,str('desc' + str(random.randint(1, 3)))) + " Yetkazildi " + str(damagetaken) + ' zarba.')
            else:
                d =  str(u'\U0001F44A' + "|" + getattr(self,str('desc' + str(random.randint(1, 3)))) + " Yetkazildi " + str(damagetaken) + ' zarba.')
            if user.target.bleedcounter == 1 and user.Hitability:
                d += u'\U00002763' + "|" + user.target.name + ' qon yo`qotayabdi!'
            elif user.target.bleedcounter > 1 and user.Hitability:
                d += u'\U00002763' + "|" 'Qon yo`qotishi ortayabdi!'
            for a in user.abilities:
                d = a.onhitdesc(a,d,user)
            return d
        else:
            return str(u'\U0001F4A8' + "|" + getattr(self,str('desc' + str(random.randint(4, 6)))))


class Burning(Weapon):
    def __init__(self, dice, damage, energy, bonus, fixed, Melee, TwoHanded, Concealable, name, damagestring, chance,
                 standart=True,natural=False):
        Weapon.__init__(self, dice, damage, energy, bonus, fixed, Melee, TwoHanded, Concealable, name, damagestring,standart=standart,natural=natural)
        self.chance = chance

    def hit(self,user):
        n = 0
        d = 0
        dmax = self.dice
        print(user.name + " otayabdi " + str(self.name) + '. Uning energiyasi - ' + str(
            user.energy) + '. Uning aniqligi va qurolning bonus aniqligi - ' + ' '
              + str(user.accuracy) + ' ' + str(self.bonus) +
              '. Tegish ehtimolligi - ' + str(11 - user.energy - self.bonus - user.accuracy - user.tempaccuracy) + "+!")
        while d != dmax:
            x = random.randint(1, 10)
            print(user.name + ' Tushib qoldi ' + str(x))
            if x > 10 - user.energy - self.bonus - user.accuracy - user.tempaccuracy + user.target.evasion:
                n += 1
            d += 1
        if n != 0 and random.randint(1,10)< self.chance:
            user.target.firecounter += 1
            user.target.offfire = user.fight.round + 2
            user.Hitability = True

            # бонусный урон персонажа
        # уходит энергия
        user.energy -= self.energy
        if n!=0:
            n += user.bonusdamage + self.damage - 1

        for a in user.abilities:
            n = a.onhit(a, n, user)
        else:
            pass
        n += user.truedamage
        # энергия загоняется в 0

        if user.energy < 0: user.energy = 0
        utils.damage(user, user.target, n, 'melee')
        print('bleed')
        return n

    def getDesc(self, damagetaken,user):
        if damagetaken != 0:
            if not self.Melee:
                d = str(u'\U0001F4A5' + "|" + getattr(self,str('desc' + str(random.randint(1, 3)))) + " Yetkazildi " + str(damagetaken) + ' zarba.')
            else:
                d = str(u'\U0001F44A' + "|" + getattr(self,str('desc' + str(random.randint(1, 3)))) + " Yetkazildi " + str(damagetaken) + ' zarba.')
            if user.target.firecounter == 1 and user.Hitability:
                d += u'\U0001F525' + "|" + user.target.name + ' yonayabdi!'
            elif user.target.firecounter > 1 and user.Hitability:
                d += u'\U0001F525' + "|" 'Olov kuchaymoqda!'
            for a in user.abilities:
                d = a.onhitdesc(a,d,user)
            return d
        else:
            return str(u'\U0001F4A8' + "|" + getattr(self,str('desc' + str(random.randint(4, 6)))))

######################################################################################################

class Olovlis(Weapon):
    def __init__(self, dice, damage, energy, bonus, fixed, Melee, TwoHanded, Concealable, name, damagestring, chance,
                 standart=True,natural=False):
        Weapon.__init__(self, dice, damage, energy, bonus, fixed, Melee, TwoHanded, Concealable, name, damagestring,standart=standart,natural=natural)
        self.chance = chance

    def hit(self,user):
        n = 0
        d = 0
        dmax = self.dice
        print(user.name + " otayabdi " + str(self.name) + '. Uning energiyasi - ' + str(
            user.energy) + '. Uning aniqligi va qurolning bonus aniqligi - ' + ' '
              + str(user.accuracy) + ' ' + str(self.bonus) +
              '. Tegish ehtimolligi - ' + str(11 - user.energy - self.bonus - user.accuracy - user.tempaccuracy) + "+!")
        while d != dmax:
            x = random.randint(1, 10)
            print(user.name + ' Tushib qoldi ' + str(x))
            if x > 10 - user.energy - self.bonus - user.accuracy - user.tempaccuracy + user.target.evasion:
                n += 1
            d += 1
        if n != 0 and random.randint(1,10)< self.chance:
            user.target.firecounter += 2
            user.target.offfire = user.fight.round + 2
            user.Hitability = True

            # бонусный урон персонажа
        # уходит энергия
        user.energy -= self.energy
        if n!=0:
            n += user.bonusdamage + self.damage - 1

        for a in user.abilities:
            n = a.onhit(a, n, user)
        else:
            pass
        n += user.truedamage
        # энергия загоняется в 0

        if user.energy < 0: user.energy = 0
        utils.damage(user, user.target, n, 'melee')
        print('bleed')
        return n

    def getDesc(self, damagetaken,user):
        if damagetaken != 0:
            if not self.Melee:
                d = str('🔥' + "|" + getattr(self,str('desc' + str(random.randint(1, 3)))) + " Yetkazildi " + str(damagetaken) + ' zarba.')
            else:
                d = str('🔥' + "|" + getattr(self,str('desc' + str(random.randint(1, 3)))) + " Yetkazildi " + str(damagetaken) + ' zarba.')
            if user.target.firecounter == 1 and user.Hitability:
                d += u'\U0001F525' + "|" + user.target.name + ' yonayabdi!'
            elif user.target.firecounter > 2 and user.Hitability:
                d += u'\U0001F525' + "|" 'Olov kuchaymoqda!'
            for a in user.abilities:
                d = a.onhitdesc(a,d,user)
            return d
        else:
            return str(u'\U0001F4A8' + "|" + getattr(self,str('desc' + str(random.randint(4, 6)))))

#################################################################################
class Stunning(Weapon):
    def __init__(self, dice, damage, energy, bonus, fixed, Melee, TwoHanded, Concealable, name, damagestring, chance,
                 standart=True,natural=False):
        Weapon.__init__(self, dice, damage, energy, bonus, fixed, Melee, TwoHanded, Concealable, name, damagestring,
                        standart=standart,natural=natural)
        self.chance = chance

    def hit(self,user):
        n = 0
        d = 0
        dmax = self.dice
        print(user.name + " otayabdi " + str(self.name) + 'dan. Uning energiyasi - ' + str(
            user.energy) + '.  Uning aniqligi va qurolning bonus aniqligi - ' + ' '
              + str(user.accuracy) + ' ' + str(self.bonus) +
              '. Tegish ehtimolligi - ' + str(11 - user.energy - self.bonus - user.accuracy - user.tempaccuracy) + "+!")
        while d != dmax:
            x = random.randint(1, 10)
            print(user.name + ' Tushib qoldi ' + str(x))
            if x > 10 - user.energy - self.bonus - user.accuracy - user.tempaccuracy + user.target.evasion:
                n += 1
            d += 1


            # бонусный урон персонажа
        # уходит энергия
        user.energy -= self.energy
        if n!=0:
            n += user.bonusdamage + self.damage - 1
            for a in user.abilities:
                n = a.onhit(a,n, user)
        else:
            pass
        n += user.truedamage
        # применяется урон
        # энергия загоняется в 0

        if user.energy < 0: user.energy = 0

        utils.damage(user, user.target, n, 'melee')
        return n

    def effect(self, user):
        if random.randint(1,10)< self.chance:
            if user.target.stuncounter < 1:
                user.target.stuncounter = 1
            user.fight.string.add(u'\U0001F300' + '|' + user.target.name + ' karaxtlandi!')
        user.weaponeffect.remove(self)

    def getDesc(self, damagetaken,user):
        if damagetaken != 0:
            user.weaponeffect.append(self)
            if not self.Melee:
                d = str(u'\U0001F4A5' + "|" + getattr(self,str('desc' + str(random.randint(1, 3)))) + " Yetkazildi " + str(damagetaken) + ' zarba.')
            else:
                d = str(u'\U0001F44A' + "|" + getattr(self,str('desc' + str(random.randint(1, 3)))) + " Yetkazildi " + str(damagetaken) + ' zarba.')
            for a in user.abilities:
                d = a.onhitdesc(a, d, user)
            return d
        else:
            return str(u'\U0001F4A8' + "|" + getattr(self,str('desc' + str(random.randint(4, 6)))))


class Crippling(Weapon):
    def __init__(self, dice, damage, energy, bonus, fixed, Melee, TwoHanded, Concealable, name, damagestring, chance,
                 standart=True,natural=False):
        Weapon.__init__(self, dice, damage, energy, bonus, fixed, Melee, TwoHanded, Concealable, name, damagestring,
                        standart=standart,natural=natural)
        self.chance = chance

    def hit(self, user):
        n = 0
        d = 0
        dmax = self.dice
        print(user.name + " otayabdi " + str(self.name) + 'dan. Uning energiyasi - ' + str(
            user.energy) + '. Uning aniqligi va qurolning bonus aniqligi - ' + ' '
              + str(user.accuracy) + ' ' + str(self.bonus) +
              '. Tegish ehtimolligi - ' + str(11 - user.energy - self.bonus - user.accuracy - user.tempaccuracy) + "+!")
        while d != dmax:
            x = random.randint(1, 10)
            print(user.name + ' Tushib qoldi ' + str(x))
            if x > 10 - user.energy - self.bonus - user.accuracy - user.tempaccuracy + user.target.evasion:
                n += 1
            d += 1


            # бонусный урон персонажа
        # уходит энергия
        user.energy -= self.energy
        if n!=0:
            n += user.bonusdamage + self.damage - 1

        for a in user.abilities:
            n = a.onhit(a,n, user)
        else:
            pass
        n += user.truedamage
        # применяется урон
        # энергия загоняется в 0
        if user.energy < 0: user.energy = 0

        utils.damage(user, user.target, n, 'melee')
        return n

    def effect(self, user):
        if random.randint(1, 10) <= self.chance:
            if user.target.toughness > 2:
                user.target.toughness -= 1
            if user.target.toughness > 2:
                user.fight.string.add(u'\U0001F915' + '|' + user.target.name + ' yaralandi!')
            else:
                user.fight.string.add(u'\U0001F915' + '|' + user.target.name + ' yaralandi! Ta`sir maksimal.')
        user.weaponeffect.remove(self)

    def getDesc(self, damagetaken,user):
        if damagetaken != 0:
            user.weaponeffect.append(self)
            if not self.Melee:
                d = str(u'\U0001F4A5' + "|" + getattr(self,str('desc' + str(random.randint(1, 3)))) + " Yetkazildi " + str(damagetaken) + ' zarba.')
            else:
                d = str(u'\U0001F44A' + "|" + getattr(self,str('desc' + str(random.randint(1, 3)))) + " Yetkazildi " + str(damagetaken) + ' zarba.')
            for a in user.abilities:
                d = a.onhitdesc(a, d, user)
            return d
        else:
            return str(u'\U0001F4A8' + "|" + getattr(self,str('desc' + str(random.randint(4, 6)))))


class Dropping(Weapon):
    def __init__(self, dice, damage, energy, bonus, fixed, Melee, TwoHanded, Concealable, name, damagestring, chance,
                 standart=True,natural=False):
        Weapon.__init__(self, dice, damage, energy, bonus, fixed, Melee, TwoHanded, Concealable, name, damagestring,
                        standart=standart,natural=natural)
        self.chance = chance

    def aquare(self, user):
        user.dropcd = 0

    def lose(self, user):
        del user.dropcd

    def get_action(self, p, call):
        keyboard1 = types.InlineKeyboardMarkup()
        enemyteam = p.targets
        p.turn = call.data
        for c in enemyteam:
            if p.dropcd != 0 or c.weapon.natural:
                keyboard1.add(types.InlineKeyboardButton(text=c.name, callback_data=str('op' + str(c.chat_id))))
            else:
                keyboard1.add(types.InlineKeyboardButton(text=c.name, callback_data=str('op' + str(c.chat_id))),
                              types.InlineKeyboardButton(text="Qurolini tushirish", callback_data=str('weaponspecial'
                                                                                                 + str(c.chat_id))))

        keyboard1.add(types.InlineKeyboardButton(text='Bekor qilish', callback_data=str('opcancel')))
        bot.send_message(p.chat_id, 'Raqibni tanlang.', reply_markup=keyboard1)

    def hit(self,user):
        n = 0
        d = 0
        dmax = self.dice
        print(user.name + " otayabdi " + str(self.name) + 'dan. Uning energiyasi - ' + str(
            user.energy) + '. Uning aniqligi va qurolning bonus aniqligi - ' + ' '
              + str(user.accuracy) + ' ' + str(self.bonus) +
              '. Tegish ehtimolligi - ' + str(11 - user.energy - self.bonus - user.accuracy - user.tempaccuracy) + "+!")
        while d != dmax:
            x = random.randint(1, 10)
            print(user.name + ' Tushib qoldi ' + str(x))
            if x > 10 - user.energy - self.bonus - user.accuracy - user.tempaccuracy:
                n += 1
            d += 1


            # бонусный урон персонажа
        # уходит энергия
        user.energy -= self.energy
        if n!=0:
            n += user.bonusdamage + self.damage - 1

        for a in user.abilities:
            n = a.onhit(a,n, user)
        else:
            pass
        n += user.truedamage
        if user.energy < 0: user.energy = 0
        utils.damage(user, user.target, n, 'melee')
        return n

    def effect(self, user):
        if user.target.turn == 'attack' + str(user.fight.round) and random.randint(1, 10) or \
                user.target.turn == 'weaponspecial' and random.randint(1, 10) <= self.chance:
            if not user.target.weapon.natural:
                user.target.lostweapon = user.target.weapon
                user.fight.string.add(u'\U0001F450' + '|' + user.target.name + ' o`z qurolini yo`qotayabdi!')
        elif user.target.turn == 'reload' + str(user.fight.round):
            if not user.target.weapon.natural:
                user.target.lostweapon = user.target.weapon
                user.fight.string.add(u'\U0001F450' + '|' + user.target.name + ' o`z qurolini yo`qotayabdi!')
        user.weaponeffect.remove(self)

    def getDesc(self, damagetaken, user):
        if damagetaken != 0:
            if not self.Melee:
                d = str(u'\U0001F4A5' + "|" + getattr(self,str('desc' + str(random.randint(1, 3)))) + " Yetkazildi " + str(damagetaken) + ' zarba.')
            else:
                d = str(u'\U0001F44A' + "|" + getattr(self,str('desc' + str(random.randint(1, 3)))) + " Yetkazildi " + str(damagetaken) + ' zarba.')
            for a in user.abilities:
                d = a.onhitdesc(a, d, user)
            return d
        else:
            return str(u'\U0001F4A8' + "|" + getattr(self,str('desc' + str(random.randint(4, 6)))))

    def special(self, user, call):
        user.target = utils.actor_from_id(call, user.game)
        user.dropcd = 4

    def special_second(self, user):
        if user.dropcd > 0:
            user.dropcd -= 1
        if user.turn == 'weaponspecial':
            damagetaken = self.hit(user)
            user.energy -= 1
            if damagetaken != 0:
                user.weaponeffect.append(self)
                d = str(
                    u'\U000026D3' + "|" + user.name + ' raqibi '
                    + user.target.name + " qo`lidagi qurolini tushirib yuborishga urinayabdi! Yetkazildi " + str(damagetaken) + ' zarba.')
            else:
                d = str(
                    u'\U0001F4A8' + "|" + user.name + ' raqibi ' + user.target.name + "qo`lidagi qurolini tushirib yuborishga urinayabdi!")
            for a in user.abilities:
                d = a.onhitdesc(a, d, user)
            user.fight.string.add(d)

########################################################################################################

class Magniy(Weapon):
    def __init__(self, dice, damage, energy, bonus, fixed, Melee, TwoHanded, Concealable, name, damagestring, chance,
                 standart=True,natural=False):
        Weapon.__init__(self, dice, damage, energy, bonus, fixed, Melee, TwoHanded, Concealable, name, damagestring,
                        standart=standart,natural=natural)
        self.chance = chance

    def aquare(self, user):
        user.dropcd = 0

    def lose(self, user):
        del user.dropcd

    def get_action(self, p, call):
        keyboard1 = types.InlineKeyboardMarkup()
        enemyteam = p.targets
        p.turn = call.data
        for c in enemyteam:
            if p.dropcd != 0 or c.weapon.natural:
                keyboard1.add(types.InlineKeyboardButton(text=c.name, callback_data=str('op' + str(c.chat_id))))
            else:
                keyboard1.add(types.InlineKeyboardButton(text=c.name, callback_data=str('op' + str(c.chat_id))),
                              types.InlineKeyboardButton(text="Mutloq kuch", callback_data=str('weaponspecial'
                                                                                                 + str(c.chat_id))))

        keyboard1.add(types.InlineKeyboardButton(text='Bekor qilish', callback_data=str('opcancel')))
        bot.send_message(p.chat_id, 'Raqibni tanlang.', reply_markup=keyboard1)

    def hit(self,user):
        n = 0
        d = 0
        dmax = self.dice
        print(user.name + " otayabdi " + str(self.name) + 'dan. Uning energiyasi - ' + str(
            user.energy) + '. Uning aniqligi va qurolning bonus aniqligi - ' + ' '
              + str(user.accuracy) + ' ' + str(self.bonus) +
              '. Tegish ehtimolligi - ' + str(11 - user.energy - self.bonus - user.accuracy - user.tempaccuracy) + "+!")
        while d != dmax:
            x = random.randint(1, 10)
            print(user.name + ' Tushib qoldi ' + str(x))
            if x > 10 - user.energy - self.bonus - user.accuracy - user.tempaccuracy:
                n += 1
            d += 1


            # бонусный урон персонажа
        # уходит энергия
        user.energy -= self.energy
        if n!=0:
            n += user.bonusdamage + self.damage - 1

        for a in user.abilities:
            n = a.onhit(a,n, user)
        else:
            pass
        n += user.truedamage
        if user.energy < 0: user.energy = 0
        utils.damage(user, user.target, n, 'melee')
        return n

    def effect(self, user):
        if user.target.turn == 'attack' + str(user.fight.round) and random.randint(1, 10) or \
                user.target.turn == 'weaponspecial' and random.randint(1, 10) <= self.chance:
            if not user.target.weapon.natural:
                user.target.lostweapon = user.target.weapon
                user.fight.string.add('⚰️' + '|' + user.target.name + ' - AJAL☠️ OLDIDA O`ZINI OJIZ EKANLIGINI HIS QILIB🕯 QUROLINI TASHLAB YUBORAYABDI!')
        elif user.target.turn == 'reload' + str(user.fight.round):
            if not user.target.weapon.natural:
                user.target.lostweapon = user.target.weapon
                user.fight.string.add('⚰️' + '|' + user.target.name + ' - AJAL☠️ OLDIDA O`ZINI OJIZ EKANLIGINI HIS QILIB🕯 QUROLINI TASHLAB YUBORAYABDI!')
        user.weaponeffect.remove(self)

    def getDesc(self, damagetaken, user):
        if damagetaken != 0:
            if not self.Melee:
                d = str(u'\U0001F4A5' + "|" + getattr(self,str('desc' + str(random.randint(1, 3)))) + " Yetkazildi " + str(damagetaken) + ' zarba.')
            else:
                d = str(u'\U0001F44A' + "|" + getattr(self,str('desc' + str(random.randint(1, 3)))) + " Yetkazildi " + str(damagetaken) + ' zarba.')
            for a in user.abilities:
                d = a.onhitdesc(a, d, user)
            return d
        else:
            return str(u'\U0001F4A8' + "|" + getattr(self,str('desc' + str(random.randint(4, 6)))))

    def special(self, user, call):
        user.target = utils.actor_from_id(call, user.game)
        user.dropcd = 4

    def special_second(self, user):
        if user.dropcd > 0:
            user.dropcd -= 1
        if user.turn == 'weaponspecial':
            damagetaken = self.hit(user)
            user.energy -= 1
            if damagetaken != 0:
                user.weaponeffect.append(self)
                d = str(
                    '🌕' + "|" + user.name + ' O`ZINING MUTLOQ QUDRATINI🌓 KO`RSATMOQDA! '
                    + user.target.name + " - YURAGIDA QATTIQ OG`RIQNI🖤 HIS QILA BOSHLADI! YETKAZILDI " + str(damagetaken) + ' ZARBA🌑.')
            else:
                d = str(
                    '🌕' + "|" + user.name + ' O`ZINING MUTLOQ QUDRATINI🌓 KO`RSATMOQDA! ' + user.target.name + " - YURAGIDA QATTIQ OG`RIQNI🖤 HIS QILA BOSHLADI!")
            for a in user.abilities:
                d = a.onhitdesc(a, d, user)
            user.fight.string.add(d)

#######################################################################################################
class Crushing(Weapon):

    def aquare(self, user):
        user.crushcd = 0

    def lose(self, user):
        del user.crushcd

    def get_action(self, p, call):
        keyboard1 = types.InlineKeyboardMarkup()
        enemyteam = p.targets
        p.turn = call.data
        for c in enemyteam:
            if p.crushcd != 0 or p.energy < 4:
                keyboard1.add(types.InlineKeyboardButton(text=c.name, callback_data=str('op' + str(c.chat_id))))
            else:
                keyboard1.add(types.InlineKeyboardButton(text=c.name, callback_data=str('op' + str(c.chat_id))),
                              types.InlineKeyboardButton(text="Qulatish", callback_data=str('weaponspecial'
                                                                                                 + str(c.chat_id))))

        keyboard1.add(types.InlineKeyboardButton(text='Bekor qilish', callback_data=str('opcancel')))
        bot.send_message(p.chat_id, 'Raqibni tanlang.', reply_markup=keyboard1)

    def special(self, user, call):
        user.target = utils.actor_from_id(call, user.game)

    def hit_sp(self, user):
        n = 0
        d = 0
        dmax = self.dice
        print(user.name + " otayabdi " + str(self.name) + '. Uning energiyasi - ' + str(
            user.energy) + '. Uning aniqligi va qurolning bonus aniqligi - ' + ' '
              + str(user.accuracy) + ' ' + str(self.bonus) +
              '. Tegish ehtimolligi - ' + str(11 - user.energy - self.bonus - user.accuracy - user.tempaccuracy) + "+!")
        while d != dmax:
            x = random.randint(1, 10)
            print(user.name + ' Tushib qoldi ' + str(x))
            if x > 10 - user.energy - self.bonus - user.accuracy - user.tempaccuracy + user.target.evasion:
                n += 1
            d += 1
        # бонусный урон персонажа
        # уходит энергия
        user.energy -= self.energy
        if n != 0:
            n += user.bonusdamage + self.damage + user.crushdamage

        for a in user.abilities:
            n = a.onhit(a, n, user)
        else:
            pass
        n += user.truedamage
        # энергия загоняется в 0

        if user.energy < 0: user.energy = 0

        print('bleed')
        utils.damage(user, user.target, n, 'melee')
        return n

    def special_second(self, user):
        if user.crushcd > 0:
            user.crushcd -= 1
        if user.turn == 'weaponspecial':
            user.crushdamage = user.target.maxenergy - user.target.energy - 1
            user.tempaccuracy -= 1
            damagetaken = self.hit_sp(user)
            if damagetaken != 0:
                d = str(
                    u'\U0001F528' + "|" + user.name + ' qulatuvchi zarbani ' + user.target.name
                    + "ga berayabdi! Yetkazildi " + str(damagetaken) + ' zarb.')
            else:
                d = str(
                    u'\U0001F4A8' + "|" + user.name
                    + ' Kuvalda bilan qulatuvchi zarb berayabdi, lekin tekkiza olmayabdi ' + user.target.name + "!")
            for a in user.abilities:
                d = a.onhitdesc(a, d, user)
            user.fight.string.add(d)
            user.energy -= 2
            user.crushcd = 3
            del user.crushdamage

#####################################################################################
class Elektrez(Weapon):

    def aquare(self, user):
        user.crushcd = 0

    def lose(self, user):
        del user.crushcd

    def get_action(self, p, call):
        keyboard1 = types.InlineKeyboardMarkup()
        enemyteam = p.targets
        p.turn = call.data
        for c in enemyteam:
            if p.crushcd != 0 or p.energy < 4:
                keyboard1.add(types.InlineKeyboardButton(text=c.name, callback_data=str('op' + str(c.chat_id))))
            else:
                keyboard1.add(types.InlineKeyboardButton(text=c.name, callback_data=str('op' + str(c.chat_id))),
                              types.InlineKeyboardButton(text="Elektron Oqimi", callback_data=str('weaponspecial'
                                                                                                 + str(c.chat_id))))

        keyboard1.add(types.InlineKeyboardButton(text='Bekor qilish', callback_data=str('opcancel')))
        bot.send_message(p.chat_id, 'Raqibni tanlang.', reply_markup=keyboard1)

    def special(self, user, call):
        user.target = utils.actor_from_id(call, user.game)

    def hit_sp(self, user):
        n = 0
        d = 0
        dmax = self.dice
        print(user.name + " otayabdi " + str(self.name) + '. Uning energiyasi - ' + str(
            user.energy) + '. Uning aniqligi va qurolning bonus aniqligi - ' + ' '
              + str(user.accuracy) + ' ' + str(self.bonus) +
              '. Tegish ehtimolligi - ' + str(11 - user.energy - self.bonus - user.accuracy - user.tempaccuracy) + "+!")
        while d != dmax:
            x = random.randint(1, 10)
            print(user.name + ' Tushib qoldi ' + str(x))
            if x > 10 - user.energy - self.bonus - user.accuracy - user.tempaccuracy + user.target.evasion:
                n += 1
            d += 1
        # бонусный урон персонажа
        # уходит энергия
        user.energy -= self.energy
        if n != 0:
            n += user.bonusdamage + self.damage + user.crushdamage

        for a in user.abilities:
            n = a.onhit(a, n, user)
        else:
            pass
        n += user.truedamage
        # энергия загоняется в 0

        if user.energy < 0: user.energy = 0

        print('bleed')
        utils.damage(user, user.target, n, 'melee')
        return n

    def special_second(self, user):
        if user.crushcd > 0:
            user.crushcd -= 1
        if user.turn == 'weaponspecial':
            user.crushdamage = user.target.maxenergy - user.target.energy - 1
            user.tempaccuracy -= 1
            damagetaken = self.hit_sp(user)
            if damagetaken != 0:
                d = str(
                    '🗡' + "|" + user.name + ' ⚡️𝙀𝙡𝙚𝙠𝙩𝙧𝙤𝙣𝙡𝙖𝙧⚡️ 𝗼𝗾𝗶𝗺𝗶 ' + user.target.name
                    + "𝗻𝗶𝗻𝗴 𝗺𝗶𝘆𝗮 𝗵𝘂𝗷𝗮𝘆𝗿𝗮𝗹𝗮𝗿𝗶𝗻𝗶 𝗼'𝗹𝗱𝗶𝗿𝗮𝘆𝗮𝗯𝗱𝗶🆘! 𝗘𝗹𝗲𝗸𝘁𝗿𝗼𝗳𝗼𝗿𝗲𝘇 " + str(damagetaken) + '❕ 𝗺𝗶𝗾𝗱𝗼𝗿𝗱𝗮 𝘇𝗮𝗿𝗮𝗿 𝘆𝗲𝘁𝗸𝗮𝘇𝗱𝗶.')
            else:
                d = str(
                    '🗡' + "|" + user.name
                    + ' ⚡️𝗘𝗹𝗲𝗸𝘁𝗿𝗼𝗻𝗹𝗮𝗿⚡️ 𝘇𝗮𝗿𝘆𝗮𝗱𝗶 ' + user.target.name + "𝗴𝗮 𝘇𝗮𝗿𝗯𝗮 𝗯𝗲𝗿𝗶𝘀𝗵 𝘂𝗰𝗵𝘂𝗻 𝘆𝗲𝘁𝗮𝗿𝗹𝗶 𝗯𝗼`𝗹𝗺𝗮𝗱𝗶!")
            for a in user.abilities:
                d = a.onhitdesc(a, d, user)
            user.fight.string.add(d)
            user.energy -= 2
            user.crushcd = 3
            del user.crushdamage

            
    def special_end(self, user):
        if user.turn == 'attack' + str(user.fight.round):
            if user.target.turn == 'reload' + str(user.fight.round) or 'dog_rest' + str(user.fight.round):
                user.target.energy -= 2
                user.fight.string.add(u'\U000026A1' + user.target.name + ' 2 energiyasini⚛️ elektr toki so`rib oldi.')
####################################################################################
class MasterFist(Weapon):

    def get_action(self, p, call):
        keyboard1 = types.InlineKeyboardMarkup()
        enemyteam = p.targets
        p.turn = call.data
        for c in enemyteam:
            if p.energy < 3:
                keyboard1.add(types.InlineKeyboardButton(text=c.name, callback_data=str('op' + str(c.chat_id))))
            else:
                keyboard1.add(types.InlineKeyboardButton(text=c.name, callback_data=str('op' + str(c.chat_id))),
                              types.InlineKeyboardButton(text="Elektr Zarba", callback_data=str('weaponspecial'
                                                                                                 + str(c.chat_id))))

        keyboard1.add(types.InlineKeyboardButton(text='Bekor qilish', callback_data=str('opcancel')))
        bot.send_message(p.chat_id, 'Raqibni tanlang.', reply_markup=keyboard1)

    def hit(self,user):
        n = 0
        d = 0
        dmax = self.dice
        print(user.name + " otayabdi " + str(self.name) + 'dan. Uning energiyasi - ' + str(
            user.energy) + '. Uning aniqligi va qurolning bonus aniqligi - ' + ' '
              + str(user.accuracy) + ' ' + str(self.bonus) +
              '. Tegish ehtimolligi - ' + str(11 - user.energy - self.bonus - user.accuracy - user.tempaccuracy) + "+!")
        while d != dmax:
            x = random.randint(1, 10)
            print(user.name + ' Tushib qoldi ' + str(x))
            if x > 10 - user.energy - self.bonus - user.accuracy - user.tempaccuracy + user.target.evasion:
                n += 1
            d += 1


            # бонусный урон персонажа
        # уходит энергия
        user.energy -= self.energy
        if n!=0:
            n += user.bonusdamage + self.damage - 1

        for a in user.abilities:
            n = a.onhit(a,n, user)
        else:
            pass
        n += user.truedamage
        # энергия загоняется в 0
        if user.energy < 0: user.energy = 0
        utils.damage(user, user.target, n, 'melee')
        return n

    def special(self, user, call):
        user.target = utils.actor_from_id(call, user.game)

    def special_second(self, user):
        if user.turn == 'weaponspecial':
            damagetaken = 0
            combo = 0
            while user.energy > 0 and combo < 3:
                damagetaken += self.hit(user)
                combo += 1
            if damagetaken != 0:
                d = str(
                    u'\U0001F91C' + "|" + user.name + ' Elektr Shokerdan ' + str(combo) + ' wolt to`k orqali '
                    + user.target.name + "ga zarb berayabdi! Yetkazildi " + str(damagetaken) + ' zarb.')
            else:
                d = str(
                    u'\U0001F4A8' + "|" + user.name + ' bitta ham zarb bera olmadi ' + user.target.name + "ga!")
            for a in user.abilities:
                d = a.onhitdesc(a, d, user)
            user.fight.string.add(d)

######################################################################################################

class Masters(Weapon):

    def get_action(self, p, call):
        keyboard1 = types.InlineKeyboardMarkup()
        enemyteam = p.targets
        p.turn = call.data
        for c in enemyteam:
            if p.energy < 3:
                keyboard1.add(types.InlineKeyboardButton(text=c.name, callback_data=str('op' + str(c.chat_id))))
            else:
                keyboard1.add(types.InlineKeyboardButton(text=c.name, callback_data=str('op' + str(c.chat_id))),
                              types.InlineKeyboardButton(text="Kombo", callback_data=str('weaponspecial'
                                                                                                 + str(c.chat_id))))

        keyboard1.add(types.InlineKeyboardButton(text='Bekor qilish', callback_data=str('opcancel')))
        bot.send_message(p.chat_id, 'Raqibni tanlang.', reply_markup=keyboard1)

    def hit(self,user):
        n = 0
        d = 0
        dmax = self.dice
        print(user.name + " otayabdi " + str(self.name) + 'dan. Uning energiyasi - ' + str(
            user.energy) + '. Uning aniqligi va qurolning bonus aniqligi - ' + ' '
              + str(user.accuracy) + ' ' + str(self.bonus) +
              '. Tegish ehtimolligi - ' + str(11 - user.energy - self.bonus - user.accuracy - user.tempaccuracy) + "+!")
        while d != dmax:
            x = random.randint(1, 100)
            print(user.name + ' Tushib qoldi ' + str(x))
            if x > 10 - user.energy - self.bonus - user.accuracy - user.tempaccuracy + user.target.evasion:
                n += 1
            d += 1


            # бонусный урон персонажа
        # уходит энергия
        user.energy -= self.energy
        if n!=0:
            n += user.bonusdamage + self.damage - 1

        for a in user.abilities:
            n = a.onhit(a,n, user)
        else:
            pass
        n += user.truedamage
        # энергия загоняется в 0
        if user.energy < 0: user.energy = 0
        utils.damage(user, user.target, n, 'melee')
        return n

    def special(self, user, call):
        user.target = utils.actor_from_id(call, user.game)

    def special_second(self, user):
        if user.turn == 'weaponspecial':
            damagetaken = 0
            combo = 0
            while user.energy > 0 and combo < 4:
                damagetaken += self.hit(user)
                combo += 1
            if damagetaken != 0:
                d = str(
                    u'\U0001F91C' + "|" + user.name + ' mushtlar bilan ' + str(combo) + ' ta kombinatsiyada🀄️ '
                    + user.target.name + "ga zarb berayabdi! Yetkazildi " + str(damagetaken) + ' zarb.')
            else:
                d = str(
                    u'\U0001F4A8' + "|" + user.name + ' bitta ham zarb bera olmadi ' + user.target.name + "ga!")
            for a in user.abilities:
                d = a.onhitdesc(a, d, user)
            user.fight.string.add(d)

###################################################################################
class Katana(Weapon):
    def __init__(self, dice, damage, energy, bonus, fixed, Melee, TwoHanded, Concealable, name, damagestring, chance,
                 standart=True, natural=False):
        Weapon.__init__(self, dice, damage, energy, bonus, fixed, Melee, TwoHanded, Concealable, name, damagestring,
                        standart=standart, natural=natural)
        self.chance = chance

    def hit(self,user):
        n = 0
        d = 0
        dmax = self.dice
        print(user.name + " otayabdi " + str(self.name) + '. Uning energiyasi - ' + str(
            user.energy) + '. Uning aniqligi va qurolning bonus aniqligi - ' + ' '
              + str(user.accuracy) + ' ' + str(self.bonus) +
              '. Tegish ehtimolligi - ' + str(11 - user.energy - self.bonus - user.accuracy - user.tempaccuracy) + "+!")
        while d != dmax:
            x = random.randint(1, 10)
            print(user.name + ' Tushib qoldi ' + str(x))
            if x > 10 - user.energy - self.bonus - user.accuracy - user.tempaccuracy + user.target.evasion:
                n += 1
            d += 1
        if n != 0 and random.randint(1,10)< self.chance:
            user.target.bleedcounter += 1
            user.target.bloodloss = False
            user.Hitability = True

            # бонусный урон персонажа
        # уходит энергия
        user.energy -= self.energy
        if n!=0:
            n += user.bonusdamage + self.damage - 1

        for a in user.abilities:
            n = a.onhit(a, n, user)
        else:
            pass
        n += user.truedamage
        # энергия загоняется в 0

        if user.energy < 0: user.energy = 0

        print('bleed')
        utils.damage(user, user.target, n, 'melee')
        return n

    def get_action(self, p, call):
        keyboard1 = types.InlineKeyboardMarkup()
        enemyteam = p.targets
        p.turn = call.data
        for c in enemyteam:
            if c.hp > 1 or p.energy < 3:
                keyboard1.add(types.InlineKeyboardButton(text=c.name, callback_data=str('op' + str(c.chat_id))))
            else:
                keyboard1.add(types.InlineKeyboardButton(text=c.name, callback_data=str('op' + str(c.chat_id))),
                              types.InlineKeyboardButton(text="Qatl etish", callback_data=str('weaponspecial' + str(c.chat_id))))

        keyboard1.add(types.InlineKeyboardButton(text='Bekor qilish', callback_data=str('opcancel')))
        bot.send_message(p.chat_id, 'Raqibni tanlang.', reply_markup=keyboard1)

    def special(self, user, call):
        user.target = utils.actor_from_id(call, user.game)

    def special_second(self, user):
        if user.turn == 'weaponspecial':
            if user.target.hp == 1:
                user.tempaccuracy += 3
                damagetaken = self.hit(user)
                if damagetaken != 0:
                    user.target.hp = 0
                    d = str(
                        u'\U00003299' + u'\U0001F494' + "|" + user.name + ' ' + user.target.name
                        + "ga qattiq zarba berayabdi va qo`rqinchli jarohatni qoldirayabdi! Yetkazildi " + str(damagetaken) + ' zarba. ' + user.target.name +
                        ' jonini yo`qotayabdi!')
                else:
                    d = str(
                        u'\U0001F4A8' + "|" + user.name
                        + ' shiddat bilan Katanani silkitayabdi, ammo tekkiza olmayabdi ' + user.target.name + "!")
                for a in user.abilities:
                    d = a.onhitdesc(a, d, user)
                user.fight.string.add(d)
                user.energy -= 3

    def getDesc(self, damagetaken, user):
        if damagetaken != 0:
            if not self.Melee:
                d = str(
                    u'\U0001F4A5' + "|" + getattr(self, str('desc' + str(random.randint(1, 3)))) + " Yetkazildi " + str(
                        damagetaken) + ' zarba.')
            else:
                d = str(
                    u'\U0001F44A' + "|" + getattr(self, str('desc' + str(random.randint(1, 3)))) + " Yetkazildi " + str(
                        damagetaken) + ' zarba.')
            if user.target.bleedcounter == 1 and user.Hitability:
                d += u'\U00002763' + "|" + user.target.name + ' qon yo`qotayabdi!'
            elif user.target.bleedcounter > 1 and user.Hitability:
                d += u'\U00002763' + "|" 'Qon yo`qotish kuchaymoqda!'
            for a in user.abilities:
                d = a.onhitdesc(a, d, user)
            return d
        else:
            return str(u'\U0001F4A8' + "|" + getattr(self, str('desc' + str(random.randint(4, 6)))))

############################################################################################
class Bazuka(Weapon):
    def __init__(self, dice, damage, energy, bonus, fixed, Melee, TwoHanded, Concealable, name, damagestring, chance,
                 standart=True, natural=False):
        Weapon.__init__(self, dice, damage, energy, bonus, fixed, Melee, TwoHanded, Concealable, name, damagestring,
                        standart=standart, natural=natural)
        self.chance = chance

    def hit(self,user):
        n = 0
        d = 0
        dmax = self.dice
        print(user.name + " otayabdi " + str(self.name) + '. Uning energiyasi - ' + str(
            user.energy) + '. Uning aniqligi va qurolning bonus aniqligi - ' + ' '
              + str(user.accuracy) + ' ' + str(self.bonus) +
              '. Tegish ehtimolligi - ' + str(11 - user.energy - self.bonus - user.accuracy - user.tempaccuracy) + "+!")
        while d != dmax:
            x = random.randint(1, 10)
            print(user.name + ' Tushib qoldi ' + str(x))
            if x > 10 - user.energy - self.bonus - user.accuracy - user.tempaccuracy + user.target.evasion:
                n += 1
            d += 1
        if n != 0 and random.randint(1,10)< self.chance:
            user.target.bleedcounter += 1
            user.target.bloodloss = False
            user.Hitability = True

            # бонусный урон персонажа
        # уходит энергия
        user.energy -= self.energy
        if n!=0:
            n += user.bonusdamage + self.damage - 1

        for a in user.abilities:
            n = a.onhit(a, n, user)
        else:
            pass
        n += user.truedamage
        # энергия загоняется в 0

        if user.energy < 0: user.energy = 0

        print('bleed')
        utils.damage(user, user.target, n, 'melee')
        return n

    def get_action(self, p, call):
        keyboard1 = types.InlineKeyboardMarkup()
        enemyteam = p.targets
        p.turn = call.data
        for c in enemyteam:
            if c.hp > 1 or p.energy < 3:
                keyboard1.add(types.InlineKeyboardButton(text=c.name, callback_data=str('op' + str(c.chat_id))))
            else:
                keyboard1.add(types.InlineKeyboardButton(text=c.name, callback_data=str('op' + str(c.chat_id))),
                              types.InlineKeyboardButton(text="☢️ATOM BOMBA⛔️", callback_data=str('weaponspecial' + str(c.chat_id))))

        keyboard1.add(types.InlineKeyboardButton(text='Bekor qilish', callback_data=str('opcancel')))
        bot.send_message(p.chat_id, '𝗡𝗶𝘀𝗵𝗼𝗻𝗶𝗻𝗶 𝘁𝗮𝗻𝗹𝗮𝗻𝗴:', reply_markup=keyboard1)

    def special(self, user, call):
        user.target = utils.actor_from_id(call, user.game)

    def special_second(self, user):
        if user.turn == 'weaponspecial':
            if user.target.hp == 1:
                user.tempaccuracy += 3
                damagetaken = self.hit(user)
                if damagetaken != 0:
                    user.target.hp -= 10
                    d = str(
                        '☢️𝘿𝙄𝙌𝙌𝘼𝙏☢️' + '\n☣️𝕆`𝕋𝔸 𝕏𝔸𝕍𝔽𝕃𝕀☣️' + "\n👨‍✈️|" + user.name + ' 𝘼𝙏𝙊𝙈 𝘽𝙊𝙈𝘽𝘼𝙎𝙄 𝘂𝗰𝗵𝗶𝗿𝗶𝘀𝗵𝗴𝗮 𝗯𝘂𝘆𝘂𝗿𝘂𝗾 𝗯𝗲𝗿𝗱𝗶. \n☢️𝗕𝗢𝗠𝗕𝗔 𝗽𝗼𝗿𝘁𝗹𝗮𝘀𝗵𝗶 ' + user.target.name
                        + " 𝘁𝗮𝗻𝗮𝘀𝗶𝗻𝗶 𝗺𝗮𝘆𝗱𝗮 𝗺𝗮𝗹𝗲𝗸𝘂𝗹𝗮𝗹𝗮𝗿𝗴𝗮 𝗽𝗮𝗿𝗰𝗵𝗮𝗹𝗮𝗯 𝘆𝘂𝗯𝗼𝗿𝗱𝗶! \n📟𝗡𝘂𝗿𝗹𝗮𝗻𝗶𝘀𝗵 𝗱𝗮𝗿𝗮𝗷𝗮𝘀𝗶: " + str(damagetaken) + '. \n🎛' + user.target.name +
                        ' 𝟭𝟬𝘁𝗮 𝗷𝗼𝗻 𝘆𝗼`𝗾𝗼𝘁𝗱𝗶!')
                else:
                    d = str(
                        '❗️' + "|" + user.name
                        + ' 𝗔𝗧𝗢𝗠 𝗕𝗢𝗠𝗔𝗦𝗜𝗡𝗜 𝗨𝗖𝗛𝗜𝗥𝗠𝗢𝗤𝗖𝗛𝗜 𝗕𝗢`𝗟𝗬𝗔𝗕𝗗𝗜, 𝗔𝗠𝗠𝗢 ' + user.target.name + " 𝗕𝗢𝗠𝗕𝗔𝗡𝗜 𝗭𝗔𝗥𝗔𝗥𝗦𝗜𝗭𝗟𝗔𝗡𝗧𝗜𝗥𝗜𝗦𝗛𝗚𝗔 𝗨𝗟𝗚𝗨𝗥𝗚𝗔𝗡𝗗𝗜!")
                for a in user.abilities:
                    d = a.onhitdesc(a, d, user)
                user.fight.string.add(d)
                user.energy -= 5

    def getDesc(self, damagetaken, user):
        if damagetaken != 0:
            if not self.Melee:
                d = str(
                    '💥' + "|" + getattr(self, str('desc' + str(random.randint(1, 3)))) + " Yetkazildi " + str(
                        damagetaken) + ' zarba.')
            else:
                d = str(
                    '💥' + "|" + getattr(self, str('desc' + str(random.randint(1, 3)))) + " Yetkazildi " + str(
                        damagetaken) + ' zarba.')
            for a in user.abilities:
                d = a.onhitdesc(a, d, user)
            return d
        else:
            return str(u'\U0001F4A8' + "|" + getattr(self, str('desc' + str(random.randint(4, 6)))))

#####################################################################################################
class Knuckles(Weapon):

    def special_end(self, user):
        if user.turn == 'attack' + str(user.fight.round):
            if user.target.turn == 'reload' + str(user.fight.round) or 'dog_rest' + str(user.fight.round):
                user.target.energy -= 1
                user.fight.string.add(u'\U000026A1' + user.target.name + ' 1 energiya yo`qotmoqda.')

########################################################################################################

##############################КОД ПАСЮКА, ДЕЛАЕТСЯ################                    
class NekoGun(Weapon):
    def __init__(self, dice, damage, energy, bonus, fixed, Melee, TwoHanded, Concealable, name, damagestring, chance,
                 standart=True, natural=False):
        Weapon.__init__(self, dice, damage, energy, bonus, fixed, Melee, TwoHanded, Concealable, name, damagestring,
                        standart=standart, natural=natural)
        self.chance = chance

    def hit(self,user):
        n = 0
        d = 0
        dmax = self.dice
        print(user.name + " стреляет из " + str(self.name) + '. Его энергия - ' + str(
            user.energy) + '. Его точность и бонусная точность оружия - ' + ' '
              + str(user.accuracy) + ' ' + str(self.bonus) +
              '. Шанс попасть - ' + str(11 - user.energy - self.bonus - user.accuracy - user.tempaccuracy) + "+!")
        while d != dmax:
            x = random.randint(1, 10)
            print(user.name + ' Выпало ' + str(x))
            if x > 10 - user.energy - self.bonus - user.accuracy - user.tempaccuracy + user.target.evasion:
                n += 1
            d += 1

            # бонусный урон персонажа
        # уходит энергия
        user.energy -= self.energy
        if n!=0:
            n += user.bonusdamage + self.damage - 1

        for a in user.abilities:
            n = a.onhit(a, n, user)
        else:
            pass
        n += user.truedamage
        # энергия загоняется в 0

        if user.energy < 0: user.energy = 0

        print('bleed')
        utils.damage(user, user.target, n, 'ranged')
        return n

    
    def aquare(self,user):
        user.nekocd = 0
    
    
    def get_action(self, p, call):
        keyboard1 = types.InlineKeyboardMarkup()
        enemyteam = p.targets
        p.turn = call.data
        for c in enemyteam:
            if p.energy < 1 or p.nekocd>0:
                keyboard1.add(types.InlineKeyboardButton(text=c.name, callback_data=str('op' + str(c.chat_id))))
            else:
                keyboard1.add(types.InlineKeyboardButton(text=c.name, callback_data=str('op' + str(c.chat_id))),
                              types.InlineKeyboardButton(text="NekoSHOT", callback_data=str('weaponspecial' + str(c.chat_id))))

        keyboard1.add(types.InlineKeyboardButton(text='Bekor qilish', callback_data=str('opcancel')))
        bot.send_message(p.chat_id, 'Raqibni tanlang.', reply_markup=keyboard1)

    def special(self, user, call):
        user.target = utils.actor_from_id(call, user.game)

    def special_second(self, user):
        if user.turn == 'weaponspecial':
                damagetaken = self.hit(user)
                if damagetaken != 0:
                    xx=random.randint(1,4)
                    if xx==1:
                        bleed=1
                        effect='💊ℚ𝕠𝕟 𝕪𝕠`𝕢𝕠𝕥𝕚𝕤𝕙(𝟛𝕩)'
                        user.target.bleedcounter=3
                    if xx==2:
                        stun=2
                        effect='🌀𝕂𝕒𝕣𝕒𝕩𝕥𝕝𝕒𝕤𝕙(𝟙𝕩)'
                        user.target.stuncounter=2
                    if xx==3:
                        Hit=3
                        effect='🔋ℍ𝕠𝕝𝕤𝕚𝕫𝕝𝕒𝕟𝕚𝕤𝕙(-𝟝)'
                        user.target.energy -= 5    
                    if xx==4:
                        fire=4
                        effect='🔥𝕐𝕠𝕟𝕚𝕤𝕙(𝟚𝕩)'
                        user.target.firecounter += 2
                        user.target.offfire = user.fight.round + 2
                        user.Hitability = True
                    d = str(
                        '🎴' + "|" + user.name + ' 𝗡𝗲𝗸𝗼-𝗸𝘂𝗰𝗵𝗻𝗶 𝗰𝗵𝗮𝗾𝗶𝗿𝗮𝘆𝗮𝗯𝗱𝗶! \n' + user.target.name
                        + " 𝗼𝗹𝗴𝗮𝗻 𝗲𝗳𝗳𝗲𝗸𝘁𝗶: " + effect +'! \n𝗬𝗲𝘁𝗸𝗮𝘇𝗶𝗹𝗱𝗶 ' + str(damagetaken) + ' 𝘇𝗮𝗿𝗯𝗮.')
                else:
                    d = str(
                        u'\U0001F4A8' + "|" + user.name
                        + ' 𝗡𝗲𝗸𝗼-𝗸𝘂𝗰𝗵𝗻𝗶 𝗰𝗵𝗮𝗾𝗶𝗿𝗮𝘆𝗮𝗯𝗱𝗶, 𝗮𝗺𝗺𝗼 ' + user.target.name + " 𝘂𝗻𝗴𝗮 𝗾𝗮𝗿𝘀𝗵𝗶𝗹𝗶𝗸 𝗸𝗼'𝗿𝘀𝗮𝘁𝗮𝘆𝗮𝗯𝗱𝗶.")
                for a in user.abilities:
                    d = a.onhitdesc(a, d, user)
                user.fight.string.add(d)
                user.energy -= 0

    def getDesc(self, damagetaken, user):
        if damagetaken != 0:
            if not self.Melee:
                d = str(
                    u'\U0001F4A5' + "|" + getattr(self, str('desc' + str(random.randint(1, 3)))) + " Yetkazildi " + str(
                        damagetaken) + ' zarba.')
            else:
                d = str(
                    u'\U0001F44A' + "|" + getattr(self, str('desc' + str(random.randint(1, 3)))) + " Yetkazild " + str(
                        damagetaken) + ' zarba.')
            if user.target.firecounter == 2 and user.Hitability:
                d += u'\U0001F525' + "|" + user.target.name + ' kuyayabdi!'
            elif user.target.firecounter > 3 and user.Hitability:
                d += u'\U0001F525' + "|" 'Olov kuchaymoqda!'                
            for a in user.abilities:
                d = a.onhitdesc(a, d, user)
            return d
        else:
            return str(u'\U0001F4A8' + "|" + getattr(self, str('desc' + str(random.randint(4, 6)))))         
                    
##############################КОНЕЦ КОДА ПАСЮКА################        
        

##############################aaaaaaaaaaaaaaaaa################                    
class Thanos(Weapon):
    def __init__(self, dice, damage, energy, bonus, fixed, Melee, TwoHanded, Concealable, name, damagestring, chance,
                 standart=True, natural=False):
        Weapon.__init__(self, dice, damage, energy, bonus, fixed, Melee, TwoHanded, Concealable, name, damagestring,
                        standart=standart, natural=natural)
        self.chance = chance

  
    def hit(self,user):
        n = 0
        d = 0
        dmax = self.dice
        print(user.name + " otayabdi " + str(self.name) + '. Uning energiyasi - ' + str(
            user.energy) + '. Uning aniqligi va qurolning bonus aniqligi - ' + ' '
              + str(user.accuracy) + ' ' + str(self.bonus) +
              '. Tegish ehtimolligi - ' + str(11 - user.energy - self.bonus - user.accuracy - user.tempaccuracy) + "+!")
        while d != dmax:
            x = random.randint(1, 100)
            print(user.name + ' Tushib qoldi ' + str(x))
            if x > 10 - user.energy - self.bonus - user.accuracy - user.tempaccuracy + user.target.evasion:
                n += 1
            d += 1
        if n != 0 and random.randint(1,2)< self.chance:
            user.target.firecounter += 1
            user.target.offfire = user.fight.round + 2
            user.Hitability = True
        if n != 0 and random.randint(1,2)< self.chance:
            user.target.bleedcounter += 1
            user.target.bloodloss = False
            user.Hitability = True

            # бонусный урон персонажа
        # уходит энергия
        user.energy -= self.energy
        if n!=0:
            n += user.bonusdamage + self.damage - 1

        for a in user.abilities:
            n = a.onhit(a, n, user)
        else:
            pass
        n += user.truedamage
        # энергия загоняется в 0

        if user.energy < 0: user.energy = 0
        utils.damage(user, user.target, n, 'melee')
        print('bleed')
        return n

    def effect(self, user):
        if random.randint(1, 2) <= self.chance:
            if user.target.toughness > 2:
                user.target.toughness -= 1
            if user.target.toughness > 2:
                user.fight.string.add('💎𝗞𝘂𝗰𝗵 𝗧𝗼𝘀𝗵𝗶 ' + '|' + user.target.name + 'ni himoyasini🛡 susaytirmoqda!')
            else:
                user.fight.string.add('💎𝗞𝘂𝗰𝗵 𝗧𝗼𝘀𝗵𝗶 ta`sirida ' + '|' + user.target.name + ' himoyasini⚙️ to`liq yo`qotdi.')
        user.weaponeffect.remove(self)

    def getDesc(self, damagetaken,user):
        if damagetaken != 0:
            user.weaponeffect.append(self)
            if not self.Melee:
                d = str('⚔️' + "|" + getattr(self,str('desc' + str(random.randint(1, 3)))) + " Yetkazildi " + str(damagetaken) + ' zarba.')
            else:
                d = str('⚔️' + "|" + getattr(self,str('desc' + str(random.randint(1, 3)))) + " Yetkazildi " + str(damagetaken) + ' zarba.')
            if user.target.firecounter == 1 and user.Hitability:
                d += '\n🦠𝗛𝗮𝗾𝗶𝗾𝗮𝘁 𝗧𝗼𝘀𝗵𝗶 kuchi ta`sirida ' + "|" + user.target.name + ' yonayabdi💥!'
            elif user.target.firecounter > 1 and user.Hitability:
                d += '\n🦠𝗛𝗮𝗾𝗶𝗾𝗮𝘁 𝗧𝗼𝘀𝗵𝗶 ' + "|" ' kuchliroq nur☄️ sochmoqda!'
            for a in user.abilities:
                d = a.onhitdesc(a,d,user)
            if user.target.bleedcounter == 1 and user.Hitability:
                d += '\n🏮𝗤𝗮𝗹𝗯 𝗧𝗼𝘀𝗵𝗶 ' + "|" + user.target.name + 'ni qon yo`qotishga❣️ majbur qilyabdi!'
            elif user.target.bleedcounter > 1 and user.Hitability:
                d += '\n🏮𝗤𝗮𝗹𝗯 𝗧𝗼𝘀𝗵𝗶 ' + "|" ' kuchi ortmoqda㊗️!'
            for a in user.abilities:
                d = a.onhitdesc(a, d, user)
            return d
        else:
            return str(u'\U0001F4A8' + "|" + getattr(self, str('desc' + str(random.randint(4, 6)))))
           
    def special_end(self, user):
        if user.turn == 'attack' + str(user.fight.round):
            if user.target.turn == 'reload' + str(user.fight.round) or 'dog_rest' + str(user.fight.round):
                user.target.energy -= 1
                user.fight.string.add('🧿𝗔𝗾𝗹 𝗧𝗼𝘀𝗵𝗶 tasirida ' + user.target.name + ' kuchini🍃 yo`qotmoqda.')


##############################КОНЕЦ КОДА ПАСЮКА################        

class Club(Weapon):

    def hit(self,user):
        n = 0
        d = 0
        dmax = self.dice
        while d != dmax:
            x = random.randint(1, 10)
            print(user.name + ' Tushib qoldi ' + str(x))
            if x > 10 - user.energy - self.bonus - user.accuracy - user.tempaccuracy + user.target.evasion:
                n += 1
            d += 1

        # уходит энергия
        user.energy -= self.energy
        if n!=0:
            n += user.bonusdamage + self.damage + user.combo_counter - 1

        for a in user.abilities:
            n = a.onhit(a, n, user)
        else:
            pass
        n += user.truedamage
        # энергия загоняется в 0
        if user.energy < 0: user.energy = 0
        utils.damage(user, user.target, n, 'melee')
        return n

    def aquare(self ,user):
        user.combo_counter = 0

    def lose(self, user):
        del user.combo_counter

    def special_end(self, user):
        if user.turn == 'attack' + str(user.fight.round):
            user.combo_counter += 1
        else:
            user.combo_counter = 0


class ULTRA(Weapon):
    def __init__(self, dice, damage, energy, bonus, fixed, Melee, TwoHanded, Concealable, name, damagestring, double,
                 standart=True):
        Weapon.__init__(self, dice, damage, energy, bonus, fixed, Melee, TwoHanded, Concealable, name, damagestring,standart=standart)
        self.double=double
            
    def aquare(self,user):
        user.longreload = 0
        user.DisabledReload = False
        
    def special_second(self, user):
        if user.turn == 'reload' + str(user.fight.round):
            user.DisabledReload = True
            user.Disabled = True
            user.longreload = user.fight.round + 1
        if user.fight.round == user.longreload:
            user.Disabled = False
            user.DisabledReload = False
            

class BowBleeding(Weapon):
    def __init__(self, dice, damage, energy, bonus, fixed, Melee, TwoHanded, Concealable, name, damagestring, chance,
                 standart=True,natural=False):
        Weapon.__init__(self, dice, damage, energy, bonus, fixed, Melee, TwoHanded, Concealable, name, damagestring,standart=standart,natural=natural)
        self.chance = chance

    def getDesc(self, damagetaken,user):
        user.weaponeffect.append(self)
        if damagetaken != 0:
            if not self.Melee:

                d =  str(u'\U0001F4A5' + "|" + getattr(self,str('desc' + str(random.randint(1, 3)))) + " Yetkazildi " + str(damagetaken) + ' zarba.')
            else:
                d =  str(u'\U0001F44A' + "|" + getattr(self,str('desc' + str(random.randint(1, 3)))) + " Yetkazildi " + str(damagetaken) + ' zarba.')
            if user.target.bleedcounter == 1 and user.Hitability:
                d += u'\U00002763' + "|" + user.target.name + ' qon yo`qotayabdi!'
            elif user.target.bleedcounter > 1 and user.Hitability:
                d += u'\U00002763' + "|" 'Qon yo`qotishi kuchaymoqda!'
            return d
        else:
            return str(u'\U0001F4A8' + "|" + getattr(self,str('desc' + str(random.randint(4, 6)))))


    def hit(self,user):
        n = 0
        d = 0
        dmax = self.dice
        print(user.name + " otayabdi " + str(self.name) + 'dan. Uning energiyasi - ' + str(
            user.energy) + '. Uning aniqligi va qurolning bonus aniqligi - ' + ' '
              + str(user.accuracy) + ' ' + str(user.bonusaccuracy) + ' ' + str(self.bonus) +
              '. Шанс попасть - ' + str(11 - user.energy - self.bonus - user.accuracy - user.bonusaccuracy - user.tempaccuracy) + "+!")
        while d != dmax:
            x = random.randint(1, 10)
            print(user.name + ' Tushib qoldi ' + str(x))
            if x > 10 - user.energy - self.bonus - user.accuracy - user.bonusaccuracy - user.tempaccuracy + user.target.evasion:
                n += 1
            d += 1

        # бонусный урон персонажа
        if n != 0:
            n += user.bonusdamage + self.damage - 1
            if user.bonusaccuracy > 0:
                n += user.bonusaccuracy*2
        if n != 0 and random.randint(1, 10) < self.chance + user.bonusaccuracy:
            user.target.bleedcounter += 1
            user.target.bloodloss = False
            user.Hitability = True
        # уходит энергия
        user.energy -= self.energy + user.bonusaccuracy
        # применяется урон
        user.target.damagetaken += n + user.truedamage
        # энергия загоняется в 0
        if user.energy < 0: user.energy = 0
        return n

    def aquare(self,user):
        user.bonusaccuracy = 0

    def lose(self,user):
        user.bonusaccuracy = 0
        user.Armed = False

    def get_action(self, p, call):
        keyboard1 = types.InlineKeyboardMarkup()
        p.turn = call.data
        for c in p.targets:
                keyboard1.add(types.InlineKeyboardButton(text=c.name, callback_data=str('op' + str(c.chat_id))))
        if p.energy - p.bonusaccuracy > 1 and p.bonusaccuracy < 3:
            keyboard1.add(types.InlineKeyboardButton(text="Cho`zish", callback_data=str('draw')))
        keyboard1.add(types.InlineKeyboardButton(text='Bekor qilish', callback_data=str('opcancel')))
        bot.send_message(p.chat_id, 'Raqibni tanlash.', reply_markup=keyboard1)

    def special(self, user, call):
        user.bonusaccuracy += 1
        user.Armed = True
        print ('scheck')

    def effect(self, user):
        x = random.randint(1, 10)
        if user.Hit:
            print('Karaxtlash ' + str(x) + ' < '+ str(user.bonusaccuracy-1)*6)
            if random.randint(1, 10) < (user.bonusaccuracy-1)*6:
                if user.target.stuncounter < 1:
                    user.target.stuncounter = 1
                user.fight.string.add(u'\U0001F300' + '|' + user.target.name + ' karaxtlandi!')
        user.weaponeffect.remove(self)

        user.bonusaccuracy = 0
        user.Armed = False


katana = Katana(5, 1, 2, 2, 0, True, False, False, 'Katana','1-3' + u'\U0001F525' + "|" + '2' + u'\U000026A1', 3, standart=False)
katana.desc1 = 'O`yinchi Raqibini Katana bilan urayabdi!'
katana.desc2 = 'O`yinchi Raqibini Katana bilan urayabdi!'
katana.desc3 = 'O`yinchi Raqibini Katana bilan urayabdi!'
katana.desc4 = 'O`yinchi Raqibini Katana bilan urayabdi, lekin tekkiza olmayabdi.'
katana.desc5 = 'O`yinchi Raqibini Katana bilan urayabdi, lekin tekkiza olmayabdi.'
katana.desc6 = 'O`yinchi Raqibini Katana bilan urayabdi, lekin tekkiza olmayabdi.'
bazuka = Bazuka(6, 3, 4, -2, 0, False, True, True, '☢️Bazooka','1-3' + u'\U0001F525' + "|" + '2' + u'\U000026A1', 3, standart=False)
bazuka.desc1 = 'O`yinchi ☢️𝗕𝗮𝘇𝗼𝗼𝗸𝗮𝗱𝗮𝗻 Raketa🚀 otib Raqibni portlatayabdi!'
bazuka.desc2 = 'O`yinchi ☢️𝗕𝗮𝘇𝗼𝗼𝗸𝗮𝗱𝗮𝗻 Raketa🚀 otib Raqibni portlatayabdi!'
bazuka.desc3 = 'O`yinchi ☢️𝗕𝗮𝘇𝗼𝗼𝗸𝗮𝗱𝗮𝗻 Raketa🚀 otib Raqibni portlatayabdi!'
bazuka.desc4 = 'O`yinchi Raqibiga ☢️𝗕𝗮𝘇𝗼𝗼𝗸𝗮𝗱𝗮𝗻 otayabdi, lekin tekkiza olmayabdi.'
bazuka.desc5 = 'O`yinchi Raqibini ☢️𝗕𝗮𝘇𝗼𝗼𝗸𝗮𝗱𝗮𝗻 otayabdi, lekin tekkiza olmayabdi.'
bazuka.desc6 = 'O`yinchi Raqibini ☢️𝗕𝗮𝘇𝗼𝗼𝗸𝗮𝗱𝗮𝗻 otayabdi, lekin tekkiza olmayabdi.'

nekogun = NekoGun(3, 2, 2, 3, 1, True, False, False, 'NekoGUN💠','1-3' + u'\U0001F525' + "|" + '2' + u'\U000026A1', 3, standart=False)
nekogun.desc1 = 'O`yinchi ℕ𝕖𝕜𝕠𝔾𝕦𝕟💠 bilan Raqibni qo`lini kesayabdi!'
nekogun.desc2 = 'O`yinchi ℕ𝕖𝕜𝕠𝔾𝕦𝕟💠 bilan Raqibni oyog`ini kesayabdi!'
nekogun.desc3 = 'O`yinchi ℕ𝕖𝕜𝕠𝔾𝕦𝕟💠 bilan Raqibni bo`ynini kesayabdi!'
nekogun.desc4 = 'O`yinchi Raqibini ℕ𝕖𝕜𝕠𝔾𝕦𝕟💠 bilan urayabdi, lekin tekkiza olmayabdi.'
nekogun.desc5 = 'O`yinchi Raqibini ℕ𝕖𝕜𝕠𝔾𝕦𝕟💠 bilan urayabdi, lekin tekkiza olmayabdi.'
nekogun.desc6 = 'O`yinchi Raqibini ℕ𝕖𝕜𝕠𝔾𝕦𝕟💠 bilan urayabdi, lekin tekkiza olmayabdi.'

thanos = Thanos(0, 1, 2, 2, 0, True, False, False, 'Cheksizlik','1-3' + u'\U0001F525' + "|" + '2' + u'\U000026A1', 3, standart=False)
thanos.desc1 = 'O`yinchi 𝗜𝗸𝗸𝗶 𝗤𝗶𝗿𝗿𝗮𝗹𝗶 𝗤𝗶𝗹𝗶𝗰𝗵 bilan Raqibini boshiga urayabdi!'
thanos.desc2 = 'O`yinchi 𝗜𝗸𝗸𝗶 𝗤𝗶𝗿𝗿𝗮𝗹𝗶 𝗤𝗶𝗹𝗶𝗰𝗵 bilan Raqibini tanasiga urayabdi!'
thanos.desc3 = 'O`yinchi 𝗜𝗸𝗸𝗶 𝗤𝗶𝗿𝗿𝗮𝗹𝗶 𝗤𝗶𝗹𝗶𝗰𝗵 bilan Raqibini oyog`iga urayabdi!'
thanos.desc4 = 'O`yinchi 𝗜𝗸𝗸𝗶 𝗤𝗶𝗿𝗿𝗮𝗹𝗶 𝗤𝗶𝗹𝗶𝗰𝗵 bilan Raqibini qo`liga urayabdi, lekin tekkiza olmayabdi.'
thanos.desc5 = 'O`yinchi 𝗜𝗸𝗸𝗶 𝗤𝗶𝗿𝗿𝗮𝗹𝗶 𝗤𝗶𝗹𝗶𝗰𝗵 bilan Raqibini bo`yniga urayabdi, lekin tekkiza olmayabdi.'
thanos.desc6 = 'O`yinchi 𝗜𝗸𝗸𝗶 𝗤𝗶𝗿𝗿𝗮𝗹𝗶 𝗤𝗶𝗹𝗶𝗰𝗵 bilan Raqibini qorniga urayabdi, lekin tekkiza olmayabdi.'

knuckles = Knuckles(4, 1, 2, 3, 0, True, False, False, "Kastet",'1-2' + u'\U0001F525' + "|" + '2' + u'\U000026A1', natural=True)
knuckles.desc1 = 'O`yinchi Raqibini Kastet bilan urayabdi!'
knuckles.desc2 = 'O`yinchi Raqibini Kastet bilan urayabdi!'
knuckles.desc3 = 'O`yinchi Raqibini Kastet bilan urayabdi!'
knuckles.desc4 = 'O`yinchi Raqibini Kastet bilan urayabdi, lekin tekkiza olmayabdi.'
knuckles.desc5 = 'O`yinchi Raqibini Kastet bilan urayabdi, lekin tekkiza olmayabdi.'
knuckles.desc6 = 'O`yinchi Raqibini Kastet bilan urayabdi, lekin tekkiza olmayabdi.'

club = Club(5, 1, 2, 3, 0, True, False, False, "Excalibur",'1-3' + u'\U0001F525' + "|" + '2' + u'\U000026A1', standart=False)
club.desc1 = 'O`yinchi Raqibini Excalibur bilan urayabdi!'
club.desc2 = 'O`yinchi Raqibini Excalibur bilan urayabdi!'
club.desc3 = 'O`yinchi Raqibini Excalibur bilan urayabdi!'
club.desc4 = 'O`yinchi Raqibini Excalibur bilan urayabdi, lekin tekkiza olmayabdi.'
club.desc5 = 'O`yinchi Raqibini Excalibur bilan urayabdi, lekin tekkiza olmayabdi.'
club.desc6 = 'O`yinchi Raqibini Excalibur bilan urayabdi, lekin tekkiza olmayabdi.'

ultra=ULTRA(3,1,2,2,0,True,False,True,'Pichoq','500' , True, standart=False)
ultra.desc1 = 'O`yinchi Raqibini Pichoq bilan urayabdi!'
ultra.desc2 = 'O`yinchi Raqibini Pichoq bilan urayabdi!'
ultra.desc3 = 'O`yinchi Raqibini Pichoq bilan urayabdi!'
ultra.desc4 = 'O`yinchi Raqibini Pichoq bilan urayabdi, lekin tekkiza olmayabdi.'
ultra.desc5 = 'O`yinchi Raqibini Pichoq bilan urayabdi, lekin tekkiza olmayabdi.'
ultra.desc6 = 'O`yinchi Raqibini Pichoq bilan urayabdi, lekin tekkiza olmayabdi.'
tazer = Tazer(3, 1, 2, 2, 0, True, False, True, 'Militsiya Dubinkasi', '1-3' + u'\U0001F44A' + "|" + '2' + u'\U000026A1')
sniper = Sniper(1, 1, 5, -4, 8, False, False, False, 'Snayper Vintovka','8' + u'\U0001F4A5' + "|" + '5' + u'\U000026A1')
flamethrower = Flamethrower(2, 1, 3, 2, 1, False, False, False, 'Ognemet','1' + u'\U0001F525' + "|" + '3' + u'\U000026A1')
kalashnikov = Kalashnikov(2, 1, 3, 2, 2, False, False, False, 'Kalashnikov','1' + u'\U0001F525' + "|" + '3' + u'\U000026A1', standart=False)
drago = Drago(18, 15, 0, 10, 0, False, False, False, 'Drago','1' + '👹' + "|" + '3' + '👹', standart=False, natural=True)
vintovka = Vintovka(3, 1, 3, 2, 2, False, False, False, 'Vintovka', '1-3' + u'\U0001F44A' + "|" + '2' +  u'\U000026A1', 3, standart=False)
knife = Bleeding(3, 1, 2, 2, 0, True, False, False, 'Pichoq','1-3' + u'\U0001F525' + "|" + '2' + u'\U000026A1',6)
knife.desc1 = 'O`yinchi Raqibini Pichoq bilan urayabdi!'
knife.desc2 = 'O`yinchi Raqibini Pichoq bilan urayabdi!'
knife.desc3 = 'O`yinchi Raqibini Pichoq bilan urayabdi!'
knife.desc4 = 'O`yinchi Raqibini Pichoq bilan urayabdi, lekin tekkiza olmayabdi.'
knife.desc5 = 'O`yinchi Raqibini Pichoq bilan urayabdi, lekin tekkiza olmayabdi.'
knife.desc6 = 'O`yinchi Raqibini Pichoq bilan urayabdi, lekin tekkiza olmayabdi.'
knifee = Bleeding(3, 1, 2, 2, 0, True, False, False, 'Lazerli Pushka','1-3' + u'\U0001F525' + "|" + '2' + u'\U000026A1',6, standart=False)
knifee.desc1 = 'O`yinchi Raqibga Lazerli Pushkadan otayabdi!'
knifee.desc2 = 'O`yinchi Raqibga Lazerli Pushkadan otayabdi!'
knifee.desc3 = 'O`yinchi Raqibga Lazerli Pushkadan otayabdi!'
knifee.desc4 = 'O`yinchi Raqibga Lazerli Pushkadan otayabdi, lekin tekkiza olmayabdi.'
knifee.desc5 = 'O`yinchi Raqibga Lazerli Pushkadan otayabdi, lekin tekkiza olmayabdi.'
knifee.desc6 = 'O`yinchi Raqibga Lazerli Pushkadan otayabdi, lekin tekkiza olmayabdi.'
tourch = Burning(2, 1, 2, 3, 0, True, False, False, 'Fakel','1-2' + u'\U0001F525' + "|" + '2' + u'\U000026A1', 8)
tourch.desc1 = 'O`yinchi Raqibini Fakel bilan urayabdi!'
tourch.desc2 = 'O`yinchi Raqibini Fakel bilan urayabdi!'
tourch.desc3 = 'O`yinchi Raqibini Fakel bilan urayabdi!'
tourch.desc4 = 'O`yinchi Raqibini Fakel bilan urayabdi, lekin tekkiza olmayabdi.'
tourch.desc5 = 'O`yinchi Raqibini Fakel bilan urayabdi, lekin tekkiza olmayabdi.'
tourch.desc6 = 'O`yinchi Raqibini Fakel bilan urayabdi, lekin tekkiza olmayabdi.'
olovlis = Olovlis(1, 1, 2, 10, 0, True, False, True, 'Olovli Kristal☀️','1' + u'\U0001F525' + "|" + '2' + u'\U000026A1', 8, standart=False)
olovlis.desc1 = 'O`yinchi Raqibini 𝕆𝕝𝕠𝕧𝕝𝕚 𝕂𝕣𝕚𝕤𝕥𝕒𝕝☀️ bilan sexrlayabdi!'
olovlis.desc2 = 'O`yinchi Raqibini 𝕆𝕝𝕠𝕧𝕝𝕚 𝕂𝕣𝕚𝕤𝕥𝕒𝕝☀️ bilan sexrlayabdi!'
olovlis.desc3 = 'O`yinchi Raqibini 𝕆𝕝𝕠𝕧𝕝𝕚 𝕂𝕣𝕚𝕤𝕥𝕒𝕝☀️ bilan sexrlayabdi!'
olovlis.desc4 = 'O`yinchi Raqibini 𝕆𝕝𝕠𝕧𝕝𝕚 𝕂𝕣𝕚𝕤𝕥𝕒𝕝☀️ bilan urayabdi, lekin tekkiza sexrlayabdi.'
olovlis.desc5 = 'O`yinchi Raqibini 𝕆𝕝𝕠𝕧𝕝𝕚 𝕂𝕣𝕚𝕤𝕥𝕒𝕝☀️ bilan urayabdi, lekin tekkiza sexrlayabdi.'
olovlis.desc6 = 'O`yinchi Raqibini 𝕆𝕝𝕠𝕧𝕝𝕚 𝕂𝕣𝕚𝕤𝕥𝕒𝕝☀️ bilan urayabdi, lekin tekkiza sexrlayabdi.'
hatchet = Crippling(3, 1, 2, 2, 0, True, False, False, 'Bolta','1-3' + u'\U0001F525' + "|" + '2' + u'\U000026A1', 8)
hatchet.desc1 = 'O`yinchi Raqibini Bolta bilan urayabdi!'
hatchet.desc2 = 'O`yinchi Raqibini Bolta bilan urayabdi!'
hatchet.desc3 = 'O`yinchi Raqibini Bolta bilan urayabdi!'
hatchet.desc4 = 'O`yinchi Raqibini Bolta bilan urayabdi, lekin tekkiza olmayabdi.'
hatchet.desc5 = 'O`yinchi Raqibini Bolta bilan urayabdi, lekin tekkiza olmayabdi.'
hatchet.desc6 = 'O`yinchi Raqibini Bolta bilan urayabdi, lekin tekkiza olmayabdi.'
chain = Dropping(3, 1, 2, 2, 0, True, False, False, 'Zanjir','1-3' + u'\U0001F525' + "|" + '2' + u'\U000026A1', 4)
chain.desc1 = 'O`yinchi Raqibini Zanjir bilan urayabdi!'
chain.desc2 = 'O`yinchi Raqibini Zanjir bilan urayabdi!'
chain.desc3 = 'O`yinchi Raqibini Zanjir bilan urayabdi!'
chain.desc4 = 'O`yinchi Raqibini Zanjir bilan urayabdi, lekin tekkiza olmayabdi.'
chain.desc5 = 'O`yinchi Raqibini Zanjir bilan urayabdi, lekin tekkiza olmayabdi.'
chain.desc6 = 'O`yinchi Raqibini Zanjir bilan urayabdi, lekin tekkiza olmayabdi.'
magniy = Magniy(20, 40, 2, 3, 0, True, False, False, "O'lim O'rog'i⏳",'1-3' + u'\U0001F525' + "|" + '2' + u'\U000026A1', 4, standart=False, natural=True)
magniy.desc1 = 'O`yinchi 𝗢`𝗹𝗶𝗺 𝗢`𝗿𝗼𝗴`𝗶💔 bilan Raqibini tanasiga 𝐬𝐡𝐢𝐤𝐚𝐬𝐭🤕, ruhiga 𝗮𝘇𝗼𝗯😭 beryabdi!'
magniy.desc2 = 'O`yinchi 𝗢`𝗹𝗶𝗺 𝗢`𝗿𝗼𝗴`𝗶💔 bilan Raqibini tanasiga 𝐬𝐡𝐢𝐤𝐚𝐬𝐭🤕, ruhiga 𝗮𝘇𝗼𝗯😭 beryabdi!'
magniy.desc3 = 'O`yinchi 𝗢`𝗹𝗶𝗺 𝗢`𝗿𝗼𝗴`𝗶💔 bilan Raqibini tanasiga 𝐬𝐡𝐢𝐤𝐚𝐬𝐭🤕, ruhiga 𝗮𝘇𝗼𝗯😭 beryabdi!'
magniy.desc4 = 'O`yinchi 𝗢`𝗹𝗶𝗺 𝗢`𝗿𝗼𝗴`𝗶💔 bilan Raqibni urayabdi, ammo unga ziyon😇 yetkaza olmayabdi.'
magniy.desc5 = 'O`yinchi 𝗢`𝗹𝗶𝗺 𝗢`𝗿𝗼𝗴`𝗶💔 bilan Raqibni urayabdi, ammo unga ziyon😇 yetkaza olmayabdi.'
magniy.desc6 = 'O`yinchi 𝗢`𝗹𝗶𝗺 𝗢`𝗿𝗼𝗴`𝗶💔 bilan Raqibni urayabdi, ammo unga ziyon😇 yetkaza olmayabdi.'
magniya = Magniy(3, 5, 2, 3, 0, True, False, False, "☠️O'lim O'rog'i⏳",'1-3' + u'\U0001F525' + "|" + '2' + u'\U000026A1', 4, standart=False, natural=True)
magniya.desc1 = 'O`yinchi 𝗢`𝗹𝗶𝗺 𝗢`𝗿𝗼𝗴`𝗶💔 bilan Raqibini tanasiga 𝐬𝐡𝐢𝐤𝐚𝐬𝐭🤕, ruhiga 𝗮𝘇𝗼𝗯😭 beryabdi!'
magniya.desc2 = 'O`yinchi 𝗢`𝗹𝗶𝗺 𝗢`𝗿𝗼𝗴`𝗶💔 bilan Raqibini tanasiga 𝐬𝐡𝐢𝐤𝐚𝐬𝐭🤕, ruhiga 𝗮𝘇𝗼𝗯😭 beryabdi!'
magniya.desc3 = 'O`yinchi 𝗢`𝗹𝗶𝗺 𝗢`𝗿𝗼𝗴`𝗶💔 bilan Raqibini tanasiga 𝐬𝐡𝐢𝐤𝐚𝐬𝐭🤕, ruhiga 𝗮𝘇𝗼𝗯😭 beryabdi!'
magniya.desc4 = 'O`yinchi 𝗢`𝗹𝗶𝗺 𝗢`𝗿𝗼𝗴`𝗶💔 bilan Raqibni urayabdi, ammo unga ziyon😇 yetkaza olmayabdi.'
magniya.desc5 = 'O`yinchi 𝗢`𝗹𝗶𝗺 𝗢`𝗿𝗼𝗴`𝗶💔 bilan Raqibni urayabdi, ammo unga ziyon😇 yetkaza olmayabdi.'
magniya.desc6 = 'O`yinchi 𝗢`𝗹𝗶𝗺 𝗢`𝗿𝗼𝗴`𝗶💔 bilan Raqibni urayabdi, ammo unga ziyon😇 yetkaza olmayabdi.'
sledge = Crushing(3, 1, 2, 2, 0, True, False, False, 'Kuvalda','1-3' + u'\U0001F525' + "|" + '2' + u'\U000026A1', standart=False)
sledge.desc1 = 'O`yinchi Raqibini Kuvalda bilan urayabdi!'
sledge.desc2 = 'O`yinchi Raqibini Kuvalda bilan urayabdi!'
sledge.desc3 = 'O`yinchi Raqibini Kuvalda bilan urayabdi!'
sledge.desc4 = 'O`yinchi Raqibini Kuvalda bilan urayabdi, lekin tekkiza olmayabdi.'
sledge.desc5 = 'O`yinchi Raqibini Kuvalda bilan urayabdi, lekin tekkiza olmayabdi.'
sledge.desc6 = 'O`yinchi Raqibini Kuvalda bilan urayabdi, lekin tekkiza olmayabdi.'
elektrez = Elektrez(3, 2, 2, 2, 0, True, False, False, 'Elektron Qilich🗡','1-3' + u'\U0001F525' + "|" + '2' + u'\U000026A1', standart=False)
elektrez.desc1 = 'O`yinchi Raqibini ⚡️𝗘𝗹𝗲𝗸𝘁𝗿𝗼𝗻 𝗤𝗶𝗹𝗶𝗰𝗵🗡 bilan urayabdi!'
elektrez.desc2 = 'O`yinchi Raqibini ⚡️𝗘𝗹𝗲𝗸𝘁𝗿𝗼𝗻 𝗤𝗶𝗹𝗶𝗰𝗵🗡 bilan urayabdi!'
elektrez.desc3 = 'O`yinchi Raqibini ⚡️𝗘𝗹𝗲𝗸𝘁𝗿𝗼𝗻 𝗤𝗶𝗹𝗶𝗰𝗵🗡 bilan urayabdi!'
elektrez.desc4 = 'O`yinchi Raqibini ⚡️𝗘𝗹𝗲𝗸𝘁𝗿𝗼𝗻 𝗤𝗶𝗹𝗶𝗰𝗵🗡 bilan urayabdi, lekin tekkiza olmayabdi.'
elektrez.desc5 = 'O`yinchi Raqibini ⚡️𝗘𝗹𝗲𝗸𝘁𝗿𝗼𝗻 𝗤𝗶𝗹𝗶𝗰𝗵🗡 bilan urayabdi, lekin tekkiza olmayabdi.'
elektrez.desc6 = 'O`yinchi Raqibini ⚡️𝗘𝗹𝗲𝗸𝘁𝗿𝗼𝗻 𝗤𝗶𝗹𝗶𝗰𝗵🗡 bilan urayabdi, lekin tekkiza olmayabdi.'
bow = BowBleeding(5, 1, 2, -1, 0, False, False, False, 'Asgard Kamoni','1-3!' + u'\U0001F525' + "|" + '2!' + u'\U000026A1', 3, standart=False)
bow.desc1 = 'O`yinchi Raqibiga Asgard Kamonidan otayabdi.'
bow.desc2 = 'O`yinchi Raqibiga Asgard Kamonidan otayabdi.'
bow.desc3 = 'O`yinchi Raqibiga Asgard Kamonidan otayabdi.'
bow.desc4 = 'O`yinchi Raqibiga Asgard Kamonidan otayabdi, lekin tekkiza olmayabdi.'
bow.desc5 = 'O`yinchi Raqibiga Asgard Kamonidan otayabdi, lekin tekkiza olmayabdi.'
bow.desc6 = 'O`yinchi Raqibiga Asgard Kamonidan otayabdi, lekin tekkiza olmayabdi.'
spear = Spear(4, 1, 3, 1, 0, True, False, True, 'Nayza', '1-4' + u'\U0001F44A' + "|" + '3' +  u'\U000026A1')
speareternal = SpearEternal(3, 1, 3, 1, 0, True, False, True, '⚡️TOR sekirasi⛏', '1-4' + u'\U0001F44A' + "|" + '3' +  u'\U000026A1', standart=False)
iceman = Iceman(1, 1, 0, 10, 0, True, False, True, 'Muzli Kristal❄️', '1-4' + u'\U0001F44A' + "|" + '3' +  u'\U000026A1', standart=False)
Sawn_off = Weapon(4, 1, 3, 1, 0, False, True, True, 'Miltiq', '1-4' + u'\U0001F4A5' + "|" + '3' + u'\U000026A1', pellets=True)
Sawn_off.desc1 = 'O`yinchi Raqibiga Miltiqdan otayabdi.'
Sawn_off.desc2 = 'O`yinchi Raqibiga Miltiqdan otayabdi.'
Sawn_off.desc3 = 'O`yinchi Raqibiga Miltiqdan otayabdi.'
Sawn_off.desc4 = 'O`yinchi Raqibiga Miltiqdan otayabdi, lekin tekkiza olmayabdi.'
Sawn_off.desc5 = 'O`yinchi Raqibiga Miltiqdan otayabdi, lekin tekkiza olmayabdi.'
Sawn_off.desc6 = 'O`yinchi Raqibiga Miltiqdan otayabdi, lekin tekkiza olmayabdi.'
Shotgun = Weapon(6, 2, 4, -2, 0, False, True, True, 'Drobovik', '2-7' + u'\U0001F4A5' + "|" + '4' + u'\U000026A1', pellets=True)
Shotgun.desc1 = 'O`yinchi Raqibiga Drobovikdan otayabdi.'
Shotgun.desc2 = 'O`yinchi Raqibiga Drobovikdan otayabdi.'
Shotgun.desc3 = 'O`yinchi Raqibiga Drobovikdan otayabdi.'
Shotgun.desc4 = 'O`yinchi Raqibiga Drobovikdan otayabdi, lekin tekkiza olmayabdi.'
Shotgun.desc5 = 'O`yinchi Raqibiga Drobovikdan otayabdi, lekin tekkiza olmayabdi.'
Shotgun.desc6 = 'O`yinchi Raqibiga Drobovikdan otayabdi, lekin tekkiza olmayabdi.'
Magnum = Weapon(2, 1, 3, 2, 3, False, False, True, 'Revolver', '3' + u'\U0001F4A5' + "|" + '3' + u'\U000026A1')
Magnum.desc1 = 'O`yinchi Raqibiga Revolverdan otayabdi.'
Magnum.desc2 = 'O`yinchi Raqibiga Revolverdan otayabdi.'
Magnum.desc3 = 'O`yinchi Raqibiga Revolverdan otayabdi.'
Magnum.desc4 = 'O`yinchi Raqibiga Revolverdan otayabdi, lekin tekkiza olmayabdi.'
Magnum.desc5 = 'O`yinchi Raqibiga Revolverdan otayabdi, lekin tekkiza olmayabdi.'
Magnum.desc6 = 'O`yinchi Raqibiga Revolverdan otayabdi, lekin tekkiza olmayabdi.'
Makarov = Weapon(3, 1, 3, 2, 0, False, False, True, 'Pistolet', '1-3' + u'\U0001F4A5' + "|" + '3' + u'\U000026A1')
Makarov.desc1 = 'O`yinchi Raqibiga Pistoletdan otayabdi.'
Makarov.desc2 = 'O`yinchi Raqibiga Pistoletdan otayabdi.'
Makarov.desc3 = 'O`yinchi Raqibiga Pistoletdan otayabdi.'
Makarov.desc4 = 'O`yinchi Raqibiga Pistoletdan otayabdi, lekin tekkiza olmayabdi.'
Makarov.desc5 = 'O`yinchi Raqibiga Pistoletdan otayabdi, lekin tekkiza olmayabdi.'
Makarov.desc6 = 'O`yinchi Raqibiga Pistoletdan otayabdi, lekin tekkiza olmayabdi.'
Bat = Stunning(3, 1, 2, 2, 0, True, False, True, 'Beysbol Bita', '1-3' + u'\U0001F44A' + "|" + '2' +  u'\U000026A1', 3)
Bat.desc1 = 'O`yinchi Raqibini Beysbol Bita bilan urayabdi.'
Bat.desc2 = 'O`yinchi Raqibini Beysbol Bita bilan urayabdi.'
Bat.desc3 = 'O`yinchi Raqibini Beysbol Bita bilan urayabdi.'
Bat.desc4 = 'O`yinchi Raqibini Beysbol Bita bilan urayabdi, lekin tekkiza olmayabdi.'
Bat.desc5 = 'O`yinchi Raqibini Beysbol Bita bilan urayabdi, lekin tekkiza olmayabdi.'
Bat.desc6 = 'O`yinchi Raqibini Beysbol Bita bilan urayabdi, lekin tekkiza olmayabdi.'
fangs = Bleeding(3, 1, 2, 1, 0, True, True, True, 'Tirnoqlar', '1-3' + u'\U0001F4A5' + "|" + '2' + u'\U000026A1', 4, standart=False, natural=True)
fangs.desc1 = 'O`yinchi Raqibiga tashlanayabdi.'
fangs.desc2 = 'O`yinchi Raqibiga tashlanayabdi.'
fangs.desc3 = 'O`yinchi Raqibiga tashlanayabdi.'
fangs.desc4 = 'O`yinchi Raqibiga tashlanayabdi, lekin tekkiza olmayabdi.'
fangs.desc5 = 'O`yinchi Raqibiga tashlanayabdi, lekin tekkiza olmayabdi.'
fangs.desc6 = 'O`yinchi Raqibiga tashlanayabdi, lekin tekkiza olmayabdi.'
fists = Weapon(1, 1, 2, 4, 0, True, True, True, 'Mushtlar', '1' + u'\U0001F4A5' + "|" + '2' + u'\U000026A1', standart=False, natural=True)
fists.desc1 = 'O`yinchi Raqibini Mushti bilan urayabdi.'
fists.desc2 = 'O`yinchi Raqibini Mushti bilan urayabdi.'
fists.desc3 = 'O`yinchi Raqibini Mushti bilan urayabdi.'
fists.desc4 = 'O`yinchi Raqibini Mushti bilan urayabdi, lekin tekkiza olmayabdi.'
fists.desc5 = 'O`yinchi Raqibini Mushti bilan urayabdi, lekin tekkiza olmayabdi.'
fists.desc6 = 'O`yinchi Raqibini Mushti bilan urayabdi, lekin tekkiza olmayabdi.'
master_fist = MasterFist(3, 1, 2, 2, 0, True, True, True, 'Elektr Shoker','1-3' + u'\U0001F525' + "|" + '2' + u'\U000026A1', standart=False, natural=True)
master_fist.desc1 = 'O`yinchi Raqibini Elektr Shoker bilan urayabdi.'
master_fist.desc2 = 'O`yinchi Raqibini Elektr Shoker bilan urayabdi.'
master_fist.desc3 = 'O`yinchi Raqibini Elektr Shoker bilan urayabdi.'
master_fist.desc4 = 'O`yinchi Raqibini Elektr Shoker bilan urayabdi, lekin tekkiza olmayabdi.'
master_fist.desc5 = 'O`yinchi Raqibini Elektr Shoker bilan urayabdi, lekin tekkiza olmayabdi.'
master_fist.desc6 = 'O`yinchi Raqibini Elektr Shoker bilan urayabdi, lekin tekkiza olmayabdi.'
masters = Masters(1, 1, 1, 2, 1, True, True, True, 'Kung-Fu♋️','1-3' + u'\U0001F525' + "|" + '2' + u'\U000026A1', standart=False, natural=True)
masters.desc1 = 'O`yinchi Raqibini Kung-Fu♋️ usuli bilan urayabdi.'
masters.desc2 = 'O`yinchi Raqibini Kung-Fu♋️ usuli bilan urayabdi.'
masters.desc3 = 'O`yinchi Raqibini Kung-Fu♋️ usuli bilan urayabdi.'
masters.desc4 = 'O`yinchi Raqibini Kung-Fu♋️ usuli bilan urayabdi, lekin tekkiza olmayabdi.'
masters.desc5 = 'O`yinchi Raqibini Kung-Fu♋️ usuli bilan urayabdi, lekin tekkiza olmayabdi.'
masters.desc6 = 'O`yinchi Raqibini Kung-Fu♋️ usuli bilan urayabdi, lekin tekkiza olmayabdi.'
