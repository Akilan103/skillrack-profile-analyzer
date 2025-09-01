import requests
from bs4 import BeautifulSoup

url=input("Enter the URL of your Profile from Skillrack :").strip()

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    total_score=0
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all parent <div class="statistic"> blocks
    name_block=soup.find('div',class_='ui big label black')
    if name_block:
        name=name_block.get_text(strip=True)
        print(f"Name : {name}")
    stats_blocks = soup.find_all('div', class_='statistic')

    for block in stats_blocks:
        value_div = block.find('div', class_='value')
        label_div = block.find('div', class_='label')

        # Ensure both parts exist
        if value_div and label_div:
            value = value_div.get_text(strip=True)
            label = label_div.get_text(strip=True)
            if label=="CODE TRACK":         #total score calculations out of 5000
                total_score+=int(value)*2
            elif label=="DC":
                total_score+=int(value)*2
            elif label=="DT":
                total_score+=int(value)*20
            print(f"{label}:{value}")
    print(f"Total Score :{total_score}/5000")
    print("Percentage :",total_score/50,"%",sep="")
else:
    print("Failed to fetch the page:", response.status_code)
