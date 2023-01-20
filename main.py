import cv2
import numpy as np
import math, cmath
import features
import json

IMAGES_DB = 323
HU_MOMENTS = 7
FOURIER_DESCRIPTORS = 21

class Image:
  def __init__(self, image_name, distanceHu , distanceFourier , distance ):
    self.image_name = image_name
    self.distanceHu = distanceHu
    self.distanceFourier = distanceFourier
    self.distance = distance
  
  def __repr__(self):
    return f"({self.image_name}, {self.distance})"



def calculate_euclidean_distance(huMoments_db, inHuMoments):
  result_sum = 0
  for i in range(HU_MOMENTS):
    result_sum += ((huMoments_db[i] - inHuMoments[i])**2)

  return math.sqrt(result_sum)







def getImageInfo(imagee):
   img = cv2.imread("static/pics/"+imagee, cv2.IMREAD_GRAYSCALE)
   retval, th = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU) 
   descriptors = features.find_descriptors(th)
   fourier_filt = descriptors[0:21]
   imageInfo={"image":imagee,"huMoments":features.find_huMoments(th).tolist(),"fourierDescriptors":str(fourier_filt.tolist()),}
   return imageInfo

def GetForierComplex(discripteur):
  TF1=discripteur.replace('(', '')
  TF1=TF1.replace(')', '')
  TF1=TF1.replace('[', '')
  TF1=TF1.replace(']', '')
  array_complex = TF1.split(',')
  TF1 = []
  for num in array_complex:
    TF1.append(complex(num))
  TF1=np.array(TF1)
  return TF1



def Search_Fct(img):
    myfile = open("database.json", "r")
    imagesInfo = json.load(myfile)
    principalImg=getImageInfo(img)
    results=list()
    i=0
    for imgInfo in imagesInfo:
      distanceHuMoment=calculate_euclidean_distance(imgInfo["huMoments"] , principalImg["huMoments"])
      try:
        distanceFourier=np.linalg.norm(GetForierComplex(imgInfo["fourierDescriptors"])- GetForierComplex(principalImg["fourierDescriptors"]))
      except:
        continue
      vect=np.array([distanceHuMoment,distanceFourier])
      norm=np.linalg.norm(vect)
      imgg=Image(imgInfo["image"] , distanceHuMoment , distanceFourier , norm )
      results.append(imgg)
      distances_sorted = sorted(results, key=lambda f: f.distance)
    return distances_sorted[:20]

