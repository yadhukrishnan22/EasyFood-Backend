from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from api.serializers import UserSerilizer, SignInSerializer, FoodCategorySerializer, FoodSerializer
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import generics
from api.models import FoodCategory, Food
from rest_framework import status
from django.db import IntegrityError
from rest_framework.exceptions import ValidationError
from rest_framework import viewsets
from rest_framework import authentication, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken




class SignUpView(CreateAPIView):

    serializer_class = UserSerilizer


class SignInView(APIView):

    def post(self, request, *args, **kwargs):

        serializer = SignInSerializer(data=request.data)

        if serializer.is_valid():

            user = serializer.validated_data['user']
            
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            return Response({
                'access_token': access_token,
                'refresh_token': str(refresh),
                'user': user.username,
                'message': 'Login successfull'
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class GetTokenView(APIView):

    serializer_class = SignInSerializer

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

    authentication_classes = [authentication.BasicAuthentication]

    permission_classes = [permissions.IsAuthenticated]


    def get(self, request, *args, **kwargs):

        qs = FoodCategory.objects.filter(seller_obj = request.user)

        serializer_instance = FoodCategorySerializer(qs, many = True)

        return Response(data= serializer_instance.data)
        

    def post(self, request, *args, **kwargs):

        serializer = FoodCategorySerializer(data = request.data)

        if serializer.is_valid():

            try:
                serializer.save()

                return Response(serializer.data, status=status.HTTP_201_CREATED)
            
            except IntegrityError:

                raise ValidationError({"message":"The category name already exists"})
                
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class FoodCategoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = FoodCategorySerializer

    queryset = FoodCategory.objects.all()



class FoodCreateListView(generics.ListCreateAPIView):

    serializer_class = FoodSerializer

    authentication_classes = [authentication.BasicAuthentication]

    permission_classes = [permissions.IsAuthenticated]   

    def get(self, request, *args, **kwargs):

        qs = Food.objects.filter(seller_obj = request.user)

        serializer_instance = FoodSerializer(qs, many = True)

        if serializer_instance.is_valid():

            try:
                serializer_instance.save()

                return Response(serializer_instance.data, status = status.HTTP_200_OK)
            
            except IntegrityError:

                raise ValidationError({"message": "category with this name already exists"})
            
   
        return Response(serializer_instance.error, status = status.HTTP_400_BAD_REQUEST)

    



class FoodRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = FoodSerializer

    queryset = Food.objects.all()






















    

        









