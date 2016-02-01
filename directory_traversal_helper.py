import os
import re

def get_filenames_matching_regex(directory_path, regex):
    ret = []
    for dirpath,_,filenames in os.walk(directory_path):
        for f in filenames:
            match_object = re.search(regex, f)
            if match_object:
                filename = os.path.abspath(os.path.join(dirpath, f))
                identifier = match_object.group(1)
                ret.append((filename, identifier))
    return ret
