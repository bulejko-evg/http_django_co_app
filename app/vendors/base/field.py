from typing import Any
from django.db import models
from django.conf import settings
from django.utils.safestring import mark_safe
from django.utils.html import format_html_join
from django.utils.translation import get_language
from app.vendors.helpers.image import resize_image
from django.db.models.fields.files import (
    FieldFile, 
    ImageFieldFile,
)
from app.vendors.helpers.validations import (
    validate_json_names,
    validate_json_descriptions,
)
from app.vendors.helpers import (
    get_url_file,
    get_path_file,
    get_format_html_img_tag,
    get_value_from_dict,
)


class KeyLanguageCodeDict(dict):
    """Dict for json field with key as language code"""
    __getattr__ = dict.get
    __setattr__ = dict.__setattr__
    __delattr__ = dict.__delattr__

    def __setitem__(self, key, item):
        """
        Set Item with check keys.
        If key is not in settings.LANGUAGES_CODES raise ValueError
        """
        if key not in settings.LANGUAGES_CODES:
            raise ValueError("Invalid language code")
        self.__dict__[key] = item

    @property
    def inst_in_current_language(self):
        """Get instance in current language"""
        return get_value_from_dict(self, by_key=get_language())
    
    @property
    def format_html_br(self):
        """Get value in format html with separator <br>"""
        _sep = mark_safe("<br>")
        _format = "({}) {}"
        return format_html_join(_sep, _format, ((k, v) for k, v in self.items()))


class KeyLanguageCodeDictJsonField(models.JSONField):
    """Custom JsonField with default dict KeyLanguageCodeDict"""
    def __init__(self, *args, **kwargs):
        kwargs["default"] = KeyLanguageCodeDict
        super().__init__(*args, **kwargs)

    def from_db_value(self, value, expression, connection):
        """Get value from db"""
        db_val = super().from_db_value(value, expression, connection)

        if db_val is None:
            return db_val
        return KeyLanguageCodeDict(**db_val)

    def get_prep_value(self, value):
        dict_value = value
        prep_value = super().get_prep_value(dict_value)
        return prep_value


class NamesJsonField(KeyLanguageCodeDictJsonField):
    """Custom JsonField for field names"""
    description = "Names in json. key is language code"

    def __init__(self, *args, **kwargs):
        kwargs["validators"] = [validate_json_names]
        super().__init__(*args, **kwargs)


class DescriptionsJsonField(KeyLanguageCodeDictJsonField):
    """Custom JsonField for field descriptions"""
    description = "Description in json. key is language code"

    def __init__(self, *args, **kwargs):
        kwargs["validators"] = [validate_json_descriptions]
        super().__init__(*args, **kwargs)


class ExtFileMixin:
    """File mixin"""
    @property
    def extension(self):
        return self.name.split('.')[-1]
    
    def is_empty(self):
        return self._file is None


class ExtImageFieldFile(ExtFileMixin, ImageFieldFile):
    """
    Custom ImageFieldFile file.
    Properties:
        extension (): get file extension
    Methods:
        get_html_img_tag ():
            Get html tag <img> with src from self.url or default image by key
            with any tags for img tag
        resize(): Resize image to width and save
        is_empty (): get file is None
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_html_img_tag(
            self,
            width: int = settings.IMAGE_WIDTH["thumbnail"],
            or_def_by_key: str = settings.DEFAULT_IMAGE_KEY,
            **tags,
        ):
        """
        Get image in html tag img.
        --------------------------
        Parameters:
            width (int): width for html tag <img>, default settings.IMAGE_WIDTH["thumbnail"]
            or_def_by_key (str): key for default image if self.url is incorrect
            **tags: any tags for <img>
        Returns:
            (str): html tag <img> with src self.url or default image by key
        """
        url = get_url_file(self, or_def_by_key=or_def_by_key)
        return get_format_html_img_tag(src=url, width=width, **tags)

    def resize(self, width: int) -> Any | None:
        """Resize image to width and save"""
        if self:
            if img_path := get_path_file(self):
                new_img = resize_image(img_path, width)
                if new_img:
                    return new_img.save(img_path)


class ExtImageField(models.ImageField):
    """Custom ImageField (with get_html_img, resize)"""
    attr_class = ExtImageFieldFile

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)



class ExtFieldFile(ExtFileMixin, FieldFile):
    """
    Custom FieldFile file.
    ----------------------
    Properties:
        extension (): get file extension
    Methods:
        is_empty (): get file is None
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    

class ExtFieldFile(models.FieldFile):
    """Custom FieldFile"""
    attr_class = ExtFieldFile

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)