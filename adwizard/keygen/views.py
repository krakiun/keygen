from django.http import Http404
from django.utils import timezone
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import status
from keygen.models import Key
from keygen.serializers import KeySerializer


# An endpoint for the root
@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'status': reverse('status', request=request, format=format),
        'get': reverse('get', request=request, format=format),
    })


class Status(APIView):

    def get(self, request, format=None):
        """Current quantity of available free keys"""
        total_free = Key.objects.filter(status='status_free').count()
        return Response(total_free)


class KeyView(APIView):
    def get_object(self, code):
        try:
            return Key.objects.get(code=code)
        except Key.DoesNotExist:
            raise Http404

    def get(self, request, code, format=None):
        """Current status of key (free/issued/expired)"""
        key = self.get_object(code)
        serialized_key = KeySerializer(key)
        return Response(serialized_key.data['status'])

    def put(self, request, code, format=None):
        """Kill issued key"""
        key = self.get_object(code)
        if key.status == 'status_expired' or (not key.issued):
            return Response(_('Key has been already killed or not yet issued to be killed'),
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            key.status = 'status_expired'
            key.expired = timezone.now()
            key.save()
            serialized_key = KeySerializer(key, data=request.data)
        if serialized_key.is_valid():
            serialized_key.save()
            return Response(serialized_key.data)
        return Response(serialized_key.errors,
                        status=status.HTTP_400_BAD_REQUEST)


class GetKey(APIView):
    def get(self, request, format=None):
        """ Get free key"""
        free_keys = Key.objects.filter(status='status_free')
        if free_keys:
            key = free_keys[0]
            key.status = 'status_issued'
            key.issued = timezone.now()
            key.save()
            serialized_key = KeySerializer(key)
            return Response(serialized_key.data['code'])
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)


def index(request):
    example_key = reverse('key_view', kwargs={'code': 'aBc1'})
    example_get_key = reverse('get_key')
    example_status = reverse('status')
    context = {'example_key': request.build_absolute_uri(example_key),
               'example_get_key': request.build_absolute_uri(example_get_key),
               'example_status': request.build_absolute_uri(example_status),
               'doc_link': settings.DOC_LINK}
    return render(request, 'home.html', context)
