---
title: 无题
date: 2024-01-10
cover: /img/cover/6.jpg
categories:
  - 信息隐藏
tags:
  - 信息隐藏
  - 数字水印
---



# blind watermark概述

blind_watermark是github上的一个图片水印开源项目，获得5.3K的收藏，几乎是github上最受欢迎的图片水印项目。
blind_watermark是不可见盲水印，这意味着向图片添加水印并不会被人察觉，并且提取水印不需要原始图片，只需要嵌入水印后的图片。blind_watermark在频域进行水印嵌入，这一定程度上保证了该水印框架的不可见性和鲁棒性。blind_watermark支持嵌入的水印类型有二进制数据，字符串，图片，支持的载体图片为三通道的任意图片，另外通过理论计算的出blind_watermark的容量为：图片像素值总数/64 （bit）。根据作者给出的示例，blind_watermark在多种攻击上表现出色，包括旋转，裁剪，遮挡，椒盐噪声，亮度改变。

# blind watermark前置知识

blind_watermark使用多种技术，包括DWT（离散小波变换），DCT（离散余弦变换），（SVD）奇异值分解。

### 离散小波变换：DWT

小波变换使用母小波在时间和频率上移动作为一组基来表达原始信号的信息，并将空域信息映射到小波域，小波域不同于时域和频域，它同时保留了两者的分辨率。
如果小波函数表示为：
![alt text](/img/steg_blind_watermark/image.png)
那么小波变换表达为：
![alt text](/img/steg_blind_watermark/image-1.png)
对于二维小波变换，通过行滤波器和列滤波器分离出四个子带分别为：LL,LH,HL,HH
![alt text](/img/steg_blind_watermark/image-2.png)
对于blind_watermark使用的小波变换，矩阵大小被选定为4 * 4的矩阵，小波母函数被选定为haar小波，小波基函数被选定为下面16个haar矩阵：
![alt text](/img/steg_blind_watermark/image-3.png)

### 离散余弦变换DCT：

离散余弦变换来自于离散傅里叶变换（DFT），离散傅里叶变换的公式为：
![alt text](/img/steg_blind_watermark/image-4.png)
对于 8×8 矩阵，下图可表示 64 个基函数。通过DCT变换可以得出奇函数的系数，也可以通过逆变换还原原始矩阵。
![alt text](/img/steg_blind_watermark/image-6.png)

### 奇异值分解：SVD

奇异值分解将矩阵（不仅仅是方阵）分解为三个矩阵：左奇异向量矩阵U，奇异值矩阵，右奇异值矩阵V。
假设A是一个  𝑚×𝑛  的矩阵，那么𝑈是一个 𝑚×𝑚 的矩阵，Σ是一个 𝑚×𝑛 的矩阵，除了主对角线上的元素以外全为0，主对角线上的每个元素都称为奇异值，𝑉是一个 𝑛×𝑛 的矩阵。𝑈和𝑉都是酉矩阵，即满足U^T𝑈=𝐼,V^T𝑉=𝐼。
![alt text](/img/steg_blind_watermark/image-7.png)
通过控制奇异值矩阵奇异值的数量，可以不同程度的还原原始矩阵，这样奇异值分解在可接受的损失范围内压缩矩阵。
![alt text](/img/steg_blind_watermark/image-8.png)

# blind watermark框架

blind_watermark对载体图片添加水印时，将图片分解为YUV三个通道并分别对三个通道都嵌入相同水印；提取水印时，提取三个通道水印取平均后四舍五入作为水印。
![alt text](/img/steg_blind_watermark/image-9.png)
Blind_watermark首先对通道进行二维dwt变换，得到四个子带LL，HL，LH，HH。然后取低频子带LL，大小为通道的1/4。
![alt text](/img/steg_blind_watermark/image-10.png)
设置4*4的窗口函数Win遍历子带LL，将子带分为干块。
![alt text](/img/steg_blind_watermark/image-11.png)
对于每块做DCT变换，得到系数矩阵M。
![alt text](/img/steg_blind_watermark/image-12.png)
使用混淆器shuffler对系数矩阵进行混淆，对混淆后的矩阵做SVD，得到奇异值矩阵Σ，对于Σ矩阵的对角线的第一个系数添加水印：
![alt text](/img/steg_blind_watermark/image-13.png)
另外blind_watermark提供了慢嵌入模式，将会对对角线第二元素进行重复嵌入：
![alt text](/img/steg_blind_watermark/image-14.png)
blind_watermark算法嵌入水印时，通过选定小波变换的LL子带，避开了图像的高频部分，这使得水印的鲁棒性大大增强。另外使用DCT和SVD来聚集子带的重要部分，通过控制修改程度参数d来保持水印的鲁棒性和不可感知性。