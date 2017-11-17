# -*- coding: utf-8 -*-
from django.forms import ModelForm
from django import forms
from soms.models import NetworkMap, Node


class FormNetworkMap(ModelForm):
    class Meta:
        model = NetworkMap
        exclude = ["images", "imgX", "imgY", "imgWidth", "imgHeight"]

class FormNetworkMapUpdate(ModelForm):
    class Meta(object):
        model = NetworkMap

class FormNetworkMapUpdateQ(ModelForm):
    class Meta(object):
        model = NetworkMap
        exclude = ["name",  "imgX", "imgY", "imgWidth", "imgHeight"]

class NewNodeForm(ModelForm):
    class Meta(object):
        model = Node
