from pathlib import Path
import json


def carregar_settings(caminho=Path(__file__).resolve().parent/ "settings.json"):
    with open(caminho,"r", encoding="utf-8") as arquivo:
        settings = json.load(arquivo)
    return settings