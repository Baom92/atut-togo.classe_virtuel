import logging
import uuid
from datetime import datetime

from flask import request
from flask_restplus import Resource
from controllers.serializers import post, get
from controllers.restplus import api
from repositories.models import mongoConnection

log = logging.getLogger(__name__)
collection = mongoConnection("localhost", "demo", "recette")
ns = api.namespace('recipes', description='Operations related to recipes')


@ns.route('/')
class RecetteCollection(Resource):

    @api.marshal_list_with(get)
    def get(self):
        """
            Returns list of recipes
        """
        recettes = list(collection.find({}))
        return recettes

    @api.response(201, 'Category successfully created.')
    @api.expect(post)
    def post(self):
        """
        Creates a new recipe
        """
        data = request.json
        data['_id'] = str(uuid.uuid4())
        collection.insert_one(data)
        return None, 201


@ns.route('/<string:id>')
@api.response(404, 'Recipe not found.')
class RecetteItem(Resource):

    @api.marshal_with(get)
    def get(self, id):
        """
            Returns a recipe with a list of posts.
        """
        return collection.find_one({"_id": id})

    @api.response(204, 'Recipe successfully updated.')
    @api.expect(post)
    def put(self, id):
        """
        Updates a recipe
        """
        data = request.json
        data['_id'] = id
        collection.replace_one(collection.find_one({'_id': id}), data, False)
        return None, 204

    @api.response(204, 'Recipe successfully deleted.')
    def delete(self, id):
        """
        Deletes blog category.
        """
        collection.delete_one(collection.find_one({'_id': id}))
        return None, 204
