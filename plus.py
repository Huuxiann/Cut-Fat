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
def local_css(page_type):
    if page_type == 'landing':
        # 温暖背景 CSS (保持原样，微调按钮质感)
        bg_style = """
        <style>
            .stApp {
                background: linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%);
                background-image: linear-gradient(to top, #fad0c4 0%, #ffd1ff 100%);
            }
            header, footer {visibility: hidden;}
            
            .btn-container {
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                height: 70vh;
            }
            
            div.stButton > button {
                width: 200px;
                height: 200px;
                border-radius: 50%;
                background: linear-gradient(45deg, #ff9a9e 0%, #fecfef 99%, #fecfef 100%);
                color: white;
                font-size: 26px;
                font-weight: bold;
                border: none;
                box-shadow: 0 10px 30px rgba(255, 107, 107, 0.4);
                transition: all 0.3s ease;
                animation: pulse 2s infinite;
                text-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            
            div.stButton > button:hover {
                transform: scale(1.08);
                box-shadow: 0 15px 40px rgba(255, 107, 107, 0.6);
                background: linear-gradient(45deg, #fecfef 0%, #ff9a9e 100%);
            }

            .sub-text {
                margin-top: 25px;
                color: #777;
                font-family: 'Helvetica Neue', sans-serif;
                font-size: 16px;
                letter-spacing: 3px;
                text-align: center;
                opacity: 0.8;
                animation: fadeInOut 3s infinite;
            }

            @keyframes pulse {
                0% { box-shadow: 0 0 0 0 rgba(255, 154, 158, 0.6); }
                70% { box-shadow: 0 0 0 25px rgba(255, 154, 158, 0); }
                100% { box-shadow: 0 0 0 0 rgba(255, 154, 158, 0); }
            }

            @keyframes fadeInOut {
                0%, 100% { opacity: 0.5; }
                50% { opacity: 1; }
            }
        </style>
        """
    else:
        # 黑色背景 CSS + 星空特效 + 流光文字
        bg_style = """
        <style>
            .stApp {
                background-color: #000000;
                /* 模拟星空背景 */
                background-image: 
                    radial-gradient(white, rgba(255,255,255,.2) 2px, transparent 3px),
                    radial-gradient(white, rgba(255,255,255,.15) 1px, transparent 2px),
                    radial-gradient(white, rgba(255,255,255,.1) 2px, transparent 3px);
                background-size: 550px 550px, 350px 350px, 250px 250px;
                background-position: 0 0, 40px 60px, 130px 270px;
                animation: starMove 100s linear infinite;
            }
            
            @keyframes starMove {
                from {background-position: 0 0, 40px 60px, 130px 270px;}
                to {background-position: 550px 550px, 390px 410px, 680px 820px;}
            }

            header, footer {visibility: hidden;}
            
            /* 中心金色文字 - 增加流光渐变效果 */
            .main-title {
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                font-size: 3.5em;
                font-weight: 900;
                background: linear-gradient(45deg, #FFD700, #FDB931, #FFFFE0, #FDB931, #FFD700);
                background-size: 200% auto;
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                text-shadow: 0 0 30px rgba(253, 185, 49, 0.3);
                z-index: 100;
                white-space: nowrap;
                animation: shine 3s linear infinite, popIn 1.5s ease-out;
            }

            @keyframes shine {
                to { background-position: 200% center; }
            }

            @keyframes popIn {
                0% { opacity: 0; transform: translate(-50%, -50%) scale(0.5); filter: blur(10px); }
                100% { opacity: 1; transform: translate(-50%, -50%) scale(1); filter: blur(0px); }
            }

            /* 浮动文字 */
            .floating-word {
                position: absolute;
                color: rgba(255, 255, 255, 0.9);
                font-family: "KaiTi", "STKaiti", "SimSun", serif; 
                user-select: none;
                opacity: 0;
                text-shadow: 0 0 5px rgba(255,255,255,0.3);
                animation: floatIn 4s ease-out forwards, drift 6s ease-in-out infinite alternate;
            }

            /* 出现动画 */
            @keyframes floatIn {
                0% { opacity: 0; transform: scale(0) translateY(50px); filter: blur(5px);}
                100% { opacity: var(--final-opacity); transform: scale(1) translateY(0); filter: blur(0px);}
            }

            /* 持续漂浮动画 */
            @keyframes drift {
                0% { transform: translateY(0px); }
                100% { transform: translateY(-10px); }
            }
            
            div.stButton > button {
                border: 1px solid #444;
                color: #666;
            }
        </style>
        """
    st.markdown(bg_style, unsafe_allow_html=True)

# --- 页面 1: 入口 (Landing Page) ---
def landing_page():
    local_css("landing")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<div style="height: 30vh;"></div>', unsafe_allow_html=True)
        
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
    if not st.session_state.generated_words:
        selected_words = random.sample(GUFENG_WORDS, 40) # 稍微增加数量到40
        
        html_elements = []
        for word in selected_words:
            top = random.randint(5, 90)
            left = random.randint(5, 90)
            
            # 避让中心区域 (加宽避让范围)
            if 30 < top < 70 and 20 < left < 80:
                continue
                
            size = random.randint(14, 38)
            delay = random.uniform(0.2, 3.5)
            # 计算透明度，并作为 CSS 变量传入，方便动画使用
            opacity = min(0.4 + (size / 60), 0.95)
            
            element = f"""
            <div class="floating-word" style="
                top: {top}vh; 
                left: {left}vw; 
                font-size: {size}px; 
                animation-delay: {delay}s;
                --final-opacity: {opacity};
            ">{word}</div>
            """
            html_elements.append(element)
        
        st.session_state.generated_words = "\n".join(html_elements)

    # 3. 渲染
    st.markdown(st.session_state.generated_words, unsafe_allow_html=True)

# --- 主程序入口 ---
def main():
    if st.session_state.page == 'landing':
        landing_page()
    else:
        animation_page()

if __name__ == "__main__":
    main()
