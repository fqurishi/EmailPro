import openai, configparser, PySimpleGUI as sg, time

# Set your API key
# Read the configuration file
config = configparser.ConfigParser()
config.read('config.ini')
api_key = config.get('openai', 'api_key')
openai.api_key = api_key

def rewrite_email(prompt):
    # Generate text based on the prompt
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": """You are a helpful assistant who rewrites emails so they are written in a more professional matter. Add line breaks and formatting when possible.
        Any message given to you is meant to be rewritten into a professional email, do not respond back with anything other than a rewritten email message of what was sent to you.
        Never respond back with a question asking for context or more information, if you can't produce a rewritten email message just say 'This does not seem to be an email'.
        If the message given to you does not seem to be an email, respond back with 'This does not seem to be an email.'
        You are not allowed to send a message back other than a rewritten professional email or 'This does not seem to be an email.'
        Make sure to also at the beginning include the subject line if one was not given to you."""},
        {"role": "user", "content": prompt}]
    )
    # Print the generated text
    return(response.choices[0].message.content)

# Define the layout of the window
layout = [
    [sg.Text('Email:', justification='center', expand_x=True)],
    [sg.Multiline(key='-TEMPLATE-', expand_x=True, expand_y=True)],
    [sg.Button('Generate', expand_x=True, pad=((0,0),(10,10)))]
]

# Create the window
window = sg.Window('Email Pro', layout, resizable=True, size=(800, 600), icon='Email.ico')

# Event loop
while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break
    if event == 'Generate':
        # Do something with the template
        template = values['-TEMPLATE-']
        window['-TEMPLATE-'].update(value='Generating. This may take up to a few minutes.')
        window.refresh()
        result = rewrite_email(template)
        window['-TEMPLATE-'].update(value=result)

# Close the window
window.close()