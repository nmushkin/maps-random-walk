import csv

import matplotlib.pyplot as plt

locs = list(csv.reader(open("locations.txt"), delimiter=" "))

lats = [float(w.split(",")[0][:12]) for w in locs[0]]
longs = [float(w.split(",")[1][:12]) for w in locs[0]]

bounding_box = (min(longs), max(longs), min(lats), max(lats))
plt.figure()
plt.scatter(longs, lats, zorder=1)
plt.xlim(bounding_box[0], bounding_box[1])
plt.ylim(bounding_box[2], bounding_box[3])
# If you have an image to be displayed under scatter e.g. map
# plt.imshow(plt.imread("map.png"), zorder=0, extent=bounding_box)
plt.show()
print(bounding_box)