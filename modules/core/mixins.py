from django.views.generic.base import TemplateView
from .models import CommonInfo, SimplePage
from .forms import FeedbackForm


class TemplateViewMixin(TemplateView):
    def get_context_data(self, **kwargs):
        context = super(TemplateViewMixin, self).get_context_data(**kwargs)
        context.update({
            'common_info': CommonInfo.objects.first(),
            'feedback_form': FeedbackForm(),
            'about': SimplePage.objects.first()
        })
        return context
