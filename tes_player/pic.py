import cv2

img = cv2.imread('src/images/player00.png')
blue, green, red = cv2.split(img)
bgr_img = cv2.merge([blue - 50, green - 50, red - 50])
cv2.imshow("B -> G -> R", bgr_img)

rgb_img = cv2.merge([green, blue, red])
cv2.imshow("R -> G -> B", rgb_img)

cv2.waitKey(0)
cv2.destroyAllWindows()