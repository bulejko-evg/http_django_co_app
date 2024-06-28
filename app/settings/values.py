import string


EMPTY_VALUE = "_"

NUMBER_PER_PAGE = 15

LENGTH = {
    "alias": {"min": 3, "max": 30},
    "username": {"min": 3, "max": 30},
    "email": {"min": 5, "max": 30},
    "password": {"min": 8, "max": 16},
    "name": {"min": 4, "max": 50},
    "description": {"min": 10, "max": 300},
    "comment": {"min": 5, "max": 300},
    "slug": {"min": 4, "max": 50},
    "url": {"min": 5, "max": 300},
    "tag": {"min": 3, "max": 30},
    "link": {"min": 3, "max": 500},
    "meta": {
        "keywords": {"min": 3, "max": 120},
        "description": {"min": 10, "max": 150},
        "author": {"min": 3, "max": 80},
    },
}

CACHE_TIME = {
    "minute": 60 * 60,
    "hour": 60 * 60 * 60,
    "day": 60 * 60 * 60 * 24,
}

CACHE_TIME_DEFAULT = CACHE_TIME["day"] * 100

USER_AGE = {"min": 4, "max": 111}
BIRTHDAY_TIMEDELTA_YEARS = 100
DATE_FORMAT = "%Y-%m-%d"

DEFAULT_FILES = {
    "img_placeholder": "images/default/placeholder.png",
    "img_logo": "images/default/logo.png",
    "img_icon": "images/default/icon.png",
    "img_user": "images/default/user.png",
}

IMAGE_WIDTH = {
    "icon": 40,
    "thumbnail": 80,
    "showcase": 220,
    "slider": 600,
    "logo": 120,
    "user": 120,
}

pdf = ("pdf", "application/pdf", "PDF document")
png = ("png", "image/png", "PNG")
jpg = ("jpg", "image/jpeg", "JFIF")
jpeg = ("jpeg", "image/jpeg", "JFIF")
ico = ("ico", "image/vnd.microsoft.icon", None)
mp3 = ("mp3", "audio/mpeg", None)
mp4 = ("mp4", "video/mp4", None)
svg = ("svg", "image/svg+xml", None)
txt = ("txt", "text/plain", "ASCII")
doc = ("doc", "application/msword", "Microsoft Word")
docx = ("docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "OpenXML")
zip = ("zip", "application/zip", "ZIP")
xls = ("xls", "application/vnd.ms-excel", "Excel")
xlsx = ("xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "OpenXML")
xml = ("xml", "application/xml", "XML")
rar = ("rar", "application/vnd.rar", "RAR")
csv = ("csv", "text/csv", "CSV")

FILE_SIZE_ONE_MB = 1048576
FILE_STRICT_CHECKING = True
FILE_BYTE_TO_CHECK = 2048
FILE_SIZES = {
    "icon": FILE_SIZE_ONE_MB,
    "image": FILE_SIZE_ONE_MB * 10,
    "thumb": FILE_SIZE_ONE_MB * 5,
    "video": FILE_SIZE_ONE_MB * 50,
    "audio": FILE_SIZE_ONE_MB * 10,
    "doc": FILE_SIZE_ONE_MB * 20,
}
FILE_TYPES = {
    "icon": [png, ico],
    "image": [png, jpeg, jpg],
    "thumb": [png, svg],
    "video": [mp4],
    "audio": [mp3],
    "doc": [txt, pdf, doc, docx],
}

RESIZABLE_IMAGES = ["png", "jpeg", "jpg"]

CHARACTERS_FOR_PASSWORD = (
    string.ascii_lowercase,
    string.ascii_uppercase,
    string.digits,
    string.punctuation,
)

SVG = {
    "block": (
        '<svg xmlns="http://www.w3.org/2000/svg"'
        ' width="16" height="16" '
        'fill="red" '
        'viewBox="0 0 16 16">'
        '<path d="M15 8a6.97 6.97 0 0 0-1.71-4.584l-9.874 9.875A7 7 '
        "0 0 0 15 8M2.71 12.584l9.874-9.875a7 7 0 0 0-9.874 9.874ZM16"
        ' 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0"/>'
        "</svg>"
    )
}
