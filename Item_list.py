import utils
import config
import telebot
import random
import Weapon_list
import special_abilities

bot = telebot.TeleBot(config.token)
types = telebot.types
itemlist = []

# itema - предмет от способности
# itemt - предмет с целью
# itemat - предмет от способности с целью
# itemh - предмет, не траятящий хода
# iteme - предмет, тратящий энергию


class Item(object):
    acting = False

    def __init__(self, name, item_id, standart=True):
        self.name = name
        self.id = item_id
        self.energy = False
        self.standart = standart
        if self.standart:
            itemlist.append(self)
        if self.id[0:5] == 'iteme':
            self.energy = True

    def usenow(self, user):
        pass

    def aquare(self, user):
        pass

    def usefirst(self, user):
        pass

    def use(self, user):
        pass

    def uselast(self, user):
        pass

    def usebefore(self, user):
        pass


class Grenade(Item):
    def use(self, user):
        damage = random.randint(2, 3)
        enemycount = len(utils.get_other_team(user).actors)
        if enemycount > 2:
            target1 = utils.get_other_team(user).actors[random.randint(0, enemycount-1)]
            newtargets = list(utils.get_other_team(user).actors)
            newtargets.remove(target1)
            target2 = newtargets[random.randint(0, enemycount-2)]
            utils.damage(user, target1, damage, 'explosion')
            utils.damage(user, target2, damage, 'explosion')
            user.fight.string.add(u'\U0001F4A3' + " |" + user.name + ' Granatani otdi! Yetkazildi ' + str(damage)
                                  + ' zarb - ' + target2.name + ' va ' + target1.name + '.')
        else:
            for c in utils.get_other_team(user).actors:
                utils.damage(user, c, damage, 'melee')
            user.fight.string.add(u'\U0001F4A3' + " |" + user.name + ' Granatani otdi! Yetkazildi ' + str(
                                  damage) + ' zarb.')
        user.energy -= 2
        user.itemlist.remove(self)


class Raketa(Item):
    def use(self, user):
        damage = random.randint(1, 1)
        enemycount = len(utils.get_other_team(user).actors)
        if enemycount > 2:
            target1 = utils.get_other_team(user).actors[random.randint(0, enemycount-1)]
            newtargets = list(utils.get_other_team(user).actors)
            newtargets.remove(target1)
            target2 = newtargets[random.randint(0, enemycount-2)]
            utils.damage(user, target1, damage, 'explosion')
            utils.damage(user, target2, damage, 'explosion')
            user.fight.string.add(u'\U0001F4A3' + " |" + user.name + ' 𝗕𝗮𝗹𝗹𝗶𝘀𝘁𝗶𝗸 𝗥𝗮𝗸𝗲𝘁𝗮🚀 𝗼𝘁𝗮𝘆𝗮𝗯𝗱𝗶❕ \n📟𝗣𝗼𝗿𝘁𝗹𝗮𝘀𝗵 𝗸𝘂𝗰𝗵𝗶: ' + str(damage)
                                  + '❕ \n📡𝗡𝗶𝘀𝗵𝗼𝗻𝗹𝗮𝗿: ' + target2.name + ' va ' + target1.name + '❕')
        else:
            for c in utils.get_other_team(user).actors:
                utils.damage(user, c, damage, 'melee')
            user.fight.string.add(u'\U0001F4A3' + " |" + user.name + ' 𝗕𝗮𝗹𝗹𝗶𝘀𝘁𝗶𝗸 𝗥𝗮𝗸𝗲𝘁𝗮🚀 𝗼𝘁𝗮𝘆𝗮𝗯𝗱𝗶!❕ \n📟𝗣𝗼𝗿𝘁𝗹𝗮𝘀𝗵 𝗸𝘂𝗰𝗵𝗶: ' + str(
                                  damage) + '❕')
        user.energy -= 0
        user.itemlist.remove(self)


