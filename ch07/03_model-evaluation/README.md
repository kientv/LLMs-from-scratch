# Chapter 7: Finetuning to Follow Instructions

This folder contains utility code that can be used for model evaluation.



&nbsp;
## Evaluating Instruction Responses Using the OpenAI API


 # Chương 7: Finetuning để theo dõi hướng dẫn
 
 Thư mục này chứa mã tiện ích có thể dùng để đánh giá mô hình.
 
 &nbsp;
 ## Đánh giá phản hồi hướng dẫn bằng API OpenAI
 
 - Notebook [llm-instruction-eval-openai.ipynb](llm-instruction-eval-openai.ipynb) sử dụng GPT-4 của OpenAI để đánh giá các phản hồi do mô hình finetune theo hướng dẫn tạo ra. Nó làm việc với một file JSON có định dạng như sau:
 
 ```python
 {
     "instruction": "What is the atomic number of helium?",
     "input": "",
     "output": "The atomic number of helium is 2.",               # <-- Mục tiêu trong bộ kiểm tra
     "model 1 response": "\\nThe atomic number of helium is 2.0.", # <-- Phản hồi từ 1 mô hình LLM
     "model 2 response": "\\nThe atomic number of helium is 3."    # <-- Phản hồi từ mô hình LLM thứ 2
 },
 ```
 
 &nbsp;
 ## Đánh giá phản hồi hướng dẫn cục bộ bằng Ollama
 
 - Notebook [llm-instruction-eval-ollama.ipynb](llm-instruction-eval-ollama.ipynb) là một lựa chọn thay thế, sử dụng mô hình Llama 3 tải về cục bộ thông qua Ollama.

&nbsp;
## Evaluating Instruction Responses Locally Using Ollama

- The [llm-instruction-eval-ollama.ipynb](llm-instruction-eval-ollama.ipynb) notebook offers an alternative to the one above, utilizing a locally downloaded Llama 3 model via Ollama.