from .models import Image, Annotator, Annotation, Consensus
from .serializers import ImageSerializer, AnnotatorSerializer, AnnotationSerializer, ConsensusSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView


class ImageAPIView(APIView):

    def get(self, request):
        images = Image.objects.all()
        serializer = ImageSerializer(images, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ImageSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
