"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True))),
]

'''
graphql/ maps the URL endpoint /graphql to the Django application's GraphQL view.
The csrf_exempt decorator is used to disable Django's Cross-Site Request Forgery (CSRF)
protection for this specific URL, which is often necessary for non-browser-based API clients.
graphiql=True enables the GraphiQL interface, a web-based IDE for exploring and testing
GraphQL APIs.
'''
