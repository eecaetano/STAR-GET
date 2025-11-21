# app/routes/auth_routes.py
from flask import render_template, request, redirect, url_for, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
import base64
from io import BytesIO
from PIL import Image
import numpy as np
import face_recognition
from .. import db
from ..models import Funcionario

# Variáveis globais
TOLERANCE = 0.5
known_encodings = []
known_names = []

def init_routes(app):
    """Inicializa todas as rotas e variáveis que dependem do app."""

    UPLOAD_DIR = os.path.join(app.root_path, 'static', 'upload')

    # ---------------- Função para carregar faces conhecidas ----------------
    def load_known_faces():
        global known_encodings, known_names
        known_encodings = []
        known_names = []

        if not os.path.exists(UPLOAD_DIR):
            os.makedirs(UPLOAD_DIR, exist_ok=True)
            return

        for filename in os.listdir(UPLOAD_DIR):
            if not filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                continue
            path = os.path.join(UPLOAD_DIR, filename)
            name = os.path.splitext(filename)[0]
            try:
                image = face_recognition.load_image_file(path)
                encs = face_recognition.face_encodings(image)
                if encs:
                    known_encodings.append(encs[0])
                    known_names.append(name)
            except Exception as e:
                print(f'Erro ao carregar {filename}: {e}')

    # Carrega faces conhecidas ao iniciar
    load_known_faces()

    # ---------------- ROTAS ----------------
    @app.route('/')
    def display():
        return render_template('display.html')

    @app.route('/cadastro', methods=['GET', 'POST'])
    def cadastro():
        if request.method == 'POST':
            rg = request.form.get('cpf_pk')
            email = request.form.get('sk_email')
            senha1 = request.form.get('senha_1')
            senha2 = request.form.get('senha_2')
            imagem = request.files.get('image')

            if senha1 != senha2:
                flash('As senhas não coincidem!')
                return redirect(url_for('cadastro'))

            if not rg or not email or not senha1:
                flash('CPF, email e senha são obrigatórios!')
                return redirect(url_for('cadastro'))

            funcionario_existente = Funcionario.query.filter_by(cpf_pk=rg).first()
            if funcionario_existente:
                flash('CPF já cadastrado!')
                return redirect(url_for('cadastro'))

            email_existente = Funcionario.query.filter_by(sk_email=email).first()
            if email_existente:
                flash('Email já cadastrado!')
                return redirect(url_for('cadastro'))

            senha_hash = generate_password_hash(senha1)

            # Salva a imagem enviada
            if imagem and imagem.filename:
                nome_arquivo = secure_filename(imagem.filename)
                os.makedirs(UPLOAD_DIR, exist_ok=True)
                caminho = os.path.join(UPLOAD_DIR, nome_arquivo)
                try:
                    imagem.save(caminho)
                    print(f"✅ Imagem salva em: {caminho}")
                    load_known_faces()  # Atualiza encodings
                except Exception as e:
                    flash(f'Erro ao salvar imagem: {str(e)}')
                    return redirect(url_for('cadastro'))

            try:
                novo_funcionario = Funcionario(cpf_pk=rg, sk_email=email, senha=senha_hash)
                db.session.add(novo_funcionario)
                db.session.commit()
                flash('Cadastro realizado com sucesso!')
                return redirect(url_for('login'))
            except Exception as e:
                db.session.rollback()
                flash(f'Erro ao realizar cadastro: {str(e)}')
                return redirect(url_for('cadastro'))

        return render_template('cadastro2.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            cp = request.form['cpf_pk']
            senha = request.form['senha']
            usuario = Funcionario.query.filter_by(cpf_pk=cp).first()
            if usuario and check_password_hash(usuario.senha, senha):
                flash('Login realizado com sucesso!')
                return redirect(url_for('pos_login'))
            else:
                flash('CPF ou senha incorretos!')
        return render_template('login.html')

    @app.route('/pos_login')
    def pos_login():
        funcionarios = Funcionario.query.all()
        return render_template('pos_login.html', dados=funcionarios)

    @app.route('/recognize_face', methods=['POST'])
    def recognize_face():
        try:
            data = request.get_json()
            if not data or 'image' not in data:
                return jsonify({'status': 'denied'})

            img_b64 = data['image'].split(",")[-1]
            img_bytes = BytesIO(base64.b64decode(img_b64))
            img = Image.open(img_bytes).convert('RGB')
            img_np = np.array(img)

            unknown_encodings = face_recognition.face_encodings(img_np)
            if not unknown_encodings:
                return jsonify({'status': 'denied'})

            for unknown in unknown_encodings:
                if not known_encodings:
                    return jsonify({'status': 'denied'})
                results = face_recognition.compare_faces(known_encodings, unknown, tolerance=TOLERANCE)
                if True in results:
                    best_idx = int(np.argmin(face_recognition.face_distance(known_encodings, unknown)))
                    return jsonify({'status': 'granted', 'name': known_names[best_idx]})

            return jsonify({'status': 'denied'})

        except Exception as e:
            print('Erro no reconhecimento facial:', e)
            return jsonify({'status': 'denied'})
