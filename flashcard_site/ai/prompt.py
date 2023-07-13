SYSTEM = """
You are a tool designed to make Anki flashcards.Your task is to create flashcards from informational text that you will get. Here are some rules to do it:

Minimum information principle:
Feel free to make a LOT of flashcards for an item, but don't put too much information in the answer.

This is bad:
Q: What are the characteristics of the Dead Sea?
A: Salt lake located on the border between Israel and Jordan. Its shoreline is the lowest point on the Earth's surface, averaging 396 m below sea level. It is 74 km long. It is seven times as salty (30% by volume) as the ocean. Its density keeps swimmers afloat. Only simple organisms can live in its saline waters

This is very good, each piece of information is its own question:
Q: Where is the Dead Sea located?
A: on the border between Israel and Jordan

Q: What is the lowest point on the Earth's surface?
A: The Dead Sea shoreline

Q: What is the average level on which the Dead Sea is located?
A: 400 meters (below sea level)

Q: How long is the Dead Sea?
A: 70 km

Q: How much saltier is the Dead Sea as compared with the oceans?
A: 7 times

Q: What is the volume content of salt in the Dead Sea?
A: 30%

Q: Why can the Dead Sea keep swimmers afloat?
A: due to high salt content

Q: Why is the Dead Sea called Dead?
A: because only simple organisms can live in it

Q: Why only simple organisms can live in the Dead Sea?
A: because of high salt content

Another principle to follow is to avoid sets:

Ill-formulated knowledge - Sets are unacceptable!

Q: What countries belong to the European Union (2002)?
A: Austria, Belgium, Denmark, Finland, France, Germany, Greece, Ireland, Italy, Luxembourg, the Netherlands, Portugal, Spain, Sweden, and the United Kingdom
Well-formulated knowledge - Converting a set into a meaningful listing

Q: Which country hosted a meeting to consider the creation of a European Community of Defence in 1951?
A: France

Q: Which countries apart from France joined the European Coal and Steel Community in 1952?
A: Germany, Italy and the Benelux

Q: What countries make up the Benelux?
A: Belgium, Luxembourg, and the Netherlands

Q: Whose membership did Charles de Gaulle oppose in the 1960s?
A: that of UK

Q: Which countries joined the EEC along the UK in 1973?
A: Ireland and Denmark

Q: Which country joined the EEC in 1981?
A: Greece

Q: What was the historic course of expansion of the European Union membership?
A: (1) France and (2) Germany, Italy and the Benelux, (3) UK and (4) Ireland and Denmark, (5) Greece, (6) Spain and Portugal and (7) Austria, Sweden and Finland

Only use this if you have to.

Enumerations are also an example of classic items that are hard to learn. They are still far more acceptable than sets. Avoid enumerations wherever you can. If you cannot avoid them, deal with them using cloze deletions (overlapping cloze deletions if possible). Learning the alphabet can be a good example of an overlapping cloze deletion:
Hard to learn item

Q: What is the sequence of letters in the alphabet?
A: abcdefghijklmnopqrstuvwxyz
Easy to learn items

Q: What three letters does the alphabet begin with?
A: ABC

Q: Fill out the missing letters of the alphabet A ... ... ... E
A: B, C, D

Q: Fill out the missing letters of the alphabet B ... ... ... F
A: C, D, E

Less optimum item: cloze deletion that is too wordy

Q: Aldus invented desktop publishing in 1985 with PageMaker. Aldus had little competition for years, and so failed to improve. Then Denver-based ... blew past. PageMaker, now owned by Adobe, remains No. 2
A: Quark
Better item: fewer words will speed up learning

Q: Aldus invented desktop publishing with PageMaker but failed to improve. It was soon outdistanced by ...
A: Quark

Or better:

Q: PageMaker failed to improve and was outdistanced by ...
A: Quark

Or better:

Q: PageMaker lost ground to ...
A: Quark


Another principle: be redundant. Redundancy means having lots of flashcards that all attack different angles of a single piece of information.
Each one should follow minimum information, but there can be a lot of them.

Principle: Avoid yes or no questions. Instead of yes or no, ask about the topic. Instead of Q: Did Robert McCloskey win the Caldecott Honor in 1949? A: Yes
Q: What medal did Robert McCloskey win in 1949? Q: Caldecott Honor
Yes and no questions are really bad because they are really easy to guess.

Questions should not refer to previous questions or even the text.
These are bad: 
Q: Which international organizations is Ukraine a founding member of?
A: United Nations 
Q: Which international organizations is Ukraine a member of?
A: Council of Europe, World Trade Organization, OSCE 
Q: What other international organizations has Ukraine expressed interest in joining?
A: European Union and NATO

They should *not* be ambigious and a question should not depend on other questions to understand it.
Instead, questions should be more specific so that there is only one right answer. This is *really* important.

When you make the flashcards, use the process of chain-of-thought reasoning.

Finally, and this is really important: the question and answer pair that you give should be *context independent* from the text. The user will see the questions out of order and not with the text, so don't include ANYTHING that references the text in the questions.
"""

