## <project-name>

## Tech Stack
* **Frontend:** [Flask](Python)
* **Language:** Python 3.10+

## Installation & Setup

### 1. Install Prerequisites
You need **Python** installed.

### For a vertual environment (optional)
    create env : conda create -p venv python=3.12 -y
    activate : conda activate .\venv
    deactivate : conda deactivate

### 2. to install requirements
    pip install -r requirements.txt

### To run every file individully for testing
    python -m <file path>
    eg python -m src.logger

### 3. To run app file
    python app.py
* app will run in http://localhost:5000/


# File Structure 
    Project/
    ├── logs/
    ├── src/
    ├── templates/
    ├── app.py
    ├── requirements.txt

## Directory & File Explanations

### logs/
* all the logs are created here for checking the progress of the code and trobolshooting

### src/
* Contains the core source code of the project.
* Common sub-components might be:
* * Data loading & preprocessing functions
* * Model training & evaluation scripts
* * Utility modules
* * Purpose: Houses reusable and production-ready code for ML pipelines.

### templates/
* Likely contains template files used by the app (if there’s a web interface) such as:
* * HTML templates
* * UI components
* Purpose: Used for rendering front-end pages if the project includes a web app/visualization interface.

### app.py
* A Python script — likely the entry point for running the application.
* Typical roles might be:
* Serving a model via an API (Flask, FastAPI, etc.)
* Running a training/testing pipeline
* Connecting UI templates with backend logic

### requirements.txt
* Lists the Python packages/dependencies needed for the project.
* Purpose: Allows others to install all required libraries in one step (e.g., pip install -r requirements.txt).
