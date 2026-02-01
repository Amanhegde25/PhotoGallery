from flask import request, url_for
from werkzeug.utils import secure_filename
from datetime import datetime
from src.logger import logger
from bson import ObjectId
import os


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_all_images(mongo):
    logger.info("Fetching all images from database")
    return list(mongo.db.images.find().sort("_id", -1))


def get_image_by_id(mongo, image_id):
    """Get a single image by its ID"""
    try:
        return mongo.db.images.find_one({"_id": ObjectId(image_id)})
    except:
        return None


def update_image(mongo, image_id, update_data):
    """Update image metadata"""
    try:
        mongo.db.images.update_one(
            {"_id": ObjectId(image_id)},
            {"$set": update_data}
        )
        return True
    except:
        return False


def delete_image(mongo, image_id, upload_folder):
    """Delete image from database and file system"""
    try:
        image = mongo.db.images.find_one({"_id": ObjectId(image_id)})
        if image:
            # Delete file from disk
            file_path = os.path.join(upload_folder, image['img_path'])
            if os.path.exists(file_path):
                os.remove(file_path)
            
            # Delete from database
            mongo.db.images.delete_one({"_id": ObjectId(image_id)})
            return True
    except Exception as e:
        logger.error(f"Error deleting image: {e}")
    return False


def upload_image(mongo, upload_folder):
    # Check if file is present
    if 'image' not in request.files:
        logger.warning("No image file in request")
        return False, None
    
    file = request.files['image']
    
    if file.filename == '':
        logger.warning("No file selected")
        return False, None
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Add timestamp to filename to avoid duplicates
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_")
        filename = timestamp + filename
        filepath = os.path.join(upload_folder, filename)
        file.save(filepath)
        
        # Save metadata to MongoDB
        image_data = {
            "img_path": filename,
            "title": request.form.get("title", "Untitled"),
            "caption": request.form.get("caption", ""),
            "location": request.form.get("location", ""),
            "taken_time": request.form.get("taken_time", ""),
            "uploaded_at": datetime.now()
        }
        
        mongo.db.images.insert_one(image_data)
        logger.info(f"Image uploaded: {filename}")
        
        return True, url_for("image_routes.gallery")
    
    return False, None
