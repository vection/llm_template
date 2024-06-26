from llm_template import JsonGenerator
from transformers import AutoModelForCausalLM, AutoTokenizer

model_id = "Qwen/Qwen2-1.5B-Instruct"
if __name__ == '__main__':
    mymodel = AutoModelForCausalLM.from_pretrained(model_id)
    tokenizer = AutoTokenizer.from_pretrained(model_id)

    prompt = """By given email that has been sent to business, we need to extract the information about the sender and also what he asks for.
    Customer can ask for bids on the business items.
    The final output need to be in this JSON format:
    {'sender' : {'email': '', 'full_name': '', 'phone': ''}, 'items': [{'item_description': '', 'quantity': '', 'measurments' : '', 'material' : ''}, ...], 'notes': ''}

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

    schema = {'sender': {'email': 'FILL', 'full_name': 'FILL', 'phone': 'FILL', 'location': 'FILL'},
              'items': [{'FILL'}], 'notes': 'FILL'}

    result = generator.generate(prompt, schema, temperature=0.1)