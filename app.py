from flask import Flask, request, jsonify, render_template
import mysql.connector
from flask_mysqldb import MySQL



app = Flask(__name__)

# app.secret_key = 'minha_chave_super_secreta_123'
# Configurações do MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="nodemysql"
)

# Configurações do MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'nodemysql'

mysql = MySQL(app)

def fetch_characters():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM characters')  # Substitua 'characters' pelo nome da sua tabela
    characters = cursor.fetchall()
    
    # Transformar os dados em uma lista de dicionários
    characters_list = []
    for character in characters:
        characters_list.append({
            'nome': character[0],
            'vida': character[1],
            'mana': character[2],
            'level': character[3],
            'dinheiro': character[4],
            'pot': character[5],
            'status': character[6],
            'outType': character[8],
            'outHead': character[9],
            'outBody': character[10],
            'outLegs': character[11],
            'outFeet': character[12],
            
        })
    
    cursor.close()
    return characters_list

# Endpoint para obter todos os characters_list
@app.route('/personagem', methods=['GET'])
def get_characters_list():
    characters_list = fetch_characters() 
    return jsonify(characters_list), 200


@app.route('/')
def index():
    return render_template('index.html')


# Endpoint para atualizar as estatísticas de um personagem específico
@app.route('/atualizar_stats/<int:id>', methods=['POST'])
def atualizar_stats(id):
    data = request.get_json()

    # Verifique se o personagem existe no banco de dados
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM characters WHERE id = %s', (id,))  # Supondo que você tenha um campo 'id'
    character = cursor.fetchone()

    if character:
        # Atualiza os dados no banco de dados
        update_query = '''
            UPDATE characters SET 
                nome = %s,
                vida = %s, 
                mana = %s, 
                level = %s, 
                dinheiro = %s, 
                pot = %s, 
                status = %s,
                outType = %s,
                outHead = %s,
                outBody = %s,
                outLegs = %s,
                outFeet = %s
            WHERE id = %s
        '''
        cursor.execute(update_query, (
            data.get('nome', character[0]),
            data.get('vida', character[1]),
            data.get('mana', character[2]),
            data.get('level', character[3]),
            data.get('dinheiro', character[4]),
            data.get('pot', character[5]),
            data.get('status', character[6]),
            data.get('outType', character[7]),
            data.get('outHead', character[8]),
            data.get('outBody', character[9]),
            data.get('outLegs', character[10]),
            data.get('outFeet', character[11]),
            id
        ))
        mysql.connection.commit()
        cursor.close()

        # Retorna o personagem atualizado
        return jsonify({
            'id': id,
            'nome': data.get('nome', character[0]),
            'vida': data.get('vida', character[1]),
            'mana': data.get('mana', character[2]),
            'level': data.get('level', character[3]),
            'dinheiro': data.get('dinheiro', character[4]),
            'pot': data.get('pot', character[5]),
            'status': data.get('status', character[6]),
            'outType': data.get('outType', character[7]),
            'outHead': data.get('outHead', character[8]),
            'outBody': data.get('outBody', character[9]),
            'outLegs': data.get('outLegs', character[10]),
            'outFeet': data.get('outFeet', character[11]),

        }), 200
    else:
        cursor.close()
        return jsonify({'error': 'Personagem não encontrado'}), 404


if __name__ == '__main__':
    app.run(host='192.168.4.132', port=5001, debug=True)