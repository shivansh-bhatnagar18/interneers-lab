import streamlit as st
import pandas as pd
import numpy as np
from mongoengine import connect
from product.models import Product
from product_category.models import ProductCategory
from sentence_transformers import SentenceTransformer

# =========================
# DB CONNECT
# =========================
connect(
    db="mydatabase",
    host="mongodb://root:example@localhost:27019/?authSource=admin",
    alias="default"
)

# =========================
# LOAD MODEL (CACHE)
# =========================
@st.cache_resource
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

model = load_model()

# =========================
# LOAD PRODUCTS
# =========================
products = list(Product.objects())

# =========================
# PREPARE TEXTS
# =========================
texts = [
    f"{p.name} {p.brand} {p.category.title if p.category else ''} {p.description or ''}"
    for p in products
]

# =========================
# BUILD EMBEDDINGS (CACHE)
# =========================
@st.cache_data
def build_embeddings(texts):
    return model.encode(texts)

embeddings = build_embeddings(texts)

# =========================
# COSINE SIMILARITY
# =========================
def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# =========================
# SEMANTIC SEARCH
# =========================
def semantic_search(query, products, embeddings, top_k=3):
    query_emb = model.encode(query)

    scores = []
    for i, p in enumerate(products):
        score = cosine_similarity(query_emb, embeddings[i])
        scores.append((p, score))

    scores.sort(key=lambda x: x[1], reverse=True)
    return scores[:top_k]

# =========================
# UI SETUP
# =========================
st.set_page_config(page_title="Inventory Dashboard", layout="wide")
st.title("📦 Inventory Dashboard")

# =========================
# DATAFRAME
# =========================
data = []
for p in products:
    data.append({
        "ID": str(p.id),
        "Name": p.name,
        "Brand": p.brand,
        "Category": p.category.title if p.category else "None",
        "Price": p.price,
        "Quantity": p.quantity
    })

df = pd.DataFrame(data)

# =========================
# FILTERS
# =========================
st.sidebar.header("🔍 Filters")

categories = ["All"] + [c.title for c in ProductCategory.objects()]
selected_category = st.sidebar.selectbox("Category", categories)

brands = ["All"] + list(df["Brand"].unique()) if not df.empty else ["All"]
selected_brand = st.sidebar.selectbox("Brand", brands)

low_stock_only = st.sidebar.checkbox("Show Low Stock (<=10)")

filtered_df = df.copy()

if selected_category != "All":
    filtered_df = filtered_df[filtered_df["Category"] == selected_category]

if selected_brand != "All":
    filtered_df = filtered_df[filtered_df["Brand"] == selected_brand]

if low_stock_only:
    filtered_df = filtered_df[filtered_df["Quantity"] <= 10]

# =========================
# 🔥 SEMANTIC SEARCH
# =========================
st.subheader("🔍 Semantic Search")

query = st.text_input("Search products semantically")

if query:
    results = semantic_search(query, products, embeddings)

    for product, score in results:
        st.write(f"**{product.name}**")
        st.write(f"Score: {score:.3f}")
        st.write(product.description)
        st.markdown("---")

# =========================
# ➕ ADD PRODUCT
# =========================
st.sidebar.markdown("---")
st.sidebar.header("➕ Add Product")

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
            st.sidebar.success("✅ Product Added")
            st.rerun()

# =========================
# METRICS
# =========================
col1, col2, col3 = st.columns(3)

col1.metric("Total Products", len(df))
col2.metric("Filtered Products", len(filtered_df))
col3.metric("Low Stock", len(df[df["Quantity"] <= 10]) if not df.empty else 0)

# =========================
# TABLE
# =========================
st.subheader("📋 Product Inventory")
st.dataframe(filtered_df, use_container_width=True)

# =========================
# LOW STOCK
# =========================
st.subheader("⚠️ Low Stock Products")

low_stock_df = df[df["Quantity"] <= 10] if not df.empty else pd.DataFrame()

if not low_stock_df.empty:
    st.dataframe(low_stock_df, use_container_width=True)
else:
    st.success("No low stock items 🎉")

# =========================
# ❌ DELETE PRODUCT
# =========================
st.markdown("---")
st.subheader("❌ Delete Product")

if products:
    product_map = {f"{p.name} ({p.brand})": str(p.id) for p in products}

    selected_label = st.selectbox("Select Product", list(product_map.keys()))
    selected_id = product_map[selected_label]

    if st.button("Delete Selected Product"):
        product = Product.objects(id=selected_id).first()

        if product:
            product.delete()
            st.success("🗑 Product Deleted Successfully")
            st.rerun()
        else:
            st.error("Product not found")
else:
    st.info("No products available to delete")