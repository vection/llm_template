from typing import Union
from .stopping_criteria import JsonStoppingCriteria, ArrayStoppingCriteria, YamlStoppingCriteria
from transformers import StoppingCriteriaList, PreTrainedModel, PreTrainedTokenizer
import torch
import ast
from .json_convertor import loads
from .base_generator import BaseGenerator


class JsonGenerator(BaseGenerator):
    """
    JsonGenerator is a subclass of BaseGenerator designed to generate JSON structures using a pre-trained language model.
    This class takes input text and produces JSON output, adhering to specified stopping criteria to ensure the output
    is in a valid JSON format. It supports both string and list inputs, and can generate outputs based on a provided template.

    Args:
        model (PreTrainedModel): The pre-trained language model to be used for text generation.
        tokenizer (PreTrainedTokenizer): The tokenizer corresponding to the pre-trained language model.
        max_tokens (int, optional): The maximum number of tokens to be generated. Default is 512.
        temperature (float, optional): The temperature for sampling during generation, which controls the randomness of
                                       predictions by scaling the logits before applying softmax. Default is 0.1.

    Attributes:
        max_tokens_generation (int): Stores the maximum number of tokens for generation.
        temperature (float): Stores the temperature value for sampling.
        json_criteria (StoppingCriteriaList): Stopping criteria list for generating JSON structures.
        array_criteria (StoppingCriteriaList): Stopping criteria list for generating JSON arrays.
        device (torch.device): The device to run the model on ('cuda' if GPU is available, else 'cpu').
    """

    def __init__(self, model: PreTrainedModel, tokenizer: PreTrainedTokenizer):
        super().__init__(model, tokenizer)
        self.json_criteria = StoppingCriteriaList([JsonStoppingCriteria(self.tokenizer)])
        self.array_criteria = StoppingCriteriaList([ArrayStoppingCriteria(self.tokenizer)])
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

        if model.device.type == 'cpu':
            model.to(self.device)

    def generate(self, inputs: Union[str, list], template: dict, max_tokens: int = 512,
                 temperature: float = 0.1) -> Union[str, dict]:
        pre_templates = str(template).split("FILL")

        if len(pre_templates) == 0:
            raise Exception("Invalid template format")

        if isinstance(inputs, list):
            text = self.tokenizer.apply_chat_template(inputs, tokenize=False, add_generation_prompt=True)
            inputs = self.tokenizer([text], return_tensors="pt").to(self.device)['input_ids']
        else:
            inputs = self.tokenizer([inputs], return_tensors="pt").to(self.device)['input_ids']

        templates_tokens = self.tokenizer(pre_templates)['input_ids']
        last_template_tokens = torch.tensor(templates_tokens[-1])
        templates_tokens = templates_tokens[:-1]

        final_response = []
        for ind, temp_tokens in enumerate(templates_tokens):
            temp_tokens = torch.tensor(temp_tokens).to(self.device)
            inputs = torch.cat([inputs, temp_tokens.unsqueeze(0)], dim=1)
            temp_instance_type = self.tokenizer.batch_decode(temp_tokens)[-1]
            if '[' in temp_instance_type:
                generated_ids = self.model.generate(
                    inputs=inputs,
                    max_new_tokens=max_tokens,
                    temperature=temperature,
                    eos_token_id=self.tokenizer.eos_token_id,
                    pad_token_id=self.tokenizer.pad_token_id,
                    stopping_criteria=self.array_criteria,
                    use_cache=True,
                )

            else:
                generated_ids = self.model.generate(
                    inputs=inputs,
                    max_new_tokens=max_tokens,
                    temperature=temperature,
                    eos_token_id=self.tokenizer.eos_token_id,
                    pad_token_id=self.tokenizer.pad_token_id,
                    stopping_criteria=self.json_criteria,
                    use_cache=True,
                )
            generated_ids = [output_ids[len(input_ids):] for input_ids, output_ids in
                             zip(inputs, generated_ids)]

            if ind == len(templates_tokens) - 1:
                final_response.extend([temp_tokens.to('cpu'), generated_ids[0].to('cpu')])
            else:
                final_response.extend([temp_tokens.to('cpu'), generated_ids[0][:-1].to('cpu')])

            inputs = torch.cat([inputs, generated_ids[0][:-1].unsqueeze(0)], dim=1)

        final_response_str = \
            self.tokenizer.batch_decode([torch.cat(final_response, dim=0).int()], skip_special_tokens=True)[0]

        try:
            final_response_str = ast.literal_eval(final_response_str)
        except:
            final_temp_response = torch.cat([torch.cat(final_response, dim=0), last_template_tokens], dim=0)
            final_response_temp = self.tokenizer.batch_decode([final_temp_response.int()], skip_special_tokens=True)[0]

            try:
                final_response_temp = ast.literal_eval(final_response_temp)
                return final_response_temp
            except:
                final_response_str += '}'
                for _ in range(2):
                    try:
                        final_response_str = ast.literal_eval(final_response_str)
                        break
                    except SyntaxError as e:
                        if "was never closed" in e.__str__():
                            final_response_str += '}'

                    finally:
                        if isinstance(final_response_str, str):
                            return loads(final_response_str)

        return final_response_str
