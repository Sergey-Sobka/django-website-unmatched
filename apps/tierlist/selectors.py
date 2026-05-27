from collections import OrderedDict

from .models import TierListEntry


def tier_list(mode='1v1'):
    result = OrderedDict(
        (
            ('S', []),
            ('A', []),
            ('B', []),
            ('C', []),
            ('D', []),
        )
    )

    entries = TierListEntry.objects.select_related(
        'character',
        'updated_by',
    ).filter(
        mode=mode
    ).order_by('tier', 'character__name')

    for entry in entries:
        result[entry.tier].append(entry)

    return result
