from django.shortcuts import render
# from .decorators import staff_required
from .serializers import BoxSerializer
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser,AllowAny
from rest_framework.response import Response
from .models import Box
from rest_framework import serializers
from django.utils.dateparse import parse_date
# Create your views here.

# Add Api: 
#     Adding a box with given dimensions(length breadth and height). 
#     Adding user should be automatically associated with the box and shall not be overridden
#     Permissions:
#           User should be logged in and should be staff to add the box
# {"length":12,"breadth":10,"height":2}

class AddBox(APIView):
    permission_classes = [IsAuthenticated,IsAdminUser]
    def post(self,request):
        serializer = BoxSerializer(data= request.data)
        if serializer.is_valid():
            box = serializer.save(creator = request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
        # length = request.data.get('length')
        # breadth = request.data.get('breadth')
        # height = request.data.get('height')
        # #   Area and Volume
        # area = length * breadth
        # volume = length * breadth * height
        # request.data['area'] = area
        # request.data['volume'] = volume
        # serializer = BoxSerializer(data=request.data)
        # print(request.data)
        # if serializer.is_valid():
        #     box = serializer.save(creator = request.user)
        #     return Response(serializer.data, status=201)
        # return Response(serializer.errors, status=400)

class UpdateBox(APIView):
    permission_classes = [IsAdminUser,IsAuthenticated]
    def put(self,request,pk):
        box = Box.objects.get(pk=pk)

        #Exclude 'creator' and "created_at" fields from request.data
        # request_data = request.data.copy()
        # request_data.pop('creator',None)
        # request_data.pop('created_at',None)

        # serializer = BoxSerializer(box, data=request_data,partial=True)
        
        #-----  Method 2 
        serializer = BoxSerializer(box, data=request.data,partial=True)

        if serializer.is_valid():
            # serializer.save()
            serializer.save(exclude = ['creator','created_at'])
            return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
        return Response(serializer.error, status=400)
    
class ListAllBox(APIView):
    #List of all boxes Available
        # Data For each box Required:
        #     1. Length
        #     2. width
        #     3. Height
        #     4. Area
        #     5. Volume
        #     6. Created By :  (This Key shall only be available if requesting user is staff)
        #     7. Last Updated :  (This Key shall only be available if requesting user is staff)
        permission_classes = [AllowAny]
        def get(self,request):
              #---- List All Boxes
            boxes = Box.objects.all()
            # --- Filters 
            # F1 - Boxes with length_more_than or length_less_than
            length_more_than = request.query_params.get('length_more_than')
            length_less_than = request.query_params.get('length_less_than')

            #F2 - Boxes with breadth_more_than or breadth_less_than
            breadth_more_than = request.query_params.get('breadth_more_than')
            breadth_less_than = request.query_params.get('breadth_less_than')

            #F3   3. Boxes with height_more_than or height_less_than
            height_more_than = request.query_params.get('height_more_than')
            height_less_than = request.query_params.get('height_less_than')
            
            # 4. Boxes with area_more_than or area_less_than
            area_more_than = request.query_params.get('area_more_than')
            area_less_than = request.query_params.get('area_less_than')

            # 5. Boxes with volume_more_than or volume_less_than
            volume_more_than = request.query_params.get('volume_more_than')
            volume_less_than = request.query_params.get('volume_less_than')

            # 6. Boxes created by a specific user by username
            creator_username = request.query_params.get('creator_username')

            # 7. Boxes created before or after a given date
            created_before = request.query_params.get('created_before')
            created_after = request.query_params.get('created_after')

            #Actual Logic
            if length_more_than:
                 boxes = boxes.filter(length__gt = length_more_than)
            if length_less_than:
                 boxes = boxes.filter(length__lt=length_less_than)
            if breadth_more_than:
                 boxes = boxes.filter(breadth__gt = breadth_more_than)
            if breadth_less_than:
                boxes = boxes.filter(breadth__lt=breadth_less_than)
            if height_more_than:
                boxes = boxes.filter(height__gt=height_more_than)
            if height_less_than:
                boxes = boxes.filter(height__lt=height_less_than)
            if area_more_than:
                boxes = boxes.filter(area__gt=area_more_than)
            if area_less_than:
                boxes = boxes.filter(area__lt=area_less_than)
            if volume_more_than:
                boxes = boxes.filter(volume__gt=volume_more_than)
            if volume_less_than:
                boxes = boxes.filter(volume__lt=volume_less_than)
            if creator_username:
                boxes = boxes.filter(creator__username=creator_username)
            if created_before:
                created_before_date = parse_date(created_after)
                boxes = boxes.filter(created_at__lt = created_before_date)
            if created_after:
                created_after_date = parse_date(created_after)
                boxes= boxes.filter(created_at__gt = created_after_date)


            serializer = BoxSerializer(boxes,many=True)

            if request.user.is_staff:
                 serializer.fields['creator'] = serializers.CharField()
                 serializer.fields['creator'] = serializers.DateTimeField()
            return Response(serializer.data)
        