class Firegrenade(Item):
    def use(self, user):
        enemycount = len(utils.get_other_team(user).actors)
        targets = []
        if enemycount > 2:
            target1 = utils.get_other_team(user).actors[random.randint(0, enemycount-1)]
            newtargets = list(utils.get_other_team(user).actors)
            newtargets.remove(target1)
            target2 = newtargets[random.randint(0, enemycount-2)]
            newtargets = list(utils.get_other_team(user).actors)
            newtargets.remove(target2)
            target1.firecounter += 1
            target1.offfire = user.fight.round + 2
            targets.append(target1)
            if random.randint(1, 3) > 1:
                target2.firecounter += 1
                target2.offfire = user.fight.round + 2
                targets.append(target2)

        else:
            utils.get_other_team(user).actors[0].firecounter += 1
            utils.get_other_team(user).actors[0].offfire = user.fight.round + 2
            targets.append(utils.get_other_team(user).actors[0])
            for c in utils.get_other_team(user).actors[1:]:
                if random.randint(1, 3) > 1:
                    c.firecounter += 1
                    c.offfire = user.fight.round + 2
                    targets.append(c)
        if targets:
            user.fight.string.add(u'\U0001F378' + " |" + user.name + ' Molotov koktelini otayabdi! '
                                  + ', '.join([x.name for x in targets]) + ' yonmoqda!')
        else:
            user.fight.string.add(u'\U0001F378' + " |" + user.name
                                  + ' Molotov koktelini otayabdi, lekin hech kimga tegmayabdi!')
        user.energy -= 2
        user.itemlist.remove(self)


class Draa(Item):
    def use(self, user):
        enemycount = len(utils.get_other_team(user).actors)
        targets = []
        if enemycount > 2:
            target1 = utils.get_other_team(user).actors[random.randint(0, enemycount-1)]
            newtargets = list(utils.get_other_team(user).actors)
            newtargets.remove(target1)
            target2 = newtargets[random.randint(0, enemycount-2)]
            newtargets = list(utils.get_other_team(user).actors)
            newtargets.remove(target2)
            target1.firecounter += 4
            target1.offfire = user.fight.round + 2
            targets.append(target1)
            if random.randint(1, 3) > 1:
                target2.firecounter += 4
                target2.offfire = user.fight.round + 2
                targets.append(target2)

        else:
            utils.get_other_team(user).actors[0].firecounter += 4
            utils.get_other_team(user).actors[0].offfire = user.fight.round + 2
            targets.append(utils.get_other_team(user).actors[0])
            for c in utils.get_other_team(user).actors[1:]:
                if random.randint(1, 3) > 1:
                    c.firecounter += 4
                    c.offfire = user.fight.round + 2
                    targets.append(c)
        if targets:
            user.fight.string.add('🔥' + " |" + user.name + ' 𝗝𝗮𝘅𝗮𝗻𝗻𝗮𝗺 𝗢𝗹𝗼𝘃𝗶𝗻𝗶🌋 chaqirmoqda! '
                                  + ', '.join([x.name for x in targets]) + ' yonmoqda!')
        else:
            user.fight.string.add('🔥' + " |" + user.name
                                  + ' butun maydonni🌋 olovga to`ldirmoqda, lekin hech kimga yonmayabdi!')
        user.energy -= 2
        user.itemlist.remove(self)


class GasGrenade(Item):
    def useact(self, user):
        keyboard = types.InlineKeyboardMarkup()
        for p in utils.get_other_team(user).actors:
            callback_button = types.InlineKeyboardButton(text=p.name, callback_data='spitem' + str(p.chat_id))
            keyboard.add(callback_button)
        keyboard.add(types.InlineKeyboardButton(text='Bekor qilish', callback_data=str('spitemcancel')))
        bot.send_message(user.chat_id, 'Otish uchun nishon tanlang.',
                         reply_markup=keyboard)

    def use(self, user):
        user.fight.string.add(u'\U0001F635' + " |" + user.name + ' Nurli portlagichni otayabdi '
                              + user.itemtarget.name + '. (- 8 energiya)')
        del user.itemtarget
        user.itemlist.remove(self)

    def usefirst(self, user):
        if special_abilities.Impaler in user.itemtarget.abilities:
            user.fight.string.add(u'\U0000274C' + "|" + user.itemtarget.name + ' yorug`likka e`tibor bermayabdi.')
        elif special_abilities.Gasmask in user.itemtarget.abilities:
            user.fight.string.add(u'\U0000274C' + "|" + user.itemtarget.name + ' yorug`likdan himoyalangan. (-1 energiya)')
            user.itemtarget.energy -= 1
        else:
            user.itemtarget.energy -= 8


