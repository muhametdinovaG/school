import logging

from django.shortcuts import get_object_or_404

from modules.core.mixins import TemplateViewMixin
from modules.core.models import *
from configs.settings import FEEDBACK_EMAIL
from django.http import JsonResponse
from django.core.mail.message import EmailMultiAlternatives
from .forms import FeedbackForm
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url

LOGGER = logging.getLogger(__name__)


class PageViewHome(TemplateViewMixin):
    """
    Страница `Главная`
    """
    template_name = 'main/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['courses'] = Course.objects.all()
        return context


class PageViewContacts(TemplateViewMixin):
    """
    Страница `Контакты`
    """
    template_name = 'main/contacts.html'


class PageViewGallery(TemplateViewMixin):
    """
    Страница `Галерея`
    """
    template_name = 'main/gallery.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['slides'] = GalleryPic.objects.all()
        return context


class PageViewCourse(TemplateViewMixin):
    """
    Страница `Курс`
    """
    template_name = 'main/course.html'

    def get_alias(self):
        alias = self.kwargs.get('alias')

    def get_context_data(self, alias, **kwargs):
        alias = self.get_alias()
        course = None

        if alias is not None:
            try:
                course = Course.objects.get(alias=alias)
            except Course.DoesNotExist:
                course = None
        LOGGER.debug('Clean page: {0}'.format(course))

        context = super().get_context_data(**kwargs)

        category = Category.objects.first()

        course = get_object_or_404(Course, alias__iexact=self.kwargs['alias'])

        context.update({
            'category': category,
            'course': course,
        })

        return context


class PageViewSimplePage(TemplateViewMixin):
    """
    Страница `О школе`
    """
    template_name = 'main/simple_page.html'

    def get_alias(self):
        about_alias = self.kwargs.get('about_alias')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['about'] = SimplePage.objects.first()
        return context


class PageNotFoundView(TemplateViewMixin):
    """
    Страница `Ошибка 404`
    """
    template_name = 'main/404.html'

    def dispatch(self, request, *args, **kwargs):
        response = super(PageNotFoundView, self).dispatch(request, *args, **kwargs)
        response.status_code = 404
        return response


class PageServerErrorView(TemplateViewMixin):
    """
    Страница `Ошибка 500`
    """
    template_name = 'main/500.html'

    def dispatch(self, request, *args, **kwargs):
        response = super(PageServerErrorView, self).dispatch(request, *args, **kwargs)
        response.status_code = 500
        return response


class FeedbackView(TemplateViewMixin):
    """
    Отправка на email
    """
    template_name = 'main/inclusion/modal.html'

    def post(self, request, *args, **kwargs):
        form = FeedbackForm(self.request.POST)
        cptch_key = CaptchaStore.generate_key()
        cptch_image = captcha_image_url(cptch_key)
        if form.is_valid():
            send_email(FEEDBACK_EMAIL, form.cleaned_data['phone_number'])
            return JsonResponse(data={'status': 'ok', 'cptch_key': cptch_key, 'cptch_image': cptch_image})
        else:
            return JsonResponse(data={'status': 'error', 'error': form.errors, 'cptch_key': cptch_key, 'cptch_image': cptch_image}, status=403)


def send_email(to, phone_number):
    description = 'Номер телефона для связи: <br>{}'.format(phone_number)
    title = 'Новая заявка с сайта "Школа UTV"'
    msg = EmailMultiAlternatives(title, description, to=to)
    msg.attach_alternative(description, 'text/html')
    msg.send()
