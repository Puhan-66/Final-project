import matplotlib.pyplot as plt
import matplotlib.image as mpimg

img = mpimg.imread('field.png')

fig, ax = plt.subplots(figsize=(12, 6))
ax.imshow(img)
plt.title('请用鼠标点击 NFL (0,0) 点')
pts = plt.ginput(1)    # 鼠标点击一次你认为的(0,0)点
print('你点击的像素坐标:', pts)
plt.show()

