from flask import Flask, request, render_template, render_template_string, redirect, session
from dotenv import load_dotenv
import os

# ================= CONFIG =================
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY") or "enfevolue-secreto"
SENHA_SITE = os.getenv("SENHA_SITE") or "1234"

# ================= PROFISSIONAIS FIXOS =================
PROFISSIONAIS = {
    "Miranilde Cardoso dos Santos Sousa": "COREN-GO 1.557.972",
    "Edna Maria Paulino da Silva": "COREN-GO 2.314.046",
    "Valderice Alves da Silva": "COREN-GO 1.062.815",
    "Barbara Elen Sales Nunes": "COREN-GO 2.375.052",
    "Elivane Sales Lima dos Santos": "COREN-GO 1.873.617"
}

profissionais_temporarios = {}

# ================= LOGIN =================
LOGIN_HTML = """ 
<!DOCTYPE html>
<html lang="pt-br">
<head>
<meta charset="UTF-8">
<title>EnfEvolue – Login</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="stylesheet" href="/static/style.css">
</head>
<body>
<header>
<h1>EnfEvolue</h1>
<p>Evolução Técnica de Enfermagem</p>
</header>
<main>
<form method="post" style="max-width:400px;margin:auto;">
<h2 style="text-align:center;">
Acesso Restrito - Versão em Desenvolvimento
</h2>
<p style="text-align:center;margin-bottom:20px;">
Usuários salvos somem ao reiniciar o sistema.
</p>

<label>Digite a senha</label>
<input type="password" name="senha" required>

{% if erro %}
<p style="color:red;text-align:center;margin-top:10px;">
Senha incorreta
</p>
{% endif %}

<button type="submit">Entrar</button>
</form>
</main>
<footer>
<p>
EnfEvolue © 2026<br>
Ferramenta de apoio à evolução técnica de enfermagem
</p>
<strong>Desenvolvido por Bárbara Nunes Programmer</strong>
</footer>
</body>
</html>
"""

@app.route("/login", methods=["GET", "POST"])
def login():
    erro = False
    if request.method == "POST":
        if request.form.get("senha") == SENHA_SITE:
            session["logado"] = True
            return redirect("/")
        erro = True
    return render_template_string(LOGIN_HTML, erro=erro)

# ================= SISTEMA =================
@app.route("/", methods=["GET", "POST"])
def index():
    if not session.get("logado"):
        return redirect("/login")

    texto = ""
    mensagem = ""

    if request.method == "POST":
        acao = request.form.get("acao")

        # 🔹 CADASTRAR PROFISSIONAL TEMPORÁRIO
        if acao == "cadastrar_profissional":
            novo_nome = request.form.get("novo_nome", "").strip()
            novo_coren = request.form.get("novo_coren", "").strip()
            if novo_nome and novo_coren:
                profissionais_temporarios[novo_nome] = novo_coren
                mensagem = "Profissional cadastrada com sucesso (temporariamente)"

        # 🔹 GERAR EVOLUÇÃO
        if acao == "gerar_evolucao":

            todos_profissionais = {**PROFISSIONAIS, **profissionais_temporarios}

            h = request.form.get("horario", "")
            consciente = request.form.get("consciente", "")
            queixa = request.form.get("queixa", "")
            desc = request.form.get("descricao_queixa", "")
            dor = request.form.get("dor", "")
            puncao = request.form.get("puncao", "")
            abocath = request.form.get("abocath", "")
            medicacao = request.form.get("medicacao", "")
            desfecho = request.form.get("desfecho", "")
            observacao = request.form.get("observacao", "")
            profissional = request.form.get("profissional", "")
            profissional_outro = request.form.get("profissional_outro", "")
            coren_manual = request.form.get("coren", "")

            if profissional == "outra" and profissional_outro:
                nome_profissional = profissional_outro
                coren = coren_manual if coren_manual else "COREN não informado"
            else:
                nome_profissional = profissional
                coren = todos_profissionais.get(profissional, "COREN não informado")

            texto = f"{h} – Recebo paciente da Sala de Medicação.\n"

            texto += (
                "Paciente consciente e orientado.\n"
                if consciente == "1"
                else "Paciente não orientado.\n"
            )

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

            if desfecho == "1":
                texto += "Paciente recebe alta.\n"
            elif desfecho == "2":
                texto += "Paciente retorna para avaliação médica.\n"
            elif desfecho == "3":
                texto += "Paciente evadiu.\n"

            if observacao:
                texto += f"Observação: {observacao}\n"

            texto += f"\n{nome_profissional} – {coren}\nTécnica de Enfermagem"

    todos_profissionais = {**PROFISSIONAIS, **profissionais_temporarios}

    return render_template(
        "index.html",
        texto=texto,
        profissionais=todos_profissionais,
        mensagem=mensagem
    )

# ================= LOGOUT =================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# ================= RODAR LOCAL =================
if __name__ == "__main__":
    app.run(debug=True)