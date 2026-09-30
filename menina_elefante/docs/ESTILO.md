# Guia de estilo (V3)

## V3 (30/09/2026): o que mudou, por decisão da autora
A autora pediu um livro com linha cronológica clara, estrutura de jornada de heroína (luta, sofre, acha que perdeu, se levanta, descobre quem é, vence, e a história continua) e, no espírito do *Plenitude*, de Camila Vieira, uma conversa com quem lê no fim de cada capítulo. Esta seção vale por cima das regras da V2 abaixo sempre que houver conflito.

- **Duas vozes em cada capítulo.** A **cena** (as regras da V2 abaixo continuam valendo para ela) e o **"Para você"**, depois da marca `§`: a Luciana de 2026 falando com quem lê. O "Para você" segue o espírito do *Plenitude* (testemunho, reflexão, pergunta), sem copiar nenhuma frase do livro da Camila Vieira.
- **Forma do "Para você"**: 130–220 palavras (o do fim do livro pode chegar a ~240). Começa por um objeto ou uma fala da cena; nomeia a mentira que a menina aprendeu ali e a verdade que a mulher sabe hoje; termina numa pergunta ao leitor, marcada com `? ` (sai em itálico). Pode usar "você", Deus, fé e o vocabulário dela ("consciência", "identidade", "nova versão", "vida extraordinária"), e frases dos posts dela. Sem listas verticais, sem emoji, sem repetir a mesma frase de efeito em dois capítulos.
- **O fio das mentiras**: cada "Para você" dos caps. 1–26 nomeia uma frase que a menina passou a acreditar sobre si ("Essa não dá trabalho", "Tanto faz", "O meu não é nada", "Eu nunca mais te peço nada", "Você tem sorte", "Eu dou conta", "Foi tudo ótimo", "Minha vida é comum"). No cap. 31, ela as escreve numa coluna, risca uma por uma e escreve a verdade ao lado (tabela no livro). A lista completa está em `docs/ROTEIRO.md`.
- **"Menina elefante"**: nasce no cap. 27. Antes disso, não aparece em lugar nenhum, nem na abertura (que só diz "uma menina que era grande e achava que era pequena"). Depois, pode voltar.
- **A narradora adulta** continua rara dentro da cena; o comentário tem lugar próprio, o "Para você".
- **Moldura**: não há mais prólogo. O livro abre com "Antes de começar" (a Luciana de hoje, ~300 palavras) e segue em ordem cronológica, de 1994 a 2026. A primeira sessão de terapia está no cap. 26, em 2024.
- **Fé**: Josué 1:9 continua sendo o versículo do livro, dito em cena no batismo (cap. 30). Os "Para você" falam de Deus como ela fala nos posts, sem pregar e sem empilhar versículos.
- **Marcações nos .txt**: `§` abre o "Para você"; `? ` pergunta ao leitor; `[carta]` e `[/carta]` para a carta do cap. 33; `~` linha alinhada à direita (assinatura); `^` linha centralizada e maior; linhas começando com `|` formam a tabela de duas colunas (a esquerda sai riscada).

---

# Guia de estilo da V2 (continua valendo para as cenas)

## Por que a V2 existe
Ver `docs/PARECER.md`. Resumo: a V1 (66 capítulos de ~90 palavras) conta a vida inteira em frases soltas, com 84% dos parágrafos de até 6 palavras, 257 reticências, um "hoje eu sei" atrás do outro e uma lição no fim de cada capítulo. A história é forte; a forma é de post. A V2 transforma resumo em cena sem perder a voz da Luciana.

## Voz
1. **Primeira pessoa, Luciana, olhando de 2026 para trás.** Tempo verbal: passado. O presente fica na abertura, nos "Para você" e no fim do epílogo.
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

## A voz pública da Luciana (Instagram)
- Os textos dela (`referencia/instagram_luciana.md`) são a melhor fonte de **ideias, fatos e fé**, e têm a mesma cadência da V1 (linhas soltas, listas, lição no fim, "E você?"). O livro usa as ideias, não a forma.
- Uma frase dela pode entrar uma vez, em cena, como fala ou pensamento, nunca como fecho de capítulo nem como definição. A lista das candidatas está em `docs/LEITURA_INSTAGRAM.md`.
- Manter dela: a autocorreção ("ou melhor"), o humor autodepreciativo, as imagens práticas (a habilitação, a caixinha, a porta automática, o mural).
- Fé: acontecimento e relação, sem sermão. No máximo um versículo no livro, dito por alguém, em cena (sugestão: Josué 1:9, o versículo dela).
- O vocabulário de palestra dos textos dela ("consciência", "nova versão", "vida extraordinária", "prosperidade", "autorresponsabilidade") pode aparecer em fala, com a mesma leveza com que O Jardim trata o nome da palestra: nunca na narração e nunca como conclusão.

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
