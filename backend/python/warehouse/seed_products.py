from mongoengine import connect
from product.models import Product
from product_category.models import ProductCategory

# =========================
# CONNECT DB
# =========================
connect(
    db="mydatabase",
    host="mongodb://root:example@localhost:27019/?authSource=admin",
    alias="default"
)

# =========================
# CATEGORY HELPER
# =========================
def get_or_create_category(title, description=""):
    category = ProductCategory.objects(title=title).first()
    if not category:
        category = ProductCategory(
            title=title,
            description=description
        )
        category.save()
    return category

# =========================
# SAMPLE PRODUCTS
# =========================
products_data = [
    {
        "name": "Lego Castle",
        "description": "Build a medieval castle with bricks, towers, and knights.",
        "price": 2500,
        "quantity": 20,
        "brand": "LEGO",
        "category": "Construction Toys"
    },
    {
        "name": "Lego City Set",
        "description": "Create roads, buildings, and vehicles with this construction set.",
        "price": 3000,
        "quantity": 15,
        "brand": "LEGO",
        "category": "Construction Toys"
    },
    {
        "name": "Wooden Blocks",
        "description": "Classic wooden blocks for stacking and creative play.",
        "price": 800,
        "quantity": 50,
        "brand": "FunWood",
        "category": "Educational Toys"
    },
    {
        "name": "Teddy Bear",
        "description": "Soft plush teddy bear for kids and comfort.",
        "price": 600,
        "quantity": 40,
        "brand": "SoftToys",
        "category": "Plush Toys"
    },
    {
        "name": "Action Figure",
        "description": "Superhero action figure with movable joints and accessories.",
        "price": 1200,
        "quantity": 25,
        "brand": "Hasbro",
        "category": "Action Figures"
    },
    {
        "name": "Puzzle Set 500 Pieces",
        "description": "Challenging puzzle set to improve problem-solving skills.",
        "price": 900,
        "quantity": 30,
        "brand": "BrainyGames",
        "category": "Board Games"
    },
    {
        "name": "Baby Rattle",
        "description": "Colorful rattle toy designed for toddlers.",
        "price": 300,
        "quantity": 60,
        "brand": "TinyPlay",
        "category": "Infant Toys"
    },
    {
        "name": "Soft Building Blocks",
        "description": "Safe and soft blocks for toddlers to stack and play.",
        "price": 700,
        "quantity": 35,
        "brand": "BabySoft",
        "category": "Educational Toys"
    }
]

# =========================
# INSERT DATA
# =========================
def seed_products():
    for item in products_data:
        category = get_or_create_category(item["category"])

        existing = Product.objects(
            name=item["name"],
            brand=item["brand"]
        ).first()

        if existing:
            print(f"⚠️ Already exists: {item['name']}")
            continue

        product = Product(
            name=item["name"],
            description=item["description"],
            price=item["price"],
            quantity=item["quantity"],
            brand=item["brand"],
            category=category
        )

        product.save()
        print(f"✅ Added: {item['name']}")

    print("\n🎉 Seeding complete!")

# =========================
# RUN
# =========================
if __name__ == "__main__":
    seed_products()