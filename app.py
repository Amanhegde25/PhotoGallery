from flask import Flask, jsonify
from flask_pymongo import PyMongo
from dotenv import load_dotenv
from src.logger import logger
from src.routes import create_image_routes
from src.routes.auth_routes import create_auth_routes
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Flask Configuration
mongo_uri = os.getenv("MONGO_URI")
if not mongo_uri:
    logger.error("MONGO_URI environment variable is not set!")
    
app.config["MONGO_URI"] = mongo_uri or "mongodb://localhost:27017/portfoleo"
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "default-secret-key")

# Initialize MongoDB with error handling
mongo = None
try:
    mongo = PyMongo(app)
    # Test connection
    mongo.db.command('ping')
    logger.info("MongoDB connected successfully")
except Exception as e:
    logger.error(f"MongoDB connection failed: {e}")

# Upload Configuration from .env
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.getenv("UPLOAD_FOLDER", "upload"))
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = int(os.getenv("MAX_CONTENT_LENGTH", 16 * 1024 * 1024))

# Register blueprints only if mongo is available
if mongo:
    image_routes = create_image_routes(mongo, UPLOAD_FOLDER)
    auth_routes = create_auth_routes()
    app.register_blueprint(image_routes)
    app.register_blueprint(auth_routes)
else:
    @app.route("/")
    def error_page():
        return jsonify({
            "error": "Database not configured",
            "message": "Please set MONGO_URI environment variable in Vercel"
        }), 500


@app.route("/health")
def health():
    """Health check endpoint"""
    logger.info("Health check route accessed")
    return "Healthy", 200


if __name__ == "__main__":
    # Ensure upload folder exists
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    
    # Get Flask config from .env
    debug = os.getenv("FLASK_DEBUG", "True").lower() == "true"
    host = os.getenv("FLASK_HOST", "127.0.0.1")
    port = int(os.getenv("FLASK_PORT", 5000))
    
    logger.info("Starting Flask server")
    app.run(debug=False, host=host, port=port, use_reloader=False)

