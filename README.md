## 📝 Generation By Template
🎛️ Control your in-house LLM outputs by producing structured JSON outputs.

**llm_template** enables the generation of robust JSON outputs from any instruction model. It can also create intricate schemas, working faster and more accurately than standard generation functions in most scenarios. This is achieved by injecting schema tokens into the response, compelling the LLM to generate only the values.

### 🛠️ Installation
To install llm_template, use pip:

```
pip install llm_template
```

Generation example of simple JSON:

Desired json output:
```
{'sender' : {'email': '', 'full_name': '', 'phone': ''}, 
'item': [{'item_description': '', 'quantity': '', 'measurments' : '', 'material' : ''}, ...], 
'notes': ''}
```

Following usage example:  
```
mymodel = AutoModelForCausalLM.from_pretrained('meta-llama/Meta-Llama-3-8B-Instruct',torch_dtype=torch.bfloat16,
    device_map="auto")
tokenizer = AutoTokenizer.from_pretrained('meta-llama/Meta-Llama-3-8B-Instruct')
tokenizer.pad_token_id = tokenizer.eos_token_id

prompt = """By given email that has been sent to business, we need to extract the information about the sender and also what he asks for.
Customer can ask for bids on the business items.
The final output need to be in this JSON format:
{'sender' : {'email': '', 'full_name': '', 'phone': ''}, 'item': [{'item_description': '', 'quantity': '', 'measurments' : '', 'material' : ''}], 'notes': ''}

Sender Email: sales@customfurnitureco.com
Target Email: client@example.com
Subject: Bid Proposal for Custom Office Furniture

**Email Content:

Dear John Doe,

Thank you for your patience. We have prepared a detailed bid proposal for the custom office furniture requested by XYZ Corp.

Bid Proposal:

Executive Office Desks (10 units)

Material: Solid wood with a walnut veneer finish
Dimensions: 60" W x 30" D x 30" H
Features: Built-in cable management, lockable drawers
Price per unit: $1,200
Total price: $12,000
Ergonomic Office Chairs (20 units)

Material: Mesh back with leather seat
Features: Adjustable height, lumbar support, tilt mechanism
Price per unit: $300
Total price: $6,000
Conference Tables (5 units)

Material: Tempered glass with metal frame
Dimensions: 96" L x 48" W x 30" H
Features: Integrated power outlets, cable management
Price per unit: $2,500
Total price: $12,500
Grand Total: $30,500

Production Time: 6-8 weeks from the date of order confirmation.

Payment Terms: 50% deposit upon order confirmation, balance upon delivery.

We are confident that our high-quality materials and modern design aesthetic will meet your needs. Please review the proposal and let us know if you have any questions or require any adjustments.

Thank you for considering Custom Furniture Co. We look forward to the possibility of working with XYZ Corp.

Best regards,
Jane Smith
Sales Manager, Custom Furniture Co.
sales@customfurnitureco.com"""

generator = JsonGenerator(model=mymodel, tokenizer=tokenizer)

schema = {'sender' : {'email': 'FILL', 'full_name': 'FILL', 'phone': 'FILL', 'location': 'FILL'}, 'items': [{'FILL'}], 'notes': 'FILL'}

result = generator.generate(text, schema,temperature=0.1)


{'sender': {'email': 'sales@customfurnitureco.com',
  'full_name': 'Jane Smith',
  'phone': '555-123-4567',
  'location': 'New York'},
 'items': [{'item_description': 'Executive Office Desks',
   'quantity': '10 units',
   'measurments': '60" W x 30" D x 30" H',
   'material': 'Solid wood with a walnut veneer finish'},
  {'item_description': 'Ergonomic Office Chairs',
   'quantity': '20 units',
   'measurments': '',
   'material': 'Mesh back with leather seat'},
  {'item_description': 'Conference Tables',
   'quantity': '5 units',
   'measurments': '96" L x 48" W x 30" H',
   'material': 'Tempered glass with metal frame'}],
 'notes': 'Please review the proposal and let us know if you have any questions or require any adjustments.'}
```

## Creating the Schema

When creating a schema for your JSON generation, follow these steps:

