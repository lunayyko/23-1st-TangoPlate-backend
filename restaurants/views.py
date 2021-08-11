from django.views           import View
from django.http            import JsonResponse
from django.db.models       import Avg, Q
from django.core.exceptions import FieldError

from restaurants.models     import Restaurant
from reviews.models         import Review, ReviewImage
from users.models           import WishList
from users.utils            import login_decorator

class RestaurantDetailView(View):
    def get(self, request, restaurant_id):
        try:
            if not Restaurant.objects.filter(id = restaurant_id).exists():
                return JsonResponse({"MESSAGE": "NOT_EXIST"}, status=404)
                
            restaurant         = Restaurant.objects.get(id = restaurant_id)
            
            results = []
            results.append({
                "id"             : restaurant.id,
                "name"           : restaurant.name,
                "rating"         : restaurant.review_set.all().aggregate(rating = Avg('rating'))['rating'],
                "restaurant_img" : restaurant.review_set.last().reviewimage_set.last().image,
                "address"        : restaurant.address,
                "phone_number"   : restaurant.phone_number,
                "category"       : restaurant.category.name,
                "location"       : restaurant.location.area,
                "serving_price"  : restaurant.serving_price.price,
                "menus" : [{   
                    "menu_id"    : menu.id,
                    "item"       : menu.item, 
                    "item_price" : menu.item_price
                } for menu in restaurant.menu_set.all()],
                # "is_wished"      : WishList.objects.filter(user_id=request.user.id).exists() if request.user is not None else False,
                #  wish_count
                "reviews"         : [{
                    "id"  : review.id,
                    "user" : {
                        "email" : review.user.email,
                        "id" : review.user.id,
                        "name"  : review.user.nickname,
                    },
                    "description": review.description,
                    "rating"     : review.rating,
                    "created_at" : review.created_at,
                    "images_url" : review.reviewimage_set.last().image,
                } for review in restaurant.review_set.all()]
            })
            return JsonResponse({"results": results}, status=200)

        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status = 400)

class RestaurantListView(View):
    def get(self, request):
        try:
            category_id       = request.GET.get("categoryId")
            location_id       = request.GET.get("locationId")
            serving_price_id  = request.GET.get("servingPriceId")

            q = Q()

            if category_id:
                q &= Q(category_id = category_id)

            if location_id:
                q &= Q(location_id = location_id)

            if serving_price_id:
                q &= Q(serving_price_id = serving_price_id)

            restaurants = [{
                    "id"          : restaurant.id,
                    "name"        : restaurant.name,
                    "image"       : restaurant.review_set.filter(restaurant_id=restaurant.id)[0].reviewimage_set.last().image,
                    "rating"      : restaurant.review_set.all().aggregate(rating = Avg('rating'))['rating'],
                    "address"     : restaurant.address,
                    "is_wished"   : restaurant.wishlist_set.exists(),
                    "btn_toggle"  : False,
                    "review_id"   : restaurant.review_set.all().order_by('-created_at')[0].id,
                    "user_id"     : restaurant.review_set.all().order_by('-created_at')[0].user_id,
                    "user_name"   : restaurant.review_set.all().order_by('-created_at')[0].user.nickname,
                    "description" : restaurant.review_set.all().order_by('-created_at')[0].description,
                } for restaurant in Restaurant.objects.filter(q).order_by('name')]
            return JsonResponse({"restaurant" : restaurants}, status=200)

        except FieldError:
            return JsonResponse({"RESULT" : "FILTER_ERROR"}, status=404)
