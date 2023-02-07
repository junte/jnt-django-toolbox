from django import forms
from django.utils.encoding import force_str

from jnt_django_toolbox.helpers import media


class FlagsArrayWidget(forms.CheckboxSelectMultiple):
    class Media:
        css = {
            "all": ["jnt_django_toolbox/css/widgets/flags-array.css"],
        }
        js = (
            *media.js_jquery(),
            "jnt_django_toolbox/js/widgets/flags-array.js",
        )

    template_name = "jnt_django_toolbox/widgets/flags_array.html"

    def render(
        self,
        name,
        value,  # noqa: WPS110
        attrs=None,
        choices=(),
        renderer=None,
    ):
        attrs = attrs or {}
        attrs.setdefault("class", "")

        if isinstance(value, int):
            real_value = []
            div = 2
            for choice_key, _choice_value in self.choices:
                if value % div != 0:  # noqa: S001
                    real_value.append(choice_key)
                    value -= value % div  # noqa: S001 WPS524 WPS110
                div *= 2
            value = real_value  # noqa: WPS110
        return super().render(name, value, attrs=attrs)

    def _has_changed(self, initial, data):  # noqa: WPS110
        if initial is None:
            initial = []
        if data is None:
            data = []  # noqa: WPS110
        if initial != data:
            return True
        initial_set = {force_str(initial_value) for initial_value in initial}
        data_set = {force_str(data_value) for data_value in data}
        return data_set != initial_set
