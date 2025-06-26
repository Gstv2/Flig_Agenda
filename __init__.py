from flask import Flask, render_template, redirect
from Controller.usuario_controller import usuario_bp

app = Flask(__name__,template_folder='View/templates', static_folder='View/Static')

app.register_blueprint(usuario_bp)

# Rota para a página inicial
@app.route('/')
def home():
    return render_template('index.html')

# Rota para a página inicial
@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

if __name__ == '__main__':
    app.run(debug=True)
