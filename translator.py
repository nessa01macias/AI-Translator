from transformers import pipeline

def translate(text):

    # Translate the tokenized text
    pipe = pipeline(
        "translation", model="Helsinki-NLP/opus-mt-en-fi",
        # not including the tensor representation in the output
        return_tensors=False, 
        # setting up the output to be already decoded text 
        return_text=True,
        # cleaning up extra spaces in the output text
        clean_up_tokenization_spaces=True,
    )

    translated_text= pipe(text)

    print(f"1. translated_text: {translated_text}")
    return translated_text[0]["translation_text"]

if __name__ == '__main__':
    response = translate("Hello!")
    print(f"2. This is the response in main: {response}")
