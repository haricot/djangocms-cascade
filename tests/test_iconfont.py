# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
from bs4 import BeautifulSoup
import json
from django import VERSION as DJANGO_VERSION
from django.contrib.auth import get_user_model
from django.test.client import Client
from django.urls import reverse, resolve
from django.core.files.uploadedfile import SimpleUploadedFile

from filer.admin.clipboardadmin import ajax_upload

from cms.api import add_plugin
from cms.utils.plugins import build_plugin_tree

from cmsplugin_cascade import app_settings
from cmsplugin_cascade.models import IconFont
from cmsplugin_cascade.bootstrap4.container import BootstrapContainerPlugin
from cmsplugin_cascade.icon.cms_plugins import FramedIconPlugin
from .test_base import CascadeTestCase


BS4_BREAKPOINT_KEYS=['xs', 'sm', 'md', 'lg','xl']

class IconFontTestCase(CascadeTestCase):
    client = Client()

    def setUp(self):
        super(IconFontTestCase, self).setUp()
        UserModel = get_user_model()
        self.admin_user = UserModel.objects.get(username='admin')

    def test_add_font(self):
        with self.login_user_context(self.admin_user):
            # upload the zipfile into the filer's clipboard
            filename = os.path.join(os.path.dirname(__file__), 'assets/fontello-b504201f.zip')
            with open(filename, 'rb') as zipfile:
                uploaded_file = SimpleUploadedFile('fontello-b504201f.zip', zipfile.read(), content_type='application/zip')
            request = self.get_request(reverse('admin:filer-ajax_upload'))
            self.assertTrue(request.user.is_staff, "User is not a staff user")
            request.FILES.update(file=uploaded_file)
            response = ajax_upload(request)
            self.assertEqual(response.status_code, 200)
            content = json.loads(response.content.decode('utf-8'))
            self.assertDictContainsSubset({'label': 'fontello-b504201f.zip'}, content)

            # save the form and submit the remaining fields
            add_iconfont_url = reverse('admin:cmsplugin_cascade_iconfont_add')
            data = {
                'identifier': "Fontellico",
                'zip_file': content['file_id'],
                '_continue': "Save and continue editing",
            }
            response = self.client.post(add_iconfont_url, data)
            self.assertEqual(response.status_code, 302)
            resolver_match = resolve(response.url)
            self.assertEqual(resolver_match.url_name, 'cmsplugin_cascade_iconfont_change')

            # check the content of the uploaded file
            if DJANGO_VERSION >= (2, 0):
                icon_font = IconFont.objects.get(pk=resolver_match.kwargs['object_id'])
            else:
                icon_font = IconFont.objects.get(pk=resolver_match.args[0])                
            self.assertEqual(icon_font.identifier, "Fontellico")
            self.assertEqual(icon_font.config_data['name'], 'fontelico')
            self.assertEqual(len(icon_font.config_data['glyphs']), 34)

            # check if the uploaded fonts are rendered inside Preview Icons
            response = self.client.get(response.url)
            self.assertEqual(response.status_code, 200)
            soup = BeautifulSoup(response.content, 'lxml')
            preview_iconfont = soup.find('div', class_="preview-iconfont")
            icon_items = preview_iconfont.ul.find_all('li')
            self.assertEqual(len(icon_items), 34)
            self.assertListEqual(icon_items[0].i.attrs['class'], ['icon-emo-happy'])
            self.assertListEqual(icon_items[33].i.attrs['class'], ['icon-marquee'])

            # select icon font from toolbar
            self.placeholder.page.cascadepage.icon_font = icon_font
            self.placeholder.page.cascadepage.save()

            # create container
            container_model = add_plugin(self.placeholder, BootstrapContainerPlugin, 'en',
                                         glossary={'breakpoints': BS4_BREAKPOINT_KEYS})
            container_plugin = container_model.get_plugin_class_instance()
            self.assertIsInstance(container_plugin, BootstrapContainerPlugin)

            # add icon as child to this container
            glossary = {"font_size": "10em", "color": ["#88258e", ""],  "background_color":[ "#c8ffcd",
                       "f"  ], "icon_font":{  "model":"cmsplugin_cascade.iconfont",   "pk":1 },
                      "symbol":"emo-wink","font_size":"1em", "text_align":"", "border":[ "0px", "solid", "#000000"],
                      "border_radius":"50%"}
            icon_model = add_plugin(self.placeholder, FramedIconPlugin, 'en', target=container_model,
                                    glossary=glossary)
            icon_plugin = icon_model.get_plugin_class_instance()
            self.assertIsInstance(icon_plugin, FramedIconPlugin)

            # render the plugins
            plugin_list = [container_model, icon_model]
            build_plugin_tree(plugin_list)
            html = self.get_html(container_model, self.get_request_context()) 
            soup = BeautifulSoup(html, 'lxml')

            # look for the icon symbol
            style = soup.find('span', class_='icon-emo-wink').attrs['style'].split(';')
            self.assertIn('color:#88258e', style)
            self.assertIn('display:inline-block', style)

            # look for the CSS file
            response = self.client.get(container_model.placeholder.page.get_absolute_url() + '?edit')
            self.assertEqual(response.status_code, 200)
            soup = BeautifulSoup(response.content, 'lxml')
            links = soup.head.find_all('link')
            for link in links:
                if link.attrs['href'].endswith('fontelico.css'):
                    break
            else:
                self.fail("No CSS file with font definition found")
