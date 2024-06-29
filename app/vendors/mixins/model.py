from django.db import models
from django.conf import settings
from django.contrib import admin
from django.utils import timezone
from django.core.cache import cache
from django.db.models.functions import Mod
from django_ckeditor_5.fields import CKEditor5Field
from django.utils.translation import gettext_lazy as _
from app.vendors.helpers import get_choices_of_languages
from django.utils.html import (
    format_html,
    mark_safe,
)
from app.vendors.base.field import (
    ExtImageField,
    NamesJsonField,
    DescriptionsJsonField,
)
from app.vendors.helpers.validations import (
    validate_file_thumb,
    validate_svg_html,
)
from django.db.models import (
    F,
    Q,
    Max,
    Min,
)
from typing import (
    Any,
    Tuple,
    List,
)


class TimestampsMixin(models.Model):
    """
    A date and time of creation and update mixin.
    ---------------------------------------------
    Attributes:
        created_at (models.DateTimeField): a date and time of creation
        updated_at (models.DateTimeField): a date and time of updation
    """
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        abstract = True


@admin.action(description=_("Mark selected as soft deleted"))
def make_soft_delete(modeladmin, request, queryset):
    queryset.update(deleted_at=timezone.now())


@admin.action(description=_("Mark selected as not soft deleted"))
def make_not_soft_delete(modeladmin, request, queryset):
    queryset.update(deleted_at=None)


class SoftDeleteMixin(models.Model):
    """
    A date and time of soft deletion mixin.
    ---------------------------------------
    Attributes:
        deleted_at (models.DateTimeField): a date and time of deletion
    Properties:
        deleted: get (bool) the deleted_at is None
    Methods:
        delete (soft=False): delete or soft delete 
        is_actual (): get tuple, is the model item actual (deleted_at is None), with fail messages (list[str])
    Admin:
        soft_deleted_actions: model soft delete actions
    """
    deleted_at = models.DateTimeField(
        blank=True,
        null=True
    )

    @property
    def deleted(self) -> bool:
        """Get the deleted_at is None."""
        return self.deleted_at is not None
    
    @deleted.setter
    def deleted(self, val: bool) -> None:
        """Set deleted_at as timezone.now or None."""
        self.deleted_at = timezone.now() if val is True else None

    class Meta:
        abstract = True
    
    def delete(self, soft=False, **kwargs) -> None:
        """Delete or soft delete."""
        if soft is True:
            self.deleted_at = timezone.now()
        super().delete(soft=soft, **kwargs)
    
    def is_actual(self) -> Tuple[bool, List[str]]:
        """
        Get (tuple) is the model item actual (bool, deleted_at is None), 
        with fail messages (list[str])."""
        is_actual, fail_messages = super().is_actual()
        if self.deleted_at is not None:
            is_actual = False
            fail_messages.append(_("Deleted"))
        
        return is_actual, fail_messages
    
    soft_deleted_actions = [
        make_soft_delete,
        make_not_soft_delete,
    ]


class RolePermissionsMixin(models.Model):
    """
    Permissions for model by roles.
    --------------------------------
    Attributes:
        _permissions (dict): {<app name:mode name>:{<role name>:[list os permissions] or "__all__"str}}
    Methods:
        get_permissions (): get attribute _permissions or empty dict
        __set
    """
    # dict permissions for roles: {<app name:mode name>:{<role name>:[list os permissions] or "__all__"str}}
    _permissions = {}

    class Meta:
        abstract = True
    
    def get_permissions(self) -> dict:
        """Get _permissions attribute or empty dict."""
        return getattr(self, "_permissions", {})
    
    def __setattr__(self, name: str, value: Any) -> None:
        """Prohibit attribute _permissions changes."""
        """Запретить изменение аттрибута """
        if name == "_permissions":
            return
        return super().__setattr__(name, value)



