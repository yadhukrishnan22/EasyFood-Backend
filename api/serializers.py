from rest_framework import serializers

from django.contrib.auth.models import User

from api.models import Seller, FoodCategory, Food


class UserSerilizer(serializers.ModelSerializer):

    password1 = serializers.CharField(write_only = True)

    password2 = serializers.CharField(write_only = True)

    password = serializers.CharField(read_only = True)

    class Meta:

        model = Seller

        fields = ['id', 'username', 'email', 'password1', 'password2', 'seller_category', 'password']
        

    
    def create(self, validated_data):

        password1 = validated_data.pop('password1')

        password2 = validated_data.pop('password2')

        

        if password1 != password2:

            raise serializers.ValidationError('Password Mismatch')

        return Seller.objects.create_user(**validated_data, password = password1)


class LoginSerilizer(serializers.Serializer):

    username = serializers.CharField()

    password = serializers.CharField()


class FoodCategorySerializer(serializers.ModelSerializer):

    class Meta:

        model = FoodCategory

        fields= "__all__"

        read_only_field = ['id', 'created_date', 'owner', 'is_active']
    
    def validate_name(self, value):

        if FoodCategory.objects.filter(food_category_name = value).exists():

            raise serializers.ValidationError("Category name already exists")
        
        return value


class FoodSerializer(serializers.ModelSerializer):

    class Meta:

        model = Food

        fields = "__all__"

        read_only_field = ['id', 'created_date', 'owner', 'is_active']




