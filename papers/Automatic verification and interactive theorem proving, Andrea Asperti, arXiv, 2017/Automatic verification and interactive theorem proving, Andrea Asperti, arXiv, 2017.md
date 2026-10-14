                                           AUTOMATIC VERIFICATION AND INTERACTIVE
                                                     THEOREM PROVING


                                                                      ANDREA ASPERTI

                                               Dipartimento di Informatica: Scienza e Ingegneria - DISI
                                                                Università di Bologna
arXiv:1701.03602v1 [cs.LO] 13 Jan 2017




                                                 Sommario. Automatic verification deals with the validation by
                                                 means of computers of correctness certificates. The related tools,
                                                 usually called proof assistant or interactive provers, provide an in-
                                                 teractive environment for the creation of formal certificates who-
                                                 se correctness can be assessed in a purely automatic way. Such
                                                 systems have applications both in mathematics, where certificates
                                                 are proofs of theorems, and in computer science, where certifica-
                                                 tes testify the correctness of a given software with respect to its
                                                 specification.


                                                                       1. Introduzione
                                            Esiste un interessante sito web1 curato da G.J.Woeginger che racco-
                                         glie oltre un centinaio di contributi di autori che asseriscono di risolvere
                                         in un senso o nell’altro (!) il problema dell’uguaglianza tra le classi di
                                         complessità P e N P . Come è noto questo è uno dei cosiddetti problemi
                                         del Millennio: non ci si aspetta che ammetta una soluzione semplice
                                         e verificarne la correttezza può essere difficile e dispendioso. Nessu-
                                         no dei lavori contenuti nella lista di Woeginger è stato pubblicato su
                                         riviste peer reviewed e/o di elevata reputazione scientifica. Tuttavia,
                                         gli autori non sono degli sprovveduti, ma ricercatori di notevole espe-
                                         rienza, e frequentemente docenti universitari della materia in oggetto
                                         o di settori affini.
                                            E-mail address: andrea.asperti@unibo.it.
                                           To appear in “Direzioni della ricerca logica in Italia, vol 2. H.Hosni, G.Lolli,
                                         C.Toffalori eds.
                                           1
                                            https://www.win.tue.nl/~gwoegi/P-versus-NP.htm
                                                                                  1
2 AUTOMATIC VERIFICATION AND INTERACTIVE THEOREM PROVING

   Sarebbe bello poter disporre di uno strumento automatico a cui da-
re in pasto questi articoli, e che rispondesse asserendo la correttezza o
meno delle argomentazioni addotte. Questo è profondamente diverso
dal cercare di dimostrare automaticamente l’uguaglianza P = N P . Se
abbiamo un sistema logico con un minimo di espressività la ricerca di
una dimostrazione non è un problema decidibile, ma il problema di
determinare se un termine di prova p è sintatticamente corretto, e in
tal caso se rispetta un determinato enunciato P (useremo la notazio-
ne p : P per esprimere che p è una dimostrazione di P ) è non solo
decidibile, ma anche relativamente semplice, almeno da un punto di
vista concettuale2: si tratta di seguire passo passo la dimostrazione e
verificare localmente che non siano stati fatti errori nell’applicazione
delle regole logiche. Il problema della dimostrazione automatica è in
effetti un problema di ricerca nello spazio delle prove, che presuppone
la possibilità di verificare che la prova sia corretta.
       Verifica Automatica       Dimostrazione Automatica
   p è una dimostrazione di P ?   esiste p che dimostra P ?
   La dicotomia ricerca vs. verifica è uno dei leit-motif dell’informati-
ca: verificare può essere semplice, mentre cercare è, di solito, molto più
complicato. Per esempio, i problemi in N P sono quei problemi deci-
sionali che ammettono un algoritmo efficiente (polinomiale) di verifica
della risposta per mezzo di un certificato di dimensione polinomia-
le nella dimensione dell’input. La ricerca di una soluzione mediante
tecniche di generate-and-test che generano in modo esaustivo tutti i
potenziali certificati e ne verificano la correttezza, fornisce tipicamente
algoritmi deterministici di complessità esponenziale. Tuttavia, molti
problemi in N P hanno anche degli algoritmi ad hoc di ricerca efficienti:
questi sono i problemi in P .
   Se dunque si ammette che la verifica sia un problema relativamen-
te semplice (almeno rapportato alla dimostrazione automatica) che
cosa rende interessante questa area di ricerca e complicati i relativi
strumenti di elaborazione?
   La complessità deriva non dal tool di verifica, che è una piccola
componente di solito chiamata “kernel” (si veda ad esempio [7]), ma
dall’ambiente di sviluppo fornito all’utente per lo sviluppo assistito e
    2La complessità pratica del problema dipende molto dal sistema logico di
riferimento e dalla nozione di prova
  AUTOMATIC VERIFICATION AND INTERACTIVE THEOREM PROVING 3

interattivo delle dimostrazioni [8]. È questo ambiente che fa si che,
mediante l’uso di proof assistants, si possano certificare prove di no-
tevole difficoltà, come il teorema di Feit-Thompson sui gruppi finiti
[33], o garantire la correttezza di componenti software particolarmen-
te complessi e delicati, come compilatori [57], parti di sistemi operativi
[50], sistemi di controllo per applicazioni critiche [61] o strumentazioni
hardware [39].
   La prospettiva rispetto alla deduzione automatica è a questo punto
completamente rovesciata. L’ambiente di sviluppo è uno strumento
che permette di costruire dimostrazioni complesse a partire da dimo-
strazioni più semplici sotto la guida dell’utente. Parte delle dimostra-
zioni più semplici, o parte di quelle manipolazioni logico-algebriche che
semplificano la combinazione dei risultati (ad esempio, adattamento
di strutture a meno di semplici isomorfismi o istanziazioni), posso-
no essere delegate a strumenti automatici di ricerca. Il dimostratore
interattivo permette dunque di combinare svariate tecniche di prova
(di solito chiamate tattiche), tra cui anche tecniche di dimostrazione
automatica. Mentre la verifica automatica è un ovvio presupposto
per la deduzione automatica, quest’ultima è solo una componente nel
variegato campo della dimostrazione interattiva.




       Figura 1. L’universo della dimostrazione assistita. La
       nuvola di parole è stata calcolata in base al contenuto
       di alcuni siti web specializzati su questo argomento.
4 AUTOMATIC VERIFICATION AND INTERACTIVE THEOREM PROVING




                    2. Dimostrazione formale
   Torniamo al caso dell’autore della dimostrazione di P = N P , proba-
bilmente frustrato dalla scarsa considerazione ottenuta nell’ambiente
scientifico dal proprio risultato. Quello che potrebbe fare, con uno
sforzo sicuramente comparabile alla rilevanza del problema, sarebbe
di formalizzare il risultato in uno degli svariati tool di dimostrazio-
ne interattiva esistenti e autenticare formalmente la correttezza della
propria argomentazione.
   Questo ci porta al problema cruciale: cosa intendiamo con dimo-
strazione formale e quanto è difficile passare da una dimostrazione
“cartacea” ad una completamente formale e verificabile tramite un
computer?
   Una dimostrazione formale è semplicemente una dimostrazione che
possa essere letta ed elaborata da una macchina. Il linguaggio ma-
tematico è spesso considerato rigoroso, ma non ha quella turgidità
sintattica propria dei linguaggi formali, ed in particolare dei linguag-
gi di programmazione, che semplifica enormemente la comunicazione
tra uomo e macchina. Questo è il primo passo importante: si deve
accettare l’idea di riscrivere la dimostrazione in un linguaggio forma-
le, e che l’apprendimento di questo linguaggio potrebbe richiedere un
certo sforzo (comparabile, indicativamente, allo sforzo di apprendere
un nuovo linguaggio di programmazione).
   Questo spiega anche la presunta cripticità delle dimostrazioni for-
mali: il linguaggio delle prove di queste applicazioni non è inteso per
la comunicazione inter-umana, ma per la comunicazione tra l’uomo e
la macchina. Un utente esperto è in grado di interpretare questo lin-
guaggio, possibilmente in un dialogo interattivo con la macchina, ma il
significato resterà essenzialmente opaco ai non addetti ai lavori. Allo
stesso modo, in informatica, l’algoritmo è celato dietro al programma,
e chi non conosce il particolare linguaggio di programmazione in uso
avrà inevitabilmente difficoltà a interpretare il significato di un certo
codice e ricostruirne l’algoritmo.
   La dimostrazione matematica sta alla sua controparte formale esat-
tamente come l’algoritmo sta ad un programma che lo implementa.
   Il problema è a volte presentato in relazione al duplice ruolo del-
