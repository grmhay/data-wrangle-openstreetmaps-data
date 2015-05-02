__author__ = 'grmhay'

def insert_osm(cleanmapdata, db):
    # cleanmapdata is a list of dictionary key-values in JSON format
    for a in cleanmapdata:
        db.osm.insert(a)

def process_file (input_file ):
    osm_file = open(input_file)
    return osm_file

def audit_street_type (street_type, street_name):
    # Looks for street names using regular expression
    # If the found street name is not in the expected list then it is added to
    # street types as something to be cleaned or ignored and count is incremented

    expected = ["Street","Avenue","Boulevard","Drive","Court","Place","Lane","Way","Trail","Road","Parkway","Highway","Freeway","Circle"]
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)






def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")

def audit (input_file):

    # Audit street names

    # Initialize counters to count streetnames and unexpected ones to measure quality of
    # expected match for cleanup - I could be cleaner and pass these back and forth as parameters
    streetname_count = 0
    streetname_notinexpected_count = 0

    print 'auditing the file'
    for event, elem in ET.iterparse(input_file, events=("start",)):
        if elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    streetname_count += 1
                    print streetname_count
                    audit_street_type(street_types, tag.attrib['v'])
    print 'done auditing'
    # Print the number of unique street names examined and the number of street types unexpected
    print 'Audit found ' + str(streetname_count) + ' unique street names'
    print 'Audit found number of unexpected street types to clean ' + str(len(dict(street_types)))
    # Print the list of unexpected street types and the street names that have this type
    pprint.pprint(dict(street_types))

    # Audit postal codes for any outside 850** (Phoenix zip codes)

    # Audit lat and long outside Phoenix boundaries (on nodes)

    # Audit tag usage consistency



def update_name(name, mapping):

    # Pull the last word of the street name (RE previous)
    # Look it up in the mapping to get the value it maps to
    # Substitute the last word of the name for the value

    m = street_type_re.search(name)
    if m:
        street_type = m.group()
        #print 'Found this street type '+ street_type
        if street_type in mapping:
            sub_street_type = mapping[street_type]
            #print 'And substituted it with ' + sub_street_type

            left, _, right = name.strip().partition(' ')
            mid, _, right = right.rpartition(' ')
            name = name.replace(right, sub_street_type, 1)
            print 'Correct street name ' + name

    return name

def shape_element_node(element):
    node ={}
    for tag in element.iter("node"):

        print 'Shaping new node element ' + tag.attrib['id'] + '\n'

        node = { 'id': tag.attrib['id'],
                 'type': 'node',
                 'created' : { 'version' : tag.attrib['version'],
                               'changeset' : tag.attrib['changeset'],
                               'timestamp' : tag.attrib['timestamp'],
                               'user' : tag.attrib['user'],
                               'uid' : tag.attrib['uid']
                               },
                 # Convert the latitude and longitude strings to floats
                 'pos' : [float(tag.attrib['lat']), float(tag.attrib['lon'])],
                 }

        if 'visible' in tag.attrib:
            node.update({'visible' : tag.attrib['visible']} )

        address = {}
        for subtag in element.iter("tag"):
        # Ignore tags with problematic characters as k values
            m = problemchars.search(subtag.attrib['k'])
            if m:
                pass

        # Map the address attributes into a dictionary address and add to node
            if subtag.attrib['k'] == "addr:housenumber" :
                address ['housenumber'] = subtag.attrib['v']
            elif subtag.attrib['k'] == "addr:postcode":
                address ['postcode'] = subtag.attrib['v']
            elif subtag.attrib['k'] == "tiger:zip_left":
                address ['postcode'] = subtag.attrib['v']
            elif subtag.attrib['k'] == "tiger:zip_left_1":
                address ['postcode'] = subtag.attrib['v']
            elif subtag.attrib['k'] == "addr:city":
                address ['city'] = subtag.attrib['v']
            elif subtag.attrib['k'] == "addr:street":
                address ['street'] = update_name(subtag.attrib['v'],mapping)
            elif subtag.attrib['k'] == "amenity":
                node.update({'amenity' : subtag.attrib['v']} )
            elif subtag.attrib['k'] == "name":
                node.update({'name' : subtag.attrib['v']} )
            elif subtag.attrib['k'] == "phone":
                node.update({'phone' : subtag.attrib['v']})
            elif subtag.attrib['k'] == "highway":
                node.update({'highway' : subtag.attrib['v']} )
            elif subtag.attrib['k'] == "power":
                node.update({'power' : subtag.attrib['v']} )
            elif subtag.attrib['k'] == "crossing":
                node.update({'crossing' : subtag.attrib['v']} )
            elif subtag.attrib['k'] == "natural":
                node.update({'natural' : subtag.attrib['v']} )
            elif subtag.attrib['k'] == "bicycle":
                node.update({'bicycle' : subtag.attrib['v']} )
            elif subtag.attrib['k'] == "horse":
                node.update({'horse' : subtag.attrib['v']} )
            elif subtag.attrib['k'] == "supervised":
                node.update({'supervised' : subtag.attrib['v']} )
            elif subtag.attrib['k'] == "traffic_calming":
                node.update({'traffic_calming' : subtag.attrib['v']} )


            node.update({'address' : address})

    return node

