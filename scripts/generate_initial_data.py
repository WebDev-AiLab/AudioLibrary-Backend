from pages.models import Page
from django.core.exceptions import ObjectDoesNotExist


def run():

    # generate important pages
    pages_to_generate = ['submit', 'faq']
    for page in pages_to_generate:
        try:
            Page.objects.get(slug=page)
        except ObjectDoesNotExist:
            Page.objects.create(
                slug=page,
                title=page.upper(),
                content='Replace Me With The Actual Text',
                is_deletable=False
            )
