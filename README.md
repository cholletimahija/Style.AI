
# StyleAI – AI Based Fashion Recommendation System

## Description
StyleAI is an AI-powered web application that provides personalized outfit suggestions based on user image, skin tone, gender, and occasion.

## Technologies Used
- Python
- Flask
- Pillow
- NumPy
- Groq API (LLaMA 3 Model)
- HTML & CSS

## How It Works
1. User uploads image
2. Skin tone is detected using brightness analysis
3. Gender & occasion selected
4. AI generates personalized outfit suggestions
5. Structured output displayed
6. Direct shopping links provided

## Setup Instructions
1. Clone the repository
2. Install requirements:
   pip install -r requirements.txt
3. Create .env file and add:
   GROQ_API_KEY=your_api_key
4. Run:
   python app.py
5. Open browser at:
   http://127.0.0.1:5000

## Future Improvements
- Body type detection
- Color palette extraction
- Virtual try-on system
- Cloud deployment
