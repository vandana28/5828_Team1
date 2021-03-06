from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

import app.posts.post_management as management

post_routes = Blueprint('post_routes', __name__)

@post_routes.route("/api/new_post", methods=["GET", "POST"])
@jwt_required
def new_post():
    username = get_jwt_identity()
    title = request.json.get("title")
    content = request.json.get("content")
    tags = request.json.get("tags")
    filename = request.json.get("filename")

    post_id = management.create_post(username, title, content, tags, filename)

    return jsonify({"msg": "created post", "id": post_id}), 200

@post_routes.route("/api/list_posts_by_date", methods=["GET", "POST"])
@jwt_required
def get_by_date():
    username = get_jwt_identity()
    timestamp = request.json.get("date")
    posts = management.get_posts_by_date(username, timestamp)
    reply = {"msg": f"Found {len(posts)}",
             "posts": posts}
    
    return jsonify(reply), 200

@post_routes.route("/api/list_posts", methods=["GET", "POST"])
@jwt_required
def list_posts():
    username = get_jwt_identity()
    posts = management.list_posts(username)

    reply = {"msg": f"Found {len(posts)} posts",
             "posts": posts}

    return jsonify(reply), 200

@post_routes.route("/api/update_post", methods=["GET", "POST"])
@jwt_required
def update_post():
    username = get_jwt_identity()
    post_id = request.json.get("id")
    title = request.json.get("title")
    content = request.json.get("content")
    tags = request.json.get("tags")
    filename = request.json.get("filename")
    updated = management.update_post(username, post_id, title, content, tags, filename)

    if updated:
        return jsonify({"msg": "Post has been updated", "id": post_id}), 200
    
    return jsonify({"msg": "Post has not been updated",  "id": post_id}), 404


@post_routes.route("/api/upload_image/<post_id>", methods=["GET", "POST"])
@jwt_required
def upload_image(post_id):
    username = get_jwt_identity()

    image = request.data
    updated = management.upload_image(username, post_id, str(image))

    if updated:
        return jsonify({"msg": "Image has been updated",  "id": post_id}), 200

    return jsonify({"msg": "Image has not been updated",  "id": post_id}), 404

@post_routes.route("/api/delete_post", methods=["GET", "POST"])
@jwt_required
def delete_post():
    username = get_jwt_identity()
    post_id = request.json.get("id")
    response = management.delete_post(username, post_id)

    if response == management.OK:
        return jsonify({"msg": "Post deleted"}), 200
    
    if response == management.NOT_FOUND:
        return jsonify({"msg": "Unable to delete message"}), 404
    
    return jsonify({"msg": "Unable to delete message"}), 401

@post_routes.route("/api/get_post", methods=["GET", "POST"])
@jwt_required
def get_post():
    username = get_jwt_identity()
    post_id = request.json.get("id")

    post = management.get_post(username, post_id)
    
    if post == None:
        return jsonify({"msg": "post not found"}), 404

    reply = {"msg": "Found post", "post": post}

    return jsonify(reply), 200

@post_routes.route("/api/search_posts", methods=["GET", "POST"])
@jwt_required
def search_post():
    username = get_jwt_identity()
    text = request.json.get("text")
    tags = request.json.get("tags")

    results = management.search_posts(username, text, tags)

    reply = {"msg": f"Found {len(results)} results", "results": results}
    
    return jsonify(reply), 200