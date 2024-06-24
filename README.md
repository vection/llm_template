# Generation By Template

**Motivation**

Many Language Models (LLMs) struggle to ensure output in valid JSON format, prompting various proposed solutions. While many of these solutions involve prompt engineering techniques, they often require explicit specification within the prompt of the expected JSON format, with no guarantee of successful generation.

These techniques frequently yield inconsistent outputs, occasionally resulting in incorrect JSON formatting, difficulty in filtering, inclusion of undesired keys, and mismatched schema. Moreover, they endure lengthy generation periods due to the necessity of strictly adhering to a predefined format, often involving repetitive characters.

Furthermore, the substantial number of tokens representing the desired JSON structure contributes to the overall context length, consequently impacting generation time.

Alternatively, more convenient methods like jsonFormer offer a solution by specifying the desired JSON template as a schema, generating each key value according to pre-defined types. Although this technique still employs prompts to obtain the JSON format, it essentially acts as a wrapper around the working prompt, striving to adjust and return the final output as valid JSON.

Another approach involves fine-tuning to achieve JSON output, which, while functional, introduces its own set of challenges and demands additional effort.

For example in LLama3 most of the outputs given not valid JSON format:

 
`Here is the extracted information in the requested JSON format:\n\n```\n{\n  "shipper": {\n    "business_party": "The Heller Group",\n    "address_details": {\n      "address_name": "745 Fifth Avenue, 4th Floor",\n      "country_name": "USA",\n      "city": "New York",\n      "postal_code": "10151"\n    },\n    "contacts": [\n      {\n        "given_name": "Anna",\n        "last_name": "Hafner",\n        "email": "anna@hellergroupllc.com",\n        "phone": "",\n        "phone2": "",\n        "title": ""\n      }\n    ]\n  }\n}\n````

Another example of output:
`The pickup address specified for picking up the goods is:\n\n* Name: David Kordansky Gallery\n* City: New York\n* State: NY\n* Postal Code: 10011\n* Country: United States\n\nHere is the output in JSON format:\n\n{\n"pickup_address": {\n"address_name": "David Kordansky Gallery",\n"city": "New York",\n"state_code": "NY",\n"state_name": "New York",\n"postal_code": "10011",\n"country_name": "United States",\n"country_code": "US"\n}`

This represents the most convenient output, but it is clear that it is not in a valid JSON format, necessitating additional post-processing and filtering.

Due to this, it is common for Language Models (LLMs) to introduce extra keys, modify their names, or even produce invalid JSON output.

Addressing these challenges demands more sophisticated approaches to enhance resilience in production environments.

Imagine if we could govern the generation process and instruct the LLM to exclusively produce the desired tokens.

### The Method 

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
"address_name": "6834 Hollywood Blvd, Los Angeles, CA"
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

Regular generation: where the output adheres to a standard JSON format.
Array generation: where the output consists of arrays.

This distinction is determined by detecting an array indicator character within the current sequence.

Upon completion of the generation process, the previously removed last token is appended, and the resulting output is converted into JSON format. To ensure reliability, several safety checks are incorporated at the conclusion, including the addition of '}' characters and attempts at re-conversion if the initial conversion fails.

This methodology affords flexibility for the integration of additional logic steps into the generation process, enhancing results tailored to specific use cases. For instance, during value generation, analysis of the first token logits enables the identification of top-K candidates, potentially leading to the provision of multiple plausible answers. Furthermore, employing distinct models for different value generation tasks, adjusting parameters such as temperature and top-p based on entity, are among the adaptable strategies facilitated by this approach.

Moreover, seamless integration with speculative decoding further optimizes the process.

By exploring this approach, we aim to alleviate the requirement of explicitly specifying the desired JSON output format to the Language Model (LLM), thereby reducing context length. This investigation encompasses an assessment of its impact on accuracy and inference generation time.

To maximize results the correlation between the template format and output format need to be the same. For example, if stated in the prompt desired JSON output, the JSON template need to be the same. This will ensure the correct values will be filled in the correct keys.

