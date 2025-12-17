import streamlit as st
import math
import pandas as pd
from datetime import datetime, timedelta

# --- 核心算法类 (集成了所有功能) ---
class FitnessCalculator:
    def __init__(self, gender, age, height_cm, weight_kg, neck_cm, waist_cm, hip_cm=0):
        self.gender = gender.lower()
        self.age = int(age)
        self.height = float(height_cm)
        self.weight = float(weight_kg)
        self.neck = float(neck_cm)
        self.waist = float(waist_cm)
        self.hip = float(hip_cm)

    # 1. 体脂率计算 (美国海军法)
    def calculate_body_fat(self):
        if self.gender == 'male':
            bfp = 495 / (1.0324 - 0.19077 * math.log10(self.waist - self.neck) + 0.15456 * math.log10(self.height)) - 450
        else:
            bfp = 495 / (1.29579 - 0.35004 * math.log10(self.waist + self.hip - self.neck) + 0.22100 * math.log10(self.height)) - 450
        return round(bfp, 2)

    # 2. 基础代谢 (BMR)
    def calculate_bmr(self):
        base = (10 * self.weight) + (6.25 * self.height) - (5 * self.age)
        if self.gender == 'male':
            return base + 5
        else:
            return base - 161

    # 3. TDEE 计算
    def calculate_tdee(self, activity_key):
        bmr = self.calculate_bmr()
        multipliers = {"Sedentary": 1.2, "Light": 1.375, "Moderate": 1.55, "Active": 1.725, "Extreme": 1.9}
        return round(bmr * multipliers.get(activity_key, 1.2))

    # 4. 营养分配
    def nutrition_plan(self, tdee, goal_key):
        adjustments = {"Cut": 0.80, "Maintain": 1.0, "Bulk": 1.10}
        target = round(tdee * adjustments.get(goal_key, 1.0))
        
        # 蛋白质 2g/kg, 脂肪 0.8g/kg
        protein = round(self.weight * 2.0)
        fat = round(self.weight * 0.8)
        
        consumed = (protein * 4) + (fat * 9)
        carbs = round((target - consumed) / 4)
        if carbs < 0: carbs = 50 # 保底

        return {"Cal": target, "Pro": protein, "Fat": fat, "Carb": carbs}

    # 5. BMI 计算
    def calculate_bmi(self):
        h_m = self.height / 100
        return round(self.weight / (h_m ** 2), 1)

    # 6. 1RM 力量计算 (静态方法，不需要身高体重)
    @staticmethod
    def calculate_1rm(lift_weight, reps):
        if reps == 1: return lift_weight
        return round(lift_weight * (1 + reps / 30), 1)

    # 7. 睡眠周期 (静态方法)
    @staticmethod
    def calculate_sleep(wake_time):
        now = datetime.now()
        wake_dt = datetime.combine(now.date(), wake_time)
        if wake_dt < now: wake_dt += timedelta(days=1)
        
        cycles = [4, 5, 6]
        bedtimes = []
        for c in cycles:
            minutes_needed = (c * 90) + 15
            bed_dt = wake_dt - timedelta(minutes=minutes_needed)
            bedtimes.append({"cycles": c, "dur": f"{c * 1.5}h", "time": bed_dt.strftime("%H:%M")})
        return bedtimes

# --- 页面 UI ---
st.set_page_config(page_title="全能健身助手 v3.0", page_icon="💪", layout="wide")

st.title("💪 全能健身助手 v3.0")

