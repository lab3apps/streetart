from __future__ import unicode_literals
import base64
import hashlib
import os


def default(thumbnailer, prepared_options, source_filename,
            thumbnail_extension, **kwargs):
    """
    Overriding Easy-thumbnails' default name processor.

    For example: ``source.jpg.cropped.jpg``
    """
    filename_parts = [source_filename]
    filename_parts.append('cropped_image')
    if thumbnail_extension != os.path.splitext(source_filename)[1][1:]:
        filename_parts.append(thumbnail_extension)
    return '.'.join(filename_parts)