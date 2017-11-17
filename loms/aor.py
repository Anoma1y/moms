#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.utils.translation import ugettext as _
from random import random
import copy, time, operator
from collections import Counter

streams = {}

def stream_add_user(stream, allow = []):
    stream.user_count += 1
    stream.users.append(allow)
    stream.node.overload -= stream.brandwidth
    stream.node.user_count += 1
def stream_del_user(stream, id=0):
    del stream.users[id]
    stream.user_count -= 1
    stream.node.overload += stream.brandwidth
    stream.node.user_count -= 1

def add_stream(stream):
    streams[stream.id] = stream

def add_stream_to_point(stream, point):
    point.streams[stream.id] = stream

def get_point_brandwidth(point):
    brandwidth = []
    for id in point.streams:
        for count in range(0, point.streams[id].user_count):
            brandwidth.append(point.streams[id].brandwidth)
    return sorted(brandwidth, reverse=True)

def point_decrease_possible(test_point):
    point = copy.deepcopy(test_point)
    streams = sorted(point.streams.items(), key=operator.itemgetter(1), reverse=True)
    for i, (from_stream_id, from_stream) in enumerate(streams[:-1]):
        for to_stream_id, to_stream in streams[i:]:
            if to_stream.brandwidth == from_stream.brandwidth: continue
            while len(from_stream.users) > 0:
                user = from_stream.users[0]
                stream_del_user(from_stream, 0)
                stream_add_user(to_stram, user)
                point.overload += from_stream.brandwidth - to_stream.brandwidth
                if point.overload >= 0: return True
    return False


def show(points):
    html = ""
    for point_id in points:
        point = points[point_id]
        html += "Node> %d:%s, <b>overload:%d</b>, user count:%d, maximum:%d<br />" % (point.id, point, point.overload, point.user_count, point.max_users)
        for stream_id in point.streams:
            stream = point.streams[stream_id]
            stream_html = "&nbsp;&nbsp;&nbsp;&nbsp;Route> %d:%s, brandwidth:%d, user count:%d<br />" % (stream.id, stream, stream.brandwidth, stream.user_count)
            html += stream_html
    return html

def check_relation(stream1_id, stream2_id, decrease=False):
    if stream1_id == stream2_id: return True

    stream1 = streams[stream1_id]
    while True:
        if not decrease:
            if stream1.start_node == stream1.end_node: break
        if stream1.parent == None: break
        else:
            stream1 = streams[stream1.parent.pk]

    stream2 = streams[stream2_id]
    while True:
        if not decrease:
            if stream2.start_node == stream2.end_node: break
        if stream2.parent == None: break
        else:
            stream2 = streams[stream2.parent.pk]

    if stream1.id == stream2.id: return True
    return False


def flatten(iterable):
    for elm in iterable:
        if isinstance(elm, (list, tuple)):
            for relm in flatten(elm):
                yield relm
        else:
            yield elm

def find_point_with_brandwidth(points, brandwidth, start_id, negative=False, except_ids=[]):
    start = points[start_id]
    destination = False
    overload = brandwidth
    if negative: overload = -brandwidth

    stream = False
    destination_stream = False
    user_count = 0
    allow_count = len(points)
    user_id = False
    founded_overload = 0

    for stream_id in start.streams:
        if start.streams[stream_id].brandwidth != brandwidth: continue
        for id in points:
            if id in except_ids: continue
            if points[id].user_count >= points[id].max_users: continue
            found = False
            for destination_stream_id in points[id].streams:
                if not check_relation(stream_id, destination_stream_id):
                    #print "%s and %s no relations" % (stream_id, destination_stream_id)
                    continue
                if points[id].streams[destination_stream_id].brandwidth == brandwidth:
                    possible_overload = min([points[id].overload, (points[id].max_users - points[id].user_count) * brandwidth])
                    #print id, "possible", possible_overload, overload
                    if possible_overload < overload: continue
                    for idx, users in enumerate(start.streams[stream_id].users):
                        if not users == [] and not id in users:
                            continue
                        if len(users) > allow_count:
                            continue
                        elif len(users) == allow_count:
                            if start.streams[stream_id].user_count < user_count:
                                continue
                            elif start.streams[stream_id].user_count == user_count:
                                if possible_overload < founded_overload: continue
                        stream = start.streams[stream_id]
                        destination_stream = points[id].streams[destination_stream_id]
                        user_count = stream.user_count
                        allow_count = len(users)
                        user_id = idx
                        founded_overload = possible_overload

                        overload = possible_overload
                        destination = points[id]

    if destination:
        #destination.overload -= brandwidth
        #start.overload += brandwidth
        stream_add_user(destination_stream, stream.users[user_id])
        stream_del_user(stream, user_id)
        return [destination.id, stream.id, destination_stream.id]

    else: return False


