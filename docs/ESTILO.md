# Guia de estilo da V2

## Por que a V2 existe
O parecer sobre a V1 encontrou: 48 capítulos de ~350 palavras; 60% dos parágrafos narrativos com até 6 palavras; mais de 30 dos 50 blocos terminando numa máxima que explica a lição (do cap. 30 ao 45, dezesseis seguidos); 48 listas verticais; 42 ocorrências de "perceber". O conjunto é uma cadência hoje muito associada a texto gerado por IA — fatal num livro sobre presença e autenticidade. Estruturalmente: clímax em 62% do livro, três finais, cronologia quebrada na Parte VI, conceito definido três vezes, mentores demais, personagens secundários sem desejo próprio.

## Regras de prosa
1. **Final de capítulo**: imagem, gesto ou fala. Nunca explicação. Teste: apague as últimas 1–3 linhas; se a cena ainda diz aquilo, deixe apagado.
2. **Ritmo**: varie o tamanho dos parágrafos. Linha curta isolada só em momento de impacto (meta: no máximo 25% dos parágrafos narrativos com até 6 palavras).
3. **Sem listas verticais.** Enumeração fica dentro do parágrafo, com vírgulas. Exceções já usadas: o "Compensava..." do prólogo e as placas do cap. 10.
4. **Fórmulas proibidas** (no máximo uma vez no livro inteiro, e com motivo): "Não era X. Era Y."; "Não A. Não B. Não C."; "Miguel percebeu que..."; "Talvez..." em série; frase que resume o sentimento que a cena já mostrou.
5. **Mostre, não explique.** O narrador não interpreta a cena para o leitor.
6. **Diálogo**: seco, com humor e subtexto. Mentores falam pouco e deixam o Miguel chegar lá. Em toda cena, alguém quer algo diferente do que ele quer.
7. **Japão pelos sentidos e pelo calendário**: ume em fevereiro, ervas de primavera em março, tsuyu em junho, cigarras no verão, figos em setembro, kinmokusei em outubro, aquecedor a querosene no inverno. Objetos e ofícios: genkan, konbini, kissaten, hanko, placa amarela de kei car, hokenjo, zangyō.
8. **Ponto de vista**: terceira pessoa próxima do Miguel, exceto os capítulos narrados por outra pessoa (cap. 5 Clara; cap. 12 Maya).
9. **Precisão técnica**: documentos, bancos, prazos e contratos específicos quando o autor reconheceria (gensen, kazei, jūminhyō, pedido de compra, 35 anos, taxa variável); genéricos quando houver risco de erro.
10. **Humor**: o livro é leve apesar do tema. Crianças e o Mori são as principais fontes.

## Metas mensuráveis (`python3 tools/metricas.py`)
- Parágrafos narrativos de até 6 palavras: ≤ 25% (V1: 60%; V2 até agora: 19–23%).
- Listas verticais: 0.
- "perceb*": no máximo 1 por capítulo.
- O cap. 10 aparece sinalizado de propósito (placas e perguntas curtas do Mori; "Perceber é trabalho" é tema do capítulo).

## Voz de referência
- Cap. 3 (Mateo): relógio correndo, tentação real, subtexto, final em fala.
- Cap. 11 (O batismo): cena pública, humor das crianças, imagem final feita de gestos.
