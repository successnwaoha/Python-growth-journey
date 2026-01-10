import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
import hashlib
from datetime import datetime

# --- 1. SETTINGS & CONSTANTS ---
st.set_page_config(page_title="Personal Expense Pro", layout="wide")
DB_FILE = "expenses_v2.db" # Updated version for new schema
CATEGORY_BUDGETS = {
    "Food": 50000, "Transport": 30000, "Rent": 150000,
    "Utilities": 20000, "Entertainment": 25000, "Other": 15000
}

# --- 2. DATABASE & AUTH FUNCTIONS ---
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT)')
    # Added 'id' as an AUTOINCREMENT primary key for easy deletion
    c.execute('''CREATE TABLE IF NOT EXISTS expenses 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id TEXT, date TEXT, 
                  category TEXT, amount REAL, description TEXT)''')
    conn.commit()
    conn.close()

def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def login_user(username, password):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username =? AND password = ?', (username, make_hashes(password)))
    data = c.fetchall()
    conn.close()
    return data

def create_user(username, password):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    try:
        c.execute('INSERT INTO users(username, password) VALUES (?,?)', (username, make_hashes(password)))
        conn.commit()
    except sqlite3.IntegrityError:
        st.sidebar.error("Username already exists.")
    conn.close()

def save_single_expense(user_id, date, category, amount, description):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('INSERT INTO expenses (user_id, date, category, amount, description) VALUES (?,?,?,?,?)', 
              (user_id, str(date), category, amount, description))
    conn.commit()
    conn.close()

def delete_expense(expense_id):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('DELETE FROM expenses WHERE id = ?', (expense_id,))
    conn.commit()
    conn.close()

def save_df_to_db(df, user_id):
    conn = sqlite3.connect(DB_FILE)
    df['user_id'] = user_id
    if 'description' not in df.columns:
        df['description'] = "Bulk Upload"
    # Filter only relevant columns to match DB
    df[['user_id', 'date', 'category', 'amount', 'description']].to_sql("expenses", conn, if_exists="append", index=False)
    conn.close()

def load_from_db(user_id):
    conn = sqlite3.connect(DB_FILE)
    query = f"SELECT id, date, category, amount, description FROM expenses WHERE user_id = '{user_id}'"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

init_db()

# --- 3. AUTHENTICATION UI ---
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
    st.session_state["username"] = ""

if not st.session_state["logged_in"]:
    st.title("🔐 Secure Expense Tracker")
    auth_mode = st.sidebar.selectbox("Login/Signup", ["Login", "Signup"])
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")

    if auth_mode == "Signup":
        if st.sidebar.button("Create Account"):
            create_user(username, password)
            st.sidebar.success("Account created! Please Login.")
    elif auth_mode == "Login":
        if st.sidebar.button("Login"):
            if login_user(username, password):
                st.session_state["logged_in"] = True
                st.session_state["username"] = username
                st.rerun()
            else:
                st.sidebar.error("Invalid Username/Password")
    st.stop()

# --- 4. MAIN APP INTERFACE ---
st.sidebar.success(f"👤 {st.session_state['username']}")
if st.sidebar.button("Logout"):
    st.session_state["logged_in"] = False
    st.rerun()

st.title("💸 Expense Tracking Dashboard")
menu = ["📊 View Dashboard", "📝 Add Single Expense", "📤 Bulk Upload (CSV)", "⚙️ Manage Data"]
choice = st.sidebar.selectbox("Menu", menu)