class NamesDescriptionsMixin(models.Model):
    """
    Names and Descriptions Mixin. 
    JsonFields with dict in which key is a language code.
    -----------------------------------------------------
    Attributes:
        names (NamesJsonField): Custom JsonField
        descriptions (DescriptionsJsonField): Custom JsonField
    Properties:
        name: get name in current language
        description: get description in current language
    Admin:
        names_to_format_html: display names in format html with separator <br>
        names_descriptions_fieldsets: names and descriptions fieldsets
    """

    names = NamesJsonField()
    descriptions = DescriptionsJsonField(
        null=True,
        blank=True,
    )

    @property
    def name(self):
        """Get name in current language"""
        return self.names.inst_in_current_language

    @property
    def description(self):
        """Get description in current language"""
        return self.descriptions.inst_in_current_language

    class Meta:
        abstract = True

    @admin.display(description=_("Names"))
    def names_format_html_via_br(self):
        """Get names via <br>"""
        return self.names.format_html_br

    names_display = (
        "names_format_html_via_br",
    )

    names_descriptions_fieldsets = (
        "names",
        "descriptions",
    )


class MetaDataMixin(models.Model):
    """
    Metadata for SEO Mixin.
    ------------------------
    Attributes:
        meta_keywords (models.CharField): meta keywords
        meta_description (models.CharField): meta description
        meta_author (models.CharField): meta author
    Admin:
        meta_data_fieldsets: meta_keywords, meta_description, meta_author fieldsets
    """

    meta_keywords = models.CharField(
        max_length=settings.LENGTH["meta"]["keywords"]["max"],
        null=True,
        blank=True,
    )
    meta_description = models.CharField(
        max_length=settings.LENGTH["meta"]["description"]["max"],
        null=True,
        blank=True,
    )
    meta_author = models.CharField(
        max_length=settings.LENGTH["meta"]["author"]["max"],
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True

    meta_data_fieldsets = (
        "meta_keywords",
        "meta_description",
        "meta_author",
    )


class OwnerMixin(models.Model):
    """
    Owner Mixin.
    -------------
    Attributes:
        created (models.ForeignKey): account who created
        updated (models.ForeignKey): account who updated
    """
    created = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        related_name="%(class)_created",
        on_delete=models.SET_NULL,
    )
    updated = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        related_name="%(class)_updated",
        on_delete=models.SET_NULL,
    )

    class Meta:
        abstract = True


class LanguageRichTextMixin(models.Model):
    """
    Language code, rich text mixin.
    -------------------------------
    Attributes:
        lang (models.CharField): language code
        rich_text (models.TextField): Rich text
    Properties:
        safe_rich_text: get rich_text in mark_safe and format_html
    Admin:
        language_rich_text_fieldsets: language code and text fieldsets
    """

    lang = models.CharField(
        default=settings.LANGUAGE_CODE,
        max_length=8,
        choices=get_choices_of_languages(),
    )
    rich_text = CKEditor5Field(
        config_name="extends",
        blank=True,
        null=True,
    )

    @property
    def safe_rich_text(self):
        return mark_safe(format_html(self.rich_text))

    class Meta:
        abstract = True

    language_rich_text_fieldsets = (
        "lang",
        "rich_text",
    )


