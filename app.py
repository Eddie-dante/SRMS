# app.py - SRMS: School Resource Management System by WeGEM (Edwin)
# A Beautiful, Radiant & Colorful School Management System
# Deploy on Streamlit Cloud: https://streamlit.io/cloud

import streamlit as st
import pandas as pd
import json
import os
import uuid
import hashlib
import random
import string
from datetime import datetime, timedelta
from io import BytesIO
import base64
from typing import Dict, List, Any, Optional
import qrcode
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
import plotly.express as px
import plotly.graph_objects as go
import sqlite3
import time

# ==================== STREAMLIT CONFIGURATION ====================
st.set_page_config(
    page_title="SRMS - School Resource Management System",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== CUSTOM CSS INJECTION ====================
def inject_custom_css():
    """Inject beautiful custom CSS with glass morphism, animations, and radiant colors"""
    st.markdown("""
    <style>
        /* ===== GLOBAL IMPORTS ===== */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
        
        /* ===== CSS VARIABLES ===== */
        :root {
            --primary: #0a0e27;
            --secondary: #1a1f4e;
            --accent: #e94560;
            --accent-hover: #c62a47;
            --gold: #d4af37;
            --gold-light: #f0d060;
            --success: #28a745;
            --warning: #ffc107;
            --danger: #dc3545;
            --info: #0f3460;
            --purple: #8b5cf6;
            --cyan: #06b6d4;
            --orange: #f97316;
            --pink: #ec4899;
            --indigo: #6366f1;
            --teal: #14b8a6;
        }
        
        /* ===== GLOBAL STYLES ===== */
        * {
            font-family: 'Inter', 'Segoe UI', system-ui, -apple-system, sans-serif !important;
        }
        
        .stApp {
            background: linear-gradient(135deg, #0a0e27 0%, #1a1f4e 25%, #0f3460 50%, #1a1f4e 75%, #0a0e27 100%) !important;
            background-size: 400% 400% !important;
            animation: gradientShift 15s ease infinite !important;
        }
        
        @keyframes gradientShift {
            0% { background-position: 0% 50%; }
            25% { background-position: 100% 0%; }
            50% { background-position: 100% 100%; }
            75% { background-position: 0% 100%; }
            100% { background-position: 0% 50%; }
        }
        
        /* ===== ANIMATED PARTICLES BACKGROUND ===== */
        .stApp::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: 
                radial-gradient(circle at 20% 30%, rgba(233, 69, 96, 0.08) 0%, transparent 50%),
                radial-gradient(circle at 80% 70%, rgba(212, 175, 55, 0.08) 0%, transparent 50%),
                radial-gradient(circle at 50% 50%, rgba(139, 92, 246, 0.05) 0%, transparent 50%),
                radial-gradient(circle at 10% 80%, rgba(6, 182, 212, 0.06) 0%, transparent 40%),
                radial-gradient(circle at 90% 20%, rgba(236, 72, 153, 0.05) 0%, transparent 40%);
            pointer-events: none;
            z-index: 0;
            animation: particleFloat 20s ease-in-out infinite;
        }
        
        @keyframes particleFloat {
            0%, 100% { transform: translate(0, 0) rotate(0deg); }
            33% { transform: translate(10px, -20px) rotate(1deg); }
            66% { transform: translate(-10px, 10px) rotate(-1deg); }
        }
        
        /* ===== MAIN CONTENT OVERLAY ===== */
        .main .block-container {
            position: relative;
            z-index: 1;
            background: rgba(255, 255, 255, 0.03) !important;
            backdrop-filter: blur(20px) !important;
            -webkit-backdrop-filter: blur(20px) !important;
            border-radius: 24px !important;
            padding: 2rem !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.05) !important;
            margin-top: 1rem !important;
            animation: containerGlow 4s ease-in-out infinite;
        }
        
        @keyframes containerGlow {
            0%, 100% { box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.05), 0 0 0 1px rgba(233, 69, 96, 0.1); }
            50% { box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.05), 0 0 30px rgba(233, 69, 96, 0.15); }
        }
        
        /* ===== HEADERS ===== */
        h1 {
            font-size: 2.5em !important;
            font-weight: 900 !important;
            background: linear-gradient(135deg, #f0d060, #d4af37, #b8941f) !important;
            -webkit-background-clip: text !important;
            -webkit-text-fill-color: transparent !important;
            background-clip: text !important;
            text-shadow: none !important;
            filter: drop-shadow(0 4px 8px rgba(212, 175, 55, 0.3)) !important;
            letter-spacing: 2px !important;
            margin-bottom: 1rem !important;
            animation: titleShine 3s ease-in-out infinite;
        }
        
        @keyframes titleShine {
            0%, 100% { filter: drop-shadow(0 4px 8px rgba(212, 175, 55, 0.3)); }
            50% { filter: drop-shadow(0 4px 16px rgba(212, 175, 55, 0.6)); }
        }
        
        h2 {
            font-size: 1.8em !important;
            font-weight: 800 !important;
            color: #ffffff !important;
            text-shadow: 0 2px 10px rgba(0, 0, 0, 0.5), 0 0 30px rgba(233, 69, 96, 0.3) !important;
            border-left: 5px solid #e94560 !important;
            padding-left: 20px !important;
            margin-bottom: 1.5rem !important;
            position: relative;
        }
        
        h2::after {
            content: '';
            position: absolute;
            left: -5px;
            bottom: -5px;
            width: 50px;
            height: 3px;
            background: linear-gradient(90deg, #e94560, transparent);
            border-radius: 3px;
        }
        
        h3 {
            font-weight: 700 !important;
            color: #ffffff !important;
            text-shadow: 0 2px 8px rgba(0, 0, 0, 0.4) !important;
        }
        
        /* ===== PARAGRAPHS & TEXT ===== */
        p, label, span, div {
            color: rgba(255, 255, 255, 0.9) !important;
        }
        
        .stMarkdown p {
            color: rgba(255, 255, 255, 0.85) !important;
            line-height: 1.6 !important;
        }
        
        /* ===== METRICS / CARDS ===== */
        .stMetric {
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.08), rgba(255, 255, 255, 0.03)) !important;
            backdrop-filter: blur(15px) !important;
            -webkit-backdrop-filter: blur(15px) !important;
            border: 1px solid rgba(255, 255, 255, 0.15) !important;
            border-radius: 16px !important;
            padding: 20px !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            position: relative;
            overflow: hidden;
        }
        
        .stMetric::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 4px;
            height: 100%;
            background: linear-gradient(180deg, #e94560, #d4af37);
            border-radius: 4px 0 0 4px;
        }
        
        .stMetric:hover {
            transform: translateY(-4px) !important;
            box-shadow: 0 12px 40px rgba(0, 0, 0, 0.3), 0 0 30px rgba(233, 69, 96, 0.1) !important;
            border-color: rgba(233, 69, 96, 0.3) !important;
        }
        
        .stMetric label {
            color: rgba(255, 255, 255, 0.7) !important;
            font-size: 0.85em !important;
            font-weight: 500 !important;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .stMetric [data-testid="stMetricValue"] {
            font-size: 2.2em !important;
            font-weight: 900 !important;
            background: linear-gradient(135deg, #ffffff, #f0d060) !important;
            -webkit-background-clip: text !important;
            -webkit-text-fill-color: transparent !important;
            background-clip: text !important;
        }
        
        /* ===== BUTTONS ===== */
        .stButton > button {
            background: linear-gradient(135deg, rgba(233, 69, 96, 0.7), rgba(197, 42, 71, 0.7)) !important;
            color: white !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            border-radius: 12px !important;
            padding: 10px 24px !important;
            font-weight: 600 !important;
            font-size: 14px !important;
            letter-spacing: 0.5px !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            position: relative;
            overflow: hidden;
            text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3) !important;
            box-shadow: 0 4px 15px rgba(233, 69, 96, 0.2) !important;
        }
        
        .stButton > button::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.15), transparent);
            transition: left 0.5s;
        }
        
        .stButton > button:hover {
            transform: translateY(-3px) !important;
            box-shadow: 0 8px 25px rgba(233, 69, 96, 0.4) !important;
            border-color: rgba(255, 255, 255, 0.4) !important;
        }
        
        .stButton > button:hover::before {
            left: 100%;
        }
        
        .stButton > button:active {
            transform: scale(0.97) !important;
        }
        
        /* ===== SECONDARY BUTTON ===== */
        .stButton > button[kind="secondary"] {
            background: linear-gradient(135deg, rgba(15, 52, 96, 0.7), rgba(26, 90, 138, 0.7)) !important;
            box-shadow: 0 4px 15px rgba(15, 52, 96, 0.3) !important;
        }
        
        .stButton > button[kind="secondary"]:hover {
            box-shadow: 0 8px 25px rgba(15, 52, 96, 0.5) !important;
        }
        
        /* ===== GOLD BUTTON ===== */
        .stButton > button[kind="primary"] {
            background: linear-gradient(135deg, rgba(212, 175, 55, 0.8), rgba(184, 148, 31, 0.8)) !important;
            color: #0a0e27 !important;
            font-weight: 700 !important;
            box-shadow: 0 4px 20px rgba(212, 175, 55, 0.3) !important;
        }
        
        .stButton > button[kind="primary"]:hover {
            box-shadow: 0 8px 30px rgba(212, 175, 55, 0.5) !important;
        }
        
        /* ===== INPUTS ===== */
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea {
            background: rgba(255, 255, 255, 0.06) !important;
            color: white !important;
            border: 2px solid rgba(255, 255, 255, 0.15) !important;
            border-radius: 12px !important;
            padding: 14px 18px !important;
            font-size: 15px !important;
            transition: all 0.3s ease !important;
        }
        
        .stTextInput > div > div > input:focus,
        .stTextArea > div > div > textarea:focus {
            border-color: #e94560 !important;
            box-shadow: 0 0 0 4px rgba(233, 69, 96, 0.15), 0 0 20px rgba(233, 69, 96, 0.1) !important;
            background: rgba(255, 255, 255, 0.1) !important;
        }
        
        .stTextInput > div > div > input::placeholder,
        .stTextArea > div > div > textarea::placeholder {
            color: rgba(255, 255, 255, 0.4) !important;
        }
        
        /* ===== SELECT BOX ===== */
        .stSelectbox > div > div {
            background: rgba(255, 255, 255, 0.06) !important;
            border: 2px solid rgba(255, 255, 255, 0.15) !important;
            border-radius: 12px !important;
        }
        
        .stSelectbox > div > div > div {
            color: white !important;
        }
        
        /* ===== DATE INPUT ===== */
        .stDateInput > div > div > input {
            background: rgba(255, 255, 255, 0.06) !important;
            color: white !important;
            border: 2px solid rgba(255, 255, 255, 0.15) !important;
            border-radius: 12px !important;
        }
        
        /* ===== DATAFRAME / TABLES ===== */
        .stDataFrame {
            background: rgba(255, 255, 255, 0.04) !important;
            border-radius: 16px !important;
            overflow: hidden !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
        }
        
        .stDataFrame th {
            background: linear-gradient(135deg, rgba(10, 14, 39, 0.9), rgba(15, 52, 96, 0.9)) !important;
            color: #f0d060 !important;
            font-weight: 700 !important;
            padding: 15px !important;
            font-size: 13px !important;
            text-transform: uppercase;
            letter-spacing: 1px;
            border-bottom: 2px solid rgba(233, 69, 96, 0.3) !important;
        }
        
        .stDataFrame td {
            color: rgba(255, 255, 255, 0.9) !important;
            padding: 12px 15px !important;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05) !important;
        }
        
        .stDataFrame tr:hover td {
            background: rgba(233, 69, 96, 0.08) !important;
        }
        
        /* ===== EXPANDERS ===== */
        .streamlit-expanderHeader {
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.06), rgba(255, 255, 255, 0.02)) !important;
            color: white !important;
            border-radius: 16px !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            font-weight: 600 !important;
            padding: 15px 20px !important;
            transition: all 0.3s ease !important;
        }
        
        .streamlit-expanderHeader:hover {
            background: rgba(233, 69, 96, 0.1) !important;
            border-color: rgba(233, 69, 96, 0.3) !important;
        }
        
        /* ===== TABS ===== */
        .stTabs [data-baseweb="tab-list"] {
            background: rgba(255, 255, 255, 0.04) !important;
            border-radius: 16px !important;
            padding: 5px !important;
            gap: 5px !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
        }
        
        .stTabs [data-baseweb="tab"] {
            color: rgba(255, 255, 255, 0.7) !important;
            border-radius: 12px !important;
            padding: 12px 24px !important;
            font-weight: 500 !important;
            transition: all 0.3s ease !important;
        }
        
        .stTabs [data-baseweb="tab"]:hover {
            background: rgba(233, 69, 96, 0.15) !important;
            color: white !important;
        }
        
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, rgba(233, 69, 96, 0.6), rgba(197, 42, 71, 0.6)) !important;
            color: white !important;
            font-weight: 600 !important;
            box-shadow: 0 4px 15px rgba(233, 69, 96, 0.3) !important;
        }
        
        /* ===== RADIO BUTTONS ===== */
        .stRadio > div {
            background: rgba(255, 255, 255, 0.04) !important;
            border-radius: 12px !important;
            padding: 5px !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
        }
        
        .stRadio [data-baseweb="radio"] {
            color: white !important;
        }
        
        /* ===== SIDEBAR ===== */
        .stSidebar {
            background: linear-gradient(180deg, rgba(10, 14, 39, 0.95), rgba(15, 52, 96, 0.95)) !important;
            backdrop-filter: blur(20px) !important;
            -webkit-backdrop-filter: blur(20px) !important;
            border-right: 1px solid rgba(255, 255, 255, 0.1) !important;
            box-shadow: 4px 0 30px rgba(0, 0, 0, 0.3) !important;
        }
        
        .stSidebar * {
            color: white !important;
        }
        
        .stSidebar button {
            background: rgba(255, 255, 255, 0.05) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 12px !important;
            transition: all 0.3s ease !important;
            margin: 3px 0 !important;
        }
        
        .stSidebar button:hover {
            background: rgba(233, 69, 96, 0.2) !important;
            border-color: rgba(233, 69, 96, 0.4) !important;
            transform: translateX(3px) !important;
        }
        
        /* ===== ALERTS / MESSAGES ===== */
        .stAlert {
            border-radius: 12px !important;
            border: 1px solid !important;
            backdrop-filter: blur(10px) !important;
        }
        
        .stSuccess {
            background: rgba(40, 167, 69, 0.15) !important;
            border-color: rgba(40, 167, 69, 0.3) !important;
            color: #4ade80 !important;
        }
        
        .stError {
            background: rgba(220, 53, 69, 0.15) !important;
            border-color: rgba(220, 53, 69, 0.3) !important;
            color: #f87171 !important;
        }
        
        .stWarning {
            background: rgba(255, 193, 7, 0.15) !important;
            border-color: rgba(255, 193, 7, 0.3) !important;
            color: #fbbf24 !important;
        }
        
        .stInfo {
            background: rgba(23, 162, 184, 0.15) !important;
            border-color: rgba(23, 162, 184, 0.3) !important;
            color: #22d3ee !important;
        }
        
        /* ===== FORM STYLING ===== */
        .stForm {
            background: rgba(255, 255, 255, 0.03) !important;
            border-radius: 16px !important;
            padding: 25px !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
        }
        
        /* ===== PROGRESS BAR ===== */
        .stProgress > div > div > div > div {
            background: linear-gradient(90deg, #e94560, #d4af37, #8b5cf6) !important;
            border-radius: 10px !important;
        }
        
        /* ===== CHAT STYLING ===== */
        .chat-container {
            background: rgba(0, 0, 0, 0.2) !important;
            border-radius: 16px !important;
            padding: 20px !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
        }
        
        /* ===== CREDIT TEXT ===== */
        .credit-text {
            background: linear-gradient(135deg, #d4af37, #f0d060) !important;
            -webkit-background-clip: text !important;
            -webkit-text-fill-color: transparent !important;
            background-clip: text !important;
            font-weight: 700 !important;
            text-align: center;
        }
        
        /* ===== LOGO TEXT ===== */
        .logo-text {
            font-size: 3.5em !important;
            font-weight: 900 !important;
            background: linear-gradient(180deg, #f0d060 0%, #d4af37 50%, #b8941f 100%) !important;
            -webkit-background-clip: text !important;
            -webkit-text-fill-color: transparent !important;
            background-clip: text !important;
            text-align: center;
            letter-spacing: 8px;
            filter: drop-shadow(0 4px 15px rgba(212, 175, 55, 0.4));
            animation: logoGlow 3s ease-in-out infinite;
        }
        
        @keyframes logoGlow {
            0%, 100% { filter: drop-shadow(0 4px 15px rgba(212, 175, 55, 0.4)); }
            50% { filter: drop-shadow(0 4px 30px rgba(212, 175, 55, 0.8)); }
        }
        
        /* ===== BADGE ===== */
        .badge {
            display: inline-block;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .badge-admin {
            background: linear-gradient(135deg, #e94560, #ff6b8a);
            color: white;
        }
        
        .badge-teacher {
            background: linear-gradient(135deg, #0f3460, #1a5a8a);
            color: white;
        }
        
        .badge-librarian {
            background: linear-gradient(135deg, #28a745, #20c997);
            color: white;
        }
        
        /* ===== DIVIDER ===== */
        hr {
            border: none;
            height: 1px;
            background: linear-gradient(90deg, transparent, rgba(233, 69, 96, 0.4), rgba(212, 175, 55, 0.4), transparent);
            margin: 20px 0;
        }
        
        /* ===== SCROLLBAR ===== */
        ::-webkit-scrollbar {
            width: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 10px;
        }
        
        ::-webkit-scrollbar-thumb {
            background: linear-gradient(180deg, #e94560, #d4af37);
            border-radius: 10px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: linear-gradient(180deg, #ff6b8a, #f0d060);
        }
        
        /* ===== RESPONSIVE ===== */
        @media (max-width: 768px) {
            .logo-text { font-size: 2em !important; }
            h1 { font-size: 1.8em !important; }
            .stMetric [data-testid="stMetricValue"] { font-size: 1.5em !important; }
        }
    </style>
    """, unsafe_allow_html=True)

# ==================== DATABASE SETUP ====================
@st.cache_resource
def init_db():
    """Initialize SQLite database"""
    conn = sqlite3.connect('srms.db', check_same_thread=False)
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY, org_id TEXT, name TEXT, email TEXT, phone TEXT,
        role TEXT, password TEXT, invite_code TEXT, staff_id TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS organizations (
        id TEXT PRIMARY KEY, name TEXT, invite_code TEXT UNIQUE,
        admin_name TEXT, admin_email TEXT, admin_phone TEXT, address TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS books (
        id TEXT PRIMARY KEY, org_id TEXT, title TEXT, type TEXT, quantity INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS members (
        id TEXT PRIMARY KEY, org_id TEXT, name TEXT, member_id TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS teachers (
        id TEXT PRIMARY KEY, org_id TEXT, name TEXT, subjects TEXT,
        classes TEXT, class_assigned TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS borrowed_books (
        id TEXT PRIMARY KEY, org_id TEXT, student_name TEXT, adm_number TEXT,
        form TEXT, stream TEXT, book_title TEXT, book_number TEXT,
        borrow_date TEXT, return_date TEXT, actual_return_date TEXT,
        returned INTEGER DEFAULT 0, lending_type TEXT DEFAULT 'individual',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS furniture (
        id TEXT PRIMARY KEY, org_id TEXT, student_name TEXT, adm_number TEXT,
        chair_number TEXT, locker_number TEXT, allocation_date TEXT,
        return_date TEXT, returned INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS class_lists (
        id TEXT PRIMARY KEY, org_id TEXT, class_name TEXT, data TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS audit_log (
        id TEXT PRIMARY KEY, org_id TEXT, user_name TEXT, action TEXT, details TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS chat_messages (
        id TEXT PRIMARY KEY, org_id TEXT, from_user TEXT, to_user TEXT,
        message TEXT, read INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    conn.commit()
    return conn

# ==================== HELPER FUNCTIONS ====================
def generate_id():
    return str(uuid.uuid4())

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def generate_invite_code() -> str:
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

def add_audit_log(org_id: str, action: str, details: str):
    conn = init_db()
    c = conn.cursor()
    user_name = st.session_state.user.get('name', 'System') if st.session_state.user else 'System'
    c.execute('INSERT INTO audit_log (id, org_id, user_name, action, details) VALUES (?,?,?,?,?)',
              (generate_id(), org_id, user_name, action, details))
    conn.commit()

def generate_qr_code(data: str) -> str:
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

# ==================== WALLPAPER GALLERY ====================
WALLPAPERS = [
    {"name": "Library", "url": "https://images.unsplash.com/photo-1521587760476-6c12a4b040da?w=1200&h=800&fit=crop"},
    {"name": "Classroom", "url": "https://images.unsplash.com/photo-1497633762265-9d179a990aa6?w=1200&h=800&fit=crop"},
    {"name": "School Hall", "url": "https://images.unsplash.com/photo-1577896851231-70ef18881754?w=1200&h=800&fit=crop"},
    {"name": "Study Desk", "url": "https://images.unsplash.com/photo-1503676260728-1c00da094a0b?w=1200&h=800&fit=crop"},
    {"name": "Education", "url": "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=1200&h=800&fit=crop"},
    {"name": "Bookshelf", "url": "https://images.unsplash.com/photo-1507842217343-583bb7270b66?w=1200&h=800&fit=crop"},
    {"name": "Mountain", "url": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1200&h=800&fit=crop"},
    {"name": "Ocean", "url": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=1200&h=800&fit=crop"},
    {"name": "Night Sky", "url": "https://images.unsplash.com/photo-1419242902214-272b3f66ee7a?w=1200&h=800&fit=crop"},
    {"name": "Sunset", "url": "https://images.unsplash.com/photo-1495616811223-4d98c6e9c869?w=1200&h=800&fit=crop"},
    {"name": "Forest", "url": "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=1200&h=800&fit=crop"},
    {"name": "Abstract", "url": "https://images.unsplash.com/photo-1550859492-d5da9d8e45f3?w=1200&h=800&fit=crop"},
]

# ==================== SESSION STATE ====================
def init_session_state():
    defaults = {
        'user': None, 'org_id': None, 'org_name': None, 'role': None,
        'invite_code': None, 'authenticated': False, 'page': '📊 Dashboard',
        'wallpaper': None, 'chat_active_user': None, 'editing_member': None,
        'loaded_class': None, 'loaded_book': None, 'furniture_class': None,
        'imported_students': None
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

# ==================== AUTHENTICATION PAGE ====================
def auth_page():
    """Beautiful authentication page"""
    inject_custom_css()
    
    # Centered layout
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<br><br>', unsafe_allow_html=True)
        st.markdown('<div class="logo-text">SRMS</div>', unsafe_allow_html=True)
        st.markdown('<p style="text-align:center;color:rgba(255,255,255,0.8);font-size:1.3em;font-weight:300;letter-spacing:2px;">School Resource Management System</p>', unsafe_allow_html=True)
        st.markdown('<p class="credit-text" style="font-size:1.1em;">by <strong style="color:#f0d060;">WeGEM</strong> (Edwin)</p>', unsafe_allow_html=True)
        
        st.markdown('<hr>', unsafe_allow_html=True)
        
        tab1, tab2, tab3 = st.tabs(["🔑 **Login**", "📝 **Sign Up**", "🏫 **Create School**"])
        
        with tab1:
            with st.form("login_form"):
                st.markdown('<p style="color:rgba(255,255,255,0.6);font-size:0.9em;">Welcome back! Please login to continue.</p>', unsafe_allow_html=True)
                name = st.text_input("👤 Full Name", placeholder="Enter your registered name")
                school = st.text_input("🏢 School Name", placeholder="Enter your school name")
                code = st.text_input("🔑 Invite Code", placeholder="Enter the invite code")
                password = st.text_input("🔒 Password", type="password", placeholder="Enter your password")
                
                col_a, col_b = st.columns([2, 1])
                with col_a:
                    submitted = st.form_submit_button("🔑 Login to Dashboard", use_container_width=True)
                
                if submitted:
                    if not all([name, school, code, password]):
                        st.error("⚠️ Please fill all fields")
                    else:
                        conn = init_db()
                        c = conn.cursor()
                        c.execute("SELECT * FROM organizations WHERE name = ?", (school,))
                        org = c.fetchone()
                        if not org:
                            st.error("❌ School not found. Please check the school name.")
                        else:
                            org_id, org_name, invite = org[0], org[1], org[2]
                            if code.upper() != invite:
                                st.error("❌ Invalid invite code.")
                            else:
                                hashed_pw = hash_password(password)
                                c.execute("SELECT * FROM users WHERE org_id = ? AND name = ? AND password = ?", 
                                         (org_id, name, hashed_pw))
                                user = c.fetchone()
                                if not user:
                                    st.error("❌ Invalid credentials. Check your name and password.")
                                else:
                                    st.session_state.user = {
                                        'id': user[0], 'name': user[2], 'email': user[3],
                                        'role': user[5], 'staff_id': user[7]
                                    }
                                    st.session_state.org_id = org_id
                                    st.session_state.org_name = org_name
                                    st.session_state.role = user[5]
                                    st.session_state.invite_code = invite
                                    st.session_state.authenticated = True
                                    add_audit_log(org_id, 'Login', f"{name} logged in successfully")
                                    st.rerun()
        
        with tab2:
            with st.form("signup_form"):
                st.markdown('<p style="color:rgba(255,255,255,0.6);font-size:0.9em;">Join your school\'s management system.</p>', unsafe_allow_html=True)
                name = st.text_input("👤 Full Name", key="signup_name", placeholder="Your full name")
                email = st.text_input("📧 Email Address", key="signup_email", placeholder="your@email.com")
                phone = st.text_input("📞 Phone Number", key="signup_phone", placeholder="+1234567890")
                school = st.text_input("🏢 School Name", key="signup_school", placeholder="Your school name")
                code = st.text_input("🔑 Invite Code", key="signup_code", placeholder="From your admin")
                staff_id = st.text_input("🪪 Staff ID (Optional)", key="signup_staff_id", placeholder="Employee ID")
                password = st.text_input("🔒 Create Password", type="password", key="signup_password", placeholder="Min 6 characters")
                
                submitted = st.form_submit_button("📝 Create Account", use_container_width=True)
                
                if submitted:
                    if not all([name, email, school, code, password]):
                        st.error("⚠️ Please fill all required fields")
                    elif len(password) < 6:
                        st.error("⚠️ Password must be at least 6 characters")
                    else:
                        conn = init_db()
                        c = conn.cursor()
                        c.execute("SELECT * FROM organizations WHERE name = ?", (school,))
                        org = c.fetchone()
                        if not org:
                            st.error("❌ School not found.")
                        elif code.upper() != org[2]:
                            st.error("❌ Invalid invite code.")
                        else:
                            org_id = org[0]
                            c.execute("SELECT * FROM users WHERE org_id = ? AND email = ?", (org_id, email))
                            if c.fetchone():
                                st.error("⚠️ Email already registered.")
                            else:
                                uid = generate_id()
                                hashed_pw = hash_password(password)
                                sid = staff_id or f"STF-{uid[:8].upper()}"
                                c.execute("INSERT INTO users (id, org_id, name, email, phone, role, password, invite_code, staff_id) VALUES (?,?,?,?,?,?,?,?,?)",
                                         (uid, org_id, name, email, phone, 'teacher', hashed_pw, code.upper(), sid))
                                conn.commit()
                                add_audit_log(org_id, 'Signup', f"{name} created account as teacher")
                                st.success(f"✅ Account created! Your Staff ID: **{sid}**")
                                st.info("🔑 Please go to the Login tab to sign in.")
        
        with tab3:
            with st.form("create_school_form"):
                st.markdown('<p style="color:rgba(255,255,255,0.6);font-size:0.9em;">Set up a new school management system.</p>', unsafe_allow_html=True)
                school_name = st.text_input("🏢 School Name", key="create_school", placeholder="e.g., Sunshine High School")
                address = st.text_input("📍 School Address", key="create_address", placeholder="School location")
                admin_name = st.text_input("👤 Admin Full Name", key="create_admin", placeholder="Administrator name")
                admin_email = st.text_input("📧 Admin Email", key="create_email", placeholder="admin@school.com")
                admin_phone = st.text_input("📞 Admin Phone", key="create_phone", placeholder="+1234567890")
                password = st.text_input("🔒 Password", type="password", key="create_password", placeholder="Min 8 characters")
                password_confirm = st.text_input("🔒 Confirm Password", type="password", key="create_password_confirm", placeholder="Re-enter password")
                
                submitted = st.form_submit_button("🚀 Create School & Launch", use_container_width=True)
                
                if submitted:
                    if not all([school_name, admin_name, admin_email, password]):
                        st.error("⚠️ Please fill all required fields")
                    elif password != password_confirm:
                        st.error("⚠️ Passwords don't match")
                    elif len(password) < 8:
                        st.error("⚠️ Password must be at least 8 characters")
                    else:
                        conn = init_db()
                        c = conn.cursor()
                        invite = generate_invite_code()
                        org_id = generate_id()
                        uid = generate_id()
                        hashed_pw = hash_password(password)
                        
                        c.execute("INSERT INTO organizations (id, name, invite_code, admin_name, admin_email, admin_phone, address) VALUES (?,?,?,?,?,?,?)",
                                 (org_id, school_name, invite, admin_name, admin_email, admin_phone, address))
                        c.execute("INSERT INTO users (id, org_id, name, email, phone, role, password, invite_code, staff_id) VALUES (?,?,?,?,?,?,?,?,?)",
                                 (uid, org_id, admin_name, admin_email, admin_phone, 'admin', hashed_pw, invite, 'ADMIN-001'))
                        conn.commit()
                        
                        st.success(f"🎉 School created successfully!")
                        st.markdown(f"""
                        <div style="background: linear-gradient(135deg, rgba(212,175,55,0.2), rgba(233,69,96,0.2)); border: 2px solid rgba(212,175,55,0.4); border-radius: 16px; padding: 25px; text-align: center; margin: 15px 0;">
                            <p style="color: rgba(255,255,255,0.7); font-size: 0.9em; margin: 0;">🏫 Your School Invite Code</p>
                            <p style="font-size: 2.5em; font-weight: 900; letter-spacing: 8px; color: #f0d060; font-family: monospace; margin: 10px 0;">{invite}</p>
                            <p style="color: rgba(255,255,255,0.6); font-size: 0.85em;">Share this code with your staff to join the system.</p>
                        </div>
                        """, unsafe_allow_html=True)
                        st.info("🔑 Please go to the **Login** tab to access your dashboard.")

# ==================== SIDEBAR ====================
def render_sidebar():
    """Beautiful sidebar navigation"""
    with st.sidebar:
        st.markdown('<br>', unsafe_allow_html=True)
        st.markdown(f'''
        <div style="text-align:center;">
            <div style="width:60px;height:60px;background:linear-gradient(135deg,#d4af37,#f0d060,#d4af37);border-radius:15px;display:inline-flex;align-items:center;justify-content:center;font-size:22px;font-weight:900;color:#0a0e27;margin-bottom:10px;box-shadow:0 8px 30px rgba(212,175,55,0.3);">SRMS</div>
            <p style="color:white;font-weight:700;font-size:1.1em;margin:0;">{st.session_state.org_name}</p>
            <p style="color:rgba(255,255,255,0.6);font-size:0.8em;margin:5px 0;">👤 {st.session_state.user["name"]}</p>
            <span class="badge badge-{st.session_state.role}">{st.session_state.role.upper()}</span>
        </div>
        ''', unsafe_allow_html=True)
        
        st.markdown('<hr>', unsafe_allow_html=True)
        
        # Navigation menu
        menu_items = [
            ("📊", "Dashboard", "dashboard_page"),
            ("📚", "Book Catalog", "catalog_page"),
            ("📖", "Book Issuing (Class)", "book_issuing_page"),
            ("👤", "Individual Lending", "lending_page"),
            ("🪑", "Furniture Allocation", "furniture_page"),
            ("↩️", "Return Items", "return_page"),
            ("📋", "Borrowed Books", "borrowed_page"),
            ("👥", "Members", "members_page"),
            ("👨‍🏫", "Teachers", "teachers_page"),
            ("📋", "Class Lists", "class_page"),
            ("📱", "QR Codes", "qr_page"),
            ("💬", "Staff Chat", "chat_page"),
            ("🔍", "System Overview", "overview_page"),
            ("📝", "Audit Log", "audit_page"),
            ("📈", "Reports", "reports_page"),
            ("🖼️", "Theme & Wallpaper", "wallpaper_page"),
            ("⚙️", "Settings", "settings_page"),
        ]
        
        for icon, label, page_key in menu_items:
            if st.sidebar.button(f"{icon}  {label}", key=f"nav_{page_key}", use_container_width=True):
                st.session_state.page = f"{icon} {label}"
                st.rerun()
        
        st.sidebar.markdown('<hr>', unsafe_allow_html=True)
        
        if st.sidebar.button("🚪 Logout", use_container_width=True, type="primary"):
            add_audit_log(st.session_state.org_id, 'Logout', st.session_state.user['name'])
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
        
        st.sidebar.markdown('<p class="credit-text" style="font-size:0.8em;text-align:center;">by <strong>WeGEM</strong> (Edwin)</p>', unsafe_allow_html=True)

# ==================== DASHBOARD ====================
def dashboard_page():
    st.markdown('<h1>📊 Dashboard Overview</h1>', unsafe_allow_html=True)
    
    org_id = st.session_state.org_id
    conn = init_db()
    
    # Get statistics
    books_df = pd.read_sql("SELECT * FROM books WHERE org_id = ?", conn, params=(org_id,))
    borrowed_df = pd.read_sql("SELECT * FROM borrowed_books WHERE org_id = ? AND returned = 0", conn, params=(org_id,))
    members_df = pd.read_sql("SELECT * FROM members WHERE org_id = ?", conn, params=(org_id,))
    teachers_df = pd.read_sql("SELECT * FROM teachers WHERE org_id = ?", conn, params=(org_id,))
    furniture_df = pd.read_sql("SELECT * FROM furniture WHERE org_id = ? AND returned = 0", conn, params=(org_id,))
    
    total_books = books_df['quantity'].sum() if not books_df.empty else 0
    books_borrowed = len(borrowed_df)
    
    overdue_count = 0
    if not borrowed_df.empty:
        today = datetime.now().date()
        for _, row in borrowed_df.iterrows():
            try:
                if datetime.strptime(row['return_date'], '%Y-%m-%d').date() < today:
                    overdue_count += 1
            except:
                pass
    
    # Stats cards
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📚 Total Books", total_books, delta=None)
        st.metric("👥 Members", len(members_df), delta=None)
    with col2:
        st.metric("📖 Books Borrowed", books_borrowed, delta=f"-{books_borrowed}" if books_borrowed > 0 else None)
        st.metric("👨‍🏫 Teachers", len(teachers_df), delta=None)
    with col3:
        st.metric("📗 Available Books", total_books - books_borrowed, delta=None)
        st.metric("🪑 Active Furniture", len(furniture_df), delta=None)
    with col4:
        st.metric("🔴 Overdue Items", overdue_count, delta=f"⚠️ {overdue_count}" if overdue_count > 0 else "✅ 0")
        st.metric("✅ Active Loans", books_borrowed, delta=None)
    
    # Invite Code Banner
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, rgba(255,255,255,0.08), rgba(255,255,255,0.03)); 
                border: 2px dashed rgba(233,69,96,0.4); 
                border-radius: 16px; 
                padding: 25px; 
                text-align: center; 
                margin: 25px 0;
                backdrop-filter: blur(10px);">
        <p style="color: rgba(255,255,255,0.6); font-size: 0.9em; margin: 0;">🏫 School Invite Code - Share with Staff</p>
        <p style="font-size: 2.8em; font-weight: 900; letter-spacing: 8px; color: #f0d060; font-family: 'Courier New', monospace; margin: 10px 0; text-shadow: 0 0 30px rgba(212,175,55,0.4);">{st.session_state.invite_code}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Recent Activity
    st.markdown('<h2>📝 Recent Activity</h2>', unsafe_allow_html=True)
    logs = pd.read_sql("SELECT * FROM audit_log WHERE org_id = ? ORDER BY created_at DESC LIMIT 8", conn, params=(org_id,))
    if not logs.empty:
        for _, log in logs.iterrows():
            icon = "🔑" if "login" in log['action'].lower() else "📖" if "book" in log['action'].lower() else "🪑" if "furniture" in log['action'].lower() else "👤" if "member" in log['action'].lower() or "teacher" in log['action'].lower() else "📝"
            st.markdown(f"""
            <div style="background: rgba(255,255,255,0.04); border-radius: 10px; padding: 12px 15px; margin: 5px 0; border-left: 3px solid rgba(233,69,96,0.5);">
                <small style="color: rgba(255,255,255,0.5);">{log['created_at'][:19]}</small>
                <span style="margin: 0 10px;">{icon}</span>
                <strong style="color: #f0d060;">{log['user_name']}</strong>
                <span style="color: rgba(255,255,255,0.8);"> - {log['action']}: {log['details']}</span>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No recent activity yet. Start using the system!")
    
    conn.close()

# ==================== BOOK CATALOG ====================
def catalog_page():
    st.markdown('<h1>📚 Book Catalog</h1>', unsafe_allow_html=True)
    
    org_id = st.session_state.org_id
    conn = init_db()
    
    with st.expander("➕ Add / Update Book", expanded=False):
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            title = st.text_input("📖 Book Title", placeholder="Enter book title")
        with col2:
            book_type = st.selectbox("📂 Type", ["Textbook", "Novel", "Reference", "Magazine", "Other"])
        with col3:
            quantity = st.number_input("🔢 Quantity", min_value=1, value=1)
        
        if st.button("📖 Add / Update Book", use_container_width=True, type="primary"):
            if title:
                c = conn.cursor()
                existing = pd.read_sql("SELECT * FROM books WHERE org_id = ? AND title = ?", conn, params=(org_id, title))
                if not existing.empty:
                    new_qty = existing.iloc[0]['quantity'] + quantity
                    c.execute("UPDATE books SET quantity = ?, type = ? WHERE org_id = ? AND title = ?",
                             (new_qty, book_type, org_id, title))
                    conn.commit()
                    add_audit_log(org_id, 'Book Updated', f"'{title}' - added {quantity} copies (Total: {new_qty})")
                    st.success(f"✅ Updated '{title}'! Total: {new_qty}")
                else:
                    c.execute("INSERT INTO books (id, org_id, title, type, quantity) VALUES (?,?,?,?,?)",
                             (generate_id(), org_id, title, book_type, quantity))
                    conn.commit()
                    add_audit_log(org_id, 'Book Added', f"'{title}' ({book_type}) x{quantity}")
                    st.success(f"✅ Added '{title}'!")
                st.rerun()
    
    st.markdown('<h2>📋 Current Catalog</h2>', unsafe_allow_html=True)
    books = pd.read_sql("SELECT * FROM books WHERE org_id = ? ORDER BY title", conn, params=(org_id,))
    
    if not books.empty:
        for _, book in books.iterrows():
            qty = book['quantity']
            if qty == 0:
                badge = '<span style="background:rgba(220,53,69,0.3);color:#f87171;padding:4px 10px;border-radius:20px;font-size:11px;">🔴 Out of Stock</span>'
            elif qty < 5:
                badge = '<span style="background:rgba(255,193,7,0.3);color:#fbbf24;padding:4px 10px;border-radius:20px;font-size:11px;">🟡 Low Stock</span>'
            else:
                badge = '<span style="background:rgba(40,167,69,0.3);color:#4ade80;padding:4px 10px;border-radius:20px;font-size:11px;">🟢 In Stock</span>'
            
            col1, col2 = st.columns([5, 1])
            with col1:
                st.markdown(f"""
                <div style="background:rgba(255,255,255,0.04);border-radius:12px;padding:15px;margin:5px 0;border:1px solid rgba(255,255,255,0.08);">
                    <strong style="font-size:1.1em;">📖 {book['title']}</strong>
                    <span style="margin-left:10px;color:rgba(255,255,255,0.5);">| {book['type']} | Qty: <strong>{qty}</strong></span>
                    {badge}
                </div>
                """, unsafe_allow_html=True)
            with col2:
                if st.button("🗑️ Delete", key=f"del_book_{book['id']}"):
                    c = conn.cursor()
                    c.execute("DELETE FROM books WHERE id = ?", (book['id'],))
                    conn.commit()
                    add_audit_log(org_id, 'Book Deleted', f"'{book['title']}'")
                    st.rerun()
    else:
        st.info("📭 No books in catalog. Add some books to get started!")
    
    conn.close()

# ==================== BOOK ISSUING (CLASS) ====================
def book_issuing_page():
    st.markdown('<h1>📖 Bulk Book Issuing to Class</h1>', unsafe_allow_html=True)
    
    org_id = st.session_state.org_id
    conn = init_db()
    
    col1, col2 = st.columns(2)
    with col1:
        books = pd.read_sql("SELECT * FROM books WHERE org_id = ? AND quantity > 0", conn, params=(org_id,))
        book_options = ["-- Select Book --"] + books['title'].tolist() if not books.empty else ["-- Select Book --"]
        selected_book = st.selectbox("📚 Select Book", book_options)
    
    with col2:
        classes = pd.read_sql("SELECT * FROM class_lists WHERE org_id = ?", conn, params=(org_id,))
        class_options = ["-- Select Class --"] + classes['class_name'].tolist() if not classes.empty else ["-- Select Class --"]
        selected_class = st.selectbox("📋 Select Class", class_options)
    
    col3, col4 = st.columns(2)
    with col3:
        borrow_date = st.date_input("📅 Issue Date", datetime.now())
    with col4:
        return_date = st.date_input("📅 Return Date", datetime.now() + timedelta(days=14))
    
    if st.button("📋 Load Class", use_container_width=True, type="secondary"):
        if selected_class != "-- Select Class --" and selected_book != "-- Select Book --":
            st.session_state.loaded_class = selected_class
            st.session_state.loaded_book = selected_book
            st.rerun()
    
    if st.session_state.loaded_class and st.session_state.loaded_book:
        class_data = pd.read_sql("SELECT * FROM class_lists WHERE org_id = ? AND class_name = ?",
                                 conn, params=(org_id, st.session_state.loaded_class))
        if not class_data.empty:
            students = json.loads(class_data.iloc[0]['data'])
            st.markdown(f'<h2>Assign "{st.session_state.loaded_book}" to {st.session_state.loaded_class}</h2>', unsafe_allow_html=True)
            
            df_data = []
            for student in students:
                existing = pd.read_sql(
                    "SELECT * FROM borrowed_books WHERE org_id = ? AND adm_number = ? AND book_title = ? AND returned = 0",
                    conn, params=(org_id, student['adm'], st.session_state.loaded_book))
                is_assigned = not existing.empty
                df_data.append({
                    "Assign": not is_assigned,
                    "Student": student['name'],
                    "ADM": student['adm'],
                    "Book Number": existing.iloc[0]['book_number'] if is_assigned else "",
                    "Status": "✅ Issued" if is_assigned else "⏳ Pending"
                })
            
            df = pd.DataFrame(df_data)
            
            filter_tab = st.radio("🔍 Filter", ["📋 All", "⏳ Pending", "✅ Issued"], horizontal=True)
            if filter_tab == "⏳ Pending":
                df = df[df['Status'] == "⏳ Pending"]
            elif filter_tab == "✅ Issued":
                df = df[df['Status'] == "✅ Issued"]
            
            edited_df = st.data_editor(df, hide_index=True, use_container_width=True,
                disabled=["Student", "ADM", "Status"])
            
            if st.button("✅ Issue Books", type="primary", use_container_width=True):
                to_assign = edited_df[edited_df['Assign'] == True]
                if to_assign.empty:
                    st.error("⚠️ No students selected")
                else:
                    book = books[books['title'] == st.session_state.loaded_book].iloc[0]
                    if len(to_assign) > book['quantity']:
                        st.error(f"⚠️ Only {book['quantity']} books available!")
                    else:
                        c = conn.cursor()
                        for _, row in to_assign.iterrows():
                            if row['Book Number']:
                                c.execute("""INSERT INTO borrowed_books 
                                    (id, org_id, student_name, adm_number, book_title, book_number, borrow_date, return_date, lending_type)
                                    VALUES (?,?,?,?,?,?,?,?,?)""",
                                    (generate_id(), org_id, row['Student'], row['ADM'], st.session_state.loaded_book,
                                     row['Book Number'], str(borrow_date), str(return_date), 'class'))
                                c.execute("UPDATE books SET quantity = quantity - 1 WHERE org_id = ? AND title = ?",
                                         (org_id, st.session_state.loaded_book))
                        conn.commit()
                        add_audit_log(org_id, 'Books Issued', f"Issued {len(to_assign)} copies to {st.session_state.loaded_class}")
                        st.success(f"✅ Successfully issued {len(to_assign)} books!")
                        st.session_state.loaded_class = None
                        st.session_state.loaded_book = None
                        st.rerun()
    
    conn.close()

# ==================== INDIVIDUAL LENDING ====================
def lending_page():
    st.markdown('<h1>👤 Individual Book Lending</h1>', unsafe_allow_html=True)
    
    org_id = st.session_state.org_id
    conn = init_db()
    
    with st.form("lend_form"):
        st.markdown('<h3>📖 Lend Book to Student</h3>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("👤 Student Name", placeholder="Full name")
            adm = st.text_input("🪪 ADM Number", placeholder="Admission number")
            form = st.text_input("🏫 Form/Class", placeholder="e.g., Form 2")
            book_title = st.selectbox("📚 Book", ["-- Select --"] + pd.read_sql(
                "SELECT title FROM books WHERE org_id = ? AND quantity > 0", conn, params=(org_id,))['title'].tolist())
        with col2:
            stream = st.text_input("📊 Stream", placeholder="e.g., East")
            book_no = st.text_input("🔢 Book Number", placeholder="Book copy number")
            borrow_date = st.date_input("📅 Borrow Date", datetime.now())
            return_date = st.date_input("📅 Return Date", datetime.now() + timedelta(days=14))
        
        if st.form_submit_button("📖 Lend Book", use_container_width=True, type="primary"):
            if not all([name, adm, book_title != "-- Select --", book_no]):
                st.error("⚠️ Please fill all required fields")
            else:
                book = pd.read_sql("SELECT * FROM books WHERE org_id = ? AND title = ?", conn, params=(org_id, book_title))
                if book.empty or book.iloc[0]['quantity'] <= 0:
                    st.error("⚠️ Book out of stock")
                else:
                    c = conn.cursor()
                    c.execute("""INSERT INTO borrowed_books 
                        (id, org_id, student_name, adm_number, form, stream, book_title, book_number, borrow_date, return_date, lending_type)
                        VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
                        (generate_id(), org_id, name, adm, form, stream, book_title, book_no, str(borrow_date), str(return_date), 'individual'))
                    c.execute("UPDATE books SET quantity = quantity - 1 WHERE org_id = ? AND title = ?", (org_id, book_title))
                    conn.commit()
                    add_audit_log(org_id, 'Book Lent', f"{name} borrowed '{book_title}'")
                    st.success(f"✅ Book lent to {name}!")
                    st.rerun()
    
    st.markdown('<h2>📋 Recent Lendings</h2>', unsafe_allow_html=True)
    lendings = pd.read_sql("""SELECT * FROM borrowed_books WHERE org_id = ? 
        AND lending_type = 'individual' AND returned = 0 ORDER BY created_at DESC LIMIT 15""", conn, params=(org_id,))
    
    if not lendings.empty:
        for _, l in lendings.iterrows():
            col1, col2 = st.columns([5, 1])
            with col1:
                st.markdown(f"""
                <div style="background:rgba(255,255,255,0.04);border-radius:10px;padding:12px;margin:5px 0;border-left:3px solid rgba(233,69,96,0.5);">
                    📖 <strong>{l['student_name']}</strong> ({l['adm_number']}) → <em>{l['book_title']}</em> (#{l['book_number']}) | Due: {l['return_date']}
                </div>
                """, unsafe_allow_html=True)
            with col2:
                if st.button("↩️ Return", key=f"ret_{l['id']}"):
                    c = conn.cursor()
                    c.execute("UPDATE borrowed_books SET returned = 1, actual_return_date = ? WHERE id = ?",
                             (str(datetime.now().date()), l['id']))
                    c.execute("UPDATE books SET quantity = quantity + 1 WHERE org_id = ? AND title = ?",
                             (org_id, l['book_title']))
                    conn.commit()
                    add_audit_log(org_id, 'Book Returned', f"{l['student_name']} returned '{l['book_title']}'")
                    st.rerun()
    else:
        st.info("No recent individual lendings")
    
    conn.close()

# ==================== FURNITURE ALLOCATION ====================
def furniture_page():
    st.markdown('<h1>🪑 Furniture Allocation</h1>', unsafe_allow_html=True)
    
    org_id = st.session_state.org_id
    conn = init_db()
    
    col1, col2 = st.columns(2)
    with col1:
        classes = pd.read_sql("SELECT * FROM class_lists WHERE org_id = ?", conn, params=(org_id,))
        class_options = ["-- Select Class --"] + classes['class_name'].tolist() if not classes.empty else ["-- Select Class --"]
        selected_class = st.selectbox("📋 Select Class", class_options)
    with col2:
        alloc_date = st.date_input("📅 Allocation Date", datetime.now())
    
    if st.button("📋 Load Class", use_container_width=True, type="secondary"):
        if selected_class != "-- Select Class --":
            st.session_state.furniture_class = selected_class
            st.rerun()
    
    if st.session_state.furniture_class:
        class_data = pd.read_sql("SELECT * FROM class_lists WHERE org_id = ? AND class_name = ?",
                                 conn, params=(org_id, st.session_state.furniture_class))
        if not class_data.empty:
            students = json.loads(class_data.iloc[0]['data'])
            st.markdown(f'<h2>Assign Furniture to {st.session_state.furniture_class}</h2>', unsafe_allow_html=True)
            
            df_data = []
            for student in students:
                existing = pd.read_sql("SELECT * FROM furniture WHERE org_id = ? AND adm_number = ? AND returned = 0",
                                      conn, params=(org_id, student['adm']))
                is_assigned = not existing.empty
                df_data.append({
                    "Assign": not is_assigned,
                    "Student": student['name'],
                    "ADM": student['adm'],
                    "Chair Number": existing.iloc[0]['chair_number'] if is_assigned else "",
                    "Locker Number": existing.iloc[0]['locker_number'] if is_assigned else "",
                    "Status": "✅ Allocated" if is_assigned else "⏳ Pending"
                })
            
            df = pd.DataFrame(df_data)
            edited_df = st.data_editor(df, hide_index=True, use_container_width=True,
                disabled=["Student", "ADM", "Status"])
            
            if st.button("✅ Assign Furniture", type="primary", use_container_width=True):
                to_assign = edited_df[edited_df['Assign'] == True]
                if to_assign.empty:
                    st.error("⚠️ No students selected")
                else:
                    c = conn.cursor()
                    for _, row in to_assign.iterrows():
                        if row['Chair Number'] or row['Locker Number']:
                            c.execute("""INSERT INTO furniture 
                                (id, org_id, student_name, adm_number, chair_number, locker_number, allocation_date)
                                VALUES (?,?,?,?,?,?,?)""",
                                (generate_id(), org_id, row['Student'], row['ADM'],
                                 row['Chair Number'] if row['Chair Number'] else None,
                                 row['Locker Number'] if row['Locker Number'] else None,
                                 str(alloc_date)))
                    conn.commit()
                    add_audit_log(org_id, 'Furniture Allocated', f"Allocated to {len(to_assign)} students")
                    st.success(f"✅ Allocated to {len(to_assign)} students!")
                    st.session_state.furniture_class = None
                    st.rerun()
    
    st.markdown('<h2>📋 Current Allocations</h2>', unsafe_allow_html=True)
    furniture = pd.read_sql("SELECT * FROM furniture WHERE org_id = ? ORDER BY created_at DESC", conn, params=(org_id,))
    if not furniture.empty:
        for _, f in furniture.iterrows():
            status = "✅ Active" if not f['returned'] else "↩️ Returned"
            col1, col2 = st.columns([5, 1])
            with col1:
                st.markdown(f"""
                <div style="background:rgba(255,255,255,0.04);border-radius:10px;padding:12px;margin:5px 0;">
                    🪑 <strong>{f['student_name']}</strong> ({f['adm_number']}) | Chair: {f['chair_number'] or '-'} | Locker: {f['locker_number'] or '-'} | {f['allocation_date']} | {status}
                </div>
                """, unsafe_allow_html=True)
            with col2:
                if not f['returned'] and st.button("↩️ Return", key=f"ret_f_{f['id']}"):
                    c = conn.cursor()
                    c.execute("UPDATE furniture SET returned = 1, return_date = ? WHERE id = ?",
                             (str(datetime.now().date()), f['id']))
                    conn.commit()
                    add_audit_log(org_id, 'Furniture Returned', f"{f['student_name']}")
                    st.rerun()
    else:
        st.info("No furniture allocations yet")
    
    conn.close()

# ==================== RETURN ITEMS ====================
def return_page():
    st.markdown('<h1>↩️ Return Items</h1>', unsafe_allow_html=True)
    
    org_id = st.session_state.org_id
    conn = init_db()
    
    search = st.text_input("🔍 Search by name, ADM, or item number", placeholder="Type to search...")
    
    if search:
        books = pd.read_sql("""SELECT * FROM borrowed_books WHERE org_id = ? AND returned = 0 
            AND (student_name LIKE ? OR adm_number LIKE ? OR book_number LIKE ?)""",
            conn, params=(org_id, f"%{search}%", f"%{search}%", f"%{search}%"))
        
        furniture = pd.read_sql("""SELECT * FROM furniture WHERE org_id = ? AND returned = 0 
            AND (student_name LIKE ? OR adm_number LIKE ? OR chair_number LIKE ? OR locker_number LIKE ?)""",
            conn, params=(org_id, f"%{search}%", f"%{search}%", f"%{search}%", f"%{search}%"))
        
        if not books.empty:
            st.markdown('<h3>📚 Books</h3>', unsafe_allow_html=True)
            for _, b in books.iterrows():
                col1, col2 = st.columns([5, 1])
                with col1:
                    st.markdown(f"📖 **{b['student_name']}** ({b['adm_number']}) → *{b['book_title']}* (#{b['book_number']}) | Due: {b['return_date']}")
                with col2:
                    if st.button("↩️ Return", key=f"sret_{b['id']}"):
                        c = conn.cursor()
                        c.execute("UPDATE borrowed_books SET returned = 1, actual_return_date = ? WHERE id = ?",
                                 (str(datetime.now().date()), b['id']))
                        c.execute("UPDATE books SET quantity = quantity + 1 WHERE org_id = ? AND title = ?",
                                 (org_id, b['book_title']))
                        conn.commit()
                        st.rerun()
        
        if not furniture.empty:
            st.markdown('<h3>🪑 Furniture</h3>', unsafe_allow_html=True)
            for _, f in furniture.iterrows():
                col1, col2 = st.columns([5, 1])
                with col1:
                    st.markdown(f"🪑 **{f['student_name']}** ({f['adm_number']}) | Chair: {f['chair_number'] or '-'} | Locker: {f['locker_number'] or '-'}")
                with col2:
                    if st.button("↩️ Return", key=f"sret_f_{f['id']}"):
                        c = conn.cursor()
                        c.execute("UPDATE furniture SET returned = 1, return_date = ? WHERE id = ?",
                                 (str(datetime.now().date()), f['id']))
                        conn.commit()
                        st.rerun()
        
        if books.empty and furniture.empty:
            st.info("No active items found matching your search")
    
    conn.close()

# ==================== BORROWED BOOKS ====================
def borrowed_page():
    st.markdown('<h1>📋 Borrowed Books Log</h1>', unsafe_allow_html=True)
    
    org_id = st.session_state.org_id
    conn = init_db()
    
    filter_option = st.radio("🔍 Filter", ["📋 All", "✅ Active", "🔴 Overdue"], horizontal=True)
    
    if filter_option == "✅ Active":
        borrowed = pd.read_sql("SELECT * FROM borrowed_books WHERE org_id = ? AND returned = 0 ORDER BY created_at DESC",
                               conn, params=(org_id,))
    elif filter_option == "🔴 Overdue":
        today = str(datetime.now().date())
        borrowed = pd.read_sql("""SELECT * FROM borrowed_books WHERE org_id = ? AND returned = 0 
            AND return_date < ? ORDER BY return_date""", conn, params=(org_id, today))
    else:
        borrowed = pd.read_sql("SELECT * FROM borrowed_books WHERE org_id = ? ORDER BY created_at DESC", conn, params=(org_id,))
    
    if not borrowed.empty:
        display_df = borrowed[['student_name', 'adm_number', 'book_title', 'book_number', 'borrow_date', 'return_date', 'returned']].copy()
        display_df.columns = ['Student', 'ADM', 'Book', 'Book No', 'Borrowed', 'Due', 'Returned']
        display_df['Returned'] = display_df['Returned'].apply(lambda x: '✅ Yes' if x else '❌ No')
        
        st.dataframe(display_df, use_container_width=True, hide_index=True)
        
        if st.button("📎 Export to Excel", type="secondary"):
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                display_df.to_excel(writer, index=False, sheet_name='Borrowed Books')
            st.download_button("📥 Download Excel", output.getvalue(), f"borrowed_{datetime.now().date()}.xlsx")
    else:
        st.info("No borrowed books found")
    
    conn.close()

# ==================== MEMBERS ====================
def members_page():
    st.markdown('<h1>👥 Members</h1>', unsafe_allow_html=True)
    
    org_id = st.session_state.org_id
    conn = init_db()
    
    if st.session_state.role == 'admin':
        with st.expander("➕ Add Member", expanded=False):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("👤 Full Name", key="mem_name")
            with col2:
                member_id = st.text_input("🪪 Member ID (optional)", key="mem_id")
            if st.button("➕ Add Member", type="primary"):
                if name:
                    c = conn.cursor()
                    mid = member_id or f"MEM-{generate_id()[:8].upper()}"
                    c.execute("INSERT INTO members (id, org_id, name, member_id) VALUES (?,?,?,?)",
                             (generate_id(), org_id, name, mid))
                    conn.commit()
                    add_audit_log(org_id, 'Member Added', f"Added {name} ({mid})")
                    st.success(f"✅ Member {name} added!")
                    st.rerun()
    
    members = pd.read_sql("SELECT * FROM members WHERE org_id = ? ORDER BY name", conn, params=(org_id,))
    if not members.empty:
        for _, m in members.iterrows():
            col1, col2, col3 = st.columns([4, 1, 1])
            with col1:
                st.markdown(f"""
                <div style="background:rgba(255,255,255,0.04);border-radius:10px;padding:12px;margin:5px 0;">
                    👤 <strong>{m['name']}</strong> <span style="color:rgba(255,255,255,0.5);">({m['member_id']})</span>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                if st.button("✏️ Edit", key=f"edit_m_{m['id']}"):
                    st.session_state.editing_member = m['id']
            with col3:
                if st.session_state.role == 'admin' and st.button("🗑️", key=f"del_m_{m['id']}"):
                    c = conn.cursor()
                    c.execute("DELETE FROM members WHERE id = ?", (m['id'],))
                    conn.commit()
                    st.rerun()
            
            if st.session_state.editing_member == m['id']:
                new_name = st.text_input("Edit name", value=m['name'], key=f"en_{m['id']}")
                new_id = st.text_input("Edit ID", value=m['member_id'], key=f"ei_{m['id']}")
                if st.button("💾 Save", key=f"sv_{m['id']}"):
                    c = conn.cursor()
                    c.execute("UPDATE members SET name = ?, member_id = ? WHERE id = ?", (new_name, new_id, m['id']))
                    conn.commit()
                    st.session_state.editing_member = None
                    st.rerun()
    else:
        st.info("No members registered yet")
    
    conn.close()

# ==================== TEACHERS ====================
def teachers_page():
    st.markdown('<h1>👨‍🏫 Teachers</h1>', unsafe_allow_html=True)
    
    org_id = st.session_state.org_id
    conn = init_db()
    
    if st.session_state.role == 'admin':
        with st.expander("➕ Add Teacher", expanded=False):
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                name = st.text_input("👤 Full Name", key="t_name")
            with col2:
                subjects = st.text_input("📚 Subjects Teaching", key="t_subjects")
            with col3:
                classes = st.text_input("🏫 Classes Teaching", key="t_classes")
            with col4:
                duty = st.text_input("📋 Class Assigned", key="t_duty")
            if st.button("➕ Add Teacher", type="primary"):
                if name:
                    c = conn.cursor()
                    c.execute("INSERT INTO teachers (id, org_id, name, subjects, classes, class_assigned) VALUES (?,?,?,?,?,?)",
                             (generate_id(), org_id, name, subjects, classes, duty))
                    conn.commit()
                    add_audit_log(org_id, 'Teacher Added', f"Added {name}")
                    st.success(f"✅ Teacher {name} added!")
                    st.rerun()
    
    teachers = pd.read_sql("SELECT * FROM teachers WHERE org_id = ? ORDER BY name", conn, params=(org_id,))
    if not teachers.empty:
        display = teachers[['name', 'subjects', 'classes', 'class_assigned']].copy()
        display.columns = ['Name', 'Subjects Teaching', 'Classes Teaching', 'Class Assigned']
        st.dataframe(display, use_container_width=True, hide_index=True)
        
        if st.session_state.role == 'admin':
            to_remove = st.selectbox("Select teacher to remove", teachers['name'].tolist())
            if st.button("🗑️ Remove Teacher", type="secondary"):
                c = conn.cursor()
                c.execute("DELETE FROM teachers WHERE org_id = ? AND name = ?", (org_id, to_remove))
                conn.commit()
                add_audit_log(org_id, 'Teacher Removed', f"Removed {to_remove}")
                st.rerun()
    else:
        st.info("No teachers registered yet")
    
    conn.close()

# ==================== CLASS LISTS ====================
def class_page():
    st.markdown('<h1>📋 Class List Manager</h1>', unsafe_allow_html=True)
    
    org_id = st.session_state.org_id
    conn = init_db()
    
    with st.expander("📥 Import from Excel", expanded=False):
        uploaded = st.file_uploader("Choose Excel file (Name & ADM columns)", type=['xlsx', 'xls'])
        if uploaded:
            try:
                df = pd.read_excel(uploaded)
                name_col = next((c for c in df.columns if 'name' in c.lower()), df.columns[0])
                adm_col = next((c for c in df.columns if 'adm' in c.lower() or 'admission' in c.lower()), 
                              df.columns[1] if len(df.columns) > 1 else df.columns[0])
                
                students = [{"name": str(row[name_col]), "adm": str(row[adm_col])} for _, row in df.iterrows()]
                st.session_state.imported_students = students
                st.success(f"✅ Imported {len(students)} students!")
                st.dataframe(pd.DataFrame(students), use_container_width=True)
                
                class_name = st.text_input("💾 Save as class name", placeholder="e.g., Form 1 East 2025")
                if st.button("💾 Save Class List", type="primary") and class_name:
                    c = conn.cursor()
                    existing = pd.read_sql("SELECT * FROM class_lists WHERE org_id = ? AND class_name = ?",
                                          conn, params=(org_id, class_name))
                    if not existing.empty:
                        c.execute("UPDATE class_lists SET data = ? WHERE org_id = ? AND class_name = ?",
                                 (json.dumps(students), org_id, class_name))
                    else:
                        c.execute("INSERT INTO class_lists (id, org_id, class_name, data) VALUES (?,?,?,?)",
                                 (generate_id(), org_id, class_name, json.dumps(students)))
                    conn.commit()
                    add_audit_log(org_id, 'Class Saved', f"'{class_name}' - {len(students)} students")
                    st.success(f"✅ Class '{class_name}' saved!")
                    st.session_state.imported_students = None
                    st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")
    
    st.markdown('<h2>📁 Saved Class Lists</h2>', unsafe_allow_html=True)
    classes = pd.read_sql("SELECT * FROM class_lists WHERE org_id = ?", conn, params=(org_id,))
    if not classes.empty:
        for _, cls in classes.iterrows():
            students = json.loads(cls['data'])
            with st.expander(f"📋 {cls['class_name']} ({len(students)} students)"):
                st.dataframe(pd.DataFrame(students), use_container_width=True)
                if st.button(f"🗑️ Delete {cls['class_name']}", key=f"dc_{cls['id']}"):
                    c = conn.cursor()
                    c.execute("DELETE FROM class_lists WHERE id = ?", (cls['id'],))
                    conn.commit()
                    st.rerun()
    else:
        st.info("No saved class lists")
    
    conn.close()

# ==================== QR CODES ====================
def qr_page():
    st.markdown('<h1>📱 QR Code Management</h1>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["🏷️ Generate QR Codes", "📷 Scan QR Code"])
    
    with tab1:
        col1, col2, col3 = st.columns(3)
        with col1:
            qr_type = st.selectbox("Type", ["book", "chair", "locker"])
        with col2:
            start = st.number_input("Start", min_value=1, value=1)
        with col3:
            end = st.number_input("End", min_value=start, max_value=start+100, value=min(start+9, start+99))
        
        if st.button("🏷️ Generate QR Codes", type="primary", use_container_width=True):
            cols = st.columns(5)
            for i in range(start, end + 1):
                data = f"{qr_type}-{i}"
                qr_img = generate_qr_code(data)
                with cols[(i - start) % 5]:
                    st.markdown(f"""
                    <div style="text-align:center;padding:10px;background:white;border-radius:12px;margin:5px;box-shadow:0 4px 15px rgba(0,0,0,0.2);">
                        <img src="data:image/png;base64,{qr_img}" width="100">
                        <p style="color:black;font-weight:700;margin:5px 0;">{qr_type.upper()}: {i}</p>
                    </div>
                    """, unsafe_allow_html=True)
    
    with tab2:
        st.info("📷 Use a mobile device camera or enter scanned code manually")
        scanned = st.text_input("Enter scanned QR code", placeholder="e.g., book-5")
        if scanned and st.button("Process Code", type="secondary"):
            parts = scanned.split('-')
            if len(parts) == 2:
                st.success(f"✅ Scanned: {parts[0].upper()} #{parts[1]}")

# ==================== STAFF CHAT ====================
def chat_page():
    st.markdown('<h1>💬 Staff Chat</h1>', unsafe_allow_html=True)
    
    org_id = st.session_state.org_id
    conn = init_db()
    current_user = st.session_state.user['name']
    
    users = pd.read_sql("SELECT * FROM users WHERE org_id = ? AND name != ?", conn, params=(org_id, current_user))
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.markdown('<h3>👥 Staff</h3>', unsafe_allow_html=True)
        if not users.empty:
            for _, u in users.iterrows():
                unread = pd.read_sql(
                    "SELECT COUNT(*) as cnt FROM chat_messages WHERE org_id = ? AND from_user = ? AND to_user = ? AND read = 0",
                    conn, params=(org_id, u['name'], current_user)).iloc[0]['cnt']
                badge = f" 🔴{unread}" if unread > 0 else ""
                if st.button(f"👤 {u['name']}{badge}", key=f"cu_{u['id']}", use_container_width=True):
                    st.session_state.chat_active_user = u['name']
                    c = conn.cursor()
                    c.execute("UPDATE chat_messages SET read = 1 WHERE org_id = ? AND from_user = ? AND to_user = ?",
                             (org_id, u['name'], current_user))
                    conn.commit()
                    st.rerun()
    
    with col2:
        if st.session_state.chat_active_user:
            st.markdown(f'<h3>💬 Chat with {st.session_state.chat_active_user}</h3>', unsafe_allow_html=True)
            
            messages = pd.read_sql("""
                SELECT * FROM chat_messages WHERE org_id = ? 
                AND ((from_user = ? AND to_user = ?) OR (from_user = ? AND to_user = ?))
                ORDER BY created_at""",
                conn, params=(org_id, current_user, st.session_state.chat_active_user,
                            st.session_state.chat_active_user, current_user))
            
            chat_container = st.container(height=350)
            with chat_container:
                if not messages.empty:
                    for _, msg in messages.iterrows():
                        is_sent = msg['from_user'] == current_user
                        align = "right" if is_sent else "left"
                        bg = "rgba(233,69,96,0.3)" if is_sent else "rgba(255,255,255,0.08)"
                        st.markdown(f"""
                        <div style="text-align:{align};margin:8px 0;">
                            <div style="display:inline-block;background:{bg};padding:10px 16px;border-radius:15px;max-width:70%;backdrop-filter:blur(10px);border:1px solid rgba(255,255,255,0.1);">
                                <p style="margin:0;color:white;">{msg['message']}</p>
                                <small style="color:rgba(255,255,255,0.4);">{msg['created_at'][:16]}</small>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info("No messages yet. Start the conversation!")
            
            with st.form("send_msg", clear_on_submit=True):
                msg_input = st.text_input("Type a message...", key="chat_input")
                if st.form_submit_button("📤 Send"):
                    if msg_input:
                        c = conn.cursor()
                        c.execute("INSERT INTO chat_messages (id, org_id, from_user, to_user, message) VALUES (?,?,?,?,?)",
                                 (generate_id(), org_id, current_user, st.session_state.chat_active_user, msg_input))
                        conn.commit()
                        st.rerun()
        else:
            st.info("👈 Select a staff member to start chatting")
    
    conn.close()

# ==================== SYSTEM OVERVIEW ====================
def overview_page():
    st.markdown('<h1>🔍 System Overview</h1>', unsafe_allow_html=True)
    
    org_id = st.session_state.org_id
    conn = init_db()
    
    org = pd.read_sql("SELECT * FROM organizations WHERE id = ?", conn, params=(org_id,)).iloc[0]
    books = pd.read_sql("SELECT * FROM books WHERE org_id = ?", conn, params=(org_id,))
    borrowed = pd.read_sql("SELECT * FROM borrowed_books WHERE org_id = ? AND returned = 0", conn, params=(org_id,))
    furniture = pd.read_sql("SELECT * FROM furniture WHERE org_id = ? AND returned = 0", conn, params=(org_id,))
    members = pd.read_sql("SELECT * FROM members WHERE org_id = ?", conn, params=(org_id,))
    teachers = pd.read_sql("SELECT * FROM teachers WHERE org_id = ?", conn, params=(org_id,))
    users = pd.read_sql("SELECT * FROM users WHERE org_id = ?", conn, params=(org_id,))
    chats = pd.read_sql("SELECT * FROM chat_messages WHERE org_id = ?", conn, params=(org_id,))
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div style="background:rgba(255,255,255,0.06);border-radius:16px;padding:20px;border:1px solid rgba(255,255,255,0.1);">
            <h3>🏫 School</h3>
            <p><strong>Name:</strong> {org['name']}</p>
            <p><strong>Address:</strong> {org['address'] or 'Not set'}</p>
            <p><strong>Admin:</strong> {org['admin_name']}</p>
            <p><strong>Email:</strong> {org['admin_email']}</p>
            <p><strong>Invite Code:</strong> <code style="color:#f0d060;">{org['invite_code']}</code></p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div style="background:rgba(255,255,255,0.06);border-radius:16px;padding:20px;border:1px solid rgba(255,255,255,0.1);">
            <h3>👥 People</h3>
            <p><strong>Staff:</strong> {len(users)} | <strong>Teachers:</strong> {len(teachers)} | <strong>Members:</strong> {len(members)}</p>
            <h3>💬 Communication</h3>
            <p><strong>Messages:</strong> {len(chats)}</p>
            <h3>📚 Books</h3>
            <p><strong>Total:</strong> {books['quantity'].sum() if not books.empty else 0} | <strong>Active Loans:</strong> {len(borrowed)}</p>
        </div>
        """, unsafe_allow_html=True)
    
    if not books.empty:
        fig = px.pie(books, values='quantity', names='type', title='Books by Type',
                    color_discrete_sequence=['#e94560', '#d4af37', '#8b5cf6', '#06b6d4', '#28a745'])
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='white')
        st.plotly_chart(fig, use_container_width=True)
    
    conn.close()

# ==================== AUDIT LOG ====================
def audit_page():
    st.markdown('<h1>📝 Audit Log</h1>', unsafe_allow_html=True)
    
    org_id = st.session_state.org_id
    conn = init_db()
    
    search = st.text_input("🔍 Search log", placeholder="Filter by action or user...")
    
    if search:
        logs = pd.read_sql("SELECT * FROM audit_log WHERE org_id = ? AND (action LIKE ? OR user_name LIKE ? OR details LIKE ?) ORDER BY created_at DESC LIMIT 100",
                          conn, params=(org_id, f"%{search}%", f"%{search}%", f"%{search}%"))
    else:
        logs = pd.read_sql("SELECT * FROM audit_log WHERE org_id = ? ORDER BY created_at DESC LIMIT 100", conn, params=(org_id,))
    
    if not logs.empty:
        st.dataframe(logs[['created_at', 'user_name', 'action', 'details']].rename(
            columns={'created_at': 'Timestamp', 'user_name': 'User', 'action': 'Action', 'details': 'Details'}
        ), use_container_width=True, hide_index=True)
    else:
        st.info("No audit log entries")
    
    conn.close()

# ==================== REPORTS ====================
def reports_page():
    st.markdown('<h1>📈 Reports & Analytics</h1>', unsafe_allow_html=True)
    
    org_id = st.session_state.org_id
    conn = init_db()
    
    report_type = st.selectbox("📊 Report Type", ["Book Summary", "Furniture Summary", "Overdue Items", "Complete Report"])
    
    if st.button("📊 Generate Report", type="primary", use_container_width=True):
        if report_type == "Book Summary":
            data = pd.read_sql("SELECT * FROM borrowed_books WHERE org_id = ?", conn, params=(org_id,))
            if not data.empty:
                st.dataframe(data, use_container_width=True)
                output = BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as w:
                    data.to_excel(w, index=False)
                st.download_button("📥 Download", output.getvalue(), "book_report.xlsx")
        
        elif report_type == "Complete Report":
            borrowed = pd.read_sql("SELECT * FROM borrowed_books WHERE org_id = ? AND returned = 0", conn, params=(org_id,))
            furniture = pd.read_sql("SELECT * FROM furniture WHERE org_id = ? AND returned = 0", conn, params=(org_id,))
            teachers = pd.read_sql("SELECT * FROM teachers WHERE org_id = ?", conn, params=(org_id,))
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Active Loans", len(borrowed))
                st.metric("Active Furniture", len(furniture))
            with col2:
                st.metric("Teachers", len(teachers))
                st.metric("Overdue", len(borrowed[borrowed['return_date'] < str(datetime.now().date())]) if not borrowed.empty else 0)
    
    conn.close()

# ==================== WALLPAPER ====================
def wallpaper_page():
    st.markdown('<h1>🖼️ Theme & Wallpaper</h1>', unsafe_allow_html=True)
    st.caption("Choose a beautiful wallpaper for your dashboard")
    
    cols = st.columns(4)
    for i, wp in enumerate(WALLPAPERS):
        with cols[i % 4]:
            st.image(wp['url'], caption=wp['name'], use_container_width=True)
            if st.button(f"🎨 Apply", key=f"wp_{i}", use_container_width=True):
                st.session_state.wallpaper = wp['url']
                st.success(f"✅ {wp['name']} applied!")
                st.rerun()
    
    st.markdown("---")
    uploaded = st.file_uploader("📤 Upload custom wallpaper", type=['png', 'jpg', 'jpeg'])
    if uploaded:
        st.session_state.wallpaper = base64.b64encode(uploaded.read()).decode()
        st.success("✅ Custom wallpaper applied!")
        st.rerun()
    
    if st.button("🔄 Reset Default", type="secondary"):
        st.session_state.wallpaper = None
        st.rerun()

# ==================== SETTINGS ====================
def settings_page():
    st.markdown('<h1>⚙️ Settings</h1>', unsafe_allow_html=True)
    
    org_id = st.session_state.org_id
    conn = init_db()
    
    tab1, tab2 = st.tabs(["👥 Staff Management", "💾 Data Management"])
    
    with tab1:
        if st.session_state.role == 'admin':
            with st.expander("➕ Create Staff Account", expanded=False):
                col1, col2, col3 = st.columns(3)
                with col1:
                    email = st.text_input("📧 Email")
                    name = st.text_input("👤 Name")
                with col2:
                    role = st.selectbox("🪪 Role", ["teacher", "librarian", "admin"])
                with col3:
                    password = st.text_input("🔒 Password", type="password", placeholder="Auto if empty")
                
                if st.button("➕ Create Staff", type="primary"):
                    if email and name:
                        c = conn.cursor()
                        pw = hash_password(password) if password else hash_password(generate_id()[:8])
                        staff_id = f"{role.upper()}-{generate_id()[:8].upper()}"
                        c.execute("INSERT INTO users (id, org_id, name, email, role, password, invite_code, staff_id) VALUES (?,?,?,?,?,?,?,?)",
                                 (generate_id(), org_id, name, email, role, pw, st.session_state.invite_code, staff_id))
                        conn.commit()
                        st.success(f"✅ Created! Staff ID: {staff_id}")
                        st.rerun()
        
        users = pd.read_sql("SELECT * FROM users WHERE org_id = ?", conn, params=(org_id,))
        if not users.empty:
            for _, u in users.iterrows():
                col1, col2 = st.columns([5, 1])
                with col1:
                    badge_class = f"badge-{u['role']}"
                    st.markdown(f"""
                    <div style="background:rgba(255,255,255,0.04);border-radius:10px;padding:12px;margin:5px 0;">
                        <strong>{u['name']}</strong> - {u['email']} | 
                        <span class="badge {badge_class}">{u['role'].upper()}</span> | 
                        ID: {u['staff_id'] or 'N/A'}
                    </div>
                    """, unsafe_allow_html=True)
                with col2:
                    if st.session_state.role == 'admin' and u['role'] != 'admin':
                        if st.button("🗑️", key=f"ds_{u['id']}"):
                            c = conn.cursor()
                            c.execute("DELETE FROM users WHERE id = ?", (u['id'],))
                            conn.commit()
                            st.rerun()
    
    with tab2:
        st.subheader("Data Management")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📥 Export Backup", use_container_width=True):
                tables = ['books', 'members', 'teachers', 'borrowed_books', 'furniture', 'class_lists']
                data = {}
                for table in tables:
                    df = pd.read_sql(f"SELECT * FROM {table} WHERE org_id = ?", conn, params=(org_id,))
                    data[table] = df.to_dict()
                st.download_button("📥 Download Backup", json.dumps(data, default=str), "srms_backup.json")
        with col2:
            if st.button("⚠️ Clear All Data", use_container_width=True):
                if st.checkbox("I understand this cannot be undone"):
                    if st.button("Confirm Delete", type="primary"):
                        c = conn.cursor()
                        for table in ['books', 'members', 'teachers', 'borrowed_books', 'furniture', 'class_lists', 'audit_log', 'chat_messages']:
                            c.execute(f"DELETE FROM {table} WHERE org_id = ?", (org_id,))
                        conn.commit()
                        st.error("All data cleared!")
                        st.rerun()
    
    conn.close()

# ==================== MAIN APP ====================
def main():
    """Main application entry point"""
    init_db()
    init_session_state()
    inject_custom_css()
    
    if not st.session_state.authenticated:
        auth_page()
        return
    
    render_sidebar()
    
    # Route to correct page
    pages = {
        "📊 Dashboard": dashboard_page,
        "📚 Book Catalog": catalog_page,
        "📖 Book Issuing (Class)": book_issuing_page,
        "👤 Individual Lending": lending_page,
        "🪑 Furniture Allocation": furniture_page,
        "↩️ Return Items": return_page,
        "📋 Borrowed Books": borrowed_page,
        "👥 Members": members_page,
        "👨‍🏫 Teachers": teachers_page,
        "📋 Class Lists": class_page,
        "📱 QR Codes": qr_page,
        "💬 Staff Chat": chat_page,
        "🔍 System Overview": overview_page,
        "📝 Audit Log": audit_page,
        "📈 Reports": reports_page,
        "🖼️ Theme & Wallpaper": wallpaper_page,
        "⚙️ Settings": settings_page,
    }
    
    current_page = st.session_state.get('page', '📊 Dashboard')
    if current_page in pages:
        pages[current_page]()
    
    # Footer
    st.markdown("""
    <div style="text-align:center;padding:20px;margin-top:30px;border-top:1px solid rgba(255,255,255,0.1);">
        <p style="color:rgba(255,255,255,0.5);font-size:0.8em;">SRMS - School Resource Management System v6.0 | <span class="credit-text">by WeGEM (Edwin)</span> | © 2025</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
