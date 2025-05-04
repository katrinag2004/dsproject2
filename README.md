# DS2002 Chatbot Project

A Flask-based chatbot assistant for [Your Chatbot's Topic - e.g., Weather, Recipes].

## Description

This chatbot answers questions using data from:
1.  A live API ([Name or Type of API])
2.  A local CSV file generated via an ETL process ([Source of original data]).

## Setup

1.  **Clone the repository:**
    ```bash
    git clone [your-repo-url]
    cd [your-repo-name]
    ```
2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Set up Environment Variables:**
    * (List any required environment variables here, e.g., API Keys)
    * Example: `export MY_API_KEY='your_key_here'` (Linux/macOS)
    * Example: `set MY_API_KEY=your_key_here` (Windows CMD)
    * Example: `$env:MY_API_KEY='your_key_here'` (Windows PowerShell)

## Running the Application

### Run ETL Pipeline (if needed)
To generate/update the `processed_local_data.csv` file:
```bash
python app.py --run-etl