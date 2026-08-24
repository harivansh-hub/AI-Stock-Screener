\# AI Stock Screener 📈



An AI-powered stock screening and analysis application built with Python and machine learning. The project combines technical indicators, market data features, liquidity analysis, backtesting, and a machine learning model to identify potentially profitable trading opportunities.



\## 🚀 Features



\- NSE stock screening

\- LTP-based stock filtering

\- Liquidity and LTQ analysis

\- SMMA 20 and SMMA 120 technical indicators

\- Feature engineering for trading signals

\- Historical trade simulation and backtesting

\- Machine learning-based profit/loss prediction

\- Random Forest classification model

\- Model evaluation and feature importance analysis

\- Interactive dashboard for stock screening and analysis



\## 🧠 Machine Learning Approach



The project uses a supervised machine learning approach to classify trading opportunities.



The model learns from historical simulated trades using features such as:



\- SMMA gap

\- Price change

\- Average LTQ

\- LTQ ratio

\- Market type

\- Other engineered market features



The target variable represents whether a simulated trade was profitable or resulted in a loss.



A Random Forest classifier is used for prediction.



\## 📊 Model Evaluation



The trained model was evaluated using a train/test split and standard classification metrics including:



\- Accuracy

\- Precision

\- Recall

\- F1-score

\- Feature importance



The model achieved approximately \*\*60.69% test accuracy\*\* on the current dataset.



> Model performance depends on the generated data, feature engineering, market conditions, and trading assumptions. The model should not be considered a guaranteed indicator of future market performance.



\## 🔄 Project Workflow



```text

Market Data

&#x20;    ↓

Stock Filtering

&#x20;    ↓

Technical Indicators

&#x20;    ↓

Feature Engineering

&#x20;    ↓

Trade Simulation / Backtesting

&#x20;    ↓

Training Dataset

&#x20;    ↓

Random Forest Model

&#x20;    ↓

Prediction

&#x20;    ↓

Stock Screening Decision





🛠️ Technologies Used

Python

Pandas

NumPy

Scikit-learn

Joblib

Streamlit

Machine Learning

Technical Analysis

Backtesting

📁 Project Structure

AI\_Stock\_Screener/

│

├── AI\_Stock\_Screener\_Submission/

│   └── sourcecode/

│       ├── backtest.py

│       ├── broker\_data.py

│       ├── dashboard.py

│       ├── data\_generator.py

│       ├── evaluate.py

│       ├── features.py

│       ├── indicators.py

│       ├── main.py

│       ├── market\_data.py

│       ├── ml\_dataset.py

│       ├── predict.py

│       ├── run\_app.py

│       ├── save\_model.py

│       ├── trade\_simulation.py

│       ├── train\_model.py

│       └── trainer\_data.py

│

├── training\_data.csv

├── requirements.txt

├── .gitignore

└── README.md

⚙️ Installation



Clone the repository:



git clone https://github.com/harivansh-hub/AI-Stock-Screener.git

cd AI-Stock-Screener



Create a virtual environment:



python -m venv venv



Activate the virtual environment on Windows:



venv\\Scripts\\activate



Install the dependencies:



pip install -r requirements.txt

▶️ Running the Project



Go to the source code directory:



cd AI\_Stock\_Screener\_Submission\\sourcecode



Run the main application:



python main.py



To run the Streamlit dashboard:



streamlit run dashboard.py



Note: Streamlit is required to run the dashboard.



📈 Backtesting



The project includes backtesting and trade simulation components to evaluate trading strategies using historical or generated market data.



The backtesting process evaluates simulated trades and determines whether each trade resulted in a profit or loss.



🔮 Prediction



The trained machine learning model predicts the probability of a trade being profitable based on engineered market features.



The prediction pipeline uses the trained Random Forest model to classify potential trading outcomes.



⚠️ Disclaimer



This project is developed for educational and experimental purposes.



It is not financial advice and should not be used as the sole basis for real-world trading or investment decisions. Stock markets involve significant risk, and simulated or historical performance does not guarantee future results.



👩‍💻 Author



Divya Jyoti Sadhotra



AI / Machine Learning Project

