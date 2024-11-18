from flask import Flask, request, jsonify
import json
import uuid

app = Flask(__name__)
DATA_FILE = 'data.json'

def read_data():
    try:
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def write_data(data):
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)

@app.route('/data', methods=['GET', 'POST', 'DELETE'])
def data():
    if request.method == 'GET':
        return jsonify(read_data())
    elif request.method == 'POST':
        new_data = request.json
        data = read_data()
        
        data_id = str(uuid.uuid4())  # Gerar um ID único para os novos dados
        new_data['id'] = data_id     # Adicionar o ID aos novos dados
        
        data[data_id] = new_data     # Usar o ID como chave para os novos dados no dicionário
        
        write_data(data)
        return jsonify({'message': 'Data saved successfully!', 'id': data_id})
    elif request.method == 'DELETE':
        data = read_data()
        delete_id = request.args.get('id')  # Obter o ID a ser excluído da query string
        
        if delete_id in data:
            del data[delete_id]
            write_data(data)
            return jsonify({'message': 'Data deleted successfully!', 'id': delete_id}), 200
        else:
            return jsonify({'error': 'ID not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)