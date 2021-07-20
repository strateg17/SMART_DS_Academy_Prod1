from googletrans import Translator
import en_core_web_sm
import torch
from transformers import BertForSequenceClassification, AdamW, BertConfig, BertForPreTraining, BertTokenizer
import torch.nn.functional as F


def f_pos(text):
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    weights = torch.load('pytorch_model.bin', map_location=torch.device('cpu'))
    config = BertConfig.from_json_file('config.json')
    model = BertForSequenceClassification(config)
    model.load_state_dict(weights)
    tokenizer = BertTokenizer.from_pretrained('neuralmind/bert-base-portuguese-cased')
    text=tokenizer.tokenize(text)
    text_1 = tokenizer.convert_tokens_to_ids(text)
    tokens_tensor = torch.tensor([text_1]).to(device).long()
    logits = model(tokens_tensor)
    res = F.softmax(logits[0], dim=1)
    score = res[0][1].item()
    if score < 0.45:
        return "negative"
    elif score > 0.66:
        return "positive"
    elif 0.45 <= score <= 0.66:
        return "neutral"
    # return res[0][1].item()
    #Tinha urgência em receber o produto para dar o presente no dia dos pais, mas não chegou no prazo e não tem nada dizendo o porque da falha na entrega do produto.
    # res = F.softmax(logits[0], dim=1)
    # return res[0][1].item()


def f_price(text):
    translator = Translator()
    translation = translator.translate(text, src='pt')
    nlp_en = en_core_web_sm.load()
    doc = nlp_en(translation.text)
    for i in doc.ents:
        if (i.label_ == 'MONEY'):
            return ''.join(list(filter(str.isdigit, i.text)))
    return "None price found"


