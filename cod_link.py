@app.route("/link",methods=["POST"])

def link():
    if request.method == "POST":
        login = request.form.to_dict()
        
        nome = login["id"]
        senha = login["pass"]
        
        client = Client(f"{nome}", 
        f"{senha}", 
        "https://sandbox.belvo.co")

        instituicoes = []

        [instituicoes.append(x) for x in client.Institutions.list()]

        link = []

        [link.append(x) for x in client.Links.list()]
        
        return render_template("link.html",id=nome,senha=senha,links = link,instituicoes=instituicoes,
    numero_instituicoes = len(instituicoes),numero_links=len(link))