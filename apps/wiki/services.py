from django.utils.text import slugify


def create_unique_slug(model_class, value):
    slug = slugify(value)
    unique_slug = slug
    number = 1

    while model_class.objects.filter(slug=unique_slug).exists():
        unique_slug = f'{slug}-{number}'
        number += 1

    return unique_slug
