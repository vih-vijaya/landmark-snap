from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
import base64
from io import BytesIO
import requests
import torch
import os
import openai
from dotenv import load_dotenv
from transformers import BlipProcessor, BlipForConditionalGeneration
import clip
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import googlemaps

# Load environment variables
load_dotenv()
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)
geolocator = Nominatim(user_agent="landmark_snap_ai")

# Load models
device = "cuda" if torch.cuda.is_available() else "cpu"
blip_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
blip_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base").to(device)
clip_model, clip_preprocess = clip.load("ViT-B/32", device=device)

# Landmark list for CLIP
landmark_list = [
    "Taj Mahal", "Eiffel Tower", "Statue of Liberty", "Golden Gate Bridge", "Mount Fuji",
    "Niagara Falls", "Burj Khalifa", "Big Ben", "Colosseum", "Great Wall of China",
    "Christ the Redeemer", "Petra", "Machu Picchu", "Sydney Opera House", "Louvre Museum",
    "Acropolis", "Angkor Wat", "Notre Dame", "London Bridge", "Hagia Sophia"
]
landmark_tokens = clip.tokenize(landmark_list).to(device)

# Cost rates
ROAD_COST_PER_KM = 0.5
FLIGHT_COST_PER_KM = 0.3

class LandmarkPredictView(APIView):
    def post(self, request):
        try:
            img_data = request.data.get("image")
            if isinstance(img_data, str) and "," in img_data:
                header, encoded = img_data.split(",", 1)
                image = Image.open(BytesIO(base64.b64decode(encoded))).convert("RGB")
            elif isinstance(img_data, InMemoryUploadedFile):
                image = Image.open(img_data).convert("RGB")
            else:
                return Response({"error": "Invalid image format"}, status=400)

            # Step 1: Get place name using CLIP
            image_tensor = clip_preprocess(image).unsqueeze(0).to(device)
            with torch.no_grad():
                image_features = clip_model.encode_image(image_tensor)
                text_features = clip_model.encode_text(landmark_tokens)
                similarities = (image_features @ text_features.T).squeeze(0)
                best_match_idx = similarities.argmax().item()
                best_place = landmark_list[best_match_idx]

            # Step 2: Get caption using BLIP
            inputs = blip_processor(images=image, return_tensors="pt").to(device)
            output = blip_model.generate(**inputs)
            raw_caption = blip_processor.decode(output[0], skip_special_tokens=True)

            # Step 3: Enhance caption using GPT
            prompt = f"You are a travel guide. In one sentence, describe this place for visitors: '{raw_caption}'"
            gpt_response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a professional travel writer."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=60
            )
            enhanced_caption = gpt_response['choices'][0]['message']['content'].strip()

            # Step 4: Geocode the predicted place
            location = geolocator.geocode(best_place)
            if not location:
                return Response({"error": f"Could not locate '{best_place}' on the map."}, status=404)
            landmark_coords = (location.latitude, location.longitude)

            # Step 5: Get user location from IP
            ip = request.META.get("REMOTE_ADDR")
            if not ip or ip.startswith("127.") or ip.startswith("192.168.") or "::1" in ip:
                ip = "73.170.44.110"
            geo_resp = requests.get(f"https://ipapi.co/{ip}/json/").json()
            user_city = geo_resp.get("city")
            user_country = geo_resp.get("country_name")
            lat = geo_resp.get("latitude")
            lon = geo_resp.get("longitude")
            if not all([user_city, user_country, lat, lon]):
                return Response({"error": "Could not determine user location from IP."}, status=400)
            user_coords = (lat, lon)
            user_location_name = f"{user_city}, {user_country}"

            # Step 6: Google Maps road distance
            directions = gmaps.distance_matrix(
                origins=user_location_name,
                destinations=f"{location.latitude},{location.longitude}",
                mode="driving"
            )
            element = directions["rows"][0]["elements"][0]
            try:
                road_km = element["distance"]["value"] / 1000
                road_cost = round(road_km * ROAD_COST_PER_KM, 2)
                road_duration = element["duration"]["text"]
                road_result = {
                    "distance_km": round(road_km, 2),
                    "duration": road_duration,
                    "estimated_cost_usd": road_cost
                }
            except KeyError:
                road_result = {"error": "Road route not available"}

            # Step 7: Flight distance
            flight_km = geodesic(user_coords, landmark_coords).km
            flight_cost = round(flight_km * FLIGHT_COST_PER_KM, 2)

            return Response({
                "predicted_place": best_place,
                "caption": enhanced_caption,
                "resolved_place": location.address,
                "coordinates": {
                    "latitude": location.latitude,
                    "longitude": location.longitude
                },
                "from": user_location_name,
                "travel_modes": {
                    "road": road_result,
                    "flight": {
                        "distance_km": round(flight_km, 2),
                        "estimated_cost_usd": flight_cost
                    }
                }
            })

        except Exception as e:
            return Response({"error": str(e)}, status=500)
