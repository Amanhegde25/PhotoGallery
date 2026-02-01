from flask import Blueprint, render_template, request, redirect, send_from_directory, session, url_for
from src.controllers.image_controller import get_all_images, upload_image, get_image_by_id, update_image, delete_image
from src.routes.auth_routes import login_required
from src.logger import logger


def create_image_routes(mongo, upload_folder):    
    image_bp = Blueprint('image_routes', __name__)
    
    @image_bp.route("/")
    def gallery():
        logger.info("Gallery route accessed")
        images = get_all_images(mongo)
        logged_in = session.get('logged_in', False)
        return render_template("gallery.html", images=images, logged_in=logged_in)
    
    @image_bp.route("/upload", methods=["GET", "POST"])
    @login_required
    def upload():
        if request.method == "POST":
            success, redirect_url = upload_image(mongo, upload_folder)
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
            update_data = {
                "title": request.form.get("title", image['title']),
                "caption": request.form.get("caption", ""),
                "location": request.form.get("location", ""),
                "taken_time": request.form.get("taken_time", "")
            }
            update_image(mongo, image_id, update_data)
            logger.info(f"Image {image_id} updated")
            return redirect(url_for('image_routes.gallery'))
        
        return render_template("edit.html", image=image)
    
    @image_bp.route("/delete/<image_id>", methods=["POST"])
    @login_required
    def delete(image_id):
        delete_image(mongo, image_id, upload_folder)
        logger.info(f"Image {image_id} deleted")
        return redirect(url_for('image_routes.gallery'))
    
    @image_bp.route("/uploads/<filename>")
    def serve_image(filename):
        return send_from_directory(upload_folder, filename)
    
    return image_bp
