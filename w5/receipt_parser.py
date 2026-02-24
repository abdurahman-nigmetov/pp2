import re
import json
import csv

with open("raw.txt", encoding="utf-8") as f:
	text = f.read()

product_pattern = re.compile(
	r"""\n\d+\.\n(.*?)\n([\d,\. ]+) x ([\d,\.]+)\n([\d,\. ]+)\nСтоимость\n([\d,\. ]+)""",
	re.DOTALL
)
products = []
for match in product_pattern.finditer(text):
	name = match.group(1).strip()
	qty = match.group(2).replace(' ', '').replace(',', '.')
	price_per_unit = match.group(3).replace(' ', '').replace(',', '.')
	total_price = match.group(5).replace(' ', '').replace(',', '.')
	products.append({
		"name": name,
		"quantity": float(qty),
		"price_per_unit": float(price_per_unit),
		"total_price": float(total_price)
	})

total_pattern = re.compile(r"ИТОГО:\s*([\d\s,]+)")
total_match = total_pattern.search(text)
total = float(total_match.group(1).replace(' ', '').replace(',', '.')) if total_match else None

datetime_pattern = re.compile(r"Время:\s*(\d{2}\.\d{2}\.\d{4} \d{2}:\d{2}:\d{2})")
datetime_match = datetime_pattern.search(text)
datetime = datetime_match.group(1) if datetime_match else None

payment_pattern = re.compile(r"Банковская карта:")
payment_method = "Банковская карта" if payment_pattern.search(text) else None

result = {
	"products": products,
	"total": total,
	"datetime": datetime,
	"payment_method": payment_method
}

print(json.dumps(result, ensure_ascii=False, indent=2))


with open("data.csv", "w", encoding="utf-8", newline='') as f:
	writer = csv.writer(f)
	writer.writerow(["name", "quantity", "price_per_unit", "total_price"])
	for p in products:
		writer.writerow([p["name"], p["quantity"], p["price_per_unit"], p["total_price"]])
    