class Shield(Item):
    def useact(self, user):
        keyboard = types.InlineKeyboardMarkup()
        for p in user.team.actors:
            callback_button = types.InlineKeyboardButton(text=p.name,callback_data='spitem' + str(p.chat_id))
            keyboard.add(callback_button)
        keyboard.add(types.InlineKeyboardButton(text='Bekor qilish', callback_data=str('spitemcancel')))
        bot.send_message(user.chat_id, 'Qalqon uchun mo`ljal tanlang.',reply_markup=keyboard)

    def use(self, user):
        if user.itemtarget == user:
            user.fight.string.add(u'\U0001F535' + " |" + user.name + ' qalqon ishlatayabdi. Zarb qaytarildi!')
        else:
            user.fight.string.add(u'\U0001F535' + " |" + user.name + ' ga qalqonni ishlatayabdi ' + user.itemtarget.name + '. Zarb qaytarildi!')

    def uselast(self, user):
        user.itemtarget.damagetaken = 0
        user.itemlist.remove(self)
        del user.itemtarget


class ThrowingKnife(Item):

    def useact(self, user):
        keyboard = types.InlineKeyboardMarkup()
        for p in utils.get_other_team(user).actors:
            callback_button = types.InlineKeyboardButton(text=p.name,callback_data='spitem' + str(p.chat_id))
            keyboard.add(callback_button)
        keyboard.add(types.InlineKeyboardButton(text='Bekor qilish', callback_data=str('spitemcancel')))
        chance = (user.energy + 4)*10
        if chance > 100:
            chance = 100
        bot.send_message(user.chat_id, 'Pichoq uchun nishonni tanlang. Tegish ehtimoli - ' + str(chance) + '%',reply_markup=keyboard)

    def use(self, user):
        if random.randint(1, 10)<=user.energy + 5:
            user.fight.string.add(u'\U0001F52A' + " |" + user.name + ' Uchar pichoqni otdi va '
                                  + user.itemtarget.name + 'ga 1ta zarb yetkazdi ' +
                                  u'\U00002763' + "|" + user.itemtarget.name + ' qon yo`qotayabdi!')
            utils.damage(user, user.itemtarget, 1, 'melee')
            user.itemtarget.bleedcounter += 1
            user.itemtarget.bloodloss = False

        else:
            user.fight.string.add(u'\U0001F4A8' + " |" + user.name + ' Uchar pichoqni otayabdi, lekin tegmayabdi.')
        user.itemlist.remove(self)
        user.energy -= 1
        del user.itemtarget


class Jet(Item):
    def useact(self, user):
        bot.send_message(user.chat_id, '3ta yurishdan so`ng energiyangiz maksimumgacha tiklanadi!')
        user.useditems.append(self)
        user.itemlist.remove(self)

    def used(self, user):
        user.fight.string.add(u'\U0001F489' + " |" + user.name + ' Djetni ishlatayabdi.')
        user.jetturn = user.fight.round + 2
        user.Drugged = True
        user.abilities.append(special_abilities.Jet)


class Chitin(Item):
    def useact(self, user):
        bot.send_message(user.chat_id, 'Siz 3 yurishga 2 sovut himoyasi olasiz! Uchinchisi ohirida siz karaxt bo`lib qolasiz.')
        user.useditems.append(self)
        user.itemlist.remove(self)

    def used(self, user):
        user.fight.string.add(u'\U0001F489' + " |" + user.name + ' Xitinni ishlatayabdi.')
        user.chitinoff = user.fight.round + 2
        user.armor += 2
        user.armorchance += 100
        user.Drugged = True
        user.abilities.append(special_abilities.Chitin)