def find_result(overload, brandwidth, larger):
    result = []
    if sum(brandwidth) < overload: return

    values = sorted(set(brandwidth), reverse=True)
    counter = Counter(brandwidth)
    count = len(values)
    boxes = [0] * count
    sizes = [0] * count
    operations = ['plus'] * count
    cursor = 0

    #print values, counter, count

    while True:
        if operations[cursor] == 'plus':
            if counter[values[cursor]] != sizes[cursor]:
                boxes[cursor] += values[cursor]
                sizes[cursor] += 1
                if sum(boxes) >= overload:
                    result = []
                    for i, size in enumerate(sizes):
                        result += [values[i]] *  size
                    if larger: yield result
                    elif sum(boxes) == overload: yield result
                    if count == 1: return
                    operations[cursor] = 'minus'
            else:
                return
        elif operations[cursor] == 'minus':
            if cursor == 0 and sizes[cursor] == 0:
                break
            if cursor == count - 1:
                boxes[cursor] = 0
                sizes[cursor] = 0
                operations[cursor] = 'plus'
                cursor -= 1
            elif sizes[cursor] == 0:
                operations[cursor] = 'plus'
                cursor -= 1
            else:
                boxes[cursor] -= values[cursor]
                sizes[cursor] -= 1
                cursor += 1


def clean(clean_points, clean_ids, negative=True, larger=True, clean_log=[]):
    start_time = time.time()

    variants = []
    new_variants = []

    new_variant = {}
    new_variant['ids'] = clean_ids
    new_variant['points'] = copy.deepcopy(clean_points)
    new_variant['log'] = clean_log

    variants.append(new_variant)

    level = 0
    while 1:
        if level == 10: break
        print 'level:', level, new_variant['log']
        count = 0
        for variant in variants:

            points = variant['points']
            point = points[variant['ids'][0]]
            overload = -point.overload
            brandwidth = get_point_brandwidth(point)

            possible_overload = 0
            for p in points:
                if p == point.id: continue
                if points[p].overload > 0:
                    possible_overload += points[p].overload

            if overload > possible_overload: continue

            for result in find_result(overload, brandwidth, larger):
                print result

                new_points = copy.deepcopy(points)
                error = False
                destinations = []
                log = []

                while len(result) > 0:
                    destination = find_point_with_brandwidth(points=new_points, brandwidth=result[0], start_id=point.id, negative=negative)
                    if destination:
                        #log.append('from:%d to:%d value:%d' % (point.id, destination.id, result[0]))
                        log.append({'from':point.id, 'to':destination[0], 'from_stream':destination[1], 'to_stream':destination[2], 'value': result[0]})
                        if new_points[destination[0]].overload < 0:
                            if not destination[0] in destinations:
                                destinations.append(destination[0])

                    else:
                        error = True
                        break
                    del result[0]

                if error == False:
                    if len(destinations) == 0:
                        if len(variant['ids']) == 1:
                            answer = [new_points, variant['log'] + log]
                            #show(new_points)
                            print variant['log'] + log
                            count += 1
                            print count
                            # если ответ найден то выход
                            break
                        if len(variant['ids']) > 1:
                            full_log = list(variant['log'])
                            full_log.append(log)
                            answer = clean(new_points, variant['ids'][1:], False, clean_log=full_log)
                            if answer:
                                count += 1
                    if len(destinations) >= 1:
                        if not log in variant['log']:
                            full_log = list(variant['log'])
                            full_log.append(log)

                            new_variant = {}
                            new_variant['ids'] = destinations
                            new_variant['points'] = copy.deepcopy(new_points)
                            new_variant['log'] = full_log
                            new_variants.append(new_variant)

        if count > 0:
            print "possible"
            elapsed = (time.time() - start_time)
            print "elapsed", elapsed
            return answer
        if(len(new_variants)) > 0:
            #for var in new_variants:
            #	print var['log']
            print 'new variants len:', len(new_variants)
            level += 1
            variants = []
            variants = copy.deepcopy(new_variants)
            new_variants = []
            continue
        else:
            print "impossible"
            elapsed = (time.time() - start_time)
            print "elapsed", elapsed
            return False

