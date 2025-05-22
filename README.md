Dynamic Pricing System with GenAI-Powered Market Insights 🚀
Welcome to the Dynamic Pricing System, a cutting-edge solution that optimizes product prices in real-time using advanced Reinforcement Learning (PPO) and generates actionable market insights with GPT-4. Deployed on Azure, this project showcases a scalable, modular, and production-ready system designed to maximize revenue for retail businesses. Built with PEP 8 standards and modern tech stacks, it’s a perfect blend of machine learning, generative AI, and cloud engineering! 💻✨

🌟 Project Overview
This project creates a real-time pricing engine that dynamically adjusts product prices based on demand, competitor prices, and market trends. It leverages the Kaggle Retail Price Optimization dataset and integrates:

Proximal Policy Optimization (PPO) for optimal pricing decisions.
GPT-4 for generating human-readable market insights (e.g., "Raise prices due to high demand in Electronics").
A sleek Flask frontend with modern HTML/CSS for user interaction.
Azure for scalable cloud deployment, ensuring accessibility via a public URL.

The system is modular, with separate pipelines for data ingestion, preprocessing, modeling, insights generation, APIs, and frontend, all communicating seamlessly. Comprehensive logging and unit tests ensure robustness. 📊🔍

🎯 Objectives

Optimize Pricing: Use PPO to set prices that maximize profit based on demand and competition.
Provide Insights: Leverage GPT-4 to explain pricing decisions in plain English.
User-Friendly Interface: Offer a modern Flask dashboard for price predictions and insights.
Scalable Deployment: Host on Azure Kubernetes Service (AKS) for production-grade performance.


🛠️ Technologies Used



Category
Tools



Programming
Python 3.11 🐍, HTML, CSS


Data Processing
PySpark, Delta Lake, Pandas, NumPy


Machine Learning
Ray RLlib (PPO), Torch


Generative AI
GPT-4 (via API for market insights)


Backend
FastAPI, Flask, Uvicorn


Frontend
Flask, HTML5, CSS3 (custom modern design)


Cloud
Azure (Blob Storage, Databricks, AKS, Container Registry)


DevOps
Docker 🐳, Kubernetes, Azure CLI


Monitoring
Python logging, Azure Monitor


Testing
Pytest


Others
YAML, Prometheus, Git, GitHub



📂 Project Structure
The project follows a modular, organized structure for maintainability and scalability:
dynamic_pricing/
├── config/                     # Configuration files 📋
│   └── config.yaml             # Azure, model, and API settings
├── src/                        # Core pipelines 🛠️
│   ├── ingestion/              # Data ingestion pipeline
│   │   └── ingest.py           # Loads dataset into Delta Lake
│   ├── preprocessing/          # Feature engineering
│   │   └── preprocess.py       # FastAPI service for feature extraction
│   ├── model/                  # PPO pricing model
│   │   └── pricing_model.py    # Trains PPO with Ray RLlib
│   ├── genai/                  # GPT-4 insights
│   │   └── insights.py         # Generates market insights
│   ├── api/                    # API service
│   │   └── serve.py            # FastAPI endpoints for pricing and insights
│   ├── utils/                  # Utilities
│   │   └── logger.py           # Logging setup
├── frontend/                   # Flask frontend 🎨
│   ├── app.py                  # Flask application
│   ├── templates/              # HTML templates
│   │   └── index.html          # Main dashboard
│   ├── static/                 # Static assets
│   │   └── css/
│   │       └── style.css       # Modern CSS styling
├── tests/                      # Unit tests 🧪
│   └── test_preprocess.py      # Tests for preprocessing
├── kubernetes/                 # Kubernetes deployment
│   └── deployment.yaml         # AKS configuration
├── Dockerfile                  # Docker configuration 🐳
├── requirements.txt            # Dependencies
├── setup.py                    # Project setup
├── run.py                      # End-to-end pipeline script
└── README.md                   # Project documentation 📖


📊 Dataset
The project uses the Kaggle Retail Price Optimization dataset with the following key columns:

product_id: Unique product identifier.
unit_price: Current product price.
comp_1, comp_2, comp_3: Competitor prices.
qty: Quantity sold (demand indicator).
product_category_name: Product category.
product_score: Customer rating.
volume: Product size.
lag_price: Previous price.
month_year: Time of sales.

Derived Features (via preprocessing):

price_gap: Difference between unit_price and average competitor price.
normalized_price: Scaled price (unit_price / max_price).
demand_signal: Scaled demand (qty / max_qty).
price_trend: Price change (unit_price - lag_price).

These features feed into the PPO model for pricing and GPT-4 for insights. 📈

🧠 Key Components
1. Data Ingestion 📥

Tool: PySpark with Delta Lake.
Process: Loads the dataset from Azure Blob Storage into a Delta table, selecting relevant columns.
File: src/ingestion/ingest.py

2. Preprocessing ⚙️

