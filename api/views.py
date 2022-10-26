from django.http import JsonResponse

def getRoutes(request):

   routes = [
       {'GET':'/api/shop'},
       {'GET':'/api/shop/id'},

   ]
   return JsonResponse(routes, safe=False)