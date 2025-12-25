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