class Drug(Item):
    def useact(self, user):
        bot.send_message(user.chat_id, 'Raund boshida sizni energiyangiz 3 ga ortadi!')
        user.useditems.append(self)
        user.itemlist.remove(self)

    def used(self, user):
        user.energy += 3
        user.Drugged = True
        user.fight.string.add(u'\U0001F489' + " |" + user.name + ' Adrenalin ishlatayabdi, energiyasini 3 taga ko`paytirdi.')


class Heal(Item):
    def useact(self, user):
        keyboard = types.InlineKeyboardMarkup()
        for p in user.team.actors:
            if p.Alive:
                callback_button = types.InlineKeyboardButton(text=p.name,callback_data='spitem' + str(p.chat_id))
                keyboard.add(callback_button)
        keyboard.add(types.InlineKeyboardButton(text='Bekor qilish', callback_data=str('spitemcancel')))
        bot.send_message(user.chat_id, 'Davolash uchun nishonni tanlang.',reply_markup=keyboard)


    def use(self, user):
        if user.itemtarget == user:
            user.fight.string.add(u'\U0001F489' + " |" + user.name + ' stimulyatorni ishlatayabdi.')
        else:
            user.fight.string.add(u'\U0001F489' + " |" + user.name + ' stimulyatorni berayabdi ' + user.itemtarget.name + 'ga.')
        user.enditems.append(self)
        user.itemlist.remove(self)

    def used(self, user):
        user.itemtarget.hp += 2
        user.Drugged = True
        if user.itemtarget.hp > user.itemtarget.maxhp: user.itemtarget.hp = user.itemtarget.maxhp
        user.fight.string.add(u'\U00002665'*user.itemtarget.hp + u'\U0001F489' + " |" + user.itemtarget.name + ' 2ta jon olayabdi. Qoldi ' + str(user.itemtarget.hp)
                                     + ' jon.')
        user.enditems.remove(self)
        del user.itemtarget


class Healt(Item):
    def useact(self, user):
        keyboard = types.InlineKeyboardMarkup()
        for p in user.team.actors:
            if p.Alive:
                callback_button = types.InlineKeyboardButton(text=p.name,callback_data='spitem' + str(p.chat_id))
                keyboard.add(callback_button)
        keyboard.add(types.InlineKeyboardButton(text='Bekor qilish', callback_data=str('spitemcancel')))
        bot.send_message(user.chat_id, 'Davolash uchun nishonni tanlang.',reply_markup=keyboard)


    def use(self, user):
        if user.itemtarget == user:
            user.fight.string.add('👨‍⚕️Doktor' + " |" + user.name + ' dorini💊 ishlatayabdi.')
        else:
            user.fight.string.add('👨‍⚕️Doktor' + " |" + user.name + ' ' + user.itemtarget.name + 'ga dori💊 beryabdi.')
        user.enditems.append(self)
        user.itemlist.remove(self)

    def used(self, user):
        user.itemtarget.hp += 1
        user.Drugged = True
        if user.itemtarget.hp > user.itemtarget.maxhp: user.itemtarget.hp = user.itemtarget.maxhp
        user.fight.string.add(u'\U00002665'*user.itemtarget.hp + '💊' + " |" + user.itemtarget.name + ' 1ta jon olyabdi. Qoldi' + str(user.itemtarget.hp)
                                     + ' jon.')
        user.enditems.remove(self)
        del user.itemtarget



drug = Drug('Adrenalin','itemh01')
shield = Shield('Qalqon', 'itemt02')
gasgrenade = GasGrenade('Nurli portlagich', 'itemt04')
grenade = Grenade('Granata', 'iteme01')
raketa = Raketa('Raketa', 'iteme04')
firegrenade = Firegrenade('Kokteyl', 'iteme02')
draa = Draa('Ajal olovi', 'iteme03', standart=False)
throwingknife = ThrowingKnife('Uchuvchi pichoq', 'itemt03')
jet = Jet('Djet', 'itemh02')
chitin = Chitin('Xitin', 'itemh03')
heal = Heal('Stimulyator', 'itemt01', standart=False)
healt = Healt('Dori', 'itemt05', standart=False)
id_items = list(itemlist)



