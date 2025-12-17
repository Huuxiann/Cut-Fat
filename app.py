import streamlit as st
import math
import pandas as pd

# --- 核心算法类 (保持不变) ---
class FitnessCalculator:
    def __init__(self, gender, age, height_cm, weight_kg, neck_cm, waist_cm, hip_cm=0):
        self.gender = gender.lower()
        self.age = int(age)
        self.height = float(height_cm)
        self.weight = float(weight_kg)
        self.neck = float(neck_cm)
        self.waist = float(waist_cm)
        self.hip = float(hip_cm)

    def calculate_body_fat(self):
        if self.gender == 'male':
            bfp = 495 / (1.0324 - 0.19077 * math.log10(self.waist - self.neck) + 0.15456 * math.log10(self.height)) - 450
        else:
            bfp = 495 / (1.29579 - 0.35004 * math.log10(self.waist + self.hip - self.neck) + 0.22100 * math.log10(self.height)) - 450
        return round(bfp, 2)

    def calculate_bmr(self):
        base = (10 * self.weight) + (6.25 * self.height) - (5 * self.age)
        if self.gender == 'male':
            return base + 5
        else:
            return base - 161

    def calculate_tdee(self, activity_level_key):
        bmr = self.calculate_bmr()
        # 将下拉菜单的 key 映射回数值
        multipliers = {
            "Sedentary": 1.2,
            "Light": 1.375,
            "Moderate": 1.55,
            "Active": 1.725,
            "Extreme": 1.9
        }
        return round(bmr * multipliers.get(activity_level_key, 1.2))

    def nutrition_plan(self, tdee, goal):
        adjustments = {
            "减脂 (Cut)": 0.80,
            "维持 (Maintain)": 1.0,
            "增肌 (Bulk)": 1.10
        }
        
        target_calories = round(tdee * adjustments.get(goal, 1.0))
        protein_g = round(self.weight * 2.0)
        fat_g = round(self.weight * 0.8)
        
        consumed_cals = (protein_g * 4) + (fat_g * 9)
        remaining_cals = target_calories - consumed_cals
        
        if remaining_cals < 0:
            carbs_g = 50 
            target_calories = consumed_cals + (carbs_g * 4)
        else:
            carbs_g = round(remaining_cals / 4)

        return {
            "Calories": target_calories,
            "Protein": protein_g,
            "Fat": fat_g,
            "Carbs": carbs_g
        }

# --- Streamlit 页面布局 ---

st.set_page_config(page_title="健身营养计算器", page_icon="💪", layout="wide")

st.title("💪 科学健身：体脂与营养计算器")
st.markdown("基于 **US Navy Method** 和 **Mifflin-St Jeor** 公式")

# 侧边栏：输入区域
with st.sidebar:
    st.header("1. 输入身体数据")
    gender = st.radio("性别", ["Male", "Female"], horizontal=True)
    
    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("年龄", value=25, step=1)
        height = st.number_input("身高 (cm)", value=175.0, step=0.1)
    with col2:
        weight = st.number_input("体重 (kg)", value=70.0, step=0.1)
        neck = st.number_input("颈围 (cm)", value=38.0, step=0.1)
    
    waist = st.number_input("腰围 (cm)", value=80.0, step=0.1, help="肚脐水平线测量")
    
    hip = 0.0
    if gender == "Female":
        hip = st.number_input("臀围 (cm)", value=95.0, step=0.1, help="臀部最宽处测量")

    st.markdown("---")
    st.header("2. 设置活动与目标")
    
    activity_map = {
        "久坐 (办公室/几乎不运动)": "Sedentary",
        "轻度活跃 (每周运动 1-3 天)": "Light",
        "中度活跃 (每周运动 3-5 天)": "Moderate",
        "高度活跃 (每周运动 6-7 天)": "Active",
        "极度活跃 (体力工作/双倍训练)": "Extreme"
    }
    activity_label = st.selectbox("日常活动水平", list(activity_map.keys()))
    activity_key = activity_map[activity_label]

    goal = st.selectbox("当前目标", ["减脂 (Cut)", "维持 (Maintain)", "增肌 (Bulk)"])
    
    calculate_btn = st.button("开始计算", type="primary")

# 主界面：显示结果
if calculate_btn:
    # 实例化计算器
    calc = FitnessCalculator(gender, age, height, weight, neck, waist, hip)
    
    # 计算核心数据
    try:
        bfp = calc.calculate_body_fat()
        tdee = calc.calculate_tdee(activity_key)
        plan = calc.nutrition_plan(tdee, goal)

        # 1. 顶部指标栏
        st.subheader("📊 你的身体指标")
        col_m1, col_m2, col_m3 = st.columns(3)
        col_m1.metric("体脂率 (Body Fat)", f"{bfp}%")
        col_m2.metric("每日总消耗 (TDEE)", f"{tdee} kcal")
        col_m3.metric("推荐摄入热量", f"{plan['Calories']} kcal", delta=f"{plan['Calories'] - tdee} kcal")

        st.markdown("---")

        # 2. 营养分配详情
        st.subheader(f"🥗 每日饮食建议：{goal}")
        
        # 准备图表数据
        macro_data = pd.DataFrame({
            '营养素': ['蛋白质 (Protein)', '脂肪 (Fat)', '碳水 (Carbs)'],
            '重量 (g)': [plan['Protein'], plan['Fat'], plan['Carbs']],
            '热量占比': [plan['Protein']*4, plan['Fat']*9, plan['Carbs']*4] # 粗略估算用于饼图
        })

        # 两列布局：左边文字详情，右边饼图
        c1, c2 = st.columns([1, 1])
        
        with c1:
            st.info("💡 **分配策略：** \n- 蛋白质: 2g/kg (保护肌肉)\n- 脂肪: 0.8g/kg (激素健康)\n- 碳水: 填充剩余热量")
            st.dataframe(
                macro_data[['营养素', '重量 (g)']], 
                hide_index=True, 
                use_container_width=True
            )
            
        with c2:
            st.bar_chart(
                macro_data, 
                x='营养素', 
                y='重量 (g)', 
                color='营养素',
                use_container_width=True
            )

    except ValueError:
        st.error("输入数据有误，请确保所有数值合理（例如腰围不能小于颈围）。")
else:
    # 初始欢迎界面
    st.info("👈 请在左侧侧边栏输入数据并点击“开始计算”")