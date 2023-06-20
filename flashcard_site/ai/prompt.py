PROMPT = """
Your task is to create flashcards from informational text that you will get. Here are some rules to do it:

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


Another principle: be redundant. Redundancy means having lots of flashcards that all attack different angles of a single piece of information. Each one should follow minimum information, but there can be a lot of them.

Principle: Avoid yes or no questions. Instead of yes or no, ask about the topic. Instead of Q: Did Robert McCloskey win the Caldecott Honor in 1949? A: Yes
Q: What medal did Robert McCloskey win in 1949? Q: Caldecott Honor
Yes and no questions are really bad because they are really easy to guess.

Example: When you make the flashcards, use this process of chain-of-thought reasoning.

INPUT: A chromosome is a long DNA molecule with part or all of the genetic material of an organism. In most chromosomes the very long thin DNA fibers are coated with packaging proteins; in eukaryotic cells the most important of these proteins are the histones. These proteins, aided by chaperone proteins, bind to and condense the DNA molecule to maintain its integrity. These chromosomes display a complex three-dimensional structure, which plays a significant role in transcriptional regulation.

Chromosomes are normally visible under a light microscope only during the metaphase of cell division (where all chromosomes are aligned in the center of the cell in their condensed form). Before this happens, each chromosome is duplicated (S phase), and both copies are joined by a centromere, resulting either in an X-shaped structure , if the centromere is located equatorially, or a two-arm structure, if the centromere is located distally. The joined copies are now called sister chromatids. During metaphase the X-shaped structure is called a metaphase chromosome, which is highly condensed and thus easiest to distinguish and study. In animal cells, chromosomes reach their highest compaction level in anaphase during chromosome segregation.

THOUGHT: I should break this down into a list of things to write flashcards about (at least 27 items)
THOUGHT: This is the list:
* chromosome
* packaging of protein
* histone
* transcripional regulation
* visiblitiy of chromosomes
* duplication of chromosomes
* chromosomes in metaphase
THOUGHT: I will generate MULTIPLE (at least 45) flashcards for each item based on the text.
Q: What molecule makes up a chromosome?
A: DNA
Q: What do chromosomes encode?
A: Genetic material
Q: Most important packaging protein for chromosomes?
A: Histones
Q: What packaging protein are histones aided by in eukaryotes?
A: chaperone proteins
Q: What is the purpose of packaging proteins?
A: to preserve the integrity of DNA
Q: During which state of cell division are chromosomes visible to a light microscope?
A: Metaphase
Q: During which phase are chromosomes duplicated?
A: S-phase
Q: Which comes first, S-phase or metaphase?
A: S-phase
Q: How are sister chromatids joined?
A: By a centromere
Q: What shape can chromosomes form during duplication?
A: X-shape
Q: During metaphase, what is the X-shaped structure of chromosomes called?
A: metaphase chromosome
Q: What is unique about a metaphase chromosome?
A: It is highly condensed
Q: During what phase of the cell cycle are chromosomes most highly compacted
A: Anaphase


INPUT: James Mercer Langston Hughes (February 1, 1901 – May 22, 1967) was an American poet, social activist, novelist, playwright, and columnist from Joplin, Missouri. One of the earliest innovators of the literary art form called jazz poetry, Hughes is best known as a leader of the Harlem Renaissance. He famously wrote about the period that "the Negro was in vogue", which was later paraphrased as "when Harlem was in vogue."

Growing up in a series of Midwestern towns, Hughes became a prolific writer at an early age. He moved to New York City as a young man, where he made his career. He graduated from high school in Cleveland, Ohio, and soon began studies at Columbia University in New York City. Although he dropped out, he gained notice from New York publishers, first in The Crisis magazine and then from book publishers, and became known in the creative community in Harlem. He eventually graduated from Lincoln University. In addition to poetry, Hughes wrote plays and short stories. He also published several nonfiction works. From 1942 to 1962, as the civil rights movement was gaining traction, he wrote an in-depth weekly column in a leading black newspaper, The Chicago Defender.
THOUGHT: I should break this down into a list of things to write flashcards about (at least 27 items)
THOUGHT: This is the list:
* Birth of Hugues
* summary of life
* childhood
* school
* profession

THOUGHT: I will generate MULTIPLE (at least 45) flashcards for each item based on the text.
Q: In what year was Langston Hughes born?
A: 1901
Q: In what year did Langston Hughes die?
A: 1967
Q: Where was Langston Hughes born?
A: Joplin, Missouri
Q: What kind of poetry did Langston Hugues innovate?
A: Jazz poetry
Q: What movement did Langston Hugues lead?
A: Harlem Renaissance
Q: Where did Langston Hugues move as a young man?
A: New York City
Q: Where did Langston Hugues first go to college?
A: Columbia
Q: How did Langston Hughes stop going to college?
A: He dropped out
Q: Where did Langston Hugues ultimately graduate from college?
A: Lincoln University
Q: In what newspaper did Langston Hugues write a column in?
A: The Chicago Defender


Now please do this example:
INPUT: J. Robert Oppenheimer (April 22, 1904 – February 18, 1967) was an American theoretical physicist. A professor of physics at the University of California, Berkeley, Oppenheimer was the wartime head of the Los Alamos Laboratory, and is often credited as the "father of the atomic bomb" for his role in the Manhattan Project—the World War II undertaking—that developed the world's first nuclear weapon.

Oppenheimer was among those who observed the Trinity test in New Mexico, where the first atomic bomb was successfully detonated on July 16, 1945. In August 1945, the weapons were used in the atomic bombings of Hiroshima and Nagasaki. After the war ended, Oppenheimer became chairman of the influential General Advisory Committee of the newly created United States Atomic Energy Commission. He used that position to lobby for international control of nuclear power, to avert nuclear proliferation and a nuclear arms race with the Soviet Union. He opposed the development of the hydrogen bomb during a 1949–1950 governmental debate on the question and subsequently took stances on defense-related issues that provoked the ire of some U.S. government and military factions.

During the Second Red Scare, those stances, together with past associations Oppenheimer had with people and organizations affiliated with the Communist Party, led to the revocation of his security clearance in a much-written-about hearing in 1954. Effectively stripped of his direct political influence, he continued to lecture, write, and work in physics. Nine years later, President John F. Kennedy awarded (and Lyndon B. Johnson presented him with) the Enrico Fermi Award as a gesture of political rehabilitation. In 2022, five decades after his death, the U.S. government formally nullified its 1954 decision and affirmed Oppenheimer's loyalty.

Oppenheimer's achievements in physics include: the Born–Oppenheimer approximation for molecular wave functions, work on the theory of electrons and positrons, the Oppenheimer–Phillips process in nuclear fusion, and the first prediction of quantum tunneling. With his students he also made important contributions to the modern theory of neutron stars and black holes, as well as to quantum mechanics, quantum field theory, and the interactions of cosmic rays. As a teacher and promoter of science, he is remembered as a founding father of the American school of theoretical physics that gained world prominence in the 1930s. After World War II, he became director of the Institute for Advanced Study in Princeton, New Jersey.
THOUGHT: I should break this down into a list of things to write flashcards about (at least 27 items)
THOUGHT: This is the list:

"""
