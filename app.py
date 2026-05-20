import streamlit as st
import pandas as pd
from datetime import date, datetime
import os

st.set_page_config(page_title="My Grocery Tracker", page_icon="🛒", layout="wide")

# ====================== DATA PERSISTENCE ======================
DATA_FILE = "grocery_list.csv"

def load_data():
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        df["Added"] = pd.to_datetime(df["Added"]).dt.date
        if "Bought" not in df.columns:
            df["Bought"] = False
        return df
    else:
        return pd.DataFrame(columns=["Item", "Quantity", "Category", "Added", "Bought"])

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

# Load data
if "items" not in st.session_state:
    st.session_state.items = load_data()

# ====================== SIDEBAR ======================
st.sidebar.header("🛒 Grocery Tracker")
st.sidebar.markdown("**Keep track of what you need**")

if st.sidebar.button("🗑️ Clear Entire List"):
    st.session_state.items = pd.DataFrame(columns=["Item", "Quantity", "Category", "Added", "Bought"])
    save_data(st.session_state.items)
    st.success("List cleared!")

st.sidebar.markdown("---")
st.sidebar.info("Data is saved automatically to grocery_list.csv")

# ====================== MAIN APP ======================
st.title("🛒 My Grocery Tracker")
st.caption(f"Last updated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}")

# --- Add new item ---
col1, col2, col3 = st.columns([3, 1, 1])
with col1:
    item = st.text_input("What do you need to buy?", placeholder="e.g. Milk, Bananas...")
with col2:
    qty = st.number_input("Quantity", min_value=1, value=1)
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
        st.success(f"Added: {item}")
    else:
        st.warning("Please enter an item name")

# --- Display the list ---
if not st.session_state.items.empty:
    st.subheader("Your Shopping List")

    # Make a copy for editing
    df = st.session_state.items.copy()

    # Add checkboxes for "Bought"
    edited_df = st.data_editor(
        df,
        hide_index=True,
        column_config={
            "Bought": st.column_config.CheckboxColumn("Bought", default=False, width=80),
            "Added": st.column_config.DateColumn("Added", disabled=True),
            "Quantity": st.column_config.NumberColumn("Qty", min_value=1),
        },
        use_container_width=True,
    )

    # Update session state if changes were made
    if not edited_df.equals(st.session_state.items):
        st.session_state.items = edited_df
        save_data(st.session_state.items)

    # Summary stats
    total_items = len(st.session_state.items)
    bought_count = st.session_state.items["Bought"].sum()
    remaining = total_items - bought_count

    col_a, col_b, col_c = st.columns(3)
    col_a.metric("Total Items", total_items)
    col_b.metric("Remaining", remaining, delta=-bought_count)
    col_c.metric("Completed", f"{bought_count}/{total_items}")

    # Download button
    csv = st.session_state.items.to_csv(index=False).encode()
    st.download_button(
        label="📥 Export to CSV",
        data=csv,
        file_name=f"grocery_list_{date.today()}.csv",
        mime="text/csv"
    )
else:
    st.info("Your list is empty. Add some items above! 🛍️")

# Nice footer
st.caption("Made with ❤️ by ROSE using Streamlit • Data saved locally")
