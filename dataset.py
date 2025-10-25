import json
import csv


with open('/content/data.json', 'r') as f:
    transaction_data = json.load(f)

category_keywords = {
    'Starbucks': ['Starbucks'],
    'Office': ['godaddy', 'CORP', 'service charge', 'analysis service', 'zoom', 'Intelius', 'Createsendcom', 'Expensify', 'Wave', 'Kauffman', 'Granada', 'Glendora', 'INC', 'Ltd', 'Pipedrive', 'comcast', 'wage', 'salary', 'Tax', 'Auto', 'Group', 'Vistaprint', 'Bamboohr', 'Ringcentral'],
    'Personal': ['CHEWY', 'wawa', 'restaurant', 'coffee', 'mcdonald', 'pizza', 'food', 'bakery', 'Wholesale', 'Holmes', 'Fashion', 'Family', 'Fun', 'Wife', 'Wifey', 'Corral', 'Slice', 'Marios'],
    'Amazon': ['amazon', 'amzn', 'prime video', 'audible'],
    'Ebay': ['ebay'],
    'Subscriptions': ['SUBSCR', 'Subscription', 'OpenAI', 'Claud AI', 'Tidal', 'Spotify', 'Yahoo', 'NYTimes'],
    'Banks': ['AMERICAN0012212750125', 'PHEONIX', 'AZ', 'Capital One', 'Chase', 'Bank'],
    'Health': ['Health', 'Hospital', 'HealthInsPremium', 'Dr', 'Doctor', 'Clinic', 'Medical', 'Dental'],
    'Apple': ['Apple', 'apple.com', 'iCloud', 'iTunes'],
    'Google': ['google', 'gmail', 'youtube', 'youtube premium'],
    'Travel': ['uber', 'airline', 'flight', 'hotel', 'american airline', 'air china', 'disney', 'Metro'],
    'Fuel': ['shell', 'chevron', 'sunoco', 'gas station', 'fuel', 'oil', 'Gas', 'EXXON MOBIL'],
    'Home': ['Wal-Mart', 'walmart', 'target', 'costco', 'grocery', 'supermarket', 'save a lot', 'shoprite', 'Home', 'Depot', 'walmart.com', 'costco.com', 'Harbor Freight', 'The Home Depot'],
    'Bills': ['pay', 'Paid to', 'Paid', 'payment', 'funding', 'internet', 'starlink', 'fee', 'fees', 'bill', 'bills', 'billpay', 'electricity', 'energy', 'water', 'electric', 'water', 'gas', 'utility', 'phone', 'internet', 'cable', 'insurance', 'Comcast'],
    'Entertainment': ['Video', 'Music', 'Movie', 'Streaming'],
    'Transactions': ['Cash App', 'Venmo', 'Zelle', 'received from', 'received', 'paypal', 'account', 'deposit', 'withdrawal', 'from account', 'mobile banking', 'zelle', 'electronic', 'branch', 'customer']
}

def categorize_description(description: str) -> str:
    """Categorize transaction description based on keywords"""
    if not description:
        return 'Uncategorized'
    
    desc_lower = description.lower()

    for category, keywords in category_keywords.items():
        for keyword in keywords:
            if keyword.lower() in desc_lower:
                return category

    return 'Others'

training_data = []
seen_descriptions = set()

for transaction in transaction_data:
    description = transaction.get('Description', '')

    if description and description.strip() and description not in seen_descriptions:
        seen_descriptions.add(description)
        category = categorize_description(description)
        training_data.append({
            'Description': description,
            'Category': category
        })

csv_filename = 'transaction_training_data.csv'
with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Description', 'Category']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()
    for row in training_data:
        writer.writerow(row)

print(f"Created training dataset with {len(training_data)} unique samples")
print(f"CSV file saved as: {csv_filename}")

category_counts = {}
for item in training_data:
    category = item['Category']
    category_counts[category] = category_counts.get(category, 0) + 1

print("\nCategory distribution:")
for category, count in sorted(category_counts.items(), key=lambda x: x[1], reverse=True):
    print(f"{category}: {count} samples")

print("\nSample training data (first 10 entries):")
print("-" * 80)
for i, item in enumerate(training_data[:10]):
    desc = item['Description'].replace('\n', ' ')
    print(f"{i+1:2d}. {item['Category']:15} | {desc[:60]}...")
