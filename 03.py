from config import get_collection

collection = get_collection()

for arbre in collection.find().limit(20):
    print(f"{arbre.get('nom', 'N/A')} - {arbre.get('latin', 'N/A')}")

