from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.urls import reverse
from pytils import translit
from embed_video.fields import EmbedVideoField
from django.core.exceptions import ValidationError


class CommonInfo(models.Model):

    def get_file_path(self, filename):
        split_name = filename.split('.')
        name, extension = split_name[:-1], split_name[-1]
        path = ''.join(["files/", translit.slugify(name[:80]), ".", extension])
        return path

    def file_size(self):
        if self.size > 5242880:
            raise ValidationError('Выбранный файл слишком большой. Максимально допустимы размер файла 5 MB.')

    headline = models.CharField('Заголовок в шапке', max_length=50, default=None, help_text='Максимальное кол-во символов: 50')
    description = models.CharField('Описание в шапке', max_length=205, default=None, help_text='Максимальное кол-во символов: 205')
    footer_text = models.TextField('Текст в футере')
    contract_offer = models.FileField('Договор оферты', upload_to=get_file_path, validators=[file_size], help_text='Максимальный размер файла 5 MB', default=None)
    privacy_policy = models.FileField('Политика конфиденциальности', upload_to=get_file_path, validators=[file_size], help_text='Максимальный размер файла 5 MB', default=None)
    number = models.CharField('Номер телефона', max_length=20, default=None)
    address = models.TextField('Адрес')
    map = models.TextField('Карта', help_text='Cгенерированный код на сайте https://yandex.ru/map-constructor/')
    vk_link = models.TextField('Ссылка на страницу ВК', help_text='Ссылка должна начинаться с https://')
    inst_link = models.TextField('Ссылка на страницу инстаграм', help_text='Ссылка должна начинаться с https://')

    class Meta:
        verbose_name = 'Общая информация'
        verbose_name_plural = 'Общая информация'


class Category(models.Model):

    headline_other = models.CharField('Заголовок', max_length=20, help_text='Максимальное кол-во символов: 20')
    text_other = RichTextUploadingField('Описание', max_length=1000, help_text='Максимальное кол-во символов: 1000')
    headline_your = models.CharField('Заголовок', max_length=20, help_text='Максимальное кол-во символов: 20')
    text_your = RichTextUploadingField('Описание', max_length=1000, help_text='Максимальное кол-во символов: 1000')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Manager(models.Model):

    def get_image_path(self, filename):
        split_name = filename.split('.')
        name, extension = split_name[:-1], split_name[-1]
        path = ''.join(["manager_photo/", translit.slugify(name), ".", extension])
        return path

    name = models.CharField('Имя и фамилия', max_length=36, help_text='Максимальное кол-во символов: 36')
    post = models.CharField('Должность', max_length=50, help_text='Максимальное кол-во символов: 50')
    photo_manager = models.ImageField('Фото', upload_to=get_image_path, default=None, help_text='Рекомендуемое разрешение: 305x536 px; изображение в формате png')

    class Meta:
        verbose_name = 'Преподаватель'
        verbose_name_plural = 'Преподаватели'

    def __str__(self):
        return self.name