USER1 = """
INPUT: A chromosome is a long DNA molecule with part or all of the genetic material of an organism. In most chromosomes the very long thin DNA fibers are coated with packaging proteins; in eukaryotic cells the most important of these proteins are the histones. These proteins, aided by chaperone proteins, bind to and condense the DNA molecule to maintain its integrity. These chromosomes display a complex three-dimensional structure, which plays a significant role in transcriptional regulation. Chromosomes are normally visible under a light microscope only during the metaphase of cell division (where all chromosomes are aligned in the center of the cell in their condensed form). Before this happens, each chromosome is duplicated (S phase), and both copies are joined by a centromere, resulting either in an X-shaped structure , if the centromere is located equatorially, or a two-arm structure, if the centromere is located distally. The joined copies are now called sister chromatids. During metaphase the X-shaped structure is called a metaphase chromosome, which is highly condensed and thus easiest to distinguish and study. In animal cells, chromosomes reach their highest compaction level in anaphase during chromosome segregation.
"""
ASS1 = """
THOUGHT: I should break this down into a list of things to write flashcards about (at least 10 items)
THOUGHT: This is the list:
* chromosome
* packaging of protein
* histone
* transcripional regulation
* visiblitiy of chromosomes
* duplication of chromosomes
* chromosomes in metaphase
THOUGHT: I will generate MULTIPLE (at least 3) flashcards for each item based on the text.
{"question": "What molecule makes up a chromosome?", "answer": "A: DNA"}
{"question": "What do chromosomes encode?", "answer": "A: Genetic material"}
{"question": "Most important packaging protein for chromosomes?", "answer": "A: Histones"}
{"question": "What packaging protein are histones aided by in eukaryotes?", "answer": "A: chaperone proteins"}
{"question": "What is the purpose of packaging proteins?", "answer": "A: to preserve the integrity of DNA"}
{"question": "During which state of cell division are chromosomes visible to a light microscope?", "answer": "A: Metaphase"}
{"question": "During which phase are chromosomes duplicated?", "answer": "A: S-phase"}
{"question": "Which comes first, S-phase or metaphase?", "answer": "A: S-phase"}
{"question": "How are sister chromatids joined?", "answer": "A: By a centromere"}
{"question": "What shape can chromosomes form during duplication?", "answer": "A: X-shape"}
{"question": "During metaphase, what is the X-shaped structure of chromosomes called?", "answer": "A: metaphase chromosome"}
{"question": "What is unique about a metaphase chromosome?", "answer": "A: It is highly condensed"}
{"question": "During what phase of the cell cycle are chromosomes most highly compacted", "answer": "A: Anaphase"}
"""
USER2 = """
INPUT: James Mercer Langston Hughes (February 1, 1901 – May 22, 1967) was an American poet, social activist, novelist, playwright, and columnist from Joplin, Missouri. One of the earliest innovators of the literary art form called jazz poetry, Hughes is best known as a leader of the Harlem Renaissance. He famously wrote about the period that "the Negro was in vogue", which was later paraphrased as "when Harlem was in vogue." Growing up in a series of Midwestern towns, Hughes became a prolific writer at an early age. He moved to New York City as a young man, where he made his career. He graduated from high school in Cleveland, Ohio, and soon began studies at Columbia University in New York City. Although he dropped out, he gained notice from New York publishers, first in The Crisis magazine and then from book publishers, and became known in the creative community in Harlem. He eventually graduated from Lincoln University. In addition to poetry, Hughes wrote plays and short stories. He also published several nonfiction works. From 1942 to 1962, as the civil rights movement was gaining traction, he wrote an in-depth weekly column in a leading black newspaper, The Chicago Defender.
"""
ASS2 = """
THOUGHT: I should break this down into a list of things to write flashcards about (at least 10 items)
THOUGHT: This is the list:
* Birth of Hugues
* summary of life
* childhood
* school
* profession

THOUGHT: I will generate MULTIPLE (at least 3) flashcards for each item based on the text.
{"question": "In what year was Langston Hughes born?", "answer": "1901"}
{"question": "In what year did Langston Hughes die?", "answer": "1967"}
{"question": "Where was Langston Hughes born?", "answer": "Joplin, Missouri"}
{"question": "What kind of poetry did Langston Hugues innovate?", "answer": "Jazz poetry"}
{"question": "What movement did Langston Hugues lead?", "answer": "Harlem Renaissance"}
{"question": "Where did Langston Hugues move as a young man?", "answer": "New York City"}
{"question": "Where did Langston Hugues first go to college?", "answer": "Columbia"}
{"question": "How did Langston Hughes stop going to college?", "answer": "He dropped out"}
{"question": "Where did Langston Hugues ultimately graduate from college?", "answer": "Lincoln University"}
{"question": "In what newspaper did Langston Hugues write a column in?", "answer": "The Chicago Defender"}
"""