# --- 侧边栏：公共输入区域 ---
with st.sidebar:
    st.header("📝 个人数据录入")
    st.info("在这里输入数据，所有功能都会自动使用！")
    
    gender = st.radio("性别", ["Male", "Female"], horizontal=True)
    
    # 修复版：显式指定 min_value 和 value
    age = st.number_input("年龄", min_value=10, max_value=100, value=25)
    
    height = st.number_input("身高 (cm)", min_value=100.0, max_value=250.0, value=175.0)
    
    weight = st.number_input("体重 (kg)", min_value=30.0, max_value=200.0, value=70.0)
    
    st.markdown("---")
    st.markdown("**体脂测量数据:**")
    
    neck = st.number_input("颈围 (cm)", min_value=20.0, max_value=60.0, value=38.0)
    
    waist = st.number_input("腰围 (cm)", min_value=40.0, max_value=150.0, value=80.0, help="肚脐处水平测量")
    
    hip = 0.0
    if gender == "Female":
        hip = st.number_input("臀围 (cm)", min_value=50.0, max_value=150.0, value=95.0, help="臀部最宽处")

    # 实例化计算器
    user = FitnessCalculator(gender, age, height, weight, neck, waist, hip)

# --- 主界面：标签页 ---
tab1, tab2, tab3, tab4 = st.tabs(["📊 体脂与饮食", "🛌 睡眠 (REM)", "🏋️‍♂️ 力量 (1RM)", "⚖️ BMI检测"])

# === Tab 1: 体脂与饮食 ===
with tab1:
    col_input1, col_input2 = st.columns(2)
    with col_input1:
        activity_label = st.selectbox("日常活动", ["久坐 (Sedentary)", "轻度 (Light)", "中度 (Moderate)", "高度 (Active)", "极度 (Extreme)"])
        activity_key = activity_label.split("(")[1].replace(")", "")
    with col_input2:
        goal_label = st.selectbox("目标", ["减脂 (Cut)", "维持 (Maintain)", "增肌 (Bulk)"])
        goal_key = goal_label.split("(")[1].replace(")", "")
    
    if st.button("开始计算身体数据", type="primary"):
        # 计算
        bfp = user.calculate_body_fat()
        tdee = user.calculate_tdee(activity_key)
        plan = user.nutrition_plan(tdee, goal_key)
        
        # 显示结果
        st.divider()
        c1, c2, c3 = st.columns(3)
        c1.metric("体脂率 (BFP)", f"{bfp}%")
        c2.metric("每日消耗 (TDEE)", f"{tdee} kcal")
        c3.metric("目标热量", f"{plan['Cal']} kcal", delta=f"{plan['Cal'] - tdee} kcal")
        
        st.subheader("🥗 宏量营养素建议")
        macro_df = pd.DataFrame({
            "营养素": ["蛋白质", "脂肪", "碳水"],
            "克重 (g)": [plan['Pro'], plan['Fat'], plan['Carb']]
        })
        st.bar_chart(macro_df, x="营养素", y="克重 (g)")

# === Tab 2: 睡眠周期 ===
with tab2:
    st.markdown("### 🛌 倒推最佳入睡时间")
    wake_time = st.time_input("我想几点起床？", datetime.strptime("07:00", "%H:%M").time())
    
    if st.button("计算睡眠时间"):
        results = user.calculate_sleep(wake_time)
        cols = st.columns(3)
        for i, res in enumerate(results):
            cols[i].metric(f"睡 {res['dur']}", res['time'], f"{res['cycles']}个周期")

# === Tab 3: 1RM 力量 ===
with tab3:
    st.markdown("### 🏋️‍♂️ 估算极限力量 (1RM)")
    c1, c2 = st.columns(2)
    w = c1.number_input("训练重量 (kg)", 60.0)
    r = c2.number_input("重复次数 (Reps)", 8)
    
    if st.button("计算 1RM"):
        one_rm = user.calculate_1rm(w, r)
        st.metric("你的 1RM 估算", f"{one_rm} kg")
        st.info(f"建议训练组 (80%强度): {round(one_rm*0.8, 1)} kg x 8-10 次")

# === Tab 4: BMI ===
with tab4:
    st.markdown("### ⚖️ BMI 健康简测")
    bmi = user.calculate_bmi()
    
    st.metric("当前 BMI", bmi)
    
    if bmi < 18.5:
        st.warning("状态：偏瘦 (Underweight)")
    elif 18.5 <= bmi < 24.9:
        st.success("状态：正常 (Normal)")
    elif 25 <= bmi < 29.9:
        st.warning("状态：超重 (Overweight)")
    else:
        st.error("状态：肥胖 (Obese)")


