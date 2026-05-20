import streamlit as st
import pandas as pd
from datetime import date, datetime
import os

st.set_page_config(page_title="My Grocery Tracker", page_icon="🛒", layout="wide")

DATA_FILE = "grocery_list.csv"

def load_data():
    try:
        if os.path.exists(DATA_FILE):
            df = pd.read_csv(DATA_FILE)
            df["Added"] = pd.to_datetime(df["Added"], errors='coerce').dt.date
            if "Bought" not in df.columns:
                df["Bought"] = False
            if "Category" not in df.columns:
                df["Category"] = "Other"
            return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
    
    # Fallback to empty DataFrame
    return pd.DataFrame(columns=["Item", "Quantity", "Category", "Added", "Bought"])

def save_data(df):
    try:
        df.to_csv(DATA_FILE, index=False)
    except Exception as e:
        st.error(f"Error saving data: {e}")

# ====================== INITIALIZE SESSION STATE ======================
if "items" not in st.session_state:
    st.session_state.items = load_data()

# Make sure it's always a DataFrame
if not isinstance(st.session_state.items, pd.DataFrame):
    st.session_state.items = pd.DataFrame(columns=["Item", "Quantity", "Category", "Added", "Bought"])

# ====================== SIDEBAR ======================
st.sidebar.header("🛒 Grocery Tracker")
if st.sidebar.button("🗑️ Clear Entire List"):
    st.session_state.items = pd.DataFrame(columns=["Item", "Quantity", "Category", "Added", "Bought"])
    save_data(st.session_state.items)
    st.success("List cleared!")
    st.rerun()

st.sidebar.info("✅ Data saved automatically")

# ====================== MAIN APP ======================
st.title("🛒 My Grocery Tracker")

# Add new item
col1, col2, col3 = st.columns([3, 1, 1])
with col1:
    item = st.text_input("What do you need?", placeholder="Milk, Bread...")
with col2:
    qty = st.number_input("Qty", min_value=1, value=1)
with col3:
    category = st.selectbox("Category", ["Produce", "Dairy", "Meat", "Pantry", "Frozen", "Beverages", "Snacks", "Other"])

if st.button("➕ Add to List", type="primary"):
    if item.strip():
        new_row = pd.DataFrame({
            "Item": [item.strip().title()],
            "Quantity": [qty],
            "Category": [category],
            "Added": [date.today()],
            "Bought": [False]
        })
        st.session_state.items = pd.concat([st.session_state.items, new_row], ignore_index=True)
        save_data(st.session_state.items)
        st.success(f"✅ Added {item}")
        st.rerun()

# Display list
st.subheader("Shopping List")

if len(st.session_state.items) > 0:
    edited_df = st.data_editor(
        st.session_state.items,
        hide_index=True,
        column_config={
            "Bought": st.column_config.CheckboxColumn("Bought", default=False),
            "Added": st.column_config.DateColumn(disabled=True),
            "Quantity": st.column_config.NumberColumn(min_value=1),
        },
        use_container_width=True,
    )

    # Save changes
    if not edited_df.equals(st.session_state.items):
        st.session_state.items = edited_df
        save_data(st.session_state.items)

    # Stats
    total = len(st.session_state.items)
    bought = st.session_state.items["Bought"].sum()
    col_a, col_b, col_c = st.columns(3)
    col_a.metric("Total Items", total)
    col_b.metric("Remaining", total - bought)
    col_c.metric("Bought", bought)

    csv = st.session_state.items.to_csv(index=False).encode()
    st.download_button("📥 Export CSV", csv, f"grocery_{date.today()}.csv", "text/csv")
else:
    st.info("Your list is empty — add items above 👆")

st.caption("Auto-saved locally on the server • Refresh to see latest")

# Nice footer
st.caption("Made with ❤️ by ROSE using Streamlit • Data saved locally")
