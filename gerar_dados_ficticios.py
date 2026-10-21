"""Gera os dados FICTÍCIOS da demonstração (pessoas, bancos e lojas inventados).

Nada aqui vem de dados reais. Uso: python3 gerar_dados_ficticios.py
Cria dados/painel-AAAA-MM.json, meses.json, resumo.json e categorias.json.
"""
import json
import random
from pathlib import Path

DADOS = Path(__file__).parent / "dados"
MESES = ["2026-08", "2026-09", "2026-10", "2026-11"]
HOJE = "2026-10-21"
BIA = "Bia"
CONTA, PAY, INTER, GLOBAL, CARTAO = "Santander", "Nubank", "Inter", "Revolut", "Cartão Nubank"
FLEX = CONTA   # o benefício cai na conta do salário
TAG = "viagem lisboa"
METAS = {"renda_propria_base": 6000, "gasto_total": 5600, "gasto_fixo": 2800, "gasto_variavel": 2800, "guardar": 600}
ORIGEM = "Dados fictícios de demonstração. Renda própria de R$ 6.000 (sem contar ajuda da família): gastos até R$ 5.600 (fixos até R$ 2.800 e variáveis até R$ 2.800) e investir pelo menos R$ 600 (10%). Ajustáveis"


def r2(x):
    return round(x + 0.0, 2)


class Mes:
    def __init__(self, mes, semente):
        self.mes, self.rnd, self.n, self.linhas = mes, random.Random(semente), 0, []

    def linha(self, dia, descricao, conta, modalidade, tipo, valor, grupo, categoria, nome_original="", **extra):
        self.n += 1
        mes = self.mes if dia > 0 else self.mes
        l = {"id": f"demo-{self.mes}-{self.n:03d}", "data": f"{mes}-{abs(dia):02d}", "conta": conta, "valor": r2(valor), "modalidade": modalidade, "tipo": tipo,
             "nome_original": nome_original or descricao.upper(), "ids_extras": [], "tags": [], "descricao": descricao, "grupo": grupo, "categoria": categoria}
        l.update(extra)
        self.linhas.append(l)
        return l

    def gasto(self, dia, descricao, categoria, valor, conta=CARTAO, modalidade="Crédito", tipo="Variável", dividido=False, tags=None, nome_original="", **extra):
        valor = abs(valor)
        if dividido:
            meio = r2(valor / 2)
            return self.linha(dia, descricao, conta, modalidade, tipo, -meio, "gasto", categoria, nome_original, bruto=-r2(valor), a_receber=meio, splitwise=True,
                              nota=f"R$ {valor:.2f} no banco, dividido com {BIA}. Sua parte R$ {meio:.2f}, a receber R$ {meio:.2f}".replace(".", ","), tags=tags or [], **extra)
        return self.linha(dia, descricao, conta, modalidade, tipo, -valor, "gasto", categoria, nome_original, tags=tags or [], **extra)


