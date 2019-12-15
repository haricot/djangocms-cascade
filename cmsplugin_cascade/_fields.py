from entangled.fields import EntangledBoundField, EntangledFormField
from entangled.widgets import EntangledFormWidget
from django.utils.html import mark_safe
from django.template import loader


class CascadeEntangledBoundField(EntangledBoundField):
    """
    Label not needed in this container boundfields and it are replaced by container title,
    container title describe nested boudfields and this can add compatiblity add  adding input helper collapse in container title.
    """
    label = '' #prevent tag and title label
    auto_id = False # prevent tag label
    template_name = 'cascade/admin/widgets/boundfield_as_widget.html'

    def __init__(self, *args,**kwargs):
        cls_cascade_entangled_form_field=args[1]
        self.title = cls_cascade_entangled_form_field.title
        self.icon =  cls_cascade_entangled_form_field.icon
        self.widget = EntangledFormWidget(self)
        super().__init__(*args,**kwargs)
        
    def as_widget(self, widget=None, attrs=None, only_initial=True):    
        output_widgets=EntangledBoundField.as_widget(self)
        context ={
        "help_text": mark_safe(self.widget._entangled_form.help_text),
        'output_widgets':output_widgets,
        #'label':self.widget._entangled_form.name, self.icon
        'title':self.title,
        'icon' :self.icon
        }
        template = loader.get_template(self.template_name).render(context)
        return mark_safe(template)


class CascadeEntangledFormField(EntangledFormField,  ):
    _html_output_kwargs= dict(   normal_row='<li%(html_class_attr)s>%(errors)s%(label)s %(field)s%(help_text)s</li>',
            error_row='<li>%s</li>',
            row_ender='</li>',
            help_text_html=' <span class="helptext">%s</span>',
            errors_on_separate_row=False)
    def __init__(self, *args,**kwargs):
        self.title = args[0].title if hasattr(args[0], 'title') else ''
        self.icon = args[0].title if hasattr(args[0], 'icon') else ''
        super().__init__(*args,**kwargs)

    def get_bound_field(self, form, field_name):
        return CascadeEntangledBoundField(form, self, field_name)
