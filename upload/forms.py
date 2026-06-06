from django import forms

from upload.validators import validate_json_upload


class JsonUploadForm(forms.Form):
    json_file = forms.FileField(
        label='JSON-файл',
        help_text='Массив объектов с ключами "name" и "date".',
    )

    def clean_json_file(self):
        uploaded_file = self.cleaned_data['json_file']

        if not uploaded_file.name.lower().endswith('.json'):
            raise forms.ValidationError('Файл должен иметь расширение .json.')

        try:
            content = uploaded_file.read().decode('utf-8')
        except UnicodeDecodeError as exc:
            raise forms.ValidationError('Файл должен быть в кодировке UTF-8.') from exc

        valid_items, errors = validate_json_upload(content)
        if errors:
            raise forms.ValidationError(errors)

        return valid_items
