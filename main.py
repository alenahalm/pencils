from skimage.measure import label, regionprops
from skimage.morphology import binary_closing
import cv2 as cv

def truncate(n, decimals=0):
    multiplier = 10 ** decimals
    return int(n * multiplier) / multiplier

sum = 0
for num in range(1, 13):
        
    filename = f'images/img{num}.jpg'
    image = cv.imread(filename)

    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    gray[gray > 125] = 0
    gray[gray != 0] = 255
    gray = binary_closing(binary_closing(gray))
    labeled = label(gray)
    regions = regionprops(labeled)

    objects = []
    area_thresh = 100000

    for i in range(len(regions)):
        area = regions[i].image.shape[0]*regions[i].image.shape[1]
        if area > area_thresh:
            objects.append(regions[i])
    
    count = 0
    min_area = 250000

    for img in objects:
        ecc = img.eccentricity
        if truncate(ecc, 3) >= 0.998 and img.area > min_area:
            count += 1
    sum += count
    print(f'image {num}: {count}')


    cv.destroyAllWindows()
print(f'{sum} pencils')
