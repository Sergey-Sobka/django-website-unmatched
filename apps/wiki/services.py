from django.utils.text import slugify


def create_unique_slug(model_class, value):
    slug = slugify(value)
    existing_slugs = set(
        model_class.objects.filter(
            slug__startswith=slug
        ).values_list('slug', flat=True)
    )

    if slug not in existing_slugs:
        return slug

    number = 1

    while f'{slug}-{number}' in existing_slugs:
        number += 1

    return f'{slug}-{number}'
