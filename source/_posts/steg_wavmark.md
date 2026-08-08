---
title: WavMark:Watermarking for Audio Generation
date: 2024-01-10
categories:
  - 信息隐藏
tags:
  - 信息隐藏
---



# WavMark: Watermarking for Audio Generation


## WavMark简介

WavMark是一种创新的音频水印框架，可以在仅仅1秒的音频片段内编码多达32位的水印。该水印对人类的感官来说是难以察觉的，并且对各种攻击表现出很强的鲁棒性。它可以作为合成声音的有效标识符，在音频版权保护方面具有更广泛的应用潜力。Wavmark迭代的将相同水印嵌入到宿主音频的一秒片段中，确保全时段的保护。即使音频被剪切，也可以使用任何完整的片段进行解码。因此，该框架具有高度的灵活性，允许多个水印段的组合，以实现更高的鲁棒性和扩展的容量。利用10到20秒的音频作为载体，WavMark在10种常见攻击中平均误码率（BER）为0.48%，并且维持了优秀的不可感知性（SNR=36.85，PESQ=4.21）。
![alt text](/img/steg_wavmark/image.png)

## WavMark框架

![alt text](/img/steg_wavmark/image-1.png)

### 音频表示

WavMark使用采样率为16kHZ的单通道音频作为载体，编码单位长度（EUL）设置为一秒。因此原始输入被表示为长度为16000的一位波形向量记为：x_wave，进一步使用短时傅里叶变换（STFT）将其转换为频谱图：
![alt text](/img/steg_wavmark/image-2.png)

### 水印表示

水印消息由长度为K的随机二进制向量表示，为m_vec，使用线性层将其展开为与波形输入大小相同的向量，然后使用相同的STFT过程获得与x_spec大小相同的特征映射：
![alt text](/img/steg_wavmark/image-3.png)

### 可逆神经网络

可逆网络是由n层可逆块堆叠而成的。每个块的输入和输出维度保持不变，编码和解码过程使用相同的参数。在编码过程中，以x_l和m_l表示第l块的输入，网络的输出x_(l+1)和m_(l+1)可以描述为:
![alt text](/img/steg_wavmark/image-4.png)
（其中σ表示sigmoid激活函数，⊙表示逐元乘法。函数φ(·)，η(·)和ρ(·)可以是任意函数）
对于最后一个可逆块的输出，丢弃消息分支的输出m_spec^n，仅利用音频分支的输出 x_spec^n。随后，我们对x_spec^n进行反短时傅里叶变换(ISTFT)重建水印音频波形:![alt text](/img/steg_wavmark/image-5.png)
在解码过程中，由于只有带水印的音频，从正态分布中采样一个变量z作为消息分支的输入。反方向第l+1块的计算过程可以表示如下:
![alt text](/img/steg_wavmark/image-6.png)
将消息分支输出的谱图表示为m_spec。执行ISTFT变换后，我们得到频域输出。然后，将其通过一个线性层，我们就可以恢复消息信息:
![alt text](/img/steg_wavmark/image-7.png)