from django.http import HttpResponse
from .models import Image, Annotator, Annotation, Consensus
from .serializers import ImageSerializer, AnnotatorSerializer, AnnotationSerializer, ConsensusSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .helpers import *


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


class AnnotationAPIView(APIView):

    def get(self, request):
        annotation = Annotation.objects.all()
        serializer = AnnotationSerializer(annotation, many=True)
        return Response(serializer.data)

    def post(self, request):
        # If annotator doesn't exists, ERROR
        annotator_id = request.data["annotator"]
        temp_annotator = Annotator.objects.filter(id=annotator_id)
        if not temp_annotator:
            # Annotator.objects.create(id=annotator_id, score=0)
            return Response(data="Annotator doesn't exist!", status=status.HTTP_404_NOT_FOUND)

        # If image doesn't exists, ERROR
        image_id = request.data["image"]
        temp_image = Image.objects.filter(id=image_id)
        if not temp_image:
            return Response(data="Image doesn't exist!", status=status.HTTP_404_NOT_FOUND)
        else:
            is_calculated = temp_image.first().calculated
            is_known = temp_image.first().known
            # If consensus calculated for the image, check boundaries
            if is_calculated:
                consensus = Consensus.objects.filter(image=image_id).first()
                if not(float(consensus.x1_lower) < float(request.data["x1"]) < float(consensus.x1_upper)):
                    request.data["x1_out"] = True
                    request.data["spam"] = True
                if not(float(consensus.x2_lower) < float(request.data["x2"]) < float(consensus.x2_upper)):
                    request.data["x2_out"] = True
                    request.data["spam"] = True
                if not(float(consensus.y1_lower) < float(request.data["y1"]) < float(consensus.y1_upper)):
                    request.data["y1_out"] = True
                    request.data["spam"] = True
                if not(float(consensus.y2_lower) < float(request.data["y2"]) < float(consensus.y2_upper)):
                    request.data["y2_out"] = True
                    request.data["spam"] = True
                request.data["processed"] = True
            if is_known:
                request.data["processed"] = True
                # If image is known calculate annotator score and update
                box1 = [temp_image.first().x1, temp_image.first().y1, temp_image.first().x2, temp_image.first().y2]
                box2 = [request.data["x1"], request.data["y1"], request.data["x2"], request.data["y2"]]
                annotator_score = get_iou(box1, box2)
                request.data["point"] = annotator_score
                if annotator_score == 0:
                    request.data["spam"] = True
                    request.data["x1_out"] = True
                    request.data["y1_out"] = True
                    request.data["x2_out"] = True
                    request.data["y2_out"] = True
                known_annotations = Annotation.objects.filter(annotator=annotator_id, image__known=True)
                user_points = [float(k.point) for k in known_annotations]
                user_points.append(annotator_score)
                annotator_point = sum(user_points) / len(user_points)
                annotator_save = Annotator.objects.get(id=annotator_id)
                setattr(annotator_save, "score", annotator_point)
                annotator_save.save()

        # If annotator already annotated the same image, DELETE previous annotation
        past_annotations = Annotation.objects.filter(annotator=annotator_id, image=image_id)
        if past_annotations:
            past_annotations.delete()
        serializer = AnnotationSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
