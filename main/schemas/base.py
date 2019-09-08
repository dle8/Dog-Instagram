from marshmallow import Schema, EXCLUDE, pre_load


class BaseSchema(Schema):
    @pre_load()
    def strip_data(self, data, **kwargs):
        for key in data:
            if isinstance(data[key], str):
                data[key] = data[key].strip()
        return data

    class Meta:
        unknown = EXCLUDE
