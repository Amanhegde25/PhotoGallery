from flask import Blueprint, render_template, request, redirect, session, url_for, Response, jsonify
from src.controllers.image_controller import (
    get_all_images, upload_image, get_image_by_id, get_image_file, 
    update_image, delete_image, get_all_tags, get_images_by_tag, parse_tags,
    get_trending_tag
)
from src.routes.auth_routes import login_required
from src.logger import logger


def create_image_routes(mongo):    
    image_bp = Blueprint('image_routes', __name__)
    
    @image_bp.route("/")
    def gallery():
        logger.info("Gallery route accessed")
        images = get_all_images(mongo)
        tags = get_all_tags(mongo)
        trending_tag = get_trending_tag(mongo)
        logged_in = session.get('logged_in', False)
        return render_template("gallery.html", images=images, tags=tags, trending_tag=trending_tag, logged_in=logged_in)
    
    @image_bp.route("/api/images/tag/<tag>")
    def get_images_for_tag(tag):
        """API endpoint to get images by tag"""
        images = get_images_by_tag(mongo, tag)
        # Convert ObjectId to string for JSON serialization
        images_data = []
        for img in images:
            images_data.append({
                "_id": str(img["_id"]),
                "title": img.get("title", ""),
                "caption": img.get("caption", ""),
                "location": img.get("location", ""),
                "taken_time": img.get("taken_time", ""),
                "tags": img.get("tags", [])
            })
        return jsonify(images_data)
    
    @image_bp.route("/upload", methods=["GET", "POST"])
    @login_required
    def upload():
        if request.method == "POST":
            success, redirect_url = upload_image(mongo)
            if success:
                return redirect(redirect_url)
            return redirect(request.url)
        
        logger.info("Upload form accessed")
        return render_template("upload.html")
    
    @image_bp.route("/edit/<image_id>", methods=["GET", "POST"])
    @login_required
    def edit(image_id):
        image = get_image_by_id(mongo, image_id)
        if not image:
            return redirect(url_for('image_routes.gallery'))
        
        if request.method == "POST":
            # Parse tags from form
            tags = parse_tags(request.form.get("tags", ""))
            
            update_data = {
                "title": request.form.get("title", image['title']),
                "caption": request.form.get("caption", ""),
                "location": request.form.get("location", ""),
                "taken_time": request.form.get("taken_time", ""),
                "tags": tags
            }
            update_image(mongo, image_id, update_data)
            logger.info(f"Image {image_id} updated")
            return redirect(url_for('image_routes.gallery'))
        
        return render_template("edit.html", image=image)
    
    @image_bp.route("/delete/<image_id>", methods=["POST"])
    @login_required
    def delete(image_id):
        delete_image(mongo, image_id)
        logger.info(f"Image {image_id} deleted")
        return redirect(url_for('image_routes.gallery'))
    
    @image_bp.route("/image/<image_id>")
    def serve_image(image_id):
        """Serve image from GridFS"""
        file_data, content_type = get_image_file(mongo, image_id)
        if file_data is None:
            return "Image not found", 404
        
        return Response(file_data, mimetype=content_type)
    
    return image_bp

