---
title: 图像空域隐写技术：LSB及其改进
date: 2024-01-11
categories:
  - 信息隐藏
tags:
  - 信息隐藏
  - LSB
---



### 灰度图

灰度图就是使用黑色，白色和它们之间不同程度的灰色表示的图片。一般来说灰度图的每个像素在计算机中使用8比特表示，也就是8比特位深，有0-255共256个颜色值。
下面是一张512*512像素8比特位深灰度图：
![Alt text](/img/steg_lsb/lena.bmp)

### 位图

对于8比特表示的灰度图，高位比特对像素颜色的贡献明显高于低位比特。就像十进制111，明显百位的“1”是100，个位的“1”是1，100对111的贡献显然比1要大得多，其他进制包括二进制也是这个道理。
编写程序取不同比特位构建出新的位平面图就可以看清每个比特位对图片了贡献了。

```python
import cv2
import numpy as np
from matplotlib import pyplot as plt

# 读取灰度图像
img = cv2.imread('lena.bmp', cv2.IMREAD_GRAYSCALE)

# 获取图像的宽度和高度
height, width = img.shape

# 初始化一个全零矩阵，用于存储每个平面的像素值
planes = np.zeros((height, width, 8), dtype=np.uint8)

# 将每个像素点的二进制表示拆分为8个位平面
for i in range(8):
    planes[:, :, i] = cv2.bitwise_and(img, 2 ** i)
    planes[:, :, i] = planes[:, :, i] * 255 / 2 ** i

# 展示每个位平面
for i in range(8):
    plt.subplot(2, 4, i+1)
    plt.imshow(planes[:, :, i], cmap='gray')
    plt.axis('off')

# 显示窗口
plt.show()

```

第1-8位平面图，可以看到高位对图像贡献高，而低位贡献低：
![Alt text](/img/steg_lsb/image.png)

### LSB

LSB表示最低位比特。
经过上面分析，发现最低位对图像的贡献很小，其实也符合直觉。比如一个8比特像素11111111表示255，那么去掉最后一位变成11111110表示254，颜色差别只会相差1。
那么这种差距人眼是否能够察觉呢？
编写代码去除最低位平面。

```python
import cv2
import numpy as np
from matplotlib import pyplot as plt

# 读取灰度图像
img = cv2.imread('lena.bmp', cv2.IMREAD_GRAYSCALE)

# 获取图像的宽度和高度
height, width = img.shape

# 去除最低位平面
planes = np.zeros((height, width, 8), dtype=np.uint8)
for i in range(8):
    planes[:, :, i] = cv2.bitwise_and(img, 2 ** i)

# 去除最低位平面
removed_plane_img = np.copy(img) # 复制原始图像
removed_plane_img &= 0xFE # 将最低位清零

# 展示原图和去除最低位平面的图像
plt.subplot(1, 2, 1)
plt.imshow(img, cmap='gray')
plt.title('Original Image')
plt.axis('off')

plt.subplot(1, 2, 2)
plt.imshow(removed_plane_img, cmap='gray')
plt.title('Image with Lowest Bit Plane Removed')
plt.axis('off')

# 显示窗口
plt.show()

```

这是将最低位平面去除的图像：
![Alt text](/img/steg_lsb/image-1.png)
既然，最低位平面去除对于视觉几乎没有影响，那么在最低位平面进行信息隐藏就具有可行性。

### LSB隐写

简单来说，首先清空灰度图的最低位平面，即将所有比特置为0。然后将所要隐写的信息填入最低位平面即可。
有一个问题是我们可能填入不了一整个位平面。因此只需要填入比特时改变原始比特为填入比特即可。
下面代码给出嵌入图片的代码：

```python
import cv2
import numpy as np

# 读取原始图像
img = cv2.imread('lena.bmp')

# 将文本转换为二进制形式
text = "Hello, World!\0"
binary_text = ''.join(format(ord(char), '08b') for char in text)


# 定义嵌入函数
def embed_text(img, text):
    # 检查文本长度是否超过图像可容纳的位数
    max_len = img.shape[0] * img.shape[1] * 3
    if len(text) > max_len:
        raise ValueError("Text is too long to embed into the image.")

    # 将文本逐位嵌入到图像的最低有效位
    text_index = 0
    for row in img:
        for pixel in row:
            for i in range(3):
                if text_index < len(text):
                    # 将文本的每一位嵌入到像素的最低有效位
                    pixel[i] = (pixel[i] & 0xFE) | int(text[text_index])
                    text_index += 1
                else:
                    break
            if text_index >= len(text):
                break
        if text_index >= len(text):
            break

    return img


# 嵌入文本到图像中
embedded_img = embed_text(np.copy(img), binary_text)

# 保存嵌入文本后的图像
cv2.imwrite('lena_embedded.bmp', embedded_img)

# 读取嵌入了文本的图像
embedded_img = cv2.imread('lena_embedded.bmp')


# 定义提取函数
def extract_text(img):
    binary_text = ''
    for row in img:
        for pixel in row:
            for i in range(3):
                # 提取像素的最低有效位
                binary_text += str(pixel[i] & 1)

    # 将二进制文本转换为字符形式
    text = ''
    for i in range(0, len(binary_text), 8):
        text += chr(int(binary_text[i:i + 8], 2))
        if text[-1] == '\0':
            break

    return text[:-1]


# 提取嵌入的文本
extracted_text = extract_text(np.copy(embedded_img))

# 打印提取的文本
print(extracted_text)

```


