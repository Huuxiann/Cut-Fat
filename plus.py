import streamlit as st
import random
import time

# --- 页面配置 ---
st.set_page_config(
    page_title="开启你的2026",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 状态管理 ---
if 'page' not in st.session_state:
    st.session_state.page = 'landing'  # 初始状态：landing (落地页) 或 animation (动画页)

if 'generated_words' not in st.session_state:
    st.session_state.generated_words = [] # 存储随机生成的词，避免刷新变动

# --- 古风词库 (100词) ---
GUFENG_WORDS = [
    "岁岁平安", "喜乐无忧", "前程似锦", "万事胜意", "吉吉利利", "百无禁忌", "长安", "常安", "长乐", "未央",
    "鸿鹄之志", "扶摇直上", "星河长明", "因为有你", "未来可期", "顺遂", "无虞", "清欢", "热烈", "如愿",
    "锦瑟", "华年", "朝暮", "安康", "多喜", "乐多", "顺意", "得偿", "所愿", "花开",
    "富贵", "荣华", "且喜", "且乐", "且宁", "且安", "不负", "韶华", "只争", "朝夕",
    "春风", "得意", "马蹄", "疾", "一日", "看尽", "长安花", "明月", "清风", "入怀",
    "山河", "远阔", "人间", "烟火", "星辰", "大海", "熠熠", "生辉", "光芒", "万丈",
    "温柔", "坚定", "勇敢", "自由", "赤诚", "善良", "可爱", "浪漫", "至死", "不渝",
    "天官", "赐福", "百病", "不侵", "诸邪", "退散", "招财", "进宝", "日进", "斗金",
    "风生", "水起", "步步", "高升", "平步", "青云", "鱼跃", "龙门", "金榜", "题名",
    "心想", "事成", "美梦", "成真", "笑口", "常开", "福如", "东海", "寿比", "南山"
]

# --- CSS 样式注入 ---
# 这里包含了所有的视觉魔法：背景切换、按钮样式、文字动画
def local_css(page_type):
    if page_type == 'landing':
        # 温暖背景 CSS
        bg_style = """
        <style>
            .stApp {
                background: linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%);
                background-image: linear-gradient(to top, #fad0c4 0%, #ffd1ff 100%);
            }
            /* 隐藏默认的header和footer */
            header {visibility: hidden;}
            footer {visibility: hidden;}
            
            /* 圆形按钮容器 */
            .btn-container {
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                height: 70vh;
            }
            
            /* 自定义按钮样式 */
            div.stButton > button {
                width: 200px;
                height: 200px;
                border-radius: 50%;
                background: linear-gradient(45deg, #ff9a9e 0%, #fecfef 99%, #fecfef 100%);
                color: white;
                font-size: 24px;
                font-weight: bold;
                border: none;
                box-shadow: 0 10px 20px rgba(0,0,0,0.1);
                transition: all 0.3s ease;
                animation: pulse 2s infinite;
            }
            
            div.stButton > button:hover {
                transform: scale(1.05);
                box-shadow: 0 15px 30px rgba(0,0,0,0.2);
                background: linear-gradient(45deg, #fecfef 0%, #ff9a9e 100%);
                border-color: transparent;
            }
            
            div.stButton > button:active {
                background-color: #ff6b6b;
                color: white;
            }

            /* 按钮下方的备注文字 */
            .sub-text {
                margin-top: 20px;
                color: #555;
                font-family: 'Helvetica Neue', sans-serif;
                font-size: 16px;
                letter-spacing: 2px;
                text-align: center;
            }

            @keyframes pulse {
                0% { box-shadow: 0 0 0 0 rgba(255, 154, 158, 0.4); }
                70% { box-shadow: 0 0 0 20px rgba(255, 154, 158, 0); }
                100% { box-shadow: 0 0 0 0 rgba(255, 154, 158, 0); }
            }
        </style>
        """
    else:
        # 黑色背景 CSS
        bg_style = """
        <style>
            .stApp {
                background-color: #000000;
            }
            header {visibility: hidden;}
            footer {visibility: hidden;}
            
            /* 中心金色文字 */
            .main-title {
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                color: #FFD700;
                font-size: 3em;
                font-weight: bold;
                text-shadow: 0 0 10px #FFD700, 0 0 20px #FF8C00;
                z-index: 100;
                white-space: nowrap;
                animation: fadeIn 3s ease-in;
            }

            /* 浮动文字的基础样式 */
            .floating-word {
                position: absolute;
                color: rgba(255, 255, 255, 0.8);
                font-family: "KaiTi", "STKaiti", serif; /* 楷体更有古风感 */
                user-select: none;
                animation-name: floatIn;
                animation-fill-mode: forwards;
                opacity: 0;
            }

            @keyframes fadeIn {
                0% { opacity: 0; transform: translate(-50%, -50%) scale(0.8); }
                100% { opacity: 1; transform: translate(-50%, -50%) scale(1); }
            }

            /* 从远处(小)飘向近处(大)或者直接淡入 */
            @keyframes floatIn {
                0% { opacity: 0; transform: scale(0.1) translateY(20px); filter: blur(4px);}
                100% { opacity: 0.8; transform: scale(1) translateY(0); filter: blur(0px);}
            }
            
            /* 返回按钮微调 */
            div.stButton > button {
                background-color: transparent;
                border: 1px solid #333;
                color: #333;
                margin-top: 20px;
            }
        </style>
        """
    st.markdown(bg_style, unsafe_allow_html=True)

# --- 页面 1: 入口 (Landing Page) ---
def landing_page():
    local_css("landing")
    
    # 使用 Streamlit 的列布局来居中内容
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<div style="height: 30vh;"></div>', unsafe_allow_html=True) # 占位符
        
        # 按钮容器
        # 注意: Streamlit 的 button 无法直接包裹 div，所以我们用 CSS hack 了它的外观
        # 这里的 key 很重要
        clicked = st.button("开启2026")
        
        st.markdown('<div class="sub-text">点击开启你的2026</div>', unsafe_allow_html=True)
        
        if clicked:
            st.session_state.page = 'animation'
            st.rerun()

# --- 页面 2: 动画展示 (Animation Page) ---
def animation_page():
    local_css("animation")
    
    # 1. 渲染中心金色文字
    st.markdown('<div class="main-title">希望2026年的你…</div>', unsafe_allow_html=True)
    
    # 2. 生成随机古风词汇
    # 我们只在第一次进入这个页面时生成位置，防止Streamlit刷新导致跳动
    if not st.session_state.generated_words:
        selected_words = random.sample(GUFENG_WORDS, 35) # 选取35个词展示，防止太拥挤
        
        html_elements = []
        for word in selected_words:
            # 随机位置 (使用 vw/vh 视口单位)
            top = random.randint(5, 90)
            left = random.randint(5, 90)
            
            # 避让中心区域 (大概范围 40-60%)
            if 35 < top < 65 and 30 < left < 70:
                continue
                
            # 随机大小 (模拟远近)
            # 大字体 = 近 (opacity高, blur少)
            # 小字体 = 远 (opacity低, blur多)
            size = random.randint(12, 40)
            
            # 随机动画延迟，制造先后浮现的效果
            delay = random.uniform(0.5, 4.0)
            
            # 根据大小计算透明度
            opacity = min(0.3 + (size / 50), 0.9)
            
            element = f"""
            <div class="floating-word" style="
                top: {top}vh; 
                left: {left}vw; 
                font-size: {size}px; 
                animation-duration: 3s;
                animation-delay: {delay}s;
                opacity: {opacity};
            ">{word}</div>
            """
            html_elements.append(element)
        
        st.session_state.generated_words = "\n".join(html_elements)

    # 3. 渲染背景漂浮词汇
    st.markdown(st.session_state.generated_words, unsafe_allow_html=True)
    
    # 4. (可选) 一个隐藏的重置按钮，或者只是单纯展示
    # 为了保持纯净的黑色背景体验，我们通常不放其他控件。
    # 如果想重置，可以刷新网页。

# --- 主程序入口 ---
def main():
    if st.session_state.page == 'landing':
        landing_page()
    else:
        animation_page()

if __name__ == "__main__":
    main()
