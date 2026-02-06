from flask import Flask, request, render_template_string, redirect, session
import os

app = Flask(__name__)
app.secret_key = "enfevolue-secreto"

# 🔐 senha simples
SENHA_SITE = "enf123"

# 🔐 tela de login
LOGIN_HTML = """
<h2>EnfEvolue</h2>
<form method="post">
    <p>Digite a senha para acessar:</p>
    <input type="password" name="senha" required>
    <br><br>
    <button type="submit">Entrar</button>
    {% if erro %}
        <p style="color:red;">Senha incorreta</p>
    {% endif %}
</form>
"""

# 🧠 HTML PRINCIPAL
HTML = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>EnfBot – Evolução de Enfermagem</title>
</head>
<body>

<h2>EnfBot – Evolução Técnica de Enfermagem</h2>

<form method="POST">

<label>Horário da evolução</label><br>
<input type="time" name="horario" required><br><br>

<label>Paciente consciente e orientado?</label><br>
<select name="consciente" required>
    <option value="">Selecione</option>
    <option value="1">1 - Sim</option>
    <option value="2">2 - Não</option>
</select><br><br>

<label>Paciente se queixa de algo?</label><br>
<select name="queixa" required>
    <option value="">Selecione</option>
    <option value="1">1 - Sim</option>
    <option value="2">2 - Não</option>
</select><br><br>

<label>Se sim, qual a queixa?</label><br>
<input type="text" name="descricao_queixa"><br><br>

<label>Escala da dor (0–10)</label><br>
<input type="number" name="dor" min="0" max="10"><br><br>

<label>Punção venosa realizada?</label><br>
<select name="puncao" required>
    <option value="">Selecione</option>
    <option value="1">1 - Sim</option>
    <option value="2">2 - Não</option>
</select><br><br>

<label>Você sabe a numeração do abocath?</label><br>
<select name="sabe_abocath" required>
    <option value="">Selecione</option>
    <option value="1">1 - Sim</option>
    <option value="2">2 - Não</option>
</select><br><br>

<label>Numeração do abocath</label><br>
<select name="abocath">
    <option value="">Selecione</option>
    <option value="18">18</option>
    <option value="20">20</option>
    <option value="22">22</option>
    <option value="24">24</option>
</select><br><br>

<label>Medicação administrada conforme prescrição?</label><br>
<select name="medicacao" required>
    <option value="">Selecione</option>
    <option value="1">1 - Sim</option>
    <option value="2">2 - Não</option>
</select><br><br>

<label>Desfecho do paciente</label><br>
<select name="desfecho" required>
    <option value="">Selecione</option>
    <option value="1">1 - Alta</option>
    <option value="2">2 - Retorno para avaliação médica</option>
</select><br><br>

<label>Técnica de enfermagem</label><br>
<input type="text" name="tecnica" required><br><br>

<button type="submit">Gerar evolução</button>

</form>

{% if texto %}
<hr>
<h3>Evolução gerada</h3>
<textarea rows="14" cols="90" readonly>{{ texto }}</textarea>
{% endif %}

</body>
</html>
"""

# 🔐 rota de login
@app.route("/login", methods=["GET", "POST"])
def login():
    erro = False
    if request.method == "POST":
        if request.form["senha"] == SENHA_SITE:
            session["logado"] = True
            return redirect("/")
        erro = True
    return render_template_string(LOGIN_HTML, erro=erro)

# 🧠 rota principal
@app.route("/", methods=["GET", "POST"])
def index():
    if not session.get("logado"):
        return redirect("/login")

    texto = ""

    if request.method == "POST":
        h = request.form["horario"]
        consciente = request.form["consciente"]
        queixa = request.form["queixa"]
        desc = request.form["descricao_queixa"]
        dor = request.form["dor"]
        puncao = request.form["puncao"]
        sabe_abocath = request.form["sabe_abocath"]
        abocath = request.form["abocath"]
        medicacao = request.form["medicacao"]
        desfecho = request.form["desfecho"]
        tecnica = request.form["tecnica"]

        texto = f"{h} – Recebo paciente da Sala de Medicação.\n"
        texto += "Paciente consciente e orientado.\n" if consciente == "1" else "Paciente não orientado.\n"

        if queixa == "1":
            texto += f"Refere {desc if desc else 'queixa não especificada'}"
            if dor:
                texto += f", escala de dor {dor}/10."
            texto += "\n"
        else:
            texto += "Paciente sem queixas no momento.\n"

        if puncao == "1":
            if sabe_abocath == "1" and abocath:
                texto += f"Punção venosa realizada com sucesso com abocath {abocath}.\n"
            else:
                texto += "Punção venosa realizada com sucesso.\n"

        texto += "Medicação administrada conforme prescrição médica.\n" if medicacao == "1" else "Medicação não administrada.\n"
        texto += "Paciente recebe alta.\n" if desfecho == "1" else "Paciente retorna para avaliação médica.\n"
        texto += f"\n{tecnica}\nTécnica de Enfermagem"

    return render_template_string(HTML, texto=texto)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))