class Shieldg(Item):
    def useact(self, user):
        keyboard = types.InlineKeyboardMarkup()
        for p in user.team.actors:
            callback_button = types.InlineKeyboardButton(text=p.name, callback_data='spitem' + str(p.chat_id))
            keyboard.add(callback_button)
        keyboard.add(types.InlineKeyboardButton(text='Bekor qilish', callback_data=str('spitemcancel')))
        bot.send_message(user.chat_id, 'Shit uchun nishon tanlang.', reply_markup=keyboard)
    def use(self, user):
        if user.itemtarget == user:
            user.fight.string.add(u'\U0001F535' + " |" + user.name + ' qalqonni ishlatayabdi. Zarb qaytarildi!')
        else:
            user.fight.string.add(u'\U0001F535' + " |" + user.name + ' qalqonni berayabdi ' + user.itemtarget.name + 'ga. Zarb qaytarildi!')
    def uselast(self, user):
        user.shieldrefresh = user.fight.round + 4
        user.itemtarget.damagetaken = 0
        user.itemlist.remove(self)
        del user.itemtarget


class Hypnosys(Item):
    def useact(self, user):
        keyboard = types.InlineKeyboardMarkup()
        for p in utils.get_other_team(user).actors:
            callback_button = types.InlineKeyboardButton(text=p.name, callback_data='spitem' + str(p.chat_id))
            keyboard.add(callback_button)
        keyboard.add(types.InlineKeyboardButton(text='Bekor qilish', callback_data=str('spitemcancel')))
        bot.send_message(user.chat_id, 'Gipnoz uchun nishonni tanlang.', reply_markup=keyboard)

    def usefirst(self, user):
        if user.itemtarget.target is None:
            user.fight.string.add(
                    u'\U0001F31D' + "|" + 'Gipnozchi ' + user.name + " nishonni gipnozlash qo`lidan kelmayabdi " + user.itemtarget.name
                    + '.')
        elif random.randint(1,100) > user.itemtarget.hypnosysresist:
            user.itemtarget.target = user.itemtarget.team.actors[
                    random.randint(0, len(user.itemtarget.team.actors) - 1)]
            user.fight.string.add(
                    u'\U0001F31A' + "|" + 'Gipnozchi ' + user.name + " nishonni gipnozlab qo`ydi " + user.itemtarget.name
                    + '. Yangi nishon - ' + user.itemtarget.target.name + '!')

            user.itemtarget.tempaccuracy -= 2
        else:
            user.fight.string.add(
                    u'\U0001F31D' + "|" + 'Gipnozchi ' + user.name + " nishonni gipnozladi, ammo " + user.itemtarget.name
                    + ' Gipnozga qarshilik ko`rsatayabdi!')
            user.itemtarget.tempaccuracy -= 10
        user.hypnosysrefresh = user.fight.round + 5
        user.itemlist.remove(self)
        del user.itemtarget


class Isaev(Item):

    def useact(self, user):
        keyboard = types.InlineKeyboardMarkup()
        for p in utils.get_other_team(user).actors:
            callback_button = types.InlineKeyboardButton(text=p.name, callback_data='spitem' + str(p.chat_id))
            keyboard.add(callback_button)
        keyboard.add(types.InlineKeyboardButton(text='Bekor qilish', callback_data=str('spitemcancel')))
        bot.send_message(user.chat_id, 'Xaqoratlash uchun nishonni tanlang.', reply_markup=keyboard)

    def usefirst(self, user):
        if random.randint(1, 100) <= 100:
            user.fight.string.add(
                u'\U0001F595' + u'\U0001F494' + "|" + 'Kachok ' + user.name + " " + user.itemtarget.name
                + 'ni so`kayabdi. ' + user.itemtarget.name + ' o`ziga ishonchini yo`qotib qo`ydi!')
            user.itemtarget.Suicide = True
        else:
            user.fight.string.add(
                u'\U0001F595' + "|" + 'Kachok ' + user.name + " " + user.itemtarget.name
                + 'ni  so`kayabdi.')
        user.isaevrefresh = user.fight.round + 2
        user.itemlist.remove(self)
        del user.itemtarget


