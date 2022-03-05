import json
import os
import sys
from django.test import TestCase
# from django.urls import reverse

from .helper import load_json_file, random_hex
from .models import BBObject, BBBatch, BBProperty


class HelperTests(TestCase):
    app_base = ""

    def setUp(self):
        BBObject.objects.all().delete()
        self.app_base = os.path.dirname(sys.modules['__main__'].__file__)
        path = "%s/files/__unit_test_file__.json" % self.app_base
        source_text = '{ "foo": "bar" }'
        with open(path, 'w') as file:
            file.write(source_text)

    def tearDown(self):
        BBObject.objects.all().delete()
        path = "%s/files/__unit_test_file__.json" % self.app_base
        os.remove(path)

    def test_load_json_file(self):
        data = load_json_file('__unit_test_file__.json')
        self.assertEqual(data['foo'], 'bar')
    
    def test_random_hex(self):
        s = random_hex(16)
        self.assertEqual(len(s), 16)


class ModelsTests(TestCase):
    def test_to_json(self):
        b = BBObject(object_id="12345678901234567890123456789012")
        b.save()
        b.properties.get_or_create(key="hola", value="hello")
        b.properties.get_or_create(key="adios", value="goodbye")
        self.assertDictEqual(b.to_json(), {
            "object_id": "12345678901234567890123456789012",
            "data": [{
                "key": "hola",
                "value": "hello"
            }, {
                "key": "adios",
                "value": "goodbye"
            }]
        })

    def test_batch_processor(self):
        good_obj = {  ## matches the schema
            "batch_id": "asdfasdfasdfasdfasdfasdfasdfasdf",
            "objects": [
                {
                    "object_id": "dfdfdfdfdfdfdfdfdfdfdfdfdfdfdfdf",
                    "data": [
                        {
                            "key": "fred",
                            "value": "barney",
                        }
                    ]
                }                
            ]
        }
        try:
            BBBatch.process(good_obj)
        except:
            self.fail("unexpected exception on good_obj")

        bad_obj = {  ## doesn't match the schema
            "batch_id": "asdfasdfasdfasdfasdfasdfasdfasdf",
            "data": [
                {
                    "key": "fred",
                    "value": "barney",
                }
            ]
        }
        with self.assertRaises(BBBatch.InvalidSchema):
            BBBatch.process(bad_obj)

class ViewsTests(TestCase):
    def setUp(self):
        self.obj = BBObject(object_id='12345678901234567890123456789012')
        self.obj.save()

    def tearDown(self):
        BBBatch.objects.all().delete()
        BBObject.objects.all().delete()
        BBProperty.objects.all().delete()

    def test_list(self):
        for x in range(0,10):
            o = BBObject(object_id=random_hex(32))
            o.save()
        response = self.client.get('/api/list?page=2')
        self.assertEqual(response.status_code, 200)

    def test_keys(self):
        response = self.client.get('/api/keys')
        self.assertEqual(response.status_code, 200)

    def test_retrieve(self):
        response = self.client.get('/api/object/12345678901234567890123456789012')
        self.assertEqual(response.status_code, 200)

    def test_upload(self):
        objs = [{
            "object_id": random_hex(32),
            "data": [
                {"key": "name", "value": "foo"}
            ]
        } for x in range(0, 10)]
        data = {
            "batch_id": random_hex(32),
            "objects": objs
        }
        response = self.client.post('/api/upload', json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 200)

        BBObject.objects.get(object_id=objs[0]['object_id'])