def construir(mes, k):
    m = Mes(mes, 100 + k)
    rnd = m.rnd
    completo = mes != "2026-11"
    sufixo = {"2026-08": "ago", "2026-09": "set", "2026-10": "out", "2026-11": "nov"}[mes]
    # ---------- entradas ----------
    if completo:
        m.linha(5, "Salário", CONTA, "Salário", "Fixo", 5200, "receita", "Salário", "EMPRESA EXEMPLO LTDA SALARIO")
        m.linha(1, "Benefício Flex", FLEX, "Benefício", "Fixo", 700, "receita", "Benefício Flex", "BENEFICIO FLEX CREDITO")
        extra = {"2026-08": 800, "2026-09": 1200, "2026-10": 950}[mes]
        m.linha(12, "Cliente: site da padaria", INTER, "PIX", "Eventual", extra, "receita", "Trabalho extra (sites)", "PIX RECEBIDO")
        ajuda = {"2026-08": 1500, "2026-09": 1000, "2026-10": 800}[mes]
        m.linha(8, "Venda do notebook", PAY, "PIX", "Eventual", ajuda, "receita", "Venda notebook", "PIX RECEBIDO COMPRADOR")
        if mes == "2026-09":
            m.linha(20, "Presente da família", PAY, "PIX", "Eventual", 200, "receita", "Presente da família", "PIX RECEBIDO")
        for d in range(1, 11):
            m.linha(d * 2, "Rendimento da reserva", PAY, "CDI", "Eventual", r2(3.4 + rnd.random() * 2.4), "rendimento", "Rendimentos", "RENDIMENTO DIARIO")
        m.linha(14, "Transferência para a Conta Global", PAY, "PIX", "", -300, "interno", "Entre contas", "PIX ENVIADO", nota="Movimento entre as suas contas (viagem)")
        m.linha(15, "Acerto com a Bia (Splitwise)", PAY, "PIX", "", 380 + k * 40, "acerto", "Acerto", "PIX RECEBIDO BIA", nota="Acerto mensal com a Bia: fora dos gastos e das entradas")
    # ---------- fixos ----------
    if completo:
        m.gasto(6, "Aluguel", "Moradia", 2400, PAY, "Boleto", "Fixo", dividido=True, nome_original="IMOBILIARIA EXEMPLO ALUGUEL")
        m.gasto(8, "Condomínio", "Contas da casa", 520, PAY, "Boleto", "Fixo", dividido=True, nome_original="CONDOMINIO RESIDENCIAL")
        m.gasto(15, "Energia", "Contas da casa", r2(170 + rnd.random() * 40), PAY, "Boleto", "Fixo", dividido=True, nome_original="DISTRIBUIDORA ENERGIA")
        m.gasto(17, "Internet", "Contas da casa", 119.90, PAY, "Boleto", "Fixo", dividido=True, nome_original="FIBRA NET 500MB")
        m.gasto(10, "Plano de celular", "Celular", 69.90, CARTAO, "Crédito", "Fixo", nome_original="OPERADORA MOVEL")
        m.gasto(11, "Streaming de vídeo", "Assinaturas", 39.90, CARTAO, "Crédito", "Fixo", nome_original="STREAMFLIX")
        m.gasto(11, "Streaming de música", "Assinaturas", 21.90, CARTAO, "Crédito", "Fixo", nome_original="MUSICAPLAY")
        m.gasto(5, "Academia Plus", "Academia", 119.90, CARTAO, "Crédito", "Fixo", nome_original="ACADEMIA PLUS MENSAL")
    # ---------- variáveis ----------
    lojas = {
        "Mercado": ["Mercado Bom Preço", "Supermercado Central", "Mercadinho da Esquina", "Hortifruti Verde"],
        "Restaurantes": ["Cantina Bella Massa", "Sushi do Porto", "Hamburgueria Brasa", "Bistrô da Praça"],
        "Delivery": ["Entrega Rápida", "Pizza Express"],
        "Rolês": ["Cinema Plaza", "Bar do Zé", "Show na Arena"],
    }
    def vezes(cat, qtd, faixa, dividir=0.5):
        for i in range(qtd):
            nome = rnd.choice(lojas[cat])
            valor = r2(faixa[0] + rnd.random() * (faixa[1] - faixa[0]))
            m.gasto(rnd.randint(1, 28), nome, cat, valor, CARTAO if rnd.random() < .8 else PAY, "Crédito", dividido=rnd.random() < dividir, nome_original=nome.upper() + " SAO PAULO BRA")
    qtd = 6 if completo else 3
    vezes("Mercado", qtd, (45, 260)); vezes("Restaurantes", qtd - 1, (38, 160)); vezes("Delivery", 3, (28, 72), .3); vezes("Rolês", 2, (40, 180))
    for i in range(7 if completo else 3):
        m.gasto(rnd.randint(1, 28), "Corrida por aplicativo", "Transporte", r2(14 + rnd.random() * 24), CARTAO, nome_original="APP CORRIDA")
    m.gasto(9, "Combustível", "Transporte", r2(170 + rnd.random() * 40), CARTAO, nome_original="POSTO ESTRADA")
    m.gasto(19, "Ração e petiscos", "Pet", 142.50, CARTAO, dividido=True, nome_original="PETSHOP AMIGO FIEL")
    m.gasto(21, "Farmácia", "Drogaria", r2(40 + rnd.random() * 60), CARTAO, nome_original="FARMACIA SAUDE")
    m.gasto(23, "Barbearia", "Estética e higiene", 55, PAY, "PIX", nome_original="PIX BARBEARIA CLASSICA")
    compra = {"2026-08": ("Tênis de corrida (2/6)", 189.90), "2026-09": ("Tênis de corrida (3/6)", 189.90), "2026-10": ("Tênis de corrida (4/6)", 189.90), "2026-11": ("Tênis de corrida (5/6)", 189.90)}[mes]
    m.gasto(3, compra[0], "Compras", compra[1], nome_original="LOJA ESPORTE 0" + str(k + 2) + "/06")
    if completo:
        m.gasto(18, "Presente de aniversário", "Presentes", r2(90 + rnd.random() * 60), CARTAO, nome_original="LOJA PRESENTES")
    # viagem (tag)
    viagem = {"2026-08": ("Passagem para Lisboa (1/10)", 410.0), "2026-09": ("Passagem para Lisboa (2/10)", 410.0), "2026-10": ("Passagem para Lisboa (3/10)", 410.0), "2026-11": ("Passagem para Lisboa (4/10)", 410.0)}[mes]
    m.gasto(2, viagem[0], "Viagem", viagem[1], CARTAO, tags=[TAG], nome_original="COMPANHIA AEREA 0" + str(k + 1) + "/10")
    if mes == "2026-10":
        m.gasto(7, "Seguro viagem", "Viagem", 232.0, PAY, "PIX", tags=[TAG], nome_original="PIX SEGURADORA VIAGEM")
    # Bia pagou (Splitwise)
    if completo:
        m.linha(22, "Jantar de sexta", "Splitwise", "Pago por " + BIA, "Variável", -r2(54 + k * 3), "gasto", "Restaurantes", "JANTAR DE SEXTA", a_pagar=r2(54 + k * 3), splitwise=True,
                nota=f"{BIA} pagou R$ {2 * (54 + k * 3):.2f}. Sua parte R$ {54 + k * 3:.2f} abate do a receber".replace(".", ","), tags=[])
    # ---------- pendências ----------
    pend = {"falta_no_splitwise": [], "sem_par_no_banco": [], "duvidas": []}
    for i in range(3 if mes == "2026-08" else 4 if mes == "2026-09" else 2 if mes == "2026-10" else 0):
        grupo, valor = ("receita", 85 + i * 20) if i == 1 else ("gasto", -r2(30 + rnd.random() * 120))
        pista = ["PIX para pessoa física sem nome no extrato", "Entrada sem identificação do remetente", "Compra sem nome da loja no cartão", "PIX para empresa que não reconheço"][i % 4]
        l = m.linha(rnd.randint(2, 27), "PIX sem identificação" if i % 2 == 0 else "Compra sem nome da loja", PAY if i % 2 == 0 else CARTAO, "PIX" if i % 2 == 0 else "Crédito", "", valor, grupo, "Dúvida", "TRANSFERENCIAS", sugestao=pista)
        pend["duvidas"].append(l)
    for l in [x for x in m.linhas if x["grupo"] == "gasto" and x["categoria"] in ("Mercado", "Restaurantes") and not x.get("splitwise")][:(4 if completo else 3)]:
        l["nota"] = "Parece dividido e não está no Splitwise"
        pend["falta_no_splitwise"].append(l)
    for i in range(2 if mes in ("2026-08", "2026-09") else 1 if mes == "2026-10" else 0):
        pend["sem_par_no_banco"].append({"splitwise_id": 9000000 + k * 10 + i, "data": f"{mes}-{10 + i * 7:02d}", "descricao": ["Feira de sábado", "Lanche com amigos", "Conserto de bicicleta"][i], "valor": [48.0, 60.0, 90.0][i], "minha_parte": [24.0, 30.0, 45.0][i], "categoria": ["Mercado", "Restaurantes", "Serviços"][i]})
    # ---------- terceiros ----------
    terceiros = []
    if completo:
        base = [("Carlos Mendes", "Academia Plus", 149.99, "2026-10-08" if mes != "2026-08" else "2026-09-10"), ("Júlia Rocha", "Academia Plus", 149.99, "2026-10-08" if mes != "2026-08" else None), ("Pedro Alves", "Academia Plus", 180.63, None)]
        for nome, desc, valor, devolveu in base:
            dia = 11
            prazo = f"{mes[:4]}-{int(mes[5:]) + (0 if mes != '2026-12' else 0):02d}-10" if False else f"{mes}-10"
            terceiros.append({"data": f"{mes}-{dia:02d}", "pessoa": nome, "valor": valor, "descricao": desc, "prazo": prazo, "reembolsado_em": devolveu})
            m.linha(dia, desc, CARTAO, "Crédito", "", -valor, "terceiros", "De terceiros", desc.upper(), nota=f"De {nome}. " + ("Já reembolsou" if devolveu else "Reembolso esperado até 10/" + mes[5:]))
    return m, pend, terceiros


