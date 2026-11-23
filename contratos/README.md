# Contratos EASY HOUSE — 工事・サービス契約書

Modelo simplificado do contrato de obra/serviço (2 páginas) e um gerador que preenche o modelo a partir de um arquivo JSON.

- **Página 1:** dados do contrato, cliente, valores, obra, itens, observações e assinaturas.
- **Página 2:** 契約約款（第2版）em duas colunas e o aviso de クーリング・オフ em quadro vermelho.

## Arquivos

| Arquivo | Para quê |
|---|---|
| `modelo/工事・サービス契約書_簡易版_ひな形.docx` | Modelo em branco. Pode ser preenchido à mão no Word. |
| `gerar_contrato.py` | Gera um contrato preenchido a partir de um JSON. Só usa a biblioteca padrão do Python. |
| `exemplos/exemplo_carport.json` | Exemplo fictício com todos os campos. |

## Como gerar um contrato

1. Copie `exemplos/exemplo_carport.json` e troque os dados.
2. Rode:

```bash
python3 contratos/gerar_contrato.py dados_do_cliente.json contrato_cliente.docx
```

O script calcula sozinho o valor sem imposto e o imposto (10%) a partir do total com imposto. Ele avisa se a soma dos itens for diferente do total.

Não guarde neste repositório os JSON e contratos com dados reais de clientes.

## Campos do JSON

| Campo | Exemplo | Observação |
|---|---|---|
| `contrato.numero`, `contrato.data`, `contrato.responsavel` | `"2026-001"`, `"2026-12-01"`, `"山中"` | Vazio deixa o campo em branco. Datas sempre `AAAA-MM-DD`. |
| `cliente.furigana`, `cliente.nome` | `"ヤマダ　タロウ"`, `"山田　太郎"` | |
| `cliente.cep`, `cliente.endereco` | `"444-0241"`, `"愛知県…"` | O CEP vai na mesma linha do endereço. |
| `cliente.tel` | `"090-…"` | Só um telefone. |
| `local_obra.mesmo_endereco` | `true` / `false` | Se `false`, preencha `local_obra.endereco`. |
| `valor_total_com_imposto` | `1614140` | Número inteiro, sem vírgula. |
| `pagamento.metodo` | `["振込"]` | Opções: 現金, 振込, その他. |
| `pagamento.condicao` | `["着工前", "完了時"]` | Opções: 契約時, 着工前, 完了時, 分割, その他. |
| `pagamento.vencimento` | `"2027-01-31"` | |
| `garantia.tipo`, `garantia.periodo` | `["メーカー"]`, `"1年"` | Opções: 当社保証, メーカー, 保証なし. |
| `obra.nome`, `obra.especificacao` | texto, lista de linhas | Até 4 ou 5 linhas cabem na página 1. |
| `obra.inicio`, `obra.entrega` | `"2026-12-22"` | |
| `itens` | lista | Cada item: `nome`, `spec`, `qtd` (padrão `1式`), `valor` (número ou texto como `"（上記に含む）"`), `unitario` (opcional; padrão = `valor`). Valores com imposto. |
| `observacoes` | lista de linhas | Vão no quadro 備考. |

## Cuidados de layout

- Todas as linhas da página 1 têm altura fixa, para o Word não aumentar o espaço conforme a fonte instalada. Ao editar no Word, mantenha o espaçamento de linha como está.
- Textos com no mínimo 8 pontos, exigência do 特定商取引法 para vendas na casa do cliente.
- Com muitos itens ou muitas linhas de especificação, confira se a página 1 continua cabendo. Se não couber, resuma e use "詳細は見積書のとおり".

## Pendências do autor

- Data de criação (制定日) do 契約約款 第2版: em branco no modelo.
- O texto das cláusulas foi condensado da 第1版. Vale revisão de um 行政書士 antes do uso.
