from datetime import datetime

from django.test import Client, SimpleTestCase, TestCase
from django.urls import reverse
from django.utils import timezone

from upload.models import UploadedItem
from upload.validators import parse_upload_date, validate_json_upload


class ValidateJsonUploadTests(SimpleTestCase):
    def test_valid_file(self):
        content = '[{"name": "test", "date": "2026-06-06_14:30", "extra": "ignored"}]'
        items, errors = validate_json_upload(content)
        self.assertEqual(errors, [])
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]['name'], 'test')
        self.assertEqual(
            items[0]['date'],
            parse_upload_date('2026-06-06_14:30'),
        )

    def test_name_too_long(self):
        content = '[{"name": "' + 'a' * 50 + '", "date": "2026-06-06_14:30"}]'
        _, errors = validate_json_upload(content)
        self.assertEqual(len(errors), 1)
        self.assertIn('name', errors[0])

    def test_missing_keys(self):
        content = '[{"name": "test"}, {"date": "2026-06-06_14:30"}]'
        _, errors = validate_json_upload(content)
        self.assertEqual(len(errors), 2)

    def test_invalid_date_format(self):
        content = '[{"name": "test", "date": "06-06-2026 14:30"}]'
        _, errors = validate_json_upload(content)
        self.assertEqual(len(errors), 1)
        self.assertIn('date', errors[0])


class SaveUploadedItemsTests(TestCase):
    def test_bulk_create_from_validated_items(self):
        items = [
            {'name': 'first', 'date': parse_upload_date('2026-06-06_10:00')},
            {'name': 'second', 'date': parse_upload_date('2026-06-06_11:30')},
        ]
        UploadedItem.objects.bulk_create(
            [UploadedItem(name=item['name'], date=item['date']) for item in items]
        )

        self.assertEqual(UploadedItem.objects.count(), 2)
        saved = UploadedItem.objects.get(name='second')
        self.assertEqual(saved.date, timezone.make_aware(datetime(2026, 6, 6, 11, 30)))


class ItemsListViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_items_list_page(self):
        UploadedItem.objects.create(
            name='alpha',
            date=parse_upload_date('2026-06-06_10:00'),
        )
        response = self.client.get(reverse('items_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'alpha')
        self.assertContains(response, 'items-table')