class ManagerNote(models.Model):

    notes = models.TextField('Заметка')
    manager = models.ForeignKey(Manager, related_name='manager_note', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Заметка о преподавателе'
        verbose_name_plural = 'Заметки о преподавателе'


class Course(models.Model):

    def get_image_path(self, filename):
        split_name = filename.split('.')
        name, extension = split_name[:-1], split_name[-1]
        path = ''.join(["stub_photo/", translit.slugify(name), ".", extension])
        return path

    def file_size(self):
        if self.size > 1048576:
            raise ValidationError('Выбранный файл слишком большой. Максимально допустимы размер файла 1 MB.')

    headline = models.CharField('Название', max_length=50, help_text='Максимальное кол-во символов: 50')
    alias = models.SlugField('Псевдоним', max_length=225, unique=True)
    description = models.CharField('Описание', max_length=205, help_text='Максимальное кол-во символов: 205')
    stub = models.ImageField('Фоновое изображение', upload_to=get_image_path, validators=[file_size], default=None, help_text='Максимальный размер файла 1 MB; изображение формата 16:9')
    manager = models.ForeignKey('core.Manager', verbose_name='Преподаватель', null=True, related_name='manager_cours', on_delete=models.SET_NULL)
    video = EmbedVideoField(verbose_name='Видео', default=None)
    schedule = models.TextField('Продолжительность курса', default=None)
    cost_headlone = models.CharField('Стоимость (заголовок)', max_length=60, default=None, help_text='Максимальное кол-во символов: 60')
    cost_text = models.TextField('Стоимость (описание)', default=None)
    reviews_visible = models.BooleanField('Показать отзывы?', default=False)
    children = models.BooleanField('Детский?', default=False)

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'

    def get_absolute_url(self):
        return reverse('course', args=[str(self.alias)])


class CourseReview(models.Model):

    def get_image_path(self, filename):
        split_name = filename.split('.')
        name, extension = split_name[:-1], split_name[-1]
        path = ''.join(["review_picture/", translit.slugify(name), ".", extension])
        return path

    course = models.ForeignKey(Course, related_name='cours_review', on_delete=models.CASCADE)
    picture = models.ImageField('Фото рецензента', upload_to=get_image_path, default=None, help_text='Рекомендуемое разрешение: 126x126 px')
    name = models.CharField('Имя и фамилия', max_length=35, help_text='Максимальное кол-во символов: 35')
    text = models.CharField('Описание от рецензента', max_length=215, default=None, help_text='Максимальное кол-во символов: 215')

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class CourseAuditory(models.Model):

    def get_image_path(self, filename):
        split_name = filename.split('.')
        name, extension = split_name[:-1], split_name[-1]
        path = ''.join(["icon/", translit.slugify(name), ".", extension])
        return path

    course = models.ForeignKey(Course, related_name='auditory_cours', on_delete=models.CASCADE)
    icon = models.ImageField('Логотип', upload_to=get_image_path, default=None, help_text='Рекомендуемое разрешение: 105x105 px; изображение в формате png')
    headline = models.CharField('Заголовок', max_length=45, help_text='Максимальное кол-во символов: 45')
    text = models.CharField('Описание', max_length=265, default=None, help_text='Максимальное кол-во символов: 265')

    class Meta:
        verbose_name = 'Заметка о курсе'
        verbose_name_plural = 'Заметки о курсе'


class CourseCatalog(models.Model):

    course = models.ForeignKey(Course, related_name='catalog_cours', on_delete=models.CASCADE)
    text = models.TextField('Название урока')

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'


class CourseSkills(models.Model):

    def get_image_path(self, filename):
        split_name = filename.split('.')
        name, extension = split_name[:-1], split_name[-1]
        path = ''.join(["picture/", translit.slugify(name), ".", extension])
        return path

    def file_size(self):
        if self.size > 1048576:
            raise ValidationError('Выбранный файл слишком большой. Максимально допустимы размер файла 1 MB.')

    course = models.ForeignKey(Course, related_name='skills_cours', on_delete=models.CASCADE)
    picture = models.ImageField('Фоновое изображение', upload_to=get_image_path, validators=[file_size], help_text='Максимальный размер файла 1 MB; изображение формата 16:9')
    headline = models.CharField('Заголовок', max_length=55, help_text='Максимальное кол-во символов: 55')
    text = models.CharField('Описание', max_length=215, help_text='Максимальное кол-во символов: 215')

    class Meta:
        verbose_name = 'Преимущество'
        verbose_name_plural = 'Преимущества'


class GalleryPic(models.Model):

    def get_image_path(self, filename):
        split_name = filename.split('.')
        name, extension = split_name[:-1], split_name[-1]
        path = ''.join(["gallery/", translit.slugify(name), ".", extension])
        return path

    pic = models.ImageField('Файл', upload_to=get_image_path, help_text='Максимальный размер файла 1 MB; рекомендуемое разрешение 1200x900 пикселей')

    class Meta:
        verbose_name = 'Изображение для галереи'
        verbose_name_plural = 'Изображения для галереи'


class SimplePage(models.Model):

    def get_image_path(self, filename):
        split_name = filename.split('.')
        name, extension = split_name[:-1], split_name[-1]
        path = ''.join(["about__picture/", translit.slugify(name), ".", extension])
        return path

    title = models.TextField('Заголовок', default=None)
    about_alias = models.SlugField('Псевдоним', max_length=225, unique=True)
    text = RichTextUploadingField('Описание', default=None)

    class Meta:
        verbose_name = 'Простая страница'
        verbose_name_plural = 'Простые страницы'

    def get_absolute_url(self):
        return reverse('about_alias', args=[str(self.about_alias)])

