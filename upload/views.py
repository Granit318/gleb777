from django.contrib import messages
from django.db import transaction
from django.shortcuts import render

from upload.forms import JsonUploadForm
from upload.models import UploadedItem


def upload_json(request):
    form = JsonUploadForm()

    if request.method == 'POST':
        form = JsonUploadForm(request.POST, request.FILES)
        if form.is_valid():
            items = form.cleaned_data['json_file']
            with transaction.atomic():
                UploadedItem.objects.bulk_create(
                    [
                        UploadedItem(name=item['name'], date=item['date'])
                        for item in items
                    ]
                )
            messages.success(
                request,
                f'Файл успешно загружен. Сохранено записей: {len(items)}.',
            )
            form = JsonUploadForm()

    return render(request, 'upload/upload.html', {'form': form})


def items_list(request):
    items = UploadedItem.objects.all()
    return render(request, 'upload/items_list.html', {'items': items})
