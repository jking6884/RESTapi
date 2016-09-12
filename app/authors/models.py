from marshmallow_jsonapi import Schema, fields
from marshmallow import validate
from app.basemodels import db, CRUD_MixIn


class Authors(db.Model, CRUD_MixIn):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(250), nullable=False)
    profile = db.Column(db.Text, nullable=False)
    url = db.Column(db.String(250), nullable=False)

    def __init__(self,  name,  profile,  url, ):

        self.name = name
        self.profile = profile
        self.url = url


class AuthorsSchema(Schema):

    not_blank = validate.Length(min=1, error='Field cannot be blank')
    # add validate=not_blank in required fields
    id = fields.Integer(dump_only=True)

    name = fields.String(validate=not_blank)
    profile = fields.String(validate=not_blank)
    url = fields.URL(validate=not_blank)

    # self links
    def get_top_level_links(self, data, many):
        if many:
            self_link = "/authors/"
        else:
            self_link = "/authors/{}".format(data['id'])
        return {'self': self_link}

    class Meta:
        type_ = 'authors'
