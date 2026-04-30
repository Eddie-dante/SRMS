# app.py - SRMS: School Resource Management System by WeGEM (Edwin)
# Beautiful, Visible, User-Friendly - Just Like the HTML Version

import streamlit as st
import pandas as pd
import json
import uuid
import hashlib
import random
import string
from datetime import datetime, timedelta
from io import BytesIO
import base64
import qrcode
import sqlite3

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="SRMS - School Resource Management System",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== BEAUTIFUL CSS - MATCHING HTML VERSION ====================
def inject_master_css():
    st.markdown("""
    <style>
        /* ===== IMPORT FONTS ===== */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
        
        /* ===== ROOT VARIABLES ===== */
        :root {
            --bg-primary: #0a0e27;
            --bg-secondary: #1a1f4e;
            --accent: #e94560;
            --accent-glow: #ff6b8a;
            --gold: #d4af37;
            --gold-bright: #f0d060;
            --gold-dark: #b8941f;
            --surface: rgba(255, 255, 255, 0.08);
            --surface-hover: rgba(255, 255, 255, 0.12);
            --border: rgba(255, 255, 255, 0.12);
            --text: #ffffff;
            --text-secondary: rgba(255, 255, 255, 0.8);
            --text-muted: rgba(255, 255, 255, 0.55);
            --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.2);
            --shadow-md: 0 8px 24px rgba(0, 0, 0, 0.3);
            --shadow-lg: 0 16px 48px rgba(0, 0, 0, 0.4);
            --radius-sm: 8px;
            --radius-md: 12px;
            --radius-lg: 16px;
            --radius-xl: 20px;
        }
        
        /* ===== GLOBAL RESET ===== */
        * {
            font-family: 'Inter', 'Segoe UI', system-ui, sans-serif !important;
        }
        
        /* ===== MAIN BACKGROUND - DARK ELEGANT ===== */
        .stApp {
            background: linear-gradient(135deg, #0a0e27 0%, #1a1f4e 25%, #0f3460 50%, #1a1f4e 75%, #0a0e27 100%) !important;
            background-size: 400% 400% !important;
            animation: bgShift 20s ease infinite !important;
        }
        
        @keyframes bgShift {
            0% { background-position: 0% 50%; }
            25% { background-position: 100% 0%; }
            50% { background-position: 100% 100%; }
            75% { background-position: 0% 100%; }
            100% { background-position: 0% 50%; }
        }
        
        /* ===== SPARKLE OVERLAY ===== */
        .stApp::after {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: 
                radial-gradient(circle at 15% 25%, rgba(233, 69, 96, 0.06) 0%, transparent 45%),
                radial-gradient(circle at 85% 75%, rgba(212, 175, 55, 0.06) 0%, transparent 45%),
                radial-gradient(circle at 50% 50%, rgba(139, 92, 246, 0.04) 0%, transparent 50%),
                radial-gradient(circle at 25% 80%, rgba(6, 182, 212, 0.04) 0%, transparent 40%);
            pointer-events: none;
            z-index: 0;
        }
        
        /* ===== MAIN CONTENT AREA ===== */
        .main .block-container {
            position: relative;
            z-index: 1;
            background: rgba(255, 255, 255, 0.04) !important;
            backdrop-filter: blur(12px) !important;
            -webkit-backdrop-filter: blur(12px) !important;
            border-radius: 20px !important;
            padding: 2rem 3rem !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            box-shadow: 0 8px 40px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.03) !important;
            margin: 1rem auto !important;
            max-width: 1400px !important;
        }
        
        /* ===== HEADERS - GOLDEN GLOW ===== */
        h1 {
            font-size: 2.2em !important;
            font-weight: 900 !important;
            background: linear-gradient(180deg, #f0d060 0%, #d4af37 40%, #b8941f 100%) !important;
            -webkit-background-clip: text !important;
            -webkit-text-fill-color: transparent !important;
            background-clip: text !important;
            letter-spacing: 3px !important;
            margin-bottom: 1.2rem !important;
            filter: drop-shadow(0 4px 12px rgba(212, 175, 55, 0.4)) !important;
            animation: headerGlow 3s ease-in-out infinite;
            text-align: center !important;
            padding: 10px 0 !important;
        }
        
        @keyframes headerGlow {
            0%, 100% { filter: drop-shadow(0 4px 12px rgba(212, 175, 55, 0.4)); }
            50% { filter: drop-shadow(0 6px 24px rgba(212, 175, 55, 0.7)); }
        }
        
        h2 {
            font-size: 1.5em !important;
            font-weight: 800 !important;
            color: #ffffff !important;
            text-shadow: 0 2px 8px rgba(0, 0, 0, 0.5) !important;
            border-left: 4px solid #e94560 !important;
            padding-left: 18px !important;
            margin: 1.5rem 0 1rem 0 !important;
        }
        
        h3 {
            font-size: 1.15em !important;
            font-weight: 700 !important;
            color: #f0d060 !important;
            text-shadow: 0 1px 4px rgba(0, 0, 0, 0.5) !important;
            margin-bottom: 0.8rem !important;
        }
        
        /* ===== PARAGRAPHS ===== */
        p, label, .stMarkdown p {
            color: rgba(255, 255, 255, 0.85) !important;
            font-size: 0.95em !important;
        }
        
        /* ===== METRIC CARDS ===== */
        [data-testid="stMetric"] {
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.07), rgba(255, 255, 255, 0.03)) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 14px !important;
            padding: 18px 20px !important;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2) !important;
            transition: all 0.35s ease !important;
            position: relative;
            overflow: hidden;
        }
        
        [data-testid="stMetric"]::before {
            content: '';
            position: absolute;
            left: 0;
            top: 0;
            bottom: 0;
            width: 3px;
            background: linear-gradient(180deg, #e94560, #d4af37);
            border-radius: 3px 0 0 3px;
        }
        
        [data-testid="stMetric"]:hover {
            transform: translateY(-4px) !important;
            box-shadow: 0 12px 32px rgba(0, 0, 0, 0.4), 0 0 20px rgba(233, 69, 96, 0.1) !important;
            border-color: rgba(233, 69, 96, 0.3) !important;
        }
        
        [data-testid="stMetric"] label {
            color: rgba(255, 255, 255, 0.65) !important;
            font-size: 0.8em !important;
            font-weight: 500 !important;
            text-transform: uppercase !important;
            letter-spacing: 1.5px !important;
        }
        
        [data-testid="stMetricValue"] {
            font-size: 2.2em !important;
            font-weight: 900 !important;
            color: #ffffff !important;
            text-shadow: 0 2px 8px rgba(0, 0, 0, 0.3) !important;
        }
        
        /* ===== BUTTONS ===== */
        .stButton > button {
            background: linear-gradient(135deg, #e94560, #c62a47) !important;
            color: #ffffff !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            border-radius: 10px !important;
            padding: 10px 22px !important;
            font-weight: 600 !important;
            font-size: 14px !important;
            letter-spacing: 0.5px !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 16px rgba(233, 69, 96, 0.25) !important;
            cursor: pointer !important;
            position: relative;
            overflow: hidden;
        }
        
        .stButton > button::after {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(255,255,255,0.15) 0%, transparent 60%);
            opacity: 0;
            transition: opacity 0.3s;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 28px rgba(233, 69, 96, 0.4) !important;
            border-color: rgba(255, 255, 255, 0.35) !important;
        }
        
        .stButton > button:hover::after {
            opacity: 1;
        }
        
        .stButton > button:active {
            transform: scale(0.96) !important;
        }
        
        /* Secondary Button */
        .stButton > button[kind="secondary"] {
            background: linear-gradient(135deg, #0f3460, #1a5a8a) !important;
            box-shadow: 0 4px 16px rgba(15, 52, 96, 0.3) !important;
        }
        
        .stButton > button[kind="secondary"]:hover {
            box-shadow: 0 8px 28px rgba(15, 52, 96, 0.5) !important;
        }
        
        /* Primary Button - Gold */
        .stButton > button[kind="primary"] {
            background: linear-gradient(135deg, #d4af37, #b8941f) !important;
            color: #0a0e27 !important;
            font-weight: 700 !important;
            box-shadow: 0 4px 20px rgba(212, 175, 55, 0.3) !important;
        }
        
        .stButton > button[kind="primary"]:hover {
            box-shadow: 0 8px 32px rgba(212, 175, 55, 0.5) !important;
        }
        
        /* ===== INPUT FIELDS ===== */
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea,
        .stSelectbox > div > div > div,
        .stDateInput > div > div > input {
            background: rgba(255, 255, 255, 0.06) !important;
            color: #ffffff !important;
            border: 2px solid rgba(255, 255, 255, 0.12) !important;
            border-radius: 10px !important;
            padding: 12px 16px !important;
            font-size: 14px !important;
            transition: all 0.3s ease !important;
        }
        
        .stTextInput > div > div > input:focus,
        .stTextArea > div > div > textarea:focus {
            border-color: #e94560 !important;
            box-shadow: 0 0 0 3px rgba(233, 69, 96, 0.15), 0 0 20px rgba(233, 69, 96, 0.08) !important;
            background: rgba(255, 255, 255, 0.1) !important;
        }
        
        .stTextInput > div > div > input::placeholder {
            color: rgba(255, 255, 255, 0.35) !important;
        }
        
        /* Select box dropdown */
        .stSelectbox [data-baseweb="select"] {
            background: rgba(15, 52, 96, 0.6) !important;
        }
        
        .stSelectbox [data-baseweb="select"] option {
            background: #1a1f4e !important;
            color: white !important;
        }
        
        /* ===== DATAFRAMES / TABLES ===== */
        [data-testid="stDataFrame"] {
            background: rgba(255, 255, 255, 0.03) !important;
            border-radius: 14px !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            overflow: hidden !important;
        }
        
        [data-testid="stDataFrame"] th {
            background: rgba(10, 14, 39, 0.9) !important;
            color: #f0d060 !important;
            font-weight: 700 !important;
            padding: 14px !important;
            font-size: 12px !important;
            text-transform: uppercase;
            letter-spacing: 1px;
            border-bottom: 2px solid rgba(233, 69, 96, 0.3) !important;
        }
        
        [data-testid="stDataFrame"] td {
            color: rgba(255, 255, 255, 0.9) !important;
            padding: 10px 14px !important;
            border-bottom: 1px solid rgba(255, 255, 255, 0.04) !important;
        }
        
        [data-testid="stDataFrame"] tr:hover td {
            background: rgba(233, 69, 96, 0.06) !important;
        }
        
        /* ===== EXPANDERS ===== */
        [data-testid="stExpander"] {
            background: rgba(255, 255, 255, 0.03) !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-radius: 14px !important;
            overflow: hidden !important;
        }
        
        [data-testid="stExpander"] summary {
            background: rgba(255, 255, 255, 0.04) !important;
            color: #ffffff !important;
            font-weight: 600 !important;
            padding: 14px 20px !important;
            border-radius: 14px !important;
        }
        
        [data-testid="stExpander"] summary:hover {
            background: rgba(233, 69, 96, 0.1) !important;
        }
        
        /* ===== TABS ===== */
        [data-baseweb="tab-list"] {
            background: rgba(255, 255, 255, 0.03) !important;
            border-radius: 14px !important;
            padding: 6px !important;
            gap: 4px !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
        }
        
        [data-baseweb="tab"] {
            color: rgba(255, 255, 255, 0.7) !important;
            border-radius: 10px !important;
            padding: 10px 20px !important;
            font-weight: 500 !important;
            transition: all 0.3s ease !important;
        }
        
        [data-baseweb="tab"]:hover {
            background: rgba(233, 69, 96, 0.12) !important;
            color: white !important;
        }
        
        [data-baseweb="tab"][aria-selected="true"] {
            background: linear-gradient(135deg, rgba(233, 69, 96, 0.5), rgba(197, 42, 71, 0.5)) !important;
            color: white !important;
            font-weight: 600 !important;
            box-shadow: 0 4px 12px rgba(233, 69, 96, 0.2) !important;
        }
        
        /* ===== RADIO BUTTONS ===== */
        .stRadio > div {
            background: rgba(255, 255, 255, 0.03) !important;
            border-radius: 12px !important;
            padding: 8px !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
        }
        
        .stRadio label {
            color: rgba(255, 255, 255, 0.85) !important;
        }
        
        /* ===== SIDEBAR ===== */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, rgba(10, 14, 39, 0.97), rgba(15, 52, 96, 0.97)) !important;
            backdrop-filter: blur(15px) !important;
            border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
            box-shadow: 4px 0 30px rgba(0, 0, 0, 0.4) !important;
        }
        
        [data-testid="stSidebar"] * {
            color: #ffffff !important;
        }
        
        [data-testid="stSidebar"] button {
            background: rgba(255, 255, 255, 0.04) !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-radius: 10px !important;
            padding: 10px 16px !important;
            margin: 3px 0 !important;
            transition: all 0.3s ease !important;
            font-weight: 500 !important;
        }
        
        [data-testid="stSidebar"] button:hover {
            background: rgba(233, 69, 96, 0.15) !important;
            border-color: rgba(233, 69, 96, 0.3) !important;
            transform: translateX(4px) !important;
        }
        
        /* ===== ALERTS ===== */
        .stAlert {
            border-radius: 12px !important;
            border: 1px solid !important;
            backdrop-filter: blur(8px) !important;
        }
        
        .stSuccess { 
            background: rgba(40, 167, 69, 0.12) !important; 
            border-color: rgba(40, 167, 69, 0.3) !important; 
        }
        .stSuccess p { color: #4ade80 !important; }
        
        .stError { 
            background: rgba(220, 53, 69, 0.12) !important; 
            border-color: rgba(220, 53, 69, 0.3) !important; 
        }
        .stError p { color: #f87171 !important; }
        
        .stWarning { 
            background: rgba(255, 193, 7, 0.12) !important; 
            border-color: rgba(255, 193, 7, 0.3) !important; 
        }
        .stWarning p { color: #fbbf24 !important; }
        
        .stInfo { 
            background: rgba(23, 162, 184, 0.12) !important; 
            border-color: rgba(23, 162, 184, 0.3) !important; 
        }
        .stInfo p { color: #22d3ee !important; }
        
        /* ===== FORMS ===== */
        [data-testid="stForm"] {
            background: rgba(255, 255, 255, 0.03) !important;
            border-radius: 16px !important;
            padding: 25px !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            backdrop-filter: blur(10px) !important;
        }
        
        /* ===== DIVIDER ===== */
        hr {
            border: none !important;
            height: 1px !important;
            background: linear-gradient(90deg, transparent, rgba(233, 69, 96, 0.3), rgba(212, 175, 55, 0.3), transparent) !important;
            margin: 20px 0 !important;
        }
        
        /* ===== SCROLLBAR ===== */
        ::-webkit-scrollbar { width: 8px; }
        ::-webkit-scrollbar-track { background: rgba(255, 255, 255, 0.03); border-radius: 10px; }
        ::-webkit-scrollbar-thumb { background: linear-gradient(180deg, #e94560, #d4af37); border-radius: 10px; }
        ::-webkit-scrollbar-thumb:hover { background: linear-gradient(180deg, #ff6b8a, #f0d060); }
        
        /* ===== RESPONSIVE ===== */
        @media (max-width: 768px) {
            .main .block-container { padding: 1rem !important; }
            h1 { font-size: 1.5em !important; }
            [data-testid="stMetricValue"] { font-size: 1.5em !important; }
        }
    </style>
    """, unsafe_allow_html=True)

