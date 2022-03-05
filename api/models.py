from django.db import models, transaction
from jsonschema import Draft201909Validator, ValidationError
import json

from .helper import load_json_file


class BBProperty(models.Model):
    key = models.CharField(max_length=40)
    value = models.CharField(max_length=40, null=True)


class BBObject(models.Model):
    object_id = models.CharField(max_length=150)
    properties = models.ManyToManyField(BBProperty)

    def to_json(self):
        return {
            "object_id": self.object_id,
            "data": [{
                "key": p.key,
                "value": p.value,
            } for p in self.properties.all()]
        }


class BBBatch(models.Model):
    batch_id = models.CharField(max_length=40)

    @staticmethod    
    def process(json):
        schema = load_json_file('schema.json')
        try:
            Draft201909Validator(schema).validate(json)
        except ValidationError:
            raise BBBatch.InvalidSchema

        b = BBBatch.objects.filter(batch_id=json["batch_id"]).exists()
        if b:
            raise BBBatch.AlreadyProcessed

        with transaction.atomic():
            for obj in json["objects"]:
                o, _ = BBObject.objects.get_or_create(object_id=obj["object_id"])
                [o.properties.get_or_create(key=p["key"], value=p["value"]) for p in obj["data"]]

            b = BBBatch(batch_id=json["batch_id"])
            b.save()
            return b

    class AlreadyProcessed(Exception):
        pass

    class InvalidSchema(Exception):
        pass