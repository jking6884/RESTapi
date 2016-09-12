from marshmallow_jsonapi import Schema, fields
from marshmallow import validate
from app.basemodels import db, CRUD_MixIn


class Posts(db.Model, CRUD_MixIn):
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    creation_date = db.Column(db.Date, nullable=False)
    published = db.Column(db.Boolean, nullable=False)

    def __init__(self,  title,  body,  author,  creation_date,  published, ):

        self.title = title
        self.body = body
        self.author = author
        self.creation_date = creation_date
        self.published = published


class PostsSchema(Schema):

    not_blank = validate.Length(min=1, error='Field cannot be blank')
    # add validate=not_blank in required fields
    id = fields.Integer(dump_only=True)

    title = fields.String(validate=not_blank)
    body = fields.String(validate=not_blank)
    author = fields.String(validate=not_blank)
    creation_date = fields.Date(required=True)
    published = fields.Boolean(required=True)

    # self links
    def get_top_level_links(self, data, many):
        if many:
            self_link = "/posts/"
        else:
            self_link = "/posts/{}".format(data['id'])
        return {'self': self_link}

    class Meta:
        type_ = 'posts'
