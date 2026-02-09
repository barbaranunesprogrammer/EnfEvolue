from flask import Flask, request, render_template, render_template_string, redirect, session

app = Flask(__name__)
app.secret_key = "enfevolue-secreto"

SENHA_SITE = "enf123"

PROFISSIONAIS = {
    "Miranilde Cardoso dos Santos Sousa": "COREN-GO 1.557.972",
    "Edna Maria Paulino da Silva": "COREN-GO 2.314.046",
    "Valderice Alves da Silva": "COREN-GO 1.062.815",
    "Barbara Elen Sales Nunes": "COREN-GO 2.375.052",
    "Elivane Sales Lima dos Santos": "COREN-GO 1.873.617"
}

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

@app.route("/login", methods=["GET", "POST"])
def login():
    erro = False
    if request.method == "POST":
        if request.form["senha"] == SENHA_SITE:
            session["logado"] = True
            return redirect("/")
        erro = True
    return render_template_string(LOGIN_HTML, erro=erro)

@app.route("/", methods=["GET", "POST"])
def index():
    if not session.get("logado"):
        return redirect("/login")

    texto = ""

    if request.method == "POST":
        h = request.form["horario"]
        consciente = request.form["consciente"]
        queixa = request.form["queixa"]
        desc = request.form.get("descricao_queixa", "")
        dor = request.form.get("dor", "")
        puncao = request.form["puncao"]
        abocath = request.form.get("abocath", "")
        medicacao = request.form["medicacao"]
        desfecho = request.form["desfecho"]

        profissional = request.form["profissional"]
        profissional_outro = request.form.get("profissional_outro", "")
        coren_manual = request.form.get("coren", "")

        if profissional == "outra" and profissional_outro:
            nome_profissional = profissional_outro
            coren = coren_manual if coren_manual else "COREN não informado"
        else:
            nome_profissional = profissional
            coren = PROFISSIONAIS.get(profissional, "COREN não informado")

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
            if abocath:
                texto += f"Punção venosa realizada com sucesso com abocath {abocath}.\n"
            else:
                texto += "Punção venosa realizada com sucesso.\n"

        texto += (
            "Medicação administrada conforme prescrição médica.\n"
            if medicacao == "1"
            else "Medicação não administrada.\n"
        )

        texto += (
            "Paciente recebe alta.\n"
            if desfecho == "1"
            else "Paciente retorna para avaliação médica.\n"
        )

        texto += f"\n{nome_profissional} – {coren}\nTécnica de Enfermagem"

    return render_template("index.html", texto=texto)

if __name__ == "__main__":
    app.run(debug=True)
