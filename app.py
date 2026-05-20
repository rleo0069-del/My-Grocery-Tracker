import streamlit as st
import pandas as pd
from datetime import date
import os

st.set_page_config(page_title="My Grocery Tracker", page_icon="🛒", layout="wide")

DATA_FILE = "grocery_list.csv"

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            df = pd.read_csv(DATA_FILE)
            df["Added"] = pd.to_datetime(df["Added"], errors='coerce').dt.date
            if "Bought" not in df.columns:
                df["Bought"] = False
            if "Category" not in df.columns:
                df["Category"] = "Other"
            return df
        except:
            pass
    # Empty DataFrame
    return pd.DataFrame(columns=["Item", "Quantity", "Category", "Added", "Bought"])

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

# ====================== SESSION STATE ======================
if "items" not in st.session_state:
    st.session_state.items = load_data()

# Force it to be a DataFrame (safety)
if not isinstance(st.session_state.items, pd.DataFrame):
    st.session_state.items = load_data()

# ====================== APP ======================
st.title("🛒 My Grocery Tracker")

# Sidebar
st.sidebar.header("Controls")
if st.sidebar.button("🗑️ Clear Entire List"):
    st.session_state.items = pd.DataFrame(columns=["Item", "Quantity", "Category", "Added", "Bought"])
    save_data(st.session_state.items)
    st.success("List cleared!")
    st.rerun()

# Add item
col1, col2, col3 = st.columns([3, 1, 1])
with col1:
    item = st.text_input("Item", placeholder="e.g. Milk")
with col2:
    qty = st.number_input("Quantity", min_value=1, value=1)
with col3:
    category = st.selectbox("Category", ["Produce", "Dairy", "Meat", "Pantry", "Frozen", "Beverages", "Snacks", "Other"])

if st.button("➕ Add Item", type="primary"):
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
        st.success(f"Added: {item.strip().title()}")
        st.rerun()

# Show list
st.subheader("Your Shopping List")

if len(st.session_state.items) > 0:
    edited = st.data_editor(
        st.session_state.items,
        hide_index=True,
        column_config={
            "Bought": st.column_config.CheckboxColumn("Bought", default=False),
            "Added": st.column_config.DateColumn("Added", disabled=True),
            "Quantity": st.column_config.NumberColumn("Qty", min_value=1),
        },
        use_container_width=True,
    )

    if not edited.equals(st.session_state.items):
        st.session_state.items = edited
        save_data(edited)

    # Stats
    total = len(st.session_state.items)
    bought_count = st.session_state.items["Bought"].sum()
    col1, col2, col3 = st.columns(3)
    col1.metric("Total", total)
    col2.metric("Remaining", total - bought_count)
    col3.metric("Bought", bought_count)

    # Export
    csv = st.session_state.items.to_csv(index=False).encode()
    st.download_button("📥 Download CSV", csv, f"grocery_list_{date.today()}.csv", "text/csv")
else:
    st.info("No items yet. Add some above!")

st.caption("💾 Your list is saved automatically")

# Nice footer
st.caption("Made with ❤️ by ROSE using Streamlit • Data saved locally")
