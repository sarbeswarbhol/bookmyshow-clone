import os
from datetime import datetime
from django.utils.text import slugify

def upload_file_with_timestamp(instance, filename, folder='uploads'):
    ext = filename.split('.')[-1]
    base_name = getattr(instance, 'name', None) or getattr(instance, 'title', None) or 'file'
    slug = slugify(base_name)
    timestamp = datetime.now().strftime('%Y%m%dT%H%M%S')
    new_filename = f"{slug}-{timestamp}.{ext}"
    return os.path.join(folder, new_filename)
