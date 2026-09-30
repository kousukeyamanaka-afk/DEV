# A Menina Elefante — revisão V2

Memória de Luciana Lumi Watanabe Yamanaka, no mesmo modelo de trabalho de *O Jardim Entre o Agora e o Depois* (a pasta-mãe deste repositório). A V1 (66 capítulos curtíssimos, ~6 mil palavras) está em `referencia/`. A V2 reescreve o livro em cenas, em primeira pessoa, seguindo o parecer e o roteiro de `docs/`.

**Já escrito (aguarda revisão):** nota ao leitor, prólogo e Parte I (capítulos 1–5, ~7.100 palavras).
**Falta:** aprovação do roteiro; Parte II (6–10), Parte III (11–15), Parte IV (16–20), Parte V (21–24), Parte VI (25–28) e o epílogo.

## Antes de escrever qualquer coisa
1. `docs/PARECER.md` — o diagnóstico da V1 e a proposta.
2. `docs/ESTILO.md` — as regras de prosa. São o motivo de a V2 existir.
3. `docs/BIBLIA.md` — pessoas, linha do tempo, lugares, motivos, o que já foi fixado e o que falta confirmar.
4. `docs/ROTEIRO.md` — o que acontece em cada capítulo, com as fontes na V1.
5. Leia inteiros o prólogo e os capítulos já escritos: são a referência de voz.
6. Fatos e falas da V1: `referencia/A_Menina_Elefante_V1.txt` (o roteiro indica os capítulos de origem).
7. Postagens e textos da Luciana: `referencia/instagram_luciana.md`, com a leitura em `docs/LEITURA_INSTAGRAM.md` (fatos, eixos do pensamento, voz, onde cada história entra, perguntas).

## Fluxo de trabalho
- Um capítulo por arquivo, nos caminhos de `manuscrito/estrutura.json`.
- Formato dos .txt: parágrafos separados por linha em branco; diálogo começa com travessão (—); `*` sozinho numa linha = quebra de cena. Não use negrito.
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

## Metas de tamanho
- Partes I–V: 1.000–1.500 palavras por capítulo. Parte VI: 1.000–1.400. Prólogo ~900. Epílogo ~500.
- Livro inteiro: ~33 mil palavras.

## Pendências que só a autora decide (sinalize, não resolva sozinho)
- Aprovar ou ajustar o roteiro (`docs/ROTEIRO.md`) e o tom da Parte I.
- Nomes: irmãos (quantos, sexo, ordem), as três filhas, o cachorro, os tios padrinhos; se o Alan aparece com o nome real (e "Kou" em casa); se a empresa aparece como Easy House.
- Batismo (data, lugar, presentes), primeiro salto (onde), Banco de Nagoya (cidade/ano), mural da vida extraordinária: perguntas em `docs/LEITURA_INSTAGRAM.md`.
- Cidade da infância no Brasil; cidade(s) no Japão (provável: região de Minokamo/Gifu); ramo do trabalho da mãe.
- O pai veio de navio criança ou adulto, e com quem.
- A origem da imagem da menina elefante (cap. 26).
- Pseudônimos da Parte I (lista na Bíblia).
