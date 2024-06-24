from transformers import PreTrainedModel, PreTrainedTokenizer


class BaseGenerator:
    def __init__(self, model: PreTrainedModel, tokenizer: PreTrainedTokenizer):
        self.model = model
        self.tokenizer = tokenizer

    def generate(self, **kwargs):
        return self.model.generate(**kwargs)
