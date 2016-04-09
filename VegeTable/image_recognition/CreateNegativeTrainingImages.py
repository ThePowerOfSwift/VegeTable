import urllib

for i in range(1,100,1):
    urllib.urlretrieve("http://lorempixel.com/200/200/", "../../data/imagenet/training_images/Unknown/negImage"+str(i)+".JPEG")
