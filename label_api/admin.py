from django.contrib import admin
from .models import Image, Annotator, Annotation, Consensus

admin.site.register(Image)
admin.site.register(Annotator)
admin.site.register(Annotation)
admin.site.register(Consensus)