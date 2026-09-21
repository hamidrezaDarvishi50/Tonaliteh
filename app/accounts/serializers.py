from rest_framework import serializers

from .models import User


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'phone']
        
class ProfileUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']
        

class RequestOTPSerializer(serializers.Serializer):
    
    phone = serializers.RegexField(regex=r"^09\d{9}$",
        error_messages={
            "invalid": "فرمت به درستی وارد نشده است، لطفا از اعداد انگلیسی استفاده کنید"
        })
    

class VerifyOTPSerializer(serializers.Serializer):
    phone = serializers.RegexField(
        regex=r"^09\d{9}$",
        error_messages={
            "invalid": "فرمت به درستی وارد نشده است، لطفا از اعداد انگلیسی استفاده کنید"
            }
    )
    otp = serializers.RegexField(
        regex=r"^\d{6}$",
        error_messages={
            "invalid":  "کد یکبار مصرف نادرست است یا منقضی شده است"
        }
    )