class TreeMixin(models.Model):
    """
    Three fields mixin (nested set).
    ---------------------------------
    Attributes:
        parent (ForeignKey by self): parent node id
        left (SmallIntegerField): left node index
        right (SmallIntegerField): right node index
        level (SmallIntegerField): node level
        position (SmallIntegerField): position node in children set
    Properties:
        with_lower: get self with lower nodes
        lower: get lower nodes
        parents: get node parents
        branch: get branch of node (parents, self and lower nodes)
    Methods:
        get_all (class method): get tree nodes
        get_lower(by_depth: int = 1): get lower nodes by depth
        get_with_lower(by_depth: int = 1): get self with lower nodes by depth
        create_tree_node: create node
        update_tree_node: update node
        delete_tree_node: delete node
        check_tree (class method): check tree for test
    Admin:
        tree_fieldsets: parent, position fieldsets
    """

    left = models.SmallIntegerField(
        blank=True,
        null=True,
    )
    right = models.SmallIntegerField(
        blank=True,
        null=True,
    )
    level = models.SmallIntegerField(
        blank=True,
        null=True,
    )
    position = models.SmallIntegerField(
        blank=True,
        null=True,
    )
    parent = models.ForeignKey(
        verbose_name=_("Parent"),
        to="self",
        blank=True,
        null=True,
        related_name="children",
        on_delete=models.CASCADE,
    )

    @property
    def with_lower(self):
        """Get self with lower"""
        return (
            type(self)
            .objects.actual()
            .filter(left__gte=self.left, right__lte=self.right)
            .order_by("left")
        )

    @property
    def lower(self):
        """Get lower"""
        return (
            type(self)
            .objects.actual()
            .filter(left__gt=self.left, right__lt=self.right)
            .order_by("left")
        )

    @property
    def parents(self):
        """Get parents nodes of node"""
        return (
            type(self)
            .objects.actual()
            .filter(left__lte=self.left, right__gte=self.right)
            .order_by("left")
        )

    @property
    def branch(self):
        """Get branch of node"""
        return (
            type(self)
            .objects.actual()
            .filter(right__gt=self.left, left__lt=self.right)
            .order_by("left")
        )

    class Meta:
        abstract = True

    @classmethod
    def get_all(cls):
        """Get all tree node"""
        return cls.objects.actual().order_by("left")

    def get_lower(self, by_depth: int = 1):
        """Get lower nodes by depth (default depth is 1)"""
        by_level = self.level + 1 + by_depth
        return (
            type(self)
            .objects.actual()
            .filter(left__gt=self.left, right__lt=self.right, level__lt=by_level)
            .order_by("left")
        )

    def get_with_lower(self, by_depth: int = 1):
        """Get self with lower nodes by depth (default depth is 1)"""
        by_level = self.level + 1 + by_depth
        return (
            type(self)
            .objects.actual()
            .filter(left__gte=self.left, right__lte=self.right, level__lt=by_level)
            .order_by("left")
        )

    def create_tree_node(self):
        """Create tree node"""
        if self.parent_id:
            parent = type(self).objects.filter(pk=self.parent_id).first()
            level = parent.level + 1 if parent else 1
            if self.position:
                near = (
                    type(self)
                    .objects.filter(parent=parent, level=level, position=self.position)
                    .first()
                )
                if near:
                    right = near.left
                    position = near.position
            else:
                right = parent.right if parent else 1
                position = parent.children.count() + 1 if parent else 1
        else:
            level = 1
            if self.position:
                near = (
                    type(self)
                    .objects.filter(level=level, position=self.position)
                    .first()
                )
                if near:
                    right = near.left
                    position = near.position
            else:
                max_right = type(self).objects.aggregate(Max("right", default=None))
                right = (
                    max_right["right__max"] + 1
                    if max_right["right__max"] is not None
                    else 1
                )
                position = type(self).objects.filter(level=level).count() + 1

        # Update the keys, the nodes behind the parent node:
        offset = 2
        type(self).objects.filter(left__gt=right).update(
            left=F("left") + offset, right=F("right") + offset
        )

        if self.parent_id:
            # Update the parent branch:
            type(self).objects.filter(right__gte=right, left__lt=right).update(
                right=F("right") + offset
            )

        if self.position:
            parent_q = (
                Q(parent_id=self.parent_id)
                if self.parent_id
                else Q(parent__isnull=True)
            )
            type(self).objects.filter(parent_q).filter(
                level=level, position__gt=position
            ).update(right=F("position") + 1)

        # Update data of new node
        self.left = right
        self.right = right + 1
        self.level = level
        self.position = position

    def update_tree_node(self):
        """Update tree node"""
        node = type(self).objects.filter(pk=self.id).first()

        if node.parent_id == self.parent_id and node.position == self.position:
            # A tree is not updated
            return

        if self.parent_id:
            parent = type(self).objects.filter(id=self.parent_id).first()
            level = parent.level + 1
            right = parent.right - 1
            if self.position:
                near = (
                    type(self)
                    .objects.filter(
                        parent_id=parent.id, level=level, position=self.position
                    )
                    .first()
                )
                if near:
                    right_key_near = near.right
            else:
                right_key_near = right
        else:
            level = 1
            max_right = type(self).objects.aggregate(Max("right", default=None))
            right = max_right["right__max"]
            if self.position:
                near = (
                    type(self)
                    .objects.filter(level=level, position=self.position)
                    .first()
                )
                if near:
                    right_key_near = near.right
            else:
                right_key_near = right

        offset = node.right - node.left + 1

        changeable = type(self).objects.filter(
            left__gte=node.left, right__lte=node.right
        )

        if right_key_near < node.left:
            offset_edit = right_key_near - node.left + 1

            # update right
            type(self).objects.filter(
                right__lt=node.left, right__gt=right_key_near
            ).update(right=F("right") + offset)
            # update left
            type(self).objects.filter(
                left__lt=node.left, left__gt=right_key_near
            ).update(left=F("left") + offset)
            # update changeable branch
            type(self).objects.filter(pk__in=changeable).update(
                left=F("left") + offset_edit,
                right=F("right") + offset_edit,
                level=F("level") + level,
            )
        if right_key_near > node.right:
            offset_edit = right_key_near - node.left + 1 - offset

            # update right
            type(self).objects.filter(
                right__gt=node.right, right__lte=right_key_near
            ).update(right=F("right") - offset)
            # update left
            type(self).objects.filter(
                left__lt=node.left, left__gt=right_key_near
            ).update(left=F("left") - offset)
            # update changeable branch
            type(self).objects.filter(pk__in=changeable).update(
                left=F("left") + offset_edit,
                right=F("right") + offset_edit,
                level=F("level") + level,
            )

        if self.position:
            parent_q = (
                Q(parent_id=self.parent_id)
                if self.parent_id
                else Q(parent__isnull=True)
            )
            type(self).objects.filter(parent_q).filter(
                level=level, position__gt=self.position
            ).update(right=F("position") + 1)

    def delete_tree_node(self):
        """Delete tree node"""
        right = self.right
        left = self.left
        offset = right - left + 1

        # Delete node or branch
        type(self).objects.filter(left__gte=left, right__lte=right).delete()

        # Update the parent branch:
        type(self).objects.filter(right__gt=right, left__lt=left).update(
            right=F("right") - offset
        )

        # Updating lower-level nodes:
        type(self).objects.filter(left__gt=right).update(
            left=F("left") - offset, right=F("right") - offset
        )

    @classmethod
    def check_tree(cls):
        """Check tree in test"""
        left_gr_right = cls.objects.filter(left__gte=F("right"))
        if len(left_gr_right):
            raise ValueError("Some left gr right")

        left_min = cls.objects.aggregate(Min("left", default=None))
        right_max = cls.objects.aggregate(Max("right", default=None))
        count = cls.objects.count()

        if left_min and left_min["left__min"] != 1:
            raise ValueError("Min left != 1")
        if right_max and right_max["right__max"] / count != 2:
            raise ValueError("Max right / count != 2")

        rem_div = cls.objects.annotate(rmd=Mod(F("right") - F("left"), 2)).filter(rmd=0)
        rem_dif = cls.objects.annotate(rmd=Mod(F("left") - F("level") + 2, 2)).filter(
            rmd=1
        )

        if len(rem_div):
            raise ValueError("Some MOD((left - right) / 2) != 0")

        if len(rem_dif):
            raise ValueError("Some MOD((left – level + 2) / 2) != 1")

        not_uniq = cls.objects.raw(
            """
            SELECT t1.id,
                COUNT(t1.id) AS rep,
                MAX(t3.right) AS max_right
            FROM %(table_name)s AS t1, %(table_name)s AS t2, %(table_name)s AS t3
            WHERE t1.left <> t2.left
            AND t1.left <> t2.right
            AND t1.right <> t2.left
            AND t1.right <> t2.right
            GROUP BY t1.id
            HAVING max_right <> SQRT(4 * rep + 1) + 1
            """
            % {"table_name": cls._meta.db_table}
        )

        if len(not_uniq):
            raise ValueError("Not unique left or right")

    tree_fieldsets = (
        "parent",
        "position",
    )


