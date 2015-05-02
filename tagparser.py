__author__ = 'grmhay'

# Parses the OSM XML file for tags, counts frequency of the node tag type and of tags themselves


import xml.etree.ElementTree as ET
from pprint import pprint
import operator

OSMFILE = 'phoenix_arizona.osm'
# OSMFILE = 'phoenix_arizona_sample.osm'

def add_tag(tag, tag_count):
    """ adds a tag to tag_count, or initializes at 1 if does not yet exist """
    if tag in tag_count:
        tag_count[tag] += 1
    else:
        tag_count[tag] = 1

def count_tags(filename):
    # Parses the OSM file and counts the tags by type for node type only

    # initialize the dictionary objects and a counter that can be used to log activity
    tag_count = {}
    tag_keys = {}
    counter = 0

    # iterate XML elements from OSM file
    for _, element in ET.iterparse(filename, events=("start",)):

        # add the found tag to the count
        add_tag(element.tag, tag_count)

        # if the tag has a key, add it to tag_keys dictionary
        if element.tag == 'tag' and 'k' in element.attrib:
            add_tag(element.get('k'), tag_keys)


        counter += 1
        # For debugging ....
        # print counter

    # create sorted list of tag key-frequency tuples
    tag_keys = sorted(tag_keys.items(), key=operator.itemgetter(1))[::-1]


    return tag_count, tag_keys



# Main Program

tags, tag_keys = count_tags(OSMFILE)
print 'Displaying Tags and Frequency of Occurrence.....\n'
pprint(tags)
print 'Displaying Tag Keys and Frequency of Occurrence....\n'
pprint(tag_keys)


