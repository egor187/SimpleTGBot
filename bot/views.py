from django.conf import settings
from django.views import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
import requests
from .core import BaseBot
import json
from django.views.decorators.csrf import csrf_exempt


@method_decorator(csrf_exempt, name='dispatch')
class WebhookView(View):
    """Handle bot behavior regardless to incoming tg update"""

    @staticmethod
    def get_payload(request):
        print(request)
        message = request.get('message')
        contact = message.get('contact')
        if message and contact:
            return {'phone': contact['phone_number'], 'login': message.get('from', {}).get('username')}

    def post(self, request):
        message = json.loads(request.body)
        BaseBot(settings.BOT_TOKEN).process_update(message)
        payload = self.get_payload(message)
        if payload:
            try:
                requests.post(settings.RECEIVER_URL, json=payload).raise_for_status()
            except requests.exceptions.HTTPError:
                JsonResponse({'status': 'external service error'})
        return JsonResponse({'status': 'ok'})
