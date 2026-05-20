import streamlit as st
import pandas as pd
from datetime import date
import os

st.set_page_config(page_title="My Grocery Tracker", page_icon="🛒", layout="wide")

# ====================== JOY HEADER ======================
st.title("🛒 My Grocery Tracker")
st.markdown("### Fresh finds, easy tracking! 🛍️✨")

food_images = [
    "https://images.unsplash.com/photo-1583258292688-d0213dc5a3a8",
    "https://images.unsplash.com/photo-1604719312566-8912e9c8a5d4",
    "https://images.unsplash.com/photo-1542838132-92c53300491e",
    "https://images.unsplash.com/photo-1600585154340-be6161a56a9c",
    "https://images.unsplash.com/photo-1518845872607-9a6c6f3c4c3e"
]
cols = st.columns(5)
for i, url in enumerate(food_images):
    with cols[i % 5]:
        st.image(url, use_container_width=True)

st.markdown("---")

# ====================== DATA ======================
DATA_FILE = "grocery_list.csv"

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            df = pd.read_csv(DATA_FILE)
            df["Added"] = pd.to_datetime(df["Added"], errors='coerce').dt.date
            if "Bought" not in df.columns: df["Bought"] = False
            if "Category" not in df.columns: df["Category"] = "Other"
            return df
        except:
            pass
    return pd.DataFrame(columns=["Item", "Quantity", "Category", "Added", "Bought"])

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

# Use a different key to avoid the bug
if "grocery_data" not in st.session_state:
    st.session_state.grocery_data = load_data()

df = st.session_state.grocery_data

# Force it to be a DataFrame
if not isinstance(df, pd.DataFrame):
    df = load_data()
    st.session_state.grocery_data = df

# ====================== APP ======================
st.sidebar.header("Controls")
if st.sidebar.button("🗑️ Clear Entire List"):
    st.session_state.grocery_data = pd.DataFrame(columns=["Item", "Quantity", "Category", "Added", "Bought"])
    save_data(st.session_state.grocery_data)
    st.success("✅ List cleared!")
    st.rerun()

# Add item
col1, col2, col3 = st.columns([3, 1, 1])
with col1:
    item = st.text_input("What do you need?", placeholder="Milk, Bananas...")
with col2:
    qty = st.number_input("Qty", min_value=1, value=1)
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
        df = pd.concat([df, new_row], ignore_index=True)
        st.session_state.grocery_data = df
        save_data(df)
        st.success(f"✅ Added {item.strip().title()}")
        st.rerun()

# Display list
st.subheader("Your Shopping List")

if len(df) > 0:
    edited = st.data_editor(
        df,
        hide_index=True,
        column_config={
            "Bought": st.column_config.CheckboxColumn("Bought", default=False),
            "Added": st.column_config.DateColumn(disabled=True),
            "Quantity": st.column_config.NumberColumn("Qty", min_value=1),
        },
        use_container_width=True,
    )

    if not edited.equals(df):
        st.session_state.grocery_data = edited
        save_data(edited)
        df = edited

    total = len(df)
    bought = int(df["Bought"].sum())
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Items", total)
    c2.metric("Remaining", total - bought)
    c3.metric("Bought", bought)

    csv = df.to_csv(index=False).encode()
    st.download_button("📥 Export CSV", csv, f"grocery_{date.today()}.csv", "text/csv")
else:
    st.info("Your list is empty — add some items above! 🛍️")

st.caption("💾 Auto-saved • Joyful edition ❤️")import streamlit as st
import pandas as pd
from datetime import date
import os

st.set_page_config(page_title="My Grocery Tracker", page_icon="🛒", layout="wide")

# ====================== JOY HEADER ======================
st.title("🛒 My Grocery Tracker")
st.markdown("### Fresh finds, easy tracking! 🛍️✨")

food_images = [
    "https://images.unsplash.com/photo-1583258292688-d0213dc5a3a8",
    "https://images.unsplash.com/photo-1604719312566-8912e9c8a5d4",
    "https://images.unsplash.com/photo-1542838132-92c53300491e",
    "https://images.unsplash.com/photo-1600585154340-be6161a56a9c",
    "https://images.unsplash.com/photo-1518845872607-9a6c6f3c4c3e"
]
cols = st.columns(5)
for i, url in enumerate(food_images):
    with cols[i % 5]:
        st.image(url, use_container_width=True)

st.markdown("---")

# ====================== DATA ======================
DATA_FILE = "grocery_list.csv"

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            df = pd.read_csv(DATA_FILE)
            df["Added"] = pd.to_datetime(df["Added"], errors='coerce').dt.date
            if "Bought" not in df.columns: df["Bought"] = False
            if "Category" not in df.columns: df["Category"] = "Other"
            return df
        except:
            pass
    return pd.DataFrame(columns=["Item", "Quantity", "Category", "Added", "Bought"])

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

# Use a different key to avoid the bug
if "grocery_data" not in st.session_state:
    st.session_state.grocery_data = load_data()

df = st.session_state.grocery_data

# Force it to be a DataFrame
if not isinstance(df, pd.DataFrame):
    df = load_data()
    st.session_state.grocery_data = df

# ====================== APP ======================
st.sidebar.header("Controls")
if st.sidebar.button("🗑️ Clear Entire List"):
    st.session_state.grocery_data = pd.DataFrame(columns=["Item", "Quantity", "Category", "Added", "Bought"])
    save_data(st.session_state.grocery_data)
    st.success("✅ List cleared!")
    st.rerun()

# Add item
col1, col2, col3 = st.columns([3, 1, 1])
with col1:
    item = st.text_input("What do you need?", placeholder="Milk, Bananas...")
with col2:
    qty = st.number_input("Qty", min_value=1, value=1)
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
        df = pd.concat([df, new_row], ignore_index=True)
        st.session_state.grocery_data = df
        save_data(df)
        st.success(f"✅ Added {item.strip().title()}")
        st.rerun()

# Display list
st.subheader("Your Shopping List")

if len(df) > 0:
    edited = st.data_editor(
        df,
        hide_index=True,
        column_config={
            "Bought": st.column_config.CheckboxColumn("Bought", default=False),
            "Added": st.column_config.DateColumn(disabled=True),
            "Quantity": st.column_config.NumberColumn("Qty", min_value=1),
        },
        use_container_width=True,
    )

    if not edited.equals(df):
        st.session_state.grocery_data = edited
        save_data(edited)
        df = edited

    total = len(df)
    bought = int(df["Bought"].sum())
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Items", total)
    c2.metric("Remaining", total - bought)
    c3.metric("Bought", bought)

    csv = df.to_csv(index=False).encode()
    st.download_button("📥 Export CSV", csv, f"grocery_{date.today()}.csv", "text/csv")
else:
    st.info("Your list is empty — add some items above! 🛍️")

st.caption("💾 Auto-saved • Joyful edition ❤️")
