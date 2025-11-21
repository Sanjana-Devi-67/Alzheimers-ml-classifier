from transformers import MarianMTModel, MarianTokenizer

# Cache loaded models so we don’t reload every call
_loaded_models = {}

def get_model(src_lang, tgt_lang):
    pair = f"{src_lang}-{tgt_lang}"
    if pair not in _loaded_models:
        model_name = f"Helsinki-NLP/opus-mt-{pair}"
        tokenizer = MarianTokenizer.from_pretrained(model_name)
        model = MarianMTModel.from_pretrained(model_name)
        _loaded_models[pair] = (tokenizer, model)
    return _loaded_models[pair]

def translate_text(text, src_lang="en", tgt_lang="hi"):
    try:
        tokenizer, model = get_model(src_lang, tgt_lang)
        inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
        translated = model.generate(**inputs)
        return tokenizer.decode(translated[0], skip_special_tokens=True)
    except Exception as e:
        return f"[Translation error: {e}]"
