# A Menina Elefante — V3 (jornada da heroína)

Memória de Luciana Lumi Watanabe Yamanaka, no mesmo modelo de trabalho de *O Jardim Entre o Agora e o Depois* (a pasta-mãe deste repositório). A V1 (66 capítulos curtíssimos, ~6 mil palavras) está em `referencia/`. A V2 reescreve o livro em cenas, em primeira pessoa, seguindo o parecer e o roteiro de `docs/`.

**V3 escrita (30/09/2026), a pedido da autora**: jornada da heroína em ordem cronológica, 7 partes com os anos, 33 capítulos, abertura "Antes de começar", epílogo "A história continua" e página de apoio. Cada capítulo tem a **cena** e, depois do `§`, o **"Para você"**: a Luciana de hoje falando com quem lê, no espírito do *Plenitude*, de Camila Vieira. ~42 mil palavras, ~230 páginas.
**V4 (01/10/2026)**: correções da família (filhas, cronologia, Kousuke, noivado, Okinawa, brigas do casal), revisão de continuidade, vinhetas em traço na abertura de cada capítulo e PDF de leitura. ~43,6 mil palavras; PDF com 238 páginas.
**Falta:** a revisão da Luciana (em especial os "Para você", o cap. 31 com a Camila e o Paulo Vieira pelo nome, e as invenções listadas em `docs/DECISOES_V2.md`, seção V3); as respostas às perguntas de `docs/LEITURA_INSTAGRAM.md`.

## Antes de escrever qualquer coisa
1. `docs/PARECER.md` — o diagnóstico da V1 e a proposta.
2. `docs/ESTILO.md` — as regras de prosa. São o motivo de a V2 existir.
3. `docs/BIBLIA.md` — pessoas, linha do tempo, lugares, motivos, o que já foi fixado e o que falta confirmar.
4. `docs/ROTEIRO.md` — roteiro V3 (jornada da heroína, anos, a mentira e a verdade de cada capítulo) e, abaixo, o da V2 com o mapa de ecos.
4b. `docs/DECISOES_V2.md` — o que foi inventado ou deduzido em cada capítulo e o que precisa ser conferido.
5. Leia inteiros a abertura e os capítulos já escritos: são a referência de voz (cena) e de tom (o "Para você").
6. Fatos e falas da V1: `referencia/A_Menina_Elefante_V1.txt` (o roteiro indica os capítulos de origem).
7. Postagens e textos da Luciana: `referencia/instagram_luciana.md`, com a leitura em `docs/LEITURA_INSTAGRAM.md` (fatos, eixos do pensamento, voz, onde cada história entra, perguntas).

## Fluxo de trabalho
- Um capítulo por arquivo, nos caminhos de `manuscrito/estrutura.json`.
- Formato dos .txt: parágrafos separados por linha em branco; diálogo começa com travessão (—); `*` sozinho numa linha = quebra de cena; `§` abre o "Para você"; `? ` = pergunta ao leitor (itálico); `[carta]`…`[/carta]`, `~` (assinatura à direita), `^` (linha centralizada e maior) e linhas com `|` (tabela de duas colunas, a esquerda riscada). Não use negrito.
- Páginas de destaque (pedido da autora, no estilo dos livros de citação): `manuscrito/destaques.json` lista as frases que ganham uma página inteira de fundo escuro com letra grande (Bebas Neue, embutida no .docx a partir de `referencia/fontes/`, licença OFL) e um ramo de oliveira num canto (quatro desenhos: ramo longo, ramos cruzados, ramo em arco e meia coroa; azeitonas em cerca de uma página a cada três, campo "azeitonas" do destaques.json; pedido da autora). `[[...]]` marca as palavras em branco. A página entra na próxima quebra de cena depois da âncora. Os fundos são gerados por `python3 tools/ornamentos.py` em `ilustracoes/`. Frase de destaque só com texto que já está no capítulo (cena ou "Para você"); cada âncora vale uma vez; nunca "menina elefante"; nenhuma no epílogo.
- Ao terminar uma parte:
  - `python3 tools/metricas.py --parte II` e ajuste o que estiver fora das metas;
  - `python3 tools/build.py --parte II` gera `saidas/A_Menina_Elefante_V4_Parte_II.docx`;
  - `python3 tools/build.py` gera o livro inteiro em `saidas/A_Menina_Elefante_V4.docx`;
  - `python3 tools/pdf.py` gera o PDF de leitura `saidas/A_Menina_Elefante_V4.pdf` (mesma diagramação, impresso pelo Chromium do ambiente; número da página no pé, sem cabeçalho corrido; hifenização própria por sílabas).
