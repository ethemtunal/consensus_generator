from rest_framework import serializers
from .models import Image, Annotator, Annotation, Consensus


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = "__all__"


class AnnotatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Annotator
        fields = "__all__"


class AnnotationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Annotation
        fields = "__all__"


class ConsensusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consensus
        fields = "__all__"
