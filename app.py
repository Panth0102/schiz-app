from flask import Flask, render_template, request, session, make_response
import joblib
import numpy as np
import os
# Simple chatbot responses instead of ChatterBot
import random
# Removed PDF dependencies for now

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'panth_sutaria_8320829286_psmsssks')

# Load trained ML model and scaler
try:
    model = joblib.load("schiz_model.pkl")
    scaler = joblib.load("scaler.pkl")
    print("Models loaded successfully")
except Exception as e:
    print(f"Error loading models: {e}")
    model = None
    scaler = None

# Simple chatbot responses
def get_bot_response(user_input):
    responses = [
        "I understand how you're feeling. Can you tell me more about that?",
        "That sounds challenging. How are you coping with this?",
        "Thank you for sharing. What emotions are you experiencing right now?",
        "I'm here to listen. How has your day been overall?",
        "It's important to acknowledge these feelings. Have you noticed any patterns?",
        "Your feelings are valid. What helps you feel better in these moments?",
        "I appreciate you opening up. How can I support you today?",
        "That's a lot to process. What would be most helpful right now?",
        "I hear you. Have you been able to talk to anyone else about this?",
        "Thank you for trusting me with this. How are you taking care of yourself?"
    ]
    return random.choice(responses)

# ----------------
# Health Check
# ----------------
@app.route("/health")
def health():
    return {"status": "healthy", "models_loaded": model is not None}

# ----------------
# Home Page
# ----------------
@app.route("/")
def home():
    return render_template("index.html")

# ----------------
# About Page
# ----------------
@app.route("/about")
def about():
    return render_template("about.html")

# ----------------
# Prediction Page
# ----------------
@app.route("/predict", methods=["GET", "POST"])
def predict():
    prediction = None
    if request.method == "POST":
        try:
            if model is None or scaler is None:
                prediction = "Model not available. Please contact administrator."
            else:
                age = float(request.form["age"])
                yrschool = int(request.form["yrschool"])
                gender = int(request.form["gender"])
                q1 = float(request.form["q1"])
                q2 = float(request.form["q2"])
                q3 = float(request.form["q3"])
                q4 = float(request.form["q4"])

                features = np.array([[age, yrschool, gender, q1, q2, q3, q4]])
                features_scaled = scaler.transform(features)
                pred = model.predict(features_scaled)[0]
                prediction = "Schizophrenia" if pred == 1 else "Sibling (no schizophrenia)"
                session["prediction"] = prediction
        except Exception as e:
            prediction = f"Error: {str(e)}"

    return render_template("predict.html", prediction=prediction)

# ----------------
# Chatbot Page
# ----------------
@app.route("/chatbot", methods=["GET", "POST"])
def chatbot():
    if request.method == "GET":
        session["chat_history"] = []
        session["mood"] = "neutral"

    if "chat_history" not in session:
        session["chat_history"] = []

    mood = session.get("mood", "neutral")

    if request.method == "POST":
        if "mood" in request.form:
            mood = request.form["mood"]
            session["mood"] = mood
        else:
            user_input = request.form["message"]
            bot_response = get_bot_response(user_input)
            session["chat_history"].append(("You", user_input))
            session["chat_history"].append(("Bot", bot_response))
            session.modified = True

    return render_template("chatbot.html", history=session["chat_history"], mood=mood)

# ----------------
# Journal Page
# ----------------
@app.route("/journal", methods=["GET", "POST"])
def journal():
    if "journal" not in session:
        session["journal"] = []

    if request.method == "POST":
        entry = request.form["entry"]
        if entry.strip():
            session["journal"].append(entry.strip())
            session.modified = True

    return render_template("journal.html", entries=session["journal"])

# ----------------
# Session Summary (Text version)
# ----------------
@app.route("/session/download")
def download_session():
    journal = session.get("journal", [])
    chat_history = session.get("chat_history", [])
    prediction = session.get("prediction", "No prediction made yet")
    
    # Create a simple text summary
    summary = f"""
SESSION SUMMARY
===============

PREDICTION RESULT:
{prediction}

JOURNAL ENTRIES ({len(journal)} entries):
"""
    for i, entry in enumerate(journal, 1):
        summary += f"{i}. {entry}\n"
    
    summary += f"\nCHAT HISTORY ({len(chat_history)} messages):\n"
    for speaker, message in chat_history:
        summary += f"{speaker}: {message}\n"
    
    response = make_response(summary)
    response.headers["Content-Type"] = "text/plain"
    response.headers["Content-Disposition"] = "attachment; filename=session_report.txt"
    return response

# ----------------
# Run the app
# ----------------
import os

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug_mode)



# from flask import Flask, render_template, request, session

# import joblib
# import numpy as np
# from chatterbot import ChatBot
# from chatterbot.trainers import ChatterBotCorpusTrainer


# app = Flask(__name__)
# app.secret_key = "your_secret_key"  # needed for session

# model = joblib.load("schiz_model.pkl")
# scaler = joblib.load("scaler.pkl")

# @app.route("/")
# def home():
#     return render_template("index.html")

# @app.route("/about")
# def about():
#     return render_template("about.html")

# @app.route("/predict", methods=["GET", "POST"])
# def predict():
#     prediction = None
#     if request.method == "POST":
#         try:
#             age = float(request.form["age"])
#             yrschool = int(request.form["yrschool"])
#             gender = int(request.form["gender"])
#             saps7 = float(request.form["saps7"])
#             saps20 = float(request.form["saps20"])
#             saps25 = float(request.form["saps25"])
#             saps34 = float(request.form["saps34"])

#             features = np.array([[age, yrschool, gender, saps7, saps20, saps25, saps34]])
#             features_scaled = scaler.transform(features)

#             pred = model.predict(features_scaled)[0]
#             prediction = "Schizophrenia" if pred == 1 else "Sibling (no schizophrenia)"
#         except Exception as e:
#             prediction = f"Error: {str(e)}"
#     return render_template("predict.html", prediction=prediction)


# schizo_bot = ChatBot("SchizoBot")
# trainer = ChatterBotCorpusTrainer(schizo_bot)
# trainer.train("chatterbot.corpus.english") 

# @app.route("/chatbot", methods=["GET", "POST"])
# def chatbot():
#     if request.method == "GET":
#         session["history"] = []    # reset chat history when user reopens
#         session["mood"] = "neutral"  # optional: reset mood if you want

#     if "history" not in session:
#         session["history"] = []

#     mood = session.get("mood", "neutral")

#     if request.method == "POST":
#         if "mood" in request.form:
#             mood = request.form["mood"]
#             session["mood"] = mood
#         else:
#             user_input = request.form["message"]
#             bot_response = schizo_bot.get_response(user_input)
#             session["history"].append(("You", user_input))
#             session["history"].append(("Bot", str(bot_response)))
#             session.modified = True

#     return render_template("chatbot.html", history=session.get("history", []), mood=mood)



# # in-memory journal storage
# journal_entries = []

# @app.route("/journal", methods=["GET", "POST"])
# def journal():
#     if request.method == "POST":
#         entry = request.form["entry"]
#         if entry.strip():
#             journal_entries.append(entry.strip())
#     return render_template("journal.html", entries=journal_entries)


# if __name__ == "__main__":
#     app.run(debug=True)