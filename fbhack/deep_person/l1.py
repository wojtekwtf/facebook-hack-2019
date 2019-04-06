# FOR WOJTEK ONLY (by M.A.C.)

ref = {
        "Therapist": {
            "cEXT": [0.5, 0.5],
            "cNEU": [0.5, 0.5],
            "cAGR": [0.9, 0.1],
            "cCON": [0.9, 0.1],
            "cOPN": [0.9, 0.1],
        },
        "Personal trainer": {
            "cEXT": [0.9, 0.1],
            "cNEU": [0.5, 0.5],
            "cAGR": [0.5, 0.5],
            "cCON": [0.9, 0.1],
            "cOPN": [0.9, 0.1],
        },
        "Software Developer": {
            "cEXT": [0.1, 0.9],
            "cNEU": [0.9, 0.1],
            "cAGR": [0.5, 0.5],
            "cCON": [0.9, 0.1],
            "cOPN": [0.1, 0.9],
        },
        "Chef": {
            "cEXT": [0.5, 0.5],
            "cNEU": [0.9, 0.1],
            "cAGR": [0.9, 0.1],
            "cCON": [0.9, 0.1],
            "cOPN": [0.5, 0.5],
        },
        "Sales Engineer": {
            "cEXT": [0.9, 0.1],
            "cNEU": [0.5, 0.5],
            "cAGR": [0.5, 0.5],
            "cCON": [0.9, 0.1],
            "cOPN": [0.9, 0.1],
        },
    }

darr = {"cEXT":[0.5,0.5], "cNEU":[0.5,0.5], "cARG":[0.5,0.5], "cCON":[0.5,0.5],
        "cOPN":[0.5,0.5]}

def l1_score(darr:dict, ref:dict):
    def __for_all(a:dict, b:dict):
        c = []
        for k in a:
                c.append(
                        abs(a[k][0] - b[k][0][0])
                    +   abs(a[k][1] - b[k][0][1])
                    )
        print(c)
        return c
    best = ""; best_l1 = +66666666
    for key in ref:
        l1 = sum(__for_all(ref[key], darr))
        if l1 < best_l1:
            best, best_l1 = key, l1
    return best
