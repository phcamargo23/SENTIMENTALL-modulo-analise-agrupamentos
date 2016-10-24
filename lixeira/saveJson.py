from flask import Flask, render_template, json

# Initialize the Flask application
app = Flask(__name__)

if __name__ == '__main__':
    # with open('../input/dataset.csv') as f:
        # data = json.load(f)
        # data = f.readlines()
        # f.write("appended text")

    # data.update(saidaEstado);
    #
    # with open(output_dir + '/_resultado.json', 'w') as f:
    #     json.dump(data, f)


    # obj = [[1, 2, 3], 123, 123.123, 'abc', {'key1': (1, 2, 3), 'key2': (4, 5, 6)}]
    #
    # # Convert python object to json
    # json_string = json.dumps(obj)
    # print 'Json: %s' % json_string
    #
    # open('_resultado.json', 'w').write(json_string)
    # json_string = open('_resultado.json').read()
    #
    # # Convert json to python object
    # new_obj = json.loads(json_string)
    # print 'Python obj: ', new_obj
    #
    # # Render template
    # # return render_template('index.html', json=json_string, obj=new_obj)

    obj = [[1, 2, 3], 123, 123.123, 'abc', {'key1': (1, 2, 3), 'key2': (4, 5, 6)}]
    json_string = json.dumps(obj)
    open('../input/dataset.csv', 'a').write(json_string)