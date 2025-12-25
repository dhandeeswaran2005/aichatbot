## AICHATBOT USING WEB SCRAPING

An intelligent chatbot system that retrieves real-time information from websites using web scraping and AI-based natural language processing, enabling users to query data seamlessly and get instant, meaningful responses.

## About the Project

The AI-Driven Web Scraping Chatbot is designed to extract live information from the internet and present it in a conversational format. Unlike traditional search systems, this chatbot directly scrapes relevant websites, processes the data, and returns precise answers.

Conventional search engines may overwhelm users with unnecessary content or advertisements. This chatbot solves that problem by:

Extracting only required information

Structuring the data intelligently

Providing instant and accurate responses

Supporting flexible user queries

This system can scrape:

Product details & pricing

News & articles

Weather information

Reviews & ratings

Custom domain-specific data

It enables automation, intelligent assistance, and efficient data retrieval in a privacy-aware and scalable manner.

## Key Features

✔️ AI-powered chatbot interaction
✔️ Real-time web scraping capabilities
✔️ Supports multiple websites and domains
✔️ Clean text extraction & structured responses
✔️ Automated preprocessing, scraping, parsing, and response generation
✔️ Graphical or JSON outputs (optional)
✔️ Lightweight, scalable, and deployable on cloud or local environments
✔️ Error handling & fallback mechanisms

🏗️ System Architecture
User Query
     ↓
Chatbot Understanding (NLP / Rule-based)
     ↓
Web Scraping Module (Requests / BS4 / Selenium)
     ↓
Data Extraction
     ↓
Response Processing
     ↓
Chatbot Output to User

## Outputs
The home page of the AICHATBOT

<img width="1916" height="957" alt="Screenshot 2025-12-25 215006" src="https://github.com/user-attachments/assets/d6c82749-c551-49de-abde-bec39243b61c" />


The extracted information by web Scraping
<img width="1919" height="914" alt="Screenshot 2025-12-25 215036" src="https://github.com/user-attachments/assets/1355fef1-f169-4bd2-aac1-845afb5621ab" />


The final Scraped data
<img width="1919" height="912" alt="Screenshot 2025-12-25 215750" src="https://github.com/user-attachments/assets/6bba457a-577f-45e2-ab15-38ddd4813a6b" />




## Requirements
🔧 System Requirements

64-bit OS (Windows / Linux recommended)

## Programming

Python 3.6+

app.py
```
import pandas as pd
from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

# ------------ INVENTORY MANAGER -------------
class InventoryManager:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = self.load_data()

    def load_data(self):
        if not os.path.exists(self.file_path):
            print("Excel file not found!")
            return pd.DataFrame(columns=["Name", "Price", "Rating", "Link"])

        try:
            data = pd.read_excel(self.file_path)

            clean_cols = {}
            for c in data.columns:
                col = str(c).strip().lower().replace(" ", "")

                if "mobile" in col or "name" in col or "model" in col:
                    clean_cols[c] = "Name"
                elif "price" in col:
                    clean_cols[c] = "Price"
                elif "rating" in col:
                    clean_cols[c] = "Rating"
                elif "link" in col:
                    clean_cols[c] = "Link"

            data.rename(columns=clean_cols, inplace=True)

            # ---------- Clean ₹ Price ----------
            if "Price" in data.columns:
                data["Price"] = (
                    data["Price"]
                    .astype(str)
                    .str.replace("₹", "", regex=False)
                    .str.replace(",", "", regex=False)
                    .str.extract(r'(\d+\.?\d*)')[0]
                    .astype(float)
                )

            return data

        except Exception as e:
            print("Error reading excel:", e)
            return pd.DataFrame(columns=["Name", "Price", "Rating", "Link"])

    def get_suggestions(self, query):
        if self.df.empty:
            return pd.DataFrame()

        query = query.lower()

        # ---- Lowest price ----
        if "low" in query or "budget" in query or "cheap" in query:
            return self.df.sort_values(by="Price", ascending=True).head(5)

        # ---- Highest price / premium ----
        if "high" in query or "expensive" in query or "premium" in query:
            return self.df.sort_values(by="Price", ascending=False).head(5)

        # ---- Best Rating ----
        if "best" in query or "top" in query or "rating" in query:
            return self.df.sort_values(by="Rating", ascending=False).head(5)

        # ---- Brand Search ----
        brands = ["iphone", "samsung", "oppo", "vivo", "redmi", "realme", "oneplus", "nothing"]
        for b in brands:
            if b in query:
                return self.df[self.df["Name"].str.lower().str.contains(b)]

        # ---- Name Search ----
        words = query.split()
        return self.df[self.df["Name"].str.lower().str.contains("|".join(words))]


manager = InventoryManager("phones.xlsx")


# ------------ ROUTES -------------
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/ask", methods=["POST"])
def ask():
    user_message = request.json.get("message", "")

    if not user_message:
        return jsonify({"reply": "Please type something!"})

    df = manager.get_suggestions(user_message)

    if df.empty:
        return jsonify({"reply": "No matching phones found in Excel!"})

    # ---------- Clickable Link ----------
    if "Link" in df.columns:
        df["Link"] = df["Link"].apply(
            lambda x: f'<a href="{x}" target="_blank" class="btn btn-warning btn-sm">Open</a>'
            if pd.notna(x) and str(x).strip() != "" else ""
        )

    table = df.to_html(
        classes="table table-dark table-hover table-bordered",
        index=False,
        escape=False
    )

    reply = f"<b>Here are the best results Sir 😎:</b><br><br>{table}"
    return jsonify({"reply": reply})


if __name__ == "__main__":
    app.run(debug=True, port=5000)

```


