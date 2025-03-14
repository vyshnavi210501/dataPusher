import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from accounts.models import Account,Log
from django.utils.timezone import now

@csrf_exempt
def receive_data(request):
    try:
        event_id=request.headers.get('CL-X-EVENT-ID')
        data=json.loads(request.body.decode('utf-8'))
        required_fields = ["event_id", "account_id", "received_data"]

        if not all(field in data for field in required_fields):
            return JsonResponse("error-Missing fields")
        try:
            account = Account.objects.get(account_id=data["account_id"])
        except Account.DoesNotExist:
            return JsonResponse({"error": "Invalid account_id"}, status=400)

        # Store Data in Log
        Log.objects.create(
            event_id=event_id,
            account_id=account, 
            received_timestamp=now(),
            processed_timestamp=None, 
            received_data=data["received_data"],
            status="SUCCESS",  # Default status
        )


        return JsonResponse({"message": "Data received successfully"})
    
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)
