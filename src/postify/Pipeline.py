import os, glob
from . import Cache
from . import To, From
_pipeline = []
_names = []

def _set_pipeline ( items ):
    global _pipeline
    _pipeline = items

def _get_pipeline ():
    global _pipeline
    return _pipeline

def InputFiles ( match ):
    files = glob.glob(match)
    images = []
    for file in files:
        print("Loading: " + file)
        From.local_file(file)
        images.append(Cache.get_last_img())
    _set_pipeline(images)
    global _names
    _names = files

def RunWith ( callback ):
    results = []
    global _names
    for i,file in enumerate(_get_pipeline()):
        print("Running: " + _names[i])
        Cache.set_last_img(file)
        callback()
        results.append(Cache.get_last_img())
    _set_pipeline(results)

def SaveFiles (directory):
    global _names
    for i, img in enumerate(_get_pipeline()):
        filename = os.path.basename(_names[i])
        filename = os.path.join(directory, filename)
        Cache.set_last_img(img)
        print("Saving: " + filename)
        To.local_file(filename)

    
def Show ( number = 3):
    print("Showing: " + str(number) + " images of " + str(len(_get_pipeline())))
    if number > len(_get_pipeline()):
        number = len(_get_pipeline())
    for i in range(number):
        Cache.set_last_img(_get_pipeline()[i])
        To.notebook()