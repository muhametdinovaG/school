from django.contrib import admin
from modules.core.forms import *
from .models import *


@admin.register(Category)
class Category(admin.ModelAdmin):
    form = CategoryModel


class ManagerInline(admin.TabularInline):
    model = ManagerNote
    form = ManagerNoteModel
    extra = 1
    formset = RequiredInlineFormSet


@admin.register(Manager)
class Manager(admin.ModelAdmin):
    form = ManagerModel
    list_display = ['name']
    inlines = [
        ManagerInline,
    ]


class ReviewInline(admin.TabularInline):
    model = CourseReview
    form = CourseReviewModel
    extra = 1


class AuditoryInline(admin.TabularInline):
    model = CourseAuditory
    form = CourseAuditoryModel
    extra = 1
    max_num = 4
    formset = RequiredInlineFormSet


class SkillsInline(admin.TabularInline):
    model = CourseSkills
    form = CourseSkillsModel
    extra = 1
    max_num = 6
    formset = RequiredInlineFormSet


class CatalogInline(admin.TabularInline):
    model = CourseCatalog
    form = CourseCatalogModel
    extra = 1
    formset = RequiredInlineFormSet


@admin.register(Course)
class Course(admin.ModelAdmin):
    save_on_top = True
    form = CourseModel
    list_display = ['headline']
    prepopulated_fields = {'alias': ('headline',)}
    inlines = [
        AuditoryInline,
        SkillsInline,
        CatalogInline,
        ReviewInline,
    ]


@admin.register(SimplePage)
class SimplePage(admin.ModelAdmin):
    form = SimplePageModel
    list_display = ['title']
    prepopulated_fields = {'about_alias': ('title',)}


@admin.register(CommonInfo)
class CommonInfo(admin.ModelAdmin):
    form = CommonInfoModel
    fieldsets = (
        (None, {
            'fields': ('headline', 'description',)
        }),
        ('Контакты', {
            'fields': ('number', 'address', 'map', 'vk_link', 'inst_link')
        }),
        ('Футер', {
            'fields': ('footer_text', 'contract_offer', 'privacy_policy',)
        })
    )


@admin.register(GalleryPic)
class GalleryPicAdmin(admin.ModelAdmin):
    form = GalleryPicModel

    # Добавляет все файлы из формы галереи кроме последнего
    def save_model(self, request, obj, form, change):
        super(GalleryPicAdmin, self).save_model(request, obj, form, change)
        keys = request.FILES.keys()
        for key in keys:
            if 'pic' in key:
                for n, f in enumerate(request.FILES.getlist(key)):
                    if n == len(request.FILES.getlist(key)) - 1:
                        break
                    GalleryPic.objects.create(pic=f)
        return obj
