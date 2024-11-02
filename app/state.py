import reflex as rx
import json
import os
from openai import OpenAI
from typing import TypedDict, List, Literal, Dict, Union
import anthropic


TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# flux.1 schnell
client = OpenAI(
    api_key=TOGETHER_API_KEY,
    base_url="https://api.together.xyz/v1",
)

claude_client = anthropic.Anthropic()


def get_completion(prompt: str, system_prompt=""):
    message = claude_client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=2000,
        temperature=0.0,
        system=system_prompt,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text


def generate_prompt(city: str):
    PROMPT = f"""
  Generate a comprehensive city guide in JSON format following the exact schema and data type requirements. Each field should match the specified type and format.

  If any information is not available, mark it with empty string or "N/A".


  city: {city}


  JSON schema:
  {{
    "city": "Dallas",
    "state": "Texas",
    "country": "United States",
    "timezone": "Central Time Zone (UTC-6)",
    "currency": "USD",
    "currency_symbol": "$",
    "cost_metrics": {{
        "budget_daily": 100,
        "moderate_daily": 200,
        "luxury_daily": 400,
        "meal_budget": 15,
        "meal_moderate": 30,
        "meal_luxury": 60
    }},
    "weather_quarterly": {{
        "Jan-Mar": "45-65 F",
        "Apr-Jun": "65-85 F",
        "Jul-Sep": "80-100 F",
        "Oct-Dec": "50-70 F"
    }},
    "best_visit_months": ["March", "April", "October", "November"],
    "transportation": {{
        "rideshare": ["Uber", "Lyft"],
        "public_transit": ["DART Rail", "DART Bus"],
        "car_rental": ["Enterprise", "Hertz", "Avis"],
        "airport_code": ["DFW"]
    }},
    "top_attractions": [
        "Dallas Museum of Art",
        "Sixth Floor Museum",
        "Reunion Tower",
        "Dallas Arboretum",
        "Perot Museum",
        "Dallas World Aquarium",
        "Klyde Warren Park"
    ],
    "hidden_gems": [
        "Deep Ellum Art Company",
        "Thanks-Giving Square",
        "Cedar Ridge Preserve",
        "Bishop Arts District",
        "Dallas Farmers Market"
    ],
    "recommended_hotels": [
        {{
            "name": "The Joule",
            "category": "Luxury",
            "area": "Downtown",
            "price_range": "400-800"
        }},
        {{
            "name": "Hotel Crescent Court",
            "category": "Luxury",
            "area": "Uptown",
            "price_range": "350-700"
        }},
        {{
            "name": "Aloft Downtown Dallas",
            "category": "Moderate",
            "area": "Downtown",
            "price_range": "150-250"
        }},
        {{
            "name": "La Quinta Inn & Suites Market Center",
            "category": "Budget",
            "area": "Market Center",
            "price_range": "80-150"
        }}
    ],
    "food_scene": {{
        "local_specialties": ["Tex-Mex", "BBQ", "Southern Comfort Food"],
        "famous_restaurants": [
            "Pecan Lodge",
            "Mi Cocina",
            "Nick & Sam's",
            "Terry Black's BBQ"
        ]
    }},
    "safety_tips": [
        "Downtown is generally safe but stay aware at night",
        "Keep valuables secure and out of sight",
        "Use rideshare services late at night",
        "Be cautious during severe weather seasons"
    ],
    "wifi_availability": "Widely available in hotels, cafes, and public spaces",
    "language": "English",
    "tipping_custom": "15-20% for services",
    "emergency_numbers": {{
        "police": "911",
        "tourist_police": "214-671-3001",
        "us_embassy": "214-922-9000"
    }}
  }}

  """
    return PROMPT


def generate_trip_image(user_prompt):
    response = client.images.generate(
        prompt=user_prompt,
        model="black-forest-labs/FLUX.1-schnell",
        n=1,
        size="1792x1024",
    )
    return response.data[0].url


# with open("app/sample.json", "r") as file:
#     data = json.load(file)


class State(rx.State):
    city_input: str = ""
    is_loading: bool = False
    is_generating: bool = False
    img_url: str | None = ""
    trip_data: dict = {}
    weather_quarterly: Dict[str, str] = {}
    transportation: Dict[str, List[str]] = {}
    best_visit: List = []
    formatted_best_visit: str = ""

    # things to do
    things_to_do: List = []
    hidden_gems: List = []

    def handle_city_change(self, value: str):
        """Handle changes to the city input field."""
        self.city_input = value

    def start_generation(self):
        self.is_loading = True

    @rx.var
    def formatted_transport(self) -> Dict[str, List[str]]:
        return {k.replace("_", " ").title(): v for k, v in self.transportation.items()}

    def generate_city_guide(self):
        """Generate city guide when button is clicked."""
        try:
            # Generate the prompt using the user's input
            prompt = generate_prompt(self.city_input)

            # Get the completion from Claude
            response = get_completion(prompt)

            # Parse the JSON response
            new_data = json.loads(response)
            print(new_data)

            # Update the state with new data
            self.trip_data = new_data
            self.weather_quarterly = new_data["weather_quarterly"]
            self.transportation = new_data["transportation"]
            self.best_visit = new_data["best_visit_months"]
            self.formatted_best_visit = " | ".join(self.best_visit)
            self.things_to_do = new_data["top_attractions"]
            self.hidden_gems = new_data["hidden_gems"]

            # Generate new image for the city
            self.img_url = generate_trip_image(
                f"cinematic wide-angle photograph of {self.city_input}'s iconic skyline during golden hour, "
                f"featuring modern architecture, city landmarks, and urban landscape, "
                f"dramatic lighting, photorealistic, high detail, 4k, high resolution, "
                f"professional photography style, urban exploration"
            )
            self.is_loading = False

        except Exception as e:
            # Handle any errors
            print(f"Error generating city guide: {str(e)}")
