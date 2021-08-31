from django.http import HttpResponse
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


class ImageDetailAPIView(APIView):

    def get_object(self, pk):
        try:
            return Image.objects.filter(uuid=pk)
        except Image.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        image = self.get_object(pk)
        serializer = ImageSerializer(image, many=True)
        return Response(serializer.data)

    def put(self, request, pk):
        image = self.get_object(pk)
        serializer = ImageSerializer(image.first(), data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        image = self.get_object(pk)
        image.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AnnotatorAPIView(APIView):

    def get(self, request):
        annotator = Annotator.objects.all()
        serializer = AnnotatorSerializer(annotator, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AnnotatorSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AnnotatorDetailAPIView(APIView):

    def get_object(self, pk):
        try:
            return Annotator.objects.filter(uuid=pk)
        except Annotator.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        annotator = self.get_object(pk)
        serializer = AnnotatorSerializer(annotator, many=True)
        return Response(serializer.data)

    def put(self, request, pk):
        annotator = self.get_object(pk)
        serializer = AnnotatorSerializer(annotator.first(), data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        annotator = self.get_object(pk)
        annotator.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