class Mental(Item):
    def useact(self, user):
        keyboard = types.InlineKeyboardMarkup()
        for p in utils.get_other_team(user).actors:
            callback_button = types.InlineKeyboardButton(text=p.name, callback_data='info' + str(p.chat_id))
            keyboard.add(callback_button)
        keyboard.add(types.InlineKeyboardButton(text='Bekor qilish', callback_data=str('infocancel')))
        bot.send_message(user.chat_id, 'Ma`lumotni olishni hohlagan nishonizni tanlang.', reply_markup=keyboard)


class Engineer(Item):
    def useact(self, user):
        keyboard = types.InlineKeyboardMarkup()
        for p in user.team.players:
            if not p.weapon.Melee and p != user:
                callback_button = types.InlineKeyboardButton(text=p.name, callback_data='spitem' + str(p.chat_id))
                keyboard.add(callback_button)
        keyboard.add(types.InlineKeyboardButton(text='Bekor qilish', callback_data=str('spitemcancel')))
        bot.send_message(user.chat_id, 'Ma`lumotni olishni hohlagan nishonizni tanlang.', reply_markup=keyboard)

    def use(self, user):
        user.fight.string.add(u'\U0001F527' + " |" + user.name + ' qayta o`qlayabdi ' + user.itemtarget.name + '. Energiya maksimalgacha tiklandi! (' + str(
            user.itemtarget.maxenergy) + ')')
        user.itemtarget.energy = user.itemtarget.maxenergy
        user.engineerrefresh = user.fight.round + 3


    def uselast(self, user):
        user.itemtarget.accuracy += 1
        user.itemtarget.accuracyfix += 1
        user.itemlist.remove(self)
        del user.itemtarget


class Ritual(Item):
    def useact(self, user):
        keyboard = types.InlineKeyboardMarkup()
        cureses = list(user.fight.actors)
        for p in cureses:
            callback_button = types.InlineKeyboardButton(text=p.name, callback_data='spitem' + str(p.chat_id))
            keyboard.add(callback_button)
        keyboard.add(types.InlineKeyboardButton(text='Bekor qilish', callback_data=str('spitemcancel')))
        bot.send_message(user.chat_id, 'O`ljani tanlang.', reply_markup=keyboard)

    def use(self, user):
        user.fight.string.add(u'\U0001F47F' + " |" + user.name + ' yerga g`alati belgilarni chizayabdi.')
        user.cursecounter = 5
        user.cursetarget = user.itemtarget
        user.itemlist.remove(self)


class Curse(Item):
    def useact(self, user):
        keyboard = types.InlineKeyboardMarkup()
        for p in user.fight.actors:
            callback_button = types.InlineKeyboardButton(text=p.name, callback_data='spitem' + str(p.chat_id))
            keyboard.add(callback_button)
        keyboard.add(types.InlineKeyboardButton(text='Bekor qilish', callback_data=str('spitemcancel')))
        bot.send_message(user.chat_id, 'Lanatlash uchun nishonni tanlang.', reply_markup=keyboard)

    def use(self, user):
        user.fight.string.add(u'\U0001F47F' + " |" + user.name + ' qo`llarini osmonga ko`tarayabdi. Chaqmoq'
                                                                 ' urdi ' + user.itemtarget.name + 'ni.')
        user.itemtarget.hp -= 2
        user.fight.string.add(u'\U00002665' * user.itemtarget.hp + ' |' + str(user.itemtarget.name) +
                         " yo`qotayabdi " + str(2) + " jonni. Qoldi " + str(user.itemtarget.hp) + " jon.")
        user.itemlist.remove(self)


