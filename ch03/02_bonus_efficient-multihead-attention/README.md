# Triển khai Multi-Head Attention hiệu quả hơn

- [mha-implementations.ipynb](mha-implementations.ipynb) chứa và so sánh các cách triển khai multi-head attention khác nhau



### Tóm tắt

Các hình dưới đây tóm tắt điểm benchmark hiệu năng (giá trị nhỏ hơn là tốt hơn).


&nbsp;
#### Chỉ forward pass

<a href="mha-implementations.ipynb"><img src="https://sebastianraschka.com/images/LLMs-from-scratch-images/bonus/mha-benchmark/1_forward-only.webp?1" width="500px"></a>

&nbsp;
#### Forward và backward pass

<a href="mha-implementations.ipynb"><img src="https://sebastianraschka.com/images/LLMs-from-scratch-images/bonus/mha-benchmark/2_forward-and-backward.webp?1" width="500px"></a>

&nbsp;
#### Forward và backward sau khi biên dịch

<a href="mha-implementations.ipynb"><img src="https://sebastianraschka.com/images/LLMs-from-scratch-images/bonus/mha-benchmark/3_forward-and-backward-compiled.webp?1" width="500px"></a>

