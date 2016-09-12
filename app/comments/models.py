from marshmallow_jsonapi import Schema, fields
from marshmallow import validate
from app.basemodels import db, CRUD_MixIn


class Comments(db.Model, CRUD_MixIn):
    id = db.Column(db.Integer, primary_key=True)

    author = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    author_url = db.Column(db.String(250), nullable=False)
    created_on = db.Column(db.Date, nullable=False)
    approved = db.Column(db.Boolean, nullable=False)

    def __init__(self,  author,  body,  author_url,  created_on,  approved, ):

        self.author = author
        self.body = body
        self.author_url = author_url
        self.created_on = created_on
        self.approved = approved


class CommentsSchema(Schema):

    not_blank = validate.Length(min=1, error='Field cannot be blank')
    # add validate=not_blank in required fields
    id = fields.Integer(dump_only=True)

    author = fields.String(validate=not_blank)
    body = fields.String(validate=not_blank)
    author_url = fields.URL(validate=not_blank)
    created_on = fields.Date(required=True)
    approved = fields.Boolean(required=True)

    # self links
    def get_top_level_links(self, data, many):
        if many:
            self_link = "/comments/"
        else:
            self_link = "/comments/{}".format(data['id'])
        return {'self': self_link}

    class Meta:
        type_ = 'comments'
