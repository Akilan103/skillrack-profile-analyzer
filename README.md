🖥️ Skillrack Profile Analyzer

A Python script to fetch and display key details from a user's Skillrack profile.
This tool is specifically designed for students in our college, where scoring above 5000 points in Skillrack is a requirement for on-campus placements.

📌 Features

Fetches and displays:

👤 User's Name

📊 Code Tracks Completed

🏆 Levels Completed

📅 Daily Challenges (DC)

📝 Daily Tests (DT)

⭐ Total Score out of 5000

📈 Percentage of the score

Calculates placement eligibility score (based on Skillrack activity).

🚀 Usage
1️⃣ Clone the Repository
git clone https://github.com/Akilan103/skillrack-profile-analyzer.git
cd skillrack-profile-analyzer

2️⃣ Install Requirements

This script uses requests and beautifulsoup4. Install them with:

pip install requests beautifulsoup4

3️⃣ Run the Script
python skillrack_profile.py


When prompted, enter your Skillrack profile URL.

🔑 How to Get Your Skillrack Profile URL

Log in to Skillrack

Go to Profile.

Skillrack will ask you to re-enter your password.

Once the profile loads, copy the URL from the address bar.

Example: https://www.skillrack.com/faces/resume.xhtml?id=XXXX

Paste this URL into the script when asked.

📊 Score Calculation

The script computes the total score (out of 5000) as:

CODE TRACK → value * 2

DC (Daily Challenges) → value * 2

DT (Daily Tests) → value * 20

Then displays:

Total Score : XXXX/5000
Percentage : YY%

🏫 College Placement Note

Students must score at least 5000 points on Skillrack to be eligible for campus placements. This script helps you quickly track your progress.

👥 Contribution

Want to improve the script?

Fork the repo

Make changes

Create a Pull Request

📜 License

This project is open-source under the MIT License.