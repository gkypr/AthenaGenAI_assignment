import requests
import json
import time

def fetch_and_analyze():
    # Fetch data from the API
    response = requests.get("https://fakestoreapi.com/products")
    if response.status_code == 200:
        products = response.json()
    else:
        print("Failed to retrieve data:", response.status_code)

    # Calculate required statistics
    total_products = len(products)
    prices = [product['price'] for product in products]
    average_price = sum(prices) / total_products

    max_price_product = max(products, key=lambda x: x['price'])
    min_price_product = min(products, key=lambda x: x['price'])

    # Count products in each category
    category_counts = {}
    for product in products:
        category = product['category']
        if category in category_counts:
            category_counts[category] += 1
        else:
            category_counts[category] = 1

    # Categorize products based on ratings
    low_rating_products = [product['title'] for product in products if product['rating']['rate'] < 3]
    high_rating_products = [product['title'] for product in products if product['rating']['rate'] > 4.1]

    # Create a report dictionary
    report = {
        "total_products": total_products,
        "average_price": average_price,
        "most_expensive_product": max_price_product['title'],
        "cheapest_product": min_price_product['title'],
        "products_per_category": category_counts,
        "low_rating_products": low_rating_products,
        "high_rating_products": high_rating_products
    }

    # Save the report to a JSON file
    with open('product_report.json', 'w') as file:
        json.dump(report, file, indent=4)


# Main loop - runs every 30 minutes
print("\nStarting product analyzer - runs every 30 minutes")
print("Press Ctrl+C to stop\n")

try:
    while True:
        fetch_and_analyze()
        print("Next run in 30 minutes...\n")
        time.sleep(30 * 60)  # 30 minutes
except KeyboardInterrupt:
    print("Stopped")