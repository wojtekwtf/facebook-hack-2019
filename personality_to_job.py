import numpy as np
import math


def personality_to_job(personality_dict):

    professions = {
        "Therapist": {
            "cEXT": np.array([0.5, 0.5]),
            "cNEU": np.array([0.5, 0.5]),
            "cARG": np.array([0.9, 0.1]),
            "cCON": np.array([0.9, 0.1]),
            "cOPN": np.array([0.9, 0.1]),
        },
        "Personal trainer": {
            "cEXT": np.array([0.9, 0.1]),
            "cNEU": np.array([0.5, 0.5]),
            "cARG": np.array([0.5, 0.5]),
            "cCON": np.array([0.9, 0.1]),
            "cOPN": np.array([0.9, 0.1]),
        },
        "Software Developer": {
            "cEXT": np.array([0.1, 0.9]),
            "cNEU": np.array([0.9, 0.1]),
            "cARG": np.array([0.5, 0.5]),
            "cCON": np.array([0.9, 0.1]),
            "cOPN": np.array([0.1, 0.9]),
        },
        "Chef": {
            "cEXT": np.array([0.5, 0.5]),
            "cNEU": np.array([0.9, 0.1]),
            "cARG": np.array([0.9, 0.1]),
            "cCON": np.array([0.9, 0.1]),
            "cOPN": np.array([0.5, 0.5]),
        },
        "Sales Engineer": {
            "cEXT": np.array([0.9, 0.1]),
            "cNEU": np.array([0.5, 0.5]),
            "cARG": np.array([0.5, 0.5]),
            "cCON": np.array([0.9, 0.1]),
            "cOPN": np.array([0.9, 0.1]),
        },
    }

    scores = []
    for profession_name, profession_values in professions.items():
        score = 0
        for personalty_name, personalty_values in personality_dict.items():
            temp = 0
            temp += profession_values[personalty_name][0] - personalty_values[0]
            temp += profession_values[personalty_name][1] - personalty_values[1]
            temp = temp ** 2
            score += temp

        score = math.sqrt(score)
        scores.append((profession_name, score))

    return min(scores, key=lambda x: x[1])

if __name__ == "__main__":
    example = {
        "cEXT": np.array([0.2, 0.8]),
        "cNEU": np.array([0.1, 0.9]),
        "cARG": np.array([0.4, 0.6]),
        "cCON": np.array([0.3, 0.7]),
        "cOPN": np.array([0.23, 0.77]),
    }

    print(personality_to_job(example))
