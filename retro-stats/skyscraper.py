import xml.etree.ElementTree as ET
import hashlib
import os.path

def get_skyscraper_title(rom_path: str,
                         system: str,
                         skyscraper_cache_dir: str = '~/.skyscraper/cache') -> str:
    BLOCKSIZE = 65536
    hasher = hashlib.sha1()
    with open(rom_path, 'rb') as f:
        buf = f.read(BLOCKSIZE)
        while len(buf) > 0:
            hasher.update(buf)
            buf = f.read(BLOCKSIZE)
    sha1sum = hasher.hexdigest()
    prio_path = os.path.join(skyscraper_cache_dir, system, 'priorities.xml')
    prio_root = ET.parse(prio_path).getroot()
    prio_nodes = prio_root.findall('.//*[@type="title"]/source')
    prio = list(map(lambda x: x.text, prio_nodes))

    prio_path = os.path.join(skyscraper_cache_dir, system, 'db.xml')
    db_root = ET.parse('db.xml').getroot()
    db_nodes = db_root.findall('.//*[@type="title"][@sha1="{}"]'.format(sha1sum))
    db = [(x.text, x.get('source')) for x in db_nodes]

    res = [y for x in prio for y in db if y[1] == x]
    return res[0][0]
