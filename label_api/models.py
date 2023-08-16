import uuid
from django.db import models
from django.core.validators import MinValueValidator
#from django.contrib.auth.models import User


class Image(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    known = models.BooleanField(default=False)
    name = models.CharField(max_length=255)
    x1 = models.FloatField(null=True, blank=True, default=None)
    x2 = models.FloatField(null=True, blank=True, default=None)
    y1 = models.FloatField(null=True, blank=True, default=None)
    y2 = models.FloatField(null=True, blank=True, default=None)
    calculated = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_created=True, auto_now_add=True)

    def __str__(self):
        return "image_" + str(self.name)


class Annotator(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=255)
    score = models.FloatField(null=True, blank=True, default=None, validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_created=True, auto_now_add=True)

    def __str__(self):
        return "annotator_" + str(self.name) + "_" + str(self.uuid)


class Annotation(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    annotator = models.ForeignKey(Annotator, on_delete=models.CASCADE)
    x1 = models.FloatField(null=False, default=0)
    x2 = models.FloatField(null=False, default=0)
    y1 = models.FloatField(null=False, default=0)
    y2 = models.FloatField(null=False, default=0)
    x1_out = models.BooleanField(default=False)
    x2_out = models.BooleanField(default=False)
    y1_out = models.BooleanField(default=False)
    y2_out = models.BooleanField(default=False)
    spam = models.BooleanField(default=False)
    processed = models.BooleanField(default=False)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    point = models.FloatField(null=True, blank=True, default=None)
    created_at = models.DateTimeField(auto_created=True, auto_now_add=True)

    def __str__(self):
        return "annotation_" + str(self.uuid)


class Consensus(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    annotators = models.ManyToManyField(Annotator)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    score = models.FloatField(null=True, blank=True, default=None)
    x1_lower = models.FloatField(null=True, blank=True, default=None)
    x1_upper = models.FloatField(null=True, blank=True, default=None)
    x2_lower = models.FloatField(null=True, blank=True, default=None)
    x2_upper = models.FloatField(null=True, blank=True, default=None)
    y1_lower = models.FloatField(null=True, blank=True, default=None)
    y1_upper = models.FloatField(null=True, blank=True, default=None)
    y2_lower = models.FloatField(null=True, blank=True, default=None)
    y2_upper = models.FloatField(null=True, blank=True, default=None)
    annotation_count = models.IntegerField(null=False, default=0, validators=[MinValueValidator(0)])
    spam_count = models.IntegerField(null=False, default=0, validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_created=True, auto_now_add=True)

    def __str__(self):
        return "consensus_" + str(self.uuid)
