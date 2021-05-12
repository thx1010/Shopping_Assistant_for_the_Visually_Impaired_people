# USAGE
# python download_images.py --urls urls.txt --output images

from imutils import paths
import argparse
import requests
import cv2
import os

#argument 파싱
ap = argparse.ArgumentParser()
ap.add_argument("-u", "--urls", required=True,
	help="path to file containing image URLs")
ap.add_argument("-o", "--output", required=True,
	help="path to output directory of images")
args = vars(ap.parse_args())

#인풋 파일로부터 URL 리스트를 받고, 다운로드할 이미지 목록을 초기화함
rows = open(args["urls"]).read().strip().split("\n")
total = 0


for url in rows:
	try:
		r = requests.get(url, timeout=60)

		p = os.path.sep.join([args["output"], "S_{}.jpg".format(
			str(total).zfill(8))])
		f = open(p, "wb")
		f.write(r.content)
		f.close()

		print("[INFO] downloaded: {}".format(p))
		total += 1

	except:
		print("[INFO] error downloading {}...skipping".format(p))

# loop over the image paths we just downloaded
for imagePath in paths.list_images(args["output"]):
	# initialize if the image should be deleted or not
	delete = False

	# try to load the image
	try:
		image = cv2.imread(imagePath)

		# if the image is `None` then we could not properly load it
		# from disk, so delete it
		if image is None:
			print("None")
			delete = True

	# if OpenCV cannot load the image then the image is likely
	# corrupt so we should delete it
	except:
		print("Except")
		delete = True

	# check to see if the image should be deleted
	if delete:
		print("[INFO] deleting {}".format(imagePath))
		os.remove(imagePath)
