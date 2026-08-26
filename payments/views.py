import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def airtel_disbursement_callback(request):
    if request.method != "POST":
        return JsonResponse(
            {"error": "Only POST requests are allowed"},
            status=405
        )

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse(
            {"error": "Invalid JSON"},
            status=400
        )

    print("Airtel Disbursement Callback:")
    print(data)

    # TODO:
    # 1. Identify the VPesa transaction
    # 2. Verify the Airtel callback
    # 3. Check the transaction status
    # 4. Update the VPesa transaction
    # 5. Update the wallet balance only after confirmed success

    return JsonResponse({"status": "received"}, status=200)