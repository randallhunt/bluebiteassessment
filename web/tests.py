from django.test import TestCase
from django.urls import reverse

from api.helper import random_hex
from api.models import BBObject


class ViewTests(TestCase):
    def test_list_view(self):
        for x in range(0,10):
            o = BBObject(object_id=random_hex(32))
            o.save()
        response = self.client.get('/list?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'web/list.html')
        self.assertEqual(response.context['count'], 10)
        self.assertEqual(response.context['page'], 2)

    def test_keys_view(self):
        for x in range(0,10):
            o = BBObject(object_id=random_hex(32))
            o.save()
        response = self.client.get(reverse('keys'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'web/keys.html')

    def test_retrieve_view(self):
        self.obj = BBObject(object_id="12345678901234567890123456789012")
        self.obj.save()
        response = self.client.get('/object/12345678901234567890123456789012')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'web/retrieve.html')

    def test_upload_view(self):
        response = self.client.get(reverse('upload'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'web/upload.html')