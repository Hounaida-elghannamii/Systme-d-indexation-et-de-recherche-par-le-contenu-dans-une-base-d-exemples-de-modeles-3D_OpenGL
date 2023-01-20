from calculeDescripteur3d import object3D
from os import walk
import json

def getObjects_names(direpath):
    objects_name = []
    for (dirpath, dirnames, filenames) in walk(direpath):  
        for filename in filenames:
            objects_name.append(direpath+"/"+filename)
        for direname in dirnames:
           objects_name.extend(getObjects_names(direpath+"/"+direname))
    return objects_name


if __name__ == "__main__":
    outstats = open('database.json', 'w')
    outstats.write("[")
    objects_names=getObjects_names("./data/3D_Models")
    
    for obj in objects_names:
        try:
            obj3d=object3D(obj)
            json.dump(
                obj3d.getObjDescripteur(),
                outstats
            )
            if(obj!=objects_names[len(objects_names)-1]):
                outstats.write(",")
        except Exception as e:
            print(e)
        

    
    # outstats.write("]")
