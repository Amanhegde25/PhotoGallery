from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from functools import wraps
from src.logger import logger
import os


def login_required(f):
    """Decorator to require login for protected routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('auth_routes.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


def create_auth_routes():
    """Create and return auth routes blueprint"""
    
    auth_bp = Blueprint('auth_routes', __name__)
    
    @auth_bp.route("/login", methods=["GET", "POST"])
    def login():
        if session.get('logged_in'):
            return redirect(url_for('image_routes.upload'))
            
        if request.method == "POST":
            username = request.form.get("username")
            password = request.form.get("password")
            
            admin_username = os.getenv("ADMIN_USERNAME", "admin")
            admin_password = os.getenv("ADMIN_PASSWORD", "admin123")
            
            if username == admin_username and password == admin_password:
                session['logged_in'] = True
                session['username'] = username
                logger.info(f"User {username} logged in")
                
                next_url = request.args.get('next')
                if next_url:
                    return redirect(next_url)
                return redirect(url_for('image_routes.gallery'))
            else:
                logger.warning(f"Failed login attempt for username: {username}")
                return render_template("login.html", error="Invalid credentials")
        
        return render_template("login.html")
    
    @auth_bp.route("/logout")
    def logout():
        session.pop('logged_in', None)
        session.pop('username', None)
        logger.info("User logged out")
        return redirect(url_for('image_routes.gallery'))
    
    return auth_bp
