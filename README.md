# UA-DETRAC to COCO

The following code converts the [UA-DETRAC](http://detrac-db.rit.albany.edu/) data to the COCO format. You will need

1. `xml_to_coco.py`
2. `pycoco_visualize.py`
3. `cocotools.yml`

## Installing the dependencies
I assume you are using the `conda` package environment. `cd` into the directory that contains the `cocotools.yml`. Then run

```
conda env -f cocotools.yml
```

These are all the dependencies you need

## Running the code

The organization of the folder must be very specific, as follows:

```
project
│   README.md
│   xml_to_coco.py
│   pycoco_visualize.py
│   MVI_20032.xml
└───MVI_20032
│   │   file011.jpg
│   │   file012.jpg
│   
│   MVI_20035.xml
└───MVI_20035
    │   file01.jpg
    │   file02.jpg
```

Basically, the folders with all the images, the XML files and `xml_to_coco.py` and `pycoco_visualize` should be in the same folder

## Running the code
Activate the environment using `conda activate cocotools`. The code is run with the following command

```
python xml_to_coco.py --visualize 1
```

When the `--visualize` flag is set to one, you will see 5 random samples of the annotations overlayed on the original images. The annotations are written to `annotations.json` in the same folder as above.