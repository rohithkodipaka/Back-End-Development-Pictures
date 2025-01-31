from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))


######################################################################
# RETURN HEALTH OF THE APP
######################################################################
@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200


######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################
@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    """
    Get all pictures in the list
    """
    return data


######################################################################
# GET A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    for picture in data:
        if picture["id"] == id:
            return picture
    return {"message": "Picture not found"}, 404


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    """
    This endpoint will add a new picture
    """
    new_picture = request.json

    # if the id is already there, return 302 with the URL for the resource
    for picture in data:
        if new_picture["id"] == picture["id"]:
            return {
                "Message": f"picture with id {new_picture['id']} already present"
            }, 302

    data.append(new_picture)
    return new_picture, 201


######################################################################
# UPDATE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    """
    This endpoint will update an existing picture
    """
    updated_picture = request.json

    # Check if picture with specified id exists in data list
    for picture in data:
        if picture["id"] == id:
            # Update existing picture with new data
            picture.update(updated_picture)
            return {"message": f"Picture with id {id} updated successfully."}, 201

    # If picture with specified id not found in data list, return 404 error
    return {"message": f"Picture with id {id} not found."}, 404


######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    """
    This endpoint will delete an existing picture
    """

    # Find the picture with the given ID
    for picture in data:
        if picture["id"] == id:
            data.remove(picture)
            return "", 204

    # If no picture is found with the given ID, return a 404 status code
    return {"message": f"No picture with id {id} found."}, 404
