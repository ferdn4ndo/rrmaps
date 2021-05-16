#!/usr/bin/python
# -*- coding: utf-8 -*-

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label

class TestApp(App):
    def build(self):
        # return Button(text='Hello World')
        return Label(text='Hello world')

TestApp().run()