le dimostrazioni: quello di certificato e quello di messaggio. È stata
  AUTOMATIC VERIFICATION AND INTERACTIVE THEOREM PROVING 5

recentemente avanzata l’ipotesi [60] che l’avvento dei dimostratori au-
tomatici conduca a un sostanziale divorzio di questi due ruoli (non è
chiaro se l’autore interpretasse questo fenomeno in senso positivo o ne-
gativo). In realtà, se da un lato è indubbiamente interessante separare
queste due funzioni della nozione di prova, è altrettanto importan-
te mantenere un allineamento tra di esse, problematica sicuramente
centrale allo sviluppo del settore della dimostrazione interattiva.
  Per meglio approfondire questa problematica, dobbiamo fare riferi-
mento ai due principali stili di scrittura delle dimostrazioni utilizzati
dai dimostratori interattivi, quello procedurale e quello dichiarativo,
che andiamo ad analizzare nella prossima sezione.

2.1. Stile dichiarativo e stile procedurale. Una dimostrazione è
un procedimento (giustificazione) che permette di ricavare una conclu-
sione C a partire da un insieme di premesse A1 , . . . An . La dimostra-
zione può tipicamente essere decomposta in una sequenza di passi più
semplici, fino ad arrivare a un insieme di passi elementari non ulterior-
mente scomponibili, che costituiscono le regole logiche fondamentali
del ragionamento deduttivo, caratteristiche del particolare sistema lo-
gico adottato. Le regole logiche sono casi particolari di dimostrazioni
la cui validità viene assunta assiomaticamente e dunque non richiedo-
no ulteriore giustificazione se non la semplice menzione della regola
invocata. Ad esempio, una regola di introduzione della congiunzione,
chiamiamola ∧I , permette di concludere A∧B a partire dalle premesse
A e B:
                                       A      B
                                  ∧I :
                                        A∧B
Dovrebbe essere chiaro che c’è una certa ridondanza nella nozione
suddetta di regola logica: conoscendo premesse e conclusione esiste
abitualmente una sola regola logica che giustifica il passo deduttivo,
facilmente individuabile dalla macchina; inoltre, e questo è molto più
interessante, conoscendo il nome della regola applicata si conosce la
relazione strutturale tra premesse e conclusione, e quindi si possono
inferire automaticamente le une dalle altre.
   Questo ci porta alla definizione delle due classi principali di linguag-
gi di specifica di dimostrazioni: dichiarativi o procedurali. Nell’acce-
zione di Hilbert, una dimostrazione di Pn , è una sequenza di formule
P1 , . . . , Pn dove ogni Pi è una ipotesi oppure si ottiene da formule che
6 AUTOMATIC VERIFICATION AND INTERACTIVE THEOREM PROVING

precedono Pi nella sequenza per mezzo di una specificata regola logi-
ca. Tuttavia, come spiegato precedentemente, per definire la prova è
sufficiente fornire la sequenza delle regole applicate (descrizione pro-
cedurale) lasciando implicita la sequenza delle formule, oppure fornire
la sequenza P1 , . . . , Pn dei passi intermedi delegando al sistema il sem-
plice compito di inferire per conto proprio le regole logiche applicate
nei singoli passi (descrizione dichiarativa).
   La differenza tra linguaggi procedurali e dichiarativi e i vantaggi de-
gli uni rispetto agli altri possono essere capiti meglio con una semplice
analogia con il gioco degli scacchi (ripresa da [2]).
   Una partita di scacchi può essere descritta essenzialmente in due
modi: mediante una sequenza di mosse o mediante una sequenza di
posizioni che descrivono lo stato dei pezzi sulla scacchiera (si veda la
Figura 2).




Figura 2. Mosse (stile procedurale) e Posizioni (stile dichiarativo)



  Nel primo caso, le posizioni sono implicite: esse possono essere ri-
costruite in modo univoco a partire dalla sequenza delle mosse. Nel
secondo caso, le mosse sono implicite, e possono essere dedotte dalla
  AUTOMATIC VERIFICATION AND INTERACTIVE THEOREM PROVING 7

differenza tra due posizioni successive. Mosse e posizioni sono rispet-
tivamente esempi di un linguaggio procedurale e di uno dichiarativo.
   I meriti relativi dei due approcci dovrebbero essere evidenti. La
descrizione procedurale è estremamente compatta ma piuttosto illeg-
gibile: ogni mossa fa implicito riferimento alla posizione raggiunta
mediante le mosse precedenti. Per seguire una descrizione procedura-
le bisognerebbe essere in grado di immaginare le configurazioni inter-
medie risultanti dall’esecuzione di ogni singolo passo. Nel caso degli
scacchi i giocatori esperti riescono abitualmente a farlo, visto che le
mosse sono operazioni abbastanza elementari e le partite non sono
mai troppo lunghe. Tuttavia, nel caso delle dimostrazioni, questo è
molto più complicato. Nella maggior parte dei casi, le dimostrazioni
in stile procedurale sono praticamente inintelleggibili per l’uomo: il
punto cruciale è che non sono pensate per essere lette, ma per essere
replicate interattivamente al computer (cosi come si può sviluppare la
partita di scacchi su una scacchiera eseguendo passo passo le mosse
descritte a partire dalla configurazione iniziale).
   D’altra parte, le descrizioni procedurali forniscono, ad ogni istante,
una descrizione esplicita e completa dello stato corrente. L’evoluzione
futura non dipende dal passato, e ci si può concentrare interamente
sul presente. Le descrizioni dichiarative sono dunque tipicamente più
leggibili di quelle procedurali, ma anche molto più prolisse, al punto
da diventare spesso tediose per l’utente.

2.2. Un esempio concreto. Per confrontare i due metodi facciamo
un semplice esempio di applicazione dell’analisi per casi sui numeri
naturali (una forma degenere dello schema di induzione):

                              P (0)∀x.P (S(x))
                        (∗)
                                   P (t)
  Supponiamo che l’obiettivo (il nostro goal corrente G) sia dimostrare
che ogni numero naturale n diverso da zero è il successore di un qualche
naturale m

                     (G) n 6= 0 → ∃m, S(m) = n
  Si vuole procedere per casi su n, intenzione che, in un linguaggio
procedurale, si traduce tipicamente nel semplice comando
                                  cases n
8 AUTOMATIC VERIFICATION AND INTERACTIVE THEOREM PROVING

Innanzitutto, il sistema capisce dal tipo di n il tipo di analisi da effet-
tuare, e che in questo caso il principio da utilizzare è (∗). Tuttavia,
(∗) è uno schema, per cui il problema successivo è capire quale è la
proprietà P a cui si fa riferimento. Questa viene inferita in modo
automatico a partire da G astraendo rispetto alle occorrenze sintat-
tiche del termine n (che potrebbe essere un termine complesso, non
necessariamente una variabile). Il predicato che si ottiene è:
                    P = λn.n 6= 0 → ∃m, S(m) = n
