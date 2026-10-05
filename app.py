import os
import streamlit as st
import plotly.express as px
from dotenv import load_dotenv

from data_service import load_sales
from stats_service import calculate_statistics
from ai_service import generate_insight, ask_data
from auth_service import firebase_enabled, login, register


# =========================================================
# ENVIRONMENT
# =========================================================

load_dotenv()

try:
    for k, v in st.secrets.items():
        if isinstance(v, (str, int, float, bool)):
            os.environ.setdefault(k, str(v))
except Exception:
    pass


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Restaurant AI Analytics",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =========================================================
# CSS
# =========================================================

st.markdown("""
<style>

/* ---------- GLOBAL ---------- */

.stApp {
    background:
        radial-gradient(circle at 8% 5%,
        rgba(255,190,125,0.18),
        transparent 25%),

        radial-gradient(circle at 92% 10%,
        rgba(115,210,170,0.16),
        transparent 25%),

        linear-gradient(
            180deg,
            #FFF8EF 0%,
            #FFFFFF 42%,
            #F2FBF6 100%
        );

    color: #182230 !important;
}

.block-container {
    max-width: 1240px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

#MainMenu,
footer {
    visibility: hidden;
}


/* ---------- TEXT ---------- */

h1 {
    color: #14213D !important;
    font-weight: 900 !important;
}

h2 {
    color: #172B4D !important;
    font-weight: 850 !important;
}

h3 {
    color: #243B53 !important;
    font-weight: 800 !important;
}

p {
    color: #475467;
}


/* ---------- HERO ---------- */

.hero {
    padding: 34px 38px;

    border-radius: 28px;

    background:
        linear-gradient(
            120deg,
            #FFE4C3 0%,
            #FFF3E0 48%,
            #DDF7E9 100%
        );

    border: 1px solid #EBC9A5;

    box-shadow:
        0 16px 40px
        rgba(91,64,35,0.10);

    margin-bottom: 26px;
}

.hero h1 {
    font-size: 2.55rem !important;
    color: #172033 !important;
    margin: 0 0 10px 0;
    font-weight: 900 !important;
}

.hero p {
    font-size: 1.07rem;
    color: #475467 !important;
    margin: 0;
    font-weight: 550;
}


/* ---------- BADGE ---------- */

.badge {
    display: inline-block;

    background: #FFFFFF;
    color: #C94620 !important;

    border: 1px solid #F1AD96;
    border-radius: 999px;

    padding: 7px 14px;

    font-size: 0.78rem;
    font-weight: 900;

    letter-spacing: 0.7px;

    margin-bottom: 14px;

    box-shadow:
        0 4px 12px
        rgba(217,79,37,0.08);
}


/* ---------- SECTION NOTE ---------- */

.section-note {
    color: #52606D !important;
    margin-top: -8px;
    margin-bottom: 20px;
    font-size: 0.98rem;
    font-weight: 500;
}

.center-note {
    text-align: center;
    color: #52606D !important;
    font-weight: 650;
}


/* ---------- UPLOAD CARD ---------- */

.upload-card {
    text-align: center;

    border: 2px dashed #E68A50;

    background:
        linear-gradient(
            135deg,
            #FFF5EA,
            #FFFFFF
        );

    margin: 16px 0 20px;

    padding: 46px 25px;

    border-radius: 24px;

    box-shadow:
        0 10px 30px
        rgba(31,41,55,0.06);
}

.upload-card h2 {
    color: #172B4D !important;
    font-weight: 900 !important;
}

.upload-card p {
    color: #52606D !important;
}


/* ---------- FILE UPLOADER ---------- */

[data-testid="stFileUploader"] {
    background: #FFFFFF;

    padding: 18px;

    border-radius: 18px;

    border: 1px solid #D9DDE3;

    box-shadow:
        0 6px 18px
        rgba(31,41,55,0.05);
}

[data-testid="stFileUploader"] * {
    color: #263445 !important;
}


/* ---------- KPI ---------- */

[data-testid="stMetric"] {
    background: #FFFFFF;

    border: 1px solid #E1E5EA;

    padding: 20px;

    border-radius: 20px;

    box-shadow:
        0 8px 24px
        rgba(31,41,55,0.07);

    transition:
        transform 0.20s ease,
        box-shadow 0.20s ease;
}

[data-testid="stMetric"]:hover {
    transform: translateY(-3px);

    box-shadow:
        0 12px 30px
        rgba(31,41,55,0.11);
}

[data-testid="stMetricLabel"],
[data-testid="stMetricLabel"] * {
    color: #475467 !important;
    font-weight: 750 !important;
}

[data-testid="stMetricValue"],
[data-testid="stMetricValue"] * {
    color: #101828 !important;
    font-weight: 900 !important;
}


/* ---------- BUTTON ---------- */

.stButton > button {
    border-radius: 14px;

    font-weight: 800;

    min-height: 46px;

    border: 1px solid #D0D5DD;

    background: #FFFFFF;

    color: #344054 !important;

    transition: all 0.20s ease;
}

.stButton > button:hover {
    border-color: #E86740;
    color: #C94620 !important;
    background: #FFF5F0;

    transform: translateY(-1px);
}


/* ---------- PRIMARY BUTTON ---------- */

.stButton > button[kind="primary"] {
    background:
        linear-gradient(
            90deg,
            #E94F2D,
            #F77B42
        ) !important;

    color: #FFFFFF !important;

    border: none !important;

    box-shadow:
        0 7px 18px
        rgba(233,79,45,0.23);
}

.stButton > button[kind="primary"] * {
    color: #FFFFFF !important;
}

.stButton > button[kind="primary"]:hover {
    background:
        linear-gradient(
            90deg,
            #CE3F21,
            #E86732
        ) !important;

    color: #FFFFFF !important;

    transform: translateY(-2px);
}


/* ---------- TEXT INPUT ---------- */

.stTextInput label {
    color: #243B53 !important;
    font-weight: 750 !important;
}

.stTextInput input {
    color: #101828 !important;

    background: #FFFFFF !important;

    border: 1px solid #BCC5D0 !important;

    border-radius: 12px !important;
}

.stTextInput input::placeholder {
    color: #7A8797 !important;
}

.stTextInput input:focus {
    border-color: #E86740 !important;

    box-shadow:
        0 0 0 3px
        rgba(232,103,64,0.13) !important;
}


/* ---------- TABS ---------- */

button[data-baseweb="tab"] {
    color: #475467 !important;
    font-weight: 750 !important;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: #C94620 !important;
    font-weight: 900 !important;
}


/* ---------- ALERT ---------- */

div[data-testid="stAlert"] {
    border-radius: 16px;
}

div[data-testid="stAlert"] * {
    color: #263445 !important;
}


/* ---------- DOWNLOAD ---------- */

[data-testid="stDownloadButton"] button {
    background: #D9F4E4 !important;

    color: #0D5C38 !important;

    border: 1px solid #9FD6B6 !important;

    border-radius: 14px;

    font-weight: 850;

    min-height: 46px;
}

[data-testid="stDownloadButton"] button * {
    color: #0D5C38 !important;
}


/* ---------- EXPANDER ---------- */

[data-testid="stExpander"] {
    background: #FFFFFF;

    border: 1px solid #E2E6EA;

    border-radius: 16px;
}

[data-testid="stExpander"] * {
    color: #344054 !important;
}


/* ---------- CAPTION ---------- */

[data-testid="stCaptionContainer"],
[data-testid="stCaptionContainer"] * {
    color: #52606D !important;
}


/* ---------- MOBILE ---------- */

@media (max-width: 768px) {

    .hero {
        padding: 25px 22px;
        border-radius: 22px;
    }

    .hero h1 {
        font-size: 2rem !important;
    }

    .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
    }
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# LOGIN / REGISTER
# =========================================================

if firebase_enabled() and not st.session_state.get("user"):

    st.markdown(
        """
<div class="hero">
<span class="badge">SMART RESTAURANT</span>
<h1>🍽️ Restaurant AI Analytics</h1>
<p>เข้าสู่ระบบเพื่อวิเคราะห์ยอดขายร้านอาหารด้วย Data Analytics + Generative AI</p>
</div>
        """,
        unsafe_allow_html=True
    )

    left, center, right = st.columns([1, 1.25, 1])

    with center:

        st.markdown("## 🔐 ยินดีต้อนรับ")

        st.caption(
            "เข้าสู่ระบบเพื่อเริ่มต้นวิเคราะห์ข้อมูลร้านของคุณ"
        )

        tab_login, tab_register = st.tabs(
            [
                "🔑 เข้าสู่ระบบ",
                "✨ สมัครสมาชิก"
            ]
        )

        # LOGIN
        with tab_login:

            email = st.text_input(
                "อีเมล",
                key="login_email",
                placeholder="name@example.com"
            )

            password = st.text_input(
                "รหัสผ่าน",
                type="password",
                key="login_password",
                placeholder="กรอกรหัสผ่าน"
            )

            if st.button(
                "เข้าสู่ระบบ ➜",
                type="primary",
                use_container_width=True
            ):

                if not email or not password:
                    st.warning(
                        "กรุณากรอกอีเมลและรหัสผ่าน"
                    )

                else:

                    ok, res = login(
                        email,
                        password
                    )

                    if ok:

                        st.session_state.user = (
                            res.get(
                                "email",
                                email
                            )
                        )

                        st.rerun()

                    else:
                        st.error(res)


        # REGISTER
        with tab_register:

            email = st.text_input(
                "อีเมล",
                key="register_email",
                placeholder="name@example.com"
            )

            password = st.text_input(
                "รหัสผ่านอย่างน้อย 6 ตัวอักษร",
                type="password",
                key="register_password",
                placeholder="สร้างรหัสผ่าน"
            )

            if st.button(
                "สร้างบัญชี ✨",
                type="primary",
                use_container_width=True
            ):

                if not email or not password:

                    st.warning(
                        "กรุณากรอกอีเมลและรหัสผ่าน"
                    )

                elif len(password) < 6:

                    st.warning(
                        "รหัสผ่านต้องมีอย่างน้อย 6 ตัวอักษร"
                    )

                else:

                    ok, res = register(
                        email,
                        password
                    )

                    if ok:

                        st.success(
                            "🎉 สมัครสมาชิกสำเร็จ "
                            "กรุณากลับไปที่แท็บเข้าสู่ระบบ"
                        )

                    else:
                        st.error(res)

    st.stop()


# =========================================================
# HEADER
# =========================================================

st.markdown(
    """
<div class="hero">
<span class="badge">RESTAURANT INTELLIGENCE</span>
<h1>🍽️ Restaurant AI Analytics</h1>
<p>เปลี่ยนข้อมูลยอดขาย CSV ให้เป็น Dashboard, Business Insight และคำตอบจาก AI</p>
</div>
    """,
    unsafe_allow_html=True
)


head1, head2 = st.columns([5, 1])


with head1:

    if st.session_state.get("user"):

        st.caption(
            f"👤 เข้าสู่ระบบด้วย "
            f"{st.session_state.user}"
        )


with head2:

    if (
        st.session_state.get("user")
        and st.button(
            "🚪 ออกจากระบบ",
            use_container_width=True
        )
    ):

        for k in [
            "user",
            "messages",
            "insight",
            "answer"
        ]:
            st.session_state.pop(k, None)

        st.rerun()


# =========================================================
# UPLOAD CSV
# =========================================================

st.markdown(
    "## 📤 นำเข้าข้อมูลยอดขาย"
)

st.markdown(
    '<p class="section-note">ระบบจะเริ่มวิเคราะห์หลังจากอัปโหลดไฟล์ CSV เท่านั้น</p>',
    unsafe_allow_html=True
)


uploaded = st.file_uploader(
    "เลือกไฟล์ CSV",
    type=["csv"],
    help=(
        "ไฟล์ต้องมีคอลัมน์ "
        "Date, Time, Menu, Category, "
        "Quantity และ Price"
    )
)


# =========================================================
# NO CSV = NO PROCESSING
# =========================================================

if uploaded is None:

    st.markdown(
        """
<div class="upload-card">
<div style="font-size:55px;margin-bottom:10px;">📁</div>
<h2>พร้อมวิเคราะห์ข้อมูลร้านของคุณ</h2>
<p>อัปโหลดไฟล์ CSV ด้านบน เพื่อเปิด Dashboard และ AI Restaurant Analyst</p>
<p class="center-note">Date • Time • Menu • Category • Quantity • Price</p>
</div>
        """,
        unsafe_allow_html=True
    )

    st.info(
        "💡 ระบบจะยังไม่คำนวณยอดขายหรือเรียก AI "
        "จนกว่าจะมีการอัปโหลด CSV"
    )

    st.stop()


# =========================================================
# LOAD CSV
# =========================================================

try:

    df = load_sales(
        uploaded
    )

except Exception as e:

    st.error(
        f"❌ อ่านไฟล์ไม่สำเร็จ: {e}"
    )

    st.info(
        "ตรวจสอบให้ไฟล์มีคอลัมน์ "
        "Date, Time, Menu, Category, Quantity, Price"
    )

    st.stop()


if df.empty:

    st.warning(
        "⚠️ ไม่พบข้อมูลที่พร้อมวิเคราะห์ในไฟล์นี้"
    )

    st.stop()


# =========================================================
# CALCULATE
# =========================================================

s = calculate_statistics(
    df
)


st.success(
    f"✅ นำเข้าไฟล์ **{uploaded.name}** สำเร็จ "
    f"• พบข้อมูล {len(df):,} รายการ"
)


# =========================================================
# KPI
# =========================================================

st.markdown(
    "## 📊 ภาพรวมธุรกิจ"
)

st.markdown(
    '<p class="section-note">ตัวชี้วัดสำคัญจากข้อมูลยอดขายที่อัปโหลด</p>',
    unsafe_allow_html=True
)


c1, c2, c3, c4, c5 = st.columns(5)


c1.metric(
    "💰 ยอดขายรวม",
    f"฿{s['total_sales']:,.0f}"
)

c2.metric(
    "🧾 รายการขาย",
    f"{s['orders']:,}"
)

c3.metric(
    "📦 จำนวนที่ขาย",
    f"{s['total_qty']:,}"
)

c4.metric(
    "💳 เฉลี่ย / รายการ",
    f"฿{s['avg_order_value']:,.0f}"
)

c5.metric(
    "⏰ Peak Hour",
    (
        f"{s['peak_hour']:02d}:00"
        if s["peak_hour"] is not None
        else "-"
    )
)


st.info(
    f"🏆 เมนูที่สร้างยอดขายสูงสุด: "
    f"**{s['best_menu']}**"
)


# =========================================================
# PLOTLY DESIGN
# =========================================================

def polish(fig, height=390):

    fig.update_layout(

        height=height,

        margin=dict(
            l=45,
            r=25,
            t=70,
            b=50
        ),

        # พื้นหลัง
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",

        # บังคับตัวหนังสือทั้งหมดให้เข้ม
        font=dict(
            family="Arial, Tahoma, sans-serif",
            size=14,
            color="#172033"
        ),

        # ชื่อกราฟ
        title=dict(
            font=dict(
                family="Arial, Tahoma, sans-serif",
                size=20,
                color="#14213D"
            ),
            x=0.02,
            xanchor="left"
        ),

        # Tooltip
        hoverlabel=dict(
            bgcolor="#FFFFFF",
            bordercolor="#98A2B3",
            font=dict(
                family="Arial, Tahoma, sans-serif",
                size=14,
                color="#101828"
            )
        ),

        showlegend=False
    )


    # ---------- X AXIS ----------

    fig.update_xaxes(

        title_font=dict(
            size=15,
            color="#344054"
        ),

        tickfont=dict(
            size=13,
            color="#344054"
        ),

        tickcolor="#475467",

        linecolor="#667085",

        gridcolor="#E4E7EC",

        zerolinecolor="#D0D5DD",

        showline=True,

        linewidth=1
    )


    # ---------- Y AXIS ----------

    fig.update_yaxes(

        title_font=dict(
            size=15,
            color="#344054"
        ),

        tickfont=dict(
            size=13,
            color="#344054"
        ),

        tickcolor="#475467",

        linecolor="#667085",

        gridcolor="#E4E7EC",

        zerolinecolor="#D0D5DD",

        showline=True,

        linewidth=1
    )

    return fig


# =========================================================
# SALES ANALYTICS
# =========================================================

st.markdown(
    "## 📈 Sales Analytics"
)

st.markdown(
    '<p class="section-note">ดูแนวโน้มยอดขาย เมนูยอดนิยม และช่วงเวลาที่สร้างยอดขาย</p>',
    unsafe_allow_html=True
)


# =========================================================
# ROW 1
# =========================================================

left, right = st.columns(2)


# ---------- DAILY ----------

with left:

    fig_daily = px.line(

        s["daily"],

        x="Date",

        y="Sales",

        markers=True,

        title="📅 แนวโน้มยอดขายรายวัน",

        labels={
            "Date": "วันที่",
            "Sales": "ยอดขาย (บาท)"
        }
    )

    fig_daily.update_traces(

        line=dict(
            width=3
        ),

        marker=dict(
            size=8
        )
    )

    st.plotly_chart(

        polish(
            fig_daily,
            400
        ),

        use_container_width=True
    )


# ---------- TOP MENU ----------

with right:

    top = (
        s["menu_sales"]
        .head(10)
        .sort_values("Sales")
    )

    fig_menu = px.bar(

        top,

        x="Sales",

        y="Menu",

        orientation="h",

        title="🏆 Top 10 เมนูตามยอดขาย",

        labels={
            "Sales": "ยอดขาย (บาท)",
            "Menu": "เมนู"
        }
    )

    # ทำชื่อเมนูให้ชัด
    fig_menu.update_yaxes(
        tickfont=dict(
            size=14,
            color="#172033"
        )
    )

    st.plotly_chart(

        polish(
            fig_menu,
            400
        ),

        use_container_width=True
    )


# =========================================================
# ROW 2
# =========================================================

left, right = st.columns(2)


# ---------- PERIOD ----------

with left:

    fig_period = px.bar(

        s["period"],

        x="Period",

        y="Sales",

        title="🕒 ยอดขายตามช่วงเวลา",

        labels={
            "Period": "ช่วงเวลา",
            "Sales": "ยอดขาย (บาท)"
        }
    )

    fig_period.update_xaxes(
        tickfont=dict(
            size=14,
            color="#172033"
        )
    )

    st.plotly_chart(

        polish(
            fig_period,
            370
        ),

        use_container_width=True
    )


# ---------- HOURLY ----------

with right:

    hourly_sorted = (
        s["hourly"]
        .sort_values("Hour")
    )

    fig_hour = px.line(

        hourly_sorted,

        x="Hour",

        y="Sales",

        markers=True,

        title="⏰ ยอดขายรายชั่วโมง",

        labels={
            "Hour": "เวลา (ชั่วโมง)",
            "Sales": "ยอดขาย (บาท)"
        }
    )

    fig_hour.update_traces(

        line=dict(
            width=3
        ),

        marker=dict(
            size=8
        )
    )

    st.plotly_chart(

        polish(
            fig_hour,
            370
        ),

        use_container_width=True
    )


# =========================================================
# AI RESTAURANT ANALYST
# =========================================================

st.markdown(
    "## 🤖 AI Restaurant Analyst"
)

st.markdown(
    '<p class="section-note">AI จะตอบจากข้อมูล CSV ที่คุณอัปโหลดในรอบนี้</p>',
    unsafe_allow_html=True
)


# =========================================================
# EXECUTIVE INSIGHT
# =========================================================

if st.button(
    "✨ สร้าง AI Executive Insight",
    type="primary",
    use_container_width=True
):

    with st.spinner(
        "🤖 AI กำลังวิเคราะห์ข้อมูลร้าน..."
    ):

        try:

            st.session_state.insight = (
                generate_insight(
                    s,
                    df
                )
            )

        except Exception as e:

            st.session_state.insight = (
                f"AI ยังไม่สามารถวิเคราะห์ได้: {e}"
            )


if st.session_state.get("insight"):

    st.info(
        st.session_state.insight
    )


# =========================================================
# ASK AI
# =========================================================

st.markdown(
    "### 💬 ถาม AI เกี่ยวกับข้อมูลร้าน"
)

st.caption(
    "AI จะใช้ข้อมูลจากไฟล์ CSV ที่คุณเพิ่งอัปโหลด"
)


q = st.text_input(

    "คำถาม",

    placeholder=(
        "เช่น เมนูไหนขายดีที่สุด? "
        "ช่วงไหนยอดขายสูงที่สุด? "
        "ควรโปรโมตเมนูอะไร?"
    ),

    key="ai_question",

    label_visibility="collapsed"
)


if st.button(

    "ส่งคำถามให้ AI ➜",

    type="primary",

    use_container_width=True,

    disabled=not bool(
        q.strip()
    )
):

    with st.spinner(
        "🔎 AI กำลังวิเคราะห์คำถาม..."
    ):

        try:

            st.session_state.answer = (
                ask_data(
                    s,
                    df,
                    q.strip()
                )
            )

        except Exception as e:

            st.session_state.answer = (
                f"AI ยังไม่สามารถตอบคำถามได้: {e}"
            )


if st.session_state.get("answer"):

    st.success(
        st.session_state.answer
    )


st.caption(
    "💡 ลองถาม: เมนูไหนขายดีที่สุด? • "
    "ช่วงเวลาไหนขายดีที่สุด? • "
    "เมนูไหนควรโปรโมต? • "
    "สรุปยอดขายให้เจ้าของร้าน"
)


# =========================================================
# DOWNLOAD
# =========================================================

st.markdown(
    "## 📥 ข้อมูลและดาวน์โหลด"
)

st.markdown(
    '<p class="section-note">ตรวจสอบหรือดาวน์โหลดข้อมูลที่ระบบใช้ในการวิเคราะห์</p>',
    unsafe_allow_html=True
)


d1, d2 = st.columns(
    [1, 2]
)


with d1:

    st.download_button(

        "⬇️ ดาวน์โหลด Cleaned CSV",

        df.to_csv(
            index=False
        ).encode(
            "utf-8-sig"
        ),

        "cleaned_restaurant_sales.csv",

        "text/csv",

        use_container_width=True
    )


with d2:

    st.caption(
        "📄 ไฟล์นี้เป็นข้อมูลที่ผ่านขั้นตอน "
        "Data Preparation ของระบบแล้ว"
    )


# =========================================================
# DATA PREVIEW
# =========================================================

with st.expander(
    "🔎 ดูข้อมูลที่นำเข้า"
):

    st.dataframe(
        df,
        use_container_width=True,
        height=380
    )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
<div style="
text-align:center;
margin-top:45px;
padding-top:22px;
border-top:1px solid #E4E7EC;
color:#667085;
font-size:13px;
">
🍽️ Restaurant AI Analytics • Data Analytics + Generative AI
</div>
    """,
    unsafe_allow_html=True
)