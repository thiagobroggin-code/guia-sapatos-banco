# Guia de sapatos: como manter este banco

Este repositório guarda `banco.json`, o banco de calçados da aba "Guia de sapatos" do Guia Ambulatorial do Dr. Thiago Dutra Rodrigues (ortopedista, pé e tornozelo, São Paulo). O guia lê este arquivo direto do GitHub, uma vez por dia. Tudo o que for enviado para a branch `main` entra no guia sem revisão humana, então a validação abaixo é obrigatória.

## Como o guia usa o arquivo

- Lê as chaves `rev`, `serie` e `m`. As demais (`legenda`, `perfis`, `usos`, itens conferidos, `pendencias`) são documentação para quem mantém o banco.
- Só aceita uma versão nova se `serie` for maior que a atual. `serie` é um inteiro `AAAAMMDDnn` (data da revisão e número da rodada no dia).
- Cada modelo é `[marca, linha, versao, categoria, sexo, idade, finalidades, atributos, preco, nota, laboratorio]`; o 11º campo é opcional.
- Quando existe `laboratorio`, o guia recalcula os atributos pelas regras em `legenda.laboratorio.regras` e mantém do 8º campo só M, T, V, Q e F. Sem laboratório, valem os atributos de catálogo do 8º campo.
- O guia indica um modelo quando ele atende ao perfil de calçado da patologia (`perfis`) e ao uso escolhido (`usos`).

## Regras do banco

- Só entra modelo com venda confirmada no Brasil em pelo menos uma loja ou site oficial brasileiro, visto na própria revisão.
- `linha` é o nome da linha sem número de versão. `versao` só é preenchida quando a versão à venda no Brasil foi conferida na revisão.
- `nota` é curta e em linguagem para paciente.
- Atributo de catálogo precisa vir da ficha do fabricante ou de avaliação técnica independente. Sem confirmação, não marque.
- Não retire um modelo só por não achar em uma loja. Retire quando houver sinal claro de que saiu de linha no Brasil.
- Não altere `perfis`, `usos` nem as regras da legenda: são critérios clínicos do médico. Sugestões vão no relatório.
- Nunca use `<`, `>` ou a sequência `</` em nenhum texto.

## Medições de laboratório

Para cada tênis, abra a página do modelo em runrepeat.com (`runrepeat.com/marca-modelo-versao`, na versão mais nova que tiver análise) e leia a tabela-resumo do topo: Arch support, Shock absorption, Drop lab e Drop brand, Heel lab, Forefoot lab, Midsole softness, Width / fit, Toebox width, Stiffness, Torsional rigidity, Heel counter stiffness, Rocker, Removable insole, Orthotic friendly, Widths available, Weight lab. Grave nos códigos de `legenda.laboratorio`.

- Leia página por página, sem coleta em massa. Guarde só esses valores e o final do endereço.
- Se a versão medida for diferente da vendida no Brasil, registre no relatório.
- Havendo segunda fonte técnica independente (ficha do fabricante, Doctors of Running, RTINGS, sites brasileiros de teste), compare. Divergência que mude a indicação (drop, rigidez, largura da frente, estabilidade) vai no relatório; o dado de laboratório fica.

## Antes de enviar

1. Atualize `rev` (mês e ano por extenso) e `serie`.
2. Rode `python3 validar.py`. Ele confere o formato e os limites por rodada (10 inclusões, 5 retiradas) contra a versão publicada.
3. Se reprovar e não der para corrigir, não envie nada.
4. Grave o relatório da rodada em `relatorios/AAAA-MM.md`: incluídos, retirados, versões e medições atualizadas, divergências, o que não deu para conferir, sugestões ao médico e fontes.
5. Envie para `main`.

Para desfazer uma atualização ruim: restaure a versão anterior de `banco.json` pelo histórico e aumente `serie`.
