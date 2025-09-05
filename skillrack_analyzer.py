import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
import matplotlib.pyplot as plt
import re  # for extracting numbers

def extract_number(text):
    """Extract the first number found in text, or 0 if none."""
    match = re.search(r'\d+', text)
    return int(match.group()) if match else 0

url = input("Enter the URL of your Profile from Skillrack :").strip()

headers = {
    "User-Agent": "Mozilla/5.0"
}

try:
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()  # Raises error for 4xx/5xx responses
except RequestException as e:
    print("Invalid URL or network issue:", e)
    exit()

if response.status_code == 200:
    total_score = 0
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all parent <div class="statistic"> blocks
    name_block = soup.find('div', class_='ui big label black')
    if name_block:
        name = name_block.get_text(strip=True)
        print(f"Name : {name}")
    stats_blocks = soup.find_all('div', class_='statistic')

    score_breakdown = {}

    for block in stats_blocks:
        value_div = block.find('div', class_='value')
        label_div = block.find('div', class_='label')

        if value_div and label_div:
            raw_value = value_div.get_text(strip=True)
            value = extract_number(raw_value)  # ✅ safe conversion
            label = label_div.get_text(strip=True)

            if label == "CODE TRACK":
                points = value * 2
            elif label == "DC":
                points = value * 2
            elif label == "DT":
                points = value * 20
            else:
                points = 0

            total_score += points
            score_breakdown[label] = points
            print(f"{label}: {raw_value}")  # show raw value like "0/10"

    print(f"Total Score :{total_score}/5000")
    print("Percentage :", total_score/50, "%", sep="")

    # ✅ Filter out 0% contributors
    filtered_scores = {k: v for k, v in score_breakdown.items() if v > 0}

    if filtered_scores:
        plt.pie(filtered_scores.values(), labels=filtered_scores.keys(),
                autopct='%1.1f%%', startangle=90)
        plt.title("Contribution (5000)")
        plt.show()
    else:
        print("No contributions to display in chart.")
else:
    print("Failed to fetch the page:", response.status_code)