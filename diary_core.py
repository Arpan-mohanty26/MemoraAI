import os
import json
import re
from datetime import datetime, timedelta
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

DATA_PATH = "data/entries.json"

# Safety keywords that indicate concerning content
SAFETY_KEYWORDS = [
    'suicide', 'kill myself', 'end it all', 'want to die', 'hurt myself',
    'kill others', 'hurt people', 'destroy everything', 'violence'
]

def load_entries():
    """Load diary entries from JSON file"""
    if not os.path.exists(DATA_PATH):
        return {}
    try:
        with open(DATA_PATH, "r") as f:
            content = f.read().strip()
            if not content:
                return {}
            return json.loads(content)
    except json.JSONDecodeError:
        return {}

def save_entry(text):
    """Save a diary entry with timestamp"""
    os.makedirs("data", exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d")
    data = load_entries()
    data[today] = text
    with open(DATA_PATH, "w") as f:
        json.dump(data, f, indent=2)

def check_safety_concerns(text):
    """Check for concerning content in the entry"""
    text_lower = text.lower()
    for keyword in SAFETY_KEYWORDS:
        if keyword in text_lower:
            return True
    return False

def reflect_on_entry(text):
    """Generate AI reflection on diary entry with safety checks"""
    
    # Safety check
    if check_safety_concerns(text):
        return """SAFETY_CONCERN: I notice some concerning thoughts in your entry. 
        
It's important to know that you're not alone, and there are people who want to help. Please consider:
- Talking to a trusted friend, family member, or counselor
- Contacting a mental health professional
- Reaching out to a crisis helpline

Your feelings are valid, but there are healthier ways to work through difficult times."""

    prompt = f"""
You are an empathetic diary assistant. Analyze this journal entry and provide a concise, supportive response with:

1. **Summary** (1-2 sentences): Brief overview of what happened
2. **Mood** (1 word + brief explanation): Current emotional state  
3. **Insight** (1-2 sentences): A gentle observation or pattern you notice
4. **Question** (1 question): A thoughtful follow-up to encourage deeper reflection

Keep your response warm, concise, and under 150 words total.

Entry: "{text}"

Format your response clearly with emojis and be encouraging.
"""
    
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"I'm having trouble processing your entry right now. Please try again later. 🤖💭"

def analyze_mood_trends(entries):
    """Analyze mood trends from recent entries"""
    if len(entries) < 3:
        return None
    
    # Get last 7 days of entries
    recent_entries = {}
    current_date = datetime.now().date()
    
    for i in range(7):
        check_date = current_date - timedelta(days=i)
        date_str = check_date.strftime("%Y-%m-%d")
        if date_str in entries:
            recent_entries[date_str] = entries[date_str]
    
    if not recent_entries:
        return None
    
    # Simple mood scoring based on positive/negative words
    positive_words = ['happy', 'good', 'great', 'amazing', 'wonderful', 'excited', 'joy', 'love', 'grateful', 'blessed', 'accomplished', 'proud']
    negative_words = ['sad', 'bad', 'terrible', 'awful', 'depressed', 'angry', 'frustrated', 'worried', 'anxious', 'stressed', 'disappointed', 'tired']
    
    mood_scores = {}
    for date, text in recent_entries.items():
        text_lower = text.lower()
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        # Simple scoring: positive words add points, negative subtract
        score = positive_count - negative_count + 5  # +5 to keep scores positive
        mood_scores[date] = max(0, min(10, score))  # Clamp between 0-10
    
    return mood_scores

def get_writing_prompt():
    """Generate a random writing prompt for inspiration"""
    prompts = [
        "What made you smile today?",
        "Describe a moment when you felt proud of yourself.",
        "What are you most grateful for right now?",
        "If you could give advice to your past self, what would it be?",
        "What's something new you learned recently?",
        "Describe your ideal day from start to finish.",
        "What challenge are you currently working through?",
        "What does success mean to you?",
        "Who has had a positive impact on your life recently?",
        "What are you looking forward to?"
    ]
    
    import random
    return random.choice(prompts)

def export_entries_to_text():
    """Export all entries to a formatted text file"""
    entries = load_entries()
    if not entries:
        return None
    
    export_content = "# My Journal Entries\n\n"
    for date, text in sorted(entries.items()):
        export_content += f"## {date}\n\n{text}\n\n---\n\n"
    
    export_path = f"data/journal_export_{datetime.now().strftime('%Y%m%d')}.txt"
    with open(export_path, "w") as f:
        f.write(export_content)
    
    return export_path