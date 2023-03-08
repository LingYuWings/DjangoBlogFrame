from django.forms import forms
from DjangoUeditor.forms import UEditorField


class ContentForm(forms.Form):
    body = UEditorField("", height=500, width=830, toolbars='besttome')