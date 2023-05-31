from rest_framework import serializers
from .models import Box
        
# class BoxSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Box
#         fields = ['id', 'length', 'width', 'height', 'area', 'volume', 'created_by']
#         read_only_fields = ['area', 'volume', 'created_by']
class BoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Box
        fields = ['id', 'length', 'breadth', 'height', 'area', 'volume']
        read_only_fields = ['id','area','volume']