1. **Identify Keys and Structure:** Determine the keys (fields) and their structure that you want in your generated output.
2. **Define Placeholder Values:** Use placeholder values like `"FILL"` for keys whose values will be filled during generation.
3. **Example Schema:**
   ```json
   {
     "sender": {
       "email": "FILL",
       "full_name": "FILL",
       "phone": "FILL",
       "location": "FILL"
     },
     "items": [
       {"FILL"}
     ],
     "notes": "FILL"
   }
   
## Best Practices
* When generating a list of dictionaries, specify the desired structure in the prompt and use [{'FILL'}] in the schema.
* For simple JSON responses, you don't need to specify the JSON output in the prompt unless you want to generate a list of dictionaries.
* Crafting a well-defined prompt significantly impacts the quality of the generated output. Clearly specifying the output format within the prompt can lead to more accurate results.
* For more advanced generation, you can incorporate logic rules to control specific values. This can involve filtering or sampling from a predefined list of tokens or analyzing logits score distances to identify other candidate tokens for possible answers..


## Future Features
* Enable to add custom logic to generation step
* Add speculative decoding support


# 📄 Technical Report
## 💡 Motivation
Many Language Models (LLMs) struggle to ensure output in valid JSON format, prompting various proposed solutions. While many of these solutions involve prompt engineering techniques, they often require explicit specification within the prompt of the expected JSON format, with no guarantee of successful generation.

These techniques frequently yield inconsistent outputs, occasionally resulting in incorrect JSON formatting, difficulty in filtering, inclusion of undesired keys, and mismatched schema. Moreover, they endure lengthy generation periods due to the necessity of strictly adhering to a predefined format, often involving repetitive characters.

Furthermore, the substantial number of tokens representing the desired JSON structure contributes to the overall context length, consequently impacting generation time.

Alternatively, more convenient methods like jsonFormer offer a solution by specifying the desired JSON template as a schema, generating each key value according to pre-defined types. Although this technique still employs prompts to obtain the JSON format, it essentially acts as a wrapper around the working prompt, striving to adjust and return the final output as valid JSON.

Another approach involves fine-tuning to achieve JSON output, which, while functional, introduces its own set of challenges and demands additional effort.

Addressing these challenges demands more sophisticated approaches to enhance resilience in production environments.
Imagine if we could govern the generation process and instruct the LLM to exclusively produce the desired tokens.

## 🚀 The Solution

The proposed methodology involves the creation of predefined JSON-based templates and the management of the generation process through the segmentation of templates into discrete entities (keys). Each key is associated with the generation of its corresponding value utilizing Language Model-based methods, adhering to appropriate stopping criteria. 

For standard JSON formatting, stop tokens such as "}" or "," are utilized, while array generation employs "]" to denote the conclusion criteria.

This approach is distinctly template-centric, prioritizing the generation of essential tokens while minimizing extraneous procedural steps.

Let us define desirable JSON output:

`{
"delivery_address": {
"country_name": "United States",
"country_code": "US",
"state_name": "California",
"state_code": "CA",
"city": "Los Angeles",
"postal_code": "90028",
"address_name": "123456 Hollywood Blvd, Los Angeles, CA"
}
}`

We can transform this JSON to more general template:

`{
"delivery_address": {
"country_name": "FILL",
"country_code": "FILL",
"state_name": "FILL",
"state_code": "FILL",
"city": "FILL",
"postal_code": "FILL",
"address_name": "FILL"
}
}`

For the generation process, we initiate with the model, finalized prompt, and template.

Next, the template is segmented into sequences of tokens based on the "FILL" value. These tokens are then tokenized, with the last token removed as it does not contribute to the generation process.

Subsequently, we traverse through the list of sequences, appending them to the prompt tokens, and commence generation from this point. This iterative process continues until all sequences are processed.

The stopping criteria are bifurcated into two categories:

### Regular generation: where the output adheres to a standard JSON format.
### Array generation: where the output consists of arrays.

This distinction is determined by detecting an array indicator character within the current sequence.

Upon completion of the generation process, the previously removed last token is appended, and the resulting output is converted into JSON format. To ensure reliability, several safety checks are incorporated at the conclusion, including the addition of '}' characters and attempts at re-conversion if the initial conversion fails.

This methodology affords flexibility for the integration of additional logic steps into the generation process, enhancing results tailored to specific use cases. For instance, during value generation, analysis of the first token logits enables the identification of top-K candidates, potentially leading to the provision of multiple plausible answers. Furthermore, employing distinct models for different value generation tasks, adjusting parameters such as temperature and top-p based on entity, are among the adaptable strategies facilitated by this approach.

Moreover, seamless integration with speculative decoding further optimizes the process.

By exploring this approach, we aim to alleviate the requirement of explicitly specifying the desired JSON output format to the Language Model (LLM), thereby reducing context length. This investigation encompasses an assessment of its impact on accuracy and inference generation time.

To maximize results the correlation between the template format and output format need to be the same. For example, if stated in the prompt desired JSON output, the JSON template need to be the same. This will ensure the correct values will be filled in the correct keys.

### 🧪 Experiments
Tested the solution on a private dataset containing emails with annotated information extraction entities. The first set includes 438 samples, while the fine tuned version tested on approximately 2400 samples.

| Model                                         | Generation Time Avg (sec) | Accuracy | Method  | Total Generated | Total JSON parsing errors |
|-----------------------------------------------|---------------------------|----------|---------|-----------------|---------------------------|
| LLama-3-7B-instruct                           | 3.08                      | 38.14%   | Template| 4356            | 0                         |
| LLama-3-7B-instruct                           | 4.99                      | 29.17%   | Generate| 3527            | 42                        |
| Qwen-2-1.5B-instruct                          | 3.25                      | 33.42%   | Template| 3833            | 0                         |
| Qwen-2-1.5B-instruct                          | 2.5                       | 24.85%   | Generate| 3375            | 39                        |
| LLama-3-7B-instruct (FineTuned)| 10.07                     | 60.3%    | Template| 15898           | 0                         |
| LLama-3-7B-instruct (FineTuned)| 17.06                     | 52.55%   | Generate| 13691           | 0                         |

**Accuracy rate is calculated by fuzzy similarity score for each entity between each generated value compared to Ground Truth value if provided. Then for each entity calculated a score and then averaging on all entities.**

