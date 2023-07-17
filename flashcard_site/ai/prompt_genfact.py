SYSTEM = """
You are an AI designed to take a paragraph and turn it into CONTEXT INDEPENDENT facts.
If the paragraph references something that is not in it (maybe using words like 'these' 'this' or 'it'), just ignore it.
Also ignore meta-references like the text (or book, ...) referencing itself.

Here's an example of what you will do:
---
INPUT:
The other tendency of atoms is to maintain a neutral charge. Only the noble gases (the elements on the right-most column of the periodic table) have zero charge with filled valence octets. All of the other elements have a charge when they have eight electrons all to themselves. The result of these two guiding principles is the explanation for much of the reactivity and bonding that is observed within atoms: atoms seek to share electrons in a way that minimizes charge while fulfilling an octet in the valence shell. 
OUTPUT:
Atoms tend to maintain a neutral charge.
The only elements that have zero charge with filled valence octets are the noble gasses.
The noble gasses are on the right-most column of the periodic table.
Every element other than the noble gasses have a charge when they have eight electrons to themself.
---
(Notice how I ignored "these guiding principles" since it referenced something not in the paragraph (we only got one guiding principle))
"""
USER1 = """
Objectivism is a philosophical system of thought first developed by the novelist and philosopher Ayn Rand. Objectivism aims to provide the student with a philosophy that is both broadly applicable and based on systematic rational thought that is free of subjective judgement. Rand's work on Objectivism is highly controversial and has not been adopted widely within the philosophical community. This book will attempt to present Rand's arguments fairly but will also cover criticisms of Objectivism. 
"""
ASS1 = """
Ayn Rand developed objectivism.
Objectivism is a philosophical system of thought.
Objectivism is broadly applicatble.
Objectivism is free of subjective judgement.
Objectivism is based on rational thought.
Objectivism is a controversial philosophy.
"""
USER2 = """
Plato was born into an Athenian aristocratic family around 427/428 BC. His father Ariston was said to be an ancestor of the last king of Athens, Crodus and his mother Perictione was a relation of the Greek politician Solon. There is not much external information about Plato's early life and most of what we know has come from his own writings. His father died when Plato was young and his mother was remarried to her uncle Pyrilampes. It is very likely that Plato knew Socrates from early childhood. Perictione's cousin Critias and her brother Charmides are known to have been friends with Socrates and they themselves were part of the oligarchic leadership of 404 BC. These connections should have led to a political career for Plato but at some stage he made a decision not to enter political life. The oligarchic leadership collapsed and democracy was restored and considering that Plato's family members had been part of the oligarchic terror must have meant that his position in Athenian society was under scrutiny. The condemning to death of Socrates by the democracy seems to have been the final political act of the state that forced Plato into exile at Megara. Plato is known to have taken refuge with Eucleides, founder of the Megarian school of philosophy and it is stated by later historians that during this period in his life he travelled extensively through Greece, Italy and Egypt. Whether these journeys took place is disputed but it is known that Plato did travel to Sicily where he met Dion, brother-in-law of the ruler of Syracuse, Dionysius I.    
"""
ASS2 = """
Plato was born into an Athenian aristocratic family.
Plato was born around 427/428 BC.
Plato's father was Ariston.
Plato's father was said to be an ancestor of the last king of Athens.
The last king of athens was Crodus.
Plato's mother was Perictione.
"""
