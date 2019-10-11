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
    form = ModelForm(data, None, instance=tabset_model)
    assert form.is_valid()
    assert 'nav-tabs' in form.base_fields['extra_css_classes']
    tabset_plugin.save_model(request, tabset_model, form, False)
    return tabset_plugin, tabset_model
