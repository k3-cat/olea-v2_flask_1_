from hashlib import sha3_256

import magic

from enums import Dep, MangoType

MIME_MTYPE = {
    'text/plain': MangoType.text,
    'audio/flac': MangoType.audio_flac,
    'audio/wav': MangoType.audio_wav,
    'image/png': MangoType.picture_png,
    'image/jpeg': MangoType.picture_jpg,
    'video/x-matroska': MangoType.video_mkv,
    'video/mp4': MangoType.video_mp4
}


def special_save(f, path: str) -> (bytes, MangoType):
    hasher = sha3_256()
    with open(path, 'wb') as tf:
        chunk = f.read(4096)
        tf.write(chunk)
        hasher.update(chunk)
        mime: str = magic.from_buffer(chunk, mime=True)
        while True:
            chunk = f.read(4096)
            if not chunk:
                break
            hasher.update(chunk)
            tf.write(chunk)

    fp = hasher.digest()
    mtype = MIME_MTYPE[mime] if mime in MIME_MTYPE else MangoType.unknown
    return fp, mtype


TYPE_ALLOWED = {
    Dep.d51: (MangoType.audio_flac, ),
    Dep.d52: (MangoType.audio_flac, ),
    Dep.d59: (MangoType.audio_flac, ),
    Dep.d60: (MangoType.picture_png, ),
    Dep.d71: (MangoType.audio_flac, ),
    Dep.d72: (MangoType.text, ),
    Dep.d73: (MangoType.video_mkv, MangoType.video_mp4)
}


def is_allowed_type(dep: Dep, mtype: MangoType) -> bool:
    return mtype in TYPE_ALLOWED[dep]


EXTS = {
    MangoType.audio_flac: 'flac',
    MangoType.picture_png: 'png',
    MangoType.text: 'txt',
    MangoType.video_mkv: 'mkv',
    MangoType.video_mp4: 'mp4'
}
