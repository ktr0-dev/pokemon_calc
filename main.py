import json

# 1. データ定義
def load_pokemon_data(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)

POKEMON_DATA = load_pokemon_data("pokemon_data.json")
TYPE_CHART = load_pokemon_data("type_chart.json")

# 2. 処理
def calculate_real_stat(stat_type, base_stat, ability_point, nature_multiplier):
    if stat_type == "H":
        return int((base_stat * 2 + 31) * 50 / 100) + 50 + 10 + ability_point
    else:
        return int((int((base_stat * 2 + 31) * 50 / 100) + 5 + ability_point) * nature_multiplier)

def calculate_damage(attacker_stat, defender_stat, move_power, is_double_spread, weather_multiplier, is_critical, is_stab, type_multiplier, is_burned_physical, wall_multiplier=1.0):
    base_damage = int((int(2 * 50 / 5 + 2) * move_power * attacker_stat / defender_stat / 50) + 2)
    
    # 1. ダブルバトル範囲技補正
    if is_double_spread:
        base_damage = int(base_damage * 0.75)
        
    # 2. 天候補正
    base_damage = int(base_damage * weather_multiplier)
    
    # 3. 急所補正
    if is_critical:
        base_damage = int(base_damage * 1.5)
    
    # 4. 乱数補正
    damage_list = []
    for r in range(85, 101):
        current_dmg = int(base_damage * r / 100)
    
        # 5. タイプ一致
        if is_stab:
            current_dmg = int(current_dmg * 1.5)
    
        # 6. タイプ相性
        current_dmg = int(current_dmg * type_multiplier)

        # 7. 物理技でやけど状態の場合の補正
        if is_burned_physical:
            current_dmg = int(current_dmg * 0.5)

        # 8. 壁のダメージ軽減
        current_dmg = int(current_dmg * wall_multiplier)
        
        damage_list.append(current_dmg)
    
    return damage_list[0], damage_list[-1], damage_list

