# Revisão da V2 — relatório editorial

**Livro:** O Jardim Entre o Agora e o Depois (V2 completa: prólogo, 26 capítulos, epílogo)
**Data:** 2026-09-30
**Método:** skills `dev-edit` (ritmo, estrutura, arcos, coerência), `continuity-check` (varredura completa, 7 categorias) e `story-analysis` (fios de trama e tensão). As skills foram adaptadas ao projeto: a bíblia está em `docs/BIBLIA.md`, e não em `wiki/`. Também rodei o `tools/metricas.py` e contei as muletas de linguagem no texto inteiro.
**Precedência:** as regras do `CLAUDE.md` e do `docs/ESTILO.md` valem sobre as sugestões genéricas das skills. Por exemplo, a skill de ritmo pede finais de capítulo com suspense, e o guia do livro pede finais em imagem, gesto ou fala. Segui o guia.

---

## 1. Resumo

O livro está estruturalmente sólido.

| Marco | Meta do roteiro | Onde caiu |
|---|---|---|
| Virada do meio (cap. 13) | ~53% | 44–49% |
| Recusa ao Kuroda (cap. 17) | ~70% | 63–67% |
| Clímax (cap. 21) | ~83% | 79–84% |
| Desfecho | ~17% | ~16% |

As regras que não se negociam foram cumpridas:
- nenhum capítulo termina em moral;
- "Contentamento Dinâmico" aparece uma única vez (cap. 23);
- as placas só aparecem em negrito no cap. 10;
- o William, o Kuroda e a Haruka não viram vilões.

Os pontos a melhorar se concentram em três áreas:

1. **Continuidade.** Encontrei quatro erros de data e contagem. **Já corrigi os quatro** (seção 2).
2. **Fios de trama que somem na Parte VI.** Mateo e Gabriel, Renato e a fé, Satomi e a pergunta que ficou entre a Maya e o pai (seção 4).
3. **Muletas de linguagem que se acumulam no livro inteiro.** "olhou para" aparece 48 vezes, "devagar" 27, "ficou olhando" 18, "como quem" 17 e "dobrar em quatro" 7 (seção 6).

---

## 2. Continuidade (`continuity-check`, varredura completa)

### 🚨 Erros críticos (já corrigidos neste PR)
- **Linha do tempo, cap. 22 × cap. 23.** O café com o Kuroda em Tóquio estava em "outubro do quinto ano", e o resort do cap. 23 acontece no "verão do quinto ano". Isso quebrava a ordem cronológica que o roteiro exige. **Correção:** o café passou para "junho daquele ano".
- **Fato, cap. 25 × cap. 26.** A Maya entra na universidade em abril do Ano 8, e em outubro do Ano 10 o texto dizia "segundo ano de economia". **Correção:** "terceiro ano".

### ⚠️ Erros menores (já corrigidos)
- **Cap. 26:** as placas, pregadas na cerca no verão do Ano 5, estavam "escurecidas por cinco verões" em outubro do Ano 10. São seis. **Correção:** "seis verões".
- **Epílogo:** "Em janeiro" jogava o epílogo para o Ano 11, e a bíblia o põe no inverno do Ano 10. **Correção:** "Em dezembro". A poda da figueira em dezembro também é correta.

### 🔍 Para o autor conferir (possivelmente intencional)
- **Cap. 24, o funeral budista do Mori.** A Setsuko ia a uma igreja, e o Mori nunca foi, então é coerente. Ainda assim, o pastor da Setsuko, que fez as quatro perguntas, poderia aparecer no velório como uma presença discreta.
- **Cap. 16, "vô Mori".** A Maya adota o nome sem cena de origem. Funciona, mas é uma decisão nova.

### ✅ Categorias limpas
Não achei problemas em descrição física, acesso à informação (quem sabe o quê), regras do mundo (bancos, escola, prazos) e deslocamentos impossíveis. Idades e anos batem com a bíblia em todos os capítulos: a Maya tem 10, 12, 13, 15, 18 e 20 anos; a Nina tem 7, 9, 10, 13, 15 e 17; o Mori tem 73 e morre aos 78.

---

## 3. Ritmo (`dev-edit`, dimensão 1)

### ⚠️ Arrastado
- **Cap. 16, o sábado sozinho com as meninas** (arroz, natação, máquina de lavar). O bloco é bom, mas fica um pouco longo antes das placas. **Sugestão:** cortar a natação e ir da máquina de lavar direto para a caixa de madeira.
- **Cap. 19, o primeiro terço** (montadoras, bancos, cortes). É o trecho mais expositivo das Partes IV–VI: três parágrafos de narrador contando a crise. **Sugestão:** transformar um deles em cena, por exemplo o Hayashi em pessoa ou a reunião do bônus vista de dentro.

