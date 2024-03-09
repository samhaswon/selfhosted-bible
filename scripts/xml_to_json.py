import json
import xml.etree.ElementTree as ET
from bibles.compresscache import CompressCache


if __name__ == '__main__':
    json_version = {}

    version_short = "RNKJV"

    tree = ET.parse(f"{version_short}.xml")
    root = tree.getroot()
    for book in root:
        if book.tag == 'INFORMATION':
            continue
        name = book.attrib["bname"]
        if name.startswith("I "):
            name = "1" + name[1:]
        elif name.startswith("II "):
            name = "2" + name[2:]
        elif name.startswith("III "):
            name = "3" + name[3:]
        elif name == "Psalm":
            name = "Psalms"
        elif "Revelation" in name:
            name = "Revelation"

        json_version[name] = {}

        for chapter in book:
            number = chapter.attrib["cnumber"]
            json_version[name][number] = []
            for verse in chapter:
                if verse.text:
                    content = verse.attrib["vnumber"] + " " + verse.text
                    json_version[name][number].append(content)

    with open(f"{version_short.lower()}.json", "w") as json_file:
        json_file.write(json.dumps(json_version))

    compress_cache = CompressCache(version_short.lower())
    compress_cache.save(json_version)
