from whitenoise.storage import CompressedManifestStaticFilesStorage


class ForgivingManifestStaticFilesStorage(CompressedManifestStaticFilesStorage):
    """WhiteNoise's compressed, cache-busting storage, minus the crashes.

    The bundled theme CSS (static/assets/**) references several hundred fonts
    and images that were never shipped. With the stock storage that makes
    ``collectstatic`` abort, and any ``{% static %}`` tag pointing at a
    missing file raise a 500 when DEBUG is off.

    Here a missing file is left un-hashed instead: the URL was already
    broken before, so nothing regresses, but deploys and pages keep working.
    """

    manifest_strict = False

    def hashed_name(self, name, content=None, filename=None):
        try:
            return super().hashed_name(name, content, filename)
        except ValueError:
            return name
