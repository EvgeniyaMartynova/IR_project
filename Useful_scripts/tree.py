from collections import defaultdict

input_ = open("topic_names.txt",'r')
"""input_ = '''dir/file
dir/dir2/file2
dir/file3
dir2/alpha/beta/gamma/delta
dir2/alpha/beta/gamma/delta/
dir3/file4
dir3/file5'''"""

FILE_MARKER = '<files>'

def attach(branch, trunk):
    '''
    Insert a branch of directories on its trunk.
    '''
    parts = branch.split('/', 1)
    if len(parts) == 1:  # branch is a file
        trunk[FILE_MARKER].append(parts[0])
    else:
        node, others = parts
        if node not in trunk:
            trunk[node] = defaultdict(dict, ((FILE_MARKER, []),))
        attach(others, trunk[node])

def prettify(d, indent=0):
    '''
    Print the file tree structure with proper indentation.
    '''
    for key, value in d.items():
        if key == FILE_MARKER:
            if value:
                print('  ' * indent + str(value))
        else:
            print('  ' * indent + str(key))
            if isinstance(value, dict):
                prettify(value, indent+1)
            else:
                print('  ' * (indent+1) + str(value))



main_dict = defaultdict(dict, ((FILE_MARKER, []),))
for l in input_:
    l = l.split('\t')
    line = l[1].rstrip() + " " + l[0]
    attach(line, main_dict)

prettify(main_dict)