### ⚡ Apressado
- **Cap. 22.** A Naomi reorganiza a empresa, a parceria de Shizuoka é assinada, o Kuroda aparece em Tóquio e o William compra o apartamento, tudo em cerca de mil palavras e mais de um ano de história. A conversa com o Kuroda, que é o título do capítulo, tem pouco espaço para respirar. **Sugestão:** cortar a cena da Keiko com o Hayashi ou a das férias em Shirahama e dar essas palavras ao café em Tóquio.
- **Cap. 26, o último capítulo.** Tem 1.120 palavras, e o roteiro previa ~1.700. A conversa com a Maya é contada mais do que mostrada ("Conversaram quase duas horas"). **Sugestão:** dramatizar um trecho da conversa (uma troca de 6 a 8 falas) antes do resumo.

### ✅ Bem ritmados
- **Caps. 3, 13, 17 e 21:** relógio correndo, decisão sob pressão e final em fala.
- **Cap. 12:** a voz da Maya, com detalhes concretos no lugar de reflexão.

### 💡 Recomendações de ritmo
- Na Parte VI, pensar em fundir o cap. 25 (A carta) com o começo do cap. 26, ou em alongar os dois um pouco. Os cinco capítulos curtos seguidos, cada um num ano diferente, dão uma sensação de álbum de fotos.

---

## 4. Estrutura e fios de trama (`dev-edit` 2 + `story-analysis` B)

### ⚖️ Equilíbrio dos atos
| Ato | Onde | Peso |
|---|---|---|
| Ato 1 (prólogo a cap. 5) | até ~20% | Equilibrado |
| Ato 2 (caps. 6 a 21) | ~20% a 84% | Equilibrado |
| Ato 3 (Parte VI e epílogo) | ~16% | Enxuto, sem estar comprimido |

### ⚠️ Fios que somem ou ficam sem fecho
| Fio | Último aparecimento | Situação | Sugestão |
|---|---|---|---|
| Mateo e Gabriel (e o tênis de luzinha, um dos motivos de "luzes" da bíblia) | Gabriel no cap. 19, Mateo no cap. 21 | Some da Parte VI | Uma aparição rápida no cap. 26 ou no epílogo: o Gabriel adolescente, com um tênis que já não pisca. As estacas do epílogo "sem saber para quem" podem ir para o quintal do Mateo. |
| Renato, o galpão e a fé do casal | Cap. 19 | Quase ausente da Parte VI (só "falou do galpão" no cap. 26) | Uma linha no cap. 24 (Renato no velório ou num culto) ou no cap. 26. A fé aparece forte até o cap. 11 e depois fica quieta. |
| Satomi | Cap. 21 | Sem despedida | Opcional: uma linha na Parte VI (aposentadoria, "Bem-vindo" invertido). |
| O sexto degrau: a Maya ouviu a conversa sobre separação, e o Miguel "não sabe quanto" | Cap. 20 ("Eles vão se separar?" / "Não. Dorme.") | Nunca é falado entre pai e filha | Na conversa do cap. 26, uma única frase da Maya ou do Miguel sobre aquela noite fecharia o fio mais íntimo do livro, sem explicar nada. |
| "Três minutos de alegria" (primeira aprovação) | Caps. 1 e 7 | Sem eco | Opcional: um eco no cap. 22, quando a Naomi pede "pelo menos uma vez, para. Olha." |

### ✅ Fios bem resolvidos
- Kuroda: proposta, recusa, retirada, "podemos rever" e o café em Tóquio.
- William: "Quem não cresce é engolido", "Eu quase pus" e "Cabe."
- A pasta do Haroldo: dos plásticos MAYA e NINA até a pasta da Maya no cap. 26.
- A figueira: da estaca, passando pela muda da Haruka, até a poda do epílogo.
- A hortelã, o LED do piano e "Como vai o futuro?".

---

## 5. Arcos de personagem (`dev-edit` 3)

### ✅ Arcos fortes
- **Miguel:** a recaída (cap. 20) evita o arco em linha reta, e a vontade de vender por cansaço (cap. 21) é a tentação mais humana do livro.
- **Maya:** da cadeira vazia até a pasta plástica própria e a escolha que o pai lhe devolve.
- **Kuroda:** "Estou dizendo que perdi". Não é vilão e também não fica bonzinho.

