import sys
import os
import numpy as np
import json
from scipy.spatial import distance

# Define the object3D class
def distanceKey(state):
    return state['distance']
class object3D:
    def __init__(self, filename):
        self.filename = filename
        self.descriptor=[]
        self.vertices=[]
        if(os.path.exists(filename)):
            self.file=open(self.filename, 'r')
        else:
            raise Exception("file "+filename+" not exist ")



    def getObjDescripteur(self):
        file = self.file
        ver=list()
        for line in file:
            if line.startswith('v '):
                vertex = line.split()
                ver.append([float(vertex[1]), float(vertex[2]), float(vertex[3])])
        ver2=np.array(ver)


        X = ver2[:, 0]
        Y = ver2[:, 1]
        Z = ver2[:, 2]
        xx=get3DFourierDescriptor(X,Y,Z,100)
        
        return {
            "filename":self.filename,
            "descriptor": xx.tolist()
        }



        


#calcul dist euc
def get3DFourierSimilarity(descriptor1, descriptor2):
    # calculate the Euclidean distance between two descriptors
    dist = distance.euclidean(descriptor1, descriptor2)
    # calculate the similarity score
    similarity_score = dist
    return similarity_score

#obtenir un tableau trié de distance entre le nom de fichier et tous les objets de la base de données
def GetSimilar(fileName):
        file = fileName
        ver=list()
        if(os.path.exists(file)):
            file=open(file, 'r')
        for line in file:
            if line.startswith('v '):
                vertex = line.split()
                ver.append([float(vertex[1]), float(vertex[2]), float(vertex[3])])
        ver2=np.array(ver)
        X = ver2[:, 0]
        Y = ver2[:, 1]
        Z = ver2[:, 2]
        disc=get3DFourierDescriptor(X,Y,Z,100)
        #print(disc.shape)
        data = open("database.json", "r")
        database = json.load(data)
        results=list()
        for obj in database:
            #print( np.array( obj["descriptor"]).shape)
            try:
                results.append(
                    {
                        "filaname":obj["filename"],
                        "image": obj['filename'].replace("3D_Models","Thumbnails").replace(".obj",".jpg"),
                        "distance": get3DFourierSimilarity(obj["descriptor"] , disc)
                    }
                )
            except :
                continue
        results=sorted(results, key=lambda k: k['distance'], reverse=False)
        return results




##calcul descripteur forrrier d'un objet 3D(objet)
def get3DFourierDescriptor(X, Y, Z, n_descriptors):
        fft3d_X = np.fft.fftn(X)
        fft3d_Y = np.fft.fftn(Y)
        fft3d_Z = np.fft.fftn(Z)
        
        # magnitude 
        mag_fft3d_X = np.abs(fft3d_X)
        mag_fft3d_Y = np.abs(fft3d_Y)
        mag_fft3d_Z = np.abs(fft3d_Z)
        
        # phase 
        phs_fft3d_X = np.angle(fft3d_X)
        phs_fft3d_Y = np.angle(fft3d_Y)
        phs_fft3d_Z = np.angle(fft3d_Z)
        
        # Get the first n_descriptors
        mag_fft3d_X_desc = mag_fft3d_X[0:n_descriptors].flatten()
        mag_fft3d_Y_desc = mag_fft3d_Y[0:n_descriptors].flatten()
        mag_fft3d_Z_desc = mag_fft3d_Z[0:n_descriptors].flatten()
        phs_fft3d_X_desc = phs_fft3d_X[0:n_descriptors].flatten()
        phs_fft3d_Y_desc = phs_fft3d_Y[0:n_descriptors].flatten()
        phs_fft3d_Z_desc = phs_fft3d_Z[0:n_descriptors].flatten()
        
        # combine the magnitude and phase into one descriptor
        descriptor = np.concatenate((mag_fft3d_X_desc, mag_fft3d_Y_desc, mag_fft3d_Z_desc,
                                    phs_fft3d_X_desc, phs_fft3d_Y_desc, phs_fft3d_Z_desc))
        #print(descriptor.shape)
        return descriptor






