from __future__ import print_function, unicode_literals, absolute_import, division

from reahl.sqlalchemysupport import Session, Base, session_scoped
from reahl.webdeclarative.webdeclarative import UserSession


from reahl.web.fw import UserInterface, Widget
from reahl.web.bootstrap.ui import HTML5Page, TextNode, Div, H, P, FieldSet
from reahl.web.bootstrap.navbar import Navbar, ResponsiveLayout
from reahl.web.bootstrap.grid import Container
from reahl.web.bootstrap.forms import TextInput, Form, FormLayout, Button, ButtonLayout
from reahl.component.modelinterface import exposed, Field, EmailField, Action, Event
from reahl.sqlalchemysupport import Session, Base, session_scoped
from sqlalchemy import Column, Integer, UnicodeText
from sqlalchemy.orm import relationship


@session_scoped
class TR(Base):
    __tablename__ = 'simple_tr_tr'

    id            = Column(Integer, primary_key=True)
    input_text    = Column(UnicodeText)
    separator     = Column(UnicodeText)
    joiner        = Column(UnicodeText)

    @exposed
    def fields(self, fields):
        fields.input_text = Field(label='Input Text', required=True)
        fields.separator  = Field(label='Separated by (Regular Expression)', required=True)
        fields.joiner     = Field(label='Join with (Character String)', required=True)

    @property
    def has_data(self):
        return self.input_text and self.separator and self.joiner

    @exposed('save', 'clear_inputs')
    def events(self, events):
        events.save = Event(label='Perform Tr')
        events.clear_inputs = Event(label='Clear Inputs', action=Action(self.clear_inputs))

    @property
    def translated_string(self):
        import re
        return re.sub(self.separator, self.joiner, self.input_text)

    def clear_inputs(self):
        self.input_text = ''
        self.separator = ''
        self.joiner = ''


class MyPage(HTML5Page):
    def __init__(self, view):
        super(__class__, self).__init__(view)

        self.body.use_layout(Container())

        layout = ResponsiveLayout('md', colour_theme='dark', bg_scheme='primary')
        navbar = Navbar(view, css_id='my_nav').use_layout(layout)
        navbar.layout.set_brand_text('Simple TR')
        navbar.layout.add(TextNode(view, 'Translate from this to that.'))

        self.body.add_child(navbar)
        self.body.add_child(MyPanel(view))


class InputForm(Form):
    def __init__(self, view, tr):
        super(__class__, self).__init__(view, 'tr_input_form')

        inputs = self.add_child(FieldSet(view, legend_text='Enter data then click button'))
        inputs.use_layout(FormLayout())

        inputs.layout.add_input(TextInput(self, tr.fields.input_text))
        inputs.layout.add_input(TextInput(self, tr.fields.separator))
        inputs.layout.add_input(TextInput(self, tr.fields.joiner))

        button = inputs.add_child(Button(self, tr.events.save))
        button.use_layout(ButtonLayout(style='primary'))


class MyPanel(Div):
    def __init__(self, view):
        super(__class__, self).__init__(view)

        tr = TR.for_current_session()
        my_form = InputForm(view, tr)
        self.add_child(my_form)

        if tr.has_data:
            self.add_child(P(view, text=tr.translated_string))


class ClearInputsPage(HTML5Page):
    def __init__(self, view):
        super(ClearInputsPage, self).__init__(view)
        self.body.add_child(ClearInputsForm(view))


class ClearInputsForm(Form):
    def __init__(self, view):
        super(ClearInputsForm, self).__init__(view, 'clear_inputs_form')

        inputs = self.add_child(FieldSet(view, legend_text='Clear all inputs'))
        inputs.use_layout(FormLayout())

        tr = TR.for_current_session()
        button = inputs.add_child(Button(self, tr.events.clear_inputs))
        button.use_layout(ButtonLayout(style='primary'))


class MyUI(UserInterface):
    def assemble(self):

        clear_inputs_view = self.define_view('/clear', title='Clear Inputs', page=ClearInputsPage.factory())
        home = self.define_view('/', title='x marksthe spot', page=MyPage.factory())
        self.define_transition(TR.events.save, home, home)
        self.define_transition(TR.events.clear_inputs, clear_inputs_view, home)

