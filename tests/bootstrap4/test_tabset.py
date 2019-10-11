import pytest
from django.template.context import RequestContext
from cms.api import add_plugin
from cms.plugin_rendering import ContentRenderer
from django.utils.html import strip_spaces_between_tags, strip_tags
from cms.utils.plugins import build_plugin_tree
from cmsplugin_cascade.models import CascadeElement
from cmsplugin_cascade.bootstrap4.tabs import BootstrapTabSetPlugin


@pytest.fixture
@pytest.mark.django_db
def bootstrap_tabset(rf, admin_site, bootstrap_column):
    request = rf.get('/')
    column_plugin, column_model = bootstrap_column

    # add tabset plugin
    tabset_model = add_plugin(column_model.placeholder, BootstrapTabSetPlugin, 'en', target=column_model)
    assert isinstance(tabset_model, CascadeElement)
    tabset_plugin = tabset_model.get_plugin_class_instance(admin_site)
    assert isinstance(tabset_plugin, BootstrapTabSetPlugin)
    ModelForm = tabset_plugin.get_form(request, tabset_model)
    data = {
              "num_children": 1, 
              "hide_plugin": False,
              "extra_css_classes":[
                "nav-tabs"
              ],
              "justified":False,
            }
    assert 'extra_css_classes' in list(ModelForm.declared_fields)
    assert 'nav-tabs' in list(ModelForm.declared_fields['extra_css_classes'])
    assert 'nav-tabs' in list(ModelForm.declared_fields['extra_css_classes'].__dict__)
    form = ModelForm(data, None, instance=tabset_model)
    assert form.is_valid()
    assert 'nav-tabs' in form['glossary']
    tabset_plugin.save_model(request, tabset_model, form, False)
    return tabset_plugin, tabset_model


@pytest.mark.django_db
def test_edit_tabset(rf, admin_site, bootstrap_tabset):
    request = rf.get('/')
    tabset_plugin, tabset_model = bootstrap_tabset
    ModelForm = tabset_plugin.get_form(request, tabset_model)
    data = {
              "num_children": 1, 
              "hide_plugin": False,
              "extra_css_classes":[
                "nav-tabs"
              ],
              "justified":False,
            }
    assert 'extra_css_classes' in list(ModelForm.declared_fields)
    assert 'nav-tabs' in list(ModelForm.declared_fields['extra_css_classes'])
    assert 'nav-tabs' in list(ModelForm.declared_fields['extra_css_classes'].__dict__)
    form = ModelForm(data, None, instance=tabset_model)
    assert form.is_valid()
    assert ('nav-tabs', 'nav-tabs') in form['extra_css_classes']._choices
    assert 'extra_inline_styles:border-radius' in form_fields.keys()
    tabset_plugin.save_model(request, tabset_model, form, False)
