from django import forms
from django.contrib.auth.models import Group
from jnt_admin_tools.fields import PermissionSelectMultipleField


class GroupAdminForm(forms.ModelForm):
    permissions = PermissionSelectMultipleField(required=False)

    class Meta:
        model = Group
        fields = "__all__"