### Experiments

Dataset: 438 samples of Extraction of entities from email such as Shipper, Consignee, Freight components and so on

4 Variations were tested:

Fine-Tuned With Output: This indicates that the prompt was provided for a fine-tuned version specific to a sub-domain, including specifications for the output JSON format.

Fine-Tuned Without Output: This indicates that the prompt was provided for a fine-tuned version specific to a sub-domain, but without specifications for the output JSON format.

Pretrained With Output: This indicates that the prompt was provided for the basic pretrained version, including specifications for the output JSON format.

Pretrained Without Output: This indicates that the prompt was provided for the basic pretrained version, but without specifications for the output JSON format.

**LLama3-8B-Instruct Fine Tuned Template With Output:** 

Total generated values: 

Template Generation: 4271 

Response Generation: 3823 

Total True values:

Template Generation: 1701

Response Generation: 1460

Total of Not JSON:

Template Generation: 0

Response Generation: 0

Generation Time:

Template Generation: 

![finetuned_with_output_template_generate_time_plot.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/c261e6b6-cd2a-412a-8df3-d68b0a77792e/a98eb8d0-9ce1-4687-b0cc-ad422c2f25b3/finetuned_with_output_template_generate_time_plot.png)

Regular Generation:

![finetuned_with_output_generate_time_plot.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/c261e6b6-cd2a-412a-8df3-d68b0a77792e/c78d1968-835b-480a-a6f6-3868dc97d6cf/finetuned_with_output_generate_time_plot.png)

**LLama3-8B-Instruct Fine Tuned Template Without Output:** 

Total generated values: 

Template Generation: 4268

Response Generation: 3899

Total True values:

Template Generation: 1687

Response Generation: 1460

Total of Not JSON:

Template Generation: 0

Response Generation: 0

Generation Time:

Template Generation:

![finetuned_without_output_template_generate_time_plot.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/c261e6b6-cd2a-412a-8df3-d68b0a77792e/38d236fd-6854-4421-9df3-d3bb9789d739/finetuned_without_output_template_generate_time_plot.png)

Regular Generation:

![finetuned_without_output_generate_time_plot.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/c261e6b6-cd2a-412a-8df3-d68b0a77792e/4ce2683c-c16c-425e-8d4a-e24a940c125b/finetuned_without_output_generate_time_plot.png)

**LLama3-8B-Instruct Pre-trained Template Without Output:** 

Total generated values: 

Template Generation: 4372

Response Generation: 3524

Total True values:

Template Generation: 924

Response Generation: 723

Total of Not JSON:

Template Generation: 0

Response Generation: 42 (after intense post-processing)

Generation Time:

Template Generation:

![pretrained_without_output_template_generate_time_plot.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/c261e6b6-cd2a-412a-8df3-d68b0a77792e/886e44fd-f3f8-4a68-9bae-b59b9ec2deb5/pretrained_without_output_template_generate_time_plot.png)

Response Generation:

![pretrained_without_output_generate_time_plot.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/c261e6b6-cd2a-412a-8df3-d68b0a77792e/f04afa05-0581-4a5c-b750-d44623b1ddb5/pretrained_without_output_generate_time_plot.png)

**LLama3-8B-Instruct Pre-trained Template With Output:** 

Total generated values: 

Template Generation: 4356

Response Generation: 3527

Total True values:

Template Generation: 1016

Response Generation: 729

Total of Not JSON:

Template Generation: 0

Response Generation: 42 (after intense post-processing)

Generation Time:

Template Generation:

![pretrained_with_output_template_generate_time_plot.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/c261e6b6-cd2a-412a-8df3-d68b0a77792e/651edd9d-1991-4cdf-bdb7-66d30b0f0391/pretrained_with_output_template_generate_time_plot.png)

Response Generation:

![pretrained_with_output_generate_time_plot.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/c261e6b6-cd2a-412a-8df3-d68b0a77792e/61d6640f-b080-4c28-9e8d-807fb10204b2/pretrained_with_output_generate_time_plot.png)