class Explode_corpse(Item):
    def use(self, user):
        damage = random.randint(2, 3)
        enemycount = len(utils.get_other_team(user).actors)
        if enemycount > 2:
            target1 = utils.get_other_team(user).actors[random.randint(0, enemycount - 1)]
            newtargets = list(utils.get_other_team(user).actors)
            newtargets.remove(target1)
            target2 = newtargets[random.randint(0, enemycount - 2)]
            utils.damage(user, target1, damage, 'melee')
            utils.damage(user, target2, damage, 'melee')
            user.fight.string.add(u'\U0001F47F' + " |" + user.name + ' o`likni portlatayabdi! Yetkaziladi ' + str(damage)
                                  + ' zarb ' + target2.name + ' va ' + target1.name + 'ga.')
        else:
            for c in utils.get_other_team(user).actors:
                utils.damage(user, c, damage, 'melee')
            user.fight.string.add(u'\U0001F47F' + " |" + user.name + ' o`likni portlatayabdi! Yetkaziladi ' + str(
                damage) + ' zarb.')
        user.corpsecounter -= 1
        user.itemlist.remove(self)


class Zombie(Item):

    def useact(self, user):
        keyboard = types.InlineKeyboardMarkup()
        zombies = list(user.team.deadplayers)
        for p in zombies:
            if not p.bot:
                callback_button = types.InlineKeyboardButton(text=p.name, callback_data='spitem' + str(p.chat_id))
                keyboard.add(callback_button)
        keyboard.add(types.InlineKeyboardButton(text='Bekor qilish', callback_data=str('spitemcancel')))
        bot.send_message(user.chat_id, 'Zombini tanlang.', reply_markup=keyboard)

    def use(self, user):
        user.fight.string.add(u'\U0001F47F' + " |" + user.name + ' zombini ko`tarayabdi.')
        if Zombie not in user.itemtarget.abilities:
            user.itemtarget.abilities = []
            user.itemtarget.itemlist = []
            user.itemtarget.passive = []
            user.itemtarget.truedamage = 0
            user.itemtarget.accuracy = 0
            user.itemtarget.mult = 1
            user.itemtarget.armor = 0
            user.itemtarget.armorchance = 0
            user.itemtarget.tempaccuracy = 0
            user.itemtarget.firecounter = 0
            user.itemtarget.bleedcounter = 0
            user.itemtarget.stuncounter = 0
            user.itemtarget.maxenergy = 0
            user.itemtarget.maxhp = 0
            user.itemtarget.weapon = Weapon_list.fangs
            user.itemtarget.abilities.append(special_abilities.Zombie)
            user.itemtarget.team.actors.append(user.itemtarget)
            user.itemtarget.team.players.append(user.itemtarget)
            try:
                user.itemtarget.team.deadplayers.remove(user.itemtarget)
            except ValueError:
                pass
            user.itemtarget.fight.activeplayers.append(user.itemtarget)
            user.itemtarget.fight.actors.append(user.itemtarget)
            user.itemtarget.hungercounter = 3
            user.itemtarget.accuracy = 7 - user.itemtarget.hungercounter*2
            user.itemtarget.turn = 'raise'
            user.itemlist.remove(self)


class Steal(Item):

    def useact(self, user):
        keyboard = types.InlineKeyboardMarkup()
        for p in utils.get_other_team(user).actors:
            callback_button = types.InlineKeyboardButton(text=p.name, callback_data='spitem' + str(p.chat_id))
            keyboard.add(callback_button)
        keyboard.add(types.InlineKeyboardButton(text='Отмена', callback_data=str('spitemcancel')))
        bot.send_message(user.chat_id, 'O`g`irlash uchun nishonni tanlang.', reply_markup=keyboard)

    def usebefore(self, user):
        if user.itemtarget.turn[:4] == 'item' and user.itemtarget.turn[:5] != 'itema':
            user.itemtarget.turn = 'loss' + user.itemtarget.turn
            for i in user.itemtarget.itemlist:
                if i.id == user.itemtarget.turn[4:11]:
                    user.itemtarget.itemlist.remove(i)
                    user.itemlist.append(i)
                    user.stolenitem = i.name
                    break
        elif user.itemtarget.useditems:
            x = user.itemtarget.useditems[-1]
            user.itemtarget.useditems.remove(x)
            user.itemlist.append(x)
            user.stolenitem = x.name


    def use(self, user):
        if not user.itemtarget.itemlist:
            bot.send_message(user.chat_id, 'Nishonda hech vaqo yo`q ekan!')
        if user.itemtarget.turn[0:4] == 'loss':
            user.fight.string.add(
                u'\U0001F60F' + "|" + user.itemtarget.name + " " + user.stolenitem
                + 'ni ishlatishga harakat qilyabdi, lekin uni ' + user.name + ' o`g`irlab ketgandi!')
            user.itemtarget.turn = 'losе'
            del user.stolenitem
        elif hasattr(user, 'stolenitem'):
            user.fight.string.add(
                u'\U0001F60F' + "|" + user.itemtarget.name + " " + user.stolenitem
                + 'ni  ishlatishga harakat qilyabdi, lekin u narsa ' + user.name + 'da edi!')
            del user.stolenitem
        else:
            user.fight.string.add(
                u'\U0001F612' + "|" + 'O`g`ri ' + user.name + ' hech narsani o`g`irlay olmadi!')
        user.stealrefresh = user.fight.round + 2
        user.itemlist.remove(self)
        del user.itemtarget


