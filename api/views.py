from django.http import JsonResponse
from django.shortcuts import render
from core.utils import extract_data, get_item_info, check_item_is_shill
# Create your views here.
def scan_item(request, item_id):
    context = {'is_shill': False, 'error': 'Request did not complete, try again later'}
    try:
        #check the item using the loaded model
        item_data = extract_data(get_item_info(item_id))
        detected_data = check_item_is_shill(item_data)
        context = {'is_shill': detected_data, 'error': False}
    except:
        context = {'is_shill': False, 'error': 'Request did not go through, try another product'}
    return JsonResponse(context, safe=True)