### LSB隐写改进

LSB隐写有不错的容量，如果考虑使用最低三位进行隐写，那么一张图片可以容纳像素*3的比特的信息。
但是如果嵌入比特，那么可能会暴露一些统计特性。由于正常图片最低位比特一般由相机噪声决定，0和1是随机生成的，各站50%。
如果大量嵌入不是50%比例的0和1，那么这个统计特性将会被改变。
即使嵌入相同比例，还是会有问题，因为清空最低位比特进行嵌入的方式将会使相邻两个值一致，嵌入相同比例比特相邻比特依然一样，在直方图中表示为阶梯分布。
下面是针对嵌入文本的改进代码，添加了一个种子秘钥生成嵌入位置秘钥，另外改进了LSB嵌入规则为嵌入比特与最低位比特不同时原比特随机加或者减一。

```python
import random
from PIL import Image
import numpy as np


def text_to_binary(text):
    binary_data = ''.join(format(ord(c), '08b') for c in text)
    return binary_data


def binary_to_text(binary):
    text = ''.join(chr(int(binary[i:i+8], 2)) for i in range(0, len(binary), 8))
    return text


image_path = 'input.png'
output_image_path = 'modified_image.png'
data_to_hide = "han1"


def png_rgb_lsb(image_path, data_to_hide, output_image_path):
    # 读取图片
    image = Image.open(image_path)

    # 将图片转换为RGB格式
    pixels = list(image.getdata())

    # 将数据转换为二进制形式
    binary_data = text_to_binary(data_to_hide)

    if len(binary_data) > len(pixels) * 3:
        raise ValueError("隐藏数据过大，无法完全嵌入到图像中")

    key = [134304, 24906, 1165134, 840434, 1034067, 256626, 960109, 677039, 604987, 1138403, 1252149, 1328829, 693323, 100995, 281079, 808381, 448302, 1262668, 622356, 1360412, 321087, 1424695, 399419, 1260153, 1180374, 1115301, 1420382, 860763, 799633, 764414, 179750, 856208]

    # 嵌入rb两个个通道的最低位
    # 相同不嵌入，不同随机加一或者减一，如果通道值为0加一，通道值为255减1
    index = 0
    for k in key:
        pixel = list(pixels[k])
        if index % 2 == 0:
            # pixel[0] = pixel[0] & 254 | int(binary_data[index])
            if pixel[0] & 1 != int(binary_data[index]):
                if random.randint(0, 1) == 0:
                    if pixel[0] & 1 == 0:
                        pixel[0] = (pixel[0] & 254) | (pixel[0] + 1)
                    else:
                        pixel[0] = (pixel[0] & 254) | (pixel[0] - 1)
                else:
                    if pixel[0] & 255 == 255:
                        pixel[0] = (pixel[0] & 254) | (pixel[0] - 1)
                    else:
                        pixel[0] = (pixel[0] & 254) | (pixel[0] + 1)
            index = index + 1
        else:
            # pixel[2] = pixel[2] & 254 | int(binary_data[index])
            if pixel[2] & 1 != int(binary_data[index]):
                if random.randint(0, 1) == 0:
                    if pixel[2] & 1 == 0:
                        pixel[2] = (pixel[2] & 254) | (pixel[2] + 1)
                    else:
                        pixel[2] = (pixel[2] & 254) | (pixel[2] - 1)
                else:
                    if pixel[2] & 255 == 255:
                        pixel[2] = (pixel[2] & 254) | (pixel[2] - 1)
                    else:
                        pixel[2] = (pixel[2] & 254) | (pixel[2] + 1)
            index = index + 1
        pixels[k] = tuple(pixel)

    new_image = Image.new(image.mode, image.size)
    new_image.putdata(pixels)
    new_image.save(output_image_path)


def png_rgb_ilsb(image_path):
    key = [134304, 24906, 1165134, 840434, 1034067, 256626, 960109, 677039, 604987, 1138403, 1252149, 1328829, 693323,
           100995, 281079, 808381, 448302, 1262668, 622356, 1360412, 321087, 1424695, 399419, 1260153, 1180374, 1115301,
           1420382, 860763, 799633, 764414, 179750, 856208]
    extracted_data = ""
    img = Image.open(image_path)
    pixels = list(img.getdata())

    extracted_binary = ""
    index = 0
    for k in key:
        pixel = pixels[k]
        if index % 2 == 0:
            extracted_binary += str(pixel[0] & 1)
            if len(extracted_binary) % 8 == 0:
                if binary_to_text(extracted_binary[-8:]) == '\x00':
                    break
                extracted_data += binary_to_text(extracted_binary[-8:])
            index = index + 1
        else:
            extracted_binary += str(pixel[2] & 1)
            if len(extracted_binary) % 8 == 0:
                if binary_to_text(extracted_binary[-8:]) == '\x00':
                    break
                extracted_data += binary_to_text(extracted_binary[-8:])
            index = index + 1

    return extracted_data


png_rgb_lsb(image_path, data_to_hide, output_image_path)
data1 = png_rgb_ilsb(output_image_path)
print(data1)

```
