import json, re, bcrypt, jwt

from django.views         import View
from django.http          import JsonResponse

from users.models         import User       as UserModel
from users.models         import WishList   as WishListModel
from restaurants.models   import Restaurant as RestaurantModel
from my_settings          import SECRET_KEY, algorithm
#from users.utils         import login_decorator

class SignUpView(View):
    def post(self, request):
        try:
            data            = json.loads(request.body)
            email           = data['email']
            password        = data['password']
            hashed_password = bcrypt.hashpw(password.encode('UTF-8'), bcrypt.gensalt())

            if UserModel.objects.filter(email=email).exists():
                return JsonResponse({"MESSAGE": "EMAIL_ALREADY_EXIST"}, status=400)

            if not re.match(r"^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email):
                return JsonResponse({"MESSAGE": "INVALID_FORMAT"}, status=400)

            if not re.match(r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$", password):
                return JsonResponse({"MESSAGE": "INVALID_FORMAT"}, status=400)

            UserModel.objects.create(
                nickname     =   data.get('nickname'),
                email        =   email,
                password     =   hashed_password.decode('UTF-8'),
                phone_number =   data['phone_number'],
            )
            return JsonResponse({"MESSAGE": "SUCCESS"}, status=201)

        except KeyError:
            return JsonResponse({"MESSAGE": "KEY_ERROR"}, status=400)

class SignInView(View):
    def post(self, request):
        try:
            data     = json.loads(request.body)      
            email    = data['email'] 
            password = data['password']        

            if not UserModel.objects.filter(email = email).exists():
                return JsonResponse({'MESSAGE':'INVALID_VALUE'}, status = 401)

            if bcrypt.checkpw(password.encode('utf-8'),UserModel.objects.get(email=email).password.encode('utf-8')):
                token = jwt.encode({'id':UserModel.objects.get(email=data['email']).id}, SECRET_KEY, algorithm=algorithm)
                return JsonResponse({'TOKEN':token}, status = 200)

            return JsonResponse({'MESSAGE':'INVALID_USER'}, status=401)

        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status = 400)