### 📉 Arcos subdesenvolvidos
- **Clara na Parte VI.** Depois do cap. 21, ela funciona sobretudo como interlocutora ("Você fez a cara do seu pai"). A fé dela, que abre a virada do livro (caps. 5 e 11), e o trabalho dela na Mirai quase não aparecem. **Sugestão:** uma cena curta do ponto de vista dela, ou um desejo próprio seu na Parte VI (algo que ela queira e que não seja do Miguel).
- **Nina.** É ótima como fonte de humor, mas não tem um momento de escolha própria. **Sugestão:** a carta colada no armário (cap. 25) é o começo; no cap. 26, ela poderia ter uma fala que não seja piada.

### ⚠️ Inconsistências
_Nenhuma sinalizada._

---

## 6. Coerência e linguagem (`dev-edit` 4 + guia de estilo)

### 🎯 Tema
O tema central ("contentamento é aprender a estar onde se está sem parar de ir") está presente em todas as partes. A zona mais quieta é a dos caps. 16 a 18, que é intencional, porque ali a tensão é externa.

### Muletas de linguagem (contagem no livro inteiro)
| Expressão | Ocorrências | Observação |
|---|---|---|
| "olhou para" | 48 | Normal em ficção, mas muitas estão em série na mesma cena |
| "devagar" | 27 | Aparece em quase todo capítulo como marca de gesto cuidadoso; virou tique |
| "de novo" | 19 | Parte são ecos intencionais ("De novo esse?") |
| "ficou olhando" | 18 | O cap. 14 tem 3 |
| "como quem" | 17 | Comparação favorita do narrador; 3 no cap. 4 e 2 em cada um dos caps. 16, 17 e 19 |
| "pela primeira vez" | 11 | Espalhado por 11 capítulos; perde força |
| "dobrar em quatro" | 7 | Motivo da bíblia (guardanapo do Kuroda, carta), mas também usado para o aviso da Maya, a pauta, o guardanapo da Naomi e a fotocópia. Recomendo deixar só os do Kuroda e da carta do Mori. |

**Sugestão:** uma passada de limpeza cortando cerca de metade de "devagar", "ficou olhando" e "como quem", sem mexer nos ecos intencionais.

### Métricas
- Todos os capítulos estão dentro das metas, exceto o cap. 10 (33% de parágrafos curtos e "perceb" 2). O `ESTILO.md` já registra o cap. 10 como exceção proposital.
- O livro tem 35.528 palavras no manuscrito, e a meta era ~34 mil.

### ✨ O que está funcionando: repetir
- **Finais em gesto ou objeto.** O cinto no vaso (15), o ponto vermelho do piano (26) e "Cabe." (22) confiam no leitor.
- **Ecos sem explicação.** O prólogo espelhado no cap. 26; "Aqui fecha mais tarde" nos caps. 3 e 20; "Não puxa" nos caps. 7, 15 e 24.
- **O mentor que não dá palestra.** As falas curtas do Mori e a Naomi que responde "Você está pagando por hora".

---

## 7. Próximos passos (por prioridade)

1. ✅ **Feito:** as quatro correções de continuidade da seção 2.
2. ✅ **Feito (aprovado pelo autor):** o fio Maya/sexto degrau foi fechado no cap. 26.
   - A conversa pai–filha agora está em cena, com a professora do centro comunitário e a planilha da Maya ("Quem te ensinou isso?" / "Você. Sem querer.").
   - A Maya diz "Eu estava no sexto degrau", e o Miguel responde "Eu ouvi o degrau", sem explicação.
3. ✅ **Feito (aprovado pelo autor):** aparições na Parte VI.
   - A Satomi se aposenta e entrega o carimbo à Naomi (cap. 22).
   - O Renato aparece com o café depois do velório (cap. 24).
   - O Mateo e o Gabriel, com onze anos e um tênis sem luz, vêm buscar mudas de hortelã e ficam para o primeiro tomate (cap. 24).
4. ✅ **Feito (aprovado pelo autor):** limpeza das muletas.

   | Expressão | Antes | Depois |
   |---|---|---|
   | "devagar" | 27 | 12 |
   | "ficou olhando" | 18 | 8 |
   | "como quem" | 17 | 11 |
   | "pela primeira vez" | 11 | 8 |

   "Dobrar em quatro" ficou só nos usos de motivo: o guardanapo e a pauta do Kuroda, a carta da construtora, o guardanapo da Naomi e a carta do Mori.
5. **Opcional, ainda pendente:**
   - dar mais espaço ao café com o Kuroda no cap. 22;
   - transformar em cena um parágrafo expositivo do cap. 19;
   - fazer a Clara querer alguma coisa própria na Parte VI.
