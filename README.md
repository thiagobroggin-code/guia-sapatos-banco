# Guia de sapatos: banco de modelos

Banco de calçados usado pela aba "Guia de sapatos" do Guia Ambulatorial (área médica com login de thiagodutrarodrigues.com.br).

- `banco.json` é o arquivo que o guia lê, uma vez por dia.
- O guia só aceita uma versão nova se o campo `serie` (inteiro no formato AAAAMMDDnn) for maior que o atual e o formato passar na validação.
- As chaves `legenda`, `perfis` e `usos` dentro do arquivo explicam os códigos.
- O arquivo é revisado automaticamente todo mês. O histórico deste repositório guarda todas as versões.

Não há dados de pacientes neste repositório.
