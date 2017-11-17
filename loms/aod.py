from django.utils.translation import ugettext as _
from random import random

def get_names():
	names = []
	for f in FUNCTIONS:
		pass
		names.append([f[0], f[1]])
	return names

def get_function(id):
	for f in FUNCTIONS:
		if f[0] == id:
			return f[2]

def f1(left, right):
	return left + ((right - left) * random())

def f2(left, right):
	return left + ((right - left) * random())

FUNCTIONS = [
	[1, _('Algorithm 1'), f1],
	[2, _('Algorithm 2'), f2],
]