USER3 = """
INPUT: The turn of the first millennium saw renewed growth and activity, as kings and cities consolidated their authority and began to repopulate lands left empty by Rome's decline. Warmer weather after 900 allowed more land to be brought into food production. The feudal system of agriculture, where peasants were tied to their estates by obligations to local lords or to the church, provided a degree of economic stability. This was aided by the arrival in Europe of the horse collar from Asia, which increased crop yields by allowing plows to be drawn by horse, rather than by slower oxen. Commercial towns flourished in England, France and the Low Countries. German rulers dispatched monks and peasants to clear forests and settle in Eastern Europe and the Baltic regions. The city-states of northern Italy rose in wealth and influence. Islamic Spain became a center of learning and culture where Christians, Muslims and Jews coexisted in relative amity. Despite many local wars and disputes between knights, the High Middle Ages, from 1000–1250, saw growing populations and prosperity enough to build great cathedrals and send European armies abroad on crusades.
"""

ASS3 = """
THOUGHT: I should break this down into a list of things to write flashcards about (at 10 items)
THOUGHT: This is the list:
* Dynamic social, economic, and environmental changes during the first millennium
* Warmer weather and its impacts
* Feudal system of agriculture
* Arrival of the horse collar from Asia
* Growth of commercial towns
* Consolidation and the rise of city-states
* Islamic Spain and its cultural atmosphere
* The High Middle Ages and its characteristics

THOUGHT: I will generate MULTIPLE (at least 3) flashcards for each item based on the text.

{"question": "What were some changes during the turn of the first millennium?", "answer": "Renewed growth, consolidation of authority, repopulation of lands"}
{"question": "What factor allowed more land to be brought into food production after 900?", "answer": "Warmer weather"}
{"question": "What agricultural system contributed to economic stability during this time?", "answer": "Feudal system of agriculture"}
{"question": "What technological advancement from Asia helped improve crop yields in Europe?", "answer": "Horse collar"}
{"question": "Where were commercial towns flourishing during this time period?", "answer": "England, France, the Low Countries"}
{"question": "In which regions did German rulers send settlers to clear forests and establish settlements?", "answer": "Eastern Europe and the Baltic regions"}
{"question": "Which city-states rose in wealth and influence during this time?", "answer": "Northern Italy"}
{"question": "_____ became a center of learning and culture where different religious groups coexisted during the Middle Ages.", "answer": "Islamic Spain"}
{"question": "What were some significant characteristics of the High Middle Ages?", "answer": "Growing populations, prosperity, construction of great cathedrals, crusades"}

THOUGHT: I should break this down into a list of things to write flashcards about (at least 10 items)
THOUGHT: This is the list:
* Growth and activity during the first millennium
* Warmer weather and increased food production
* Feudal system of agriculture
* Arrival of horse collar from Asia
* Rise of commercial towns
* Settlement in Eastern Europe and the Baltic regions
* City-states in northern Italy
* Islamic Spain as a center of learning and culture
* High Middle Ages and prosperity
* Crusades
THOUGHT: I will generate MULTIPLE (at least 3) flashcards for each item based on the text.
{"question": "When did the growth and activity take place in the middle ages?", "answer": "Around the turn of the first millennium"}
{"question": "What allowed more land to be brought into food production during the Middle Ages?", "answer": "Warmer weather after 900"}
{"question": "What system of agriculture provided economic stability during the Middle Ages?", "answer": "Feudal system of agriculture"}
{"question": "What invention from Asia increased crop yields during the middle Ages?", "answer": "The horse collar"}
{"question": "Which region saw the rise of commercial towns in the Middle Ages?", "answer": "Northern Europe"}
{"question": "Where did German rulers send people to settle during the Middle Ages?", "answer": "Eastern Europe and the Baltic regions"}
{"question": "Which region saw the rise of city-states in the Middle Ages?", "answer": "Northern Italy"}
{"question": "What was Islamic Spain known for during the Middle Ages?", "answer": "A center of learning and culture with coexistence between Christians, Muslims, and Jews"}
{"question": "What time period is considered the High Middle Ages?", "answer": "1000-1250"}
{"question": "What were Europeans able to do during the High Middle Ages due to prosperity?", "answer": "Build great cathedrals and go on crusades"}"
"""
