from rest_framework import serializers

class ImageSerializer(serializers.Serializer):
    imgs = serializers.ListField( child=serializers.ImageField(), min_length=1, max_length=5)
    ocr_engine = serializers.CharField()

    def validate_ocr_engine(self, value):
        if value.upper() == "PY_TESSERACT":
            value=0
        elif value.upper() == "EASYOCR":
            value=1
        
        return value
