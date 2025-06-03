# Dynamic Pricing System with GenAI-Powered Market Insights 🚀

Welcome to the **Dynamic Pricing System**, a cutting-edge solution that optimizes product prices in real-time using advanced Reinforcement Learning (PPO) and generates actionable market insights with GPT-4. Deployed on Azure, this project showcases a scalable, modular, and production-ready system designed to maximize revenue for retail businesses.

--- 

## 🌟 Project Overview 

This project creates a real-time pricing engine that dynamically adjusts product prices based on demand, competitor prices, and market trends. It integrates:
 
* **Proximal Policy Optimization (PPO)** for pricing decisions
* **GPT-4** for generating plain-language market insights
* **Flask frontend** for a sleek dashboard interface
* **Azure cloud** for scalable deployment

The architecture is modular with well-separated pipelines for ingestion, processing, modeling, insight generation, API service, and frontend.
 
--- 

## 🎯 Objectives 

* **Optimize Pricing**: Use PPO to maximize profit based on real-world signals
* **Generate Insights**: Leverage GPT-4 to provide human-readable pricing recommendations
* **User-Friendly Interface**: Provide a modern dashboard for interaction
* **Scalable Deployment**: Host using Azure Kubernetes Service (AKS)

---

## 🛠️ Technologies Used

| Category         | Tools                                                     |
| ---------------- | --------------------------------------------------------- |
| Programming      | Python 3.11 🐍, HTML5, CSS3                               |
| Data Processing  | PySpark, Delta Lake, Pandas, NumPy                        |
| Machine Learning | Ray RLlib (PPO), Torch                                    |
| Generative AI    | GPT-4 (via API)                                           |
| Backend          | FastAPI, Flask, Uvicorn                                   |
| Frontend         | Flask, HTML5, CSS3 (custom styling)                       |
| Cloud            | Azure (Blob Storage, Databricks, AKS, Container Registry) |
| DevOps           | Docker 🐳, Kubernetes, Azure CLI                          |
| Monitoring       | Python logging, Azure Monitor                             |
| Testing          | Pytest                                                    |
| Others           | YAML, Git, GitHub                                         |

---

## 📂 Project Structure

Note: Few files have been added to .gitignore in order to hide connection_strings and other secure tokens

```plaintext
dynamic_pricing/
├── config/
│   └── config.yaml              # Azure, model, and API settings
├── src/
│   ├── ingestion/
│   │   └── ingest.py            # Loads dataset
│   ├── preprocessing/
│   │   └── preprocess.py        # Feature engineering
│   ├── model/
│   │   └── pricing_model.py     # PPO pricing model
│   ├── genai/
│   │   └── insights.py          # GPT-4 insight generation
│   ├── api/
│   │   └── serve.py             # FastAPI endpoints
│   ├── utils/
│   │   └── logger.py            # Logging setup
├── frontend/
│   ├── app.py
│   ├── templates/
│   │   └── index.html           # Dashboard
│   ├── static/css/
│       └── style.css            # Styling
├── tests/
│   └── test_preprocess.py       # Unit tests
├── kubernetes/
│   └── deployment.yaml          # AKS deployment config
├── Dockerfile
├── requirements.txt
├── setup.py
├── run.py                       # Pipeline runner
└── README.md
```

---

## 📊 Dataset

Uses Kaggle's Retail Price Optimization dataset:

* **Core Columns**: `product_id`, `unit_price`, `comp_1`, `qty`, `product_category_name`, `product_score`, etc.
* **Derived Features**: `price_gap`, `normalized_price`, `demand_signal`, `price_trend`

---

## 🧠 Key Components

### 1. Data Ingestion 📥

* **Tool**: PySpark + Delta Lake
* **File**: `src/ingestion/ingest.py`

### 2. Preprocessing ⚙️

* **Tool**: FastAPI
* **File**: `src/preprocessing/preprocess.py`

### 3. Pricing Model (PPO) 🤖

* **Tool**: Ray RLlib
* **File**: `src/model/pricing_model.py`

### 4. Market Insights (GPT-4) 💡

* **Tool**: GPT-4 API
* **File**: `src/genai/insights.py`

### 5. API Service 🌐

* **Tool**: FastAPI
* **File**: `src/api/serve.py`

### 6. Frontend 🎨

* **Tool**: Flask
* **Files**: `frontend/app.py`, `frontend/templates/index.html`, `frontend/static/css/style.css`

### 7. End-to-End Pipeline 🚀

* **File**: `run.py`

---

## ☁️ Azure Deployment

### Services Used:

* Azure Blob Storage, Databricks, ACR, AKS

### Public Access:

* Flask Dashboard: `http://<EXTERNAL-IP>:5000`
* APIs: `/predict_price`, `/generate_insights`

### Deployment Steps:

```bash
docker build -t <your-acr>.azurecr.io/dynamic-pricing:latest .
docker push <your-acr>.azurecr.io/dynamic-pricing:latest
kubectl apply -f kubernetes/deployment.yaml
kubectl get services  # to get external IP
```

---

## 🚀 How It Works

### Input via Dashboard:

* `product_id`, `unit_price`, `comp_1`, `qty`, etc.

### Processing:

* **Preprocessing**: Feature generation
* **PPO Model**: Price recommendation
* **GPT-4**: Insight generation

### Output:

* Recommended Price (e.g., `$110`)
* Market Insight (e.g., *"Increase price due to high demand"*)

---

## 🧪 Testing

* **Tool**: Pytest
* **File**: `tests/test_preprocess.py`
* **Command**: `pytest tests/test_preprocess.py`

---

## 📜 Setup Instructions

### Clone & Install:

```bash
git clone <your-repo-url>
cd dynamic_pricing
pip install -r requirements.txt
```

### Configure Azure:

* Update `config/config.yaml`

### Upload Dataset:

* Upload `retail_data.csv` to Blob Storage (`retail-data/data/`)

### Run Locally:

```bash
python run.py
```

* Dashboard: `http://localhost:5000`
* APIs: `http://localhost:8000/predict_price`

---

## 👽 Why This Project Stands Out

* **Advanced AI**: PPO + GPT-4
* **Scalable Architecture**: Microservices, modular
* **User-Centric UI**: Responsive Flask dashboard
* **Production-Ready**: Docker, Kubernetes, logging
* **Business Value**: Actionable insights + profit optimization

---

## 💪 Future Enhancements

* Real-time data ingestion via APIs
* Fine-tune GPT-4 with large corpora
* Add authentication to dashboard

