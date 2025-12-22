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

# --- 背景音乐链接 (已修正为 GitHub Raw 链接) ---
# 注意：GitHub 链接必须使用 raw.githubusercontent.com 格式才能直接播放
BGM_URL = "https://raw.githubusercontent.com/Huuxiann/Cut-Fat/main/%E5%9C%A8%E8%99%9A%E6%97%A0%E4%B8%AD%E6%B0%B8%E5%AD%98%20-%20%E8%8B%B1%E9%9B%84%E4%B8%BB%E4%B9%89.flac"

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

# --- 播放背景音乐函数 (增强版) ---
def play_bgm():
    # 注入 HTML5 Audio 和 JavaScript 控制脚本
    # 增加右上角悬浮按钮，如果自动播放失败，用户可以点击图标播放
    # type="audio/flac" 适配 flac 格式
    st.markdown(f"""
    <div style="display:none">
        <audio id="bgm_audio" preload="auto" loop>
            <source src="{BGM_URL}" type="audio/flac">
        </audio>
    </div>
    
    <!-- 音乐控制悬浮按钮 -->
    <div id="music_btn" onclick="toggleMusic()" style="
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
    ">
        🔇
    </div>

    <script>
        var audio = document.getElementById("bgm_audio");
        var btn = document.getElementById("music_btn");
        
        // 尝试自动播放
        function tryPlay() {{
            var playPromise = audio.play();
            if (playPromise !== undefined) {{
                playPromise.then(_ => {{
                    // 播放成功
                    btn.innerHTML = "🎵";
                    btn.style.animation = "spin 4s linear infinite";
                }}).catch(error => {{
                    // 播放失败（通常是因为浏览器策略）
                    console.log("Autoplay prevented. Waiting for user interaction.");
                    btn.innerHTML = "🔇";
                    btn.style.animation = "none";
                }});
            }}
        }}
        
        // 页面加载后立即尝试
        setTimeout(tryPlay, 500);

        // 切换播放状态
        function toggleMusic() {{
            if (audio.paused) {{
                audio.play();
                btn.innerHTML = "🎵";
                btn.style.animation = "spin 4s linear infinite";
            }} else {{
                audio.pause();
                btn.innerHTML = "🔇";
                btn.style.animation = "none";
            }}
        }}
    </script>
    <style>
        @keyframes spin {{ 100% {{ transform: rotate(360deg); }} }}
    </style>
    """, unsafe_allow_html=True)

# --- CSS 样式注入 ---
def local_css(page_type):
    # 通用重置样式：移除 Streamlit 默认的 padding，确保内容铺满全屏
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
                display: block; /* 修复某些布局下的显示问题 */
            }
            
            /* 涟漪效果 */
            div.stButton > button::before {
                content: '';
                position: absolute;
                top: 50%; left: 50%;
                transform: translate(-50%, -50%);
                width: 100%; height: 100%;
                border-radius: 50%;
                border
