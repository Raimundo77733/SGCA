from pathlib import Path
import json

PASTA_SETTINGS = Path(__file__).resolve().parent / "settings"


def carregar_settings(caminho=None):
    if caminho is None:
        caminho = PASTA_SETTINGS / "settings.json"
    with open(caminho, encoding="utf-8") as arquivo:
        settings = json.load(arquivo)
    return settings
