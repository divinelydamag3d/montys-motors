import streamlit as st
import sqlite3
import bcrypt

# -------------------------
# PAGE SETUP
# -------------------------

st.set_page_config(
    page_title="Monty's Motors Shop AI",
    layout="wide"
)

st.markdown("""
<style>
.footer {text-align:center;font-size:12px;}
</style>
<div class='footer'>Monty's Motors © 2026</div>
""", unsafe_allow_html=True)

# -------------------------
# DATABASE
# -------------------------

DB_NAME = "montys_motors.db"

conn = sqlite3.connect(DB_NAME, check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS Users (
id INTEGER PRIMARY KEY,
username TEXT UNIQUE,
password BLOB,
role TEXT,
must_change_password INTEGER
)
""")

conn.commit()

# -------------------------
# CREATE DEFAULT USERS
# -------------------------

def create_user(username,password,role,force_change):

    cursor.execute("SELECT * FROM Users WHERE username=?", (username,))
    user = cursor.fetchone()

    if not user:

        hashed = bcrypt.hashpw(password.encode(),bcrypt.gensalt())

        cursor.execute(
        "INSERT INTO Users (username,password,role,must_change_password) VALUES (?,?,?,?)",
        (username,hashed,role,force_change)
        )

        conn.commit()

create_user("greg","montys1956","admin",1)
create_user("tech1","tech123","tech",0)

# -------------------------
# SESSION STATE
# -------------------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.role = None
    st.session_state.must_change = 0

# -------------------------
# LOGIN
# -------------------------

if not st.session_state.logged_in:

    st.sidebar.header("Login")

    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")

    if st.sidebar.button("Login"):

        cursor.execute("SELECT * FROM Users WHERE username=?", (username,))
        user = cursor.fetchone()

        if user:

            if bcrypt.checkpw(password.encode(), user[2]):

                st.session_state.logged_in = True
                st.session_state.user = user[1]
                st.session_state.role = user[3]
                st.session_state.must_change = user[4]

                st.rerun()

            else:
                st.error("Incorrect password")

        else:
            st.error("User not found")

# -------------------------
# FORCE PASSWORD CHANGE
# -------------------------

elif st.session_state.must_change == 1:

    st.title("Change Your Password")

    new_pw = st.text_input("New Password", type="password")

    if st.button("Update Password"):

        hashed = bcrypt.hashpw(new_pw.encode(), bcrypt.gensalt())

        cursor.execute(
        "UPDATE Users SET password=?, must_change_password=0 WHERE username=?",
        (hashed, st.session_state.user)
        )

        conn.commit()

        st.success("Password updated successfully")

        st.session_state.must_change = 0
        st.rerun()

# -------------------------
# MAIN SYSTEM
# -------------------------

elif st.session_state.logged_in:

    st.sidebar.success(f"Logged in as {st.session_state.user}")

    if st.sidebar.button("Logout"):

        st.session_state.logged_in = False
        st.session_state.user = None
        st.session_state.role = None
        st.session_state.must_change = 0

        st.rerun()

# =========================
# ADMIN ACCESS
# =========================

    if st.session_state.role == "admin":

        menu = st.sidebar.selectbox(
            "Admin Menu",
            [
                "Dashboard",
                "Technicians",
                "Inventory",
                "Reports",
                "AI Diagnostics"
            ]
        )

        if menu == "Dashboard":

            st.title("Admin Dashboard")
            st.write("Shop analytics, revenue, and system overview.")

        if menu == "Technicians":

            st.title("Technician Management")

            st.subheader("Create Technician")

            new_user = st.text_input("Technician Username")
            new_pass = st.text_input("Temporary Password", type="password")

            if st.button("Create Technician"):

                if new_user and new_pass:

                    hashed = bcrypt.hashpw(new_pass.encode(),bcrypt.gensalt())

                    try:

                        cursor.execute(
                        "INSERT INTO Users (username,password,role,must_change_password) VALUES (?,?,?,?)",
                        (new_user,hashed,"tech",1)
                        )

                        conn.commit()

                        st.success(f"{new_user} created. Must change password on login.")

                    except:
                        st.error("Username already exists")

            st.divider()

            st.subheader("Current Users")

            cursor.execute("SELECT username, role FROM Users")
            users = cursor.fetchall()

            for u in users:
                st.write(f"👤 {u[0]} — {u[1]}")

        if menu == "Inventory":

            st.title("Inventory Management")
            st.write("Parts tracking and stock alerts will go here.")

        if menu == "Reports":

            st.title("Shop Reports")
            st.write("Revenue reports and technician performance.")

        if menu == "AI Diagnostics":

            st.title("Shop AI Diagnostics")

            problem = st.text_input("Describe vehicle issue")

            if problem:
                st.write("Possible causes:")
                st.write("- Ignition coil failure")
                st.write("- Vacuum leak")
                st.write("- Fuel delivery issue")
                st.write("- Dirty throttle body")

# =========================
# TECHNICIAN ACCESS
# =========================

    elif st.session_state.role == "tech":

        menu = st.sidebar.selectbox(
            "Technician Menu",
            [
                "My Jobs",
                "Vehicle Diagnostics",
                "Repair Notes",
                "AI Mechanic"
            ]
        )

        if menu == "My Jobs":

            st.title("Assigned Repair Jobs")
            st.write("Technician job list will appear here.")

        if menu == "Vehicle Diagnostics":

            st.title("Vehicle Diagnostics")
            st.write("Scan VIN, log problems, check history.")

        if menu == "Repair Notes":

            st.title("Repair Notes")

            notes = st.text_area("Write repair notes")

            if st.button("Save Notes"):
                st.success("Notes saved.")

        if menu == "AI Mechanic":

            st.title("AI Mechanic Assistant")

            symptoms = st.text_input("Describe symptoms")

            if symptoms:
                st.write("Possible issues:")
                st.write("- Faulty spark plugs")
                st.write("- Fuel injector problem")
                st.write("- Mass airflow sensor failure")
                st.write("- Bad oxygen sensor")
