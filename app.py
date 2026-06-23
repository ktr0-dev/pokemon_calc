import streamlit as st
import json
import pandas as pd

# 1. データ定義
@st.cache_data  # 毎回JSONを読み直さないようにキャッシュ化
def load_data():
    with open("pokemon_data.json", "r", encoding="utf-8") as f:
        pokemon_data = json.load(f)
    with open("type_chart.json", "r", encoding="utf-8") as f:
        type_chart = json.load(f)
    return pokemon_data, type_chart

POKEMON_DATA, TYPE_CHART = load_data()

# 2. 処理
def calculate_real_stat(stat_type, base_stat, ability_point, nature_multiplier):
    if stat_type == "H":
        return int((base_stat * 2 + 31) * 50 / 100) + 50 + 10 + ability_point
    else:
        return int((int((base_stat * 2 + 31) * 50 / 100) + 5 + ability_point) * nature_multiplier)

def calculate_damage(attacker_stat, defender_stat, move_power, is_double_spread, weather_multiplier, is_critical, is_stab, type_multiplier, is_burned_physical, wall_multiplier, item_multiplier):
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

        # 9. アイテム補正
        current_dmg = int(current_dmg * item_multiplier)
        
        damage_list.append(current_dmg)
    
    return damage_list[0], damage_list[-1], damage_list

def calculate_required_hits(all_damages, defender_hp, type_multiplier):

    if type_multiplier == 0.0:
        return "技が無効なため、倒すことはできません。"
        
    min_dmg = all_damages[0]
    max_dmg = all_damages[-1]
    
    # 1. 確定1発 / 乱数1発の計算
    ohko_count = sum(1 for d in all_damages if d >= defender_hp)
    ohko_probability = (ohko_count / 16) * 100

    if min_dmg >= defender_hp:
        return "確定 1 発（100%の確率でひんし）"
    elif max_dmg >= defender_hp:
        return f"乱数 1 発（{ohko_probability:.1f}% の確率でひんし）"
        
    # 2. 乱数2発 / 確定2発の計算
    min_dmg_2hits = min_dmg * 2
    max_dmg_2hits = max_dmg * 2
    
    if min_dmg_2hits >= defender_hp:
        return "確定 2 発"
    elif max_dmg_2hits >= defender_hp:
        # 2発の組み合わせ（256通り）
        two_hits_count = 0
        for d1 in all_damages:
            for d2 in all_damages:
                if d1 + d2 >= defender_hp:
                    two_hits_count += 1
        two_hits_probability = (two_hits_count / 256) * 100
        return f"乱数 2 発（{two_hits_probability:.1f}% の確率でひんし）"
        
    # 3. 3発目以降の概算
    min_hits = (defender_hp + max_dmg - 1) // max_dmg
    max_hits = (defender_hp + min_dmg - 1) // min_dmg
    
    if min_hits == max_hits:
        return f"確定 {min_hits} 発"
    else:
        return f"乱数 {min_hits} 発 〜 確定 {max_hits} 発"


# --- 画面の構築 (UI) ---
st.title("=== ポケモンチャンピオンズ ダメージ計算ソフト ===")

tab1, tab2 = st.tabs(["ダメージ計算", "素早さ・ダメージ一覧（将来用）"])

with tab1:
    st.header("条件入力")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("攻撃側")
        attacker_name = st.selectbox("ポケモンを選択", list(POKEMON_DATA.keys()), key="atk")
        # ここに攻撃側の努力値スライダーなどを配置
        a_point = st.slider("能力ポイント(努力値)", 0, 252, 0, step=4, key="atk_p")
        a_nature = st.radio("性格補正", [1.1, 1.0, 0.9], index=1, key="atk_n")

    with col2:
        st.subheader("防御側")
        defender_name = st.selectbox("ポケモンを選択", list(POKEMON_DATA.keys()), key="def")
        # ここに防御側の努力値スライダーなどを配置
        h_point = st.slider("HP能力ポイント", 0, 252, 0, step=4, key="def_hp")

    st.subheader("技の情報")
    move_power = st.number_input("技の威力", min_value=1, max_value=250, value=100)
    move_type = st.selectbox("技のタイプ", list(TYPE_CHART.keys()))
    
    # 計算実行ボタン
    if st.button("ダメージを計算する"):
        # ここで calculate_damage や calculate_required_hits を呼び出す
        # 結果を st.write() や st.success() で表示
        st.success("計算結果がここに表示されます！")

with tab2:
    st.header("登録チームの一覧・早見表")
    st.info("ここに将来、12体の素早さ順ソート表（pd.DataFrameを活用）などを表示させます！")