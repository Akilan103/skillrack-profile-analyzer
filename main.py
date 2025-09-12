import re
import io
import base64
import os
from typing import Dict

import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

from fastapi import FastAPI, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# allow requests from your local frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ensure temp folder exists
os.makedirs("static", exist_ok=True)


def normalize_url(url: str) -> str:
    """Ensure https scheme for skillrack URLs."""
    url = url.strip()
    if url.startswith("http://"):
        url = "https://" + url[len("http://"):]
    if not url.startswith("http"):
        url = "https://" + url
    return url


def extract_number(text: str) -> int:
    """Return first integer found in text or 0."""
    match = re.search(r"\d+", text)
    return int(match.group()) if match else 0


def find_value_in_text(full_text: str, label: str) -> str:
    """Find number near label in text."""
    # 1) number immediately before label
    p1 = re.search(r"(\d+(?:/\d+)?)(?=\s*[:\-–]?\s*" + re.escape(label) + r")", full_text, flags=re.I)
    if p1:
        return p1.group(1).strip()
    # 2) label followed by number
    p2 = re.search(re.escape(label) + r"\s*[:\-–]?\s*(\d+(?:/\d+)?)", full_text, flags=re.I)
    if p2:
        return p2.group(1).strip()
    # 3) looser search nearby
    p3 = re.search(r"(\d+(?:/\d+)?).{0,40}?" + re.escape(label), full_text, flags=re.I)
    if p3:
        return p3.group(1).strip()
    p4 = re.search(re.escape(label) + r".{0,40}?(\d+(?:/\d+)?)", full_text, flags=re.I)
    if p4:
        return p4.group(1).strip()
    return ""


@app.post("/process")
def process_profile(url: str = Form(...)):
    url = normalize_url(url)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36"
    }

    try:
        resp = requests.get(url, headers=headers, timeout=15)
        resp.raise_for_status()
    except Exception as e:
        return JSONResponse({"error": f"Failed to fetch URL: {e}"}, status_code=400)

    soup = BeautifulSoup(resp.text, "html.parser")
    page_text = soup.get_text(" ", strip=True)

    details: Dict[str, str] = {}

    # ✅ Extract Name
    name_block = soup.find("div", class_="ui big label black")
    if name_block:
        details["Name"] = name_block.get_text(strip=True)
    else:
        possible = soup.find(["h1", "h2"])
        details["Name"] = possible.get_text(strip=True) if possible else "Unknown"

    # ✅ Fixed labels
    fixed_labels = [
        "RANK", "LEVEL", "GOLD", "SILVER", "BRONZE",
        "PROGRAMS SOLVED", "CODE TEST", "CODE TRACK",
        "DC", "DT", "CODE TUTOR"
    ]

    for lbl in fixed_labels:
        raw = find_value_in_text(page_text, lbl)
        details[lbl] = raw if raw != "" else "0"

    # ✅ Dynamic language extraction (C, Python3, Java, C++, SQL, …)
    stats = soup.select("div.ui.six.small.statistics div.statistic")
    for stat in stats:
        value = stat.select_one(".value")
        label = stat.select_one(".label")
        if value and label:
            lang = label.get_text(strip=True)   # Language name
            val = value.get_text(strip=True)    # Count (e.g., 473, 208, 20)
            details[lang] = val

    # ✅ Convert to numeric dict
    numeric = {}
    for key, raw in details.items():
        if key == "LEVEL":
            numeric[key] = extract_number(raw)
        else:
            numeric[key] = extract_number(raw)

    # ✅ Points calculation
    total_score = 0
    points_map = {}
    for label in ["CODE TRACK", "DC", "DT"]:
        val = numeric.get(label, 0)
        if label == "CODE TRACK":
            pts = val * 2
        elif label == "DC":
            pts = val * 2
        elif label == "DT":
            pts = val * 20
        else:
            pts = 0
        points_map[label] = pts
        total_score += pts

    percentage = round((total_score / 5000) * 100, 2)

    # ✅ Pie chart (base64)
    filtered = {k: v for k, v in points_map.items() if v > 0}
    chart_b64 = None
    if filtered:
        fig, ax = plt.subplots(figsize=(5, 5))
        ax.pie(filtered.values(), labels=filtered.keys(), autopct="%1.1f%%", startangle=90)
        ax.set_title("Contribution to 5000 Points")
        buf = io.BytesIO()
        plt.savefig(buf, format="png", bbox_inches="tight")
        plt.close(fig)
        buf.seek(0)
        chart_b64 = base64.b64encode(buf.read()).decode("utf-8")

    return {
        "details": details,
        "numeric": numeric,
        "points_breakdown": points_map,
        "total_score": f"{total_score}/5000",
        "percentage": f"{percentage}%",
        "chart": chart_b64,
        "fetched_url": url
    }
