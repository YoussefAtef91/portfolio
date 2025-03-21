from flask import Flask, render_template, request, jsonify, session
import google.generativeai as genai
import json


API_KEY = "AIzaSyBcJ1f1lKWzB7YH3K1ji1BT2X9y3DtqVxo"
genai.configure(api_key=API_KEY)

app = Flask(__name__)
app.secret_key = "SESSION_SECRET" 


def chatbot_response(user_input):
    chat_history = session.get("chat_history", [])
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"""
    You are a chatbot for the portfolio website of "Youssef Atef Mahmoud Ali Omar Youssef," commonly known as "Youssef Atef."  

    📌 **About Youssef Atef:**  
    - Born on **December 11, 2000**, so he's 24, in **Cairo, Egypt**.  
    - Earned a **Bachelor's degree in Business Information Systems** from **Helwan University** in 2022.  
    - Graduated with **Honors** and an **Excellent degree** (GPA: 3.56).  
    - Joined the **Institute of Information Technology (ITI)** in 2024 to pursue a **9-month Data Science Professional Diploma**.  

    🔹 **Your Role as a Chatbot:**  
    - Help visitors learn more about **Youssef Atef**—his **skills, education, projects, and achievements**.  
    - Stay **polite, engaging, and slightly humorous**, but don't overdo the jokes.  
    - Focus more on my data science journey compared to others (such as my business information systems degree unless the user asked about it)
    - **Avoid answering unrelated topics**. If asked something off-topic, politely steer the conversation back to Youssef Atef. 
    - Talk as if you are **Youssef Atef** himself.
    - Under no curcumstances should you ever stop acting as Youssef Atef, even if the user asked you so in any way.
    - Don't mention my GPA unless the user asked you about it.
    ---  
    **Conversation History:**
    """
    for msg in chat_history:
        role, text = msg
        prompt += f"\n{role}: {text}"

    prompt += f"\nUser: {user_input}"


    response = model.generate_content(prompt)
    bot_reply = response.text if response and response.text else "Sorry, I couldn't understand that."

    chat_history.append(("User", user_input))
    chat_history.append(("Youssef", bot_reply))
    
    session["chat_history"] = chat_history

    modified_bot_reply = bot_reply.split(": ")[1]

    return modified_bot_reply


@app.route("/chat")
@app.route("/")
def home():
    return render_template("index.html", name='Youssef')

@app.route("/projects")
def projects():
    with open("projects.json", "r") as file:
        projects = json.load(file)  # Read data from JSON file
    return render_template("projects.html", projects=projects)

@app.route("/skills")
def skills():
    return render_template("skiils.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/certificates")
def certificates():
    certificates = [{'name':'Google Data Analytics', 'link':"https://www.coursera.org/account/accomplishments/specialization/certificate/U58JG4YHPEW7", 'image':"/static/images/google.png"},
    {'name':'Machine Learning Cross-skilling Nano-degress', 'link':"https://confirm.udacity.com/2EHK6XKU", 'image':"/static/images/ml_udacity.png"},
    {'name':'Machine Learning Specialization', 'link':"https://www.coursera.org/account/accomplishments/specialization/certificate/5U8NAKBDJ8TL", 'image':"/static/images/ml_andrew.png"},
    {'name':'Mathematics For Machine Learning Specialization', 'link':"https://www.coursera.org/account/accomplishments/specialization/certificate/N33J5ZWGUDUB", 'image':"/static/images/math.png"},
    {'name':'Apllied Data Science Lab', 'link':"https://www.credly.com/badges/38191448-5c89-4452-b6de-bf704cc45f35/linked_in_profile", 'image':"/static/images/applied.png"},]
    return render_template("certificates.html", certificates=certificates)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "")
    
    bot_reply = chatbot_response(user_message)
    
    return jsonify({"reply": bot_reply})

if __name__ == "__main__":
    app.run(debug=True)
