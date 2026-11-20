#!/usr/bin/env python3
"""Valida banco.json antes de publicar. Uso: python3 validar.py
Sai com código 1 e lista os erros se algo estiver fora do formato que o guia aceita."""
import json
import re
import subprocess
import sys

MAX_INCLUSOES = 10
MAX_RETIRADAS = 5
erros = []


def erro(msg):
    erros.append(msg)


def texto_ok(x, n):
    return isinstance(x, str) and len(x) <= n and not re.search(r"[<>]", x)


try:
    bruto = open("banco.json", encoding="utf-8").read()
    d = json.loads(bruto)
except Exception as e:  # noqa: BLE001
    print("ERRO: banco.json não é um JSON válido:", e)
    sys.exit(1)

if "</" in bruto:
    erro('o arquivo contém a sequência "</"')
if not (isinstance(d.get("rev"), str) and d["rev"] and len(d["rev"]) <= 40 and not re.search(r"[<>]", d["rev"])):
    erro('"rev" precisa ser um texto curto, por exemplo "dezembro de 2026"')
serie = d.get("serie")
if not (isinstance(serie, int) and not isinstance(serie, bool) and 2026111901 <= serie <= 2099123199):
    erro('"serie" precisa ser um inteiro no formato AAAAMMDDnn')
m = d.get("m")
if not isinstance(m, list) or not (40 <= len(m) <= 600):
    erro('"m" precisa ser uma lista com 40 a 600 modelos')
    m = []

leg = d.get("legenda", {})
letras = set(leg.get("atributos", {}).keys())
fins = set(leg.get("finalidades", {}).keys())
NUM = ["d", "db", "h", "f", "g", "rk", "in", "or"]
COD = ["a", "sh", "so", "fi", "to", "st", "tr", "hc"]
vistos = set()
for i, x in enumerate(m):
    onde = f"modelo {i + 1}"
    if not isinstance(x, list) or len(x) not in (10, 11):
        erro(f"{onde}: precisa ter 10 ou 11 campos")
        continue
    onde = f"{x[0]} {x[1]}"
    if not (texto_ok(x[0], 40) and x[0] and texto_ok(x[1], 80) and x[1]):
        erro(f"{onde}: marca ou linha inválida")
    if (x[0], x[1], x[5]) in vistos:
        erro(f"{onde}: modelo repetido")
    vistos.add((x[0], x[1], x[5]))
    if not texto_ok(x[2], 12):
        erro(f"{onde}: versão inválida")
    if x[3] not in ("T", "S", "D", "C", "B"):
        erro(f"{onde}: categoria inválida")
    if x[4] not in ("U", "F", "M"):
        erro(f"{onde}: sexo inválido")
    if x[5] not in ("A", "I", "AI"):
        erro(f"{onde}: idade inválida")
    if not (isinstance(x[6], str) and re.fullmatch(r"[a-z]{1,12}", x[6]) and set(x[6]) <= fins):
        erro(f"{onde}: finalidades fora da legenda")
    if not (isinstance(x[7], str) and re.fullmatch(r"[A-Z]{0,14}", x[7]) and set(x[7]) <= letras):
        erro(f"{onde}: atributos fora da legenda")
    if x[8] not in (1, 2, 3) or isinstance(x[8], bool):
        erro(f"{onde}: preço precisa ser 1, 2 ou 3")
    if not texto_ok(x[9], 140):
        erro(f"{onde}: nota longa demais ou com caracteres proibidos")
    if len(x) == 11 and x[10] is not None:
        b = x[10]
        if not isinstance(b, dict) or not (isinstance(b.get("u"), str) and re.fullmatch(r"[a-z0-9-]{3,80}", b["u"])):
            erro(f"{onde}: laboratório sem endereço válido em 'u'")
            continue
        for k in NUM:
            if b.get(k) is not None and not (isinstance(b[k], (int, float)) and not isinstance(b[k], bool) and 0 <= b[k] < 1000):
                erro(f"{onde}: laboratório, campo {k} precisa ser número")
        for k in COD:
            if b.get(k) is not None and not (isinstance(b[k], str) and re.fullmatch(r"[A-Z]", b[k])):
                erro(f"{onde}: laboratório, campo {k} precisa ser uma letra maiúscula")
        if b.get("w") is not None and not (isinstance(b["w"], str) and re.fullmatch(r"[nNWX]{1,4}", b["w"])):
            erro(f"{onde}: laboratório, campo w inválido")

# Comparação com a versão publicada (último commit)
try:
    ant = json.loads(subprocess.run(["git", "show", "HEAD:banco.json"], capture_output=True, text=True, check=True).stdout)
except Exception:  # noqa: BLE001
    ant = None
if ant and isinstance(ant.get("m"), list) and m:
    chave = lambda x: (x[0], x[1], x[5])  # noqa: E731
    antes, agora = {chave(x) for x in ant["m"]}, {chave(x) for x in m if isinstance(x, list) and len(x) >= 6}
    novas, fora = agora - antes, antes - agora
    mudou = json.dumps(ant.get("m"), sort_keys=True) != json.dumps(m, sort_keys=True) or ant.get("rev") != d.get("rev")
    if mudou and isinstance(serie, int) and isinstance(ant.get("serie"), int) and serie <= ant["serie"]:
        erro(f'"serie" ({serie}) precisa ser maior que a publicada ({ant["serie"]}), senão o guia ignora a atualização')
    if len(novas) > MAX_INCLUSOES:
        erro(f"{len(novas)} inclusões nesta rodada; o limite é {MAX_INCLUSOES}")
    if len(fora) > MAX_RETIRADAS:
        erro(f"{len(fora)} retiradas nesta rodada; o limite é {MAX_RETIRADAS}")
    print(f"Comparação com a versão publicada: {len(novas)} inclusões, {len(fora)} retiradas, total {len(m)}.")

if erros:
    print("REPROVADO:")
    for e in erros:
        print(" -", e)
    sys.exit(1)
print(f"APROVADO: {len(m)} modelos, {sum(1 for x in m if len(x) == 11 and x[10])} com medição de laboratório, serie {serie}.")