- Vinhetas (V4, pedido da autora): `python3 tools/ilustracoes.py` desenha em SVG e renderiza `ilustracoes/vinheta_<capítulo>.png` (uma por capítulo, mais `abertura` e `epilogo`), que entram no alto de cada abertura de capítulo, no .docx e no PDF. Para trocar um desenho, edite o dicionário `D` do script e rode de novo só com a chave (`python3 tools/ilustracoes.py 27`).
- Só biblioteca padrão do Python. Não instale nada.
- Escreva uma parte por sessão e pare no fim dela para a autora revisar. Faça commit dos .txt e dos .docx gerados. No PR, liste: o que acontece em cada capítulo, toda decisão nova (nomes, fatos, datas, pseudônimos) e todo detalhe técnico, médico ou jurídico que a autora deve conferir.

## Regras que não se negociam
- A **cena** termina em imagem, gesto ou fala, nunca em lição. A lição mora no **"Para você"** (depois do `§`), que termina numa pergunta ao leitor. Regras do "Para você" em `docs/ESTILO.md` (seção V3).
- A expressão "menina elefante" nasce no cap. 27 (a história do elefante). Antes dele, não aparece em lugar nenhum; depois, pode voltar.
- Dentro da cena, a narradora adulta comenta pouco: "hoje eu sei / hoje eu entendo / olhando pra trás" no máximo uma vez por parte.
- Sem cadência de post: nada de reticências partindo frases da narração, listas de três em linhas soltas, 👉.
- O pai não é vilão; a mãe não é santa; o marido não é salvador; ninguém existe só para provar que a Luciana estava certa ou errada. Em cada cena, alguém quer algo diferente do que ela quer.
- Traição, tentativa de suicídio e câncer: contenção, sem detalhe gráfico, sem melodrama.
- Precisão: o marido da autora trabalha com financiamento imobiliário para estrangeiros no Japão. Vistos, seguro de saúde, fábrica/empreiteira, empréstimos, bancos, regras da pandemia e procedimentos médicos precisam estar certos. Na dúvida, genérico e sinalizado no PR.
- Português do Brasil. Termos japoneses sem itálico; na primeira vez, uma aposição curta explica.
- Pessoas secundárias reais usam pseudônimo até a autora decidir.

## Diagramação (a autora pediu ~200 páginas sem enxugar; com os acréscimos da V3, ~230)
- `tools/build.py` diagrama o livro: 5,5 × 8,5 pol., EB Garamond (tamanho em `DIAG`), margens espelhadas (interna 2 cm, externa 1,5 cm), hifenização em português, cabeçalho com o título do livro nas páginas pares e o do capítulo nas ímpares, e sem cabeçalho na folha de rosto, nas páginas de parte, nas aberturas de capítulo e nas páginas de destaque. Fontes embutidas (OFL) em `referencia/fontes/`.
- V3: corpo 11,5 pt com entrelinha exata de 16,8 pt. Com ~42 mil palavras e 26 páginas de destaque, o livro fica com ~230 páginas (simulação no navegador; confirmar no Word). Em corpo 11 pt, ~220.

## Metas de tamanho
- Cena: 800–1.500 palavras por capítulo. "Para você": 130–220 (até ~240 no fim do livro). Abertura ~300.
- Livro inteiro: ~42 mil palavras (~230 páginas).

## Pendências que só a autora decide (sinalize, não resolva sozinho)
- Aprovar ou ajustar o roteiro (`docs/ROTEIRO.md`) e o tom da Parte I.
- Nomes: irmãos (Marcos é irmão; Simone e Xavier?), o cachorro, os tios padrinhos; o marido aparece como **Kousuke** na voz dela (confirmar); se a empresa aparece como Easy House.
- Batismo (data, lugar, presentes), primeiro salto (onde), Banco de Nagoya (cidade/ano), mural da vida extraordinária: perguntas em `docs/LEITURA_INSTAGRAM.md`.
- Cidade(s) no Japão (a cidade no Brasil é Jacareí, confirmada) (provável: região de Minokamo/Gifu); ramo do trabalho da mãe.
- O pai veio de navio criança ou adulto, e com quem.
- A origem da imagem da menina elefante (cap. 27).
- Pseudônimos da Parte I (lista na Bíblia).
