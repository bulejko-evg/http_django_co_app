from django import forms
from django.db.models import Q
from django_ckeditor_5.widgets import CKEditor5Widget
from django.utils.translation import gettext_lazy as _
from app.vendors.base.widget import (
    NamesTabsWidget,
    DescriptionsTabsWidget,
)


class NamesDescriptionsTabsByLangMixin:
    """Widgets for names, descriptions tabs json fields, form mixin."""
    __slots__ = ()

    class Meta:
        widgets = {
            "names": NamesTabsWidget(
                attrs={
                    "cols": 40,
                    "rows": 2
                },
            ),
            "descriptions": DescriptionsTabsWidget(
                attrs={
                    "cols": 40,
                    "rows": 10
                },
            ),
        }


class RichTextMixin:
    """Rich text form mixin."""
    __slots__ = ()

    class Meta:
        widgets = {
            "rich_text": CKEditor5Widget(
                attrs={
                    "cols": 40,
                    "rows": 20
                },
                config_name="extends",
            ),
        }


class TreePositionFormMixin:
    """Form mixin for set position field for TreeMixin."""

    def set_position_choices(self, *args, **kwargs):
        inst = kwargs.get("instance", None)
        if inst is not None:
            parent_q = Q(parent_id=inst.parent_id) if inst.parent else Q(parent__isnull=True)
            cnt = type(inst).objects.filter(parent_q).count()
        else:
            _model = self._meta.model
            cnt = _model.objects.filter(parent__isnull=True).count()

        choices = [(i, str(i)) for i in range(1, cnt + 1)]
        choices.append((0, _("Last"),))
        _disabled = True if len(choices) <= 1 else False

        self.fields["position"] = forms.ChoiceField(
            choices=choices,
            required=False,
            disabled=_disabled,
        )
