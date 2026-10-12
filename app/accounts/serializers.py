from rest_framework import serializers

from .models import User, Address
from art.models import Art

class AddressSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.phone", read_only=True)
    
    class Meta:
        model = Address
        fields = ["id", "user", "address", "postal_code"]
        read_only_fields = ["id"]

class ProfileSerializer(serializers.ModelSerializer):
    addresses = AddressSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'phone', 'addresses']
        
class ProfileUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']

class RequestOTPSerializer(serializers.Serializer):
    
    phone = serializers.RegexField(regex=r"^09\d{9}$",
        error_messages={
            "invalid": "فرمت به درستی وارد نشده است، لطفا از اعداد انگلیسی استفاده کنید"})

class VerifyOTPSerializer(serializers.Serializer):
    phone = serializers.RegexField(
        regex=r"^09\d{9}$",
        error_messages={"invalid": "فرمت به درستی وارد نشده است، لطفا از اعداد انگلیسی استفاده کنید"})
    
    otp = serializers.RegexField(
        regex=r"^\d{6}$",
        error_messages={"invalid":  "کد یکبار مصرف نادرست است یا منقضی شده است"})

class FavoriteArtsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Art
        fields = ['id', 'name', 'slug', 'image', 'artist']
