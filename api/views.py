from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from api.serializers import UserSerilizer, LoginSerilizer, FoodCategorySerializer, FoodSerializer
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import generics
from api.models import FoodCategory, Food
from rest_framework import status


class SignUpView(CreateAPIView):

    serializer_class = UserSerilizer


class GetTokenView(APIView):

    serializer_class = LoginSerilizer

    def post(self, request, *args, **kwargs):

        serializer_instance = self.serializer_class(data = request.data)


        if serializer_instance.is_valid():

            uname = serializer_instance.validated_data.get("username")

            pwd = serializer_instance.validated_data.get("password")

            user_obj = authenticate(request, username = uname, password = pwd)

            if user_obj:

                token, created = Token.objects.get_or_create(user = user_obj)

                return Response(data = token.key)
            
            return Response(data = {"message":"invalid credential"})


class FoodCategoryCreateView(APIView):

    def get(self, request, *args, **kwargs):

        qs = FoodCategory.objects.all()

        serializer_instance = FoodCategorySerializer(qs, many = True)

        print(request.user)

        return Response(data= serializer_instance.data)
        

    def post(self, request, *args, **kwargs):

        serializer = FoodCategorySerializer(data = request.data)

        if serializer.is_valid():

            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)
    

class FoodCategoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = FoodCategorySerializer

    queryset = FoodCategory.objects.all()



class FoodCreateListView(generics.ListCreateAPIView):

    serializer_class = FoodSerializer

    queryset = Food.objects.all()


class FoodRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = FoodSerializer

    queryset = Food.objects.all()











    

        









