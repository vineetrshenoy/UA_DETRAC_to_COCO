from pycocotools.coco import COCO
import numpy as np
import skimage.io as io
import matplotlib.pyplot as plt
import pylab
import random
pylab.rcParams['figure.figsize'] = (8.0, 10.0)


class CocoVisualize:

    def __init__(self, annotations):

        self.annFile = annotations
        self.coco = COCO(self.annFile)




    def visualize(self, category_id):
        catIds = self.coco.getCatIds(catNms=['car'])
        imgIds = self.coco.getImgIds(catIds=catIds )

        #for i in range(0, len(imgIds), 150):
        for i in random.sample(imgIds, 5):

            img = self.coco.loadImgs(imgIds[i])[0]
            
            I = io.imread(img['file_name'])
            plt.imshow(I); plt.axis('off')
            annIds = self.coco.getAnnIds(imgIds=img['id'], catIds=catIds, iscrowd=None)
            anns = self.coco.loadAnns(annIds)
            self.coco.showAnns(anns)
            plt.title(img['file_name'])
            plt.show()
            


if __name__ == '__main__':

    #c = CocoVisualize('annotations.json')
    #c.visualize('car')

    
    annFile='annotations.json'
    coco=COCO(annFile)


    # initialize COCO api for instance annotations
    # get all images containing given categories, select one at random
    catIds = coco.getCatIds(catNms=['car'])
    #imgIds = coco.getImgIds(catIds=catIds )
    imgIds = coco.getImgIds(imgIds = [372])
    img = coco.loadImgs(imgIds[0])[0]

    # load and display image
    # I = io.imread('%s/images/%s/%s'%(dataDir,dataType,img['file_name']))
    # use url to load image

    I = io.imread(img['file_name'])
    plt.axis('off')
    plt.imshow(I)
    plt.show()

    # load and display instance annotations
    # load and display instance annotations
    plt.imshow(I); plt.axis('off')
    annIds = coco.getAnnIds(imgIds=img['id'], catIds=catIds, iscrowd=None)
    anns = coco.loadAnns(annIds)
    coco.showAnns(anns)
    plt.title(img['file_name'])
    plt.show()
    x = 5
    