# --- CHOICE: ADD SINGLE ---
if choice == "📝 Add Single Expense":
    st.header("📝 Log a Purchase")
    with st.form("expense_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            exp_date = st.date_input("Date", datetime.now())
            exp_category = st.selectbox("Category", list(CATEGORY_BUDGETS.keys()))
        with col2:
            exp_amount = st.number_input("Amount (₦)", min_value=0.0, step=100.0)
            exp_desc = st.text_input("Description (Optional)")
        if st.form_submit_button("Save Expense"):
            save_single_expense(st.session_state["username"], exp_date, exp_category, exp_amount, exp_desc)
            st.balloons()
            st.success("Expense saved to your profile!")

# --- CHOICE: BULK UPLOAD ---
elif choice == "📤 Bulk Upload (CSV)":
    st.header("📤 Bulk Upload")
    st.info("Upload a CSV with these headers: date, category, amount")
    uploaded_file = st.file_uploader("Choose CSV file", type=["csv"])
    if uploaded_file:
        temp_df = pd.read_csv(uploaded_file)
        st.write("Preview:")
        st.dataframe(temp_df.head())
        if st.button("💾 Confirm & Save to Database"):
            save_df_to_db(temp_df, st.session_state["username"])
            st.success(f"Successfully imported {len(temp_df)} records!")

# --- CHOICE: MANAGE DATA (DELETE) ---
elif choice == "⚙️ Manage Data":
    st.header("⚙️ Data Management")
    df = load_from_db(st.session_state["username"])
    if df.empty:
        st.info("No data to manage.")
    else:
        st.subheader("Delete Records")
        st.write("Select an entry to permanently remove it:")
        # Display simplified list for deletion selection
        df['display'] = df['date'] + " | " + df['category'] + " | ₦" + df['amount'].astype(str)
        delete_list = st.selectbox("Select entry to delete", options=df['id'].tolist(), 
                                   format_func=lambda x: df[df['id']==x]['display'].values[0])
        
        if st.button("🗑️ Delete Selected Entry", type="primary"):
            delete_expense(delete_list)
            st.warning("Entry deleted.")
            st.rerun()

# --- CHOICE: VIEW DASHBOARD ---
else:
    df = load_from_db(st.session_state["username"])
    if df.empty:
        st.info("Your dashboard is empty. Add expenses to see analysis!")
    else:
        # DATA CLEANING
        df["date"] = pd.to_datetime(df["date"], errors='coerce')
        df = df.dropna(subset=["date"])
        df["month"] = df["date"].dt.to_period("M").astype(str)

        # SIDEBAR FILTERS
        st.sidebar.header("Global Filters")
        categories = st.sidebar.multiselect("Categories", options=sorted(df["category"].unique()), default=df["category"].unique())
        
        # Apply filters
        filtered_df = df[df["category"].isin(categories)]
        
        if filtered_df.empty:
            st.warning("No data matches your filters.")
        else:
            selected_month = st.sidebar.selectbox("Detailed Month Analysis", options=sorted(filtered_df["month"].unique(), reverse=True))
            monthly_df = filtered_df[filtered_df["month"] == selected_month]

            # KPI CALCULATIONS
            total_spent = monthly_df['amount'].sum()
            budget_df = monthly_df.groupby("category")["amount"].sum().reset_index()
            budget_df["budget"] = budget_df["category"].map(CATEGORY_BUDGETS).fillna(0)
            budget_df["remaining"] = budget_df["budget"] - budget_df["amount"]

            # VISUALS
            st.subheader(f"📅 Monthly Report: {selected_month}")
            m1, m2, m3 = st.columns(3)
            m1.metric("Total Spent", f"₦{total_spent:,.2f}")
            m2.metric("Transactions", len(monthly_df))
            m3.metric("Avg / Transaction", f"₦{(total_spent/len(monthly_df)):,.2f}")

            # ALERTS
            overspent = budget_df[budget_df["remaining"] < 0]
            if not overspent.empty:
                with st.expander("🚨 Budget Alerts", expanded=True):
                    for _, row in overspent.iterrows():
                        st.error(f"**{row['category']}** is over budget by ₦{abs(row['remaining']):,.2f}")

            # CHARTS
            c1, c2 = st.columns(2)
            with c1:
                st.plotly_chart(px.pie(monthly_df, names="category", values="amount", title="Where your money went", hole=0.4), use_container_width=True)
            with c2:
                daily_trend = filtered_df.groupby("date")["amount"].sum().reset_index()
                st.plotly_chart(px.line(daily_trend, x="date", y="amount", title="Spending Timeline"), use_container_width=True)

            # BUDGET CHART
            st.divider()
            st.subheader("Budget vs Actual")
            st.plotly_chart(px.bar(budget_df, x="category", y=["amount", "budget"], barmode="group", color_discrete_sequence=['#EF553B', '#00CC96']), use_container_width=True)
            
            # RAW DATA & EXPORT
            with st.expander("📄 View All Records & Export"):
                st.dataframe(filtered_df.sort_values("date", ascending=False), use_container_width=True)
                csv = filtered_df.to_csv(index=False).encode('utf-8')
                st.download_button("📥 Download filtered data as CSV", data=csv, file_name=f"expenses_{st.session_state['username']}.csv", mime='text/csv')