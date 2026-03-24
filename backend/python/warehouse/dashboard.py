import streamlit as st
import pandas as pd
import sys
import os
print(sys.path)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
from mongoengine import connect
from product.models import Product
from product_category.models import ProductCategory

connect(
    db="mydatabase",
    host="mongodb://root:example@localhost:27019/?authSource=admin",
    alias="default"
)

st.set_page_config(page_title="Inventory Dashboard", layout="wide")

st.title("Inventory Dashboard")

products = Product.objects()

data = []
for p in products:
    data.append({
        "ID": str(p.id),
        "Name": p.name,
        "Brand": p.brand,
        "Category": p.category.title if p.category else "None",
        "Price": p.price,
        "Quantity": p.quantity,
        "Created At": p.created_at
    })

df = pd.DataFrame(data)

st.sidebar.header(" Filters")

# Category filter
categories = ["All"] + [c.title for c in ProductCategory.objects()]
selected_category = st.sidebar.selectbox("Category", categories)

# Brand filter
brands = ["All"] + list(df["Brand"].unique()) if not df.empty else ["All"]
selected_brand = st.sidebar.selectbox("Brand", brands)

# Low stock filter
low_stock_only = st.sidebar.checkbox("Show Low Stock (<=10)")

# 🎯 Apply Filters
filtered_df = df.copy()

if selected_category != "All":
    filtered_df = filtered_df[filtered_df["Category"] == selected_category]

if selected_brand != "All":
    filtered_df = filtered_df[filtered_df["Brand"] == selected_brand]

if low_stock_only:
    filtered_df = filtered_df[filtered_df["Quantity"] <= 10]

# =========================
# ➕ ADD PRODUCT
# =========================

st.sidebar.markdown("---")
st.sidebar.header(" Add Product")

with st.sidebar.form("add_product_form"):
    new_name = st.text_input("Name")
    new_description = st.text_input("Description")
    new_price = st.number_input("Price", min_value=0.0)
    new_quantity = st.number_input("Quantity", min_value=0)

    new_brand = st.text_input("Brand")

    category_objs = list(ProductCategory.objects())
    category_map = {c.title: c for c in category_objs}

    new_category_title = st.selectbox("Category", list(category_map.keys()))

    submit = st.form_submit_button("Add Product")

    if submit:
        if not new_name or not new_brand:
            st.sidebar.error("Name and Brand are required")
        else:
            product = Product(
                name=new_name,
                description=new_description,
                price=new_price,
                quantity=new_quantity,
                brand=new_brand,
                category=category_map[new_category_title]
            )
            product.save()

            st.sidebar.success(" Product Added")

            st.rerun()

#  Metrics
col1, col2, col3 = st.columns(3)

col1.metric("Total Products", len(df))
col2.metric("Filtered Products", len(filtered_df))
col3.metric("Low Stock Items", len(df[df["Quantity"] <= 10]) if not df.empty else 0)

#  Display Table
st.subheader(" Product Inventory")

st.dataframe(filtered_df, use_container_width=True)

#  Low Stock Highlight
st.subheader(" Low Stock Products")

low_stock_df = df[df["Quantity"] <= 10] if not df.empty else pd.DataFrame()

if not low_stock_df.empty:
    st.dataframe(low_stock_df, use_container_width=True)
else:
    st.success("No low stock items ")

# =========================
# ❌ DELETE PRODUCT
# =========================

st.markdown("---")
st.subheader(" Delete Product")

product_list = list(Product.objects())

if product_list:
    product_display = {
        f"{p.name} ({p.brand})": str(p.id)
        for p in product_list
    }

    selected_product_label = st.selectbox(
        "Select Product",
        list(product_display.keys())
    )

    selected_product_id = product_display[selected_product_label]

    if st.button("Delete Selected Product"):
        product = Product.objects(id=selected_product_id).first()

        if product:
            product.delete()
            st.success("🗑 Product Deleted Successfully")
            st.rerun()
        else:
            st.error("Product not found")
else:
    st.info("No products available to delete")
