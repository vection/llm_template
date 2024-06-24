import torch
from transformers import StoppingCriteria, PreTrainedTokenizer


class JsonStoppingCriteria(StoppingCriteria):
    stop_tokens = {"',", "'}", "}", "}}", "'}}", "']", "\"}", "\",", "'},", ".',"}

    def __init__(self, tokenizer: PreTrainedTokenizer):
        super().__init__()
        stop_tokens = set()
        for stop in list(self.stop_tokens):
            token_ids = tokenizer.encode(stop, add_special_tokens=False)
            if token_ids:
                stop_tokens.update(token_ids)

        self.stop_tokens = stop_tokens
        self.tokenizer = tokenizer

    def __call__(self, input_ids: torch.LongTensor, scores: torch.FloatTensor, **kwargs) -> bool:
        last_token = input_ids.flatten()[-1].item()
        if last_token in self.stop_tokens:
            return True
        return False


class ArrayStoppingCriteria(StoppingCriteria):
    stop_tokens = {"]", "']", "\"]", "}]"}

    def __init__(self, tokenizer: PreTrainedTokenizer):
        super().__init__()
        stop_tokens = set()
        for stop in list(self.stop_tokens):
            token_ids = tokenizer.encode(stop, add_special_tokens=False)
            if token_ids:
                stop_tokens.update(token_ids)

        self.stop_tokens = stop_tokens
        self.tokenizer = tokenizer

    def __call__(self, input_ids: torch.LongTensor, scores: torch.FloatTensor, **kwargs) -> bool:
        last_token = input_ids.flatten()[-1].item()
        if last_token in self.stop_tokens:
            return True
        return False


class YamlStoppingCriteria(StoppingCriteria):
    stop_tokens = {"\"\n", "'\n", "\"", "\"\n", ")\n", "]\n", ".\n", "\n"}

    def __init__(self, tokenizer: PreTrainedTokenizer):
        super().__init__()
        stop_tokens = set()
        for stop in list(self.stop_tokens):
            token_ids = tokenizer.encode(stop, add_special_tokens=False)
            if token_ids:
                stop_tokens.update(token_ids)

        self.stop_tokens = stop_tokens

    def __call__(self, input_ids: torch.LongTensor, scores: torch.FloatTensor, **kwargs) -> bool:
        last_token = input_ids.flatten()[-1].item()

        if last_token in self.stop_tokens:
            return True
        return False
