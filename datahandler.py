import json
import os
from datetime import datetime
from threading import Lock
import math

# === Конфигурация ===
database_path = 'player_database.json'
db_lock = Lock()

# === Инициализация базы данных ===
if not os.path.exists(database_path):
    with open(database_path, "w", encoding="utf-8") as f:
        json.dump({}, f)

# === Загрузка и сохранение ===
def load_db():
    with db_lock:
        if not os.path.exists(database_path):
            return {}
        with open(database_path, 'r', encoding='utf-8') as f:
            return json.load(f)

def save_db(data):
    with db_lock:
        with open(database_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)


# === Игрок по умолчанию ===
def create_default_player(chat_id, username=None, name=None):
    return {
        'id': chat_id,
        'games_played': 0,
        'games_won': 0,
        'name': name,
        'username': '@' + username if username else None,
        'private_string': 0,
        'unique_weapon': [],
        'unique_items': [],
        'unique_skills': [],
        'current_weapons': None,
        'current_items': [],
        'current_skills': [],
        'rating': 1000
    }

# === Работа с рейтингами ===

def fetch_player(chat_id):
    db = load_db()
    return db.get(str(chat_id))

def get_rating(chat_id):
    player = fetch_player(chat_id)
    return player.get("rating", 1000) if player else 1000

def set_rating(chat_id, new_rating):
    db = load_db()
    cid = str(chat_id)
    if cid not in db:
        return  # безопасно игнорируем, если игрока нет
    db[cid]["rating"] = int(new_rating)
    save_db(db)

# === Алгоритм Elo ===
def get_k(rating):
    if rating > 2400:
        return 10
    if 2400 > rating > 1100:
        return 20
    return 40

#def get_k(rating):
 #   return 50  # постоянное значение K для более динамичного рейтинга

def expected_score(rating, opponent_rating):
    return 1 / (1 + 10 ** ((opponent_rating - rating) / 400))

def outcome(a_rating, b_rating, a_score, b_score):
    expected_a = expected_score(a_rating, b_rating)
    expected_b = 1 - expected_a

    if a_score > b_score:
        actual_a, actual_b = 1, 0
    elif a_score < b_score:
        actual_a, actual_b = 0, 1
    else:
        actual_a, actual_b = 0.5, 0.5

    goal_diff = abs(a_score - b_score)
    goal_factor = 1 + math.log2(1 + goal_diff)

    k_a = get_k(a_rating)
    k_b = get_k(b_rating)

    k_a_adjusted = int(k_a * goal_factor)
    k_b_adjusted = int(k_b * goal_factor)

    loss_factor = 0.3
    MIN_CHANGE = 5

    delta_a = round(k_a_adjusted * (actual_a - expected_a))
    delta_b = round(k_b_adjusted * (actual_b - expected_b))

    if abs(delta_a) < MIN_CHANGE:
        delta_a = MIN_CHANGE if delta_a > 0 else -MIN_CHANGE
    if abs(delta_b) < MIN_CHANGE:
        delta_b = MIN_CHANGE if delta_b > 0 else -MIN_CHANGE

    if actual_a < expected_a:
        delta_a = int(delta_a * loss_factor)
    if actual_b < expected_b:
        delta_b = int(delta_b * loss_factor)

    new_a_rating = a_rating + delta_a
    new_b_rating = b_rating + delta_b

    return new_a_rating, new_b_rating

# === Топ игроков ===
def load_all_players():
    return load_db().values()

def get_top_ratings(limit=10):
    all_players = load_all_players()
    sorted_players = sorted(all_players, key=lambda p: p.get("rating", 1000), reverse=True)
    return sorted_players[:limit]


# === Основные функции ===
def get_player(chat_id, username, first_name):
    db = load_db()
    cid = str(chat_id)
    if cid not in db:
        db[cid] = create_default_player(chat_id, username, first_name)
        save_db(db)

def get_all_stats():
    db = load_db()
    result = []
    for player_id, player in db.items():
        games = player.get("games_played", 0)
        wins = player.get("games_won", 0)
        name = player.get("name") or (player.get("username") or f"ID:{player_id}")
        if games > 0:  # фильтруем тех, кто вообще не играл
            result.append({
                "id": player_id,
                "name": name,
                "games": games,
                "wins": wins
            })
    return result


