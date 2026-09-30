# A Menina Elefante — revisão V2

Memória de Luciana Lumi Watanabe Yamanaka, no mesmo modelo de trabalho de *O Jardim Entre o Agora e o Depois* (a pasta-mãe deste repositório). A V1 (66 capítulos curtíssimos, ~6 mil palavras) está em `referencia/`. A V2 reescreve o livro em cenas, em primeira pessoa, seguindo o parecer e o roteiro de `docs/`.

**Já escrito (versão completa revisada; visita ao pai, "Mãe sabe" e o cubo montado pela Luciana aprovados pela autora):** nota ao leitor, prólogo, Partes I–VI (capítulos 1–29) e epílogo, ~34.300 palavras.
**Falta:** a revisão da Luciana; as respostas às perguntas de `docs/LEITURA_INSTAGRAM.md`; ajustar o texto conforme `docs/DECISOES_V2.md` (tudo o que foi inventado ou deduzido, capítulo por capítulo).

## Antes de escrever qualquer coisa
1. `docs/PARECER.md` — o diagnóstico da V1 e a proposta.
2. `docs/ESTILO.md` — as regras de prosa. São o motivo de a V2 existir.
3. `docs/BIBLIA.md` — pessoas, linha do tempo, lugares, motivos, o que já foi fixado e o que falta confirmar.
4. `docs/ROTEIRO.md` — roteiro definitivo: espinha, mapa de ecos e o que acontece em cada capítulo.
4b. `docs/DECISOES_V2.md` — o que foi inventado ou deduzido em cada capítulo e o que precisa ser conferido.
5. Leia inteiros o prólogo e os capítulos já escritos: são a referência de voz.
6. Fatos e falas da V1: `referencia/A_Menina_Elefante_V1.txt` (o roteiro indica os capítulos de origem).
7. Postagens e textos da Luciana: `referencia/instagram_luciana.md`, com a leitura em `docs/LEITURA_INSTAGRAM.md` (fatos, eixos do pensamento, voz, onde cada história entra, perguntas).

## Fluxo de trabalho
- Um capítulo por arquivo, nos caminhos de `manuscrito/estrutura.json`.
- Formato dos .txt: parágrafos separados por linha em branco; diálogo começa com travessão (—); `*` sozinho numa linha = quebra de cena. Não use negrito.
- Páginas de destaque (pedido da autora, no estilo dos livros de citação): `manuscrito/destaques.json` lista as frases que ganham uma página inteira de fundo escuro com letra grande (Bebas Neue, embutida no .docx a partir de `referencia/fontes/`, licença OFL) e ornamento. `[[...]]` marca as palavras em branco. A página entra na próxima quebra de cena depois da âncora. Os fundos são gerados por `python3 tools/ornamentos.py` em `ilustracoes/`. Frase de destaque só com texto que já está no capítulo; nunca "menina elefante"; nenhuma no epílogo.
- Ao terminar uma parte:
  - `python3 tools/metricas.py --parte II` e ajuste o que estiver fora das metas;
  - `python3 tools/build.py --parte II` gera `saidas/A_Menina_Elefante_V2_Parte_II.docx`;
  - `python3 tools/build.py` gera o livro inteiro em `saidas/A_Menina_Elefante_V2.docx`.
- Só biblioteca padrão do Python. Não instale nada.
- Escreva uma parte por sessão e pare no fim dela para a autora revisar. Faça commit dos .txt e dos .docx gerados. No PR, liste: o que acontece em cada capítulo, toda decisão nova (nomes, fatos, datas, pseudônimos) e todo detalhe técnico, médico ou jurídico que a autora deve conferir.

## Regras que não se negociam
- Nenhum capítulo termina em lição ou frase que explica o que o capítulo significou. Termine em imagem, gesto ou fala.
- A expressão "menina elefante" só aparece no texto no cap. 26, onde a imagem é explicada uma única vez. Em nenhum outro lugar (títulos à parte).
- A narradora adulta comenta pouco: "hoje eu sei / hoje eu entendo / olhando pra trás" no máximo uma vez por parte.
- Sem cadência de post: nada de reticências partindo frases da narração, listas de três em linhas soltas, 👉.
- O pai não é vilão; a mãe não é santa; o marido não é salvador; ninguém existe só para provar que a Luciana estava certa ou errada. Em cada cena, alguém quer algo diferente do que ela quer.
- Traição, tentativa de suicídio e câncer: contenção, sem detalhe gráfico, sem melodrama.
- Precisão: o marido da autora trabalha com financiamento imobiliário para estrangeiros no Japão. Vistos, seguro de saúde, fábrica/empreiteira, empréstimos, bancos, regras da pandemia e procedimentos médicos precisam estar certos. Na dúvida, genérico e sinalizado no PR.
- Português do Brasil. Termos japoneses sem itálico; na primeira vez, uma aposição curta explica.
- Pessoas secundárias reais usam pseudônimo até a autora decidir.

## Diagramação (decisão da autora: cerca de 200 páginas, sem enxugar mais)
- `tools/build.py` diagrama o livro: 5,5 × 8,5 pol., EB Garamond 12 pt com entrelinha exata de 17,6 pt, margens espelhadas (interna 2 cm, externa 1,5 cm), hifenização em português, cabeçalho com o título do livro nas páginas pares e o do capítulo nas ímpares, e sem cabeçalho na folha de rosto, nas páginas de parte, nas aberturas de capítulo e nas páginas de destaque. Fontes embutidas (OFL) em `referencia/fontes/`.
- Com ~34 mil palavras e 23 páginas de destaque, o livro fica com ~195–200 páginas (simulação no navegador; confirmar no Word).

## Metas de tamanho
- Partes I–V: 1.000–1.500 palavras por capítulo. Parte VI: 1.000–1.400. Prólogo ~900. Epílogo ~500.
- Livro inteiro: ~34 mil palavras.

## Pendências que só a autora decide (sinalize, não resolva sozinho)
- Aprovar ou ajustar o roteiro (`docs/ROTEIRO.md`) e o tom da Parte I.
- Nomes: irmãos (Marcos é irmão; Simone e Xavier?), a ordem e o nome da terceira filha (Mity e Tiemi já aparecem), o cachorro, os tios padrinhos; o marido aparece como **Kousuke** na voz dela (confirmar); se a empresa aparece como Easy House.
- Batismo (data, lugar, presentes), primeiro salto (onde), Banco de Nagoya (cidade/ano), mural da vida extraordinária: perguntas em `docs/LEITURA_INSTAGRAM.md`.
- Cidade da infância no Brasil; cidade(s) no Japão (provável: região de Minokamo/Gifu); ramo do trabalho da mãe.
- O pai veio de navio criança ou adulto, e com quem.
- A origem da imagem da menina elefante (cap. 26).
- Pseudônimos da Parte I (lista na Bíblia).