Utilizzando questo predicato, il sistema ricostruisce per semplice istan-
ziazione le due ipotesi corrispondenti alle premesse di (*), riducendo
quindi G ai due sottogoal seguenti:
                (G1 ) (0 6= 0 → ∃m, S(m) = 0
                (G2 ) ∀x, S(x) 6= 0 → ∃m, S(m) = S(x)
che è quanto ci aspettavamo.
   Questo passo di dimostrazione in linguaggio procedurale è dunque
interamente racchiuso nel comando “cases n”, dove n fa implicitamente
riferimento al goal corrente G. La stessa dimostrazione in linguaggio
dichiarativo è descritta dalla sequenza dei goals G1 , G2 , G, possibil-
mente decorati con del testo aggiuntivo, sia per ragioni di leggibilità
che per semplificare il lavoro di verifica. Ad esempio:
             (G1 ) (0 6= 0 → ∃m, S(m) = 0
             (G2 ) ∀x, S(x) 6= 0 → ∃m, S(m) = S(x)
             By case analysis from G1 and G2 we obtain
             (G) n 6= 0 → ∃m, S(m) = n
2.3. Breve storia. I sistemi di prova procedurali discendono da uno
strumento dei primi anni settanta ideato dal premio Turing Robin
Milner e denominato LCF [35], un acronimo per Logic of Computable
Functionals (si veda anche la sottosezione 3.2, più avanti). Tali sistemi
hanno una nozione di “stato corrente della prova” che consiste in un
insieme di cosiddette “proof obligations” corrispondenti ai sottogoal
pendenti che ancora devono essere dimostrati. Lo stato è trasformato
mediante le cosiddette tattiche che prendono un goal e lo riducono a un
insieme (possibilmente vuoto) di sottogoal più semplici. La dimostra-
zione comincia con l’asserto da dimostrare come unica obbligazione e
termina quando non resta nessun sottogoal aperto. A questo punto
la dimostrazione può essere salvata in memoria e diventa utilizzabile
  AUTOMATIC VERIFICATION AND INTERACTIVE THEOREM PROVING 9

per usi futuri. Per via del processo di prova, che parte dall’asserto
finale e procede riducendo via via goal complessi a goal più semplici,
le dimostrazioni procedurali vengono tipicamente costruite all’indietro
(backward), dalla conclusione verso le ipotesi.
   Il primo linguaggio ad adottare uno stile dichiarativo è stato il si-
stema di prova Mizar [71, 38], sviluppato fin dai primi anni settanta
dal logico polacco Trybulec, recentemente scomparso. Il linguaggio
di Mizar è stato espressamente studiato per essere comprensibile al-
l’uomo, pur mantenendo un livello di formalità sufficiente per essere
decifrabile dalla macchina.
   Mizar era poco noto in occidente. In seguito ad una sua visita al
gruppo di Trybulec in Bialystok, J.Harrison, sviluppatore di HOL-
light, provò a ideare uno stile di prova procedurale per il proprio proof
assistant, detto appunto Mizar-mode [43], che contribuı̀ in modo note-
vole a popolarizzare questo stile di scrittura delle dimostrazioni. Molti
altri strumenti nati in forma procedurale hanno in seguito sviluppa-
to intefacce in grado di gestire prove scritte in forma dichiarativa: si
veda ad esempio [26] per COQ, [24] per Matita, o il linguaggio Isar
[75] per Isabelle. Quest’ultimo è probabilmente, al momento attuale,
l’esempio più compiuto di linguaggio dichiarativo, ed ha praticamente
soppiantato lo stile procedurale nell’ambito degli utenti di Isabelle. Si
vedano anche i seguenti lavori per un interessante raffronto fra i vari
linguaggi: [76, 44].
   Come dovrebbe essere chiaro dalla descrizione che abbiamo fatto
e dai risultati precedenti, la distanza tra linguaggi procedurali e di-
chiarativi non è cosi ampia come potrebbe apparire a prima vista: in
realtà sono complementari uno all’altro e si integrano bene insieme
[77, 49, 78]. Da uno script procedurale è possibile di solito ricostruire
in modo automatico una versione dicharativa apprezzabile, cosı̀ co-
me, in linea di principio, sarebbe possibile riassumere una descrizione
procedurale in forma dicharativa (poco esplorato, e forse poco utile).
   Tuttavia, più che una integrazione tra i due stili, l’obiettivo proba-
bilmente più importante per l’approccio procedurale è quello di arri-
vare ad una descrizione maggiormente strutturata delle dimostrazioni,
mirata non tanto ad incrementarne la leggibilità, quanto la loro ma-
nutenzione e il loro aggiornamento. Questa tendenza è chiaramente
testificata dai tool più recenti come Ssreflect [34] e Matita [5, 6].
10 AUTOMATIC VERIFICATION AND INTERACTIVE THEOREM PROVING

2.4. Obiettivi comuni, strategie contrastanti. L’obiettivo comu-
ne, sia per l’approccio procedurale che per quello dichiarativo è un
progressivo aumento della granularità della dimostrazione, il che cor-
risponde essenzialmente ad un potenziamento delle regole logiche.
   Nel caso dell’approccio procedurale, la regola logica viene inferita
in modo automatico dal sistema, quindi l’obiettivo è un aumento delle
sue capacità di dimostrazione automatica, o in alternativa la sua inte-
roperabilità con sistemi esterni cui delegare la sintesi di questi passi
di dimostrazione. La tematica è cosi descritta in [18]:
       The main ingredients underlying this approach are ef-
       ficient automatic theorem provers that can cope with
       hundreds of axioms, suitable translations of richer lo-
       gics to their formalisms, heuristic and learning methods
       that select relevant facts from large libraries, and me-
       thods that reconstruct the automatically found proofs
       inside the proof assistants.
Lo scopo finale è quello di descrivere la prova come un elenco (pos-
sibilmente strutturato) di un certo numero di passi intermedi parti-
colarmente significativi, eventualmente inframezzato da annotazioni
che aiutino l’automazione a sintetizzare la prova. Queste annotazioni
protrebbero essere semplicemente un elenco dei risultati utili a comple-
tare la prova: “otteniamo P mediante H1 , . . . Hn ”. Queste permette
al dimostratore automatico di confinare lo spazio di ricerca all’interno
delle librerie dei risultati noti, che potrebbe altrimenti risultare trop-
po ampio. Questo settore è al momento attuale uno dei più vivaci
e promettenti, con particolare riferimento all’uso di tecniche di ap-
prendimento automatico per migliore le prestazioni dei dimostratori
[73, 48].
   Nel caso dell’approccio dichiarativo, i passi di prova sono le tattiche,
ovvero i comandi che l’utente utilizza per procedere nella dimostrazio-
ne e ridurre un goal a goal più semplici. Aumentare la granularità
significa concepire tattiche via via più espressive, potenti e generali.
Dei particolari costrutti, detti tatticali permettono di combinare assie-
me tattiche per generare comandi ancora più espressivi. Determinati
sistemi permettono inoltre agli utenti di definire le proprie tattiche,
fornendo della applicative user interfaces per la manipolazione dei ter-
mini di prova. In molti casi, questi linguaggi sono utilizzati per costrui-
re dei dimostratori automatici specifici per un determinato dominio,
  AUTOMATIC VERIFICATION AND INTERACTIVE THEOREM PROVING 11

in contrasto con le tecniche generali dell’approccio procedurale.
    Un’altra importante tematica di sviluppo dei linguaggi procedurali
è il progressivo uso della riflessione [21, 14] per ridurre passi logici a
semplici problemi computazionali. Per fare un esempio, supponiamo
che l’uguaglianza tra elementi di un certo tipo A sia decidibile, cioè
che si disponga di un algoritmo di decisione eqA : A → A → bool e
supponiamo di avere dimostrato la sua correttezza, ovvero che
                  ∀x, y : A, eqA (x, y) = true ⇔ x = y
Allora possiamo riflettere la dimostrazione di uguaglianza tra due ele-
menti a e b di tipo A sul semplice calcolo di eqA (a, b). Questo è un
tipico esempio di small scale reflection, promosso da [34]. Qualunque
predicato decidibile da luogo a una forma interessante di riflessione.
   Le complesse tattiche di prova correntemente utilizzate nei dimo-
stratori procedurali sembrano difficilmente rimpiazzabili da procedure
automatiche generaliste. Nonostante l’innegabile appealing dello stile
dichiarativo non è al momento immaginabile che questo possa com-
pletamente soppiantare lo stile procedurale, soprattutto nell’ambito
delle applicazione all’informatica (verifica di proprietà di componenti
software o hardware).
                    3. Il quadro fondazionale
   Il sistema logico fondazionale utilizzato dal sistema interattivo di di-
mostrazione ha un ruolo più marginale di quanto si possa immaginare.
La ragione di questo fatto è che tra l’utente e il livello fondazionale
possono essere aggiunti svariati livelli intermedi che permettono di
lavorare ad un livello di astrazione maggiore rispetto al formalismo
inevitabilmente grezzo, pedante e prolisso fornito dal sistema logico di
base.
   Per fare una analogia con i linguaggi di programmazione, il pa-
radigma fondazionale fornisce un linguaggio di basso livello, atto a
essere eseguito su strutture hardware, ma di difficile utilizzo da parte
dell’uomo. In informatica, i sistemi operativi permettono di astrarre
dall’architettura fisica del sistema, virtualizzando i suoi componenti,
e i compilatori permettono di astrarre dal linguaggio macchina di bas-
so livello, consentendo all’utente di scrivere programmi in linguaggi
molto più evoluti. Allo stesso modo, ogni proof assistant fornisce un
linguaggio di prova “di alto livello” e un complesso sistema di astra-
zioni che tendono a sopperire alle inevitabili lacune e restrizioni del
12 AUTOMATIC VERIFICATION AND INTERACTIVE THEOREM PROVING

quadro fondazionale, e al tempo stesso diminuire la dipendenza da
esso.

               hardware = sistema logico fondazionale

   L’osservazione precedente fa cadere l’obiezione principale abitual-
mente addotta per sostenere l’impossibilità pratica di un approccio
strettamente formale alla matematica (si veda ad esempio [28]), de-
rivante dall’eccessiva lunghezza delle dimostrazioni in oggetto. Bour-
baki stesso, pur essendo considerato un fautore di un approccio mag-
giormente formale alla matematica [54], riteneva che il progetto di una
completa formalizzazione di questa disciplina fosse assolutamente ir-
realizzabile, e non per ragioni di incompletezza ma di pura dimensione
delle dimostrazioni [20]:
       the tiniest proof at the beginning of the Theory of Sets
       would already require several hundreds of signs for its
       complete formalization.
Come osservato in [3], l’argomentazione ricorda la generale mancanza
di fiducia nella possibilità di scrivere programmi per svolgere compiti
complessi tipica della della prima metà degli anni cinquanta, nel pe-
riodo antecedente alla costruzione dei primi compilatori e all’avvento
dei linguaggi di programmazione di alto livello. Per citare Harrison
[45]:
       the arrival of the computer changes the situation dra-
       matically. [...] checking conformance to formal rules is
       one of the things computers are very good at. [...] the
       Bourbaki claim that the transition to a completely for-
       mal text is routine seems almost an open invitation to
       give the task to computers.
   Allo stato attuale dell’arte, la presunta lunghezza delle dimostrazio-
ni formali non rappresenta più un ostacolo, come ampiamente dimo-
strato dalla completa formalizzazione e verifica automatica della cor-
rettezza di risultati matematici complessi come la distribuzione asinto-
tica dei numeri primi [10], il teorema dei quattro colori [32], il teorema
della curva di Jordan [42] o il già citato teorema di Feit-Thompson sui
gruppi finiti [33].
  AUTOMATIC VERIFICATION AND INTERACTIVE THEOREM PROVING 13

3.1. Teoria degli insiemi vs. Teoria dei tipi. Benchè per l’uten-
te finale il quadro fondazionale non sia (o non dovrebbe essere) cosı̀
rilevante, è comunque interessante, anche per ragioni storiche, fare un
piccolo escursus sui sistemi logici tipicamente adottati dai dimostrato-
ri interattivi. Questo ci permetterà anche di discutere e capire meglio
l’architettura complessiva dei diversi sistemi.
   È opinione diffusa che il “vero” fondamento della matematica sia
la teoria degli insiemi, tuttavia non esiste una ragione profonda a
supporto di questa tesi, ed è significativo osservare che la quasi totalità
dei sistemi di prova interattivi, con l’unica eccezione di Mizar, non si
basano su questa teoria fondazionale.
   Le ragioni di questo fatto non sono facilmenti individuabili e sicu-
ramente ci sono anche delle importanti motivazioni storiche, dovute
al particolare momento in cui questi sistemi sono stati sviluppati, alle
tematiche che si stavano approfondendo, e ai gruppi di ricerca a cui
appartenevano gli sviluppatori, o di cui subivano l’influenza.
   Volendo cercare una motivazione generale che rende la teoria degli
insiemi poco attraente dal punto di vista della verifica formale, il punto
nodale riguarda probabilmente il concetto di funzione. In teoria degli
insiemi una funzione non è che un caso particolare di relazione, tota-
le e univoca. Questo è in apparente contrasto con la centralità della
nozione di funzione, sia in matematica che, forse ancor più, in infor-
matica (dove, ai fini della verifica, la funzione è l’oggetto principale del
discorso). È naturale voler disporre di un framework logico-linguistico
di base che permetta la definizione e la manipolazione più semplice
possibile di queste entità.
   Una caratteristica comune a tutti i moderni sistemi di prova inte-
rattivi è l’utilizzo di logiche di ordine superiore. I vari sistemi si diffe-
renziano tuttavia per le forme variegate che possono assumere questi
sistemi logici, dalla teoria dei tipi semplici di Church, ai vari sistemi
intuizionisti, predicativi o impredicativi, con sottotipi, tipi dipenden-
ti, e via dicendo. Questa pletora di sistemi, tanto simili uno all’altro
e tuttavia praticamente incompatibili tra loro è una delle principali
ricchezze/disgrazie di questa area di ricerca.

3.2. LCF e la famiglia HOL. Un primo gruppo di dimostratori è
quello che appartiene alla famiglia HOL (si veda [36, 37] per delle inte-
ressanti rassegne storiche). I sistemi di questa famiglia si isipirano alla
Logic of Computable Functionals (LCF) di Milner [35], che racchiude il
14 AUTOMATIC VERIFICATION AND INTERACTIVE THEOREM PROVING

sistema logico all’interno di un metalinguaggio programmabile (nel ca-
so di Milner, il linguaggio ML). I termini e le formule sono espressioni
del linguaggio, che possono essere manipolate liberamente. I teoremi
sono valori di un particolare tipo di dato astratto, i cui metodi sono
le regole di base del sistema logico. Fintanto che solo queste funzioni
sono utilizzate per costruire nuovi teoremi (cosa che può essere veri-
ficata dal sistema dei tipi del metalinguaggio di programmazione) si
ha la garanzia di correttezza delle deduzioni fatte. Questo per quanto
riguarda la costruzione in avanti delle dimostrazioni. Per supportare
il ragionamento all’indietro, si implementano goals e tattiche sul tipo
di dato astratto. Ogni tattica verifica che il goal in input ha la for-
ma sintattica che ci si attende, genera i nuovi sottogoals e sintetizza la
funzione di validazione che giustifica la conclusione a partire dalle pre-
messe. Funzioni di validazione e tattiche sono dunque essenzialmente
inverse le une alle altre. La dimostrazione (validazione) non è di per
sè un oggetto sintattico del linguaggio, ma un programma: può essere
eseguito, ma non ispezionato. Le tattiche possono essere combinate
assieme mediante dei costrutti più complessi, detti tatticali, che con-
sentono di implementare passi logici di notevole complessità. L’utente
è incoraggiato a scrivere le proprie tattiche e i propri tatticali, spesso
caratteristici del particolare ambito in cui si sta lavorando.
    Ogni sistema logico può essere implementato in questa forma, ma
la famiglia HOL si caratterizza appunto dal fatto di adottare come
paradigma fondazionale varianti della logica di ordine superiore basate
sulla teoria dei tipi semplici di Church.


3.3. Isabelle. Isabelle è un framework logico originariamente svilup-
pato da Paulson a Cambridge verso la fine degli anni 80. La concezione
di Isabelle deriva dallo sforzo di aggiungere al modello architetturale
di LCF una visione maggiormente integrata della dimostrazione. In
particolare, i sottogoal generati da una tattica possono condividere
informazioni (ad esempio termini non ancora instanziati) richiedendo
una nozione di metavariabile “esistenziale” e la gestione delle opera-
zioni rilevanti associate a questa, a partire dalla nozione di unifica-
zione. La conseguenza è quella di spostare l’attenzione dalla nozione
di teorema (centrale all’approccio LCF) verso quella di sequente, in
particolare in relazione alle regole di inferenza.
   Mentre nell’approccio LCF ogni regola di inferenza è implicitamente
  AUTOMATIC VERIFICATION AND INTERACTIVE THEOREM PROVING 15

rappresentata da una funzione per la sua applicazione in avanti (va-
lidazione) e da una per la sua applicazione all’indietro (tattica), in
Isabelle, ogni regola di inferenza è descritta da una clausola di Horn.
Le regole logiche si compongono (istanziandosi) mediante il mecca-
nismo di risoluzione, senza bisogno di differenziare tra il loro uso in
avanti o all’indietro.
   Un sistema di ordine superiore minimale, chiamato M , è utilizza-
to come framework sintattico in cui esplicitare le regole. Isabelle è
un esempio di Logical Framework: per poter utilizzare lo strumen-
to concretamente bisogna prima istanzianziarlo su una qualche logica
più espressiva e quindi lavorare all’interno di questa (detta logica og-
getto, per distinguerla dalla meta-logica di Isabelle). La versione at-
tualmente più utilizzata di Isabelle è Isabelle-HOL, che utilizza HOL
come logica oggetto, estesa con un nucleo assiomatico per permette-
re ragionamenti di tipo set-theoretic; esistono però delle librerie per
constructive type theory (CTT) e Zermelo Fraenkel Set Theory.
   Per concludere, la differenza tra Isabelle e HOL può essere essen-
zialmente riassunta nella seguente frase di Paulson [67]:
        I have criticized LCF for representing inference rules as
        functions, preferring visible structures. But colleagues
        have pointed out that such structures are essentially the
        theorems of a (meta) logic, and the functions that ma-
        nipulate them are (meta) rules. Thus Isabelle adopts
        LCF’s representation at the meta-level.


3.4. Teoria dei Tipi. L’altro grande filone di dimostratori interattivi
è quello che si ispira alla teoria dei tipi, ed in particolare alle cosiddette
teorie costruttive. Appartengono a questa categoria Coq [17], Agda
[22], Matita [6], e benchè in forma leggermente differente, Nuprl [25].
    Queste applicazioni sono il risultato di un fecondo lavoro di ricerca
che a partire dagli anni settanta ha coinvolto, in strettissima sinergia
tra di loro, teoria delle categorie, costruttivismo e lambda calcolo (si
vedano ad esempio [62, 53, 30] per una introduzione all’argomento).
Questa relazione è tutt’altro che esaurita, come dimostrano le recenti
scoperte nel campo della Homotopy Type Theory (HoTT) [72] pro-
mossa da Voevodsky, vincitore di una medaglia Field per i suoi lavori
sulle coomologie algebriche.
16 AUTOMATIC VERIFICATION AND INTERACTIVE THEOREM PROVING

   Dal punto di vista della verifica formale, i punti salienti dell’approc-
cio type-theoretic sono essenzialmente due: la nozione di tipo induttivo
e la cosiddetta analogia di Curry-Howard.

3.4.1. Tipi induttivi. Col termine tipi induttivi si intende un meccani-
smo uniforme ed estremamente potente che permette di definire tipi di
dato ricorsivi unitamente ai rispettivi principi di eliminazione, ovvero,
in termini di programmazione, unitamente ai meccanismi di ricorsio-
ne che permettono la visita e la elaborazione strutturata dei dati in
oggetto.
   Questo è un punto filosofico caratterizzante della teoria dei tipi co-
struttiva. Il tipo non è semplicemente una collezione di oggetti con una
certa etichetta, ma è definito dai suoi costruttori, dai suoi eliminatori
(distruttori) e dalle regole di interazione tra costruttori e distruttori
(regole di riduzione). Quindi un tipo non è una collezione di oggetti
statici, ma definisce anche la dinamica dei propri elementi, fornendo
una procedura di normalizzazione degli stessi. Non si ha dunque solo
una logica per ragionare sui dati, ma anche un calcolo per esprimere
computazioni su di essi.

3.4.2. Analogia di Curry-Howard. L’analogia di Curry-Howard [46] è
una corrispondenza formale tra logica e programmazione che mette in
relazione le formule logiche e le relative dimostrazioni da un lato, con i
tipi e i programmi dall’altro. La relazione è in stretta relazione con la
intrepretazione operazionale di Brouwer-Heyting-Kolmogorov, per cui
una dimostrazione di A1 . . . An → B è un procedimento costruttivo
di sintesi di una prova di B a partire dalle prove di A1 , . . . , An . Con
isomorfismo di Curry-Howard si intende una versione formale di que-
sta corrispondenza tra vari sistemi di logica intuizionista e opportune
versioni del lambda calcolo tipato ([15, 13, 70]). In accordo a questa
analogia, verificare che una dimostrazione è corretta equivale a verifi-
care che un programma è ben tipato (il cosiddetto type-checking), che
è la principale operazione di analisi statica dei programmi svolta dai
compilatori. Al tempo stesso, l’analogia permette di avere notazioni e
strutture dati uniformi per prove e programmi, semplificando sensibil-
mente la struttura architetturale dei sistemi di prova. La corrispon-
denza di Curry-Howard apre inoltre una prospettiva completamente
nuova sulla verifica dei programmi: invece di cercare di stabilire l’a-
deguatezza di un programma rispetto alla sua specifica, si può cercare
  AUTOMATIC VERIFICATION AND INTERACTIVE THEOREM PROVING 17

           Tabella 1. Corrispondenza di Curry-Howard

              Matematica                Programmazione
              teorema                   tipo
              prova                     programma
              verifica di correttezza   type checking
              eliminazione dei tagli    computazione


semplicemente di dimostrare la coerenza logica della specifica. Se la
dimostrazione è costruttiva, è possibile estrarre in modo automatico il
contenuto algoritmico della dimostrazione, ottenendo un programma
che è garantito essere corretto per costruzione. Questo procedimen-
to, noto come estrazione di programmi, è stato sfruttato per la prima
volta nel sistema Nuprl [25], ed è in seguito stato implementato in
molti altri sistemi [66, 58]. L’analogia di Curry-Howard e la tecnica
di estrazione possono essere anche estesi, entro certi limiti, ai sistemi
logici classici [65, 12].

3.5. Altri dimostratori interattivi. Esistono svariati altri impor-
tanti dimostratori interattivi che non rientrano nelle due grandi fami-
glie precedenti. Questi si differenziano per i meccanismi logici legger-
mente diversi che sono supportati, il linguaggio di programmazione in
cui sono scritti, e le finalità per cui sono stati progettati. Tra questi
ricordiamo in particolare PVS [64], Twelf [69] e il recente sistema De-
dukti [9] basato sul lambda-pi-calcolo modulo di Dowek [27, 29]. Altri
sistemi hanno avuto una notevole importanza storica, ma al momento
non sono più supportati. Tra questi vogliamo ricordare i vari sistemi
del progetto Automath [63] di De Bruijn, e il proof assistant Lego di
Luo e Pollack [59].


                 4. Alcuni risultati importanti
   Concludiamo questo articolo con una rassegna di alcuni importanti
risultati che, per varie ragioni, hanno costituito delle importanti pie-
tre miliari per la verifica automatica, o per l’evoluzione del particolare
sistema di prova. I risultati menzionati sono spesso solamente i primi
di una lunga serie di ulteriori approfondimenti; lo stesso risultato è
stato frequentemente ridimostrato con altri strumenti, o con tecniche
18 AUTOMATIC VERIFICATION AND INTERACTIVE THEOREM PROVING

differenti. La lista è necessariamente incompleta: ci scusiamo in an-
ticipo con tutti gli autori i cui contributi, per ovvie ragioni di spazio,
non sono stati citati.
   Suddividiamo i risultati in tre grossi gruppi: fondamenti (sia di
matematica che di informatica), teoremi di matematica avanzata, e
applicazioni alla verifica di hardware e software.
        70                           80                         90                         00                          10                Hardware verification
                                                                                                                                         Miller−Rabin probabilistic primality test
                                                        HOL88              ProofPower              HOL4
                                          HOL                                                                                            Jordan Curve Theorem
                                                                HOL90             HOL light                                              CakeML (verified ML compiler)

                         Edinburgh                                                                                                      Kepler Conjecture (Flyspeck)
  LCF
             Stanford                 Cambridge                                                                                         Prime Number Theorem
                                                                                           Isar                                         OS Kernel
                                          Isabelle                                                                                      Goedel Incompleteness Theorem
                                                                                                                                        Green’s Theorem
                                                                                                                                        Borskuk’s Theorem
        Mizar                                                                                                                           Scott’s Domains
                                                                                                                                        Jordan Curve Theorem
                                                                                        Alfa                         Agda
Automath                                                                   Agda                                                         Homotopy Type Theory
                                                                                                           Cayenne
                                                                                                                                        Four Color Theorem
           Landau’s "Grundlagen"                  Coc                Cic                                                    SSreflect   Compcert (compiler verification)
                                          Coq                                                                                           Odd Order Theorem
                                                                                                                                        Coq in Coq

           System f normalization                    Lego                                         Matita                                CerCo (Certified Complexity)
                                                                                                                                        Universal Turing Machine


                                                            PVS                                                                          NASA specifications




                                          Tabella 2. Alcuni risultati notevoli


4.1. Fondamenti di Matematica e Informatica. Nel 1977, nella
sua tesi di dottorato [74] sotto la direzione di De Bruijn, van Benthem
Jutting presentò la completa formalizzazione e verifica automatica dei
Grundlagen der Matematik di Landau. Il risultato era notevole e passò
per parecchio tempo insuperato, anche perchè LCF stava cedendo il
passo alla seconda generazione di dimostratori interattivi: HOL, Isa-
belle e Coq. Nella seconda metà degli anni ottanta e negli anni no-
vanta, sul fronte della formalizzazione, gran parte dei sistemi sono
impegnati a sviluppare le librerie matematiche di base sulla falsariga
dei grundlagen, ma andando ben oltre di questi.
   Un risultato notevole dei primi anni novanta è la formalizzazione
in Lego da parte di Berardi della normalizzazione forte del sistema F
[16]. Il lavoro è importante sia perchè inaugura un filone fecondissimo
di studio formale della metateoria del lambda calcolo e dei meccanismi
di binding (notazione di De Bruijn diretta e inversa, tecniche nominali,
etc.), sia perchè rappresenta uno dei primi tentativi di dimostrare la
  AUTOMATIC VERIFICATION AND INTERACTIVE THEOREM PROVING 19

consistenza (di parte) del sistema logico dello strumento all’interno
del sistema stesso, ricerca recentemente culminata nel monumentale
lavoro di Barras [23] di verifica della consistenza di Coq all’interno di
Coq stesso (a meno di un livello di universi).
   Sempre sui fondamenti dell’informatica, un’altro lavoro notevole è
la formalizzazione della teoria dei domini di Scott fatta all’interno del
sistema Mizar da parte di Bancerek, Rudniki e altri [11].
   Per quanto riguarda la teoria della calcolabiltià, esiste una discreta
quantità di risultati sul lambda calcolo puro. L’esistenza di macchine
di Turing universali è stata certificata formalmente per la prima volta
nel sistema Matita nel 2015[4]. La teoria degli automi, cosi come
la teoria dei linguaggi formali è discretamente supportata in molti
sistemi.
   Sul fronte logico, il risultato più notevole è probabilmente la forma-
lizzazione da parte di Paulson in Isabelle dei teoremi di incompletezza
di Gödel [68].
   Un programma di ricerca particolarmente interessante è il complesso
lavoro di revisitazione fondazionale della matematica basato sulla in-
terpretazione omologica della teoria dei tipi (Univalent Foundations)
recentemente promosso da Voevodsky. In Homotopy Type Theory
(HoTT) [72], l’uguaglianza proposizionale è interpretata come omoto-
pia, e l’isomorfismo di tipi come equivalenza omologica. I teoremi e le
dimostrazioni in HoTT hanno in questo modo una diretta interpreta-
zione omologica. L’Homotopy Type Theory si è interamente svilup-
pata congiuntamente alla sua implementazione formale: i sistemi che
attualmente supportano HoTT sono Agda e Coq.


4.2. Matematica. I primi risultati matematici di una certa comples-
sità che sono stati completamente formalizzati e verificati automati-
camente risalgono ai primi anno del nuovo millennio. Quasi contem-
poraneamente vengono presentate due dimostrazioni alternative del
teorema della curva di Jordan (ogni curva chiusa del piano non in-
trecciata lo divide in due parti, una “interna” e l’altra “esterna”). La
prima dimostrazione è di Kornilowicz [51] in Mizar, la seconda di Ha-
les [42] in HOL-light. Hales è un noto matematico, famoso sia per la
sua dimostrazione della congettura di Keplero sul modo più compatto
per disporre delle sfere in uno spazio euclideo tridimensionale, sia per
gli eventi relativi alla pubblicazione di questo risultato. Il punto era
20 AUTOMATIC VERIFICATION AND INTERACTIVE THEOREM PROVING

che la sua dimostrazione comportava un largo uso di calcoli per risol-
vere dei sistemi di vincoli che venivano delegati al computer. Dopo
tre anni di lavoro i revisori degli Annals of Mathematics, a cui il lavo-
ro era stato sottoposto per pubblicazione, concludevano che, benchè
ritenessero valido il lavoro, non erano in grado di certificarne la cor-
rettezza dato il largo uso di “low-level components” su cui non erano
in grado di esprimere un giudizio. Alla fine gli Annals of Mathema-
tics pubblicarono una versione breve della prova [41], scorporando le
parti di codice. Una versione rivista e completa dell’articolo venne
in seguito pubblicata su Discrete and Computational Geometry. In
seguito a questa esperienza Hales iniziò a interessarsi ai dimostratori
automatici ([42] era un esercizio in questo senso), e avviò un grosso
progetto denominato Flyspeck (see [40]), per verificare in modo auto-
matico e formale la correttezza della sua dimostrazione. Il progetto si
è concluso con successo nel 2014 (il lavoro è in corso di pubblicazione).
    Altri due risultati importanti vengono raggiunti in quegli anni. Nel
2007 [10], Avigad e altri dimostrano il teorema sulla distribuzione asin-
titoca dei numeri primi. Quasi contemporaneamente, Gonthier presen-
ta la sua dimostrazione del teorema dei quattro colori [31]. Per que-
st’ultimo teorema Gonthier sviluppa una interessante estensione del
linguaggio Coq (SSreflect [34]) particolarmente orientata alla manipo-
lazione di strutture finite. Al fine di mostrare le potenzialità di questo
linguaggio Gonthier decide di affrontare il teorema di Feit-Thomson
(ogni gruppo finito di ordine dispari è risolubile), noto semplicemente
come odd-order theorem. La dimostrazione matematica “cartacea” è
mostruosa: occupa da sola un intero libro di 255 pagine ed è tutt’altro
che self contained. Anche in questo caso la formalizzazione è stata
conclusa con successo dopo tre anni di lavoro [33]. È utile osserva-
re che la dimostrazione formale ha una dimensione comparabile con
quella cartacea.

4.3. Verifica di hardware e software. Le prime applicazioni ri-
levanti della verifica automatica all’informatica si hanno nel campo
dell’hardware. I sistemi della classe HOL nascono in effetti dall’os-
servazione di Gordon e altri riguardo alla naturalezza di impiegare
meccanismi di ordine superiore nella specifica di proprietà di circuiti
logici [19]. Per lungo tempo la verifica si incentra per lo più sulla
correttezza di particolari algoritmi, e la verifica di proprietà di pro-
tocolli. Tra gli esempi più rilevanti, ricordiamo il lavoro di Hurd [47]
  AUTOMATIC VERIFICATION AND INTERACTIVE THEOREM PROVING 21

sul test di pimalità probabilistico di Miller-Rabin, che costituisce la
prima formalizzazione significativa nel campo della programmazione
probabilistica. In parallelo si affronta la semantica dei linguaggi di
programmazione, con importanti applicazioni alla sicurezza dei sistemi
informativi [55, 61].
   Nel 2006, suscita un immediato scalpore il lavoro di Leroy [56, 57]
in cui per la prima volta si affronta la correttezza di un programma
software ragionevolmente complesso: un compilatore ottimizzante per
un sottoinsieme quasi completo del linguaggio C, detto Cminor, verso
codice assembler per PowerPC. Il lavoro da luogo ad un grosso proget-
to di ricerca (Compcert) che approfondisce l’argomento lungo svariate
direzioni.
   La tematica viene inoltre ripresa ed estesa anche da altri gruppi
di ricerca: ricordiamo il progetto CerCo [1] dove si affrontano anche
problematiche di complessità computazionale del codice oggetto, o il
progetto CakeML [52] che fornisce per la prima volta un compilatore
certificato per il linguaggo SML.
   Avendo acquisito confidenza sulla possibilità pratica di certificare
in modo completo la correttezza del software, la ricerca si sta ora
allargando a problematiche via via più complesse, come ad esempio
la verifica di nuclei di sistemi operativi [50] e sistemi critici di varia
natura.


                      Riferimenti bibliografici
 [1] Roberto M. Amadio, Nicholas Ayache, François Bobot, Jaap Boender, Brian
     Campbell, Ilias Garnier, Antoine Madet, James McKinna, Dominic P. Mul-
     ligan, Mauro Piccolo, Randy Pollack, Yann Régis-Gianas, Claudio Sacerdo-
     ti Coen, Ian Stark, and Paolo Tranquilli. Certified complexity (cerco). In
     Foundational and Practical Aspects of Resource Analysis - Third Internatio-
     nal Workshop, FOPARA 2013, Bertinoro, Italy, August 29-31, 2013, Revised
     Selected Papers, pages 1–18, 2013.
 [2] Andrea Asperti. Proof, message and certificate. In Intelligent Computer Ma-
     thematics - CICM 2012, Bremen, Germany, July 8-13, 2012. Proceedings,
     volume 7362 of Lecture Notes in Computer Science, pages 17–31. Springer,
     2012.
 [3] Andrea Asperti, Herman Geuvers, and Raja Natarajan. Social processes, pro-
     gram verification and all that. Mathematical Structures in Computer Science,
     19(5):877–896, 2009.
 [4] Andrea Asperti and Wilmer Ricciotti. A formalization of multi-tape turing
     machines. Theor. Comput. Sci., 603:23–42, 2015.
22 AUTOMATIC VERIFICATION AND INTERACTIVE THEOREM PROVING

 [5] Andrea Asperti, Wilmer Ricciotti, Claudio Sacerdoti Coen, and Enrico Tassi.
     The Matita Interactive Theorem Prover. In Proceedings of the 23rd Interna-
     tional Conference on Automated Deduction (CADE-2011), Wroclaw, Poland,
     volume 6803 of LNCS, pages 64–69, 2011.
 [6] Andrea Asperti, Wilmer Ricciotti, and Claudio Sacerdoti Coen. Matita
     Tutorial. Journal of Formalized Reasoning, 7(2):91–199, 2014.
 [7] Andrea Asperti, Wilmer Ricciotti, Claudio Sacerdoti Coen, and Enrico Tas-
     si. A compact kernel for the Calculus of Inductive Constructions. Sadhana,
     34(1):71–144, 2009.
 [8] Andrea Asperti, Claudio Sacerdoti Coen, Enrico Tassi, and Stefano Zacchiroli.
     Crafting a proof assistant. In Proceedings of Types 2006: Conference of the
     Types Project. Nottingham, UK – April 18-21, volume 4502 of Lecture Notes
     in Computer Science, pages 18–32. Springer-Verlag, 2006.
 [9] Ali Assaf. A framework for defining computational higher-order logics. PhD
     thesis, McGill University, Canada, 2015.
[10] Jeremy Avigad, Kevin Donnelly, David Gray, and Paul Raff. A formally ve-
     rified proof of the prime number theorem. ACM Trans. Comput. Log., 9(1),
     2007.
[11] Grzegorz Bancerek and Piotr Rudnicki. A compendium of continuous lattices
     in mizar. Journal of Automated Reasoning, 29(3-4):189–224, 2002.
[12] Franco Barbanera and Stefano Berardi. A symmetric lambda calculus for
     classical program extraction. Information and Computation, 125(2):103–117,
     1996.
[13] Henk Barendregt. Lambda Calculi with Types. In Abramsky, Gabbay and
     Maibaum, editor, Handbook of Logic in Computer Science, volume 2. Oxford
     University Press, 1992.
[14] Henk Barendregt and Erik Barendsen. Autarkic computations in formal
     proofs. J. Autom. Reasoning, 28(3):321–336, 2002.
[15] Stefano Berardi. Towards a mathematical analysis of the coquand-huet cal-
     culus of constructions and the other systems in barendregt’s cube. Tech-
     nical report, Dept.of Computer Science, Carnegie Mellon Unviersity and
     Dipartimento di Matemtica, Università di Torino, 1988.
[16] Stefano Berardi. Girard normalization proof in lego. In Proceedings of the
     First Workshop on Logical Frameworks, pages 67–78, 1990.
[17] Yves Bertot and Pierre Castéran. Interactive Theorem Proving and Program
     Development. Texts in Theoretical Computer Science. Springer Verlag, 2004.
     ISBN-3-540-20854-2.
[18] Jasmin Christian Blanchette, Cezary Kaliszyk, Lawrence C. Paulson, and
     Josef Urban. Hammering towards QED. J. Formalized Reasoning, 9(1):101–
     148, 2016.
[19] Richard J. Boulton, Andrew D. Gordon, Michael J. C. Gordon, John Harri-
     son, John Herbert, and John Van Tassel. Experience with embedding hard-
     ware description languages in HOL. In Theorem Provers in Circuit Design,
     Proceedings of the IFIP TC10/WG 10.2 Inter. Conf. on Theorem Provers
   AUTOMATIC VERIFICATION AND INTERACTIVE THEOREM PROVING 23

     in Circuit Design: Theory, Practice and Experience, Nijmegen, The Nether-
     lands, 22-24 June 1992, volume A-10 of IFIP Transactions, pages 129–156.
     North-Holland, 1992.
[20] Nicolas Bourbaki. Theory of Sets. Elements of mathematics. Addison Wesley,
     1968.
[21] Samuel Boutin. Using reflection to build efficient and certified decision proce-
     dures. In Martin Abadi and Takahashi Ito editors, editors, Theoretical Aspect
     of Computer Software TACS’97, Lecture Notes in Computer Science, volume
     1281, pages 515–529. Springer-Verlag, 1997.
[22] Ana Bove, Peter Dybjer, and Ulf Norell. A brief overview of Agda - a functio-
     nal language with dependent types. In Theorem Proving in Higher Order Lo-
     gics, 22nd International Conference, TPHOLs 2009, Munich, Germany, Au-
     gust 17-20, 2009. Proceedings, volume 5674 of LNCS, pages 73–78. Springer,
     2009.
[23] Barras Bruno and Werner Benjamin. Coq in coq.
     http://www.lix.polytechnique.fr/~barras/publi/coqincoq.pdf, 2016.
[24] Claudio Sacerdoti Coen. Declarative representation of proof terms. J. Autom.
     Reasoning, 44(1-2):25–52, 2010.
[25] Robert L. Constable, Stuart F. Allen, H. M. Bromley, W. R. Cleaveland,
     J. F. Cremer, R. W. Harper, Douglas J. Howe, T. B. Knoblock, N. P. Mend-
     ler, P. Panangaden, James T. Sasaki, and Scott F. Smith. Implementing
     Mathematics with the Nuprl Development System. Prentice-Hall, NJ, 1986.
[26] Pierre Corbineau. A declarative proof language for the Coq proof assi-
     stant. http://foundations.cs.ru.nl/chitchat//slides/chat-corbineau.pdf. Pre-
     sented at the Connecting Humans and Type-checkers Workshop (CHAT)
     2006, Nijmegen.
[27] Denis Cousineau and Gilles Dowek. Embedding pure type systems in the
     lambda-pi-calculus modulo. In Typed Lambda Calculi and Applications, 8th
     International Conference, TLCA 2007, Paris, France, June 26-28, 2007, Pro-
     ceedings, volume 4583 of Lecture Notes in Computer Science, pages 102–117.
     Springer, 2007.
[28] Richard A. De Millo, Richard J. Lipton, and Alan J. Perlis. Social processes
     and proofs of theorems and programs. Commun. ACM, 22(5):271–280, 1979.
[29] Gilles Dowek, Thérèse Hardin, and Claude Kirchner. Theorem proving
     modulo. J. Autom. Reasoning, 31(1):33–72, 2003.
[30] Jean-Yves Girard, Yves Lafont, and Paul Taylor. Proofs and Types, volume 7
     of Cambridge Tracts in Theoretical Computer Science. Cambridge University
     Press, 1989.
[31] Georges Gonthier. The four colour theorem: Engineering of a formal proof.
     In Proc. of ASCM 2007, volume 5081 of LNCS, 2007.
[32] Georges Gonthier. Formal proof – the four color theorem. Notices of the
     American Mathematical Society, 55:1382–1394, 2008.
[33] Georges Gonthier, Andrea Asperti, Jeremy Avigad, Yves Bertot, Cyril Cohen,
     François Garillot, Stéphane Le Roux, Assia Mahboubi, Russell O’Connor,
     Sidi Ould Biha, Ioana Pasca, Laurence Rideau, Alexey Solovyev, Enrico Tassi,
24 AUTOMATIC VERIFICATION AND INTERACTIVE THEOREM PROVING

     and Laurent Théry. A Machine-Checked Proof of the Odd Order Theorem.
     In Interactive Theorem Proving - 4th International Conference, ITP 2013,
     Rennes, France, July 22-26, 2013. Proceedings, volume 7998 of Lecture Notes
     in Computer Science, pages 163–179. Springer, 2013.
[34] Georges Gonthier and Assia Mahboubi. An introduction to small scale
     reflection in coq. Journal of Formalized Reasoning, 3(2):95–152, 2010.
[35] Michael J. C. Gordon, Robin Milner, and Christopher P. Wadsworth. Edin-
     burgh LCF: a mechanised logic of computation. volume 78 of Lecture Notes
     in Computer Science. Springer-Verlag, 1979.
[36] Mike Gordon. From lcf to hol: a short history. In Proof, Language, and Inte-
     raction: Essays in Honour of Robin Milner, pages 169–186. The MIT Press,
     2000.
[37] Mike Gordon. Twenty years of theorem proving for hols past, present and futu-
     re. In Theorem Proving in Higher Order Logics (TPHOLs), 21st International
     Conference, pages 1–5, 2008.
[38] Adam Grabowski, Artur Kornilowicz, and Adam Naumowicz. Mizar in a
     nutshell. J. Formalized Reasoning, 3(2):153–245, 2010.
[39] Bruce Greer, John Harrison, Greg Henry, Wei Wayne Li, and Peter Tang.
     Scientific computing on the itanium® processor. Scientific Programming,
     10(4):329–337, 2002.
[40] Thomas Hales. Formal proof. Notices of the American Mathematical Society,
     55:1370–1381, 2008.
[41] Thomas C. Hales. A proof of the Kepler conjecture. Ann. Math., 162:1065–
     1185, 2005.
[42] Thomas C. Hales. The Jordan curve theorem, formally and informally. The
     American Mathematical Monthly, 114:882–894, 2007.
[43] John Harrison. A Mizar Mode for HOL. In J. von Wright, J. Grundy, and
     J. Harrison, editors, Theorem Proving in Higher Order Logics: 9th Inter-
     national Conference, TPHOLs’96, volume 1125 of LNCS, pages 203–220.
     Springer-Verlag, 1996.
[44] John Harrison. Proof style. In Eduardo Giménez and Christine Paulin-
     Mohring, editors, Selected Papers 4th Intl. Workshop on Types for Proofs
     and Programs, TYPES’96, Aussois, France, 15–19 Decemeber 1996, volume
     1512, pages 154–172, Berlin, 1996. Springer.
[45] John Harrison. Formal proof – theory and practice. Notices of the American
     Mathematical Society, 55:1395–1406, 2008.
[46] William A. Howard. The formulae-as-types notion of construction. In
     J.P.Seldin and J.R.Hindley, editors, To H.B. Curry: Essays on Combina-
     tory Logic, Lambda Calculus and Formalism, pages 479–490. Academic Press,
     Boston MA, 1980.
[47] Joe Hurd. Verification of the miller-rabin probabilistic primality test. J. Log.
     Algebr. Program., 56(1-2):3–21, 2003.
[48] Cezary Kaliszyk and Josef Urban. Learning-assisted theorem proving with
     millions of lemmas. J. Symb. Comput., 69:109–128, 2015.
[49] Cezary Kaliszyk and Freek Wiedijk. Merging procedural and declarative
   AUTOMATIC VERIFICATION AND INTERACTIVE THEOREM PROVING 25

     proof. In Types for Proofs and Programs, International Conference, TYPES
     2008, Torino, Italy, March 26-29, 2008, Revised Selected Papers, volume 5497
     of Lecture Notes in Computer Science, pages 203–219. Springer, 2008.
[50] Gerwin Klein, June Andronick, Kevin Elphinstone, Gernot Heiser, David
     Cock, Philip Derrin, Dhammika Elkaduwe, Kai Engelhardt, Rafal Kolanski,
     Michael Norrish, Thomas Sewell, Harvey Tuch, and Simon Winwood. sel4:
     formal verification of an operating-system kernel. Commun. ACM, 53(6):107–
     115, 2010.
[51] Artur Kornilowicz. Jordan curve theorem. Formalized mathematics,
     1(13):481–491, 2005.
[52] Ramana Kumar, Magnus O. Myreen, Michael Norrish, and Scott Owens. Ca-
     keml: a verified implementation of ML. In The 41st Annual ACM SIGPLAN-
     SIGACT Symposium on Principles of Programming Languages, POPL ’14,
     San Diego, CA, USA, January 20-21, 2014, pages 179–192, 2014.
[53] Joachim Lambek and Philip J Scott. Introduction to higher-order categorical
     logic, volume 7. Cambridge University Press, 1988.
[54] Joong Kwoen Lee. Philosophical perspectives on proof in mathematics
     education. Philosophy of Mathematics Education Journal, 16, 2002.
[55] Xavier Leroy. Bytecode verification on java smart cards. Softw., Pract. Exper.,
     32(4):319–340, 2002.
[56] Xavier Leroy. Formal certification of a compiler back-end or: programming
     a compiler with a proof assistant. In Proc. of the 33rd ACM SIGPLAN-
     SIGACT Symposium on Principles of Programming Languages, POPL 2006,
     Charleston, South Carolina, USA, pages 42–54, 2006.
[57] Xavier Leroy. Formal verification of a realistic compiler. Commun. ACM,
     52(7):107–115, 2009.
[58] Pierre Letouzey. A New Extraction for Coq. In Herman Geuvers and Freek
     Wiedijk, editors, Types for Proofs and Programs, Second International Work-
     shop, TYPES 2002, Berg en Dal, The Netherlands, April 24-28, 2002, volume
     2646 of Lecture Notes in Computer Science. Springer-Verlag, 2003.
[59] Zhaohui Luo and Robert Pollack. Lego proof development system: User’s
     manual.
[60] Dana MacKenzie. What in the name of Euclid is going on here? Science,
     207(5714):1402–1403, 2005.
[61] Claude Marché, Christine Paulin-Mohring, and Xavier Urbain. The kraka-
     toa tool for certificationof java/javacard programs annotated in jml. J. Log.
     Algebr. Program., 58(1-2):89–106, 2004.
[62] Per Martin-Löf. Intuitionistic type theory. Naples: Bibliopolis, 76, 1984.
[63] R.P. Nederpelt, J.H. Geuvers, and R.C. de Vrijer, editors. Selected Pa-
     pers on Automath, volume 133 of Studies in Logic and the Foundations of
     Mathematics. Elsevier Science, 1994. ISBN-0444898220.
[64] Sam Owre, John M. Rushby, and Natarajan Shankar. PVS: A prototype ve-
     rification system. In Automated Deduction - CADE-11, 11th International
26 AUTOMATIC VERIFICATION AND INTERACTIVE THEOREM PROVING

     Conference on Automated Deduction, Saratoga Springs, NY, USA, June 15-
     18, 1992, Proceedings, volume 607 of Lecture Notes in Computer Science,
     pages 748–752. Springer, 1992.
[65] Michel Parigot. Lambda-mu calculus: An algorithmic interpretation of clas-
     sical natural deduction. In Proc. of the Logic Programming and Automated
     Reasoning International Conference LPAR’92, volume 624 of LNCS, pages
     190–201. Springer, 1992.
[66] Christine Paulin-Mohring. Extracting Fω ’s programs from proofs in the Cal-
     culus of Constructions. In Sixteenth Annual ACM Symposium on Principles
     of Programming Languages, Austin, January 1989. ACM.
[67] Lawrence C. Paulson. The foundation of a generic theorem prover. J. Autom.
     Reasoning, 5(3):363–397, 1989.
[68] Lawrence C. Paulson. A mechanised proof of gödel’s incompleteness theorems
     using nominal isabelle. J. Autom. Reasoning, 55(1):1–37, 2015.
[69] Frank Pfenning and Carsten Schürmann. System description: Twelf - A meta-
     logical framework for deductive systems. In 16th International Conference on
     Automated Deduction, Trento, Italy, July 7-10, 1999, Proceedings, volume
     1632 of Lecture Notes in Computer Science, pages 202–206. Springer, 1999.
[70] Morten Heine Sorensen and Pawel Urzyczyn. Lectures on the Curry-Howard
     Isomorphism, volume 149. Elsevier, 2006.
[71] Andrzej Trybulec and Howard A. Blair. Computer Assisted Reasoning with
     MIZAR. In Proceedings of the 9th International Joint Conference on Artifi-
     cial Intelligence (IJCAI), Los Angeles, CA, pages 26–28. Morgan Kaufmann,
     1985.
[72] The Univalent Foundations Program. Homotopy Type Theory: Univa-
     lent Foundations of Mathematics. http://homotopytypetheory.org/book,
     Institute for Advanced Study, 2013.
[73] Josef Urban. Blistr: The blind strategymaker. In Global Conference on
     Artificial Intelligence, GCAI 2015, Tbilisi, Georgia, October 16-19, 2015,
     volume 36 of EPiC Series in Computing, pages 312–319. EasyChair, 2015.
[74] J. van Benthem Jutting. Checking Landau’s Grundlagen in the Automath sy-
     stem. Mathematical centre tracts n.83, Amsterdam: Mathematisch Centrum,
     1979.
[75] Markus Wenzel. Isar – a generic interpretative approach to readable formal
     proof documents. In Theorem Proving in Higher Order Logics, volume 1690
     of LNCS, pages 167–184. Springer, 1999.
[76] Markus Wenzel and Freek Wiedijk. A comparison of mizar and isar. J. Autom.
     Reasoning, 29(3-4):389–411, 2002.
[77] Freek Wiedijk. Mizar light for HOL light. In Theorem Proving in Higher Or-
     der Logics, 14th International Conference, TPHOLs 2001, Edinburgh, Sco-
     tland, UK, September 3-6, 2001, Proceedings, volume 2152 of Lecture Notes
     in Computer Science, pages 378–394. Springer, 2001.
[78] Freek Wiedijk. A synthesis of the procedural and declarative styles of
     interactive theorem proving. Logical Methods in Computer Science, 8(1), 2012.
