# Dashboard financeira (demonstração)

Painel de finanças pessoais que junta, numa tela só, o que entra, o que sai, quanto sobrou, quanto falta pagar e o que ainda precisa da sua atenção.

> **Esta é uma demonstração.** Todos os nomes, valores, bancos, lojas e pessoas são **fictícios**, gerados pelo script `gerar_dados_ficticios.py`. Nada aqui vem de contas reais. As ações da tela (classificar uma despesa, “já lancei”, atualizar dados) são **simuladas**.

**Ver a demonstração:** https://fricheiago-ux.github.io/dashboard-financeira-demo/

## O que ela faz

- **Visão do mês**: balanço, entradas, gastos (só a sua parte), patrimônio e navegação entre meses.
- **Entradas por categoria** (rosca) e **saídas fixas x variáveis** (rosca); clicar numa fatia filtra a lista.
- **Limites do mês**: gasto total, gastos fixos, gastos variáveis e quanto sobrou para investir, com barras animadas e cores por estado (dentro, perto, passou).
- **Divisão com a parceira (Splitwise)**: quem adiantou o quê, saldo do acerto e quem ainda deve devolver (com prazo e atraso).
- **Tarefas pendentes** em formato de checklist: mapear gastos que ninguém identificou, lançar gastos no Splitwise (botão “já lancei” que confere), cobrar devedores e conferir lançamentos sem par no banco. Ao concluir, a tarefa risca, some e as de baixo sobem. Quando acaba, aparece o parabéns.
- **Bancos, cartão e fatura**: saldos, entradas e saídas por conta, fatura conferida com o total oficial.
- **Patrimônio**: reserva de emergência (meta de meses do custo de vida e a partir de quanto dá para começar a investir com mais risco), rendimento de cada ativo e evolução do total.
- **Movimentações** do mês, com busca, filtros (fixos, variáveis, divididos, dúvidas) e nomes amigáveis.
- Visual próprio: fundo quadriculado, números animados, blur ao rolar, tema dourado.

## Como abrir no computador

Precisa só de um servidor de arquivos (não há instalação):

```bash
python3 -m http.server 8000
```

Depois abra http://localhost:8000.

## Gerar os dados fictícios de novo

```bash
python3 gerar_dados_ficticios.py
```

## Créditos

Veja [LICENCAS.md](LICENCAS.md).

© Todos os direitos reservados ao autor. Código e imagens deste repositório são mostrados apenas para avaliação.