def get_thumbnail_save_url(instance, filename) -> str:
    """Get url for save thumbnail file"""
    return f"{instance.get_instance_media_path()}/thumb/{filename}"


class ThumbMixin(models.Model):
    """
    Thumbnail Mixin. Image file, or svg (html), or None (hidden).
    -------------------------------------------------------------
    Attributes:
        thumb_file (ExtImageField): Custom file field
        svg_html (models.TextField): text field for svg html str
        thumb_type (TextChoices): file, svg (html) or hidden
    Properties:
        is_thumb_hidden (): is thmbnail hidden
        is_thumb_file (): is thmbnail file
        is_thumb_svg (): is thmbnail svg html str
    Admin:
        thumb_img: display thumbnail by type (image, svg html or hidden)
        thumb_fieldsets: thumb_file svg_html thumb_type fieldsets
    )
    Required:
        In model add method: get_thumb_path -> return path: str
    """

    class ThumbType(models.TextChoices):
        FILE = "FILE", _("File (image or svg)")
        SVG = "SVG", _("SVG (html)")
        HIDDEN = "HIDDEN", _("Hidden")

    thumb_file = ExtImageField(
        upload_to=get_thumbnail_save_url,
        null=True,
        blank=True,
        validators=[validate_file_thumb],
    )
    _svg_html = models.TextField(
        db_column="svg_html",
        null=True,
        blank=True,
        validators=[validate_svg_html],
    )
    thumb_type = models.CharField(
        max_length=15,
        choices=ThumbType.choices,
        default=ThumbType.HIDDEN,
        verbose_name=(_("Thumbnail type")),
    )

    @property
    def is_thumb_hidden(self):
        """Get bool, self.type_ is HIDDEN"""
        return self.thumb_type == self.ThumbType.HIDDEN

    @property
    def is_thumb_file(self):
        """Get bool, self.type_ is FILE"""
        return self.thumb_type == self.ThumbType.FILE

    @property
    def is_thumb_svg(self):
        """Get bool, self.type_ is SVG (html)"""
        return self.thumb_type == self.ThumbType.SVG
    
    @property
    def safe_svg_html(self):
        return mark_safe(format_html(self._svg_html))

    class Meta:
        abstract = True

    @admin.display(description=_("Thumbnail"))
    def thumb_img(self):
        """Get thumbnail image or svg icon or None."""
        if self.is_thumb_svg and self.svg_html:
            return format_html(self.svg_html)
        elif self.is_thumb_file:
            return self.thumb_file.get_html_img_tag(
                width=settings.IMAGE_WIDTH["thumbnail"],
                or_def_by_key="img_placeholder", 
                alt="thumbnail"
            )
        return None

    thumb_fieldsets = (
        "thumb_file",
        "svg_html",
        "thumb_type",
    )
    thumb_display = (
        "thumb_img",
    )


