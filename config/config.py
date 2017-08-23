
import configparser
from collections import namedtuple


config = configparser.ConfigParser()
config.read("./sample.cfg")

all_sections = " ".join(config.sections())
ConfigStruct = namedtuple('ConfigStruct', all_sections)
sections = dict()

for section in config.items():
    section_name = section[0]
    if "DEFAULT" == section_name:
        continue
    print(" > Building section {}...".format(section_name))
    section_all_keys = " ".join(section[1].keys())
    # print (all_sections_keys)
    SectionStruct = namedtuple('SectionStruct', section_all_keys)
    section_pairs = dict()
    for k, v in section[1].items():
        if "csv" in k.lower():
            section_pairs[k] = v.split(",")
        else:
            section_pairs[k] = v
    section_details = SectionStruct(**section_pairs)

    sections[section_name] = section_details

app = ConfigStruct(**sections)
