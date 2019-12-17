from app import app


@app.template_filter("listify")
def listify(list):
    return f"{list[0]}{', '.join(list[1:-1])} and {list[-1]}"
