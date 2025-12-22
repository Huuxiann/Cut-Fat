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

# --- 背景音乐链接 (关键修改) ---
# 使用 raw.githack.com 代理以获取正确的 Content-Type (audio/flac)，解决浏览器不播放的问题
BGM_URL = "https://raw.githack.com/Huuxiann/Cut-Fat/main/%E5%9C%A8%E8%99%9A%E6%97%A0%E4%B8%AD%E6%B0%B8%E5%AD%98%20-%20%E8%8B%B1%E9%9B%84%E4%B8%BB%E4%B9%89.flac"

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

# --- 播放背景音乐函数 (更稳定的原生方案) ---
def play_bgm():
    # 使用 Streamlit 原生音频组件，隐藏它但保持自动播放
    # 注意：某些浏览器(如Chrome)如果用户没有交互，依然会拦截自动播放。
    # 点击首页的"开启"按钮通常算作一次交互，所以进入第二页后应该能自动播放。
    
    # 隐藏原生播放器的 CSS
    st.markdown("""
        <style>
            audio { display: none; }
        </style>
    """, unsafe_allow_html=True)
    
    # 渲染音频，autoplay=True 是 Streamlit 1.33+ 的特性，如果报错请升级 streamlit
    # 如果版本较低，它可能不会自动播放，但至少文件加载是正确的
    st.audio(BGM_URL, format="audio/flac", start_time=0, autoplay=True)

    # 备用的右上角手动开关 (保留以防自动播放彻底失败)
    st.markdown(f"""
    <!-- 音乐控制悬浮按钮 (纯 JS 控制原生 audio 标签的备份方案) -->
    <div id="music_btn" onclick="document.querySelector('audio').paused ? document.querySelector('audio').play() : document.querySelector('audio').pause()" style="
        position: fixed; 
        top: 20px; 
        right: 20px; 
        z-index: 99999; 
        cursor: pointer; 
        width: 40px; 
        height: 40px;
        line-height: 40px;
        text-align: center;
        border-radius: 50%;
        background: rgba(255,255,255,0.2);
        backdrop-filter: blur(4px);
        font-size: 20px;
        color: white;
        transition: all 0.3s;
        user-select: none;
    " title="点击播放/暂停">
        🎵
    </div>
    """, unsafe_allow_html=True)