class CacheMixin(models.Model):
    """
    Cache mixin.
    ------------
    Methods:
        get_from_cache (by_key: str, prefix: str, postfix: str, **kwargs):
            get cache by key, with prefix and postfix
            kwargs is parameters for method cache_queryset
        delete_cache (by_key: str, prefix: str, postfix: str):
            delete cache by key with prefix and postfix
    Required:
        In model add class method: cache_queryset(**kwargs) -> queryset for cache
    """

    @classmethod
    def get_from_cache(cls, by_key: str = "", prefix: str = "", postfix: str = "", **kwargs) -> Any:
        """
        Get result of queryset from cache by key.
        -----------------------------------------
        Parameters:
            by_key (str): cache key, if empty key is class name, default empty str,
            prefix (str): cache key prefix, default empty str
            postfix (str): cache key postfix, default empty str
            **kwargs: parameters for cache_queryset method
        Methods:
            delete_cache (): delete cache by key
        Returns:
            result from queryset: from class method cache_queryset
        """
        _by_key = cls._get_cache_key(by_key, prefix, postfix)
        res = cache.get(_by_key, None)
        if res is None:
            res = cls.cache_queryset(**kwargs)
        return res

    def delete_cache(self, by_key: str = "", prefix: str = "", postfix: str = "") -> None:
        """
        Parameters:
            by_key (str): cache key, if empty key is class name, default empty str,
            prefix (str): cache key prefix, default empty str
            postfix (str): cache key postfix, default empty str
        Returns:
            _
        """
        _by_key = type(self)._get_cache_key(by_key, prefix, postfix)
        cache.delete(_by_key)

    class Meta:
        abstract = True

    @classmethod
    def _get_cache_key(cls, by_key: str = "", prefix: str = "", postfix: str = "") -> str:
        """
        Get cache key. if by_key is empty, key is class name.
        -----------------------------------------------------
        Parameters:
            by_key (str): cache key, if empty key is class name, default empty str,
            prefix (str): cache key prefix, default empty str
            postfix (str): cache key postfix, default empty str
        Returns:
            (str): prefix + _ + cache_key + _ + postfix
        """
        _by_key = by_key or cls.__name__.upper()
        _prefix = f"{prefix}_" or ""
        _postfix = f"_{postfix}" or ""
        return f"{prefix}{_by_key}{postfix}"