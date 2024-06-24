from src.llm_parser import JsonGenerator
from transformers import AutoModelForCausalLM, AutoTokenizer

if __name__ == '__main__':

    mymodel = AutoModelForCausalLM.from_pretrained('Qwen/Qwen2-1.5B-Instruct')
    tokenizer = AutoTokenizer.from_pretrained('Qwen/Qwen2-1.5B-Instruct')
    myclass = JsonGenerator(model=mymodel, tokenizer=tokenizer)

    text = """<|im_start|>system\nExamine the email structure to identify the details of the shipper involved in the shipment. Extract the business name and address details of the shipper.\nOutput JSON Format: {'shipper': {'company_name': '','address_details': {'country_name': '','city': '','postal_code': '','address_name': ''},'contacts' : [{'given_name': '', 'last_name': '', 'email': ''}]}}\n<|im_end|>\n<|im_start|>user\nEmail:\nSender: Emma.Pessato@momart.co.uk\nReceiver: marina.takagi@dietl.com\nSubject: E57182 - Import one crate and delivery to Delaware Freeport\nBody: Hi Marina,\nCan you please send us your charges for the following import?\nDelivery to:\nMr Gabriel Rouadi\nc/o Delaware Freeport\n111 Alan Dr\nNEWARK DE 19711-8097\nCrate: 313 x 20 x 161 cm LDH\nWork:\nRafa Macarrn, Sin ttulo (Los lirios del campo y las aves del cielo), 2016, acrylic on aluminium\n295 x 5 x 143 cm, 50 kg\n52,400.00\nThanks,\nEmma\nSignature: Emma Pessato\nGallery Services Estimator | Momart Ltd\nT. +44 (0)20 7426 3000\nD. +44 (0)20 7426 3119\nE.  emma.pessato@momart.co.uk<mailto:%20emma.pessato@momart.co.uk>\nExchange Tower, 9th Floor\n1 Harbour Exchange Square\nLondon E14 9GE\nFollow: twitter.com/MomartLtd<https://protect-eu.mimecast.com/s/bfU5CRLAjTyYvmsPF5oB?domain=twitter.com>\nLike: facebook.com/MomartLtd<https://protect-eu.mimecast.com/s/BWlqCW8JoFN359Im_CGe?domain=facebook.com>\nwww.momart.co.uk<https://protect-eu.mimecast.com/s/DCRnCYMLqFjYL1i3YtXf?domain=momart.co.uk><|im_end|>\n"""
    schema = {'shipper': {'company_name': 'FILL',
                  'address_details': {'country_name': 'FILL',
                   'city': 'FILL',
                   'postal_code': 'FILL',
                   'address_name': 'FILL'},
                   'contacts' : [{'given_name': 'FILL', 'last_name': 'FILL', 'email': 'FILL'}]}}


    ### {'freight_forwarder': {'business_party': '', 'address_details': {'country_name': '', 'country_code' : '', 'state_name' : '', 'state_code' : '', 'country_name': '', 'city': '', 'postal_code': '', 'address_name' : ''}, 'contacts': [{'given_name': '', 'last_name': '', 'email': '', 'phone': '', 'phone2': '', 'title': ''}]}}
    result = myclass.generate(text, schema)
    print(result)
    print(type(result))
