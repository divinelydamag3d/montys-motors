import streamlit as st
import bcrypt
import sqlite3
import pandas as pd
import datetime

# Database Initialization
def create_connection():
    conn = sqlite3.connect('montys_motors.db')
    return conn

def create_tables():
    conn = create_connection()
    cursor = conn.cursor()
    tables = [
        "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT, role TEXT)",
        "CREATE TABLE IF NOT EXISTS customers (id INTEGER PRIMARY KEY, name TEXT, contact TEXT)",
        "CREATE TABLE IF NOT EXISTS inventory (id INTEGER PRIMARY KEY, item_name TEXT, quantity INTEGER)",
        "CREATE TABLE IF NOT EXISTS invoices (id INTEGER PRIMARY KEY, customer_id INTEGER, amount REAL)",
        "CREATE TABLE IF NOT EXISTS payroll (id INTEGER PRIMARY KEY, employee_name TEXT, salary REAL)",
        "CREATE TABLE IF NOT EXISTS appointments (id INTEGER PRIMARY KEY, customer_id INTEGER, date TEXT)",
        "CREATE TABLE IF NOT EXISTS metrics (id INTEGER PRIMARY KEY, total_sales REAL)",
        "CREATE TABLE IF NOT EXISTS chat_logs (id INTEGER PRIMARY KEY, message TEXT, timestamp TEXT)",
        "CREATE TABLE IF NOT EXISTS role_management (id INTEGER PRIMARY KEY, role_name TEXT)",
        "CREATE TABLE IF NOT EXISTS services (id INTEGER PRIMARY KEY, service_name TEXT, price REAL)",
        "CREATE TABLE IF NOT EXISTS payments (id INTEGER PRIMARY KEY, amount REAL, date TEXT)",
        "CREATE TABLE IF NOT EXISTS feedback (id INTEGER PRIMARY KEY, customer_id INTEGER, message TEXT)",
        "CREATE TABLE IF NOT EXISTS support_tickets (id INTEGER PRIMARY KEY, customer_id INTEGER, issue TEXT)",
        "CREATE TABLE IF NOT EXISTS admin_logs (id INTEGER PRIMARY KEY, action TEXT, timestamp TEXT)",
        "CREATE TABLE IF NOT EXISTS settings (id INTEGER PRIMARY KEY, setting_name TEXT, setting_value TEXT)"
    ]
    for table in tables:
        cursor.execute(table)
    conn.commit()
    conn.close()

create_tables()

# Role-based Authentication
def register_user(username, password, role):
    conn = create_connection()
    cursor = conn.cursor()
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, hashed, role))
    conn.commit()
    conn.close()

def login_user(username, password):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT password, role FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    if result and bcrypt.checkpw(password.encode('utf-8'), result[0]):
        return result[1]
    return None

# Streamlit UI
st.set_page_config(page_title='Monty’s Motors', layout='wide')

# Custom CSS
st.markdown('<style>footer {visibility: hidden;}</style>', unsafe_allow_html=True)

st.title('Welcome to Monty’s Motors')

menu = st.sidebar.selectbox('Select Action', ['Login', 'Admin Dashboard', 'Chat', 'Schedule Appointment'])

if menu == 'Login':
    st.subheader('Login')
    username = st.text_input('Username')
    password = st.text_input('Password', type='password')
    if st.button('Login'):
        role = login_user(username, password)
        if role:
            st.success(f'Logged in as {role}')
            # Load features based on role
        else:
            st.error('Invalid credentials')

# Other features for admin dashboard, chat and scheduling will go here

st.markdown('---')
st.markdown('**Contact us:**
123 Main St, Motor City\n555-555-5555')