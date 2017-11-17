from django.utils.translation import ugettext as _
from random import random
from loms import aor

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

def find_stream_without_overload(points, destination_stream, mode=1):
	first = True
	for point_id in points:
		if mode == 1:
			if points[point_id].user_count >= points[point_id].max_users: continue
		elif mode == 2:
			if points[point_id].user_count == 0: continue

		for stream_id in points[point_id].streams:
			if not aor.check_relation(stream_id, destination_stream.id): continue
			overload = aor.streams[stream_id].node.overload
			if first:
				first = False
				point_overload = overload
				stream = aor.streams[stream_id]
			else:
				if overload > point_overload:
					point_overload = overload 
					stream = aor.streams[stream_id]
	if first == False:
		return stream
	else: return False

def find_stream_with_overload(points, destination_stream, mode=1):
	first = True
	for point_id in points:
		if mode == 1:
			if points[point_id].user_count >= points[point_id].max_users: continue
		elif mode == 2:
			if points[point_id].user_count == 0: continue

		for stream_id in points[point_id].streams:
			if not aor.check_relation(stream_id, destination_stream.id): continue
			overload = aor.streams[stream_id].node.overload
			if first:
				first = False
				point_overload = overload
				stream = aor.streams[stream_id]
			else:
				if overload < point_overload:
					point_overload = overload 
					stream = aor.streams[stream_id]
	if first == False:
		return stream
	else: return False

FUNCTIONS = [
	[1, _('Algorithm of Connection 1'), find_stream_without_overload],
	[2, _('Algorithm of Connection 2'), find_stream_with_overload],
]