def montar(mes, k):
    m, pend, terceiros = construir(mes, k)
    L = m.linhas
    gastos = [l for l in L if l["grupo"] == "gasto" and l["categoria"] != "Dúvida"]
    receitas = [l for l in L if l["grupo"] == "receita" and l["categoria"] != "Dúvida"]
    soma = lambda ls: r2(sum(x["valor"] for x in ls))
    fixo, var = -soma([l for l in gastos if l["tipo"] == "Fixo"]), -soma([l for l in gastos if l["tipo"] != "Fixo"])
    por_cat, rec_cat = {}, {}
    for l in gastos:
        por_cat[l["categoria"]] = r2(por_cat.get(l["categoria"], 0) - l["valor"])
    for l in receitas:
        rec_cat[l["categoria"]] = r2(rec_cat.get(l["categoria"], 0) + l["valor"])
    t = {"receita_fixa": soma([l for l in receitas if l["tipo"] == "Fixo"]), "receita_eventual": soma([l for l in receitas if l["tipo"] != "Fixo"]), "rendimentos": soma([l for l in L if l["grupo"] == "rendimento"]),
         "gasto_total": r2(fixo + var), "gasto_fixo": r2(fixo), "gasto_variavel": r2(var), "a_receber_mes": r2(sum(l.get("a_receber", 0) for l in gastos)), "a_pagar_mes": r2(sum(l.get("a_pagar", 0) for l in gastos)),
         "a_receber_outros_mes": 0, "duvida_saida": -soma([d for d in pend["duvidas"] if d["valor"] < 0]), "duvida_entrada": soma([d for d in pend["duvidas"] if d["valor"] > 0]),
         "a_receber_terceiros": r2(sum(x["valor"] for x in terceiros if not x["reembolsado_em"]))}
    t["receitas_total"] = r2(t["receita_fixa"] + t["receita_eventual"] + t["rendimentos"])
    t["ajuda_familia"] = r2(sum(v for c, v in rec_cat.items() if c in ("Ajuda da família", "Presente da família")))
    t["renda_propria"] = r2(t["receitas_total"] - t["ajuda_familia"])
    t["sobra_sem_ajuda"] = r2(t["renda_propria"] - t["gasto_total"])
    t["movimentado"] = r2(t["gasto_total"] - t["a_pagar_mes"] + t["a_receber_mes"] + t["a_receber_outros_mes"] + sum(x["valor"] for x in terceiros))
    t["balanco"] = r2(t["receitas_total"] - t["gasto_total"])
    tag = [l for l in gastos if TAG in l["tags"]]
    t["viagem_tag"] = -soma(tag); t["viagem_tag_n"] = len(tag)
    cartao = [l for l in gastos if l["conta"] == CARTAO]
    bruta = r2(-sum(l.get("bruto", l["valor"]) for l in cartao) + sum(x["valor"] for x in terceiros))
    ult = {"2026-08": "08", "2026-09": "09", "2026-10": "10", "2026-11": "11"}[mes]
    contas = [{"nome": CONTA, "tipo": "BANK", "saldo": 1284.5, "atualizado_em": HOJE}, {"nome": PAY, "tipo": "BANK", "saldo": 5680.0, "atualizado_em": HOJE},
              {"nome": INTER, "tipo": "BANK", "saldo": 3150.0, "atualizado_em": HOJE},
              {"nome": GLOBAL, "tipo": "MANUAL", "saldo": 640.0, "atualizado_em": HOJE, "nota": "Convertendo em euro para a viagem (informado por você)"}]
    datas = ["2026-07-31", "2026-08-31", "2026-09-30", "2026-10-20", "2026-10-21"]
    # patrimônio de R$ 70.000 em 21/10/2026
    ativos = [("Reserva Nubank (CDI)", "CDI", PAY, None, 8000.0, 66.4, True, [7300, 7550, 7800, 8000, 8000]),
              ("CDB Inter (4 aplicações)", "CDI", "Inter (automático)", 33900.0, 36400.0, None, True, [32800, 33900, 35300, 36350, 36400]),
              ("Fundo Renda Fixa Plus", "Fundos de investimento", "Inter (automático)", 13800.0, 14600.0, None, True, [13700, 13950, 14350, 14590, 14600]),
              ("Bitcoin (0,0130 BTC)", "Cripto", "Inter", 3800.0, 4150.0, None, False, [4350, 3980, 4420, 4140, 4150]),
              ("Ações dos EUA (US$ 1.200)", "Ações EUA", "Inter Global", 5900.0, 6850.0, None, False, [5900, 6150, 6480, 6830, 6850])]
    inv = {"teste": False, "aviso": "Valores fictícios de demonstração.", "atualizado_em": "2026-10-20", "caixa": 680.0, "aportes_mes": [],
           "ativos": [{"nome": n, "classe": c, "instituicao": i, "aplicado": ap, "atual": at, "rendimento_mes": rm, "real": True, **({"automatico": True} if au else {})} for n, c, i, ap, at, rm, au, _ in ativos],
           "historico": {n: dict(zip(datas, [float(x) for x in h])) for n, *_, h in ativos}}
    return {"mes": mes, "gerado_em": HOJE, "metas": METAS, "metas_origem": ORIGEM, "reserva_emergencia": {"meses_de_cobertura": 5, "meses_na_media": 3, "classes": ["CDI"]},
            "totais": t, "splitwise_saldos": {BIA: 214.5}, "por_categoria": dict(sorted(por_cat.items(), key=lambda kv: -kv[1])), "receitas_por_categoria": dict(sorted(rec_cat.items(), key=lambda kv: -kv[1])),
            "contas": contas,
            "cartao_aurora": {"conectado": True, "vencimento_dia": 10, "finais_usuario": ["4821"], "outros_cartoes_ignorados": {"1033": 12, "7720": 6}, "fatura_bruta": bruta, "terceiros": r2(sum(x["valor"] for x in terceiros)),
                              "minha_parte": r2(-sum(l["valor"] for l in cartao)), "a_receber": r2(sum(l.get("a_receber", 0) for l in cartao)), "compras": len(cartao), "fatura_total_cartao": bruta,
                              "conferencia_fatura": {"oficial": bruta, "soma_lancamentos": bruta, "completa": True}, "vencimento": f"{mes}-10"},
            "terceiros": terceiros, "investimentos": inv, "pendentes": pend, "movimentacoes": L}