Tool: FastAPI microservice.
Process: Engineers features like price_gap and demand_signal for the PPO model.
File: src/preprocessing/preprocess.py

3. Pricing Model (PPO) 🤖

Tool: Ray RLlib with Proximal Policy Optimization (PPO).
Process: Trains a PPO model to optimize prices:
State: [price_gap, normalized_price, demand_signal, price_trend, product_score]
Action: Price adjustment (e.g., -10% to +10%).
Reward: Profit (qty * (unit_price - cost); cost = 70% of unit_price).


File: src/model/pricing_model.py

4. Market Insights (GPT-4) 💡

Tool: GPT-4 via API.
Process: Generates human-readable insights based on pricing features and PPO output (e.g., "Increase price due to high demand").
File: src/genai/insights.py

5. API Service 🌐

Tool: FastAPI with Ray Serve.
Process: Exposes endpoints for price prediction (/predict_price) and insights (/generate_insights).
File: src/api/serve.py

6. Frontend 🎨

Tool: Flask with HTML5/CSS3.
Process: Provides a modern, responsive dashboard for users to input product details and view recommended prices and insights.
Files: frontend/app.py, frontend/templates/index.html, frontend/static/css/style.css

7. End-to-End Pipeline 🚀

Tool: Python script with subprocess.
Process: Orchestrates all pipelines (ingestion, preprocessing, model training, insights, API, frontend).
File: run.py


☁️ Azure Deployment
The system is deployed on Azure for scalability and accessibility:

Azure Blob Storage: Stores the dataset and Delta tables.
Azure Databricks: Trains the PPO model and fine-tunes GPT-4 prompts.
Azure Container Registry (ACR): Hosts the Docker image.
Azure Kubernetes Service (AKS): Runs the FastAPI and Flask services with a public URL.
Public URL: http://<EXTERNAL-IP>:5000 (Flask dashboard).
API Endpoints: http://<EXTERNAL-IP>:8000/predict_price, http://<EXTERNAL-IP>:8000/generate_insights.



Deployment Steps:

Build Docker image: docker build -t <your-acr>.azurecr.io/dynamic-pricing:latest .
Push to ACR: docker push <your-acr>.azurecr.io/dynamic-pricing:latest
Deploy to AKS: kubectl apply -f kubernetes/deployment.yaml
Get public IP: kubectl get services


🚀 How It Works

User Input:

Via the Flask dashboard, users enter:
product_id (e.g., "123")
unit_price (e.g., $100)
comp_1, comp_2, comp_3 (e.g., $95, $97, $93)
qty (e.g., 50)
product_category_name (e.g., "Electronics")
product_score (e.g., 4.5)
volume (e.g., 100)
lag_price (e.g., $98)




Processing:

Preprocessing: Generates features like price_gap and demand_signal.
PPO Model: Recommends an optimal price (e.g., $110).
GPT-4: Generates insights (e.g., "Increase price due to high demand in Electronics").


Output:

The dashboard displays:
Recommended Price: $110
Market Insights: "Increase price due to high demand in Electronics"






🧪 Testing

Unit Tests: Pytest scripts validate the preprocessing pipeline.
File: tests/test_preprocess.py
Run: pytest tests/test_preprocess.py


📜 Setup Instructions

Clone Repository:
git clone <your-repo-url>
cd dynamic_pricing


Install Dependencies:
pip install -r requirements.txt


Configure Azure:

Set up Blob Storage, Databricks, ACR, and AKS.
Update config/config.yaml with your Azure credentials.


Upload Dataset:

Place retail_data.csv in Azure Blob Storage (retail-data/data/).


Run Locally:
python run.py


Access frontend: http://localhost:5000
Access APIs: http://localhost:8000/predict_price


Deploy to Azure:

Follow the deployment steps above.




🌈 Why This Project Stands Out

Advanced AI: Combines PPO for pricing and GPT-4 for insights, aligning with FAANG-level tech stacks.
Scalable Architecture: Modular pipelines with microservices and cloud deployment.
User-Centric Design: Modern Flask frontend with a sleek, responsive UI.
Production-Ready: Dockerized, Kubernetes-deployed, and monitored with logs.
Business Impact: Optimizes revenue through dynamic pricing and clear insights.

This project demonstrates expertise in machine learning, generative AI, cloud engineering, and full-stack development, making it a powerful portfolio piece! 🚀

🛠️ Future Enhancements

Real-Time Data: Integrate live sales and competitor data via APIs.
Advanced Insights: Fine-tune GPT-4 with a larger retail dataset.
Authentication: Add user login to the Flask dashboard.
Monitoring: Integrate Prometheus and Grafana for real-time metrics.


📬 Contact
Feel free to reach out for collaboration or questions:

GitHub: [Your GitHub Profile]
Email: [Your Email]
LinkedIn: [Your LinkedIn Profile]


Built with 💖 by [Your Name] to revolutionize retail pricing!
