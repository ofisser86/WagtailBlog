from django.db import models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailcore import blocks
from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsearch import index
from wagtail.wagtailimages.blocks import ImageChooserBlock


class BlogPage(Page):
    body = StreamField([
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
    ])
    author = models.CharField(max_length=255, default='admin')
    main_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
        FieldPanel('author'),
        FieldPanel('date'),
        ImageChooserPanel('main_image'),
        FieldPanel('intro'),

    ]


class BlogIndexPage(Page):
        intro = RichTextField(blank=True)
        @property
        def blogs(self):
            # Получить список страниц блога, которые являются потомками этой страницы
            blogs = BlogPage.objects.live().descendant_of(self)

            # Сортировать по дате
            blogs = blogs.order_by('-date')

            return blogs

        def get_context(self, request):
            blogs = self.blogs

            # Пагинация
            page = request.GET.get('page')
            # Показывать 9 постов
            paginator = Paginator(blogs, 9)
            try:
                blogs = paginator.page(page)
            except PageNotAnInteger:
                blogs = paginator.page(1)
            except EmptyPage:
                blogs = paginator.page(paginator.num_pages)

        # Обновить контекст шаблона
            context = super(BlogIndexPage, self).get_context(request)
            context['blogs'] = blogs
            # Обновить контекст шаблона
            return context


        content_panels = Page.content_panels + [
                 FieldPanel('intro', classname="full")
        ]