def main():
    DADOS.mkdir(exist_ok=True)
    resumo, cats_g, cats_r = [], set(), set()
    for k, mes in enumerate(MESES):
        p = montar(mes, k)
        p["cartao"] = p.pop("cartao_aurora")
        (DADOS / f"painel-{mes}.json").write_text(json.dumps(p, indent=1, ensure_ascii=False))
        resumo.append({"mes": mes, "totais": p["totais"], "duvidas": len(p["pendentes"]["duvidas"])})
        cats_g |= set(p["por_categoria"]); cats_r |= set(p["receitas_por_categoria"])
        print(mes, "gasto", p["totais"]["gasto_total"], "(fixo", p["totais"]["gasto_fixo"], "var", p["totais"]["gasto_variavel"], ") receitas", p["totais"]["receitas_total"], "balanço", p["totais"]["balanco"])
    (DADOS / "meses.json").write_text(json.dumps(sorted(MESES, reverse=True)))
    (DADOS / "resumo.json").write_text(json.dumps(resumo, ensure_ascii=False))
    (DADOS / "categorias.json").write_text(json.dumps({"gasto": sorted(cats_g | {"Delivery", "Transporte", "Outros"}), "receita": sorted(cats_r | {"Venda"})}, ensure_ascii=False))


if __name__ == "__main__":
    main()