# ==================== DATABASE ====================
@st.cache_resource
def get_db():
    conn = sqlite3.connect('srms.db', check_same_thread=False)
    c = conn.cursor()
    
    tables = [
        '''CREATE TABLE IF NOT EXISTS organizations (
            id TEXT PRIMARY KEY, name TEXT, invite_code TEXT UNIQUE,
            admin_name TEXT, admin_email TEXT, admin_phone TEXT, address TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''',
        '''CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY, org_id TEXT, name TEXT, email TEXT, phone TEXT,
            role TEXT, password TEXT, invite_code TEXT, staff_id TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''',
        '''CREATE TABLE IF NOT EXISTS books (
            id TEXT PRIMARY KEY, org_id TEXT, title TEXT, type TEXT, quantity INTEGER)''',
        '''CREATE TABLE IF NOT EXISTS members (
            id TEXT PRIMARY KEY, org_id TEXT, name TEXT, member_id TEXT)''',
        '''CREATE TABLE IF NOT EXISTS teachers (
            id TEXT PRIMARY KEY, org_id TEXT, name TEXT, subjects TEXT,
            classes TEXT, class_assigned TEXT)''',
        '''CREATE TABLE IF NOT EXISTS borrowed_books (
            id TEXT PRIMARY KEY, org_id TEXT, student_name TEXT, adm_number TEXT,
            form TEXT, stream TEXT, book_title TEXT, book_number TEXT,
            borrow_date TEXT, return_date TEXT, actual_return_date TEXT,
            returned INTEGER DEFAULT 0, lending_type TEXT DEFAULT 'individual')''',
        '''CREATE TABLE IF NOT EXISTS furniture (
            id TEXT PRIMARY KEY, org_id TEXT, student_name TEXT, adm_number TEXT,
            chair_number TEXT, locker_number TEXT, allocation_date TEXT,
            return_date TEXT, returned INTEGER DEFAULT 0)''',
        '''CREATE TABLE IF NOT EXISTS class_lists (
            id TEXT PRIMARY KEY, org_id TEXT, class_name TEXT, data TEXT)''',
        '''CREATE TABLE IF NOT EXISTS audit_log (
            id TEXT PRIMARY KEY, org_id TEXT, user_name TEXT, action TEXT, details TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''',
        '''CREATE TABLE IF NOT EXISTS chat_messages (
            id TEXT PRIMARY KEY, org_id TEXT, from_user TEXT, to_user TEXT,
            message TEXT, read INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)'''
    ]
    
    for table in tables:
        c.execute(table)
    
    conn.commit()
    return conn