class Throwing(Item):
    def useact(self, user):
        keyboard = types.InlineKeyboardMarkup()
        for p in utils.get_other_team(user).actors:
            callback_button = types.InlineKeyboardButton(text=p.name,callback_data='spitem' + str(p.chat_id))
            keyboard.add(callback_button)
        keyboard.add(types.InlineKeyboardButton(text='Bekor qilish', callback_data=str('spitemcancel')))
        chance = utils.get_hit_chance(user, 0)
        bot.send_message(user.chat_id, 'Sekira uchun nishonni tanlang. Tegish ehtimolligi - ' + str(int(chance)) + '%',reply_markup=keyboard)

    def use(self, user):
        n = 0
        d = 0
        dmax = 5
        while d != dmax:
            x = random.randint(1, 10)
            print(user.name + ' Tushib qoldi ' + str(x))
            if x > 10 - user.energy - user.accuracy - user.tempaccuracy - 1:
                n += 1
            d += 1
        for a in user.abilities:
            n = a.onhit(a, n, user)
        # бонусный урон персонажа
        if n != 0:
            n += user.bonusdamage + 2
        # уходит энергия
        user.energy -= 3
        utils.damage(user, user.itemtarget, n, 'melee')
        if n != 0:
            user.fight.string.add('🌩' + " |" + user.name + ' SEKIRA teleportatsiyasidan⭕️ foydalanib Oyboltani⛏ '
                                  + user.itemtarget.name + 'ga masofadan uloqtirayabdi. Yetkazildi ' + str(n) + ' zarb!')

        else:
            user.fight.string.add(u'\U0001F4A8' + " |" + user.name + ' Oyboltani⛏ otayabdi, lekin tekkiza olmayabdi.')
        user.itemlist.remove(self)
        user.throwcd += 2
        user.lostweapon = Weapon_list.speareternal
        del user.itemtarget

zombie = Zombie('O`likni turg`izish', 'itemat6',standart=False)
shieldg = Shieldg('Qalqon|Generator', 'itemat1',standart=False)
hypnosys = Hypnosys('Gipnoz', 'itemat2',standart=False)
isaev = Isaev('So`kish', 'itemat7',standart=False)
steal = Steal('O`g`irlash', 'itemat8',standart=False)
mental = Mental('Kuzatish', 'mitem01',standart=False)
engineer = Engineer('Qurolchi', 'itemat3',standart=False)
ritual = Ritual('Ritual', 'itemat4',standart=False)
curse = Curse('Lanatlash', 'itemat5',standart=False)
explode_corpse = Explode_corpse('O`likni portlatish', 'itema01',standart=False)
throw = Throwing('Sekirani otish', 'itemat0',standart=False)
id_items.append(shieldg)
id_items.append(hypnosys)
id_items.append(mental)
id_items.append(isaev)
id_items.append(engineer)
id_items.append(ritual)
id_items.append(curse)
id_items.append(heal)
id_items.append(healt)
id_items.append(zombie)
id_items.append(steal)
id_items.append(explode_corpse)
id_items.append(throw)
id_items.append(draa)
items = {p.id:p for p in id_items}
