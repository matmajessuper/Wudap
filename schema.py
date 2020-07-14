from marshmallow import Schema, fields


class BrowserHistorySchema(Schema):
    site = fields.Str()
    count = fields.Int()
