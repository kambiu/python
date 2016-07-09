from lxml import etree
# from pprint import pprint

ns = {"de": "http://www.develop.com/student"}

# def dump(obj):
#   for attr in dir(obj):
#     print "obj.%s = %s" % (attr, getattr(obj, attr))

tree = etree.parse(open('sample.xml'))
root = tree.getroot()

# print root.findall("/de:id", ns)
for s in  root.xpath("/student/de:id/de:kk", namespaces=ns):
    print s.text
