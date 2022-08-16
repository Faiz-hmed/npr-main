# from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets, status
from rest_framework.decorators import action
from .serializers import ImageSerializer
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from .inference import recognize_lpns

# Create your views here.
class LicenseReadViewSet(viewsets.ViewSet):

    @action(methods=['POST'], detail=False, url_name="text-only" , url_path="nums")
    def plate_text(self, request):
        serializer=ImageSerializer(data=request.data)
        
        lpn_dict = {}
        imgs_list, ocr_engine = self.get_request_data(serializer) 
            
        for img in imgs_list:
            lpn_dict[img.name] = recognize_lpns([img], ocr_engine)[0]
        
        return Response(data=lpn_dict,status=status.HTTP_200_OK)


    @action(methods=['POST'],detail=False,url_name='boxes-text',url_path="boxes-nums")
    def boxes_w_plate_text(self, request):
        serializer=ImageSerializer(data=request.data)
        imgs_list, ocr_engine = self.get_request_data(serializer) 

        lp_bn_dict = {}
        for img in imgs_list:
            lp_bx,lpns = recognize_lpns([img],ocr_engine,return_boxes=True)
            lpns = lpns[0]
            lp_bx = lp_bx[0]
            sub_res = []

            for i in range(len(lp_bx)):
                sub_res.append([lpns[i], lp_bx[i]])
            
            lp_bn_dict[img.name] = sub_res

        return Response(data=lp_bn_dict,status=status.HTTP_200_OK)

    def get_request_data(self, serializer):

        if serializer.is_valid():
            v = serializer.validated_data

            imgs = v.get('imgs')
            ocr = v.get('ocr_engine')
            return (imgs, ocr)
        else:
            raise ParseError(detail="Invalid field data!")

def liveness(request):
    return HttpResponse("Server is live!")