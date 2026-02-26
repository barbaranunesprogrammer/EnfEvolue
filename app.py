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

# 🔹 Temporários (somem ao reiniciar)
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
Acesso Restrito
</h2>

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
<p>EnfEvolue © 2026</p>
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

        # =========================
        # CADASTRAR PROFISSIONAL TEMPORÁRIO
        # =========================
        if acao == "cadastrar_profissional":
            nome = request.form.get("novo_nome", "").strip()
            coren = request.form.get("novo_coren", "").strip()

            if nome and coren:
                profissionais_temporarios[nome] = coren
                mensagem = "Profissional temporária cadastrada com sucesso."

        # =========================
        # GERAR EVOLUÇÃO / CURATIVO
        # =========================
        if acao == "gerar_evolucao":

            tipo = request.form.get("tipo_registro")

            todos_profissionais = {**PROFISSIONAIS, **profissionais_temporarios}

            profissional = request.form.get("profissional", "")
            coren = todos_profissionais.get(profissional, "COREN não informado")

            # =====================================
            # 🏥 EVOLUÇÃO NORMAL
            # =====================================
            if tipo == "evolucao":

                h = request.form.get("horario", "")
                setor = request.form.get("setor", "")
                consciente = request.form.get("consciente")
                queixa = request.form.get("queixa")
                descricao = request.form.get("descricao_queixa", "")
                dor = request.form.get("dor", "")
                puncao = request.form.get("puncao")
                abocath = request.form.get("abocath", "")
                medicacao = request.form.get("medicacao")
                desfecho = request.form.get("desfecho")

                texto += f"{h} – Recebo paciente na {setor}.\n"

                if consciente == "Sim":
                    texto += "Paciente consciente e orientado.\n"
                else:
                    texto += "Paciente não consciente ou desorientado.\n"

                if queixa == "Sim":
                    texto += f"Paciente refere: {descricao}.\n"
                    if dor:
                        texto += f"Escala de dor: {dor}/10.\n"
                else:
                    texto += "Paciente sem queixas no momento.\n"

                if puncao == "Sim":
                    texto += f"Realizada punção venosa com abocath nº {abocath}.\n"
                else:
                    texto += "Não foi necessária punção venosa.\n"

                if medicacao == "Sim":
                    texto += "Medicação administrada conforme prescrição médica.\n"
                else:
                    texto += "Medicação não administrada.\n"

                if desfecho:
                    texto += f"{desfecho}.\n"

            # =====================================
            # 🩹 CURATIVO
            # =====================================
            elif tipo == "curativo":

                h = request.form.get("horario_curativo", "")
                tipo_curativo = request.form.get("tipo_curativo", "")
                qtd_gaze = request.form.get("qtd_gaze")
                alcool = request.form.get("alcool")
                clorexidina = request.form.get("clorexidina")
                sf = request.form.get("sf")
                pomada = request.form.get("pomada", "")
                outros = request.form.get("outros_materiais", "")
                exsudato = request.form.get("exsudato", "")
                aspecto = request.form.get("aspecto", "")

                texto += f"{h} – Realizado curativo.\n\n"
                texto += f"Tipo de curativo: {tipo_curativo}.\n"

                materiais = []

                if qtd_gaze and qtd_gaze.isdigit() and int(qtd_gaze) > 0:
                    materiais.append(f"{qtd_gaze} gaze(s)")

                if alcool:
                    materiais.append("Álcool 70%")

                if clorexidina:
                    materiais.append("Clorexidina")

                if sf:
                    materiais.append("SF 0,9%")

                if pomada.strip():
                    materiais.append(f"Pomada {pomada.strip()}")

                if outros.strip():
                    materiais.append(outros.strip())

                if materiais:
                    texto += "Utilizado: " + ", ".join(materiais) + ".\n"

                if aspecto:
                    texto += f"Aspecto da ferida: {aspecto}.\n"

                if exsudato:
                    texto += f"Exsudato {exsudato}.\n"

                texto += "Procedimento realizado com técnica asséptica.\n"

            # =====================================
            # PROFISSIONAL
            # =====================================
            texto += f"\n{profissional} – {coren}\n"
            texto += "Técnica de Enfermagem"

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

# ================= RODAR =================
if __name__ == "__main__":
    app.run(debug=True)