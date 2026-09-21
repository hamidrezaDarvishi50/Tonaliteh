from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
from .models import User
import jwt

def user_authenticate(request):
    auth_header = request.headers.get('Authorization')

    if not auth_header:
        raise AuthenticationFailed('Authorization header is missing')

    parts = auth_header.split()


    if len(parts) != 2 :
        raise AuthenticationFailed('Invalid Authorization header format')
    if parts[0].lower() != 'bearer':
         raise AuthenticationFailed("Token didnt start with Bearer")

    raw_token = parts[1]

    try:
        payload = jwt.decode(raw_token,settings.SECRET_KEY,algorithms=['HS256'])
        # print("**********",payload)
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed("Token expired")

    except jwt.DecodeError:
        raise AuthenticationFailed("Token decoding error")

    except jwt.InvalidTokenError:
        raise AuthenticationFailed("Invalid token")



    user_id = payload["user_id"]
    if not user_id : 
        raise AuthenticationFailed("Invalid token payload")

    try:
        user = User.objects.get(pk=user_id)

    except User.DoesNotExist:

        raise AuthenticationFailed("User not found")

    if not user.is_active:
        raise AuthenticationFailed("User is banned")

    return user