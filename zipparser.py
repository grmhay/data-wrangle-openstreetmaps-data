__author__ = 'grmhay'

# Parses the OSM XML file for zipcode-esque tag types only and counts frequency of the zipcode found

import xml.etree.ElementTree as ET
from pprint import pprint
import operator

OSMFILE = 'phoenix_arizona.osm'
#OSMFILE = 'phoenix_arizona_sample.osm'

def add_zip(zip, zip_count):
    """ adds a tag to tag_count, or initializes at 1 if does not yet exist """
    if zip in zip_count:
        zip_count[zip] += 1
    else:
        zip_count[zip] = 1

def count_zips(filename):
    # Parses the OSM file and counts the tags by type for node type only

    # initialize the dictionary objects and a counter that can be used to log activity
    zip_count = {}
    zip_keys = {}
    counter = 0

    # iterate XML elements from OSM file
    for _, element in ET.iterparse(filename, events=("start",)):

        # if tag and has key
        if element.tag == 'tag' and 'k' in element.attrib:
            # Iterate through the children of the tag ... look for zipcode-like key names
            for tag in element.iter("tag"):
                if element.get('k') == 'addr:postcode' or element.get('k') == 'tiger:zip_left' or element.get('k') == 'tiger:zip_left_1':
                    # if you find a zipcode-like key name, increment the counter of that key value in zip_keys dictionary
                    add_zip(element.get('v'), zip_keys)
                    counter += 1
                    # For debugging ....
                    print counter

    # create sorted list of zipcode-frequency tuples
    zip_keys = sorted(zip_keys.items(), key=operator.itemgetter(1))[::-1]


    return zip_keys



# Main Program

zip_keys = count_zips(OSMFILE)
print 'Displaying Zips and Frequency of Occurrence....\n'
pprint(zip_keys)


