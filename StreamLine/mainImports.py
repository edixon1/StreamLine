# -*- coding: utf-8 -*-
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.lang import Builder
from kivy.uix.textinput import TextInput
from kivy.uix.listview import ListItemButton
import sqlite3
import os
from plyer import gps
from kivy.clock import Clock, mainthread
from kivy.uix.popup import Popup
from kivy.uix.label import Label
import gspread
import sqlite3
import os
from oauth2client.service_account import ServiceAccountCredentials