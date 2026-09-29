# Guia de estilo da V2

## Por que a V2 existe
Ver `docs/PARECER.md`. Resumo: a V1 (66 capítulos de ~90 palavras) conta a vida inteira em frases soltas, com 84% dos parágrafos de até 6 palavras, 257 reticências, um "hoje eu sei" atrás do outro e uma lição no fim de cada capítulo. A história é forte; a forma é de post. A V2 transforma resumo em cena sem perder a voz da Luciana.

## Voz
1. **Primeira pessoa, Luciana, olhando de 2024 para trás.** Tempo verbal: passado. O presente só na moldura (prólogo, cap. 26 e epílogo) e em comentários curtos da narradora adulta.
2. **A criança em cena, a adulta quase calada.** O comentário retrospectivo ("hoje eu sei", "hoje eu entendo", "sem perceber", "olhando pra trás") aparece no máximo **uma vez por parte**. A cena diz; a narradora não traduz.
3. **Oralidade com medida.** "A gente" pode, na fala e na narração. "Pra", "tá", "né" só no diálogo. A narração usa "para".
4. **Humor.** A V1 quase não tem, mas a vida tem: o vestido bufante, a franjinha de cuia, a família de doze, o pai de 1,65 que se achava galã, as filhas. Em toda parte, pelo menos uma cena em que o leitor ri.

## Regras de prosa
1. **Final de capítulo**: imagem, gesto ou fala. Nunca explicação. Teste: apague as últimas 1–3 linhas; se a cena ainda diz aquilo, deixe apagado.
2. **Ritmo**: varie o tamanho dos parágrafos. Linha curta isolada só em momento de impacto (meta: no máximo 25% dos parágrafos narrativos com até 6 palavras; a V1 tem 84%).
3. **Reticências**: só em fala interrompida ou hesitante. Nunca para partir uma frase da narração em duas ("E foi ali… / que eu percebi."). Meta: no máximo 2 por capítulo.
4. **Sem listas verticais**, sem 👉, sem "Cansada de X. Cansada de Y. Cansada de Z." Enumeração fica dentro do parágrafo, com vírgulas, e de preferência com coisas concretas.
5. **Fórmulas proibidas** (no máximo uma vez no livro inteiro, e com motivo): "Não era X. Era Y."; "Mas não era. Era..."; "Era sobre X"; "E foi ali que..."; "E, mais uma vez..."; "Eu percebi que..."; "Talvez..." em série; frase que resume o sentimento que a cena já mostrou.
6. **Palavras gastas**: "perceb*" no máximo 1 por capítulo; "dar conta" e "mais uma vez" no máximo 1 por capítulo cada (o `tools/metricas.py` conta).
7. **Mostre, não explique.** Nada de "eu estava me tornando invisível para mim mesma". Mostre a menina que diz "o meu não é nada" enquanto lava a louça da amiga.
8. **Diálogo**: seco, com subtexto. Em toda cena, alguém quer algo diferente do que a Luciana quer (a mãe quer a foto perfeita; o pai quer ser admirado; a amiga quer não falar; o marido não quer gravar curso de investimento).
9. **Os dois países pelos sentidos.** Brasil: o calor da escola, a Kombi do transporte, o feijão de domingo, a novena, o ônibus intermunicipal da faculdade. Japão: fábrica, bentō, zangyō, konbini às cinco da manhã, inverno de aquecedor a querosene, tsuyu, cigarras. Termos japoneses sem itálico; na primeira vez, uma aposição curta explica (ex.: "o zangyō, as horas extras").
10. **Precisão**: o autor trabalha com financiamento imobiliário para estrangeiros no Japão. Vistos, seguro de saúde, bancos, empréstimos, contratos de fábrica (empreiteira), regras da pandemia e procedimentos médicos precisam estar certos. Na dúvida, genérico e sinalizado no PR.

## Pessoas reais
- O pai não é vilão; a mãe não é santa; o marido não é salvador; as filhas não são adereço. A traição do pai e a tentativa de suicídio são contadas sem julgamento, sem descrição gráfica, sem cena de tribunal.
- As pessoas que diminuíram a Luciana ("Você tem sorte de ter seu esposo") não são caricaturas. Elas acreditam que estão ajudando, ou nem pensam no que dizem.
- A amiga da adolescência, a menina do bullying, colegas e parentes secundários usam pseudônimo até a Luciana decidir (lista em `docs/BIBLIA.md`).
- Fé: a Luciana reza e acredita; o livro trata a fé com respeito e sem sermão. O que o pai viu no monte não é explicado nem desmentido.

## Metas mensuráveis (`python3 tools/metricas.py`)
- Parágrafos narrativos de até 6 palavras: ≤ 25%.
- Listas verticais: 0.
- Reticências: ≤ 2 por capítulo.
- "perceb*", "dar conta", "mais uma vez", "hoje eu": ≤ 1 por capítulo cada.
- "menina elefante": zero fora do cap. 26 (o título do livro e o título da Parte VI não contam).

## Voz de referência
- Prólogo (A foto): moldura, fuso de doze horas, a terapeuta que espera, final em imagem.
- Cap. 1 (A franjinha): a criança em cena, humor, a mãe que quer uma coisa e a menina que quer outra.