# --- CSS 样式注入 ---
def local_css(page_type):
    # 通用重置样式
    reset_style = """
    <style>
        .block-container {
            padding-top: 0rem !important;
            padding-bottom: 0rem !important;
            padding-left: 0rem !important;
            padding-right: 0rem !important;
            max-width: 100% !important;
        }
        [data-testid="stHeader"], [data-testid="stToolbar"] {
            display: none;
        }
    </style>
    """
    st.markdown(reset_style, unsafe_allow_html=True)

    if page_type == 'landing':
        # 温暖背景 CSS + 强制居中样式
        bg_style = """
        <style>
            .stApp {
                background: linear-gradient(135deg, #FFF6B7 0%, #F6416C 100%);
            }
            
            /* 强制定位按钮容器：屏幕正中心 */
            div.stButton {
                position: fixed;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                z-index: 999;
                width: auto !important;
            }
            
            /* 按钮样式优化 */
            div.stButton > button {
                width: 180px;
                height: 180px;
                border-radius: 50%;
                background: rgba(255, 255, 255, 0.25);
                backdrop-filter: blur(10px);
                border: 2px solid rgba(255, 255, 255, 0.6);
                color: white;
                font-size: 24px;
                font-weight: 600;
                box-shadow: 0 0 20px rgba(255,255,255,0.3);
                transition: all 0.3s ease;
                position: relative;
                overflow: visible;
                animation: floatBtn 3s ease-in-out infinite;
                display: block;
            }
            
            /* 涟漪效果 */
            div.stButton > button::before {
                content: '';
                position: absolute;
                top: 50%; left: 50%;
                transform: translate(-50%, -50%);
                width: 100%; height: 100%;
                border-radius: 50%;
                border: 2px solid rgba(255, 255, 255, 0.5);
                animation: ripple 2s infinite;
                z-index: -1;
            }
            
            div.stButton > button:hover {
                transform: scale(1.1);
                background: rgba(255, 255, 255, 0.4);
                color: #fff;
                border-color: #fff;
            }

            /* 备注文字强制定位：按钮下方 */
            .sub-text {
                position: fixed;
                top: 50%;
                left: 50%;
                transform: translate(-50%, calc(-50% + 140px));
                color: rgba(255,255,255,0.95);
                font-family: 'Helvetica Neue', sans-serif;
                font-size: 16px;
                letter-spacing: 4px;
                text-align: center;
                text-shadow: 0 2px 4px rgba(0,0,0,0.1);
                white-space: nowrap;
                z-index: 998;
            }

            @keyframes ripple {
                0% { width: 100%; height: 100%; opacity: 0.8; }
                100% { width: 220%; height: 220%; opacity: 0; }
            }
            
            @keyframes floatBtn {
                0%, 100% { transform: translateY(0); }
                50% { transform: translateY(-10px); }
            }
        </style>
        """
    else:
        # 黑色背景 CSS + 3D星空穿梭 + 强制居中标题
        bg_style = """
        <style>
            .stApp {
                background-color: #050505;
                background-image: 
                    radial-gradient(1px 1px at 50% 50%, #ffffff 50%, transparent),
                    radial-gradient(2px 2px at 10% 20%, #ffffff 50%, transparent),
                    radial-gradient(1px 1px at 90% 80%, #ffffff 50%, transparent);
                background-size: 100% 100%;
                overflow: hidden;
            }
            
            .star-layer {
                position: fixed;
                top: 0; left: 0; width: 100%; height: 100%;
                background-image: 
                    radial-gradient(white, rgba(255,255,255,.2) 2px, transparent 3px),
                    radial-gradient(white, rgba(255,255,255,.15) 1px, transparent 2px),
                    radial-gradient(white, rgba(255,255,255,.1) 2px, transparent 3px);
                background-size: 550px 550px, 350px 350px, 250px 250px; 
                animation: starMove 60s linear infinite;
                z-index: 0;
                pointer-events: none;
            }

            @keyframes starMove {
                from {transform: translateY(0);}
                to {transform: translateY(-550px);}
            }
            
            /* 中心金色文字 - 强制 fixed 定位确保绝对居中 */
            .main-title {
                position: fixed;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                font-size: 3.8em;
                font-weight: 900;
                font-family: "SimSun", serif;
                background: linear-gradient(120deg, #bf953f, #fcf6ba, #b38728, #fbf5b7, #aa771c);
                background-size: 200% auto;
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                text-shadow: 0 0 20px rgba(191, 149, 63, 0.4);
                z-index: 100;
                white-space: nowrap;
                text-align: center;
                width: 100%;
                animation: shine 4s linear infinite, scaleIn 1s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            }

            @keyframes shine {
                to { background-position: 200% center; }
            }
            
            @keyframes scaleIn {
                from { transform: translate(-50%, -50%) scale(0.5); opacity: 0; }
                to { transform: translate(-50%, -50%) scale(1); opacity: 1; }
            }

            .floating-word {
                position: fixed;
                color: rgba(255, 255, 255, 0.85);
                font-family: "KaiTi", "STKaiti", serif;
                font-weight: bold;
                user-select: none;
                opacity: 0;
                text-shadow: 0 0 8px rgba(255,215,0,0.3);
                transform-origin: center center;
            }

            @keyframes tunnelFly {
                0% { 
                    opacity: 0; 
                    transform: translate(-50%, -50%) scale(0.1) rotate(0deg); 
                    filter: blur(4px);
                }
                20% { opacity: 0.8; }
                100% { 
                    opacity: 0; 
                    transform: translate(var(--tx), var(--ty)) scale(2.5) rotate(var(--rot)); 
                    filter: blur(0px);
                }
            }
            
            div.stButton > button {
                display: none;
            }
        </style>
        """
    st.markdown(bg_style, unsafe_allow_html=True)
    if page_type != 'landing':
        st.markdown('<div class="star-layer"></div>', unsafe_allow_html=True)

# --- 页面 1: 入口 (Landing Page) ---
def landing_page():
    local_css("landing")
    
    # 不再使用 st.columns，直接渲染组件，依靠 CSS position: fixed 定位
    clicked = st.button("开启2026")
    st.markdown('<div class="sub-text">点击开启你的2026</div>', unsafe_allow_html=True)
    
    if clicked:
        st.session_state.page = 'animation'
        st.rerun()

# --- 页面 2: 动画展示 (Animation Page) ---
def animation_page():
    local_css("animation")
    
    # 注入背景音乐
    play_bgm()
    
    # 1. 渲染中心金色文字
    st.markdown('<div class="main-title">希望2026年的你…</div>', unsafe_allow_html=True)
    
    # 2. 生成随机古风词汇
    if not st.session_state.generated_words:
        selected_words = random.sample(GUFENG_WORDS, 45) 
        
        html_elements = []
        for word in selected_words:
            angle_deg = random.uniform(0, 360)
            
            import math
            angle_rad = math.radians(angle_deg)
            # 使用视口单位 vw/vh 确保飞出屏幕
            tx = f"{math.cos(angle_rad) * 80}vw"
            ty = f"{math.sin(angle_rad) * 80}vh"
            rot = f"{random.randint(-20, 20)}deg"
            
            # 起始点：屏幕中心 (50% 50%)
            start_top = 50 + random.uniform(-2, 2)
            start_left = 50 + random.uniform(-2, 2)

            size = random.randint(18, 40)
            duration = random.uniform(3.0, 6.0)
            delay = random.uniform(0, 4.0)
            
            element = f"""
            <div class="floating-word" style="
                top: {start_top}%; 
                left: {start_left}%; 
                font-size: {size}px; 
                animation: tunnelFly {duration}s ease-out infinite;
                animation-delay: {delay}s;
                --tx: {tx};
                --ty: {ty};
                --rot: {rot};
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
