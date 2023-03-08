from django.forms import forms
from DjangoUeditor.forms import UEditorField


class ContentForm(forms.Form):
    body = UEditorField("", height=600, width=600, toolbars='besttome')