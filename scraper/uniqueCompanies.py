# import json

# def remove_duplicates_from_json(input_file="all_companies.json", output_file="unique_companies.json"):
#     with open(input_file, "r", encoding="utf-8") as f:
#         companies = json.load(f)

#     seen = set()
#     unique_companies = []

#     for company in companies:
#         website = company["website"]
#         if website not in seen:
#             seen.add(website)
#             unique_companies.append(company)

#     with open(output_file, "w", encoding="utf-8") as f:
#         json.dump(unique_companies, f, indent=2, ensure_ascii=False)

#     print(f"✅ Removed duplicates. {len(unique_companies)} unique companies saved to {output_file}")

# if __name__ == "__main__":
#     remove_duplicates_from_json()




import json
import csv

# Load the JSON file
with open("unique_companies.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Write website links to a CSV file
with open("company_websites.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["website"])  # Header
    for company in data:
        writer.writerow([company["website"]])