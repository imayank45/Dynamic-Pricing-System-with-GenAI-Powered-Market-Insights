from flask import Flask, render_template, request, jsonify
import requests
import yaml
from src.utils.logger import setup_logger

app = Flask(__name__)
logger = setup_logger("config/config.yaml")

with open("config/config.yaml", "r") as file:
    config = yaml.safe_load(file)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            data = {
                "product_id": request.form["product_id"],
                "unit_price": float(request.form["unit_price"]),
                "comp_1": float(request.form["comp_1"]),
                "comp_2": float(request.form["comp_2"]),
                "comp_3": float(request.form["comp_3"]),
                "qty": int(request.form["qty"]),
                "product_category_name": request.form["product_category_name"],
                "product_score": float(request.form["product_score"]),
                "volume": float(request.form["volume"]),
                "lag_price": float(request.form["lag_price"])
            }
            logger.info(f"Processing request for product: {data['product_id']}")
            
            # Call APIs
            price_response = requests.post(
                f"http://{config['api']['host']}:{config['api']['port']}/predict_price",
                json=data
            ).json()
            insights_response = requests.post(
                f"http://{config['api']['host']}:{config['api']['port']}/generate_insights",
                json=data
            ).json()
            
            return render_template(
                "index.html",
                result={
                    "recommended_price": price_response["recommended_price"],
                    "insights": insights_response["insights"]
                }
            )
        except Exception as e:
            logger.error(f"Frontend request failed: {str(e)}")
            return render_template("index.html", error=str(e))
    
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host=config["frontend"]["host"], port=config["frontend"]["port"])