def get_games(chat_id):
    db = load_db()
    player = db.get(str(chat_id))
    return (player['games_played'], player['games_won']) if player else (0, 0)

def add_played_games(chat_id, game=1):
    db = load_db()
    player = db.get(str(chat_id))
    if player:
        player['games_played'] += game
        save_db(db)

def add_won_games(chat_id, game=1):
    db = load_db()
    player = db.get(str(chat_id))
    if player:
        player['games_won'] += game
        save_db(db)

def getallplayers():
    return list(load_db().keys())

def get_dataname(chat_id):
    return load_db().get(str(chat_id), {}).get('name')

def get_current(chat_id):
    player = load_db().get(str(chat_id))
    if player:
        return player['current_weapons'], player['current_items'], player['current_skills']
    return None

def get_private_string(chat_id):
    return load_db().get(str(chat_id), {}).get('private_string')

def change_private_string(chat_id):
    db = load_db()
    player = db.get(str(chat_id))
    if player:
        player['private_string'] = 1 - player['private_string']
        save_db(db)

def get_unique(chat_id):
    player = load_db().get(str(chat_id))
    if player:
        return player['unique_weapon'], player['unique_items'], player['unique_skills']
    return None

def change_weapon(cid, weapon_name):
    db = load_db()
    player = db.get(str(cid))
    if player:
        player['current_weapons'] = weapon_name
        save_db(db)

def add_item(cid, item_id):
    db = load_db()
    player = db.get(str(cid))
    if player and len(player['current_items']) < 2 and item_id not in player['current_items']:
        player['current_items'].append(item_id)
        save_db(db)
        return True
    return False

def delete_item(cid, item_id):
    db = load_db()
    player = db.get(str(cid))
    if player and item_id in player['current_items']:
        player['current_items'].remove(item_id)
        save_db(db)
        return True
    return False

def add_skill(cid, skill_name):
    db = load_db()
    player = db.get(str(cid))
    if player and len(player['current_skills']) < 2 and skill_name not in player['current_skills']:
        player['current_skills'].append(skill_name)
        save_db(db)
        return True
    return False

def delete_skill(cid, skill_name):
    db = load_db()
    player = db.get(str(cid))
    if player and skill_name in player['current_skills']:
        player['current_skills'].remove(skill_name)
        save_db(db)
        return True
    return False

def player_exists(player_id):
    return str(player_id) in load_db()

def add_unique_weapon(player_id, weapon_name):
    data = load_db()
    pid = str(player_id)
    if pid not in data:
        data[pid] = create_default_player(int(pid))
    weapons = data[pid].setdefault("unique_weapon", [])
    if weapon_name in weapons:
        return False
    weapons.append(weapon_name)
    save_db(data)
    return True

def delete_unique_weapon(player_id, weapon_name):
    data = load_db()
    pid = str(player_id)
    if pid not in data:
        data[pid] = create_default_player(int(pid))
    weapons = data[pid].get("unique_weapon", [])
    if weapon_name in weapons:
        weapons.remove(weapon_name)
        save_db(data)
        return True
    return False

def get_unique_weapon(player_id):
    data = load_db()
    pid = str(player_id)
    if pid not in data:
        data[pid] = create_default_player(int(pid))
        save_db(data)
    return data[pid].get("unique_weapon", [])

def delete_dungeon_weapons():
    dungeon_weapons = [
        "Kuvalda", "Bumerang〽️", "☠️O'lim O'rog'i⏳", "Sehrli Tayoqcha🧚‍♂",
        "🐺Bo`ri infeksiyasi🧬", "ShotGun🧨", "🔹Muzli Kristal🔹",
        "⚡️TOR sekirasi⛏", "🔸Olovli Kristal🔸"
    ]
    data = load_db()
    for player in data.values():
        player["unique_weapon"] = [w for w in player.get("unique_weapon", []) if w not in dungeon_weapons]
    save_db(data)

def delete_inventory(player_id):
    data = load_db()
    pid = str(player_id)
    if pid in data:
        data[pid]["unique_weapon"] = []
        save_db(data)

def delete_all_players():
    save_db({})