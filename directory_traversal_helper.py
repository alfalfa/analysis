import os
import re

def get_files_matching_regex(directory_path, regex):
    ret = []
    for dirpath,_,filenames in os.walk(directory_path):
        for f in filenames:
            filepath = os.path.abspath(os.path.join(dirpath, f))
            match_object = re.search(regex, filepath)
            if match_object:
                # if regex has no subgroups use file name as identifier
                identifier = f if len(match_object.groups()) is 0 else match_object.group(1)
                ret.append((filepath, identifier))
            else:
                print("no match for " + f)
    return ret
