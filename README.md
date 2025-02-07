# 🚀 Introducing Meowsenti 🚀

Meowsenti is a simple application designed to analyze sentiment in Indonesian mobile banking applications.

## 🤖 Model Overview

This system is built using two popular Natural Language Processing algorithms: **Multinomial Naïve Bayes** and **Support Vector Machine (SVM)**. The model has been trained on a dataset of **13,527 reviews** from the BRImo mobile banking application.

The dataset is split into **60% for training** and **40% for testing**.

## 🔍 MFSvc Model (Support Vector Machine)

The **MFSvc** model is optimized using GridSearchCV. Below is the parameter grid used:

| Parameter        | Values         |
| ---------------- | -------------- |
| **C**            | 0.1, 1, 10     |
| **kernel**       | linear, rbf    |
| **gamma**        | scale, auto    |
| **class_weight** | balanced, None |

After hyperparameter tuning, the best configuration is:

```shell
Best parameters found: {'C': 10, 'class_weight': 'balanced', 'gamma': 'scale', 'kernel': 'rbf'}
Best cross-validation accuracy: 95.67%
```

### 📊 Evaluation Metrics

| Class            | Precision | Recall | F1-score |
| ---------------- | --------- | ------ | -------- |
| **Positive (1)** | 0.9226    | 0.9179 | 0.9202   |
| **Negative (0)** | 0.6281    | 0.6281 | 0.6281   |
| **Neutral (2)**  | 0.7348    | 0.7436 | 0.7392   |

- **Train Accuracy:** 95.67%
- **Test Accuracy:** 83.11%

### 🔥 Visualizations

- **Classification Report:**

  ![Classification Report SVM](./assets/images/mfsvc/classification-report.png)

- **Confusion Matrix:**

  ![Confusion Matrix SVM](./assets/images/mfsvc/confusion-matrix.png)

## 📉 MFNb Model (Naïve Bayes)

The **MFNb** model is also optimized using GridSearchCV. Below is the parameter grid used:

| Parameter     | Values           |
| ------------- | ---------------- |
| **alpha**     | 0.01, 0.1, 1, 10 |
| **fit_prior** | True, False      |

After hyperparameter tuning, the best configuration is:

```shell
Best parameters found: {'alpha': 0.01, 'fit_prior': True}
Best cross-validation accuracy: 95.23%
```

### 📊 Evaluation Metrics

| Class            | Precision | Recall | F1-score |
| ---------------- | --------- | ------ | -------- |
| **Positive (1)** | 0.9012    | 0.9338 | 0.9172   |
| **Negative (0)** | 0.6507    | 0.6006 | 0.6246   |
| **Neutral (2)**  | 0.7386    | 0.7085 | 0.7232   |

- **Train Accuracy:** 95.23%
- **Test Accuracy:** 82.77%

### 🔥 Visualizations

- **Classification Report:**

  ![Classification Report NB](./assets/images/mfnb/classification-report.png)

- **Confusion Matrix:**

  ![Confusion Matrix NB](./assets/images/mfnb/confusion-matrix.png)

---

## 🛠️ How to Run Meowsenti Locally

### 🐳 Using Docker

First, pull the image and run:

```sh
# Pull the Docker image
docker pull mframadann/meowsenti

# Run the container
docker run -d --name sentiment-app -p 5001:7860 mframadann/meowsenti
```

### 🔬 Testing the API

Use tools like **Postman** or **Insomnia**, or send a request via **cURL**:

```sh
curl -X POST \
  http://localhost:5001/api/v1/analyze-sentiment \
  -H "Content-Type: application/json" \
  -d '{
        "reviews": [
           {"review": "Bagus banget aplikasinya"},
           {"review": "Aplikasi apa ini, jelek banget idih"},
           {"review": "Cukup membantu saya bertransaksi"},
           {"review": "Mantap banget euy aplikasinya"}
        ],
        "model": "MFNb"
    }'
```

### 📡 API Response

```json
{
  "data": {
    "sentiment": [
      {
        "alg_type": "Naïve Bayes",
        "kind_of_sentiment": "Positive",
        "review": "Bagus banget aplikasinya"
      },
      {
        "alg_type": "Naïve Bayes",
        "kind_of_sentiment": "Negative",
        "review": "Aplikasi apa ini, jelek banget idih"
      },
      {
        "alg_type": "Naïve Bayes",
        "kind_of_sentiment": "Neutral",
        "review": "Cukup membantu saya bertransaksi"
      },
      {
        "alg_type": "Naïve Bayes",
        "kind_of_sentiment": "Positive",
        "review": "Mantap banget euy aplikasinya"
      }
    ]
  },
  "status": "success"
}
```

## 💻 Running Meowsenti Manually

### Clone the Repository

```sh
git clone https://github.com/mframadann/meowsenti.git && cd meowsenti
```

### Set Up a Virtual Environment

```sh
python3 -m venv .venv
source .venv/bin/activate
```

### Install Dependencies

```sh
pip install --no-cache-dir -r requirements.txt
```

### Start the Application

```sh
python app.py ## run on http://localhost:7860
```

---

## 📜 API Documentation

For detailed API documentation, visit: [Mframadan Labs](https://labs.mframadan.dev). You can also try Meowsenti directly on Hugging Face Spaces:

🔗 [Meowsenti on Hugging Face](https://huggingface.co/spaces/mframadann/meowsenti)

## ⚠️ Note

This model works **only for Indonesian text and last updated of analytics report is based on model observation in oct 2024**. Thanks for visiting! Feel free to connect with me:

🔗 [LinkedIn](https://linkedin.com/in/muhamad-firly-ramadan)

---
