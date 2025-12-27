import streamlit as st
import json
from datetime import datetime, timedelta
import pandas as pd
import random

# Page config
st.set_page_config(
    page_title="Pune Events Discovery",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for modern attractive UI
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Modern gradient background */
    .main {
        background: #ffffff;
        color: #2c3e50;
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 50%, #dee2e6 100%);
    }
    
    /* Glassmorphism header */
    .hero-header {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 20px;
        padding: 3rem 2rem;
        text-align: center;
        margin: 2rem 0;
        position: relative;
        overflow: hidden;
        color: #2c3e50;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }
    
    .hero-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        animation: shine 3s infinite;
    }
    
    @keyframes shine {
        0% { left: -100%; }
        100% { left: 100%; }
    }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: 700;
        color: #4ecdc4;
        margin-bottom: 1rem;
    }
    
    .hero-subtitle {
        font-size: 1.2rem;
        color: #6c757d;
        font-weight: 400;
    }
    
    /* Modern glass cards */
    .neon-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
        position: relative;
        color: #2c3e50;
    }
    
    .neon-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
        border-color: rgba(78, 205, 196, 0.3);
        background: rgba(255, 255, 255, 0.15);
    }
    
    /* Ensure all text is visible */
    .stMarkdown, .stText, p, span, div {
        color: #2c3e50 !important;
    }
    
    /* Modern button styling */
    .stButton > button {
        background: #4ecdc4 !important;
        color: white !important;
        border: none !important;
        border-radius: 25px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 600 !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.2) !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(78, 205, 196, 0.3) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(78, 205, 196, 0.4) !important;
        background: #45b7d1 !important;
    }
    
    /* Selectbox styling */
    .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.9) !important;
        color: #2c3e50 !important;
        border: 2px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 10px !important;
        backdrop-filter: blur(10px) !important;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab"] {
        background: #4ecdc4 !important;
        color: white !important;
        border-radius: 15px !important;
        font-weight: 600 !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.2) !important;
        margin: 0 5px !important;
        box-shadow: 0 4px 15px rgba(78, 205, 196, 0.3) !important;
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: #45b7d1 !important;
        box-shadow: 0 6px 20px rgba(69, 183, 209, 0.4) !important;
    }
    
    /* Info boxes */
    .stInfo {
        background: #74b9ff !important;
        color: white !important;
        font-weight: 500 !important;
        border-radius: 10px !important;
        border: none !important;
    }
    
    .stSuccess {
        background: #00b894 !important;
        color: white !important;
        font-weight: 500 !important;
        border-radius: 10px !important;
        border: none !important;
    }
    
    .stWarning {
        background: #fdcb6e !important;
        color: white !important;
        font-weight: 500 !important;
        border-radius: 10px !important;
        border: none !important;
    }
    
    .stError {
        background: #fd79a8 !important;
        color: white !important;
        font-weight: 500 !important;
        border-radius: 10px !important;
        border: none !important;
    }
    
    /* Modern metric cards */
    .metric-card {
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        margin: 0.5rem 0;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
    }
    
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.15);
        background: rgba(255, 255, 255, 0.15);
        border-color: rgba(78, 205, 196, 0.3);
    }
    
    .metric-card h4 {
        font-size: 1.5rem;
        font-weight: 700;
        color: #4ecdc4;
        margin: 0;
    }
    
    .metric-card p {
        color: #6c757d;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin: 0.5rem 0 0 0;
    }
    
    /* Slider styling */
    .stSlider > div > div > div {
        background: linear-gradient(90deg, #ff6b6b, #4ecdc4) !important;
    }
    
    /* Enhanced expander styling */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.9) !important;
        border-radius: 10px !important;
        border: 2px solid rgba(255, 255, 255, 0.3) !important;
        backdrop-filter: blur(10px) !important;
    }
    
    /* Radio button styling */
    .stRadio > div {
        background: rgba(255, 255, 255, 0.9) !important;
        border-radius: 10px !important;
        padding: 1rem !important;
        backdrop-filter: blur(10px) !important;
    }
    
    /* Checkbox styling */
    .stCheckbox > div {
        background: rgba(255, 255, 255, 0.9) !important;
        border-radius: 10px !important;
        padding: 0.5rem !important;
        backdrop-filter: blur(10px) !important;
    }
    
    /* Multiselect styling */
    .stMultiSelect > div > div {
        background: rgba(255, 255, 255, 0.9) !important;
        border: 2px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 10px !important;
        backdrop-filter: blur(10px) !important;
    }
    
    /* Chart styling */
    .stPlotlyChart {
        background: rgba(255, 255, 255, 0.9) !important;
        border-radius: 15px !important;
        padding: 1rem !important;
        backdrop-filter: blur(10px) !important;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1) !important;
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(45deg, #4ecdc4, #45b7d1);
    }
    
    /* Loading animation */
    .loading {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid rgba(255, 107, 107, 0.3);
        border-radius: 50%;
        border-top-color: #ff6b6b;
        animation: spin 1s ease-in-out infinite;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    
    /* Floating elements */
    .floating {
        animation: float 3s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
</style>
""", unsafe_allow_html=True)

# Load local context (you'll customize this with your city's info)
@st.cache_data
def load_local_context():
    return {
        "city_name": "Pune",
        "popular_venues": [
            "Shaniwar Wada", "Phoenix MarketCity", "Koregaon Park", 
            "FC Road", "Pune University", "Sinhagad Fort", "Osho Ashram", "Deccan Gymkhana"
        ],
        "neighborhoods": [
            "Koregaon Park", "FC Road", "Deccan", "Baner", "Camp Area", "Kothrud", "Viman Nagar"
        ],
        "event_types": [
            "Classical Music", "Marathi Theater", "Tech Meetups", "Food Festivals", 
            "Outdoor Treks", "Cultural Shows", "Startup Events", "Wellness Events"
        ]
    }

# Sample event data (in real app, this would come from APIs)
@st.cache_data
def load_sample_events():
    return [
        # KOREGAON PARK - All Event Types
        {
            "title": "Osho Morning Meditation",
            "venue": "Osho Ashram",
            "date": "2025-12-22",
            "time": "06:00",
            "type": "Wellness Events",
            "neighborhood": "Koregaon Park",
            "description": "Daily meditation and mindfulness session",
            "price": "₹500",
            "cultural_note": "International crowd, dress in white or maroon"
        },
        {
            "title": "Jazz Night at German Bakery",
            "venue": "German Bakery",
            "date": "2025-12-22",
            "time": "20:00",
            "type": "Classical Music",
            "neighborhood": "Koregaon Park",
            "description": "Live jazz performance with international artists",
            "price": "₹400",
            "cultural_note": "Popular expat hangout, book tables early"
        },
        {
            "title": "International Food Festival",
            "venue": "Koregaon Park Club",
            "date": "2025-12-23",
            "time": "18:00",
            "type": "Food Festivals",
            "neighborhood": "Koregaon Park",
            "description": "Cuisines from 15 countries in one venue",
            "price": "₹600",
            "cultural_note": "Diverse crowd, vegetarian options available"
        },
        {
            "title": "Digital Nomad Meetup",
            "venue": "Cafe Mocha",
            "date": "2025-12-24",
            "time": "16:00",
            "type": "Tech Meetups",
            "neighborhood": "Koregaon Park",
            "description": "Networking for remote workers and freelancers",
            "price": "₹200",
            "cultural_note": "Bring laptop, WiFi and coffee provided"
        },
        {
            "title": "International Theater Workshop",
            "venue": "Osho Auditorium",
            "date": "2025-12-25",
            "time": "14:00",
            "type": "Marathi Theater",
            "neighborhood": "Koregaon Park",
            "description": "Multi-language theater techniques workshop",
            "price": "₹800",
            "cultural_note": "English and Hindi, some Marathi elements"
        },
        {
            "title": "Morning Yoga in the Park",
            "venue": "Koregaon Park Gardens",
            "date": "2025-12-26",
            "time": "06:30",
            "type": "Outdoor Treks",
            "neighborhood": "Koregaon Park",
            "description": "Outdoor yoga session in peaceful gardens",
            "price": "₹150",
            "cultural_note": "Bring yoga mat, suitable for beginners"
        },

        # FC ROAD - All Event Types
        {
            "title": "College Band Competition",
            "venue": "Fergusson College Auditorium",
            "date": "2025-12-22",
            "time": "19:00",
            "type": "Classical Music",
            "neighborhood": "FC Road",
            "description": "Inter-college music competition with local bands",
            "price": "₹100",
            "cultural_note": "Young energetic crowd, very loud and fun"
        },
        {
            "title": "Street Food Festival",
            "venue": "FC Road Main Street",
            "date": "2025-12-23",
            "time": "17:00",
            "type": "Food Festivals",
            "neighborhood": "FC Road",
            "description": "Best street food vendors from across Pune",
            "price": "₹200",
            "cultural_note": "Try vada pav, misal pav, and bhel puri"
        },
        {
            "title": "Coding Bootcamp",
            "venue": "Fergusson College Computer Lab",
            "date": "2025-12-24",
            "time": "10:00",
            "type": "Tech Meetups",
            "neighborhood": "FC Road",
            "description": "Learn Python programming in one day",
            "price": "₹300",
            "cultural_note": "Student-friendly, bring laptop if you have one"
        },
        {
            "title": "College Drama Festival",
            "venue": "Modern College Theater",
            "date": "2025-12-25",
            "time": "18:30",
            "type": "Marathi Theater",
            "neighborhood": "FC Road",
            "description": "Students perform classic Marathi plays",
            "price": "₹80",
            "cultural_note": "Affordable tickets, enthusiastic student audience"
        },
        {
            "title": "Fitness Flash Mob",
            "venue": "Goodluck Cafe Area",
            "date": "2025-12-26",
            "time": "07:00",
            "type": "Wellness Events",
            "neighborhood": "FC Road",
            "description": "Group fitness session with dance moves",
            "price": "Free",
            "cultural_note": "Join spontaneously, very inclusive atmosphere"
        },
        {
            "title": "Heritage Cycle Tour",
            "venue": "FC Road to Shaniwar Wada",
            "date": "2025-12-27",
            "time": "06:00",
            "type": "Outdoor Treks",
            "neighborhood": "FC Road",
            "description": "Cycling tour of historic Pune landmarks",
            "price": "₹250",
            "cultural_note": "Cycles provided, helmet mandatory"
        },

        # DECCAN - All Event Types
        {
            "title": "Classical Music Concert",
            "venue": "Shaniwar Wada",
            "date": "2025-12-22",
            "time": "19:30",
            "type": "Classical Music",
            "neighborhood": "Deccan",
            "description": "Renowned artists perform Hindustani classical",
            "price": "₹400",
            "cultural_note": "Traditional venue, dress modestly"
        },
        {
            "title": "Maharashtrian Thali Festival",
            "venue": "Deccan Gymkhana",
            "date": "2025-12-23",
            "time": "12:00",
            "type": "Food Festivals",
            "neighborhood": "Deccan",
            "description": "Authentic Maharashtrian cuisine showcase",
            "price": "₹350",
            "cultural_note": "Traditional recipes, eat with hands for authenticity"
        },
        {
            "title": "AI & Machine Learning Seminar",
            "venue": "Pune University",
            "date": "2025-12-24",
            "time": "14:00",
            "type": "Tech Meetups",
            "neighborhood": "Deccan",
            "description": "Academic conference on latest AI trends",
            "price": "₹500",
            "cultural_note": "Academic setting, bring notepad"
        },
        {
            "title": "Traditional Marathi Natya Sangam",
            "venue": "Bharat Natya Mandir",
            "date": "2025-12-25",
            "time": "19:00",
            "type": "Marathi Theater",
            "neighborhood": "Deccan",
            "description": "Classic Marathi theater by veteran actors",
            "price": "₹300",
            "cultural_note": "Pure Marathi, traditional audience"
        },
        {
            "title": "Ayurveda Workshop",
            "venue": "Tilak Maharashtra Vidyapeeth",
            "date": "2025-12-26",
            "time": "10:00",
            "type": "Wellness Events",
            "neighborhood": "Deccan",
            "description": "Learn traditional Ayurvedic practices",
            "price": "₹600",
            "cultural_note": "Ancient wisdom, modern application"
        },
        {
            "title": "Parvati Hill Trek",
            "venue": "Parvati Hill Base",
            "date": "2025-12-27",
            "time": "05:30",
            "type": "Outdoor Treks",
            "neighborhood": "Deccan",
            "description": "Early morning trek to Parvati Temple",
            "price": "₹100",
            "cultural_note": "Religious significance, remove shoes at temple"
        },

        # BANER - All Event Types
        {
            "title": "Corporate Music Night",
            "venue": "Westin Hotel Baner",
            "date": "2025-12-22",
            "time": "20:00",
            "type": "Classical Music",
            "neighborhood": "Baner",
            "description": "Professional musicians for corporate crowd",
            "price": "₹800",
            "cultural_note": "Business casual dress code, networking opportunity"
        },
        {
            "title": "Global Cuisine Food Truck Festival",
            "venue": "Baner Balewadi Sports Complex",
            "date": "2025-12-23",
            "time": "18:00",
            "type": "Food Festivals",
            "neighborhood": "Baner",
            "description": "International food trucks in one location",
            "price": "₹400",
            "cultural_note": "IT crowd favorite, card payments accepted"
        },
        {
            "title": "Startup Pitch Competition",
            "venue": "WeWork Baner",
            "date": "2025-12-24",
            "time": "15:00",
            "type": "Tech Meetups",
            "neighborhood": "Baner",
            "description": "Entrepreneurs pitch to investors",
            "price": "₹300",
            "cultural_note": "Bring business cards, great for networking"
        },
        {
            "title": "Corporate Theater Workshop",
            "venue": "Baner Community Hall",
            "date": "2025-12-25",
            "time": "16:00",
            "type": "Marathi Theater",
            "neighborhood": "Baner",
            "description": "Team building through theater activities",
            "price": "₹500",
            "cultural_note": "Mix of languages, corporate-friendly"
        },
        {
            "title": "Office Wellness Program",
            "venue": "Cerebrum IT Park",
            "date": "2025-12-26",
            "time": "08:00",
            "type": "Wellness Events",
            "neighborhood": "Baner",
            "description": "Stress management for IT professionals",
            "price": "₹250",
            "cultural_note": "Designed for working professionals"
        },
        {
            "title": "Corporate Adventure Challenge",
            "venue": "Baner Hills",
            "date": "2025-12-27",
            "time": "06:00",
            "type": "Outdoor Treks",
            "neighborhood": "Baner",
            "description": "Team building adventure activities",
            "price": "₹600",
            "cultural_note": "Company groups welcome, safety gear provided"
        },

        # CAMP AREA - All Event Types
        {
            "title": "Elite Classical Concert",
            "venue": "Pune Club",
            "date": "2025-12-22",
            "time": "19:00",
            "type": "Classical Music",
            "neighborhood": "Camp Area",
            "description": "Premium classical music performance",
            "price": "₹1000",
            "cultural_note": "Formal dress code, elite crowd"
        },
        {
            "title": "Fine Dining Festival",
            "venue": "JW Marriott Pune",
            "date": "2025-12-23",
            "time": "19:30",
            "type": "Food Festivals",
            "neighborhood": "Camp Area",
            "description": "Michelin-style cuisine showcase",
            "price": "₹2000",
            "cultural_note": "Upscale dining, reservations required"
        },
        {
            "title": "Executive Tech Summit",
            "venue": "Hotel Hyatt",
            "date": "2025-12-24",
            "time": "09:00",
            "type": "Tech Meetups",
            "neighborhood": "Camp Area",
            "description": "C-level executives discuss tech trends",
            "price": "₹1500",
            "cultural_note": "Business formal, high-level networking"
        },
        {
            "title": "English Theater Performance",
            "venue": "Camp Cultural Center",
            "date": "2025-12-25",
            "time": "20:00",
            "type": "Marathi Theater",
            "neighborhood": "Camp Area",
            "description": "International English play adaptation",
            "price": "₹600",
            "cultural_note": "English language, sophisticated audience"
        },
        {
            "title": "Luxury Spa Experience",
            "venue": "The Ritz Carlton Spa",
            "date": "2025-12-26",
            "time": "11:00",
            "type": "Wellness Events",
            "neighborhood": "Camp Area",
            "description": "Premium wellness and relaxation",
            "price": "₹3000",
            "cultural_note": "Luxury experience, advance booking required"
        },
        {
            "title": "Golf Tournament",
            "venue": "Pune Race Course",
            "date": "2025-12-27",
            "time": "07:00",
            "type": "Outdoor Treks",
            "neighborhood": "Camp Area",
            "description": "Corporate golf championship",
            "price": "₹2500",
            "cultural_note": "Golf attire required, club membership preferred"
        },

        # KOTHRUD - All Event Types
        {
            "title": "Community Bhajan Evening",
            "venue": "Kothrud Temple",
            "date": "2025-12-22",
            "time": "18:00",
            "type": "Classical Music",
            "neighborhood": "Kothrud",
            "description": "Traditional devotional music gathering",
            "price": "Free",
            "cultural_note": "Family-friendly, remove shoes before entering"
        },
        {
            "title": "Home-style Cooking Competition",
            "venue": "Kothrud Community Center",
            "date": "2025-12-23",
            "time": "11:00",
            "type": "Food Festivals",
            "neighborhood": "Kothrud",
            "description": "Local families showcase traditional recipes",
            "price": "₹100",
            "cultural_note": "Authentic home cooking, family atmosphere"
        },
        {
            "title": "Computer Literacy for Seniors",
            "venue": "Kothrud Library",
            "date": "2025-12-24",
            "time": "15:00",
            "type": "Tech Meetups",
            "neighborhood": "Kothrud",
            "description": "Basic computer skills for elderly residents",
            "price": "₹50",
            "cultural_note": "Patient instructors, family members welcome"
        },
        {
            "title": "Local Marathi Drama Group",
            "venue": "Kothrud Natya Mandir",
            "date": "2025-12-25",
            "time": "19:30",
            "type": "Marathi Theater",
            "neighborhood": "Kothrud",
            "description": "Community theater by local residents",
            "price": "₹150",
            "cultural_note": "Pure Marathi, neighborhood audience"
        },
        {
            "title": "Family Yoga Session",
            "venue": "Kothrud Garden",
            "date": "2025-12-26",
            "time": "07:00",
            "type": "Wellness Events",
            "neighborhood": "Kothrud",
            "description": "Yoga for all ages and fitness levels",
            "price": "₹80",
            "cultural_note": "Bring children, mats provided"
        },
        {
            "title": "Nature Walk for Families",
            "venue": "Kothrud Hills",
            "date": "2025-12-27",
            "time": "06:30",
            "type": "Outdoor Treks",
            "neighborhood": "Kothrud",
            "description": "Easy nature walk suitable for all ages",
            "price": "₹50",
            "cultural_note": "Child-friendly, educational about local flora"
        },

        # VIMAN NAGAR - All Event Types
        {
            "title": "Airport Lounge Jazz",
            "venue": "Marriott Courtyard",
            "date": "2025-12-22",
            "time": "21:00",
            "type": "Classical Music",
            "neighborhood": "Viman Nagar",
            "description": "Smooth jazz for business travelers",
            "price": "₹700",
            "cultural_note": "International crowd, flight schedules considered"
        },
        {
            "title": "International Business Lunch",
            "venue": "Phoenix MarketCity Food Court",
            "date": "2025-12-23",
            "time": "12:30",
            "type": "Food Festivals",
            "neighborhood": "Viman Nagar",
            "description": "Global cuisine for corporate professionals",
            "price": "₹500",
            "cultural_note": "Quick service, business discussions welcome"
        },
        {
            "title": "IT Industry Conference",
            "venue": "Eon IT Park Convention Center",
            "date": "2025-12-24",
            "time": "09:30",
            "type": "Tech Meetups",
            "neighborhood": "Viman Nagar",
            "description": "Latest trends in software development",
            "price": "₹800",
            "cultural_note": "Tech professionals, bring laptop and business cards"
        },
        {
            "title": "Corporate Drama Workshop",
            "venue": "Viman Nagar Cultural Center",
            "date": "2025-12-25",
            "time": "17:00",
            "type": "Marathi Theater",
            "neighborhood": "Viman Nagar",
            "description": "Team building through theater exercises",
            "price": "₹400",
            "cultural_note": "English and Hindi, corporate-friendly timing"
        },
        {
            "title": "Executive Fitness Program",
            "venue": "Airport Road Gym",
            "date": "2025-12-26",
            "time": "06:00",
            "type": "Wellness Events",
            "neighborhood": "Viman Nagar",
            "description": "High-intensity workout for busy professionals",
            "price": "₹300",
            "cultural_note": "Early timing for working professionals"
        },
        {
            "title": "Corporate Adventure Race",
            "venue": "Viman Nagar Sports Complex",
            "date": "2025-12-27",
            "time": "07:00",
            "type": "Outdoor Treks",
            "neighborhood": "Viman Nagar",
            "description": "Team building through adventure challenges",
            "price": "₹800",
            "cultural_note": "Corporate teams, safety equipment provided"
        }
    ]

def main():
    # Initialize session state
    if 'saved_events' not in st.session_state:
        st.session_state.saved_events = []
    if 'user_preferences' not in st.session_state:
        st.session_state.user_preferences = {}
    if 'show_map' not in st.session_state:
        st.session_state.show_map = False
    
    # Colorful header
    st.markdown("""
    <div class="main-header">
        <h1>🎉 Pune Events Discovery</h1>
        <p>Discover events that match Pune's unique culture and your preferences</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Load data
    local_context = load_local_context()
    events = load_sample_events()
    
    # Top navigation tabs with colors
    tab1, tab2, tab3, tab4 = st.tabs(["🔍 Discover Events", "❤️ Saved Events", "🎯 Preferences", "📊 Insights"])
    
    with tab1:
        # Main discovery interface
        col1, col2 = st.columns([2, 1])
        
        with col2:
            # Colorful filter section
            st.markdown("""
            <div style="background: linear-gradient(135deg, #ff6b6b 0%, #4ecdc4 100%); 
                        padding: 1.5rem; border-radius: 15px; color: white; margin-bottom: 1rem;
                        box-shadow: 0 8px 25px rgba(255, 107, 107, 0.3);">
                <h3 style="margin: 0; text-shadow: 1px 1px 2px rgba(0,0,0,0.2);">🎛️ Find Your Vibe</h3>
            </div>
            """, unsafe_allow_html=True)
            
            # Interactive filters with emojis
            selected_neighborhood = st.selectbox(
                "🏘️ Neighborhood", 
                ["All Areas"] + local_context["neighborhoods"],
                help="Each area has its own personality!"
            )
            
            selected_type = st.selectbox(
                "🎭 Event Type",
                ["All Types"] + local_context["event_types"],
                help="What's your mood today?"
            )
            
            # Price range slider
            price_range = st.slider(
                "💰 Price Range (₹)",
                0, 1000, (0, 500),
                step=50,
                help="Budget-friendly to premium events"
            )
            
            # Time preference
            time_pref = st.radio(
                "⏰ Preferred Time",
                ["Any Time", "Morning (6-12)", "Afternoon (12-18)", "Evening (18-24)"],
                help="When do you like to have fun?"
            )
            
            # Weather consideration
            weather_aware = st.checkbox(
                "🌧️ Consider Pune Weather",
                value=True,
                help="Filter based on current season"
            )
            
            # Quick mood selector with colorful buttons
            st.markdown("""
            <div style="background: linear-gradient(135deg, #45b7d1 0%, #96ceb4 100%); 
                        padding: 1rem; border-radius: 10px; color: white; margin: 1rem 0;
                        box-shadow: 0 6px 20px rgba(69, 183, 209, 0.3);">
                <strong style="text-shadow: 1px 1px 2px rgba(0,0,0,0.2);">🎯 Quick Mood Selector:</strong>
            </div>
            """, unsafe_allow_html=True)
            
            mood_cols = st.columns(3)
            with mood_cols[0]:
                if st.button("🎵 Musical", use_container_width=True):
                    selected_type = "Classical Music"
                    st.rerun()
            with mood_cols[1]:
                if st.button("🍛 Foodie", use_container_width=True):
                    selected_type = "Food Festivals"
                    st.rerun()
            with mood_cols[2]:
                if st.button("🏔️ Adventure", use_container_width=True):
                    selected_type = "Outdoor Treks"
                    st.rerun()
        
        with col1:
            # Filter events based on selections
            filtered_events = filter_events(events, selected_neighborhood, selected_type, price_range, time_pref)
            
            if filtered_events:
                # Colorful results header
                st.markdown(f"""
                <div style="background: linear-gradient(90deg, #74b9ff, #0984e3); 
                            padding: 1rem; border-radius: 10px; text-align: center; margin-bottom: 1rem;
                            box-shadow: 0 6px 20px rgba(116, 185, 255, 0.3);">
                    <h3 style="color: white; margin: 0; text-shadow: 1px 1px 2px rgba(0,0,0,0.2);">🎪 Found {len(filtered_events)} events for you!</h3>
                </div>
                """, unsafe_allow_html=True)
                
                # Sort options
                sort_by = st.selectbox(
                    "Sort by:", 
                    ["Date", "Price (Low to High)", "Price (High to Low)", "Neighborhood"]
                )
                
                # Display events with enhanced interactivity and colors
                for i, event in enumerate(filtered_events):
                    # Colorful event card
                    card_colors = [
                        "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                        "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)",
                        "linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)",
                        "linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)"
                    ]
                    card_color = card_colors[i % len(card_colors)]
                    
                    with st.expander(f"🎫 {event['title']} - {event['venue']}", expanded=(i==0)):
                        st.markdown(f"""
                        <div style="background: {card_color}; 
                                    padding: 1rem; border-radius: 10px; color: white; margin-bottom: 1rem;">
                        """, unsafe_allow_html=True)
                        
                        event_cols = st.columns([2, 1, 1])
                        
                        with event_cols[0]:
                            st.markdown(f"**📍 Location:** {event['venue']}, {event['neighborhood']}")
                            st.markdown(f"**📅 When:** {event['date']} at {event['time']}")
                            st.markdown(f"**📝 About:** {event['description']}")
                            
                            # Enhanced cultural insights
                            if event.get("cultural_note"):
                                st.info(f"🧠 **Pune Insider Tip:** {event['cultural_note']}")
                            
                            # Add venue-specific tips
                            venue_tip = get_venue_tip(event['venue'])
                            if venue_tip:
                                st.success(f"🏛️ **Venue Tip:** {venue_tip}")
                        
                        with event_cols[1]:
                            # Colorful metrics
                            st.markdown(f"""
                            <div class="metric-card">
                                <h4>💰 {event['price']}</h4>
                                <p>Price</p>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            st.markdown(f"""
                            <div class="metric-card">
                                <h4>🏷️ {event['type']}</h4>
                                <p>Type</p>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Weather compatibility
                            if weather_aware:
                                weather_score = get_weather_compatibility(event)
                                st.markdown(f"""
                                <div class="metric-card">
                                    <h4>🌤️ {weather_score}%</h4>
                                    <p>Weather Match</p>
                                </div>
                                """, unsafe_allow_html=True)
                        
                        with event_cols[2]:
                            # Interactive buttons
                            if st.button(f"❤️ Save", key=f"save_{event['title']}", use_container_width=True):
                                if event not in st.session_state.saved_events:
                                    st.session_state.saved_events.append(event)
                                    st.success("Saved! ✨")
                                else:
                                    st.info("Already saved!")
                            
                            if st.button(f"📍 Get Directions", key=f"dir_{event['title']}", use_container_width=True):
                                st.info(f"🚗 Directions to {event['venue']}")
                            
                            if st.button(f"📱 Share", key=f"share_{event['title']}", use_container_width=True):
                                st.success("Link copied! 📋")
                            
                            # Interest rating
                            interest = st.slider(
                                "Interest Level",
                                1, 5, 3,
                                key=f"interest_{event['title']}",
                                help="Help us learn your preferences"
                            )
                        
                        st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style="background: linear-gradient(135deg, #ffeaa7, #fab1a0); 
                            padding: 2rem; border-radius: 15px; text-align: center;">
                    <h3>🔍 No events match your criteria</h3>
                    <p><strong>💡 Suggestions:</strong></p>
                    <p>• Try 'All Areas' for neighborhood</p>
                    <p>• Expand your price range</p>
                    <p>• Check 'Any Time' for timing</p>
                </div>
                """, unsafe_allow_html=True)
    
    with tab2:
        # Saved events tab
        st.subheader("❤️ Your Saved Events")
        
        if st.session_state.saved_events:
            st.success(f"You have {len(st.session_state.saved_events)} saved events!")
            
            for event in st.session_state.saved_events:
                with st.container():
                    cols = st.columns([3, 1])
                    with cols[0]:
                        st.markdown(f"**🎫 {event['title']}**")
                        st.markdown(f"📍 {event['venue']} • 📅 {event['date']}")
                    with cols[1]:
                        if st.button(f"🗑️ Remove", key=f"remove_{event['title']}"):
                            st.session_state.saved_events.remove(event)
                            st.rerun()
                    st.divider()
            
            # Export options
            if st.button("📤 Export to Calendar"):
                st.success("Calendar file downloaded! 📅")
        else:
            st.info("No saved events yet. Start exploring! 🎯")
    
    with tab3:
        # User preferences tab
        st.subheader("🎯 Customize Your Experience")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**🏘️ Favorite Neighborhoods:**")
            fav_neighborhoods = st.multiselect(
                "Select your preferred areas:",
                local_context["neighborhoods"],
                default=st.session_state.user_preferences.get('neighborhoods', [])
            )
            
            st.markdown("**🎭 Preferred Event Types:**")
            fav_types = st.multiselect(
                "What do you enjoy?",
                local_context["event_types"],
                default=st.session_state.user_preferences.get('types', [])
            )
        
        with col2:
            st.markdown("**⏰ Preferred Times:**")
            pref_times = st.multiselect(
                "When are you usually free?",
                ["Morning", "Afternoon", "Evening", "Weekend"],
                default=st.session_state.user_preferences.get('times', [])
            )
            
            st.markdown("**💰 Budget Range:**")
            budget = st.slider(
                "Typical spending on events (₹):",
                0, 2000, 
                st.session_state.user_preferences.get('budget', 500)
            )
        
        if st.button("💾 Save Preferences"):
            st.session_state.user_preferences = {
                'neighborhoods': fav_neighborhoods,
                'types': fav_types,
                'times': pref_times,
                'budget': budget
            }
            st.success("Preferences saved! Your recommendations will be personalized. ✨")
    
    with tab4:
        # Insights and analytics tab
        st.subheader("📊 Pune Event Scene Insights")
        
        # Create some interactive charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**🏘️ Events by Neighborhood**")
            neighborhood_data = {}
            for event in events:
                neighborhood_data[event['neighborhood']] = neighborhood_data.get(event['neighborhood'], 0) + 1
            
            st.bar_chart(neighborhood_data)
        
        with col2:
            st.markdown("**🎭 Popular Event Types**")
            type_data = {}
            for event in events:
                type_data[event['type']] = type_data.get(event['type'], 0) + 1
            
            st.bar_chart(type_data)
        
        # Cultural insights
        st.markdown("**🧠 Cultural Intelligence**")
        insights = [
            "🎵 Classical music events are most popular in winter months",
            "🍛 Food festivals peak during festival seasons",
            "🏔️ Trekking events are weather-dependent (avoid monsoons)",
            "🎭 Marathi theater has strong weekend audiences",
            "💻 Tech events cluster in Baner-Hinjewadi corridor"
        ]
        
        for insight in insights:
            st.info(insight)
    
    # Floating action button simulation
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🔄 Refresh Events", use_container_width=True):
            st.success("Events refreshed! ✨")
            st.rerun()

# Helper functions for enhanced interactivity
def filter_events(events, neighborhood, event_type, price_range, time_pref):
    filtered = events.copy()
    
    if neighborhood != "All Areas":
        filtered = [e for e in filtered if e["neighborhood"] == neighborhood]
    
    if event_type != "All Types":
        filtered = [e for e in filtered if e["type"] == event_type]
    
    # Price filtering (convert ₹ strings to numbers)
    filtered = [e for e in filtered if extract_price(e["price"]) >= price_range[0] and extract_price(e["price"]) <= price_range[1]]
    
    return filtered

def extract_price(price_str):
    if "Free" in price_str:
        return 0
    # Extract number from ₹300 format
    import re
    numbers = re.findall(r'\d+', price_str)
    return int(numbers[0]) if numbers else 0

def get_venue_tip(venue):
    tips = {
        "Shaniwar Wada": "Best visited in evening, limited parking available",
        "FC Road": "Vibrant student area, try local street food",
        "Phoenix MarketCity": "Ample parking, good for family events",
        "Sinhagad Fort": "Carry water and wear good shoes for trekking"
    }
    return tips.get(venue, "")

def get_weather_compatibility(event):
    # Simulate weather compatibility based on event type
    outdoor_events = ["Outdoor Treks", "Food Festivals"]
    if event["type"] in outdoor_events:
        return random.randint(60, 85)  # Lower for outdoor events in current weather
    return random.randint(85, 100)  # Higher for indoor events

if __name__ == "__main__":
    main()