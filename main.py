import json

# 1. データ定義
def load_pokemon_data(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)

POKEMON_DATA = load_pokemon_data("pokemon_data.json")

# 2. 処理
def calculate_real_stat(stat_type, base_stat, ability_point, nature_multiplier):
    if stat_type == "H":
        return int((base_stat * 2 + 31) * 50 / 100) + 50 + 10 + ability_point
    else:
        return int((int((base_stat * 2 + 31) * 50 / 100) + 5 + ability_point) * nature_multiplier)

def calculate_damage(attacker_stat, defender_stat, move_power):
    base_damage = int((int(2 * 50 / 5 + 2) * move_power * attacker_stat / defender_stat / 50) + 2)
    
    min_damage = int(base_damage * 0.85)
    max_damage = int(base_damage * 1.0)
    
    return min_damage, max_damage

# 3. 実行部分
if __name__ == "__main__":
    print("=== ポケモンチャンピオンズ ダメージ計算ソフト ===")
    
    
    # 情報入力
    # 攻撃側の情報入力
    attacker_name = input("攻撃するポケモンを入力してください: ")
    if attacker_name not in POKEMON_DATA:
        print("そのポケモンは登録されていません。ソフトを終了します。")
        exit()
    a_point = int(input(f"{attacker_name}の攻撃の能力ポイントを入力してください: "))
    a_nature = float(input(f"{attacker_name}の攻撃の性格補正を入力してください: "))
    
    # 防御側の情報入力
    defender_name = input("防御するポケモンを入力してください: ")
    if defender_name not in POKEMON_DATA:
        print("そのポケモンは登録されていません。ソフトを終了します。")
        exit()
    h_point = int(input(f"{defender_name}のHPの能力ポイントを入力してください: "))
    b_point = int(input(f"{defender_name}の防御の能力ポイントを入力してください: "))
    b_nature = float(input(f"{defender_name}の防御の性格補正を入力してください: "))
    
    # 技の情報入力
    move_power = int(input("攻撃技の威力を入力してください: "))
    
    
    print("\n--- 計算結果 ---")
    
    
    # 各種計算
    # 攻撃側の実数値
    attacker_base_a = POKEMON_DATA[attacker_name]["A"]
    attacker_real_a = calculate_real_stat("A", attacker_base_a, a_point, a_nature)
    print(f"{attacker_name}の攻撃実数値: {attacker_real_a}")
    
    # 防御側の実数値
    defender_base_h = POKEMON_DATA[defender_name]["H"]
    defender_real_h = calculate_real_stat("H", defender_base_h, h_point, 1.0)
    print(f"{defender_name}のHP実数値: {defender_real_h}")
    defender_base_b = POKEMON_DATA[defender_name]["B"]
    defender_real_b = calculate_real_stat("B", defender_base_b, b_point, b_nature)
    print(f"{defender_name}の防御実数値: {defender_real_b}")
    
    # ダメージ計算
    min_dmg, max_dmg = calculate_damage(attacker_real_a, defender_base_b, move_power)
    print(f"ダメージ乱数幅: {min_dmg} ~ {max_dmg}")
    
    # 割合計算
    min_percent = (min_dmg / defender_real_h) * 100
    max_percent = (max_dmg / defender_real_h) * 100
    print(f"相手のHPに対する割合: {min_percent:.1f}% ~ {max_percent:1f}%")
    