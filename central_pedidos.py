Segue código do arquivo central_pedidos.py, realizado no Visual Studio Code. No fim do código estará o resultado obtido.

import threading
import time

principal = {
    "online" : True,
    "estoque" : 10
}

replica = {
    "online" : True,
    "estoque" : 10
}

MAXIMO_SIMULTANEO = 3

semaforo = threading.Semaphore(MAXIMO_SIMULTANEO)
trava = threading.Lock()

pedidos_confirmados = []

def processar_pedido(numero):
    with semaforo:
        time.sleep(0.1)

        with trava:
            if principal["estoque"] > 0:
                principal["estoque"] -= 1
                pedidos_confirmados.append(numero)

def sincronizar():
    replica["estoque"] = replica["estoque"]

def consultar_estoque():
    if principal["online"]:
        return (
            "PRINCIPAL",
            principal["estoque"]
        )

    if principal["online"]:
        return (
            "REPLICA",
            replica["estoque"]
        )
    return "INDISPONIVEL", None

print("=== Central de Pedidos ===")

print(
    "Limite simultaneo: ",
    MAXIMO_SIMULTANEO
)

print(
    "Estoque inicial",
    principal["estoque"]
)

trabalhadores = [
    threading.Thread(
        target=processar_pedido,
        args=(numero,)
    )
    for numero in [101, 102, 103]
]

for trabalhador in trabalhadores:
    trabalhador.start()

for trabalhador in trabalhadores:
    trabalhador.join()

print(
"Pedidos confirmados:",
sorted(pedidos_confirmados)
)

print(
    "Estoque principal:",
    principal["estoque"]
)

print(
    "Replica antes:",
    replica["estoque"]
)

sincronizar()

print(
    "Replica depois:",
    replica["estoque"]
)

principal["online"] = False

nome, estoque = consultar_estoque()

print(
    "Consulta apos falha:",
    nome,
    estoque
)


Resultado:

 py central_pedidos.py
=== Central de Pedidos ===
Limite simultaneo:  3
Estoque inicial 10
Pedidos confirmados: [101, 102, 103]
Estoque principal: 7
Replica antes: 10
Replica depois: 10
Consulta apos falha: INDISPONIVEL None
