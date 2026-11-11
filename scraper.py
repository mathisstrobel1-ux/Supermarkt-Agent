import json

PRIO_STORES = ["Lidl", "Kaufland"]
MIN_DISCOUNT = 15

def run_scraper():
    # Hier liest der Bot die Daten ein und filtert
    # (Beispiel-Datenstruktur für den automatischen Abruf)
    raw_deals = [
        {"store": "Lidl", "title": "Barilla Pasta 500g", "price": 0.88, "old_price": 1.89, "category": "Vorrat"},
        {"store": "Lidl", "title": "Oatly Haferdrink 1L", "price": 1.29, "old_price": 2.19, "category": "Veggie"},
        {"store": "Kaufland", "title": "Jacobs Krönung 500g", "price": 3.99, "old_price": 7.49, "category": "Kaffee"},
        {"store": "Kaufland", "title": "Nutella 750g", "price": 2.79, "old_price": 4.29, "category": "Süßwaren"},
        {"store": "ALDI", "title": "Barilla Pasta 500g", "price": 0.99, "old_price": 1.89, "category": "Vorrat"},
        {"store": "REWE", "title": "Melitta Kaffee 500g", "price": 4.44, "old_price": 6.99, "category": "Kaffee"},
        {"store": "EDEKA", "title": "Tchibo Kaffee 500g", "price": 4.99, "old_price": 7.49, "category": "Kaffee"}
    ]

    processed_deals = []
    seen_products = set()

    for item in raw_deals:
        discount = round(((item["old_price"] - item["price"]) / item["old_price"]) * 100)
        if discount < MIN_DISCOUNT:
            continue

        prod_key = item["title"].lower().split()[0]
        if prod_key in seen_products:
            continue
        seen_products.add(prod_key)

        processed_deals.append({
            "store": item["store"],
            "title": item["title"],
            "price": item["price"],
            "old_price": item["old_price"],
            "discount": discount,
            "category": item["category"],
            "is_prio": item["store"] in PRIO_STORES
        })

    processed_deals.sort(key=lambda x: (0 if x["is_prio"] else 1, -x["discount"]))

    with open("deals.json", "w", encoding="utf-8") as f:
        json.dump(processed_deals, f, ensure_ascii=False, indent=2)

    print("deals.json erfolgreich aktualisiert!")

if __name__ == "__main__":
    run_scraper()
