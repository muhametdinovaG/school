from django.urls import path
from modules.core.views import *
from django.views.decorators.csrf import csrf_protect

urlpatterns = [
    path('', PageViewHome.as_view(), name='home'),
    path('course/<slug:alias>/', PageViewCourse.as_view(), name='course'),
    path('gallery/', PageViewGallery.as_view(), name='gallery'),
    path('contacts/', PageViewContacts.as_view(), name='contacts'),
    path('page/<slug:about_alias>/', PageViewSimplePage.as_view(), name='about_alias'),
    path('feedback/', csrf_protect(FeedbackView.as_view()), name='feedback')
]
