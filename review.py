import streamlit as st
import pandas as pd
import random

# ==========================================
# 1. 页面配置与自定义样式
# ==========================================
st.set_page_config(
    page_title="眼科高分逻辑站 (OphthLogic)",
    page_icon="👁️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 注入CSS：优化表格、引用块、字体
st.markdown("""
<style>
    /* 全局字体优化 */
    .stApp { font-family: 'Helvetica Neue', 'PingFang SC', 'Microsoft YaHei', sans-serif; }
    
    /* 重点高亮块 */
    .highlight-box { 
        background-color: #f0f7ff; 
        padding: 15px; 
        border-radius: 8px; 
        border-left: 5px solid #0068c9; 
        margin-bottom: 15px;
    }
    
    /* 口诀块 */
    .mnemonic-box {
        background-color: #fff8c4;
        padding: 15px;
        border-radius: 8px;
        border: 1px dashed #f6b93b;
        font-style: italic;
        margin-bottom: 15px;
    }
    
    /* 陷阱/警示块 */
    .pitfall-box {
        background-color: #fff0f0;
        padding: 15px;
        border-radius: 8px;
        border-left: 5px solid #ff4b4b;
        margin-bottom: 15px;
    }

    /* 标题样式 */
    .section-title { font-size: 24px; font-weight: bold; color: #333; margin-top: 20px; margin-bottom: 10px; }
    .sub-title { font-size: 18px; font-weight: bold; color: #555; margin-top: 10px; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. 核心知识库 (Data Structure)
#    将文档内容结构化为字典，方便调用
# ==========================================

KNOWLEDGE_BASE = {
    "mnemonics": [
        "结膜鲜红穹隆起，推之能动肾上消，分泌物多视力好。",
        "睫状紫红角膜绕，推之不动难消退，痛畏流泪视力掉。",
        "外油中水内黏膜（对应：睑板腺-泪腺-杯状细胞）；油防蒸发，水供营养，黏抓角膜。",
        "上皮再生不留痕，前弹基质留疤痕；后弹坚韧防穿孔，内皮只大不生人。",
        "细菌急，脓性多，湿润坏死视力没。",
        "真菌缓，植物伤，牙膏羽毛卫星旁。",
        "病毒复，树枝长，激素一用穿孔忙。",
        "Marfan 高富帅，眼睛往上看（外上方）；同型 傻白甜，眼睛往下看（内下方）。",
        "前房红痛畏光泪，中间飞蚊雪球飞，后部无痛视力退。",
        "腰疼B27男前房，口腔溃疡白塞忙，晚霞白发VKH，外伤双眼交感伤。",
        "虹睫炎：充血紫，瞳孔缩小怕光死；KP角膜后方挂，房水闪辉若晨曦。",
        "青光眼视神经：大杯垂直长，盘沿ISNT亡；血管鼻侧移，刺刀出血忙。",
        "青光眼视野：早期旁中心，鼻侧阶梯藏；中期连成弓，晚期管状望。"
    ],
    
    "red_eye_table": {
        "columns": ["鉴别点", "结膜充血 (Conjunctival)", "睫状充血 (Ciliary)"],
        "data": [
            ["别名", "表层充血", "深层充血"],
            ["血管来源", "结膜后动脉（眼睑动脉弓）", "角膜缘血管网（睫状前动脉）"],
            ["充血外观", "鲜红色，树枝状/网状", "紫红色，毛刷状/放射状"],
            ["充血部位", "穹隆部明显，向角膜变淡", "角膜缘明显，向后变淡"],
            ["移动性", "推得动（随结膜移动）", "推不动（位置固定）"],
            ["肾上腺素试验", "敏感（立即消失）", "不敏感"],
            ["伴随症状", "异物感、分泌物多、视力好", "疼痛、畏光、流泪、视力减退"],
            ["常见病变", "结膜炎", "角膜炎、虹睫炎、青光眼"]
        ]
    },

    "tear_layers": {
        "columns": ["层次", "名称", "主要来源", "功能", "异常表现"],
        "data": [
            ["外层", "脂质层", "睑板腺 (MGD)", "防蒸发", "蒸发过强型干眼，BUT缩短"],
            ["中层", "水液层", "主/副泪腺", "供氧/营养/抗菌", "水液缺乏型干眼 (Sjogren)"],
            ["内层", "黏蛋白层", "结膜杯状细胞", "亲水界面/抓角膜", "黏蛋白缺乏型，泪液无法铺展"]
        ]
    },

    "cornea_layers": {
        "columns": ["层次", "名称", "再生能力 (核心考点)", "特点"],
        "data": [
            ["1", "上皮细胞层", "✅ 极强，不留瘢痕", "富含神经，痛觉敏锐"],
            ["2", "前弹力层", "❌ 不可再生", "损伤后留云翳/斑翳"],
            ["3", "基质层", "❌ 不可再生", "最厚(90%)，透明的基础"],
            ["4", "后弹力层", "✅ 可再生", "坚韧，耐侵蚀 (Descemetocele)"],
            ["5", "内皮细胞层", "❌ 不可再生 (只大不生人)", "泵功能，受损致大泡性角膜病变"]
        ]
    },

    "keratitis_diff": {
        "columns": ["鉴别点", "细菌性", "真菌性", "病毒性 (HSV)"],
        "data": [
            ["典型病史", "外伤、隐形眼镜、慢性泪囊炎", "植物外伤 (树枝/玉米叶)", "感冒/发热后复发"],
            ["起病/痛感", "急，剧痛", "缓，症状轻体征重", "复发性，痛感轻(知觉减退)"],
            ["分泌物", "大量脓性", "少，粘稠", "水样"],
            ["溃疡形态", "边界不清，湿润坏死", "牙膏/乳酪样，干燥，边界清", "树枝状、地图状"],
            ["特征性体征", "前房积脓(流动性)", "羽毛状、卫星灶、菌丝苔被", "末端膨大、知觉减退"],
            ["核心药物", "左氧氟沙星/妥布霉素", "纳他霉素/氟康唑", "更昔洛韦/阿昔洛韦"]
        ]
    },

    "uveitis_class": {
        "columns": ["类型", "主战场", "核心症状", "特有体征"],
        "data": [
            ["前葡萄膜炎", "前房 (虹膜/睫状体)", "红、痛、畏光", "KP、房水闪辉 (Tyndall)"],
            ["中间葡萄膜炎", "玻璃体", "飞蚊症、视物模糊", "雪球状混浊 (Snowballs)"],
            ["后葡萄膜炎", "视网膜/脉络膜", "无痛视力下降", "眼底病灶"],
            ["全葡萄膜炎", "所有层次", "混合上述", "病情最重"]
        ]
    },

    "three_demons": {
        "columns": ["鉴别点", "急性虹膜睫状体炎", "急性结膜炎", "急性闭角型青光眼"],
        "data": [
            ["充血", "睫状充血 (紫红)", "结膜充血 (鲜红)", "混合充血"],
            ["瞳孔", "缩小 (梅花瓣状)", "正常", "散大 (垂直椭圆)"],
            ["角膜", "透明，后背KP", "透明", "雾状水肿"],
            ["前房", "正常/房水闪辉", "正常", "极浅"],
            ["眼压", "正常/偏低", "正常", "极高 (坚硬如石)"],
            ["分泌物", "水样 (流泪)", "黏液脓性", "水样"]
        ]
    },
    
    "glaucoma_diff": {
        "columns": ["鉴别点", "闭角型 (PACG)", "开角型 (POAG)"],
        "data": [
            ["机制", "房角关闭 (门关了)", "小梁网功能障碍 (下水道堵了)"],
            ["房角", "窄/闭", "宽/开"],
            ["起病", "急骤 (头痛呕吐)", "隐匿 (视力杀手)"],
            ["视力", "剧降", "早期正常，晚期管状视野"],
            ["治疗", "激光虹膜周切/晶体摘除", "药物/小梁切除术"]
        ]
    }
}

# ==========================================
# 3. 辅助函数
# ==========================================

def display_table(data_dict, title=None, blind_mode=False):
    """渲染表格，支持遮挡模式"""
    if title:
        st.subheader(title)
    
    df = pd.DataFrame(data_dict["data"], columns=data_dict["columns"])
    
    if blind_mode:
        # 遮挡除第一列外的所有列
        cols_to_show = [data_dict["columns"][0]]
        st.dataframe(df[cols_to_show], use_container_width=True)
        st.caption("🙈 遮挡模式已开启，请回忆详细内容...")
    else:
        st.dataframe(df, use_container_width=True)

def render_mnemonic_box(text):
    st.markdown(f'<div class="mnemonic-box">🔔 <b>口诀：</b>{text}</div>', unsafe_allow_html=True)

def render_highlight_box(title, text):
    st.markdown(f'<div class="highlight-box"><b>{title}</b><br>{text}</div>', unsafe_allow_html=True)

def render_pitfall_box(title, text):
    st.markdown(f'<div class="pitfall-box">❌ <b>{title}</b><br>{text}</div>', unsafe_allow_html=True)

# ==========================================
# 4. 侧边栏导航
# ==========================================
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/ophthalmology.png", width=70)
    st.title("OphthLogic Review")
    st.caption("基于文档：解剖-机制-临床-实战")
    
    menu = st.radio(
        "导航菜单",
        [
            "🏠 首页 (Dashboard)",
            "🧬 解剖：泪液与角膜",
            "🔴 核心：红眼与角膜病",
            "🔥 核心：葡萄膜炎",
            "🌑 核心：青光眼 & 晶状体",
            "⚔️ 实战：病例模拟",
            "🎒 考前工具箱"
        ]
    )
    
    st.divider()
    st.info("💡 每日一记：\n" + random.choice(KNOWLEDGE_BASE["mnemonics"]))

# ==========================================
# 5. 主页面逻辑
# ==========================================

# --- 首页 ---
if "首页" in menu:
    st.title("眼科高分逻辑复习站")
    st.markdown("#### *Slogan: 从机制推导临床，用逻辑代替死记。*")
    
    st.info("👋 欢迎回来！本网站包含文档中所有核心考点：解剖五层楼、红眼鉴别、细菌真菌病毒角膜炎对比、葡萄膜炎分类及青光眼机制。")
    
    col1, col2 = st.columns(2)
    with col1:
        render_highlight_box("复习策略", "1. 先看【解剖】，理解血管走行和膜层结构。\n2. 重点背诵【工具箱】里的黄金表格。\n3. 用【病例模拟】检验临床思维。")
    with col2:
        render_pitfall_box("常见误区", "看到红眼就是结膜炎？(错！可能是青光眼)\n视力下降就是近视？(错！查查眼底和晶状体)")

# --- 解剖模块 ---
elif "解剖" in menu:
    st.title("🧬 解剖与基础机制")
    
    tab1, tab2 = st.tabs(["💧 泪液系统", "👁️ 角膜五层楼"])
    
    with tab1:
        st.subheader("1. 泪膜三层结构 (Tear Film)")
        st.markdown("直接关联干眼症分类。从外向内：")
        display_table(KNOWLEDGE_BASE["tear_layers"])
        render_mnemonic_box("外油中水内黏膜，油防蒸发水供养。")
        
        st.subheader("2. 泪道流向")
        st.code("点 → 小 → 总 → 囊 → 鼻 → 下 (Hasner瓣)", language=None)
        render_pitfall_box("易错点", "鼻泪管开口于**下鼻道**，不是中鼻道！\n新生儿泪囊炎常因Hasner瓣未破。")
        
    with tab2:
        st.subheader("1. 角膜五层结构")
        st.markdown("重点记忆**再生能力**，决定了是否留疤。")
        display_table(KNOWLEDGE_BASE["cornea_layers"])
        render_mnemonic_box(KNOWLEDGE_BASE["mnemonics"][3])
        
        st.markdown("---")
        st.subheader("2. 透明机制")
        st.markdown("- **解剖**：胶原纤维规则排列、无血管、无色素。\n- **生理**：内皮泵功能维持脱水状态（一旦泵衰竭 -> 水肿）。")

# --- 红眼与角膜病 ---
elif "红眼" in menu:
    st.title("🔴 临床核心：红眼与角膜病")
    
    # 开关：死记硬背模式
    blind = st.toggle("🛡️ 开启遮挡模式 (自测用)")
    
    st.subheader("1. 充血鉴别 (The Red Eye)")
    st.markdown("见“充血”二字，迅速建立鉴别树。")
    display_table(KNOWLEDGE_BASE["red_eye_table"], blind_mode=blind)
    
    render_highlight_box("机制解析", 
    "- **结膜充血**：表浅，推得动，滴肾上腺素变白。\n- **睫状充血**：深层，推不动，滴肾上腺素无效（提示角膜/虹膜/青光眼病变）。")
    
    st.markdown("---")
    st.subheader("2. 感染性角膜炎鉴别 (Keratitis)")
    st.markdown("关键词匹配法：看到“羽毛状”选真菌，看到“树枝状”选病毒。")
    display_table(KNOWLEDGE_BASE["keratitis_diff"], blind_mode=blind)
    
    col1, col2 = st.columns(2)
    with col1:
        render_pitfall_box("死刑题", "病毒性角膜炎（上皮型），**绝对禁止**使用激素！否则穿孔。")
    with col2:
        render_highlight_box("棘阿米巴角膜炎", "关键词：隐形眼镜 + 自来水冲洗。\n特征：症状与体征分离（痛得打滚，角膜看着还行）。")

# --- 葡萄膜炎 ---
elif "葡萄膜炎" in menu:
    st.title("🔥 葡萄膜炎 (Uveitis)")
    
    st.subheader("1. 国际SUN分类")
    display_table(KNOWLEDGE_BASE["uveitis_class"])
    
    st.subheader("2. 临床体征核心")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("**KP (角膜后沉着物)**")
        st.markdown("- 尘状：非肉芽肿性 (HLA-B27)\n- 羊脂状：肉芽肿性 (结核/梅毒)")
    with c2:
        st.markdown("**房水闪辉 (Tyndall)**")
        st.markdown("- 像阳光照进灰尘屋\n- 代表血-房水屏障破坏")
    with c3:
        st.markdown("**瞳孔改变**")
        st.markdown("- 缩小、梅花瓣状 (后粘连)\n- **治疗首选：阿托品散瞳！**")
        
    st.subheader("3. 自身免疫病“四大金刚”")
    with st.expander("点击展开详细鉴别"):
        st.markdown("""
        * **HLA-B27相关**：年轻男性 + 强直性脊柱炎 (AS) + 急性前葡萄膜炎。
        * **白塞病 (Behcet)**：口腔溃疡 + 外阴溃疡 + 游走性前房积脓。
        * **VKH综合征**：晚霞状眼底 + 白发/白癜风 + 双眼全葡。
        * **交感性眼炎**：一眼穿通伤后，另一眼发炎（2周-2月）。
        """)

    st.subheader("4. 红眼三大魔头鉴别")
    st.markdown("**必考！必考！必考！**")
    display_table(KNOWLEDGE_BASE["three_demons"])

# --- 青光眼与晶状体 ---
elif "青光眼" in menu:
    st.title("🌑 青光眼与晶状体")
    
    tab_g, tab_c = st.tabs(["青光眼 (Glaucoma)", "晶状体 (Lens)"])
    
    with tab_g:
        st.subheader("1. 定义与分类")
        st.markdown("定义核心：视神经萎缩 + 视野缺损 (眼压只是危险因素)。")
        display_table(KNOWLEDGE_BASE["glaucoma_diff"])
        
        st.subheader("2. 视神经损害 (C/D比)")
        render_mnemonic_box(KNOWLEDGE_BASE["mnemonics"][-2]) # 视神经口诀
        st.markdown("""
        - **ISNT法则丧失**：盘沿变窄。
        - **C/D > 0.6** 或双眼差 > 0.2。
        - **刺刀征**：血管90度折曲。
        """)
        
        st.subheader("3. 视野缺损演变")
        st.code("旁中心暗点/鼻侧阶梯 → 弓形暗点 (Bjerrum) → 环形暗点 → 管状视野 → 颞侧视岛")
        
    with tab_c:
        st.subheader("1. 白内障四期 (皮质性)")
        st.markdown("""
        1. **初发期**：楔形混浊。
        2. **膨胀期**：晶体吸水肿胀 → **诱发青光眼** (重要并发症)。
        3. **成熟期**：完全混浊。
        4. **过熟期**：核下沉，诱发晶状体溶解性青光眼。
        """)
        
        st.subheader("2. 晶状体脱位")
        st.info(KNOWLEDGE_BASE["mnemonics"][7])

# --- 实战演练 ---
elif "实战" in menu:
    st.title("⚔️ 临床病例实战")
    
    # 病例 1
    with st.expander("病例 1：农民伯伯的遭遇", expanded=True):
        st.write("患者男性，农民。右眼红痛、视力下降10天。收割玉米时被叶片划伤。查体：混合充血，角膜中央灰白溃疡，表面干燥，边缘呈羽毛状。")
        ans1 = st.radio("你的诊断？", ["细菌性角膜炎", "真菌性角膜炎", "病毒性角膜炎", "棘阿米巴角膜炎"], key="c1")
        if st.button("提交病例1"):
            if ans1 == "真菌性角膜炎":
                st.success("✅ 正确！关键词：植物外伤 + 羽毛状/干燥 = 真菌。")
                st.markdown("**治疗**：纳他霉素，忌激素。")
            else:
                st.error("❌ 错误。提示：注意植物外伤史和'羽毛状'特征。")

    # 病例 2
    with st.expander("病例 2：拳击手的红眼", expanded=True):
        st.write("拳击手，右眼被击中。痛，视力模糊。裂隙灯：前房下方可见红色液平，瞳孔呈D形。")
        ans2 = st.radio("最可能的体征描述？", ["前房积脓", "前房积血+虹膜根部离断", "玻璃体积血", "角膜穿通伤"], key="c2")
        if st.button("提交病例2"):
            if ans2 == "前房积血+虹膜根部离断":
                st.success("✅ 正确！钝挫伤导致'隔山打牛'。")
                st.markdown("**解析**：液平=积血；D形瞳孔=虹膜根部离断。")
            else:
                st.error("❌ 错误。红色液平是血液，脓是黄白色的。")

    # 病例 3
    with st.expander("病例 3：腰痛的年轻人", expanded=True):
        st.write("25岁男性，反复腰骶部疼痛伴晨僵3年。现突发右眼红痛、畏光。查体：睫状充血，KP(+)，房水闪辉(++)。")
        ans3 = st.radio("最可能的关联疾病？", ["白塞病", "Vogt-小柳-原田综合征", "强直性脊柱炎", "类风湿关节炎"], key="c3")
        if st.button("提交病例3"):
            if ans3 == "强直性脊柱炎":
                st.success("✅ 正确！HLA-B27相关前葡萄膜炎。")
            else:
                st.error("❌ 错误。腰骶痛+晨僵是强直性脊柱炎的典型表现。")

# --- 工具箱 ---
elif "工具箱" in menu:
    st.title("🎒 考前工具箱")
    
    st.subheader("📜 记忆口诀大全")
    for m in KNOWLEDGE_BASE["mnemonics"]:
        st.markdown(f"- {m}")
        
    st.markdown("---")
    st.subheader("💊 核心药物速查")
    st.markdown("""
    | 药物 | 适应症 | 备注 |
    | :--- | :--- | :--- |
    | **阿托品** | 虹睫炎、角膜炎 | **散瞳止痛**，防后粘连 (首要任务！) |
    | **毛果芸香碱** | 青光眼 (闭角型) | **缩瞳**，拉开房角 |
    | **纳他霉素** | 真菌性角膜炎 | 首选抗真菌 |
    | **更昔洛韦** | 病毒性角膜炎 | 抗HSV |
    | **糖皮质激素** | 葡萄膜炎 | **禁用于**病毒性角膜炎上皮期 |
    """)

# ==========================================
# 底部
# ==========================================
st.markdown("---")
st.caption("© 2025 OphthLogic | 基于用户上传文档生成 | 祝考试高分！")
