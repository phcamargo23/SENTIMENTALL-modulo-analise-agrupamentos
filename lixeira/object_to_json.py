from flask import Flask, render_template, json

# Initialize the Flask application
app = Flask(__name__)


@app.route('/')
def index():
    obj = [[1, 2, 3], 123, 123.123, 'abc', {'key1': (1, 2, 3), 'key2': (4, 5, 6)}]

    # Convert python object to json
    json_string = json.dumps(obj)
    print 'Json: %s' % json_string

    open('_resultado.json', 'w').write(json_string)
    json_string = open('_resultado.json').read()


    # Convert json to python object
    new_obj = json.loads(json_string)
    print 'Python obj: ', new_obj

    # Render template
    # return render_template('index.html', json=json_string, obj=new_obj)


# Run
if __name__ == '__main__':
    # app.run()
    index()