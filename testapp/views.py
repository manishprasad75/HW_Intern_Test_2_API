from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Profile
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


# Create your views here.


@csrf_exempt
def DetailApi(request):
    data = request.body
    try:
        data = json.loads(data)
    except ValueError:
        json_data = {'msg': 'Please provide valid json data'}
        return JsonResponse(json_data)

    user_id = data.get('user_id')
    data = Profile.objects.filter(id=user_id).first()

    if data:
        p_data = {
            'email': data.user.email,
            'first_name': data.user.first_name,
            'last_name': data.user.last_name,
            'favorites': data.favorites
        }
        return JsonResponse(p_data)
    json_data = ({'msg': 'Resource Not Found'})
    return JsonResponse(json_data)



def AddFavouriteAPI(request):
    data = request.body
    try:
        data = json.loads(data)
    except ValueError:
        json_data = {'msg': 'Please provide valid json data'}
        return JsonResponse(json_data)

    user_id = data.get('user_id', None)
    favorite = data.get('favorite', None)

    if user_id is None or favorite is None or len(favorite) == 0:
        json_data = {'msg': 'Please provide user_id and favorite'}
        return JsonResponse(json_data)


    data = Profile.objects.filter(id=user_id).first()
    # import pdb
    # pdb.set_trace() 
    if data:
        p_data = {
            'favorites': data.favorites
        }
        print(p_data)
        p_data["favorites"]["list"].append(favorite)
        print(p_data)
        p_data = json.dumps(p_data)
        data.favorite = p_data
        data.save()
        json_data = {'msg': "Added Successfully"}
        return JsonResponse(json_data)
    json_data = ({'msg': 'Resource Not Found'})
    return JsonResponse(json_data)




def RemoveFavouriteAPI(request):
    data = request.body
    try:
        data = json.loads(data)
    except ValueError:
        json_data = {'msg': 'Please provide valid json data'}
        return JsonResponse(json_data)
    
    user_id = data.get('user_id', None)
    favorite = data.get('favorite', None)

    if user_id is None or favorite is None or len(favorite) == 0:
        json_data = {'msg': 'Please provide user_id and favorite'}
        return JsonResponse(json_data)

    data = Profile.objects.filter(id=user_id).first()
    # import pdb
    # pdb.set_trace()
    if data:
        p_data = {
            'favorites': data.favorites
        }
        print(p_data)
        try:
            p_data["favorites"]["list"].remove(favorite)
        except :
            json_data = {'msg': 'Please provide valid favorite'}
            return JsonResponse(json_data)

        p_data = json.dumps(p_data)
        data.favorite = p_data
        data.save()
        json_data = {'msg': "Remove Successfully"}
        return JsonResponse(json_data)
    json_data = ({'msg': 'Resource Not Found'})
    return JsonResponse(json_data)