# ==================== HELPERS ====================
def gen_id(): return str(uuid.uuid4())
def hash_pw(pw): return hashlib.sha256(pw.encode()).hexdigest()
def gen_code(): return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

def audit(org_id, action, details):
    conn = get_db()
    user = st.session_state.get('user', {}).get('name', 'System')
    conn.cursor().execute('INSERT INTO audit_log (id, org_id, user_name, action, details) VALUES (?,?,?,?,?)',
                          (gen_id(), org_id, user, action, details))
    conn.commit()

def gen_qr(data):
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buf = BytesIO()
    img.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode()

# ==================== SESSION STATE ====================
def init_session():
    defaults = {
        'user': None, 'org_id': None, 'org_name': None, 'role': None,
        'invite_code': None, 'authenticated': False, 'page': '📊 Dashboard',
        'chat_user': None, 'edit_member': None, 'load_class': None,
        'load_book': None, 'furn_class': None, 'imported': None
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

# ==================== AUTH PAGE - BEAUTIFUL STARTUP ====================
def auth_page():
    inject_master_css()
    
    # Centered layout
    _, center, _ = st.columns([1, 1.5, 1])
    
    with center:
        st.markdown('<br><br>', unsafe_allow_html=True)
        
        # SRMS Logo
        st.markdown("""
        <div style="text-align:center; margin-bottom: 10px;">
            <div style="display:inline-block; width:100px; height:100px; 
                        background:linear-gradient(135deg,#d4af37,#f0d060,#d4af37);
                        border-radius:25px; display:flex; align-items:center; justify-content:center;
                        font-size:38px; font-weight:900; color:#0a0e27;
                        box-shadow:0 15px 50px rgba(212,175,55,0.4), 0 0 80px rgba(212,175,55,0.2);
                        animation: pulse 2.5s ease-in-out infinite;
                        margin: 0 auto;">
                SRMS
            </div>
        </div>
        <style>
            @keyframes pulse {
                0%,100% { box-shadow:0 15px 50px rgba(212,175,55,0.4),0 0 80px rgba(212,175,55,0.2); }
                50% { box-shadow:0 15px 70px rgba(212,175,55,0.7),0 0 120px rgba(212,175,55,0.4); }
            }
        </style>
        
        <h1 style="font-size:3em !important; letter-spacing:10px !important;">SRMS</h1>
        <p style="text-align:center; color:rgba(255,255,255,0.75); font-size:1.2em; letter-spacing:3px; font-weight:300;">
            School Resource Management System
        </p>
        <p style="text-align:center; color:#d4af37; font-size:1.05em; font-weight:500; letter-spacing:1px;">
            by <strong style="color:#f0d060;">WeGEM</strong> (Edwin)
        </p>
        """, unsafe_allow_html=True)
        
        st.markdown('<hr>', unsafe_allow_html=True)
        
        # Tabs
        tab1, tab2, tab3 = st.tabs(["🔑 **Login**", "📝 **Sign Up**", "🏫 **Create School**"])
        
        with tab1:
            with st.form("login_f"):
                st.markdown('<p style="color:rgba(255,255,255,0.6);font-size:0.9em;">Welcome back! Please sign in.</p>', unsafe_allow_html=True)
                name = st.text_input("👤 Full Name", key="l_name", placeholder="Your registered name")
                school = st.text_input("🏢 School Name", key="l_school", placeholder="School name")
                code = st.text_input("🔑 Invite Code", key="l_code", placeholder="Invite code from admin")
                password = st.text_input("🔒 Password", type="password", key="l_pw", placeholder="Your password")
                
                if st.form_submit_button("🔑 Login to Dashboard", use_container_width=True):
                    if not all([name, school, code, password]):
                        st.error("⚠️ Please fill all fields")
                    else:
                        conn = get_db()
                        c = conn.cursor()
                        c.execute("SELECT * FROM organizations WHERE name=?", (school,))
                        org = c.fetchone()
                        if not org:
                            st.error("❌ School not found")
                        elif code.upper() != org[2]:
                            st.error("❌ Invalid invite code")
                        else:
                            hp = hash_pw(password)
                            c.execute("SELECT * FROM users WHERE org_id=? AND name=? AND password=?", (org[0], name, hp))
                            user = c.fetchone()
                            if not user:
                                st.error("❌ Invalid credentials")
                            else:
                                st.session_state.user = {'id':user[0],'name':user[2],'email':user[3],'role':user[5],'staff_id':user[7]}
                                st.session_state.org_id = org[0]
                                st.session_state.org_name = org[1]
                                st.session_state.role = user[5]
                                st.session_state.invite_code = org[2]
                                st.session_state.authenticated = True
                                audit(org[0], 'Login', f"{name} logged in")
                                st.rerun()
        
        with tab2:
            with st.form("signup_f"):
                st.markdown('<p style="color:rgba(255,255,255,0.6);font-size:0.9em;">Join your school\'s system.</p>', unsafe_allow_html=True)
                name = st.text_input("👤 Full Name", key="s_name", placeholder="Your full name")
                email = st.text_input("📧 Email", key="s_email", placeholder="your@email.com")
                phone = st.text_input("📞 Phone", key="s_phone", placeholder="+1234567890")
                school = st.text_input("🏢 School Name", key="s_school", placeholder="School name")
                code = st.text_input("🔑 Invite Code", key="s_code", placeholder="From admin")
                sid = st.text_input("🪪 Staff ID (Optional)", key="s_sid", placeholder="Employee ID")
                pw = st.text_input("🔒 Password", type="password", key="s_pw", placeholder="Min 6 characters")
                
                if st.form_submit_button("📝 Create Account", use_container_width=True):
                    if not all([name, email, school, code, pw]):
                        st.error("⚠️ Fill all required fields")
                    elif len(pw) < 6:
                        st.error("⚠️ Password min 6 characters")
                    else:
                        conn = get_db()
                        c = conn.cursor()
                        c.execute("SELECT * FROM organizations WHERE name=?", (school,))
                        org = c.fetchone()
                        if not org:
                            st.error("❌ School not found")
                        elif code.upper() != org[2]:
                            st.error("❌ Invalid invite code")
                        else:
                            c.execute("SELECT * FROM users WHERE org_id=? AND email=?", (org[0], email))
                            if c.fetchone():
                                st.error("⚠️ Email already registered")
                            else:
                                uid = gen_id()
                                hp = hash_pw(pw)
                                sfid = sid or f"STF-{uid[:8].upper()}"
                                c.execute("INSERT INTO users VALUES (?,?,?,?,?,?,?,?,?)",
                                         (uid, org[0], name, email, phone, 'teacher', hp, code.upper(), sfid))
                                conn.commit()
                                audit(org[0], 'Signup', f"{name} signed up")
                                st.success(f"✅ Account created! Staff ID: **{sfid}**")
                                st.info("Go to Login tab to sign in.")
        
        with tab3:
            with st.form("create_f"):
                st.markdown('<p style="color:rgba(255,255,255,0.6);font-size:0.9em;">Set up your school.</p>', unsafe_allow_html=True)
                sname = st.text_input("🏢 School Name", key="c_school", placeholder="e.g., Sunshine High")
                addr = st.text_input("📍 Address", key="c_addr", placeholder="School location")
                aname = st.text_input("👤 Admin Name", key="c_admin", placeholder="Administrator")
                aemail = st.text_input("📧 Admin Email", key="c_email", placeholder="admin@school.com")
                aphone = st.text_input("📞 Admin Phone", key="c_phone", placeholder="+1234567890")
                pw = st.text_input("🔒 Password", type="password", key="c_pw", placeholder="Min 8 characters")
                pw2 = st.text_input("🔒 Confirm Password", type="password", key="c_pw2", placeholder="Re-enter")
                
                if st.form_submit_button("🚀 Create School", use_container_width=True):
                    if not all([sname, aname, aemail, pw]):
                        st.error("⚠️ Fill required fields")
                    elif pw != pw2:
                        st.error("⚠️ Passwords don't match")
                    elif len(pw) < 8:
                        st.error("⚠️ Password min 8 characters")
                    else:
                        conn = get_db()
                        c = conn.cursor()
                        code = gen_code()
                        oid = gen_id()
                        uid = gen_id()
                        hp = hash_pw(pw)
                        c.execute("INSERT INTO organizations VALUES (?,?,?,?,?,?,?)",
                                 (oid, sname, code, aname, aemail, aphone, addr))
                        c.execute("INSERT INTO users VALUES (?,?,?,?,?,?,?,?,?)",
                                 (uid, oid, aname, aemail, aphone, 'admin', hp, code, 'ADMIN-001'))
                        conn.commit()
                        
                        st.success("🎉 School created!")
                        st.markdown(f"""
                        <div style="background:linear-gradient(135deg,rgba(212,175,55,0.15),rgba(233,69,96,0.15));
                                    border:2px dashed rgba(212,175,55,0.4);border-radius:16px;padding:20px;
                                    text-align:center;margin:15px 0;">
                            <p style="color:rgba(255,255,255,0.7);margin:0;">🏫 Invite Code</p>
                            <p style="font-size:2.2em;font-weight:900;letter-spacing:6px;color:#f0d060;
                                      font-family:monospace;margin:8px 0;">{code}</p>
                            <p style="color:rgba(255,255,255,0.5);font-size:0.85em;">Share with staff</p>
                        </div>
                        """, unsafe_allow_html=True)
                        st.info("Go to Login tab to access your dashboard.")

# ==================== SIDEBAR ====================
def sidebar():
    with st.sidebar:
        st.markdown('<br>', unsafe_allow_html=True)
        
        # Logo and info
        st.markdown(f"""
        <div style="text-align:center;">
            <div style="width:55px;height:55px;background:linear-gradient(135deg,#d4af37,#f0d060,#d4af37);
                        border-radius:14px;display:inline-flex;align-items:center;justify-content:center;
                        font-size:20px;font-weight:900;color:#0a0e27;margin-bottom:8px;
                        box-shadow:0 8px 25px rgba(212,175,55,0.3);">SRMS</div>
            <p style="color:white;font-weight:700;font-size:1em;margin:5px 0;">{st.session_state.org_name}</p>
            <p style="color:rgba(255,255,255,0.6);font-size:0.8em;margin:3px 0;">👤 {st.session_state.user['name']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Role badge
        role_colors = {'admin': '#e94560', 'teacher': '#0f3460', 'librarian': '#28a745'}
        rc = role_colors.get(st.session_state.role, '#e94560')
        st.markdown(f"""
        <div style="text-align:center;margin:8px 0;">
            <span style="background:{rc};color:white;padding:4px 14px;border-radius:20px;
                        font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:1px;">
                {st.session_state.role}
            </span>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<hr>', unsafe_allow_html=True)
        
        # Navigation
        nav_items = [
            ("📊", "Dashboard"),
            ("📚", "Book Catalog"),
            ("📖", "Book Issuing"),
            ("👤", "Individual Lending"),
            ("🪑", "Furniture"),
            ("↩️", "Return Items"),
            ("📋", "Borrowed Books"),
            ("👥", "Members"),
            ("👨‍🏫", "Teachers"),
            ("📋", "Class Lists"),
            ("📱", "QR Codes"),
            ("💬", "Staff Chat"),
            ("🔍", "System Overview"),
            ("📝", "Audit Log"),
            ("📈", "Reports"),
            ("🖼️", "Theme"),
            ("⚙️", "Settings"),
        ]
        
        for icon, label in nav_items:
            if st.sidebar.button(f"{icon}  {label}", key=f"nav_{label}", use_container_width=True):
                st.session_state.page = label
                st.rerun()
        
        st.sidebar.markdown('<hr>', unsafe_allow_html=True)
        
        if st.sidebar.button("🚪 Logout", use_container_width=True):
            audit(st.session_state.org_id, 'Logout', st.session_state.user['name'])
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.rerun()
        
        st.sidebar.markdown('<p style="text-align:center;color:#d4af37;font-size:0.75em;font-weight:600;">by WeGEM (Edwin)</p>', unsafe_allow_html=True)

# ==================== DASHBOARD ====================
def dashboard():
    st.markdown('<h1>📊 Dashboard Overview</h1>', unsafe_allow_html=True)
    
    conn = get_db()
    oid = st.session_state.org_id
    
    books = pd.read_sql("SELECT * FROM books WHERE org_id=?", conn, params=(oid,))
    borrowed = pd.read_sql("SELECT * FROM borrowed_books WHERE org_id=? AND returned=0", conn, params=(oid,))
    members = pd.read_sql("SELECT * FROM members WHERE org_id=?", conn, params=(oid,))
    teachers = pd.read_sql("SELECT * FROM teachers WHERE org_id=?", conn, params=(oid,))
    furniture = pd.read_sql("SELECT * FROM furniture WHERE org_id=? AND returned=0", conn, params=(oid,))
    
    tb = books['quantity'].sum() if not books.empty else 0
    bb = len(borrowed)
    ov = 0
    if not borrowed.empty:
        today = datetime.now().date()
        for _, r in borrowed.iterrows():
            try:
                if datetime.strptime(r['return_date'], '%Y-%m-%d').date() < today:
                    ov += 1
            except: pass
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("📚 Total Books", tb)
    c2.metric("📖 Borrowed", bb)
    c3.metric("📗 Available", tb - bb)
    c4.metric("🔴 Overdue", ov)
    
    c5, c6, c7, c8 = st.columns(4)
    c5.metric("👥 Members", len(members))
    c6.metric("👨‍🏫 Teachers", len(teachers))
    c7.metric("🪑 Furniture", len(furniture))
    c8.metric("✅ Active Loans", bb)
    
    # Invite code banner
    st.markdown(f"""
    <div style="background:rgba(255,255,255,0.05);border:2px dashed rgba(233,69,96,0.3);
                border-radius:16px;padding:20px;text-align:center;margin:20px 0;">
        <p style="color:rgba(255,255,255,0.6);font-size:0.85em;margin:0;">🏫 School Invite Code</p>
        <p style="font-size:2.4em;font-weight:900;letter-spacing:6px;color:#f0d060;
                  font-family:monospace;margin:8px 0;">{st.session_state.invite_code}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Recent activity
    st.markdown('<h2>📝 Recent Activity</h2>', unsafe_allow_html=True)
    logs = pd.read_sql("SELECT * FROM audit_log WHERE org_id=? ORDER BY created_at DESC LIMIT 6", conn, params=(oid,))
    if not logs.empty:
        for _, l in logs.iterrows():
            st.markdown(f"""
            <div style="background:rgba(255,255,255,0.035);border-radius:10px;padding:10px 15px;
                        margin:4px 0;border-left:3px solid rgba(233,69,96,0.4);">
                <small style="color:rgba(255,255,255,0.45);">{l['created_at'][:19]}</small>
                <strong style="color:#d4af37;"> {l['user_name']}</strong>
                <span style="color:rgba(255,255,255,0.8);"> - {l['action']}: {l['details']}</span>
            </div>
            """, unsafe_allow_html=True)

# ==================== BOOK CATALOG ====================
def catalog():
    st.markdown('<h1>📚 Book Catalog</h1>', unsafe_allow_html=True)
    conn = get_db()
    oid = st.session_state.org_id
    
    with st.expander("➕ Add / Update Book"):
        c1, c2, c3 = st.columns([2,1,1])
        title = c1.text_input("Book Title", placeholder="Enter title")
        btype = c2.selectbox("Type", ["Textbook","Novel","Reference","Magazine","Other"])
        qty = c3.number_input("Quantity", min_value=1, value=1)
        if st.button("📖 Add/Update Book", use_container_width=True):
            if title:
                c = conn.cursor()
                ex = pd.read_sql("SELECT * FROM books WHERE org_id=? AND title=?", conn, params=(oid,title))
                if not ex.empty:
                    nq = ex.iloc[0]['quantity'] + qty
                    c.execute("UPDATE books SET quantity=?, type=? WHERE org_id=? AND title=?", (nq, btype, oid, title))
                    conn.commit()
                    audit(oid, 'Book Updated', f"'{title}' +{qty} (Total:{nq})")
                    st.success(f"✅ Updated! Total: {nq}")
                else:
                    c.execute("INSERT INTO books VALUES (?,?,?,?,?)", (gen_id(), oid, title, btype, qty))
                    conn.commit()
                    audit(oid, 'Book Added', f"'{title}' x{qty}")
                    st.success(f"✅ Added '{title}'!")
                st.rerun()
    
    st.markdown('<h2>📋 Catalog</h2>', unsafe_allow_html=True)
    books = pd.read_sql("SELECT * FROM books WHERE org_id=? ORDER BY title", conn, params=(oid,))
    if not books.empty:
        for _, b in books.iterrows():
            q = b['quantity']
            badge = "🔴 Out" if q==0 else ("🟡 Low" if q<5 else "🟢 OK")
            c1, c2 = st.columns([5,1])
            with c1:
                st.markdown(f"""
                <div style="background:rgba(255,255,255,0.04);border-radius:10px;padding:12px;margin:4px 0;">
                    📖 <strong>{b['title']}</strong> | {b['type']} | Qty: <strong>{q}</strong> | {badge}
                </div>
                """, unsafe_allow_html=True)
            with c2:
                if st.button("🗑️", key=f"db_{b['id']}"):
                    conn.cursor().execute("DELETE FROM books WHERE id=?", (b['id'],))
                    conn.commit()
                    st.rerun()

# ==================== BOOK ISSUING ====================
def book_issuing():
    st.markdown('<h1>📖 Bulk Book Issuing</h1>', unsafe_allow_html=True)
    conn = get_db()
    oid = st.session_state.org_id
    
    c1, c2 = st.columns(2)
    books = pd.read_sql("SELECT * FROM books WHERE org_id=? AND quantity>0", conn, params=(oid,))
    classes = pd.read_sql("SELECT * FROM class_lists WHERE org_id=?", conn, params=(oid,))
    
    book_opts = ["-- Select --"] + books['title'].tolist() if not books.empty else ["-- Select --"]
    class_opts = ["-- Select --"] + classes['class_name'].tolist() if not classes.empty else ["-- Select --"]
    
    sel_book = c1.selectbox("📚 Book", book_opts)
    sel_class = c2.selectbox("📋 Class", class_opts)
    
    c3, c4 = st.columns(2)
    bdate = c3.date_input("Issue Date", datetime.now())
    rdate = c4.date_input("Return Date", datetime.now()+timedelta(14))
    
    if st.button("📋 Load Class", use_container_width=True):
        if sel_class != "-- Select --" and sel_book != "-- Select --":
            st.session_state.load_class = sel_class
            st.session_state.load_book = sel_book
            st.rerun()
    
    if st.session_state.load_class and st.session_state.load_book:
        cd = pd.read_sql("SELECT * FROM class_lists WHERE org_id=? AND class_name=?", conn, params=(oid, st.session_state.load_class))
        if not cd.empty:
            students = json.loads(cd.iloc[0]['data'])
            st.markdown(f'<h2>Assign "{st.session_state.load_book}"</h2>', unsafe_allow_html=True)
            
            data = []
            for s in students:
                ex = pd.read_sql("SELECT * FROM borrowed_books WHERE org_id=? AND adm_number=? AND book_title=? AND returned=0",
                                conn, params=(oid, s['adm'], st.session_state.load_book))
                done = not ex.empty
                data.append({"Select": not done, "Student": s['name'], "ADM": s['adm'],
                            "Book No": ex.iloc[0]['book_number'] if done else "", "Status": "✅ Issued" if done else "⏳ Pending"})
            
            df = pd.DataFrame(data)
            edf = st.data_editor(df, hide_index=True, use_container_width=True, disabled=["Student","ADM","Status"])
            
            if st.button("✅ Issue Books", type="primary", use_container_width=True):
                ta = edf[edf['Select']==True]
                if ta.empty:
                    st.error("No students selected")
                else:
                    bk = books[books['title']==st.session_state.load_book].iloc[0]
                    if len(ta) > bk['quantity']:
                        st.error(f"Only {bk['quantity']} available!")
                    else:
                        c = conn.cursor()
                        for _, r in ta.iterrows():
                            if r['Book No']:
                                c.execute("""INSERT INTO borrowed_books (id,org_id,student_name,adm_number,book_title,book_number,borrow_date,return_date,lending_type)
                                    VALUES (?,?,?,?,?,?,?,?,?)""",
                                    (gen_id(), oid, r['Student'], r['ADM'], st.session_state.load_book, r['Book No'], str(bdate), str(rdate), 'class'))
                                c.execute("UPDATE books SET quantity=quantity-1 WHERE org_id=? AND title=?", (oid, st.session_state.load_book))
                        conn.commit()
                        audit(oid, 'Books Issued', f"{len(ta)} copies to {st.session_state.load_class}")
                        st.success(f"✅ Issued {len(ta)} books!")
                        st.session_state.load_class = None
                        st.session_state.load_book = None
                        st.rerun()

# ==================== INDIVIDUAL LENDING ====================
def lending():
    st.markdown('<h1>👤 Individual Lending</h1>', unsafe_allow_html=True)
    conn = get_db()
    oid = st.session_state.org_id
    
    with st.form("lend_f"):
        c1, c2 = st.columns(2)
        name = c1.text_input("Student Name")
        adm = c1.text_input("ADM Number")
        form = c1.text_input("Form/Class")
        book_title = c1.selectbox("Book", ["-- Select --"] + pd.read_sql(
            "SELECT title FROM books WHERE org_id=? AND quantity>0", conn, params=(oid,))['title'].tolist())
        stream = c2.text_input("Stream")
        book_no = c2.text_input("Book Number")
        bdate = c2.date_input("Borrow Date", datetime.now())
        rdate = c2.date_input("Return Date", datetime.now()+timedelta(14))
        
        if st.form_submit_button("📖 Lend Book", use_container_width=True):
            if not all([name, adm, book_title!="-- Select --", book_no]):
                st.error("Fill all fields")
            else:
                bk = pd.read_sql("SELECT * FROM books WHERE org_id=? AND title=?", conn, params=(oid, book_title))
                if bk.empty or bk.iloc[0]['quantity']<=0:
                    st.error("Out of stock")
                else:
                    c = conn.cursor()
                    c.execute("""INSERT INTO borrowed_books (id,org_id,student_name,adm_number,form,stream,book_title,book_number,borrow_date,return_date,lending_type)
                        VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
                        (gen_id(), oid, name, adm, form, stream, book_title, book_no, str(bdate), str(rdate), 'individual'))
                    c.execute("UPDATE books SET quantity=quantity-1 WHERE org_id=? AND title=?", (oid, book_title))
                    conn.commit()
                    audit(oid, 'Book Lent', f"{name} - {book_title}")
                    st.success(f"✅ Lent to {name}!")
                    st.rerun()
    
    st.markdown('<h2>Recent Lendings</h2>', unsafe_allow_html=True)
    lends = pd.read_sql("SELECT * FROM borrowed_books WHERE org_id=? AND lending_type='individual' AND returned=0 ORDER BY created_at DESC LIMIT 10",
                        conn, params=(oid,))
    if not lends.empty:
        for _, l in lends.iterrows():
            c1, c2 = st.columns([5,1])
            with c1:
                st.markdown(f"📖 **{l['student_name']}** → *{l['book_title']}* (#{l['book_number']}) | Due: {l['return_date']}")
            with c2:
                if st.button("↩️", key=f"rl_{l['id']}"):
                    c = conn.cursor()
                    c.execute("UPDATE borrowed_books SET returned=1, actual_return_date=? WHERE id=?", (str(datetime.now().date()), l['id']))
                    c.execute("UPDATE books SET quantity=quantity+1 WHERE org_id=? AND title=?", (oid, l['book_title']))
                    conn.commit()
                    st.rerun()

# ==================== FURNITURE ====================
def furniture_page():
    st.markdown('<h1>🪑 Furniture Allocation</h1>', unsafe_allow_html=True)
    conn = get_db()
    oid = st.session_state.org_id
    
    classes = pd.read_sql("SELECT * FROM class_lists WHERE org_id=?", conn, params=(oid,))
    copts = ["-- Select --"] + classes['class_name'].tolist() if not classes.empty else ["-- Select --"]
    
    c1, c2 = st.columns(2)
    sel = c1.selectbox("Class", copts)
    date = c2.date_input("Date", datetime.now())
    
    if st.button("📋 Load", use_container_width=True):
        if sel != "-- Select --":
            st.session_state.furn_class = sel
            st.rerun()
    
    if st.session_state.furn_class:
        cd = pd.read_sql("SELECT * FROM class_lists WHERE org_id=? AND class_name=?", conn, params=(oid, st.session_state.furn_class))
        if not cd.empty:
            students = json.loads(cd.iloc[0]['data'])
            st.markdown(f'<h2>Assign to {st.session_state.furn_class}</h2>', unsafe_allow_html=True)
            
            data = []
            for s in students:
                ex = pd.read_sql("SELECT * FROM furniture WHERE org_id=? AND adm_number=? AND returned=0", conn, params=(oid, s['adm']))
                done = not ex.empty
                data.append({"Select": not done, "Student": s['name'], "ADM": s['adm'],
                            "Chair": ex.iloc[0]['chair_number'] if done else "",
                            "Locker": ex.iloc[0]['locker_number'] if done else "",
                            "Status": "✅ Done" if done else "⏳ Pending"})
            
            df = pd.DataFrame(data)
            edf = st.data_editor(df, hide_index=True, use_container_width=True, disabled=["Student","ADM","Status"])
            
            if st.button("✅ Assign", type="primary", use_container_width=True):
                ta = edf[edf['Select']==True]
                if ta.empty:
                    st.error("No students selected")
                else:
                    c = conn.cursor()
                    for _, r in ta.iterrows():
                        if r['Chair'] or r['Locker']:
                            c.execute("INSERT INTO furniture (id,org_id,student_name,adm_number,chair_number,locker_number,allocation_date) VALUES (?,?,?,?,?,?,?)",
                                     (gen_id(), oid, r['Student'], r['ADM'], r['Chair'] or None, r['Locker'] or None, str(date)))
                    conn.commit()
                    audit(oid, 'Furniture', f"Allocated to {len(ta)}")
                    st.success(f"✅ Done! {len(ta)} students")
                    st.session_state.furn_class = None
                    st.rerun()
    
    st.markdown('<h2>Current Allocations</h2>', unsafe_allow_html=True)
    furn = pd.read_sql("SELECT * FROM furniture WHERE org_id=? ORDER BY created_at DESC", conn, params=(oid,))
    if not furn.empty:
        for _, f in furn.iterrows():
            c1, c2 = st.columns([5,1])
            with c1:
                st.markdown(f"🪑 **{f['student_name']}** | Chair: {f['chair_number'] or '-'} | Locker: {f['locker_number'] or '-'} | {f['allocation_date']}")
            with c2:
                if not f['returned'] and st.button("↩️", key=f"rf_{f['id']}"):
                    conn.cursor().execute("UPDATE furniture SET returned=1, return_date=? WHERE id=?", (str(datetime.now().date()), f['id']))
                    conn.commit()
                    st.rerun()

# ==================== RETURN ====================
def return_page():
    st.markdown('<h1>↩️ Return Items</h1>', unsafe_allow_html=True)
    conn = get_db()
    oid = st.session_state.org_id
    
    search = st.text_input("🔍 Search by name, ADM, or number")
    if search:
        books = pd.read_sql("SELECT * FROM borrowed_books WHERE org_id=? AND returned=0 AND (student_name LIKE ? OR adm_number LIKE ? OR book_number LIKE ?)",
                           conn, params=(oid, f"%{search}%", f"%{search}%", f"%{search}%"))
        furniture = pd.read_sql("SELECT * FROM furniture WHERE org_id=? AND returned=0 AND (student_name LIKE ? OR adm_number LIKE ? OR chair_number LIKE ? OR locker_number LIKE ?)",
                               conn, params=(oid, f"%{search}%", f"%{search}%", f"%{search}%", f"%{search}%"))
        
        if not books.empty:
            st.subheader("📚 Books")
            for _, b in books.iterrows():
                c1, c2 = st.columns([5,1])
                with c1:
                    st.markdown(f"📖 **{b['student_name']}** → *{b['book_title']}* (#{b['book_number']})")
                with c2:
                    if st.button("↩️", key=f"sr_{b['id']}"):
                        c = conn.cursor()
                        c.execute("UPDATE borrowed_books SET returned=1, actual_return_date=? WHERE id=?", (str(datetime.now().date()), b['id']))
                        c.execute("UPDATE books SET quantity=quantity+1 WHERE org_id=? AND title=?", (oid, b['book_title']))
                        conn.commit()
                        st.rerun()
        
        if not furniture.empty:
            st.subheader("🪑 Furniture")
            for _, f in furniture.iterrows():
                c1, c2 = st.columns([5,1])
                with c1:
                    st.markdown(f"🪑 **{f['student_name']}** | Chair: {f['chair_number'] or '-'} | Locker: {f['locker_number'] or '-'}")
                with c2:
                    if st.button("↩️", key=f"sf_{f['id']}"):
                        conn.cursor().execute("UPDATE furniture SET returned=1, return_date=? WHERE id=?", (str(datetime.now().date()), f['id']))
                        conn.commit()
                        st.rerun()

# ==================== BORROWED ====================
def borrowed():
    st.markdown('<h1>📋 Borrowed Books</h1>', unsafe_allow_html=True)
    conn = get_db()
    oid = st.session_state.org_id
    
    filt = st.radio("Filter", ["All","Active","Overdue"], horizontal=True)
    if filt == "Active":
        df = pd.read_sql("SELECT * FROM borrowed_books WHERE org_id=? AND returned=0", conn, params=(oid,))
    elif filt == "Overdue":
        df = pd.read_sql("SELECT * FROM borrowed_books WHERE org_id=? AND returned=0 AND return_date<?",
                        conn, params=(oid, str(datetime.now().date())))
    else:
        df = pd.read_sql("SELECT * FROM borrowed_books WHERE org_id=?", conn, params=(oid,))
    
    if not df.empty:
        st.dataframe(df[['student_name','adm_number','book_title','book_number','borrow_date','return_date','returned']],
                    use_container_width=True, hide_index=True)

# ==================== MEMBERS ====================
def members():
    st.markdown('<h1>👥 Members</h1>', unsafe_allow_html=True)
    conn = get_db()
    oid = st.session_state.org_id
    
    if st.session_state.role == 'admin':
        with st.expander("➕ Add"):
            n = st.text_input("Name")
            mid = st.text_input("ID (optional)")
            if st.button("➕ Add") and n:
                conn.cursor().execute("INSERT INTO members VALUES (?,?,?,?)", (gen_id(), oid, n, mid or f"MEM-{gen_id()[:8]}"))
                conn.commit()
                st.rerun()
    
    mems = pd.read_sql("SELECT * FROM members WHERE org_id=?", conn, params=(oid,))
    if not mems.empty:
        for _, m in mems.iterrows():
            c1, c2 = st.columns([5,1])
            c1.markdown(f"👤 **{m['name']}** ({m['member_id']})")
            if st.session_state.role == 'admin' and c2.button("🗑️", key=f"dm_{m['id']}"):
                conn.cursor().execute("DELETE FROM members WHERE id=?", (m['id'],))
                conn.commit()
                st.rerun()

# ==================== TEACHERS ====================
def teachers():
    st.markdown('<h1>👨‍🏫 Teachers</h1>', unsafe_allow_html=True)
    conn = get_db()
    oid = st.session_state.org_id
    
    if st.session_state.role == 'admin':
        with st.expander("➕ Add"):
            c1, c2, c3, c4 = st.columns(4)
            n = c1.text_input("Name")
            s = c2.text_input("Subjects")
            cl = c3.text_input("Classes")
            d = c4.text_input("Class Assigned")
            if st.button("➕ Add") and n:
                conn.cursor().execute("INSERT INTO teachers VALUES (?,?,?,?,?,?)", (gen_id(), oid, n, s, cl, d))
                conn.commit()
                st.rerun()
    
    df = pd.read_sql("SELECT * FROM teachers WHERE org_id=?", conn, params=(oid,))
    if not df.empty:
        st.dataframe(df[['name','subjects','classes','class_assigned']], use_container_width=True, hide_index=True)

# ==================== CLASS LISTS ====================
def class_lists():
    st.markdown('<h1>📋 Class Lists</h1>', unsafe_allow_html=True)
    conn = get_db()
    oid = st.session_state.org_id
    
    upload = st.file_uploader("Import Excel", type=['xlsx','xls'])
    if upload:
        df = pd.read_excel(upload)
        students = [{"name": str(r[0]), "adm": str(r[1])} for _, r in df.iterrows()]
        st.dataframe(pd.DataFrame(students))
        cn = st.text_input("Save as")
        if st.button("💾 Save") and cn:
            c = conn.cursor()
            ex = pd.read_sql("SELECT * FROM class_lists WHERE org_id=? AND class_name=?", conn, params=(oid, cn))
            if not ex.empty:
                c.execute("UPDATE class_lists SET data=? WHERE org_id=? AND class_name=?", (json.dumps(students), oid, cn))
            else:
                c.execute("INSERT INTO class_lists VALUES (?,?,?,?)", (gen_id(), oid, cn, json.dumps(students)))
            conn.commit()
            st.success("Saved!")
            st.rerun()

# ==================== QR ====================
def qr_page():
    st.markdown('<h1>📱 QR Codes</h1>', unsafe_allow_html=True)
    t, s, e = st.columns(3)
    qtype = t.selectbox("Type", ["book","chair","locker"])
    start = s.number_input("Start", 1, value=1)
    end = e.number_input("End", start, value=min(start+9, start+99))
    
    if st.button("🏷️ Generate", use_container_width=True):
        cols = st.columns(5)
        for i in range(start, end+1):
            d = f"{qtype}-{i}"
            qr = gen_qr(d)
            with cols[(i-start)%5]:
                st.markdown(f"""
                <div style="text-align:center;padding:8px;background:white;border-radius:10px;margin:4px;box-shadow:0 3px 12px rgba(0,0,0,0.2);">
                    <img src="data:image/png;base64,{qr}" width="90">
                    <p style="color:black;font-weight:700;font-size:11px;margin:4px 0;">{qtype.upper()}:{i}</p>
                </div>
                """, unsafe_allow_html=True)

# ==================== CHAT ====================
def chat():
    st.markdown('<h1>💬 Staff Chat</h1>', unsafe_allow_html=True)
    conn = get_db()
    oid = st.session_state.org_id
    cu = st.session_state.user['name']
    
    users = pd.read_sql("SELECT * FROM users WHERE org_id=? AND name!=?", conn, params=(oid, cu))
    
    c1, c2 = st.columns([1,3])
    with c1:
        st.subheader("Staff")
        for _, u in users.iterrows():
            unread = pd.read_sql("SELECT COUNT(*) as c FROM chat_messages WHERE org_id=? AND from_user=? AND to_user=? AND read=0",
                                conn, params=(oid, u['name'], cu)).iloc[0]['c']
            badge = f" 🔴{unread}" if unread else ""
            if st.button(f"👤 {u['name']}{badge}", key=f"cu_{u['id']}", use_container_width=True):
                st.session_state.chat_user = u['name']
                conn.cursor().execute("UPDATE chat_messages SET read=1 WHERE org_id=? AND from_user=? AND to_user=?",
                                     (oid, u['name'], cu))
                conn.commit()
                st.rerun()
    
    with c2:
        if st.session_state.chat_user:
            st.subheader(f"Chat with {st.session_state.chat_user}")
            msgs = pd.read_sql("""SELECT * FROM chat_messages WHERE org_id=? AND 
                ((from_user=? AND to_user=?) OR (from_user=? AND to_user=?)) ORDER BY created_at""",
                conn, params=(oid, cu, st.session_state.chat_user, st.session_state.chat_user, cu))
            
            for _, m in msgs.iterrows():
                sent = m['from_user'] == cu
                bg = "rgba(233,69,96,0.25)" if sent else "rgba(255,255,255,0.06)"
                align = "right" if sent else "left"
                st.markdown(f"""
                <div style="text-align:{align};margin:6px 0;">
                    <div style="display:inline-block;background:{bg};padding:8px 14px;border-radius:14px;
                                max-width:70%;border:1px solid rgba(255,255,255,0.08);">
                        <p style="margin:0;color:white;font-size:0.9em;">{m['message']}</p>
                        <small style="color:rgba(255,255,255,0.4);">{m['created_at'][:16]}</small>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            msg = st.text_input("Message", key="chat_msg", placeholder="Type...")
            if st.button("📤 Send") and msg:
                conn.cursor().execute("INSERT INTO chat_messages (id,org_id,from_user,to_user,message) VALUES (?,?,?,?,?)",
                                     (gen_id(), oid, cu, st.session_state.chat_user, msg))
                conn.commit()
                st.rerun()

# ==================== OVERVIEW ====================
def overview():
    st.markdown('<h1>🔍 System Overview</h1>', unsafe_allow_html=True)
    conn = get_db()
    oid = st.session_state.org_id
    
    org = pd.read_sql("SELECT * FROM organizations WHERE id=?", conn, params=(oid,)).iloc[0]
    books = pd.read_sql("SELECT * FROM books WHERE org_id=?", conn, params=(oid,))
    borrowed = pd.read_sql("SELECT * FROM borrowed_books WHERE org_id=? AND returned=0", conn, params=(oid,))
    users = pd.read_sql("SELECT * FROM users WHERE org_id=?", conn, params=(oid,))
    teachers = pd.read_sql("SELECT * FROM teachers WHERE org_id=?", conn, params=(oid,))
    members = pd.read_sql("SELECT * FROM members WHERE org_id=?", conn, params=(oid,))
    chats = pd.read_sql("SELECT * FROM chat_messages WHERE org_id=?", conn, params=(oid,))
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""
        <div style="background:rgba(255,255,255,0.05);border-radius:14px;padding:20px;border:1px solid rgba(255,255,255,0.08);">
            <h3>🏫 {org['name']}</h3>
            <p>📍 {org['address'] or 'N/A'}</p>
            <p>👤 Admin: {org['admin_name']}</p>
            <p>📧 {org['admin_email']}</p>
            <p>🔑 Code: <code style="color:#f0d060;">{org['invite_code']}</code></p>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div style="background:rgba(255,255,255,0.05);border-radius:14px;padding:20px;border:1px solid rgba(255,255,255,0.08);">
            <h3>📊 Stats</h3>
            <p>📚 Books: {books['quantity'].sum() if not books.empty else 0}</p>
            <p>📖 Active Loans: {len(borrowed)}</p>
            <p>👥 Staff: {len(users)} | Teachers: {len(teachers)} | Members: {len(members)}</p>
            <p>💬 Messages: {len(chats)}</p>
        </div>
        """, unsafe_allow_html=True)

# ==================== AUDIT ====================
def audit_page():
    st.markdown('<h1>📝 Audit Log</h1>', unsafe_allow_html=True)
    conn = get_db()
    oid = st.session_state.org_id
    df = pd.read_sql("SELECT * FROM audit_log WHERE org_id=? ORDER BY created_at DESC LIMIT 100", conn, params=(oid,))
    if not df.empty:
        st.dataframe(df[['created_at','user_name','action','details']], use_container_width=True, hide_index=True)

# ==================== REPORTS ====================
def reports():
    st.markdown('<h1>📈 Reports</h1>', unsafe_allow_html=True)
    conn = get_db()
    oid = st.session_state.org_id
    
    if st.button("📊 Generate Complete Report", use_container_width=True):
        books = pd.read_sql("SELECT * FROM books WHERE org_id=?", conn, params=(oid,))
        borrowed = pd.read_sql("SELECT * FROM borrowed_books WHERE org_id=? AND returned=0", conn, params=(oid,))
        furniture = pd.read_sql("SELECT * FROM furniture WHERE org_id=? AND returned=0", conn, params=(oid,))
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Books", books['quantity'].sum() if not books.empty else 0)
        c2.metric("Active Loans", len(borrowed))
        c3.metric("Active Furniture", len(furniture))

# ==================== WALLPAPER ====================
WALLPAPERS = [
    ("Library", "https://images.unsplash.com/photo-1521587760476-6c12a4b040da?w=600&h=400&fit=crop"),
    ("Classroom", "https://images.unsplash.com/photo-1497633762265-9d179a990aa6?w=600&h=400&fit=crop"),
    ("School", "https://images.unsplash.com/photo-1577896851231-70ef18881754?w=600&h=400&fit=crop"),
    ("Study", "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=600&h=400&fit=crop"),
    ("Books", "https://images.unsplash.com/photo-1507842217343-583bb7270b66?w=600&h=400&fit=crop"),
    ("Sunset", "https://images.unsplash.com/photo-1495616811223-4d98c6e9c869?w=600&h=400&fit=crop"),
    ("Ocean", "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=600&h=400&fit=crop"),
    ("Night", "https://images.unsplash.com/photo-1419242902214-272b3f66ee7a?w=600&h=400&fit=crop"),
]

def wallpaper_page():
    st.markdown('<h1>🖼️ Theme</h1>', unsafe_allow_html=True)
    cols = st.columns(4)
    for i, (name, url) in enumerate(WALLPAPERS):
        with cols[i%4]:
            st.image(url, caption=name, use_container_width=True)
            if st.button(f"Apply {name}", key=f"wp_{i}", use_container_width=True):
                st.session_state.wallpaper = url
                st.success(f"✅ {name} applied!")
                st.rerun()

# ==================== SETTINGS ====================
def settings():
    st.markdown('<h1>⚙️ Settings</h1>', unsafe_allow_html=True)
    conn = get_db()
    oid = st.session_state.org_id
    
    if st.session_state.role == 'admin':
        with st.expander("➕ Create Staff"):
            c1, c2, c3 = st.columns(3)
            email = c1.text_input("Email")
            name = c2.text_input("Name")
            role = c3.selectbox("Role", ["teacher","librarian","admin"])
            pw = st.text_input("Password", type="password", placeholder="Auto if empty")
            if st.button("➕ Create") and email and name:
                hp = hash_pw(pw) if pw else hash_pw(gen_id()[:8])
                sid = f"{role.upper()}-{gen_id()[:8]}"
                conn.cursor().execute("INSERT INTO users VALUES (?,?,?,?,?,?,?,?,?)",
                                     (gen_id(), oid, name, email, '', role, hp, st.session_state.invite_code, sid))
                conn.commit()
                st.success(f"✅ Created! ID: {sid}")
                st.rerun()
    
    users = pd.read_sql("SELECT * FROM users WHERE org_id=?", conn, params=(oid,))
    if not users.empty:
        for _, u in users.iterrows():
            c1, c2 = st.columns([5,1])
            c1.markdown(f"**{u['name']}** - {u['email']} | {u['role'].upper()} | ID: {u['staff_id']}")
            if st.session_state.role == 'admin' and u['role'] != 'admin' and c2.button("🗑️", key=f"ds_{u['id']}"):
                conn.cursor().execute("DELETE FROM users WHERE id=?", (u['id'],))
                conn.commit()
                st.rerun()

# ==================== MAIN ====================
def main():
    init_session()
    
    if not st.session_state.authenticated:
        auth_page()
        return
    
    inject_master_css()
    sidebar()
    
    pages = {
        "Dashboard": dashboard,
        "Book Catalog": catalog,
        "Book Issuing": book_issuing,
        "Individual Lending": lending,
        "Furniture": furniture_page,
        "Return Items": return_page,
        "Borrowed Books": borrowed,
        "Members": members,
        "Teachers": teachers,
        "Class Lists": class_lists,
        "QR Codes": qr_page,
        "Staff Chat": chat,
        "System Overview": overview,
        "Audit Log": audit_page,
        "Reports": reports,
        "Theme": wallpaper_page,
        "Settings": settings,
    }
    
    page = st.session_state.get('page', 'Dashboard')
    if page in pages:
        pages[page]()
    
    st.markdown("""
    <div style="text-align:center;padding:20px;margin-top:30px;border-top:1px solid rgba(255,255,255,0.08);">
        <p style="color:rgba(255,255,255,0.45);font-size:0.8em;">SRMS v6.0 | <span style="color:#d4af37;font-weight:600;">by WeGEM (Edwin)</span> | © 2025</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
