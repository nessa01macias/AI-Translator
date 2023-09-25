#  Metropolia-Wide AI Translator

Metropolia-Wide AI Translator is a user-friendly web application designed to simplify translation tasks between Finnish and English languages. Whether you need to translate texts, or phrases, this app has got you covered.

## How to use it?
Please refer to the section "webpage images" below to get an overview of how the app looks like for now. It is also possible to fork the repostory, and then run the following to get the webpage running locally:
```
pip install -r requirements.txt
python3 run.py
```

The deployment is now in progress, the URL is http://3.84.155.114/home. 
NOTE: Please take into consideration that the deployment is in progress, therefore some routes might not work yet. Also, the instance may be shut down to avoid costs so it would be not accessible at all.
However, it is currently deployed on a EC2 Linux Server.

## Key Features 
### Without an account

- Seamless Translation: Translate text effortlessly between Finnish and English, and vice versa. The app leverages state-of-the-art language models to provide accurate and reliable translations.
- No Login Required: You can start using the translation service without the need for registration or login. It's quick and convenient for one-time translations.


### With an account
- Seamless translation: Enjoy the same seamless translation capabilities as without an account.
- Translation history: Keep track of your translation history. Easily refer back to previous translations, making it handy for recurring tasks.


## Who can use it?

Whether you're a student, professional, or language enthusiast, Metropolia-Wide AI Translator simplifies language translation tasks. Try it out today, and experience the convenience of accurate and efficient translations.

Note: This app is powered by advanced language models, ensuring high-quality translations. It's a handy tool for anyone dealing with Finnish and English languages.

## Acknowledgements

 - [Helsinki-NLP/opus-mt-en-fi](https://huggingface.co/Helsinki-NLP/opus-mt-en-fi)
 - [Helsinki-NLP/opus-mt-fi-en](https://huggingface.co/Helsinki-NLP/opus-mt-fi-en)
 - [TranslationPipeline](https://huggingface.co/docs/transformers/main_classes/pipelines#transformers.TranslationPipeline)

## Website 
/Home: translation from finnish to english
<img width="971" alt="image" src="https://github.com/nessa01macias/Metropolia-Wide-AI-Translator/assets/92785400/8cf80563-3c8e-4cd6-b5f6-964ed247dd35">

/Home: translation from english to finnish
<img width="969" alt="image" src="https://github.com/nessa01macias/Metropolia-Wide-AI-Translator/assets/92785400/7ed2e86f-38f5-4a7d-b78e-b5adecb1c11f">

/Register: validation for registering users inplace
<img width="976" alt="image" src="https://github.com/nessa01macias/Metropolia-Wide-AI-Translator/assets/92785400/da9b0d86-d93a-4c54-9b31-342059597aa2">

/Login: after user creation, it redirects to login page
<img width="972" alt="image" src="https://github.com/nessa01macias/Metropolia-Wide-AI-Translator/assets/92785400/063b1e19-8cd6-4f1a-bdd6-43f0b1ac07a8">

/Login: validation for user log 
<img width="975" alt="image" src="https://github.com/nessa01macias/Metropolia-Wide-AI-Translator/assets/92785400/19743d70-ba9e-4c39-816c-87417586b1f9">

/Home: when an user is logged in, translations history page unlocks
<img width="1488" alt="image" src="https://github.com/nessa01macias/Metropolia-Wide-AI-Translator/assets/92785400/632424c4-7ce9-43e8-adaf-9bf2fe72b895">

/Translations: it displays the translations from that specific user
<img width="1482" alt="image" src="https://github.com/nessa01macias/Metropolia-Wide-AI-Translator/assets/92785400/b00cb4c5-000d-4fad-8294-2e3de575f6e0">

/Translations: view when an user is new and they have no translations yet. It is also mobile responsible.
<img width="627" alt="image" src="https://github.com/nessa01macias/Metropolia-Wide-AI-Translator/assets/92785400/d0a86b2a-b817-4fba-9277-4d313a3f666c">

/About: contains information about the webpage purposes
<img width="1477" alt="image" src="https://github.com/nessa01macias/Metropolia-Wide-AI-Translator/assets/92785400/fc5449d3-c3c4-46b7-a9d0-8191e1a0ddbe">

