from django import forms
from django import template



register = template.Library()


@register.filter(name='field_type')
def field_type(bound_field):
    return bound_field.field.widget.__class__.__name__


@register.filter(name='input_class')
def input_class(bound_field):
    css_class = ''
    if bound_field.form.is_bound:
        if bound_field.errors:
            css_class = 'is-invalid'
        elif field_type(bound_field) != 'PasswordInput':
            css_class = 'is-valid'
    return 'form-control {}'.format(css_class)

    
@register.filter(name='is_checkbox')
def is_checkbox(field):
    """
    Boolean filter for form fields to determine if a field is using a checkbox
    widget.
    """
    return isinstance(field.field.widget, forms.CheckboxInput)