# 3. 実行部分
if __name__ == "__main__":
    print("=== ポケモンチャンピオンズ ダメージ計算ソフト ===")
    
    # 1. 攻撃側の情報入力
    attacker_name = input("攻撃するポケモンを入力してください: ")
    if attacker_name not in POKEMON_DATA:
        print("そのポケモンは登録されていません。")
        exit()

    # 2. 防御側の情報入力
    defender_name = input("防御するポケモンを入力してください: ")
    if defender_name not in POKEMON_DATA:
        print("そのポケモンは登録されていません。")
        exit()

    # 3. 技の情報入力
    print("\n--- 技の情報を入力 ---")
    move_power = int(input("攻撃技の威力を入力してください（例: 100）: "))
    if move_power <= 0:
        print("威力は正の整数で入力してください。ソフトを終了します。")
        exit()

    move_type = input("攻撃技のタイプを入力してください（例: じめん）: ")
    if move_type not in TYPE_CHART:
        print("そのタイプは登録されていません。ソフトを終了します。")
        exit()
    
    print("技の分類を選んでください (1: 物理技 / 2: 特殊技)")
    move_category = input("番号を入力してください: ")
    
    if move_category == "1":
        atk_key = "A"
        def_key = "B"
        category_name = "物理"
        is_physical = True
    elif move_category == "2":
        atk_key = "C"
        def_key = "D"
        category_name = "特殊"
        is_physical = False
    else:
        print("無効な番号が入力されました。ソフトを終了します。")
        exit()
    
    # バトル形式の確認
    print("バトル形式を選んでください (1: シングル / 2: ダブル)")
    battle_format = input("番号を入力してください: ")
    is_double_battle = (battle_format == "2")
    
    # ダブル補正の確認
    is_double_spread = False
    if is_double_battle:
        print("ダブルバトルで相手複数に当たる範囲技（じしん、いわなだれ等）ですか？ (1: はい / 2: いいえ)")
        double_input = input("番号を入力してください: ")
        is_double_spread = (double_input == "1")
    
    # 天候の確認
    print("現在の天候を選んでください (1: 通常 / 2: 晴れ / 3: 雨)")
    weather_input = input("番号を入力してください: ")
    
    weather_multiplier = 1.0
    weather_name = "通常"

    if weather_input == "2":
        weather_name = "晴れ"
        if move_type == "ほのお":
            weather_multiplier = 1.5
        elif move_type == "みず":
            weather_multiplier = 0.5
    elif weather_input == "3":
        weather_name = "雨"
        if move_type == "みず":
            weather_multiplier = 1.5
        elif move_type == "ほのお":
            weather_multiplier = 0.5
            
    # 急所の確認
    print("急所に当たりましたか？ (1: はい / 2: いいえ)")
    crit_input = input("番号を入力してください: ")
    is_critical = (crit_input == "1")
    
    # タイプ一致の確認     
    attacker_types = POKEMON_DATA[attacker_name]["types"]
    is_stab = move_type in attacker_types
    if is_stab:
        print(f"\n※ 「{move_type}」タイプ一致ボーナス(1.5倍)が適用されます！")

    #タイプ相性の確認
    defender_types = POKEMON_DATA[defender_name]["types"]
    type_multiplier = 1.0
    for def_type in defender_types:
        if move_type in TYPE_CHART and def_type in TYPE_CHART[move_type]:
            type_multiplier *= TYPE_CHART[move_type][def_type]
        else:
            type_multiplier *= 1.0

    # 物理技でやけど状態の確認
    print("攻撃側はやけど状態ですか？ (1: はい / 2: いいえ)")
    burned_input = input("番号を入力してください: ")
    is_burned_physical = is_physical and (burned_input == "1")

    # 壁の確認
    is_wall = False
    wall_multiplier = 1.0
    if not is_critical:  # 急所補正がある場合、壁の補正は無視される
        print("壁（リフレクター / 光の壁）が張られていますか？ (1: はい / 2: いいえ)")
        wall_input = input("番号を入力してください: ")
        is_wall = (wall_input == "1")
        if is_wall:
            wall_multiplier = 2 / 3 if is_double_battle else 0.5

    # タイプ相性の表示        
    if type_multiplier > 1.0:
        print(f"※ 効果は ばつぐん だ！ (倍率: {type_multiplier})")
    elif type_multiplier == 0.0:
        print(f"※ 効果がないみたいだ… (倍率: {type_multiplier})")
    elif type_multiplier < 1.0:
        print(f"※ 効果は いまひとつ だ… (倍率: {type_multiplier})")
    
    # 特殊な補正メッセージの表示
    if is_double_spread:
        print("※ ダブルバトルの範囲技補正(0.75倍)が適用されます！")
    if weather_multiplier != 1.0:
        print(f"※ 天候「{weather_name}」による補正({weather_multiplier}倍)が適用されます！")    
    if is_critical:
        print("※急所に当たった！(1.5倍補正)が適用されます！")
    if is_burned_physical:
        print("※攻撃側はやけど状態のため、物理技の威力が半減します！(0.5倍補正)")
    if is_wall:
        wall_label = "ダブル" if is_double_battle else "シングル"
        print(f"※ 壁によるダメージ軽減({wall_label}で{wall_multiplier:.3g}倍)が適用されます！")

    # 4. 能力ポイント・性格補正の入力
    print(f"\n--- ステータス詳細を入力 ({category_name}想定) ---")
    a_point = int(input(f"{attacker_name}の{atk_key}(能力ポイント)を入力してください: "))
    a_nature = float(input(f"{attacker_name}の{atk_key}(性格補正)を入力してください（例: 1.1 / 1.0）: "))
    
    h_point = int(input(f"{defender_name}のH(能力ポイント)を入力してください: "))
    
    b_point = int(input(f"{defender_name}の{def_key}(能力ポイント)を入力してください: "))
    b_nature = float(input(f"{defender_name}の{def_key}(性格補正)を入力してください（例: 1.0）: "))

    print("\n--- 計算結果 ---")

    # 5. 計算の実行
    # 攻撃側の実数値
    attacker_base_stat = POKEMON_DATA[attacker_name][atk_key]
    attacker_real_stat = calculate_real_stat(atk_key, attacker_base_stat, a_point, a_nature)
    print(f"{attacker_name}の{atk_key}実数値: {attacker_real_stat}")

    # 防御側のHP実数値
    defender_base_h = POKEMON_DATA[defender_name]["H"]
    defender_real_h = calculate_real_stat("H", defender_base_h, h_point, 1.0)
    print(f"{defender_name}のHP実数値: {defender_real_h}")

    # 防御側の防御/特防実数値
    defender_base_stat = POKEMON_DATA[defender_name][def_key]
    defender_real_stat = calculate_real_stat(def_key, defender_base_stat, b_point, b_nature)
    print(f"{defender_name}の{def_key}実数値: {defender_real_stat}")

    # ダメージ計算
    min_dmg, max_dmg, all_damages = calculate_damage(
        attacker_real_stat,
        defender_real_stat,
        move_power,
        is_double_spread,
        weather_multiplier,
        is_critical,
        is_stab,
        type_multiplier,
        is_burned_physical,
        wall_multiplier,
    )
    print(f"ダメージ乱数幅: {min_dmg} ~ {max_dmg}")

    print(f"16段階のダメージ詳細: {all_damages}")

    # 割合計算
    if type_multiplier == 0.0:
        print(f"相手のHPに対する割合: 0.0% ~ 0.0%")
    else:
        min_percent = (min_dmg / defender_real_h) * 100
        max_percent = (max_dmg / defender_real_h) * 100
        print(f"相手のHPに対する割合: {min_percent:.1f}% ~ {max_percent:.1f}%")