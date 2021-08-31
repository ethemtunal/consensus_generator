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


class AnnotationDetailAPIView(APIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Annotation.objects.filter(uuid=pk)
        except Annotation.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        annotation = self.get_object(pk)
        serializer = AnnotationSerializer(annotation, many=True)
        return Response(serializer.data)

    def put(self, request, pk):
        annotation = self.get_object(pk)

        annotator_id = request.data["annotator"]
        temp_annotator = Annotator.objects.filter(id=annotator_id)
        if not temp_annotator:
            #Annotator.objects.create(id=annotator_id, score=0)
            return Response(data="Annotator doesn't exist!", status=status.HTTP_404_NOT_FOUND)

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

        serializer = AnnotationSerializer(annotation.first(), data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        annotation = self.get_object(pk)
        annotation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ConsensusAPIView(APIView):

    def get(self, request):
        consensus = Consensus.objects.all()
        serializer = ConsensusSerializer(consensus, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ConsensusSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CalculateConsensusAPIView(APIView):

    def get(self, request):
        # Calculate annotator scores for known images
        images = Image.objects.filter(known=True)
        for image in images:
            known_image_id = image.id
            # Get unprocessed annotations for the known image
            annotations = Annotation.objects.filter(image=known_image_id, processed=False)
            for annotation in annotations:
                annotator_id = annotation.annotator
                box1 = [image.x1, image.y1, image.x2, image.y2]
                box2 = [annotation.x1, annotation.y1, annotation.x2, annotation.y2]
                annotation_score = get_iou(box1, box2)
                previous_known_annotations = Annotation.objects.filter(annotator=annotator_id, image__known=True, processed=True)
                annotator_points = [float(k.point) for k in previous_known_annotations]
                annotator_points.append(annotation_score)
                annotator_point = sum(annotator_points) / len(annotator_points)
                annotator_save = Annotator.objects.get(id=annotator_id)
                setattr(annotator_save, "score", annotator_point)
                annotator_save.save()
                annotation.processed.set(True)
                annotation.save()

        images_to_calculate = Image.objects.filter(known=False, calculated=False)
        for image_calculate in images_to_calculate:
            image_id = image_calculate.id
            # Get unprocessed annotation
            calculate_annotations = Annotation.objects.filter(image=image_id, processed=False)
            boxes = []
            for c_annotation in calculate_annotations:
                c_annotator_id = c_annotation.annotator.id
                box = [c_annotation.x1, c_annotation.y1, c_annotation.x2, c_annotation.y2]
                annotator_score = c_annotation.annotator.score
                boxes.append({"annotator": c_annotator_id, "box": box, "score": annotator_score, "annotation": c_annotation.id})

            non_valids = get_non_valid(boxes)
            # Add annotation ids to remove
            to_remove = []
            for i in non_valids:
                update_annotation = Annotation.objects.get(id=i)
                update_annotation.x1_out = non_valids[i][0]
                update_annotation.y1_out = non_valids[i][1]
                update_annotation.x2_out = non_valids[i][2]
                update_annotation.y2_out = non_valids[i][3]
                update_annotation.spam = True if True in non_valids[i] else False
                if True in non_valids[i]:
                    to_remove.append(i)
                update_annotation.save()
            # Filter outliers from boxes
            filtered_boxes = [b for b in boxes if b["annotation"] not in to_remove]
            consensus_details = calculate_consensus(filtered_boxes)

            data = {
                #"annotators": consensus_annotators,
                "image": Image.objects.get(id=image_id),
                "score": consensus_details["consensus_score"],
                "x1_lower": consensus_details["bounds"]["x1_bounds"]["lower"],
                "x1_upper": consensus_details["bounds"]["x1_bounds"]["upper"],
                "x2_lower": consensus_details["bounds"]["x2_bounds"]["lower"],
                "x2_upper": consensus_details["bounds"]["x2_bounds"]["upper"],
                "y1_lower": consensus_details["bounds"]["y1_bounds"]["lower"],
                "y1_upper": consensus_details["bounds"]["y1_bounds"]["upper"],
                "y2_lower": consensus_details["bounds"]["y2_bounds"]["lower"],
                "y2_upper": consensus_details["bounds"]["y2_bounds"]["upper"],
                "annotation_count": len(boxes),
                "spam_count": len(to_remove),
            }
            created_consensus = Consensus.objects.create(**data)
            for i in consensus_details["annotator_ids"]:
                temp_annotator = Annotator.objects.get(id=i)
                created_consensus.annotators.add(temp_annotator)
            #created_consensus.save()
            image_calculate.calculated = True
            image_calculate.save()
        return Response("Consensus created", status=status.HTTP_201_CREATED)

    def post(self, request):
        serializer = ConsensusSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CalculateImageConsensus(APIView):

    def get_object(self, pk):
        try:
            return Image.objects.get(uuid=pk)
        except Image.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        image_calculate = self.get_object(pk)
        if image_calculate.known:
            return Response(data="Image is known!", status=status.HTTP_400_BAD_REQUEST)
        if image_calculate.calculated:
            return Response(data="Image is calculated!", status=status.HTTP_400_BAD_REQUEST)

        images = Image.objects.filter(known=True)
        for image in images:
            score_image_id = image.id
            # Get unprocessed annotations for the known image
            annotations = Annotation.objects.filter(image=score_image_id, processed=False)
            for annotation in annotations:
                annotator_id = annotation.annotator
                box1 = [image.x1, image.y1, image.x2, image.y2]
                box2 = [annotation.x1, annotation.y1, annotation.x2, annotation.y2]
                annotation_score = get_iou(box1, box2)
                previous_known_annotations = Annotation.objects.filter(annotator=annotator_id, image__known=True,
                                                                       processed=True)
                annotator_points = [float(k.point) for k in previous_known_annotations]
                annotator_points.append(annotation_score)
                annotator_point = sum(annotator_points) / len(annotator_points)
                annotator_save = Annotator.objects.get(id=annotator_id)
                setattr(annotator_save, "score", annotator_point)
                annotator_save.save()
                annotation.processed.set(True)
                annotation.save()

        image_id = image_calculate.id
        # Get unprocessed annotation
        annotations = Annotation.objects.filter(image=image_id, processed=False)
        boxes = []
        for annotation in annotations:
            annotator_id = annotation.annotator.id
            box = [annotation.x1, annotation.y1, annotation.x2, annotation.y2]
            annotator_score = annotation.annotator.score
            boxes.append(
                {"annotator": annotator_id, "box": box, "score": annotator_score, "annotation": annotation.id})

        non_valids = get_non_valid(boxes)
        # Add annotation ids to remove
        to_remove = []
        for i in non_valids:
            update_annotation = Annotation.objects.get(id=i)
            update_annotation.x1_out = non_valids[i][0]
            update_annotation.y1_out = non_valids[i][1]
            update_annotation.x2_out = non_valids[i][2]
            update_annotation.y2_out = non_valids[i][3]
            update_annotation.spam = True if True in non_valids[i] else False
            if True in non_valids[i]:
                to_remove.append(i)
            update_annotation.save()
        # Filter outliers from boxes
        filtered_boxes = [b for b in boxes if b["annotation"] not in to_remove]
        consensus_details = calculate_consensus(filtered_boxes)

        data = {
            #"annotators": consensus_annotators[0],
            "image": Image.objects.get(id=image_id),
            "score": consensus_details["consensus_score"],
            "x1_lower": consensus_details["bounds"]["x1_bounds"]["lower"],
            "x1_upper": consensus_details["bounds"]["x1_bounds"]["upper"],
            "x2_lower": consensus_details["bounds"]["x2_bounds"]["lower"],
            "x2_upper": consensus_details["bounds"]["x2_bounds"]["upper"],
            "y1_lower": consensus_details["bounds"]["y1_bounds"]["lower"],
            "y1_upper": consensus_details["bounds"]["y1_bounds"]["upper"],
            "y2_lower": consensus_details["bounds"]["y2_bounds"]["lower"],
            "y2_upper": consensus_details["bounds"]["y2_bounds"]["upper"],
            "annotation_count": len(boxes),
            "spam_count": len(to_remove),
        }
        created_consensus = Consensus.objects.create(**data)
        for i in consensus_details["annotator_ids"]:
            temp_annotator = Annotator.objects.get(id=i)
            created_consensus.annotators.add(temp_annotator)
        image_calculate.calculated = True
        image_calculate.save()
        # created_consensus.save()

        return Response("Consensus created", status=status.HTTP_201_CREATED)
