# 🌍 Landmark Snap AI — Intelligent Location Recognition & Travel Estimator

**Landmark Snap AI** is a full-stack AI-powered platform that lets users upload any image of a famous landmark and receive:

- 🏛️ Accurate place name (via CLIP)
- 🧠 Smart, human-friendly descriptions (via GPT-4)
- 📍 Coordinates & resolved address
- 🚗 Road travel distance, duration, and cost
- ✈️ Flight distance and estimated flight cost

> Built with Django + React + Deep Learning + OpenAI, this project showcases intelligent geolocation, computer vision, and real-world cost estimation — all automated via CI/CD and container-ready.

---

## ✨ Features

- **🔍 Landmark Recognition**: Identifies global landmarks from images using OpenAI's CLIP model
- **📝 Natural Language Captions**: Generates rich descriptions using BLIP + GPT-4
- **📍 Geolocation Intelligence**: Uses Nominatim + Google Maps APIs to fetch place coordinates and calculate routes
- **💸 Cost Estimation**: Estimates travel costs for road and flight modes
- **🖼️ User-Friendly Frontend**: Clean React interface with image preview, upload, and real-time results
- **🔐 Secure Key Handling**: Environment variable-based config (no hardcoded secrets)
- **⚙️ CI/CD Ready**: GitHub Actions workflows for backend and frontend deployments
- **☁️ Cloud Deployable**: Designed for Azure App Service and Azure Static Web Apps

---

## 🛠️ Tech Stack

| Layer     | Technology |
|-----------|------------|
| Frontend  | React (Vite) + JavaScript |
| Backend   | Django + Django REST Framework |
| AI Models | CLIP (OpenAI), BLIP (Salesforce), GPT-4 |
| Geolocation | geopy, Google Maps API, Nominatim |
| Infra     | Azure App Service + Static Web Apps |
| CI/CD     | GitHub Actions |
| Other     | Gunicorn, dotenv, CORS, PIL |

---

## 🚀 Getting Started Locally

### 1. Clone the Repo

git clone https://github.com/vih-vijaya/landmark-snap.git
cd landmark-snap

2. Backend Setup (Django)
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
touch .env
✏️ .env file should include:
OPENAI_API_KEY=your-key
GOOGLE_MAPS_API_KEY=your-key
Then run:
python manage.py migrate
python manage.py runserver

3. Frontend Setup (React)
cd ../frontend
npm install
npm run dev
Visit: http://localhost:5173

Make sure to update your API URL inside App.jsx to match your local or production backend.

🧪 Sample API Response
{
  "predicted_place": "Taj Mahal",
  "caption": "The Taj Mahal is a breathtaking white marble mausoleum renowned for its iconic dome and romantic symbolism.",
  "resolved_place": "Taj Mahal, Agra, Uttar Pradesh, India",
  "from": "Fremont, United States",
  "coordinates": {
    "latitude": 27.1751,
    "longitude": 78.0421
  },
  "travel_modes": {
    "road": {
      "distance_km": 12540.4,
      "duration": "142 hours",
      "estimated_cost_usd": 6270.2
    },
    "flight": {
      "distance_km": 12360.8,
      "estimated_cost_usd": 3708.24
    }
  }
}
🖥️ CI/CD with GitHub Actions
frontend.yml: Deploys React app to Azure Static Web App on every push to main

backend.yml: Deploys Django app to Azure Web App using a zipped package and publish profile

📸 Screenshots / Demo
(Add screenshots of the UI and prediction output here)

💡 Project Highlights
✅ Combines Computer Vision + Natural Language + Geolocation

✅ Uses real models like CLIP, BLIP, and GPT — not dummy mockups

✅ Includes full DevOps pipeline with GitHub Actions

✅ Designed for real-world deployment (Azure-ready)

📚 Future Improvements
🌐 Add multilingual GPT captions

🗺️ Integrate interactive map for location display

🧠 Add historical facts or tourism tips

👤 Add user accounts and saved prediction history

🧑‍💻 Author
Vijayalakshmi
🧠 Machine Learning + Full Stack Developer

📄 License
This project is licensed under the MIT License.
---

Let me know if you'd like:
- A version tailored for your resume or portfolio
- Screenshots added
- It converted to a markdown file and pushed to your repo

You're ready to showcase this like a pro! 💪🚀
