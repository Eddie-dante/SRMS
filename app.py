# app.py - SRMS: School Resource Management System
# Deploy on Streamlit Cloud: https://streamlit.io/cloud
# Requirements: pip install streamlit pandas openpyxl qrcode pillow email-validator plotly

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
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go
import sqlite3
import time

# ==================== DATABASE SETUP ====================
def init_db():
    """Initialize SQLite database"""
    conn = sqlite3.connect('srms.db')
    c = conn.cursor()
    
    # Users table
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        org_id TEXT,
        name TEXT,
        email TEXT,
        phone TEXT,
        role TEXT,
        password TEXT,
        invite_code TEXT,
        staff_id TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Organizations table
    c.execute('''CREATE TABLE IF NOT EXISTS organizations (
        id TEXT PRIMARY KEY,
        name TEXT,
        invite_code TEXT UNIQUE,
        admin_name TEXT,
        admin_email TEXT,
        admin_phone TEXT,
        address TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Books table
    c.execute('''CREATE TABLE IF NOT EXISTS books (
        id TEXT PRIMARY KEY,
        org_id TEXT,
        title TEXT,
        type TEXT,
        quantity INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Members table
    c.execute('''CREATE TABLE IF NOT EXISTS members (
        id TEXT PRIMARY KEY,
        org_id TEXT,
        name TEXT,
        member_id TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Teachers table
    c.execute('''CREATE TABLE IF NOT EXISTS teachers (
        id TEXT PRIMARY KEY,
        org_id TEXT,
        name TEXT,
        subjects TEXT,
        classes TEXT,
        class_assigned TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Borrowed books table
    c.execute('''CREATE TABLE IF NOT EXISTS borrowed_books (
        id TEXT PRIMARY KEY,
        org_id TEXT,
        student_name TEXT,
        adm_number TEXT,
        form TEXT,
        stream TEXT,
        book_title TEXT,
        book_number TEXT,
        borrow_date TEXT,
        return_date TEXT,
        actual_return_date TEXT,
        returned INTEGER DEFAULT 0,
        lending_type TEXT DEFAULT 'individual',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Furniture allocations table
    c.execute('''CREATE TABLE IF NOT EXISTS furniture (
        id TEXT PRIMARY KEY,
        org_id TEXT,
        student_name TEXT,
        adm_number TEXT,
        chair_number TEXT,
        locker_number TEXT,
        allocation_date TEXT,
        return_date TEXT,
        returned INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Class lists table
    c.execute('''CREATE TABLE IF NOT EXISTS class_lists (
        id TEXT PRIMARY KEY,
        org_id TEXT,
        class_name TEXT,
        data TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Audit log table
    c.execute('''CREATE TABLE IF NOT EXISTS audit_log (
        id TEXT PRIMARY KEY,
        org_id TEXT,
        user_name TEXT,
        action TEXT,
        details TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Chat messages table
    c.execute('''CREATE TABLE IF NOT EXISTS chat_messages (
        id TEXT PRIMARY KEY,
        org_id TEXT,
        from_user TEXT,
        to_user TEXT,
        message TEXT,
        read INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Wallpaper/theme settings
    c.execute('''CREATE TABLE IF NOT EXISTS settings (
        id TEXT PRIMARY KEY,
        org_id TEXT,
        setting_key TEXT,
        setting_value TEXT,
        UNIQUE(org_id, setting_key)
    )''')
    
    conn.commit()
    conn.close()

# ==================== SESSION STATE INITIALIZATION ====================
def init_session_state():
    """Initialize all session state variables"""
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'org_id' not in st.session_state:
        st.session_state.org_id = None
    if 'org_name' not in st.session_state:
        st.session_state.org_name = None
    if 'role' not in st.session_state:
        st.session_state.role = None
    if 'invite_code' not in st.session_state:
        st.session_state.invite_code = None
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'page' not in st.session_state:
        st.session_state.page = 'login'
    if 'wallpaper' not in st.session_state:
        st.session_state.wallpaper = None
    if 'chat_active_user' not in st.session_state:
        st.session_state.chat_active_user = None

# ==================== HELPER FUNCTIONS ====================
def generate_id():
    """Generate a unique ID"""
    return str(uuid.uuid4())

def hash_password(password: str) -> str:
    """Hash a password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def generate_invite_code() -> str:
    """Generate a random invite code"""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

def add_audit_log(org_id: str, action: str, details: str):
    """Add an entry to the audit log"""
    conn = sqlite3.connect('srms.db')
    c = conn.cursor()
    user_name = st.session_state.user.get('name', 'System') if st.session_state.user else 'System'
    c.execute('INSERT INTO audit_log (id, org_id, user_name, action, details) VALUES (?,?,?,?,?)',
              (generate_id(), org_id, user_name, action, details))
    conn.commit()
    conn.close()

def get_db_connection():
    """Get database connection"""
    return sqlite3.connect('srms.db')

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
]

# ==================== STYLING ====================
def apply_custom_css():
    """Apply custom CSS styling"""
    wallpaper = st.session_state.wallpaper
    bg_style = f'background-image: url("{wallpaper}"); background-size: cover; background-position: center; background-attachment: fixed;' if wallpaper else 'background: linear-gradient(135deg, #0a0e27, #1a1f4e, #0f3460);'
    
    st.markdown(f"""
    <style>
        /* Main styling */
        .stApp {{
            {bg_style}
        }}
        
        /* Overlay for readability */
        .main .block-container {{
            background: rgba(0, 0, 0, 0.75);
            backdrop-filter: blur(10px);
            border-radius: 16px;
            padding: 2rem;
            border: 1px solid rgba(255,255,255,0.1);
        }}
        
        /* Headers */
        h1, h2, h3 {{
            color: #ffffff !important;
            text-shadow: 0 2px 4px rgba(0,0,0,0.5);
        }}
        
        /* Cards */
        .stMetric {{
            background: rgba(255,255,255,0.08) !important;
            border: 1px solid rgba(255,255,255,0.15) !important;
            border-radius: 12px !important;
            padding: 15px !important;
            border-left: 4px solid #e94560 !important;
        }}
        
        .stMetric label {{
            color: rgba(255,255,255,0.75) !important;
        }}
        
        .stMetric [data-testid="stMetricValue"] {{
            color: #ffffff !important;
            font-size: 2em !important;
        }}
        
        /* Buttons */
        .stButton > button {{
            background: rgba(233, 69, 96, 0.7) !important;
            color: white !important;
            border: 1px solid rgba(255,255,255,0.2) !important;
            border-radius: 8px !important;
            transition: all 0.3s !important;
        }}
        
        .stButton > button:hover {{
            background: rgba(233, 69, 96, 0.9) !important;
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        }}
        
        /* Inputs */
        .stTextInput > div > div > input,
        .stSelectbox > div > div,
        .stDateInput > div > div > input {{
            background: rgba(255,255,255,0.1) !important;
            color: white !important;
            border: 1px solid rgba(255,255,255,0.2) !important;
            border-radius: 8px !important;
        }}
        
        /* Tables */
        .stDataFrame {{
            background: rgba(255,255,255,0.05) !important;
            border-radius: 12px !important;
            overflow: hidden;
        }}
        
        .stDataFrame th {{
            background: rgba(10, 14, 39, 0.8) !important;
            color: white !important;
        }}
        
        .stDataFrame td {{
            color: rgba(255,255,255,0.9) !important;
        }}
        
        /* Expanders */
        .streamlit-expanderHeader {{
            background: rgba(255,255,255,0.08) !important;
            color: white !important;
            border-radius: 12px !important;
        }}
        
        /* Success/Error messages */
        .stAlert {{
            background: rgba(40, 167, 69, 0.2) !important;
            color: white !important;
            border: 1px solid rgba(40, 167, 69, 0.3) !important;
        }}
        
        /* Sidebar */
        .stSidebar {{
            background: rgba(10, 14, 39, 0.9) !important;
            backdrop-filter: blur(10px) !important;
        }}
        
        .stSidebar * {{
            color: white !important;
        }}
        
        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {{
            background: rgba(255,255,255,0.05) !important;
            border-radius: 12px !important;
            gap: 5px !important;
        }}
        
        .stTabs [data-baseweb="tab"] {{
            color: white !important;
            border-radius: 8px !important;
        }}
        
        .stTabs [aria-selected="true"] {{
            background: rgba(233, 69, 96, 0.6) !important;
        }}
        
        /* Chat styling */
        .chat-message {{
            padding: 10px 15px;
            border-radius: 15px;
            margin: 5px 0;
            max-width: 70%;
        }}
        
        .chat-sent {{
            background: rgba(233, 69, 96, 0.3);
            margin-left: auto;
            text-align: right;
        }}
        
        .chat-received {{
            background: rgba(255,255,255,0.1);
            margin-right: auto;
        }}
        
        /* Logo */
        .logo-text {{
            font-size: 3em;
            font-weight: 900;
            background: linear-gradient(180deg, #f0d060, #d4af37, #b8941f);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
            letter-spacing: 8px;
        }}
        
        .credit-text {{
            color: #d4af37;
            text-align: center;
            font-weight: 500;
        }}
    </style>
    """, unsafe_allow_html=True)

# ==================== QR CODE GENERATION ====================
def generate_qr_code(data: str) -> str:
    """Generate QR code and return as base64 string"""
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

# ==================== AUTHENTICATION PAGES ====================
def auth_page():
    """Display authentication page"""
    apply_custom_css()
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<div class="logo-text">SRMS</div>', unsafe_allow_html=True)
        st.markdown('<p style="text-align:center;color:rgba(255,255,255,0.8);font-size:1.2em;">School Resource Management System</p>', unsafe_allow_html=True)
        st.markdown('<p class="credit-text">by <strong style="color:#f0d060;">WeGEM</strong> (Edwin)</p>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        tab1, tab2, tab3 = st.tabs(["🔑 Login", "📝 Sign Up", "🏫 Create School"])
        
        with tab1:
            with st.form("login_form"):
                st.subheader("Staff Login")
                name = st.text_input("👤 Full Name", placeholder="Your registered name")
                school = st.text_input("🏢 School Name", placeholder="School name")
                code = st.text_input("🔑 Invite Code", placeholder="Enter invite code")
                password = st.text_input("🔒 Password", type="password")
                submitted = st.form_submit_button("🔑 Login", use_container_width=True)
                
                if submitted:
                    if not all([name, school, code, password]):
                        st.error("Please fill all fields")
                    else:
                        conn = get_db_connection()
                        c = conn.cursor()
                        c.execute("SELECT * FROM organizations WHERE name = ?", (school,))
                        org = c.fetchone()
                        if not org:
                            st.error("School not found")
                        else:
                            org_id = org[0]
                            invite = org[2]
                            if code.upper() != invite:
                                st.error("Invalid invite code")
                            else:
                                hashed_pw = hash_password(password)
                                c.execute("SELECT * FROM users WHERE org_id = ? AND name = ? AND password = ?", 
                                         (org_id, name, hashed_pw))
                                user = c.fetchone()
                                if not user:
                                    st.error("Invalid credentials")
                                else:
                                    st.session_state.user = {
                                        'id': user[0], 'name': user[2], 'email': user[3],
                                        'role': user[5], 'staff_id': user[7]
                                    }
                                    st.session_state.org_id = org_id
                                    st.session_state.org_name = org[1]
                                    st.session_state.role = user[5]
                                    st.session_state.invite_code = invite
                                    st.session_state.authenticated = True
                                    add_audit_log(org_id, 'Login', f"{name} logged in")
                                    st.rerun()
                        conn.close()
        
        with tab2:
            with st.form("signup_form"):
                st.subheader("Staff Sign Up")
                st.caption("Join your school's management system")
                name = st.text_input("👤 Full Name", key="signup_name")
                email = st.text_input("📧 Email", key="signup_email")
                phone = st.text_input("📞 Phone", key="signup_phone", placeholder="+1234567890")
                school = st.text_input("🏢 School Name", key="signup_school")
                code = st.text_input("🔑 Invite Code", key="signup_code", placeholder="From your admin")
                staff_id = st.text_input("🪪 Staff ID (Optional)", key="signup_staff_id")
                password = st.text_input("🔒 Password", type="password", key="signup_password", placeholder="Min 6 characters")
                submitted = st.form_submit_button("📝 Sign Up", use_container_width=True)
                
                if submitted:
                    if not all([name, email, school, code, password]):
                        st.error("Please fill all required fields")
                    elif len(password) < 6:
                        st.error("Password must be at least 6 characters")
                    else:
                        conn = get_db_connection()
                        c = conn.cursor()
                        c.execute("SELECT * FROM organizations WHERE name = ?", (school,))
                        org = c.fetchone()
                        if not org:
                            st.error("School not found")
                        elif code.upper() != org[2]:
                            st.error("Invalid invite code")
                        else:
                            org_id = org[0]
                            c.execute("SELECT * FROM users WHERE org_id = ? AND email = ?", (org_id, email))
                            if c.fetchone():
                                st.error("Email already registered")
                            else:
                                uid = generate_id()
                                hashed_pw = hash_password(password)
                                sid = staff_id or f"STF-{uid[:8].upper()}"
                                c.execute("INSERT INTO users (id, org_id, name, email, phone, role, password, invite_code, staff_id) VALUES (?,?,?,?,?,?,?,?,?)",
                                         (uid, org_id, name, email, phone, 'teacher', hashed_pw, code.upper(), sid))
                                conn.commit()
                                add_audit_log(org_id, 'Signup', f"{name} signed up as teacher")
                                st.success(f"Account created! Your Staff ID: {sid}")
                                st.info("Please login with your credentials")
                        conn.close()
        
        with tab3:
            with st.form("create_school_form"):
                st.subheader("Create New School")
                st.caption("Set up your school's management system")
                school_name = st.text_input("🏢 School Name", key="create_school")
                address = st.text_input("📍 School Address", key="create_address")
                admin_name = st.text_input("👤 Admin Name", key="create_admin")
                admin_email = st.text_input("📧 Admin Email", key="create_email")
                admin_phone = st.text_input("📞 Admin Phone", key="create_phone")
                password = st.text_input("🔒 Password", type="password", key="create_password", placeholder="Min 8 characters")
                password_confirm = st.text_input("🔒 Confirm Password", type="password", key="create_password_confirm")
                submitted = st.form_submit_button("🚀 Create School", use_container_width=True)
                
                if submitted:
                    if not all([school_name, admin_name, admin_email, password]):
                        st.error("Please fill all required fields")
                    elif password != password_confirm:
                        st.error("Passwords don't match")
                    elif len(password) < 8:
                        st.error("Password must be at least 8 characters")
                    else:
                        conn = get_db_connection()
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
                        conn.close()
                        
                        st.success(f"School created! Invite Code: **{invite}**")
                        st.info("Share this code with your staff. Please login to continue.")

# ==================== DASHBOARD ====================
def dashboard_page():
    """Display dashboard"""
    st.header("📊 Dashboard")
    
    conn = get_db_connection()
    org_id = st.session_state.org_id
    
    # Get statistics
    books = pd.read_sql("SELECT * FROM books WHERE org_id = ?", conn, params=(org_id,))
    total_books = books['quantity'].sum() if not books.empty else 0
    
    borrowed = pd.read_sql("SELECT * FROM borrowed_books WHERE org_id = ? AND returned = 0", conn, params=(org_id,))
    books_borrowed = len(borrowed)
    
    overdue = 0
    if not borrowed.empty:
        today = datetime.now().date()
        for _, row in borrowed.iterrows():
            try:
                return_date = datetime.strptime(row['return_date'], '%Y-%m-%d').date()
                if return_date < today:
                    overdue += 1
            except:
                pass
    
    members = pd.read_sql("SELECT * FROM members WHERE org_id = ?", conn, params=(org_id,))
    teachers = pd.read_sql("SELECT * FROM teachers WHERE org_id = ?", conn, params=(org_id,))
    furniture = pd.read_sql("SELECT * FROM furniture WHERE org_id = ? AND returned = 0", conn, params=(org_id,))
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📚 Total Books", total_books)
        st.metric("👥 Members", len(members))
    with col2:
        st.metric("📖 Books Borrowed", books_borrowed)
        st.metric("👨‍🏫 Teachers", len(teachers))
    with col3:
        st.metric("📗 Available", total_books - books_borrowed)
        st.metric("🪑 Furniture Items", len(furniture))
    with col4:
        st.metric("🔴 Overdue", overdue)
        st.metric("✅ Active Loans", books_borrowed)
    
    # Invite Code Banner
    st.markdown(f"""
    <div style="background: rgba(255,255,255,0.1); border: 2px dashed rgba(233,69,96,0.5); border-radius: 12px; padding: 20px; text-align: center; margin: 20px 0;">
        <p style="color: rgba(255,255,255,0.7); margin: 0;">🏫 School Invite Code</p>
        <p style="font-size: 2em; font-weight: 800; letter-spacing: 6px; color: white; font-family: monospace; margin: 10px 0;">{st.session_state.invite_code}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Recent Activity
    st.subheader("Recent Activity")
    logs = pd.read_sql("SELECT * FROM audit_log WHERE org_id = ? ORDER BY created_at DESC LIMIT 10", conn, params=(org_id,))
    if not logs.empty:
        for _, log in logs.iterrows():
            st.text(f"🕐 {log['created_at'][:19]} | 👤 {log['user_name']} | {log['action']}: {log['details']}")
    else:
        st.info("No recent activity")
    
    conn.close()

# ==================== BOOK CATALOG ====================
def book_catalog_page():
    """Display and manage book catalog"""
    st.header("📚 Book Catalog")
    
    org_id = st.session_state.org_id
    conn = get_db_connection()
    
    # Add book form
    with st.expander("➕ Add / Update Book", expanded=False):
        with st.form("add_book_form"):
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                title = st.text_input("Book Title")
            with col2:
                book_type = st.selectbox("Type", ["Textbook", "Novel", "Reference", "Magazine", "Other"])
            with col3:
                quantity = st.number_input("Quantity", min_value=1, value=1)
            
            if st.form_submit_button("📖 Add / Update Book", use_container_width=True):
                if title:
                    c = conn.cursor()
                    existing = pd.read_sql("SELECT * FROM books WHERE org_id = ? AND title = ?", conn, params=(org_id, title))
                    if not existing.empty:
                        new_qty = existing.iloc[0]['quantity'] + quantity
                        c.execute("UPDATE books SET quantity = ?, type = ? WHERE org_id = ? AND title = ?",
                                 (new_qty, book_type, org_id, title))
                        conn.commit()
                        add_audit_log(org_id, 'Book Updated', f"Updated '{title}' - added {quantity} copies")
                        st.success(f"Updated '{title}'! New quantity: {new_qty}")
                    else:
                        c.execute("INSERT INTO books (id, org_id, title, type, quantity) VALUES (?,?,?,?,?)",
                                 (generate_id(), org_id, title, book_type, quantity))
                        conn.commit()
                        add_audit_log(org_id, 'Book Added', f"Added '{title}' ({book_type}) - {quantity} copies")
                        st.success(f"Added '{title}'!")
    
    # Display catalog
    st.subheader("Current Catalog")
    books = pd.read_sql("SELECT * FROM books WHERE org_id = ? ORDER BY title", conn, params=(org_id,))
    
    if not books.empty:
        for _, book in books.iterrows():
            qty = book['quantity']
            badge = "🔴 Out of Stock" if qty == 0 else ("🟡 Low Stock" if qty < 5 else "🟢 In Stock")
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"**{book['title']}** - *{book['type']}* | Qty: **{qty}** | {badge}")
            with col2:
                if st.button("🗑️ Delete", key=f"del_book_{book['id']}"):
                    c = conn.cursor()
                    c.execute("DELETE FROM books WHERE id = ?", (book['id'],))
                    conn.commit()
                    add_audit_log(org_id, 'Book Deleted', f"Deleted '{book['title']}'")
                    st.rerun()
    else:
        st.info("No books in catalog")
    
    conn.close()

# ==================== BOOK ISSUING (Class Based) ====================
def book_issuing_page():
    """Bulk book issuing to a class"""
    st.header("📖 Bulk Book Issuing to Class")
    
    org_id = st.session_state.org_id
    conn = get_db_connection()
    
    col1, col2 = st.columns(2)
    with col1:
        books = pd.read_sql("SELECT * FROM books WHERE org_id = ? AND quantity > 0", conn, params=(org_id,))
        book_options = ["-- Select --"] + books['title'].tolist() if not books.empty else ["-- Select --"]
        selected_book = st.selectbox("Select Book", book_options)
    
    with col2:
        classes = pd.read_sql("SELECT * FROM class_lists WHERE org_id = ?", conn, params=(org_id,))
        class_options = ["-- Select --"] + classes['class_name'].tolist() if not classes.empty else ["-- Select --"]
        selected_class = st.selectbox("Select Class", class_options)
    
    col3, col4 = st.columns(2)
    with col3:
        borrow_date = st.date_input("Issue Date", datetime.now())
    with col4:
        return_date = st.date_input("Return Date", datetime.now() + timedelta(days=14))
    
    if st.button("📋 Load Class", use_container_width=True):
        if selected_class != "-- Select --" and selected_book != "-- Select --":
            st.session_state.loaded_class = selected_class
            st.session_state.loaded_book = selected_book
            st.rerun()
    
    # Display class students for assignment
    if 'loaded_class' in st.session_state and 'loaded_book' in st.session_state:
        class_data = pd.read_sql("SELECT * FROM class_lists WHERE org_id = ? AND class_name = ?", 
                                 conn, params=(org_id, st.session_state.loaded_class))
        if not class_data.empty:
            students = json.loads(class_data.iloc[0]['data'])
            st.subheader(f"Assign '{st.session_state.loaded_book}' to {st.session_state.loaded_class}")
            
            # Create a dataframe for assignment
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
                    "Status": "✓ Issued" if is_assigned else "Pending"
                })
            
            df = pd.DataFrame(df_data)
            
            # Filter tabs
            filter_tab = st.radio("Filter", ["All", "Pending", "Assigned"], horizontal=True)
            if filter_tab == "Pending":
                df = df[df['Status'] == "Pending"]
            elif filter_tab == "Assigned":
                df = df[df['Status'] == "✓ Issued"]
            
            edited_df = st.data_editor(
                df,
                column_config={
                    "Assign": st.column_config.CheckboxColumn("Select"),
                    "Book Number": st.column_config.TextColumn("Book Number", disabled=df['Status'] == "✓ Issued"),
                },
                hide_index=True,
                use_container_width=True,
                disabled=["Student", "ADM", "Status"]
            )
            
            if st.button("✅ Issue Books", type="primary", use_container_width=True):
                to_assign = edited_df[edited_df['Assign'] == True]
                if to_assign.empty:
                    st.error("No students selected")
                else:
                    book = books[books['title'] == st.session_state.loaded_book].iloc[0]
                    if len(to_assign) > book['quantity']:
                        st.error(f"Only {book['quantity']} books available!")
                    else:
                        c = conn.cursor()
                        for _, row in to_assign.iterrows():
                            if row['Book Number']:
                                bid = generate_id()
                                c.execute("""INSERT INTO borrowed_books 
                                    (id, org_id, student_name, adm_number, book_title, book_number, borrow_date, return_date, lending_type)
                                    VALUES (?,?,?,?,?,?,?,?,?)""",
                                    (bid, org_id, row['Student'], row['ADM'], st.session_state.loaded_book,
                                     row['Book Number'], str(borrow_date), str(return_date), 'class'))
                                # Update book quantity
                                c.execute("UPDATE books SET quantity = quantity - 1 WHERE org_id = ? AND title = ?",
                                         (org_id, st.session_state.loaded_book))
                        
                        conn.commit()
                        add_audit_log(org_id, 'Books Issued', f"Issued {len(to_assign)} copies of '{st.session_state.loaded_book}' to {st.session_state.loaded_class}")
                        st.success(f"Issued {len(to_assign)} books!")
                        del st.session_state.loaded_class
                        del st.session_state.loaded_book
                        st.rerun()
    
    conn.close()

# ==================== INDIVIDUAL LENDING ====================
def individual_lending_page():
    """Individual book lending by librarian"""
    st.header("👤 Individual Book Lending")
    
    org_id = st.session_state.org_id
    conn = get_db_connection()
    
    with st.form("individual_lend_form"):
        st.subheader("Lend Book to Student")
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Student Name")
            adm = st.text_input("ADM Number")
            form = st.text_input("Form/Class")
            book_title = st.selectbox("Book", ["-- Select --"] + pd.read_sql(
                "SELECT title FROM books WHERE org_id = ? AND quantity > 0", conn, params=(org_id,))['title'].tolist())
        with col2:
            stream = st.text_input("Stream")
            book_no = st.text_input("Book Number")
            borrow_date = st.date_input("Borrow Date", datetime.now())
            return_date = st.date_input("Return Date", datetime.now() + timedelta(days=14))
        
        if st.form_submit_button("📖 Lend Book", use_container_width=True):
            if not all([name, adm, book_title != "-- Select --", book_no]):
                st.error("Please fill all required fields")
            else:
                book = pd.read_sql("SELECT * FROM books WHERE org_id = ? AND title = ?", conn, params=(org_id, book_title))
                if book.empty or book.iloc[0]['quantity'] <= 0:
                    st.error("Book out of stock")
                else:
                    c = conn.cursor()
                    c.execute("""INSERT INTO borrowed_books 
                        (id, org_id, student_name, adm_number, form, stream, book_title, book_number, borrow_date, return_date, lending_type)
                        VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
                        (generate_id(), org_id, name, adm, form, stream, book_title, book_no, str(borrow_date), str(return_date), 'individual'))
                    c.execute("UPDATE books SET quantity = quantity - 1 WHERE org_id = ? AND title = ?", (org_id, book_title))
                    conn.commit()
                    add_audit_log(org_id, 'Individual Lend', f"{name} borrowed '{book_title}'")
                    st.success(f"Book lent to {name}!")
    
    # Recent lendings
    st.subheader("Recent Lendings")
    lendings = pd.read_sql("""SELECT * FROM borrowed_books WHERE org_id = ? 
        AND lending_type = 'individual' AND returned = 0 ORDER BY created_at DESC LIMIT 20""", conn, params=(org_id,))
    
    if not lendings.empty:
        for _, l in lendings.iterrows():
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"📖 **{l['student_name']}** ({l['adm_number']}) → *{l['book_title']}* (#{l['book_number']}) | Due: {l['return_date']}")
            with col2:
                if st.button("Return", key=f"return_{l['id']}"):
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
def furniture_allocation_page():
    """Furniture allocation management"""
    st.header("🪑 Furniture Allocation")
    
    org_id = st.session_state.org_id
    conn = get_db_connection()
    
    col1, col2 = st.columns(2)
    with col1:
        classes = pd.read_sql("SELECT * FROM class_lists WHERE org_id = ?", conn, params=(org_id,))
        class_options = ["-- Select --"] + classes['class_name'].tolist() if not classes.empty else ["-- Select --"]
        selected_class = st.selectbox("Select Class", class_options)
    with col2:
        alloc_date = st.date_input("Allocation Date", datetime.now())
    
    if st.button("📋 Load Class", use_container_width=True):
        if selected_class != "-- Select --":
            st.session_state.furniture_class = selected_class
            st.rerun()
    
    if 'furniture_class' in st.session_state:
        class_data = pd.read_sql("SELECT * FROM class_lists WHERE org_id = ? AND class_name = ?",
                                 conn, params=(org_id, st.session_state.furniture_class))
        if not class_data.empty:
            students = json.loads(class_data.iloc[0]['data'])
            st.subheader(f"Assign Furniture to {st.session_state.furniture_class}")
            
            df_data = []
            for student in students:
                existing = pd.read_sql(
                    "SELECT * FROM furniture WHERE org_id = ? AND adm_number = ? AND returned = 0",
                    conn, params=(org_id, student['adm']))
                is_assigned = not existing.empty
                df_data.append({
                    "Assign": not is_assigned,
                    "Student": student['name'],
                    "ADM": student['adm'],
                    "Chair": existing.iloc[0]['chair_number'] if is_assigned else "",
                    "Locker": existing.iloc[0]['locker_number'] if is_assigned else "",
                    "Status": "✓ Allocated" if is_assigned else "Pending"
                })
            
            df = pd.DataFrame(df_data)
            edited_df = st.data_editor(df, hide_index=True, use_container_width=True,
                disabled=["Student", "ADM", "Status"])
            
            if st.button("✅ Assign Furniture", type="primary", use_container_width=True):
                to_assign = edited_df[edited_df['Assign'] == True]
                if to_assign.empty:
                    st.error("No students selected")
                else:
                    c = conn.cursor()
                    for _, row in to_assign.iterrows():
                        if row['Chair'] or row['Locker']:
                            c.execute("""INSERT INTO furniture 
                                (id, org_id, student_name, adm_number, chair_number, locker_number, allocation_date)
                                VALUES (?,?,?,?,?,?,?)""",
                                (generate_id(), org_id, row['Student'], row['ADM'],
                                 row['Chair'] if row['Chair'] else None,
                                 row['Locker'] if row['Locker'] else None,
                                 str(alloc_date)))
                    conn.commit()
                    add_audit_log(org_id, 'Furniture Allocated', f"Allocated to {len(to_assign)} students")
                    st.success(f"Allocated to {len(to_assign)} students!")
                    del st.session_state.furniture_class
                    st.rerun()
    
    # Current allocations
    st.subheader("Current Allocations")
    furniture = pd.read_sql("SELECT * FROM furniture WHERE org_id = ? ORDER BY created_at DESC", conn, params=(org_id,))
    if not furniture.empty:
        for _, f in furniture.iterrows():
            col1, col2 = st.columns([4, 1])
            with col1:
                status = "✅ Active" if not f['returned'] else "↩️ Returned"
                st.markdown(f"🪑 **{f['student_name']}** ({f['adm_number']}) | Chair: {f['chair_number'] or '-'} | Locker: {f['locker_number'] or '-'} | {f['allocation_date']} | {status}")
            with col2:
                if not f['returned'] and st.button("Return", key=f"ret_furn_{f['id']}"):
                    c = conn.cursor()
                    c.execute("UPDATE furniture SET returned = 1, return_date = ? WHERE id = ?",
                             (str(datetime.now().date()), f['id']))
                    conn.commit()
                    add_audit_log(org_id, 'Furniture Returned', f"{f['student_name']}")
                    st.rerun()
    else:
        st.info("No furniture allocations")
    
    conn.close()

# ==================== RETURN ITEMS ====================
def return_items_page():
    """Return borrowed items"""
    st.header("↩️ Return Items")
    
    org_id = st.session_state.org_id
    conn = get_db_connection()
    
    search = st.text_input("🔍 Search by name, ADM, or item number", placeholder="Type to search...")
    
    if search:
        # Search books
        books = pd.read_sql("""SELECT * FROM borrowed_books WHERE org_id = ? AND returned = 0 
            AND (student_name LIKE ? OR adm_number LIKE ? OR book_number LIKE ?)""",
            conn, params=(org_id, f"%{search}%", f"%{search}%", f"%{search}%"))
        
        # Search furniture
        furniture = pd.read_sql("""SELECT * FROM furniture WHERE org_id = ? AND returned = 0 
            AND (student_name LIKE ? OR adm_number LIKE ? OR chair_number LIKE ? OR locker_number LIKE ?)""",
            conn, params=(org_id, f"%{search}%", f"%{search}%", f"%{search}%", f"%{search}%"))
        
        if not books.empty:
            st.subheader("📚 Books")
            for _, b in books.iterrows():
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.markdown(f"**{b['student_name']}** ({b['adm_number']}) → *{b['book_title']}* (#{b['book_number']}) | Due: {b['return_date']}")
                with col2:
                    if st.button("Return", key=f"search_ret_{b['id']}"):
                        c = conn.cursor()
                        c.execute("UPDATE borrowed_books SET returned = 1, actual_return_date = ? WHERE id = ?",
                                 (str(datetime.now().date()), b['id']))
                        c.execute("UPDATE books SET quantity = quantity + 1 WHERE org_id = ? AND title = ?",
                                 (org_id, b['book_title']))
                        conn.commit()
                        st.rerun()
        
        if not furniture.empty:
            st.subheader("🪑 Furniture")
            for _, f in furniture.iterrows():
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.markdown(f"**{f['student_name']}** ({f['adm_number']}) | Chair: {f['chair_number'] or '-'} | Locker: {f['locker_number'] or '-'}")
                with col2:
                    if st.button("Return", key=f"search_ret_furn_{f['id']}"):
                        c = conn.cursor()
                        c.execute("UPDATE furniture SET returned = 1, return_date = ? WHERE id = ?",
                                 (str(datetime.now().date()), f['id']))
                        conn.commit()
                        st.rerun()
        
        if books.empty and furniture.empty:
            st.info("No active items found")
    
    conn.close()

# ==================== BORROWED BOOKS LOG ====================
def borrowed_log_page():
    """View all borrowed books"""
    st.header("📋 Borrowed Books Log")
    
    org_id = st.session_state.org_id
    conn = get_db_connection()
    
    filter_option = st.radio("Filter", ["All", "Active", "Overdue"], horizontal=True)
    
    if filter_option == "Active":
        borrowed = pd.read_sql("SELECT * FROM borrowed_books WHERE org_id = ? AND returned = 0 ORDER BY created_at DESC",
                               conn, params=(org_id,))
    elif filter_option == "Overdue":
        today = str(datetime.now().date())
        borrowed = pd.read_sql("""SELECT * FROM borrowed_books WHERE org_id = ? AND returned = 0 
            AND return_date < ? ORDER BY return_date""", conn, params=(org_id, today))
    else:
        borrowed = pd.read_sql("SELECT * FROM borrowed_books WHERE org_id = ? ORDER BY created_at DESC", conn, params=(org_id,))
    
    if not borrowed.empty:
        display_df = borrowed[['student_name', 'adm_number', 'form', 'stream', 'book_title', 'book_number', 'borrow_date', 'return_date', 'returned']]
        display_df.columns = ['Student', 'ADM', 'Form', 'Stream', 'Book', 'Book No', 'Borrowed', 'Due', 'Returned']
        display_df['Returned'] = display_df['Returned'].apply(lambda x: '✅ Yes' if x else '❌ No')
        
        st.dataframe(display_df, use_container_width=True, hide_index=True)
        
        # Export button
        if st.button("📎 Export to Excel"):
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                display_df.to_excel(writer, index=False, sheet_name='Borrowed Books')
            st.download_button("Download Excel", output.getvalue(), f"borrowed_{datetime.now().date()}.xlsx")
    else:
        st.info("No borrowed books")
    
    conn.close()

# ==================== MEMBERS MANAGEMENT ====================
def members_page():
    """Manage members"""
    st.header("👥 Members")
    
    org_id = st.session_state.org_id
    conn = get_db_connection()
    
    if st.session_state.role == 'admin':
        with st.expander("➕ Add Member", expanded=False):
            with st.form("add_member_form"):
                col1, col2 = st.columns(2)
                with col1:
                    name = st.text_input("Full Name")
                with col2:
                    member_id = st.text_input("Member ID (optional)")
                if st.form_submit_button("➕ Add Member"):
                    if name:
                        c = conn.cursor()
                        mid = member_id or f"MEM-{generate_id()[:8].upper()}"
                        c.execute("INSERT INTO members (id, org_id, name, member_id) VALUES (?,?,?,?)",
                                 (generate_id(), org_id, name, mid))
                        conn.commit()
                        add_audit_log(org_id, 'Member Added', f"Added {name}")
                        st.success(f"Member {name} added!")
                        st.rerun()
    
    members = pd.read_sql("SELECT * FROM members WHERE org_id = ? ORDER BY name", conn, params=(org_id,))
    if not members.empty:
        for _, m in members.iterrows():
            col1, col2, col3 = st.columns([4, 1, 1])
            with col1:
                st.markdown(f"**{m['name']}** ({m['member_id']})")
            with col2:
                if st.button("✏️ Edit", key=f"edit_mem_{m['id']}"):
                    st.session_state.editing_member = m['id']
            with col3:
                if st.session_state.role == 'admin' and st.button("🗑️", key=f"del_mem_{m['id']}"):
                    c = conn.cursor()
                    c.execute("DELETE FROM members WHERE id = ?", (m['id'],))
                    conn.commit()
                    st.rerun()
            
            if st.session_state.get('editing_member') == m['id']:
                new_name = st.text_input("Edit name", value=m['name'], key=f"edit_name_{m['id']}")
                new_id = st.text_input("Edit ID", value=m['member_id'], key=f"edit_id_{m['id']}")
                if st.button("💾 Save", key=f"save_mem_{m['id']}"):
                    c = conn.cursor()
                    c.execute("UPDATE members SET name = ?, member_id = ? WHERE id = ?", (new_name, new_id, m['id']))
                    conn.commit()
                    del st.session_state.editing_member
                    st.rerun()
    else:
        st.info("No members registered")
    
    conn.close()

# ==================== TEACHERS MANAGEMENT ====================
def teachers_page():
    """Manage teachers"""
    st.header("👨‍🏫 Teachers")
    
    org_id = st.session_state.org_id
    conn = get_db_connection()
    
    if st.session_state.role == 'admin':
        with st.expander("➕ Add Teacher", expanded=False):
            with st.form("add_teacher_form"):
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    name = st.text_input("Full Name")
                with col2:
                    subjects = st.text_input("Subjects Teaching")
                with col3:
                    classes = st.text_input("Classes Teaching")
                with col4:
                    class_assigned = st.text_input("Class Assigned (Duty)")
                if st.form_submit_button("➕ Add Teacher"):
                    if name:
                        c = conn.cursor()
                        c.execute("INSERT INTO teachers (id, org_id, name, subjects, classes, class_assigned) VALUES (?,?,?,?,?,?)",
                                 (generate_id(), org_id, name, subjects, classes, class_assigned))
                        conn.commit()
                        add_audit_log(org_id, 'Teacher Added', f"Added {name}")
                        st.success(f"Teacher {name} added!")
                        st.rerun()
    
    teachers = pd.read_sql("SELECT * FROM teachers WHERE org_id = ? ORDER BY name", conn, params=(org_id,))
    if not teachers.empty:
        st.dataframe(
            teachers[['name', 'subjects', 'classes', 'class_assigned']].rename(
                columns={'name': 'Name', 'subjects': 'Subjects', 'classes': 'Classes', 'class_assigned': 'Class Assigned'}
            ),
            use_container_width=True,
            hide_index=True
        )
        
        if st.session_state.role == 'admin':
            selected = st.selectbox("Select teacher to remove", teachers['name'].tolist())
            if st.button("🗑️ Remove Teacher", type="secondary"):
                c = conn.cursor()
                c.execute("DELETE FROM teachers WHERE org_id = ? AND name = ?", (org_id, selected))
                conn.commit()
                add_audit_log(org_id, 'Teacher Removed', f"Removed {selected}")
                st.rerun()
    else:
        st.info("No teachers registered")
    
    conn.close()

# ==================== CLASS LIST MANAGER ====================
def class_list_page():
    """Manage class lists with Excel import"""
    st.header("📋 Class List Manager")
    
    org_id = st.session_state.org_id
    conn = get_db_connection()
    
    # Import from Excel
    with st.expander("📥 Import from Excel", expanded=False):
        uploaded_file = st.file_uploader("Choose Excel file (must have Name and ADM columns)", type=['xlsx', 'xls'])
        if uploaded_file:
            try:
                df = pd.read_excel(uploaded_file)
                # Try to find name and adm columns
                name_col = next((c for c in df.columns if 'name' in c.lower()), df.columns[0])
                adm_col = next((c for c in df.columns if 'adm' in c.lower() or 'admission' in c.lower()), df.columns[1] if len(df.columns) > 1 else df.columns[0])
                
                students = []
                for _, row in df.iterrows():
                    students.append({
                        "name": str(row[name_col]),
                        "adm": str(row[adm_col])
                    })
                
                st.session_state.imported_students = students
                st.success(f"Imported {len(students)} students!")
                
                # Preview
                preview_df = pd.DataFrame(students)
                st.dataframe(preview_df, use_container_width=True)
                
                class_name = st.text_input("Save as class name", placeholder="e.g., Form 1 East 2025")
                if st.button("💾 Save Class List") and class_name:
                    c = conn.cursor()
                    # Check if class exists
                    existing = pd.read_sql("SELECT * FROM class_lists WHERE org_id = ? AND class_name = ?", 
                                          conn, params=(org_id, class_name))
                    if not existing.empty:
                        c.execute("UPDATE class_lists SET data = ? WHERE org_id = ? AND class_name = ?",
                                 (json.dumps(students), org_id, class_name))
                    else:
                        c.execute("INSERT INTO class_lists (id, org_id, class_name, data) VALUES (?,?,?,?)",
                                 (generate_id(), org_id, class_name, json.dumps(students)))
                    conn.commit()
                    add_audit_log(org_id, 'Class List Saved', f"Saved '{class_name}' with {len(students)} students")
                    st.success(f"Class '{class_name}' saved!")
                    del st.session_state.imported_students
                    st.rerun()
            except Exception as e:
                st.error(f"Error reading file: {e}")
    
    # View saved class lists
    st.subheader("Saved Class Lists")
    classes = pd.read_sql("SELECT * FROM class_lists WHERE org_id = ?", conn, params=(org_id,))
    if not classes.empty:
        for _, cls in classes.iterrows():
            students = json.loads(cls['data'])
            with st.expander(f"📋 {cls['class_name']} ({len(students)} students)"):
                st.dataframe(pd.DataFrame(students), use_container_width=True)
                if st.button(f"🗑️ Delete {cls['class_name']}", key=f"del_class_{cls['id']}"):
                    c = conn.cursor()
                    c.execute("DELETE FROM class_lists WHERE id = ?", (cls['id'],))
                    conn.commit()
                    st.rerun()
    else:
        st.info("No saved class lists")
    
    conn.close()

# ==================== QR CODE GENERATOR ====================
def qr_code_page():
    """Generate and display QR codes"""
    st.header("📱 QR Code Management")
    
    tab1, tab2 = st.tabs(["🏷️ Generate QR Codes", "📷 Scan QR Code"])
    
    with tab1:
        col1, col2, col3 = st.columns(3)
        with col1:
            qr_type = st.selectbox("Type", ["book", "chair", "locker"])
        with col2:
            start_num = st.number_input("Start Number", min_value=1, value=1)
        with col3:
            end_num = st.number_input("End Number", min_value=start_num, max_value=start_num + 100, value=min(start_num + 9, start_num + 99))
        
        if st.button("🏷️ Generate QR Codes", type="primary"):
            if end_num - start_num > 100:
                st.error("Maximum 100 QR codes at a time")
            else:
                cols = st.columns(5)
                for i in range(start_num, end_num + 1):
                    data = f"{qr_type}-{i}"
                    qr_img = generate_qr_code(data)
                    with cols[(i - start_num) % 5]:
                        st.markdown(f"""
                        <div style="text-align:center; padding:10px; background:white; border-radius:8px; margin:5px;">
                            <img src="data:image/png;base64,{qr_img}" width="100">
                            <p style="color:black; font-weight:bold; margin:5px 0;">{qr_type.upper()}: {i}</p>
                        </div>
                        """, unsafe_allow_html=True)
    
    with tab2:
        st.info("📷 To scan QR codes, use a mobile device camera or external QR scanner. The scanned code will identify items for return or allocation.")
        scanned_result = st.text_input("Enter scanned QR code manually", placeholder="e.g., book-5")
        if scanned_result and st.button("Process Scanned Code"):
            parts = scanned_result.split('-')
            if len(parts) == 2:
                st.success(f"Scanned: {parts[0].upper()} #{parts[1]}")
                # Auto-search for return
                org_id = st.session_state.org_id
                conn = get_db_connection()
                if parts[0] == 'book':
                    result = pd.read_sql("SELECT * FROM borrowed_books WHERE org_id = ? AND book_number = ? AND returned = 0",
                                        conn, params=(org_id, parts[1]))
                    if not result.empty:
                        st.info(f"Found: {result.iloc[0]['student_name']} - {result.iloc[0]['book_title']}")
                elif parts[0] in ['chair', 'locker']:
                    col = 'chair_number' if parts[0] == 'chair' else 'locker_number'
                    result = pd.read_sql(f"SELECT * FROM furniture WHERE org_id = ? AND {col} = ? AND returned = 0",
                                        conn, params=(org_id, parts[1]))
                    if not result.empty:
                        st.info(f"Found: {result.iloc[0]['student_name']}")
                conn.close()

# ==================== STAFF CHAT ====================
def chat_page():
    """Staff chat system"""
    st.header("💬 Staff Chat")
    
    org_id = st.session_state.org_id
    conn = get_db_connection()
    current_user = st.session_state.user['name']
    
    # Get other users for chat
    users = pd.read_sql("SELECT * FROM users WHERE org_id = ? AND name != ?", conn, params=(org_id, current_user))
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.subheader("Staff")
        if not users.empty:
            for _, u in users.iterrows():
                unread = pd.read_sql(
                    "SELECT COUNT(*) as count FROM chat_messages WHERE org_id = ? AND from_user = ? AND to_user = ? AND read = 0",
                    conn, params=(org_id, u['name'], current_user)).iloc[0]['count']
                
                badge = f" 🔴{unread}" if unread > 0 else ""
                if st.button(f"👤 {u['name']}{badge}", key=f"chat_user_{u['id']}", use_container_width=True):
                    st.session_state.chat_active_user = u['name']
                    # Mark messages as read
                    c = conn.cursor()
                    c.execute("UPDATE chat_messages SET read = 1 WHERE org_id = ? AND from_user = ? AND to_user = ?",
                             (org_id, u['name'], current_user))
                    conn.commit()
                    st.rerun()
        else:
            st.info("No other staff")
    
    with col2:
        if st.session_state.chat_active_user:
            st.subheader(f"💬 Chat with {st.session_state.chat_active_user}")
            
            # Display messages
            messages = pd.read_sql("""
                SELECT * FROM chat_messages 
                WHERE org_id = ? AND ((from_user = ? AND to_user = ?) OR (from_user = ? AND to_user = ?))
                ORDER BY created_at""",
                conn, params=(org_id, current_user, st.session_state.chat_active_user, 
                            st.session_state.chat_active_user, current_user))
            
            chat_container = st.container(height=400)
            with chat_container:
                if not messages.empty:
                    for _, msg in messages.iterrows():
                        is_sent = msg['from_user'] == current_user
                        align = "right" if is_sent else "left"
                        bg = "rgba(233, 69, 96, 0.3)" if is_sent else "rgba(255,255,255,0.1)"
                        st.markdown(f"""
                        <div style="text-align:{align}; margin: 5px 0;">
                            <div style="display:inline-block; background:{bg}; padding:10px 15px; border-radius:15px; max-width:70%;">
                                <p style="margin:0; color:white;">{msg['message']}</p>
                                <small style="color:rgba(255,255,255,0.5);">{msg['created_at'][:16]}</small>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info("No messages yet. Start the conversation!")
            
            # Send message
            with st.form("send_message_form", clear_on_submit=True):
                msg_input = st.text_input("Type a message...", key="chat_input")
                if st.form_submit_button("📤 Send"):
                    if msg_input:
                        c = conn.cursor()
                        c.execute("INSERT INTO chat_messages (id, org_id, from_user, to_user, message) VALUES (?,?,?,?,?)",
                                 (generate_id(), org_id, current_user, st.session_state.chat_active_user, msg_input))
                        conn.commit()
                        st.rerun()
        else:
            st.info("Select a staff member to start chatting")
    
    conn.close()

# ==================== SYSTEM OVERVIEW ====================
def system_overview_page():
    """Complete system overview for admins"""
    st.header("🔍 System Overview")
    
    org_id = st.session_state.org_id
    conn = get_db_connection()
    
    # Get all stats
    org = pd.read_sql("SELECT * FROM organizations WHERE id = ?", conn, params=(org_id,)).iloc[0]
    books = pd.read_sql("SELECT * FROM books WHERE org_id = ?", conn, params=(org_id,))
    borrowed = pd.read_sql("SELECT * FROM borrowed_books WHERE org_id = ? AND returned = 0", conn, params=(org_id,))
    furniture = pd.read_sql("SELECT * FROM furniture WHERE org_id = ? AND returned = 0", conn, params=(org_id,))
    members = pd.read_sql("SELECT * FROM members WHERE org_id = ?", conn, params=(org_id,))
    teachers = pd.read_sql("SELECT * FROM teachers WHERE org_id = ?", conn, params=(org_id,))
    users = pd.read_sql("SELECT * FROM users WHERE org_id = ?", conn, params=(org_id,))
    chats = pd.read_sql("SELECT * FROM chat_messages WHERE org_id = ?", conn, params=(org_id,))
    classes = pd.read_sql("SELECT * FROM class_lists WHERE org_id = ?", conn, params=(org_id,))
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🏫 School Information")
        st.markdown(f"""
        - **Name:** {org['name']}
        - **Address:** {org['address'] or 'Not set'}
        - **Admin:** {org['admin_name']}
        - **Email:** {org['admin_email']}
        - **Phone:** {org['admin_phone'] or 'Not set'}
        - **Invite Code:** `{org['invite_code']}`
        - **Created:** {org['created_at'][:10]}
        """)
        
        st.subheader("📚 Book Statistics")
        total_books = books['quantity'].sum() if not books.empty else 0
        st.markdown(f"""
        - **Total Books:** {total_books}
        - **Active Loans:** {len(borrowed)}
        - **Available:** {total_books - len(borrowed)}
        - **Catalog Items:** {len(books)}
        """)
    
    with col2:
        st.subheader("👥 People")
        st.markdown(f"""
        - **Staff Users:** {len(users)}
        - **Teachers:** {len(teachers)}
        - **Members:** {len(members)}
        - **Class Lists:** {len(classes)}
        """)
        
        st.subheader("💬 Communication")
        st.markdown(f"""
        - **Total Messages:** {len(chats)}
        - **Active Conversations:** {chats['from_user'].nunique() if not chats.empty else 0}
        """)
    
    st.subheader("🪑 Furniture")
    if not furniture.empty:
        st.markdown(f"""
        - **Active Allocations:** {len(furniture)}
        - **Chairs Assigned:** {len(furniture[furniture['chair_number'].notna()])}
        - **Lockers Assigned:** {len(furniture[furniture['locker_number'].notna()])}
        """)
    
    # Charts
    if not books.empty:
        st.subheader("📊 Book Distribution")
        fig = px.pie(books, values='quantity', names='type', title='Books by Type')
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    conn.close()

# ==================== AUDIT LOG ====================
def audit_log_page():
    """View audit log"""
    st.header("📝 Audit Log")
    
    org_id = st.session_state.org_id
    conn = get_db_connection()
    
    search = st.text_input("🔍 Search log", placeholder="Filter by action or user...")
    
    if search:
        logs = pd.read_sql("SELECT * FROM audit_log WHERE org_id = ? AND (action LIKE ? OR user_name LIKE ? OR details LIKE ?) ORDER BY created_at DESC LIMIT 100",
                          conn, params=(org_id, f"%{search}%", f"%{search}%", f"%{search}%"))
    else:
        logs = pd.read_sql("SELECT * FROM audit_log WHERE org_id = ? ORDER BY created_at DESC LIMIT 100", conn, params=(org_id,))
    
    if not logs.empty:
        st.dataframe(
            logs[['created_at', 'user_name', 'action', 'details']].rename(
                columns={'created_at': 'Timestamp', 'user_name': 'User', 'action': 'Action', 'details': 'Details'}
            ),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No audit log entries")
    
    conn.close()

# ==================== REPORTS ====================
def reports_page():
    """Generate and export reports"""
    st.header("📈 Reports & Analytics")
    
    org_id = st.session_state.org_id
    conn = get_db_connection()
    
    report_type = st.selectbox("Report Type", ["Book Summary", "Furniture Summary", "Overdue Items", "Complete Report"])
    
    if st.button("📊 Generate Report", type="primary"):
        if report_type == "Book Summary":
            data = pd.read_sql("SELECT * FROM borrowed_books WHERE org_id = ?", conn, params=(org_id,))
            if not data.empty:
                st.dataframe(data, use_container_width=True)
                output = BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    data.to_excel(writer, index=False, sheet_name='Books')
                st.download_button("📎 Download Excel", output.getvalue(), f"book_report_{datetime.now().date()}.xlsx")
        
        elif report_type == "Furniture Summary":
            data = pd.read_sql("SELECT * FROM furniture WHERE org_id = ?", conn, params=(org_id,))
            if not data.empty:
                st.dataframe(data, use_container_width=True)
                output = BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    data.to_excel(writer, index=False, sheet_name='Furniture')
                st.download_button("📎 Download Excel", output.getvalue(), f"furniture_report_{datetime.now().date()}.xlsx")
        
        elif report_type == "Overdue Items":
            today = str(datetime.now().date())
            data = pd.read_sql("SELECT * FROM borrowed_books WHERE org_id = ? AND returned = 0 AND return_date < ?",
                              conn, params=(org_id, today))
            if not data.empty:
                st.dataframe(data, use_container_width=True)
                st.metric("Overdue Items", len(data))
            else:
                st.success("No overdue items!")
        
        else:  # Complete Report
            books = pd.read_sql("SELECT * FROM books WHERE org_id = ?", conn, params=(org_id,))
            borrowed = pd.read_sql("SELECT * FROM borrowed_books WHERE org_id = ? AND returned = 0", conn, params=(org_id,))
            furniture = pd.read_sql("SELECT * FROM furniture WHERE org_id = ? AND returned = 0", conn, params=(org_id,))
            teachers = pd.read_sql("SELECT * FROM teachers WHERE org_id = ?", conn, params=(org_id,))
            members = pd.read_sql("SELECT * FROM members WHERE org_id = ?", conn, params=(org_id,))
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Books", books['quantity'].sum() if not books.empty else 0)
                st.metric("Active Loans", len(borrowed))
                st.metric("Furniture Items", len(furniture))
            with col2:
                st.metric("Teachers", len(teachers))
                st.metric("Members", len(members))
                st.metric("Overdue", len(borrowed[borrowed['return_date'] < str(datetime.now().date())]) if not borrowed.empty else 0)
    
    conn.close()

# ==================== WALLPAPER/THEME ====================
def wallpaper_page():
    """Choose wallpaper theme"""
    st.header("🖼️ Theme & Wallpaper")
    
    st.caption("Click a wallpaper to apply it as background")
    
    cols = st.columns(5)
    for i, wp in enumerate(WALLPAPERS):
        with cols[i % 5]:
            st.image(wp['url'], caption=wp['name'], use_container_width=True)
            if st.button(f"Apply", key=f"wp_{i}"):
                st.session_state.wallpaper = wp['url']
                st.success(f"Applied {wp['name']}!")
                st.rerun()
    
    # Custom upload
    st.subheader("Upload Custom")
    uploaded = st.file_uploader("Choose an image", type=['png', 'jpg', 'jpeg'])
    if uploaded:
        st.session_state.wallpaper = base64.b64encode(uploaded.read()).decode()
        st.success("Custom wallpaper applied!")
        st.rerun()
    
    if st.button("🔄 Reset Default"):
        st.session_state.wallpaper = None
        st.rerun()

# ==================== SETTINGS ====================
def settings_page():
    """Settings and staff management"""
    st.header("⚙️ Settings")
    
    org_id = st.session_state.org_id
    conn = get_db_connection()
    
    tab1, tab2, tab3 = st.tabs(["👥 Staff Management", "💾 Data Management", "📧 Email Settings"])
    
    with tab1:
        st.subheader("Staff Members")
        if st.session_state.role == 'admin':
            with st.expander("➕ Create Staff Account", expanded=False):
                with st.form("create_staff_form"):
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        email = st.text_input("Email")
                        name = st.text_input("Full Name")
                    with col2:
                        role = st.selectbox("Role", ["teacher", "librarian", "admin"])
                    with col3:
                        password = st.text_input("Password (auto if empty)", type="password")
                    if st.form_submit_button("➕ Create"):
                        if email and name:
                            c = conn.cursor()
                            pw = hash_password(password) if password else hash_password(generate_id()[:8])
                            staff_id = f"{role.upper()}-{generate_id()[:8].upper()}"
                            c.execute("INSERT INTO users (id, org_id, name, email, role, password, invite_code, staff_id) VALUES (?,?,?,?,?,?,?,?)",
                                     (generate_id(), org_id, name, email, role, pw, st.session_state.invite_code, staff_id))
                            conn.commit()
                            add_audit_log(org_id, 'Staff Created', f"Created {role}: {name}")
                            st.success(f"Created! Staff ID: {staff_id}")
                            if not password:
                                st.info(f"Auto-generated password: {generate_id()[:8]}")
                            st.rerun()
        
        # List staff
        users = pd.read_sql("SELECT * FROM users WHERE org_id = ?", conn, params=(org_id,))
        if not users.empty:
            for _, u in users.iterrows():
                col1, col2 = st.columns([4, 1])
                with col1:
                    badge = f"🔴 {u['role'].upper()}" if u['role'] == 'admin' else f"🟢 {u['role'].upper()}" if u['role'] == 'teacher' else f"🔵 {u['role'].upper()}"
                    st.markdown(f"**{u['name']}** - {u['email']} | {badge} | ID: {u['staff_id'] or 'N/A'}")
                with col2:
                    if st.session_state.role == 'admin' and u['role'] != 'admin':
                        if st.button("🗑️", key=f"del_staff_{u['id']}"):
                            c = conn.cursor()
                            c.execute("DELETE FROM users WHERE id = ?", (u['id'],))
                            conn.commit()
                            st.rerun()
    
    with tab2:
        st.subheader("Data Management")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📥 Export Backup", use_container_width=True):
                # Export all data
                data = {
                    'books': pd.read_sql("SELECT * FROM books WHERE org_id = ?", conn, params=(org_id,)).to_dict(),
                    'members': pd.read_sql("SELECT * FROM members WHERE org_id = ?", conn, params=(org_id,)).to_dict(),
                    'teachers': pd.read_sql("SELECT * FROM teachers WHERE org_id = ?", conn, params=(org_id,)).to_dict(),
                    'borrowed': pd.read_sql("SELECT * FROM borrowed_books WHERE org_id = ?", conn, params=(org_id,)).to_dict(),
                    'furniture': pd.read_sql("SELECT * FROM furniture WHERE org_id = ?", conn, params=(org_id,)).to_dict(),
                    'classes': pd.read_sql("SELECT * FROM class_lists WHERE org_id = ?", conn, params=(org_id,)).to_dict(),
                }
                st.download_button("Download Backup", json.dumps(data, default=str), "srms_backup.json")
        
        with col2:
            if st.button("⚠️ Clear All Data", use_container_width=True, type="secondary"):
                if st.checkbox("I understand this cannot be undone"):
                    if st.button("Confirm Delete All Data", type="primary"):
                        tables = ['books', 'members', 'teachers', 'borrowed_books', 'furniture', 'class_lists', 'audit_log', 'chat_messages']
                        c = conn.cursor()
                        for table in tables:
                            c.execute(f"DELETE FROM {table} WHERE org_id = ?", (org_id,))
                        conn.commit()
                        st.error("All data cleared!")
                        st.rerun()
    
    with tab3:
        st.subheader("Email Settings")
        st.info("Configure EmailJS integration for notifications")
        st.text_input("EmailJS Public Key", type="password", key="email_public_key")
        st.text_input("EmailJS Service ID", key="email_service_id")
        st.text_input("EmailJS Template ID", key="email_template_id")
        st.text_input("Recipient Email", key="email_recipient")
        if st.button("💾 Save Email Settings"):
            st.success("Email settings saved!")

# ==================== MAIN APP ====================
def main():
    """Main application entry point"""
    st.set_page_config(
        page_title="SRMS - School Resource Management System",
        page_icon="📚",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Initialize database
    init_db()
    init_session_state()
    
    # Authentication check
    if not st.session_state.authenticated:
        auth_page()
        return
    
    # Apply custom styling
    apply_custom_css()
    
    # Sidebar navigation
    with st.sidebar:
        st.markdown('<div style="text-align:center; font-size:2em; font-weight:900; color:#d4af37;">SRMS</div>', unsafe_allow_html=True)
        st.markdown(f'<p style="text-align:center; color:white;">{st.session_state.org_name}</p>', unsafe_allow_html=True)
        st.markdown(f'<p style="text-align:center; color:rgba(255,255,255,0.7);">👤 {st.session_state.user["name"]} ({st.session_state.role.upper()})</p>', unsafe_allow_html=True)
        st.markdown("---")
        
        pages = {
            "📊 Dashboard": dashboard_page,
            "📚 Book Catalog": book_catalog_page,
            "📖 Book Issuing (Class)": book_issuing_page,
            "👤 Individual Lending": individual_lending_page,
            "🪑 Furniture Allocation": furniture_allocation_page,
            "↩️ Return Items": return_items_page,
            "📋 Borrowed Books": borrowed_log_page,
            "👥 Members": members_page,
            "👨‍🏫 Teachers": teachers_page,
            "📋 Class Lists": class_list_page,
            "📱 QR Codes": qr_code_page,
            "💬 Staff Chat": chat_page,
            "🔍 System Overview": system_overview_page,
            "📝 Audit Log": audit_log_page,
            "📈 Reports": reports_page,
            "🖼️ Theme": wallpaper_page,
            "⚙️ Settings": settings_page,
        }
        
        for page_name, page_func in pages.items():
            if st.sidebar.button(page_name, use_container_width=True):
                st.session_state.page = page_name
                st.rerun()
        
        st.sidebar.markdown("---")
        if st.sidebar.button("🚪 Logout", use_container_width=True, type="primary"):
            add_audit_log(st.session_state.org_id, 'Logout', st.session_state.user['name'])
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
        
        st.sidebar.markdown('<p class="credit-text" style="font-size:0.8em;">by <strong>WeGEM</strong> (Edwin)</p>', unsafe_allow_html=True)
    
    # Main content area
    pages = {
        "📊 Dashboard": dashboard_page,
        "📚 Book Catalog": book_catalog_page,
        "📖 Book Issuing (Class)": book_issuing_page,
        "👤 Individual Lending": individual_lending_page,
        "🪑 Furniture Allocation": furniture_allocation_page,
        "↩️ Return Items": return_items_page,
        "📋 Borrowed Books": borrowed_log_page,
        "👥 Members": members_page,
        "👨‍🏫 Teachers": teachers_page,
        "📋 Class Lists": class_list_page,
        "📱 QR Codes": qr_code_page,
        "💬 Staff Chat": chat_page,
        "🔍 System Overview": system_overview_page,
        "📝 Audit Log": audit_log_page,
        "📈 Reports": reports_page,
        "🖼️ Theme": wallpaper_page,
        "⚙️ Settings": settings_page,
    }
    
    current_page = st.session_state.get('page', '📊 Dashboard')
    if current_page in pages:
        pages[current_page]()

if __name__ == "__main__":
    main()
