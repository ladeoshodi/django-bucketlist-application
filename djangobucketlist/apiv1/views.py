from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View


class IndexView(View):

    def get(self, request):
        return HttpResponse("success")
