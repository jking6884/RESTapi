from flask import Blueprint, request, jsonify, make_response
from app.comments.models import Comments, CommentsSchema
from flask_restful import Api
from app.baseviews import Resource
from app.basemodels import db
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError

comments = Blueprint('comments', __name__)
# http://marshmallow.readthedocs.org/en/latest/quickstart.html#declaring-schemas
# https://github.com/marshmallow-code/marshmallow-jsonapi
schema = CommentsSchema(strict=True)
api = Api(comments)

# Comments


class CreateListComments(Resource):
    """http://jsonapi.org/format/#fetching
    A server MUST respond to a successful request to fetch an individual resource or resource collection with a 200 OK response.
    A server MUST respond with 404 Not Found when processing a request to fetch a single resource that does not exist, except when the request warrants a 200 OK response with null as the primary data (as described above)
    a self link as part of the top-level links object"""

    def get(self):
        comments_query = Comments.query.all()
        results = schema.dump(comments_query, many=True).data
        return results

    """http://jsonapi.org/format/#crud
    A resource can be created by sending a POST request to a URL that represents a collection of comments. The request MUST include a single resource object as primary data. The resource object MUST contain at least a type member.
    If a POST request did not include a Client-Generated ID and the requested resource has been created successfully, the server MUST return a 201 Created status code"""

    def post(self):
        raw_dict = request.get_json(force=True)
        try:
            schema.validate(raw_dict)
            request_dict = raw_dict['data']['attributes']
            comment = Comments(request_dict['author'], request_dict['body'], request_dict[
                               'author_url'], request_dict['created_on'], request_dict['approved'],)
            comment.add(comment)
            # Should not return password hash
            query = Comments.query.get(comment.id)
            results = schema.dump(query).data
            return results, 201

        except ValidationError as err:
            resp = jsonify({"error": err.messages})
            resp.status_code = 403
            return resp

        except SQLAlchemyError as e:
            db.session.rollback()
            resp = jsonify({"error": str(e)})
            resp.status_code = 403
            return resp


class GetUpdateDeleteComment(Resource):

    """http://jsonapi.org/format/#fetching
    A server MUST respond to a successful request to fetch an individual resource or resource collection with a 200 OK response.
    A server MUST respond with 404 Not Found when processing a request to fetch a single resource that does not exist, except when the request warrants a 200 OK response with null as the primary data (as described above)
    a self link as part of the top-level links object"""

    def get(self, id):
        comment_query = Comments.query.get_or_404(id)
        result = schema.dump(comment_query).data
        return result

    """http://jsonapi.org/format/#crud-updating"""

    def patch(self, id):
        comment = Comments.query.get_or_404(id)
        raw_dict = request.get_json(force=True)
        try:
            schema.validate(raw_dict)
            request_dict = raw_dict['data']['attributes']
            for key, value in request_dict.items():
                setattr(comment, key, value)

            comment.update()
            return self.get(id)

        except ValidationError as err:
            resp = jsonify({"error": err.messages})
            resp.status_code = 401
            return resp

        except SQLAlchemyError as e:
            db.session.rollback()
            resp = jsonify({"error": str(e)})
            resp.status_code = 401
            return resp

    # http://jsonapi.org/format/#crud-deleting
    # A server MUST return a 204 No Content status code if a deletion request
    # is successful and no content is returned.
    def delete(self, id):
        comment = Comments.query.get_or_404(id)
        try:
            delete = comment.delete(comment)
            response = make_response()
            response.status_code = 204
            return response

        except SQLAlchemyError as e:
            db.session.rollback()
            resp = jsonify({"error": str(e)})
            resp.status_code = 401
            return resp


api.add_resource(CreateListComments, '.json')
api.add_resource(GetUpdateDeleteComment, '/<int:id>.json')
