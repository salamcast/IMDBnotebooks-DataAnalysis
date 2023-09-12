# files
import os
import re
import shutil

global USB
global SD

def scan_dir(path, Dir):
    files = os.listdir(path)
    #base
    for n1 in files:
        if os.path.isdir(path + '/' + n1):
            Dir.append ( path + '/' + n1)
            Dir = scan_dir(path + '/' + n1, Dir)
    return Dir

def scan_files(path, Files):
    files = os.listdir(path)
    #base
    for n1 in files:
        if os.path.isfile(path + '/' + n1):
            Files.append (path + '/' + n1)
        elif os.path.isdir(path + '/' + n1):
            Files = scan_files(path + '/' + n1, Files)
    return Files

def show_files(Dir, output=False):
    Files = []
    Files = scan_files(Dir, Files)
    Files.sort()
    Cast = {}
    for f in Files:

        show = get_show(Dir)
        year = get_year(Dir)
        fileBase=re.sub('\D*\([0-9]{4}\)', '', re.sub('.[mM][4Pp][4Vv]', '', os.path.basename(f)))
        E = re.findall(r'([1-9]|[1-9][0-9])', fileBase)
        key = E[0]+"x"+E[1]

        Cast[key] = {
            'show': show,
            'year': year,
            'S': E[0],
            'E': E[1],
            'file': f,
            'dir': Dir
        }
        if output:
            print(show + ", "+ year+ ", "+ E[0]+ ", "+ E[1]+", "+f+", "+Dir )
            #print(dirBase, ", ", E[0], ", ", E[1], ", ",  fileBase, ", ", f, ", ", Dir )
    return Cast

def scan_TV(TVCast):
    TV = []
    for t in TVCast:
        TV = scan_dir(t, TV)
    #TV.sort()
    return TV

def install_movie_match(old, new, Dir):  
    os.makedirs(Dir, mode = 0o777, exist_ok = True)
    file = shutil.move(old,new)
    if file:
#        os.remove(old)
        return True

def get_year(path):
    base = os.path.basename(path)
    S = re.split('\(', base)
    if len(S) > 1:
        year = re.sub(' ', '', re.sub('\)', '', re.sub('.[mM][Oo4Pp][4Vv]', '', S[1])))
        year = year.strip()
        return year
    return "1900"

def get_show(path):
    base = os.path.basename(path)
    S = re.split('\(', base)
    show = re.sub(';', ':', S[0], 1)
    show = show.strip()
    return show


def new_dir(MediaType, Dir):
    new = Root + "/" + MediaType + "/" + Dir
    return re.sub('#', '', re.sub(':', ';', new) )
    
def new_file(MediaType, Dir, File):
    new = Root + '/' + MediaType + "/" + Dir + '/' + re.sub('/', '_',File)
    return re.sub('#', '', re.sub(':', ';', new) ) + '.mp4'