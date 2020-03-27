import xml.etree.ElementTree as ET
import datetime
import os
import json
import glob
import argparse
from pycoco_visualize import CocoVisualize
count = 0

class UA_to_COCO:

	## 
	#	@details Creates the UA_to_COCO object
	#	
	#
	def __init__(self, item_list):

		self.annot_count = 1
		self.image_count = 1
		self.item_list = item_list
		self.dict_map = {}

	## 
	#	@details Creates the 'info' section of the annotations
	#	@returns 'info' dictionary
	#
	def get_info(self):

		info = {'year': datetime.date.today().year, 'version': '1.0',
		'description': "UA-Detrac", 'contributor': "Vineet Shenoy", 
		'url': 'http://detrac-db.rit.albany.edu/', 'date_created': datetime.datetime.now().strftime("%H:%M:%S.%f - %b %d %Y") }

		return info

	## 
	#	@details Creates the 'licenses' section of the annotations
	#	@returns 'licenses' dictionary
	#
	def get_licenses(self):

		license = [{'id': 1, 'name': "Creative Commons Attribution-NonCommercial-ShareAlike 3.0 License",
		'url': 'https://creativecommons.org/licenses/by-nc-sa/3.0/' }]

		return license

	## 
	#	@details Creates the 'catgeories' section of the annotations
	#	@returns 'categoies' array of dictionaries
	#
	def get_categories(self):

		categories = [
		{'id': 1, 'name': 'car', 'supercategory': 'vehicle'},
		{'id': 2, 'name': 'bus', 'supercategory': 'vehicle'},
		{'id': 3, 'name': 'van', 'supercategory': 'vehicle'}]
		
		return categories

	## 
	#	@details Creates the 'images' section of the annotations
	#	@param folder_path The folder path from which to pull the images
	#	@returns 'images' array
	#
	def get_images(self, folder_path):

		os.chdir(folder_path)
		filenames = glob.glob('*.jpg')
		os.chdir('..')
		imgs = [None] * len(filenames)
		fol_ident = folder_path.split('_')[1]
		self.dict_map[fol_ident] = {}
		for i in range(0, len(filenames)):

			image_file_number = os.path.splitext(filenames[i])[0]
			image_file_number = int(image_file_number.split('g')[1].lstrip('0'))
			img_id = self.image_count
			self.dict_map[fol_ident][image_file_number] = img_id
			image_dict = {'width': 960, 'height': 540, 'license': 1, 
			'date_captured': datetime.datetime.now().strftime("%H:%M:%S.%f - %b %d %Y"), 'id': img_id}
			image_dict['file_name'] = folder_path + '/' + filenames[i]
			imgs[i] = image_dict

			self.image_count += 1

		return imgs

	## 
	#	@details Helper Function: Returns the category ID for a certain 
	#	@param item The string from the XML file, which will be converted to an int category_id
	#	@returns 'category_id' integer
	#
	def get_category_id(self, item):


		#return 1
		
		return {
			'car': 1,
			'bus': 2, 
			'van': 3,
		}.get(item, 1)
		

	## 
	#	@details Gets segmentation data in the coco format
	#	@param item The XML file for a certain folder
	#	@returns 'annotations' array
	#
	def get_annotation(self, item):

		#os.chdir('annot')
		tree = ET.parse(item)
		#os.chdir('..')
		root = tree.getroot()
		fol_ident = item.split('_')[1].split('.')[0]
		annotations = []

		for frame in root.findall('frame'):

			for target in frame[0]:
				#count += 1
				
				area = int(float((target[0].attrib['height']))) * int(float((target[0].attrib['width'])))
				image_id = int(frame.attrib['num'])
				category_id = self.get_category_id(target[1].attrib['vehicle_type'])

				x = float(target[0].attrib['left'])
				y = float(target[0].attrib['top'])
				width = float(target[0].attrib['width'])
				height = float(target[0].attrib['height'])
				bbox = [x, y, width, height]

				seg_dict = {
					'id': self.annot_count,
					'image_id': self.dict_map[fol_ident][image_id],
					'category_id': category_id,
					'segmentation': [[x, y, x + width, y, x + width, y + height, x, y + height]],
					'area': float(area),
					'bbox': bbox,
					'iscrowd': 0
				}

				self.annot_count += 1
				annotations.append(seg_dict)
		
		return annotations

	## 
	#	@details Builds the annotation structure from the individual parts. The 'main' of the program
	#	@returns None. Writes annotations to a file called 'annotations.json'
	#
	def build_structure(self):

		da = {}
		da['info'] = self.get_info()
		da['licenses'] = self.get_licenses()
		da['categories'] = self.get_categories()
		da['images'] = []
		da['annotations'] = []

		if '__pycache__' in self.item_list:
			self.item_list.remove('__pycache__')
		
		for item in self.item_list:
			images = self.get_images(item)
			annotations = self.get_annotation(item + '.xml') 

			da['images'] = da['images'] + images
			da['annotations'] = da['annotations'] + annotations
		
		with open('annotations.json', 'w') as fp:
			json.dump(da, fp)
			
		


if __name__ == '__main__':
	
	parser = argparse.ArgumentParser('Annotation generator')
	parser.add_argument('--visualize', default=1)

	args = vars(parser.parse_args())
	
	
	obj = UA_to_COCO(next(os.walk('.'))[1])
	obj.build_structure()
	
	print(args)
	if int(args['visualize']) == 1:
		c = CocoVisualize('annotations.json')
		c.visualize('car')
	
	#obj = UA_to_COCO(next(os.walk('.'))[1])
	#print(obj.get_category_id('bus'))