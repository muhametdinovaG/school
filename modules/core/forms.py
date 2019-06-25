from django import forms

from modules.core.templates.main.widgets import MultiImageInput
from .models import *
from captcha.fields import CaptchaField
from django.core.exceptions import ValidationError
from django.forms.models import BaseInlineFormSet

"""
    Раздел `Общая информация`
"""


class CommonInfoModel(forms.ModelForm):
    class Meta:
        save_on_top = True
        model = CommonInfo
        fields = "__all__"
        widgets = {
            'headline': forms.TextInput(attrs={'size': 50}),
            'alias': forms.TextInput(attrs={'size': 50}),
            'description': forms.Textarea(attrs={'rows': 2, 'cols': 100}),
            'footer_text': forms.Textarea(attrs={'rows': 3, 'cols': 100}),
            'number': forms.TextInput(attrs={'size': 50}),
            'address': forms.TextInput(attrs={'size': 50}),
            'map': forms.Textarea(attrs={'rows': 3, 'cols': 100}),
            'vk_link': forms.TextInput(attrs={'size': 50}),
            'inst_link': forms.TextInput(attrs={'size': 50})
        }


"""
    Раздел `Категории`
"""


class CategoryModel(forms.ModelForm):
    class Meta:
        save_on_top = True
        model = Category
        fields = "__all__"
        widgets = {
            'text_other': forms.Textarea(attrs={'rows': 3, 'cols': 150}),
            'text_your': forms.Textarea(attrs={'rows': 3, 'cols': 150})
        }


"""
    Раздел `Преподаватели`
"""


class ManagerModel(forms.ModelForm):
    """
    Преподаватель
    """
    class Meta:
        save_on_top = True
        model = Manager
        fields = "__all__"
        widgets = {
            'name': forms.TextInput(attrs={'size': 50}),
            'post': forms.TextInput(attrs={'size': 50})
        }


class ManagerNoteModel(forms.ModelForm):
    """
    Заметки о преподавателе
    """
    class Meta:
        model = ManagerNote
        fields = "__all__"
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 2, 'cols': 100})
        }


"""
    Раздел `Курсы`
"""


class CourseModel(forms.ModelForm):
    """
    Основная инфа по курсу
    """
    class Meta:
        save_on_top = True
        model = Course
        fields = "__all__"
        widgets = {
            'headline': forms.TextInput(attrs={'size': 50}),
            'alias': forms.TextInput(attrs={'size': 50}),
            'description': forms.Textarea(attrs={'rows': 2, 'cols': 100}),
            'video': forms.TextInput(attrs={'size': 50}),
            'schedule': forms.Textarea(attrs={'rows': 2, 'cols': 100}),
            'cost_headlone': forms.TextInput(attrs={'size': 50}),
            'cost_text': forms.Textarea(attrs={'rows': 2, 'cols': 100})
        }


class CourseCatalogModel(forms.ModelForm):
    """
    Уроки в учебном плане
    """
    class Meta:
        model = CourseCatalog
        fields = "__all__"
        widgets = {
            'text': forms.Textarea(attrs={'rows': 2, 'cols': 50})
        }


class CourseAuditoryModel(forms.ModelForm):
    """
    Заметки о курсе
    """
    class Meta:
        model = CourseAuditory
        fields = "__all__"
        widgets = {
            'headline': forms.TextInput(attrs={'size': 50}),
            'text': forms.Textarea(attrs={'rows': 3, 'cols': 50})
        }


class CourseSkillsModel(forms.ModelForm):
    """
    Преимущества
    """
    class Meta:
        model = CourseSkills
        fields = "__all__"
        widgets = {
            'headline': forms.TextInput(attrs={'size': 50}),
            'text': forms.Textarea(attrs={'rows': 3, 'cols': 50})
        }


class CourseReviewModel(forms.ModelForm):
    """
    Отзывы
    """
    class Meta:
        model = CourseReview
        fields = "__all__"
        widgets = {
            'name': forms.TextInput(attrs={'size': 50}),
            'text': forms.Textarea(attrs={'rows': 3, 'cols': 50})
        }


"""
    Раздел `Изображения для галереи`
"""


class GalleryPicModel(forms.ModelForm):
    class Meta:
        model = GalleryPic
        fields = "__all__"
        widgets = {
            'pic': MultiImageInput(),
        }


"""
    Раздел `Простые страницы`
"""


class SimplePageModel(forms.ModelForm):
    class Meta:
        save_on_top = True
        model = SimplePage
        fields = "__all__"
        widgets = {
            'title': forms.TextInput(attrs={'size': 50}),
            'about_alias': forms.TextInput(attrs={'size': 50})
        }


class FeedbackForm(forms.Form):
    """
    Форма отправки заявки
    """
    phone_number = forms.CharField()
    captcha = CaptchaField()


class RequiredInlineFormSet(BaseInlineFormSet):
    """
    Дополнительная валидация для связанных объектов у курса и преподавателя
    """
    def clean(self):
        super(RequiredInlineFormSet, self).clean()
        non_empty_forms = 0
        for form in self:
            if form.cleaned_data:
                non_empty_forms += 1
        print(non_empty_forms)
        if non_empty_forms < 2:
            raise ValidationError("Пожалуйста, заполните данные в формах. Нужно заполнить минимум 2 записи.")

        if self.deleted_forms:
            if non_empty_forms - len(self.deleted_forms) < 2:
                raise ValidationError("Удаление невозможно! Для корректного отображения на сайте требуется минимум 2 записи.")
