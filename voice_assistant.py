import datetime
import logging.config
import speech_recognition as sr
import pyttsx3
import webbrowser
import wikipedia
import wolframalpha

# Initialize the speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # 0 = male, 1 = female
activation_word = 'computer'  # Single word

# Configure the browser
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))

# Wolfram Alpha client
app_id = '5R49J7-J888YX9J2V'
wolfram_client = wolframalpha.Client(app_id)


def speak(text, rate=120):
    engine.setProperty('rate', rate)
    engine.say(text)
    engine.runAndWait()


def parse_command():
    listener = sr.Recognizer()
    print('Listening for a command')

    with sr.Microphone() as source:
        listener.pause_threshold = 2
        input_speech = listener.listen(source)

    try:
        print('Recognizing speech...')
        query = listener.recognize_google(input_speech, language='en_gb')
        print(f'Received command: {query}')
    except Exception as exception:
        print('Sorry, I didn\'t quite catch that')
        speak('Sorry, I didn\'t quite catch that')
        print(exception)
        return 'None'

    return query


def search_wikipedia(query=''):
    search_results = wikipedia.search(query)
    if not search_results:
        print('No Wikipedia results found')
        return 'No result received'
    try:
        wiki_page = wikipedia.page(search_results[0])
    except wikipedia.DisambiguationError as error:
        wiki_page = wikipedia.page(error.options[0])
    print('Wikipedia article title:', wiki_page.title)
    wiki_summary = str(wiki_page.summary)
    return wiki_summary


def list_or_dict(var):
    if isinstance(var, list):
        return var[0]['plaintext']
    else:
        return var['plaintext']


def search_wolfram_alpha(query=''):
    response = wolfram_client.query(query)

    if response['@success'] == 'false':
        return 'Could not compute'
    else:
        result = ''
        pod0 = response['pod'][0]
        pod1 = response['pod'][1]

        if ('result' in pod1['@title'].lower()) or (pod1.get('@primary', 'false') == 'true') or (
                'definition' in pod1['@title'].lower()):
            result = list_or_dict(pod1['subpod'])
            return result.split('(')[0]
        else:
            question = list_or_dict(pod0['subpod'])
            return question.split('(')[0]


if __name__ == '__main__':
    speak('All systems online and ready.')

    while True:
        query = parse_command().lower().split()

        if query[0] == activation_word:
            query.pop(0)

            if query[0] == 'speak':
                if 'hello' in query:
                    speak('Greetings, everyone.')
                else:
                    query.pop(0)
                    speech = ' '.join(query)
                    speak(speech)

            if query[0] == 'navigate' and query[1] == 'to':
                speak('Opening...')
                query = ' '.join(query[2:])
                webbrowser.get('chrome').open_new(query)

            if query[0] == 'lookup':
                query = ' '.join(query[1:])
                speak('Searching the vast knowledge repository.')
                speak(search_wikipedia(query))

            if query[0] == 'calculate' or query[0] == 'compute':
                query = ' '.join(query[1:])
                speak('Processing computation')
                try:
                    result = search_wolfram_alpha(query)
                    speak(result)
                except:
                    speak('Unable to perform the calculation.')

            if query[0] == 'record':
                speak('Ready to jot down your note')
                new_note = parse_command().lower()
                now = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
                with open('note_%s.txt' % now, 'w') as new_file:
                    new_file.write(new_note)
                speak('Note saved successfully.')

            if query[0] == 'shutdown':
                speak('Goodbye')
                break
