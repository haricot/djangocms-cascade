# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from cms.extensions.toolbar import ExtensionToolbar
from cms.toolbar_pool import toolbar_pool
from cms.toolbar.items import Break
from cms.cms_toolbars import PAGE_MENU_SECOND_BREAK, ADMIN_MENU_IDENTIFIER, CLIPBOARD_BREAK 
from cmsplugin_cascade.models import CascadePage

@toolbar_pool.register
class CascadePageToolbar(ExtensionToolbar):
    model = CascadePage

    def populate(self):
        current_page_menu = self._setup_extension_toolbar()
        if current_page_menu:
            # retrieves the instance of the current extension (if any) and the toolbar item URL
            page_extension, url = self.get_page_extension_admin()
            if url:
                position = current_page_menu.find_first(Break, identifier=PAGE_MENU_SECOND_BREAK)
                disabled = not self.toolbar.edit_mode_active
                current_page_menu.add_modal_item(_("Extra Page Fields"), position=position, url=url, disabled=disabled)
                
                
        admin_menu = self.toolbar.get_or_create_menu(ADMIN_MENU_IDENTIFIER, _('Site'))
        position = admin_menu.find_first(Break, identifier=CLIPBOARD_BREAK )
        admin_menu.add_link_item(_('Clips Libraries'), url='#', extra_classes=('cms-show-clips-lib',), position=position )
