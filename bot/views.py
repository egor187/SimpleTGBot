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
    def parse_number(request):
        message = json.loads(request.body)
        if message.get('message') and message.get('message').get('contact'):
            return message.get('message').get('contact')['phone_number']

    def post(self, request):
        message = json.loads(request.body)
        BaseBot(settings.BOT_TOKEN).process_update(message)
        contact = self.parse_number(request)
        if contact:
            try:
                requests.post(settings.RECEIVER_URL, json=message.get('message').get('contact')['phone_number']).raise_for_status()
            except requests.exceptions.HTTPError:
                JsonResponse({'status': 'external service error'})
        return JsonResponse({'status': 'ok'})
