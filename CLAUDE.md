# O Jardim Entre o Agora e o Depois — revisão V2

Romance de Alan Yamanaka (o dono deste repositório). A V1 (17 mil palavras, 48 capítulos curtos) está em `referencia/`. A V2 reescreve o livro seguindo um parecer editorial e um roteiro aprovados pelo autor.

**Já escrito e aprovado:** folha de rosto, Nota ao Leitor, prólogo e Partes I–III (capítulos 1–11, ~13.200 palavras).
**Falta:** Parte IV (12–15), Parte V (16–21), Parte VI (22–26) e o epílogo.

## Antes de escrever qualquer coisa
1. `docs/ESTILO.md` — as regras de prosa. São o motivo de a V2 existir.
2. `docs/BIBLIA.md` — personagens, linha do tempo, lugares, motivos e falas recorrentes.
3. `docs/ROTEIRO_V2.md` — o que acontece em cada capítulo, com as fontes na V1.
4. Leia inteiros pelo menos `manuscrito/parte1/cap03.txt` e `manuscrito/parte3/cap11.txt`: são a referência de voz e de nível. De preferência, leia os 11 capítulos antes de começar a Parte IV.
5. Para reaproveitar falas da V1, procure em `referencia/O_Jardim_V1.txt` (o roteiro indica os capítulos de origem).
6. `docs/DOSSIE_CONTENTAMENTO_DINAMICO.md` — dossiê-mestre do autor com as teses, os relatos e os cuidados científicos e teológicos. Ele vale como contexto; em caso de conflito, prevalecem as regras deste arquivo. `docs/ATUALIZACAO_DOSSIE.md` registra como o dossiê já foi integrado.

## Fluxo de trabalho
- Um capítulo por arquivo, nos caminhos já definidos em `manuscrito/estrutura.json` (ex.: `manuscrito/parte4/cap12.txt`).
- Formato dos .txt: parágrafos separados por linha em branco; diálogo começa com travessão (—); `*` sozinho numa linha = quebra de cena; `**TEXTO**` = parágrafo em negrito (não use: as placas em negrito já apareceram no cap. 10).
- Ao terminar uma parte:
  - `python3 tools/metricas.py --parte IV` e ajuste o que estiver fora das metas;
  - `python3 tools/build.py --parte IV` gera `saidas/O_Jardim_V2_Parte_IV.docx`;
  - `python3 tools/build.py` gera o livro inteiro em `saidas/O_Jardim_V2.docx`.
- Só biblioteca padrão do Python. Não instale nada.
- Escreva uma parte por sessão e pare no fim dela para o autor revisar. Faça commit dos .txt e dos .docx gerados. No PR, liste: o que acontece em cada capítulo, toda decisão nova que você tomou (nomes, fatos, datas) e todo detalhe técnico ou jurídico que o autor deve conferir.

## Regras que não se negociam
- Nenhum capítulo termina em moral ou frase que explica a lição. Termine em imagem, gesto ou fala.
- "Contentamento Dinâmico" é nomeado e definido uma única vez, no cap. 23, pela Maya, com deboche ("parece nome de palestra de coach"). Em nenhum outro lugar.
- As `NOTAS DO AUTOR` (`manuscrito/notas_autor.txt`, depois do epílogo) explicam fontes e limites sem nomear o conceito; não as transforme em palestra nem cite autores com aspas sem edição e página conferidas.
- As placas não voltam em negrito. No cap. 26 aparecem em prosa. Epílogo sem palestra, sem placas, sem definição.
- O William não fracassa para provar que o Miguel estava certo. O Kuroda não é vilão. A Haruka não é vilã.
- Os mentores não dão palestra. Em cada cena, alguém quer algo diferente do que o Miguel quer.
- Precisão: o autor trabalha com financiamento imobiliário para estrangeiros no Japão. Bancos, documentos, contratos, prazos e leis precisam estar certos. Na dúvida, deixe genérico e sinalize no PR.
- Português do Brasil. Termos japoneses sem itálico; na primeira vez, uma aposição curta explica (ex.: "o hokenjo, o centro de saúde da prefeitura").
- O livro é próximo da vida do autor. Trate a família com respeito; nada de melodrama.

## Metas de tamanho
- Partes IV e V: 1.300–1.800 palavras por capítulo. Parte VI: 1.000–1.500. Epílogo: ~500.
- Livro inteiro: ~34 mil palavras.

## Pendências que só o autor decide (sinalize, não resolva sozinho)
- Cidade do seu Dito no Brasil (padrão atual: interior de São Paulo).
- Nomes criados na V2: seu Dito, Haruka, Setsuko, Everton, Kenta, Priscila, Roberto, dona Cida, Hayashi.
- Cap. 2: o prazo de três meses do registro no consulado é o da reserva de nacionalidade; o autor pode ajustar à história da família.