def decrease_point(point_id, points, negative=False):
    start = points[point_id]
    destination = False

    destination_stream = False
    destination = False
    user_count = 0
    allow_count = len(points)
    user_id = False

    streams = sorted(start.streams.items(), key=operator.itemgetter(1), reverse=True)
    for i, (from_stream_id, from_stream) in enumerate(streams):
        brandwidth = from_stream.brandwidth
        found_brandwidth = 0

        found = False
        negative_overload = -100000000
        try_overload = 0
        for id in points:
            if points[id].user_count >= points[id].max_users: continue
            if points[id].user_count == points[id].max_users and not id == point_id: continue
            for destination_stream_id in points[id].streams:
                if not check_relation(from_stream_id, destination_stream_id, decrease=True):
                    continue
                stream_brandwidth = points[id].streams[destination_stream_id].brandwidth
                if not id == point_id and points[id].overload - stream_brandwidth < 0:
                    if negative:
                        try_overload = points[id].overload - stream_brandwidth
                    else:
                        continue
                if stream_brandwidth >= brandwidth: continue
                if stream_brandwidth < found_brandwidth: continue
                if stream_brandwidth == found_brandwidth and not id == point_id:
                    if negative:
                        if try_overload < negative_overload: continue
                    else:
                        continue

                for idx, users in enumerate(start.streams[from_stream_id].users):
                    if not users == [] and not id in users:
                        continue
                    if len(users) > allow_count:
                        continue
                    elif len(users) == allow_count:
                        if start.streams[from_stream_id].user_count < user_count:
                            continue

                    found = True
                    from_brandwidth = brandwidth
                    found_brandwidth = stream_brandwidth
                    found_stream = from_stream
                    destination_stream = points[id].streams[destination_stream_id]
                    destination = points[id]
                    user_count = found_stream.user_count
                    allow_count = len(users)
                    user_id = idx
                    if negative: negative_overload = try_overload

        if found:
            #destination.overload -= found_brandwidth
            #start.overload += from_brandwidth
            stream_add_user(destination_stream, found_stream.users[user_id])
            stream_del_user(found_stream, user_id)
            answer = {'from':found_stream.id, 'to':destination_stream.id, 'value':from_brandwidth, 'decreased':found_brandwidth}
            return [destination.id, answer]
    return False

def clear(clear_points, clear_id, negative=True, larger=True):
    point = clear_points[clear_id]
    overload = 0
    while point.overload < 0:
        answer = clean(clear_points, [clear_id], negative, larger)
        if answer:
            print "clear possible:", point.overload
            answer[clear_id].overload -= overload
            break
        point.overload += 1
        overload += 1

def clear_with_decrease(points, clear_id, negative=True, larger=True):
    start_time = time.time()

    clear_points = copy.deepcopy(points)
    point = clear_points[clear_id]
    overload = 0
    negative_points = []
    log = []

    while point.overload < 0:
        result = decrease_point(clear_id, clear_points)
        if not result:
            negative_result = decrease_point(clear_id, clear_points, negative=True)
            if negative_result:
                log.append(negative_result[1])
                if not negative_result[0] in negative_points: negative_points.append(negative_result[0])
                print "negative decrease possible"
                continue
            else:
                print "decrease not possible"
                return False
        log.append(result[1])

        if point.overload >= 0:
            print "decreased"
            elapsed = (time.time() - start_time)
            print "elapsed", elapsed
            return [clear_points, [], log]

        answer = clean(clear_points, [clear_id], negative, larger)
        if answer:
            print "clear with decrease possible"
            elapsed = (time.time() - start_time)
            print "elapsed", elapsed
            answer.append(log)
            return answer

    if len(negative_points) > 0:
        answer = clean(clear_points, negative_points)
        if answer:
            print "decrease with clean possible"
            answer.append(log)
            return answer
        else:
            print "negative decrease not possible"
            return False
            possible = True
            for point_id in negative_points:
                if not point_decrease_possible(clear_points[point_id]):
                    possible = False
                    break
            if possible:
                print "decrease with self-decrease possible"
            else:
                print "decrease not possible"

    print "decrease not possible"
    return False


