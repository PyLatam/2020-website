from langdetect import detect

from django.utils.text import slugify, Truncator

from .models import Talk, Speaker


def import_from_json(data):
    existing = frozenset(Talk.objects.values_list('title', flat=True))

    for raw_proposal in data:
        if raw_proposal['title'] in existing:
            continue

        if raw_proposal['state'] != 'accepted':
            continue

        speaker = Speaker.objects.get_or_create(
            name=raw_proposal['name'],
            email=raw_proposal['email'],
        )[0]

        talk_title = raw_proposal['title']
        talk_language = detect(raw_proposal['abstract'])

        Talk.objects.create(
            slug=slugify(Truncator(talk_title).chars(50)),
            title=talk_title,
            language=talk_language,
            abstract=raw_proposal['abstract'],
            description=raw_proposal['description'],
            audience_level=raw_proposal['audience_level'].lower(),
            speaker=speaker,
            room=f'room_{talk_language}',
        )
