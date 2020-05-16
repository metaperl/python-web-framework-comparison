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
        fields.separator  = Field(label='Separated by', required=True)
        fields.joiner     = Field(label='Join with', required=True)

    @property
    def has_data(self):
        return self.input_text and self.separator and self.joiner

    @exposed('save')
    def events(self, events):
        events.save = Event(label='Perform Tr')

    @property
    def translated_string(self):
        import re
        return re.sub(self.separator, self.joiner, self.input_text)


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
        super(__class__, self).__init__(view, 'address_form')

        inputs = self.add_child(FieldSet(view, legend_text='Enter data then click button'))
        inputs.use_layout(FormLayout())

        inputs.layout.add_input(TextInput(self, tr.fields.input_text))
        inputs.layout.add_input(TextInput(self, tr.fields.separator), help_text='(Regular expression)')
        inputs.layout.add_input(TextInput(self, tr.fields.joiner), help_text='(Character string)')

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


class MyUI(UserInterface):
    def assemble(self):

        home = self.define_view('/', title='x marksthe spot', page=MyPage.factory())
        self.define_transition(TR.events.save, home, home)
