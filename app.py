import os
import sys
from flask import Flask, render_template, request, jsonify, send_from_directory

# Adiciona o diretório atual ao path para garantir importações corretas
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.hash import RepositorioUsuarios, HashEducacional
from core.simetria import CifraSimetricaEducacional
from core.assimetria import CifraAssimetricaEducacional

app = Flask(__name__)

# Instanciação global do repositório em memória para persistência de sessão
user_repo = RepositorioUsuarios()

@app.route('/uniateneulogo/<path:filename>')
def serve_logo(filename):
    return send_from_directory('uniateneulogo', filename)

@app.route('/')
def index():
    """Rota principal que serve a interface gráfica unificada."""
    return render_template('index.html')

# ==========================================
# ROTAS DA API: HASH E AUTENTICAÇÃO
# ==========================================

@app.route('/api/hash/register', methods=['POST'])
def hash_register():
    data = request.get_json() or {}
    username = data.get('username', '')
    password = data.get('password', '')
    
    try:
        success, message, logs = user_repo.cadastrar(username, password)
        return jsonify({
            "success": success,
            "message": message,
            "logs": logs
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Erro interno no servidor: {str(e)}",
            "logs": []
        }), 500

@app.route('/api/hash/login', methods=['POST'])
def hash_login():
    data = request.get_json() or {}
    username = data.get('username', '')
    password = data.get('password', '')
    
    try:
        success, message, logs = user_repo.autenticar(username, password)
        return jsonify({
            "success": success,
            "message": message,
            "logs": logs
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Erro interno no servidor: {str(e)}",
            "logs": []
        }), 500

@app.route('/api/hash/users', methods=['GET'])
def hash_users():
    try:
        users = user_repo.obter_lista_usuarios()
        return jsonify({
            "success": True,
            "users": users
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

# ==========================================
# ROTAS DA API: CRIPTOGRAFIA SIMÉTRICA (FEISTEL)
# ==========================================

@app.route('/api/symmetric/encrypt', methods=['POST'])
def symmetric_encrypt():
    data = request.get_json() or {}
    message = data.get('message', '')
    key = data.get('key', '')
    
    if not message:
        return jsonify({"success": False, "message": "Mensagem vazia."}), 400
        
    try:
        ciphertext_hex, logs = CifraSimetricaEducacional.cifrar(message, key)
        return jsonify({
            "success": True,
            "ciphertext": ciphertext_hex,
            "logs": logs
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Erro na cifragem: {str(e)}",
            "logs": []
        }), 500

@app.route('/api/symmetric/decrypt', methods=['POST'])
def symmetric_decrypt():
    data = request.get_json() or {}
    ciphertext = data.get('ciphertext', '')
    key = data.get('key', '')
    
    if not ciphertext:
        return jsonify({"success": False, "message": "Ciphertext vazio."}), 400
        
    try:
        decrypted_text, logs = CifraSimetricaEducacional.decifrar(ciphertext, key)
        return jsonify({
            "success": decrypted_text != "",
            "plaintext": decrypted_text,
            "logs": logs
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Erro na decifragem. Certifique-se de que o texto cifrado é hexadecimal válido: {str(e)}",
            "logs": []
        }), 500

# ==========================================
# ROTAS DA API: CRIPTOGRAFIA ASSIMÉTRICA (RSA)
# ==========================================

@app.route('/api/asymmetric/keygen', methods=['POST'])
def asymmetric_keygen():
    data = request.get_json() or {}
    try:
        p = int(data.get('p', 61))
        q = int(data.get('q', 53))
        
        keys, logs = CifraAssimetricaEducacional.gerar_chaves(p, q)
        return jsonify({
            "success": True,
            "keys": keys,
            "logs": logs
        })
    except ValueError as ve:
        return jsonify({
            "success": False,
            "message": str(ve),
            "logs": [f"Erro de Validação: {str(ve)}"]
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Erro interno na geração das chaves: {str(e)}",
            "logs": []
        }), 500

@app.route('/api/asymmetric/encrypt', methods=['POST'])
def asymmetric_encrypt():
    data = request.get_json() or {}
    message = data.get('message', '')
    try:
        e = int(data.get('e'))
        n = int(data.get('n'))
        
        ciphertext, logs = CifraAssimetricaEducacional.cifrar(message, e, n)
        return jsonify({
            "success": True,
            "ciphertext": ciphertext,
            "logs": logs
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Erro ao cifrar: {str(e)}",
            "logs": []
        }), 500

@app.route('/api/asymmetric/decrypt', methods=['POST'])
def asymmetric_decrypt():
    data = request.get_json() or {}
    try:
        ciphertext_raw = data.get('ciphertext')
        if isinstance(ciphertext_raw, str):
            # Tenta converter string separada por vírgula em lista de inteiros
            ciphertext = [int(x.strip()) for x in ciphertext_raw.replace('[', '').replace(']', '').split(',') if x.strip()]
        else:
            ciphertext = [int(x) for x in ciphertext_raw]
            
        d = int(data.get('d'))
        n = int(data.get('n'))
        
        decrypted_text, logs = CifraAssimetricaEducacional.decifrar(ciphertext, d, n)
        return jsonify({
            "success": True,
            "plaintext": decrypted_text,
            "logs": logs
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Erro ao decifrar: {str(e)}. Certifique-se de passar uma lista válida de inteiros.",
            "logs": []
        }), 500


if __name__ == '__main__':
    # Roda em localhost na porta 5000 por padrão
    print("Iniciando o servidor Flask educacional MiniCript...")
    print("Por favor, acesse http://127.0.0.1:5000 no seu navegador.")
    app.run(debug=True, host='127.0.0.1', port=5000)
