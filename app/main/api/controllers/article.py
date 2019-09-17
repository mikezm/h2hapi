import logging

from flask import abort
from flask_restplus import Resource
from app.main.api.models import serializers
from app.main.services import article_service
from app.main.api.restplus import api
from app.main.api.middleware.token_auth import token_required
from app.main.api.middleware.access import access_level

log = logging.getLogger(__name__)

ns = api.namespace('articles', description='Operations for managing articles')


@ns.route('/summary')
class GetArticleSummary(Resource):
    @api.response(200, model=serializers.articles_summary_response, description='Summary of Articles')
    @api.response(404, model=serializers.message, description='Articles Not Found')
    @api.marshal_with(serializers.articles_summary_response)
    def get(self):
        """
        Returns a summary of all articles
        """
        fetched_articles = article_service.get_articles_summary()
        if not fetched_articles:
            abort(404, 'Articles Not Found.')
        return { 'data': fetched_articles }, 200
        

@ns.route('/article')
class GetArticle(Resource):
    @api.expect(serializers.get_article_request)
    @api.response(200, model=serializers.article, description='Article Detail')
    @api.response(404, model=serializers.message, description='Article Not Found')
    @api.marshal_with(serializers.article, code=200)
    def post(self):
        """
        Returns a single article
        """
        fetched_article = article_service.get_article(api.payload['headline'])
        if fetched_article:
            return fetched_article, 200
        abort(404, 'Article Not Found.')   
    
@ns.route('/new')
class PostNewArticle(Resource):
    @api.expect(serializers.article)
    @api.marshal_with(serializers.message)
    @api.doc(security='apikey')
    @token_required
    @access_level('admin', parameters=False)
    def post(self, data):
        """
        Creates a new article
        """
        message, status = article_service.add_article(api.payload)
        return { 'message': message }, status


