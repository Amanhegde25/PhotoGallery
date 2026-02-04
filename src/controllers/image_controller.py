from flask import request, url_for, Response
from werkzeug.utils import secure_filename
from datetime import datetime
from src.logger import logger
from bson import ObjectId
from gridfs import GridFS
import io


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

# Content type mapping for serving images
CONTENT_TYPES = {
    'png': 'image/png',
    'jpg': 'image/jpeg',
    'jpeg': 'image/jpeg',
    'gif': 'image/gif',
    'webp': 'image/webp'
}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_file_extension(filename):
    """Get the file extension from filename"""
    if '.' in filename:
        return filename.rsplit('.', 1)[1].lower()
    return 'jpg'  # Default


def get_all_images(mongo):
    logger.info("Fetching all images from database")
    try:
        return list(mongo.db.images.find().sort("_id", -1))
    except Exception as e:
        logger.error(f"Error fetching images: {e}")
        return []


def get_images_by_tag(mongo, tag):
    """Get all images with a specific tag"""
    logger.info(f"Fetching images with tag: {tag}")
    try:
        return list(mongo.db.images.find({"tags": tag}).sort("_id", -1))
    except Exception as e:
        logger.error(f"Error fetching images by tag: {e}")
        return []


def get_all_tags(mongo):
    """Get all unique tags from all images with counts"""
    try:
        pipeline = [
            {"$unwind": "$tags"},
            {"$group": {"_id": "$tags", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}}
        ]
        result = list(mongo.db.images.aggregate(pipeline))
        # Return just tag names for backward compatibility
        return [item["_id"] for item in result]
    except Exception as e:
        logger.error(f"Error fetching tags: {e}")
        return []


def get_tags_with_counts(mongo):
    """Get all unique tags with their image counts"""
    try:
        pipeline = [
            {"$unwind": "$tags"},
            {"$group": {"_id": "$tags", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}}
        ]
        result = list(mongo.db.images.aggregate(pipeline))
        return [{"tag": item["_id"], "count": item["count"]} for item in result]
    except Exception as e:
        logger.error(f"Error fetching tags with counts: {e}")
        return []


def get_trending_tag(mongo):
    """Get the trending tag - prefers tags with 3+ images, otherwise returns most popular tag"""
    try:
        tags_with_counts = get_tags_with_counts(mongo)
        if not tags_with_counts:
            return None
        
        # First, try to find a tag with more than 3 images
        for tag_data in tags_with_counts:
            if tag_data["count"] > 3:
                return tag_data["tag"]
        
        # If no tag has more than 3 images, return the tag with most images
        return tags_with_counts[0]["tag"]
    except Exception as e:
        logger.error(f"Error getting trending tag: {e}")
        return None


def parse_tags(tags_string):
    """Parse comma-separated tags string into a list"""
    if not tags_string:
        return []
    return [tag.strip().lower() for tag in tags_string.split(',') if tag.strip()]


def get_image_by_id(mongo, image_id):
    """Get a single image by its ID"""
    try:
        return mongo.db.images.find_one({"_id": ObjectId(image_id)})
    except:
        return None


def get_image_file(mongo, image_id):
    """Get the image file data from GridFS"""
    try:
        image = mongo.db.images.find_one({"_id": ObjectId(image_id)})
        if not image or 'file_id' not in image:
            return None, None
        
        fs = GridFS(mongo.db)
        grid_out = fs.get(image['file_id'])
        
        # Get content type from extension
        extension = image.get('extension', 'jpg')
        content_type = CONTENT_TYPES.get(extension, 'image/jpeg')
        
        return grid_out.read(), content_type
    except Exception as e:
        logger.error(f"Error retrieving image file: {e}")
        return None, None


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


def delete_image(mongo, image_id):
    """Delete image from database and GridFS"""
    try:
        image = mongo.db.images.find_one({"_id": ObjectId(image_id)})
        if image:
            # Delete file from GridFS
            if 'file_id' in image:
                fs = GridFS(mongo.db)
                fs.delete(image['file_id'])
            
            # Delete from database
            mongo.db.images.delete_one({"_id": ObjectId(image_id)})
            return True
    except Exception as e:
        logger.error(f"Error deleting image: {e}")
    return False


def upload_image(mongo):
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
        extension = get_file_extension(filename)
        
        # Add timestamp to filename to avoid duplicates
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_")
        filename = timestamp + filename
        
        # Read file data
        file_data = file.read()
        
        # Store in GridFS
        fs = GridFS(mongo.db)
        file_id = fs.put(
            file_data,
            filename=filename,
            content_type=CONTENT_TYPES.get(extension, 'image/jpeg')
        )
        
        # Parse tags from form
        tags = parse_tags(request.form.get("tags", ""))
        
        # Save metadata to MongoDB
        image_data = {
            "file_id": file_id,
            "filename": filename,
            "extension": extension,
            "title": request.form.get("title", "Untitled"),
            "caption": request.form.get("caption", ""),
            "location": request.form.get("location", ""),
            "taken_time": request.form.get("taken_time", ""),
            "tags": tags,
            "uploaded_at": datetime.now()
        }
        
        mongo.db.images.insert_one(image_data)
        logger.info(f"Image uploaded to GridFS: {filename}")
        
        return True, url_for("image_routes.gallery")
    
    return False, None