index.html
```
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>MR SCRAPPER</title>

<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">

<style>
body {
    margin: 0;
    font-family: 'Segoe UI', sans-serif;
    height: 100vh;
    background: linear-gradient(-45deg, #1f1c2c, #928dab, #1f4037, #99f2c8);
    background-size: 400% 400%;
    animation: gradientBG 15s ease infinite;
    display: flex;
    align-items: center;
    justify-content: center;
}
@keyframes gradientBG {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

.chat-card {
    width: 90%;
    max-width: 800px;
    background: rgba(0,0,0,0.85);
    border-radius: 25px;
    box-shadow: 0 8px 50px rgba(0,0,0,0.7);
    display: flex;
    flex-direction: column;
    overflow: hidden;
    border: 2px solid rgba(255,255,255,0.3);
    animation: popIn 1s ease;
}
@keyframes popIn {
    0% { transform: scale(0.8); opacity: 0; }
    100% { transform: scale(1); opacity: 1; }
}

.card-header {
    background: linear-gradient(90deg, #ff6a00, #ee0979);
    color: white;
    text-align: center;
    font-weight: bold;
    font-size: 1.5rem;
    padding: 15px;
}

#chat-display {
    flex: 1;
    padding: 20px;
    overflow-y: auto;
    background: rgba(255,255,255,0.05);
}

.msg {
    margin-bottom: 20px;
    padding: 15px 25px;
    border-radius: 30px;
    max-width: 75%;
    position: relative;
    opacity: 0;
    animation: fadeIn 0.5s forwards, bounce 0.5s forwards;
    font-weight: 500;
    box-shadow: 0 0 15px rgba(0,0,0,0.4);
}

.bot-msg {
    background: linear-gradient(135deg, #ff6a00, #ee0979);
    color: #fff;
    float: left;
    clear: both;
}

.user-msg {
    background: linear-gradient(135deg, #0d6efd, #00c6ff);
    color: #fff;
    float: right;
    clear: both;
}

@keyframes fadeIn { to { opacity: 1; } }
@keyframes bounce {
    0% { transform: translateY(-10px); }
    50% { transform: translateY(3px); }
    100% { transform: translateY(0); }
}

.input-group {
    padding: 15px;
    background: rgba(0,0,0,0.9);
}

.btn {
    border-radius: 0 25px 25px 0;
    background: linear-gradient(90deg, #ff6a00, #ee0979);
    font-weight: bold;
}
</style>
</head>

<body>
<div class="chat-card">
    <div class="card-header">MR SCRAPPER – Phone AI</div>

    <div id="chat-display">
        <div class="msg bot-msg">
            MR SCRAPPER Connected to <b>phones.xlsx</b> ✔️<br>
            Try:
            <br>• low price mobiles
            <br>• best rating
            <br>• samsung / iphone
        </div>
    </div>

    <div class="input-group">
        <input id="user-input" class="form-control" placeholder="Type your query...">
        <button class="btn" onclick="handleSend()">Send</button>
    </div>
</div>

<script>
const display = document.getElementById("chat-display");
const input = document.getElementById("user-input");

async function handleSend() {
    const text = input.value.trim();
    if (!text) return;

    let userDiv = document.createElement("div");
    userDiv.className = "msg user-msg";
    userDiv.innerText = text;
    display.appendChild(userDiv);
    input.value = "";
    display.scrollTop = display.scrollHeight;

    try {
        const res = await fetch("/ask", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: text })
        });

        const data = await res.json();

        let botDiv = document.createElement("div");
        botDiv.className = "msg bot-msg w-100";
        botDiv.innerHTML = data.reply;
        display.appendChild(botDiv);
        display.scrollTop = display.scrollHeight;

        if ('speechSynthesis' in window) {
            let speech = new SpeechSynthesisUtterance("Here are the best results sir");
            speech.rate = 1;
            window.speechSynthesis.speak(speech);
        }

    } catch {
        let botDiv = document.createElement("div");
        botDiv.className = "msg bot-msg";
        botDiv.innerText = "⚠️ Error connecting to server.";
        display.appendChild(botDiv);
    }
}

input.addEventListener("keypress", e => {
    if (e.key === "Enter") handleSend();
});
</script>
</body>
</html>

```



## Libraries & Frameworks

Requests / Selenium / BeautifulSoup

Flask / Django (for chatbot interface)

NLTK / Transformers (optional for NLP)

Pandas

JSON handling modules

🔗 Development Tools

Git (Version Control)

Google Colab / Jupyter / VS Code

## References

Web Scraping Documentation (BeautifulSoup / Selenium)

NLP & Chatbot Architecture Studies

AI-based conversational systems research papers
