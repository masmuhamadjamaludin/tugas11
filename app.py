from flask import Flask,redirect,url_for,render_template,request,jsonify
from pymongo import MongoClient
import requests
from datetime import datetime
from bson import ObjectId

app = Flask (__name__)


client = MongoClient('mongodb://jamal:jamal@ac-qxx6olp-shard-00-00.lbomoax.mongodb.net:27017,ac-qxx6olp-shard-00-01.lbomoax.mongodb.net:27017,ac-qxx6olp-shard-00-02.lbomoax.mongodb.net:27017/?ssl=true&replicaSet=atlas-2kj0jp-shard-0&authSource=admin&retryWrites=true&w=majority')
db = client.dbsparta_plus_week2

@app.route('/')
def main():
    words_result = db.words.find({}, {'_id': False})
    words = []
    for word in words_result:
        definition = word['definitions']
        definition = definition if type(definition) is str else definition[0]
        words.append({
            'word': word['word'],
            'definition': definition,
        })
    msg = request.args.get('msg')
    return render_template(
        'index.html',
        words=words,
        msg=msg
    )

@app.route('/detail/<keyword>')
def detail(keyword):
    api_key = "2ef83c94-9560-4ae3-b1a0-62dc81ee4581"
    url = f'https://www.dictionaryapi.com/api/v3/references/collegiate/json/{keyword}?key={api_key}'
    response = requests.get(url)
    definitions = response.json()

    if not definitions:
        return redirect(url_for(
            'main',
            msg=f'Could not find {keyword}'
        ))

    if type(definitions[0]) is str:
        return redirect(url_for(
            'main',
            msg=f'Could not find {keyword}, did you mean {", ".join(definitions)}?'
        ))

    status = request.args.get('status_give', 'new')
    return render_template(
        'detail.html',
        word=keyword,
        definitions=definitions,
        status=status
    )
@app.route('/api/word', methods=['GET'])
def word():
    return jsonify({'result': 'success'})

@app.route('/api/save_word', methods=['POST'])
def save_word():
    json_data = request.get_json()
    word = json_data.get('word_give')
    definitions = json_data.get('definitions_give')

    doc = {
        'word': word,
        'definitions': definitions,
        'date': datetime.now().strftime('%Y%m%d'),
    }
    
    # print(doc)
    db.words.insert_one(doc)

    return jsonify({
        'result': 'success',
        'msg': f'the word, {word}, was saved!!!',
    })

@app.route('/api/delete_word', methods=['POST'])
def delete_word():
    word = request.form.get('word_give')
    db.words.delete_one({'word': word})
    db.examples.delete_many({'word': word})
    return jsonify({
        'result': 'success',
        'msg': f'the word, {word}, was deleted',
    })

@app.route('/api/get_exs', methods=['GET'])
def get_exs():
    word = request.args.get('word')
    example_data = db.examples.find({'word': word})
    examples = []
    for example in example_data:
        examples.append({
            'example': example.get('example'),
            'id': str(example.get('_id')),
        })
    return jsonify({'result': 'success'})

@app.route('/api/save_ex', methods=['POST'])
def save_ex():
    word = request.form.get('word')
    example = request.form.get('example')
    doc = {
        'word': word,
        'example': example,
    }
    db.examples.insert_one(doc)
    return jsonify({
        'result': 'success',
        'msg': f'Your example, {example}, for the word, {word}, was saved!',
        })

@app.route('/api/delete_ex', methods=['POST'])
def delete_ex():
    id = request.form.get('id')
    word = request.form.get('word')
    db.example.delete_one({'id': ObjectId(id)})
    return jsonify({'result': 'success',
    'msg': f'Your example fo the word, {word}, was deleted!',
    })

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)