# from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets, status
from rest_framework.decorators import action
from .serializers import ImageSerializer
from rest_framework.response import Response
from .inference import recognize_lpns

# Create your views here.
class LicenseReadViewSet(viewsets.ViewSet):

    @action(methods=['POST'], detail=False, url_name="text-only" , url_path="nums")
    def get_plate_text(self, request):
        serializer=ImageSerializer(data=request.data)
        # print(request.data)

        if serializer.is_valid():
            v = serializer.validated_data
            lpn_dict = {}

            imgs_list = v.get('imgs')
            ocr_engine = v.get('ocr_engine')
            
            for img in imgs_list:
                lpn_dict[img.name] = recognize_lpns([img], ocr_engine)[0]
            
            return Response(data=lpn_dict,status=status.HTTP_200_OK)

        return Response(data="Invalid data!",status=status.HTTP_400_BAD_REQUEST)

def liveness(request):
    return HttpResponse("Server is live!")