import os
import sqlite3
import paramiko
import subprocess
from flask import Flask, request, jsonify
from flask_cors import CORS

class SSHManager:
    def __init__(self, db_path='servers.db'):
        self.db_path = db_path
        self._init_database()

    def _init_database(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS servers (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    host TEXT,
                    port INTEGER DEFAULT 22,
                    username TEXT,
                    password TEXT,
                    private_key TEXT,
                    category TEXT
                )
            ''')
            conn.commit()

    def add_server(self, name, host, port, username, password=None, private_key=None, category='默认'):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO servers 
                (name, host, port, username, password, private_key, category) 
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (name, host, port, username, password, private_key, category))
            conn.commit()
            return cursor.lastrowid

    def get_servers(self, category=None):
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            if category:
                cursor.execute('SELECT * FROM servers WHERE category = ?', (category,))
            else:
                cursor.execute('SELECT * FROM servers')
            return [dict(row) for row in cursor.fetchall()]

    def check_server_status(self, host, port=22):
        try:
            # Ping检测
            ping_result = subprocess.run(['ping', '-c', '3', host], 
                                          capture_output=True, text=True, timeout=3)
            ping_success = ping_result.returncode == 0

            # SSH连接检测
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(host, port=port, timeout=3)
            ssh_success = True
            client.close()

            return {
                'ping_status': ping_success,
                'ssh_status': ssh_success,
                'overall_status': ping_success and ssh_success
            }
        except Exception as e:
            return {
                'ping_status': False,
                'ssh_status': False,
                'overall_status': False,
                'error': str(e)
            }

    def delete_server(self, server_id):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM servers WHERE id = ?', (server_id,))
            conn.commit()
            return cursor.rowcount > 0

app = Flask(__name__)
CORS(app)
ssh_manager = SSHManager()

@app.route('/servers', methods=['GET'])
def list_servers():
    category = request.args.get('category')
    servers = ssh_manager.get_servers(category)
    return jsonify(servers)

@app.route('/servers', methods=['POST'])
def add_server():
    data = request.json
    server_id = ssh_manager.add_server(
        name=data['name'],
        host=data['host'],
        port=data.get('port', 22),
        username=data['username'],
        password=data.get('password'),
        private_key=data.get('private_key'),
        category=data.get('category', '默认')
    )
    return jsonify({'id': server_id})

@app.route('/servers/<int:server_id>', methods=['DELETE'])
def delete_server(server_id):
    result = ssh_manager.delete_server(server_id)
    return jsonify({'success': result})

@app.route('/servers/status/<string:host>', methods=['GET'])
def check_server_status(host):
    port = request.args.get('port', 22, type=int)
    status = ssh_manager.check_server_status(host, port)
    return jsonify(status)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
