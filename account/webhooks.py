import json
import stripe
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def my_webhook_view(request):
    payload = request.body
    event = None

    try:
        event = stripe.Event.construct_from(
            json.loads(payload), stripe.api_key
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)

    print(event.data.object.customer)
    print(event.data.object.plan.id)

    if event.type == 'customer.subscription.created':
        pass

    # Handle the event
    # if event.type == 'charge.succeeded':
    #     # profile = Profile.objects.get(user=request.user)
    #     # profile.paid = True
    #     # profile.save()
    #     # print(request.user)
    #     # print("succeeded")
    #     payment_sun = PaymentSun.objects.all()
    #     for user in payment_sun:
    #         if user.payment_id == event.data.object.id:
    #             profile = Profile.objects.get(user=user.user)
    #             profile.paid = True
    #             profile.save()
    #
    # elif event.type == 'charge.failed':
    #     print("Failed payment")
    #     pass
    # # ... handle other event types
    # else:
    #     # Unexpected event type
    #     return HttpResponse(status=400)

    return HttpResponse(status=200)

