"""
Методы отвечающие за работу с ИИ
"""
from sklearn.metrics.pairwise import cosine_similarity
from transformers import AutoTokenizer, AutoModelForCausalLM
from sentence_transformers import SentenceTransformer
from peft import PeftModel
import torch
import numpy as np
import time

BASE_MODEL_PATH = "/mistral-7b"
QLORA_ADAPTER_PATH = "/mistral-qlora"

# Загружаем токенизатор (из базовой модели)
tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL_PATH)

# Загружаем базовую модель
base_model = AutoModelForCausalLM.from_pretrained(
    BASE_MODEL_PATH,
    device_map="auto",
    torch_dtype=torch.float16
)

# Загружаем QLoRA адаптер
model = PeftModel.from_pretrained(
    base_model,
    QLORA_ADAPTER_PATH,
    device_map="cuda"
)

sentence_model = SentenceTransformer("ai-forever/sbert_large_nlu_ru")

dataset_embeddings = np.load("/embeddings/embeddings.npy")


def process(message: dict) -> str:
    """
    Функция запускающая обработку запроса от ИИ помощника
    :return: ответ от нейросети
    """

    text = message["chat"][-1]["text"]

    # Проверка эмбеддинга
    text_embeddings = sentence_model.encode(text)
    scores = cosine_similarity([text_embeddings], dataset_embeddings)[0]
    
    if max(scores) < 0.80:
        return "Я не могу ответить на этот вопрос, так как он не является частью моей сферы деятельности. Сорян :(" 
	    
    prompt = f"<s>[INST] {text} [/INST]"
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    
    with torch.no_grad():
        outputs = model.generate(**inputs, max_new_tokens=128)
        decoded = tokenizer.decode(outputs[0], skip_special_tokens=False)
        return decoded.replace(prompt.strip(), "").strip().replace("</s>", "").replace("<s>", "")
