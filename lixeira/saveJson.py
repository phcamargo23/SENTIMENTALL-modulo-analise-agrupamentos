from flask import Flask, render_template, json

# Initialize the Flask application
app = Flask(__name__)

if __name__ == '__main__':
    obj = {
        'total': 0,
        'progress': 0,
        'percentual': 0
    }

    # Convert python object to json
    json_string = json.dumps(obj)
    open('_resultado.json', 'w').write(json_string)

    json_string = open('_resultado.json').read()
    new_obj = json.loads(json_string)
    print new_obj
    new_obj['total'] = 99

    # Convert python object to json
    json_string = json.dumps(new_obj)
    open('_resultado.json', 'w').write(json_string)