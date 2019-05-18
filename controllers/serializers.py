from flask_restplus import fields
from controllers.restplus import api

etape_preparation = api.model('A recipe preparation step', {
    'numero': fields.Integer(required=True, description='Index of the step'),
    'description': fields.String(required=True, description='The step description')
})

post = api.model('Recipe post', {
    "nom": fields.String(required=True, description='The recipe name'),
    "nombre_personnes": fields.String(required=True, description='The number of people'),
    "temps_preparation": fields.String(required=True, description='The preparation time'),
    "temps_cuisson": fields.String(required=True, description='The cooking time'),
    "temps_total": fields.String(required=True, description='The total duration'),
    "ingredients": fields.List(fields.String,required=True, description='The recipe ingredients list'),
    "etapes_preparation": fields.List(fields.Nested(etape_preparation), required=True,
                                      description='The recipe preparation steps')
})

get = api.model('Recipe get', {
    '_id': fields.String(readOnly=True, description='The unique identifier of a recipe'),
    "nom": fields.String(required=True, description='The recipe name'),
    "nombre_personnes": fields.String(required=True, description='The number of people'),
    "temps_preparation": fields.String(required=True, description='The preparation time'),
    "temps_cuisson": fields.String(required=True, description='The cooking time'),
    "temps_total": fields.String(required=True, description='The total duration'),
    "ingredients": fields.List(fields.String,required=True, description='The recipe ingredients list'),
    "etapes_preparation": fields.List(fields.Nested(etape_preparation), required=True,
                                      description='The recipe preparation steps')
})
