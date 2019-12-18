from app import app


@app.template_filter("listify")
def listify(list, attr=None, extract_attr=False):
    if extract_attr:
        list = [l.__getattribute__(attr) for l in list]
    if len(list) == 1:
        return str(list[0])
    if len(list) == 0:
        return ""
    return f"{list[0]}{', '.join(list[1:-1])} and {list[-1]}"


@app.template_filter("getattr")
def getattr(obj, key):
    return obj.__getattribute__(key)
