import xml.etree.ElementTree as ET
import hashlib
import os.path
from typing import Callable, Dict, Optional
from functools import lru_cache

@lru_cache(maxsize=None)
def _get_title_dict(cache_dir, system) -> Dict[str, str]:
    prio_path = os.path.join(cache_dir, system, 'priorities.xml')
    if not os.path.exists(prio_path):
        return {}
    prio_root = ET.parse(prio_path).getroot()
    prio_nodes = prio_root.findall('.//*[@type="title"]/source')
    prio = list(map(lambda x: x.text, prio_nodes))

    db_path = os.path.join(cache_dir, system, 'db.xml')
    if not os.path.exists(db_path):
        return {}
    db_root = ET.parse(db_path).getroot()
    db_nodes = db_root.findall('.//*[@type="title"]')

    title_dict = {}
    for node in db_nodes:
        db = [(x.text, x.get('source')) for x in node]
        res = (y[0] for x in prio for y in db if y[1] == x)
        title_dict[node.get('sha1')] = node.text
    return title_dict


@lru_cache(maxsize=None)
def _calculate_hash(rom_path: str) -> str:
    BLOCKSIZE = 65536
    hasher = hashlib.sha1()
    with open(rom_path, 'rb') as f:
        buf = f.read(BLOCKSIZE)
        while len(buf) > 0:
            hasher.update(buf)
            buf = f.read(BLOCKSIZE)
    return hasher.hexdigest()

def get_skyscraper_callable(cache_dir: Optional[str] = None
                           ) -> Callable[[str, str], Optional[str]]:
    def get_rom_title(rom_path: str, system: str) -> str:
        if not os.path.exists(rom_path):
            return None
        sha1sum = _calculate_hash(rom_path)
        td = _get_title_dict(cache_dir, system)
        return td.get(sha1sum)
    return get_rom_title