def shape_element_way(element):
    node ={}
    for tag in element.iter("way"):

        print 'Shaping new way element ' + tag.attrib['id'] + '\n'

        node = { 'id': tag.attrib['id'],
                 'type': 'way',
                 'created' : { 'version' : tag.attrib['version'],
                               'changeset' : tag.attrib['changeset'],
                               'timestamp' : tag.attrib['timestamp'],
                               'user' : tag.attrib['user'],
                               'uid' : tag.attrib['uid']
                               }
                 }
        if 'visible' in tag.attrib:
            node.update({'visible' : tag.attrib['visible']} )

        address = {}
        for subtag in element.iter("tag"):
        # Ignore tags with problematic characters as k values
            m = problemchars.search(subtag.attrib['k'])
            if m:
                pass

        # Map the address attributes into a dictionary address and add to node
            if subtag.attrib['k'] == "addr:housenumber" :
                address ['housenumber'] = subtag.attrib['v']
            elif subtag.attrib['k'] == "addr:postcode":
                address ['postcode'] = subtag.attrib['v']
            elif subtag.attrib['k'] == "tiger:zip_left":
                address ['postcode'] = subtag.attrib['v']
            elif subtag.attrib['k'] == "tiger:zip_left_1":
                address ['postcode'] = subtag.attrib['v']
            elif subtag.attrib['k'] == "addr:city":
                address ['city'] = subtag.attrib['v']
            elif subtag.attrib['k'] == "addr:street":
                address ['street'] = update_name(subtag.attrib['v'],mapping)


            node.update({'address' : address})

            node_refs = []
            for subtag in element.iter("nd"):
                node_refs.append(subtag.attrib['ref'])
                node.update({'node_refs' : node_refs})

    return node


def clean_and_reformat (input_file):
    # Clean street names
    # Creates a JSON file with starting format
    # Change this so it takes the whole file in element by element
    # Should call a routine to clean the data based on what type the element is - way or node
    # just like in shape element except shape element also calls update_name for street names
    # and others for other cleanup we may do
    # Write it out to the JSON file

    # Switch this from sample to full data set
    print 'cleaning the file'
    #file_out = "phoenix_arizona_sample.json".format(input_file)
    file_out = "phoenix_arizona.json".format(input_file)
    with codecs.open(file_out, "w") as fo:
        for event, element in ET.iterparse(input_file, events=("start",)):
            if element.tag == "node":
                el = shape_element_node (element)
                fo.write(json.dumps(el, indent=2) + "\n")
            elif element.tag == "way":
                el = shape_element_way(element)
                fo.write(json.dumps(el, indent=2) + "\n")
            elif element.tag == "osm":
                # ignore the osm tag at the start of the file
                pass
            else:
                # ignore other element tags such as member and relation
                #print element.tag
                #print 'We have an element type that isnt node or way'
                pass





if __name__ == "__main__":
    from pymongo import MongoClient
    from collections import defaultdict
    import xml.etree.ElementTree as ET
    import re
    import pprint
    import codecs
    import json
    # Mongo running on VM at this address via host-only network 3
    client = MongoClient("mongodb://10.1.1.10:27017")
    street_types = defaultdict(set)
    street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
    problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

    mapping = { "St": "Street",
            "St.": "Street",
            "Ave": "Avenue",
            "Rd.": "Road",
            "Rd" : "Road",
            "Blvd": "Boulevard",
            "Parkwway" : "Parkway"
            }


    db = client.osm
    # Read the data in - switch this and the JSON output file name
    m = process_file('phoenix_arizona.osm')
    #m = process_file('phoenix_arizona_sample.osm')

    # Audit the data
    audit (m)

    # Clean the data, reformats and writes out to JSON file
    # We have to reopen the file because it has been read previously it seems
    m = process_file('phoenix_arizona.osm')
    #m = process_file('phoenix_arizona_sample.osm')
    clean_and_reformat (m)


    # Now the output data is ready for importing into MongoDB using mongoimport from Mac client
    # mongoimport -h 10.1.1.10 --db osm -c phoenix --file phoenix_arizona_sample.json
    # mongoimport -h 10.1.1.10 --db osm -c phoenix --file phoenix_arizona.json

    # use db.phoenix.drop() to drop the phoenix database and the collections in it to redo import