                                             A formal model of Algorand smart contracts

                                                    Massimo Bartoletti1 , Andrea Bracciali2, Cristian Lepore2 ,
                                                              Alceste Scalas3 , Roberto Zunino4
                                                          1
                                                            Università degli Studi di Cagliari, Cagliari, Italy
                                                                 2
                                                                    Stirling University, Stirling, UK
                                                        3
                                                          Technical University of Denmark, Lyngby, Denmark
                                                           4
                                                             Università degli Studi di Trento, Trento, Italy
arXiv:2009.12140v3 [cs.CR] 26 Jan 2021




                                               Abstract. We develop a formal model of Algorand stateless smart con-
                                               tracts (stateless ASC1). We exploit our model to prove fundamental
                                               properties of the Algorand blockchain, and to establish the security of
                                               some archetypal smart contracts. While doing this, we highlight various
                                               design patterns supported by Algorand. We perform experiments to vali-
                                               date the coherence of our formal model w.r.t. the actual implementation.


                                         1   Introduction
                                         Smart contracts are agreements between two or more parties that are auto-
                                         matically enforced without trusted intermediaries. Blockchain technologies rein-
                                         vented the idea of smart contracts, providing trustless environments where they
                                         are incarnated as computer programs. However, writing secure smart contracts
                                         is difficult, as witnessed by the multitude of attacks on smart contracts platforms
                                         (notably, Ethereum) — and since smart contracts control assets, their bugs may
                                         directly lead to financial losses.
                                             Algorand [22] is a late-generation blockchain that features a set of interesting
                                         features, including high-scalability and a no-forking consensus protocol based
                                         on Proof-of-Stake [9]. Its smart contract layer (ASC1) aims to mitigate smart
                                         contract risks, and adopts a non-Turing-complete programming model, natively
                                         supporting atomic sets of transactions and user-defined assets. These features
                                         make it an intriguing smart contract platform to study.
                                             The official specification and documentation of ASC1 consists of English
                                         prose and a set of templates to assist programmers in designing their contracts
                                         [1,5]. This conforms to standard industry practices, but there are two drawbacks:
                                          1. Algorand lacks a mathematical model of contracts and transactions suitable
                                             for formal reasoning on their behaviour, and for the verification of their
                                             properties. Such a model is needed to develop techniques and tools to ensure
                                             that contracts are correct and secure;
                                          2. furthermore, even preliminary informal reasoning on non-trivial smart con-
                                             tracts can be challenging, as it may require, in some corner cases, to resort
                                             to experiments, or direct inspection of the platform source code.
                                         Given these drawbacks, we aim at developing a formal model that:
2         Bartoletti et al.

o1. is high-level enough to simplify the design of Algorand smart contracts and
    enable formal reasoning about their security properties;
o2. expresses Algorand contracts in a simple declarative language, similar to
    PyTeal (the official Python binding for Algorand smart contracts) [7];
o3. provides a basis for the automatic verification of Algorand smart contracts.

Contributions. This paper presents:

    – a formal model of stateless ASC1 providing a solid theoretical foundation
      to Algorand smart contracts (§2). Such a model formalises both Algorand
      accounts and transactions (§2.1 – §2.4, §2.6), and smart contracts (§2.5);
    – a validation of our model through experiments [6] on the Algorand platform;
    – the formalisation and proof of some fundamental properties of the Algorand
      state machine: no double spending, determinism, value preservation (§2.7);
    – an analysis of Algorand contract design patterns (§3.2), based on several
      non-trivial contracts (covering both standard use cases, and novel ones).
      Quite surprisingly, we show that stateless contracts are expressive enough to
      encode arbitrary finite state machines;
    – the proof of relevant security properties of smart contracts in our model;
    – a prototype tool that compiles smart contracts (written in our formal declar-
      ative language) into executable TEAL code (§4).

    Our formal model is faithful to the actual ASC1 implementation; by ob-
jectives o1–o3, it strives at being high-level and simple to understand, while
covering the most commonly used primitives and mechanisms of Algorand, and
supporting the specification and verification of non-trivial smart contracts (§3.2,
§4). To achieve these objectives, we introduce minor high-level abstractions over
low-level details: e.g., since TEAL code has the purpose of accepting or rejecting
transactions, we model it using expressions that evaluate to true or false (simi-
larly to PyTEAL); we also formalise different transaction types by focusing on
their function, rather than their implementation. Our objectives imply that we
do not aim at covering all the possible TEAL contracts with bytecode-level ac-
curacy, and our Algorand model is not designed as a full low-level formalisation
of the behavior of the Algorand blockchain. We discuss the differences between
our model and the actual Algorand platform in §5.


2      The Algorand state machine

We present our formal model of the Algorand blockchain, including its smart
contracts (stateless ASC1), incrementally. We first define the basic transactions
that generate and transfer assets (§2.1–§2.3), and then add atomic groups of
transactions (§2.4), smart contracts (§2.5), and authorizations (§2.6). We discuss
the main differences between our model and Algorand in §5.
                                        A formal model of Algorand smart contracts               3

 a, b, . . .              Users (key pairs)   Tlv ⊆ T             Transactions in last ∆max rounds
 x, y, . . . ∈ X          Addresses           fasst ∈ A → X       Asset manager
 τ , τ ′, . . . ∈ A       Assets              flx ∈ (X × N) ⇀ N   Lease map
 v, w, . . . ∈ 0..264 − 1 Values              ffrz ∈ X ⇀ 2A       Freeze map
 σ, σ ′ ∈ A ⇀ N           Balances            Γ, Γ ′ , . . .      Blockchain states
 x[σ]                     Accounts            |= σ                Valid balance
 t, t′ , . . . ∈ T        Transactions        flx , r |= t        Valid time constraint
 e, e ′ , . . .           Scripts             W |= T, i           Authorized transaction in group
 r, r ′ . . . ∈ N         Rounds              JeKW T ,i           Script evaluation

                                Table 1: Summary of notation.



2.1     Accounts and transactions

We use a, b, . . . to denote public/private key pairs (kap , kas ). Users interact with
Algorand through pseudonymous identities, obtained as a function of their public
keys. Hereafter, we freely use a to refer to the public or the private key of a, or to
the user associated with them, relying on the context to resolve the ambiguity.
The purpose of Algorand is to allow users to exchange assets τ , τ ′ , . . . Besides
the Algorand native cryptocurrency Algo, users can create custom assets.
   We adopt the following notational convention:

 – lowercase letters for single entities (e.g., a user a);
 – uppercase letters for sets of entities (e.g., a set of users A);
 – calligraphic uppercase letters for sequences of entities (e.g., list of users A).

Given a sequence L, we write |L| for its length, set (L) for the set of its elements,
and L.i for its ith element (i ∈ 1..|L|); ε denotes the empty sequence. We write:

 – {x 7→ v} for the function mapping x to v, and having domain equal to {x};
 – f {x 7→ v} for the function mapping x to v, and y to f (y) if y 6= x;
 – f {x 7→ ⊥} for the function undefined at x, and mapping y to f (y) if y 6= x.

Accounts. An account is a deposit of one or more crypto-assets. We model
accounts as terms x[σ], where x is an address uniquely identifying the account,
and σ is a balance, i.e., a finite map from assets to non-negative 64-bit integers.
In the concrete Algorand, an address is a 58-characters word; for mathematical
elegance, in our model we represent an address as either:

 – a single user a. Performing transactions on a[σ] requires a’s authorization;
 – a pair (A, n), where A is a sequence of users, and 1 ≤ n ≤ |A|, are multisig
   (multi-signature) addresses. Performing transactions on (A, n)[σ] requires
   that at least n users out of those in A grant their authorization;5
 – a script 6 e. Performing transactions on e[σ] requires e to evaluate to true.
5
    W.l.o.g., we consider a single-user address a equivalent to (A, n) with A = hai, n = 1.
6
    We formalize scripts (i.e., smart contracts) later on, in §2.5.
4       Bartoletti et al.

pay      snd, rcv, val, asst snd transfers val units of asst to rcv (possibly creating rcv)
close    snd, rcv, asst      snd gives asst to rcv and removes it (if Algo, closes snd)
gen      snd, rcv, val       snd mints val units of a new asset, managed by rcv
optin    snd, asst           snd opts in to receive units of asset asst
burn     asst                asst is removed from the creator (if sole owner)
rvk      snd, rcv, val, asst asst’s manager transfers val units of asst from snd to rcv
frz      snd, asst           asst’s manager freezes snd’s use of asset asst
unfrz    snd, asst           asst’s manager unfreezes snd’s use of asset asst
delegate snd, asst, rcv      asst’s manager delegates asst to new manager rcv
    Fig. 1: Transaction types. Fields type, fv, lv, lx are common to all types.


   Each balance is required to own Algos, have at least 100000 micro-Algos for
each owned asset, and cannot control more than 1000 assets. Formally, we say
that σ is a valid balance (in symbols, |= σ) when:7
      Algo ∈ dom (σ) ∧ σ(Algo) ≥ 100000 · | dom (σ)| ∧ | dom (σ)| ≤ 1001


Transactions. Accounts can append various kinds of transactions to the
blockchain, in order to, e.g., alter their balance or set their usage policies. We
model transactions as records with the structure in Fig. 1. Each transaction
has a type, which determines which of the other fields are relevant.8 The field
snd usually refers to the subject of the transaction (e.g., the sender in an assets
transfer), while rcv refers to the receiver in an assets transfer. The fields asst and
val refer, respectively, to the affected asset, and to its amount. The fields fv (“first
valid”), lv (“last valid”) and lx (“lease”) are used to impose time constraints.
    Algorand groups transactions into rounds r = 1, 2, . . . To establish when a
transaction t is valid, we must consider both the current round r, and a lease
map flx binding pairs (address, lease identifier) to rounds: this is used to enforce
mutual exclusion between two or more transactions (see e.g. the periodic payment
contract in §3). Formally, we define the temporal validity of a transaction
t by the predicate flx , r |= t, which holds whenever:
         t.fv ≤ r ≤ t.lv and t.lv − t.fv ≤ ∆max and                       
          t.lx = 0 or (t.snd, t.lx) 6∈ dom (flx ) or r > flx (t.snd, t.lx)
First, the current round must lie between t.fv and t.lv, whose distance cannot
exceed ∆max rounds9 . Second, t must have a null lease identifier, or the identifier
has not been seen before (i.e., flx (t.snd, t.lx) is undefined), or the lease has expired
(i.e., r > flx (t.snd, t.lx)). When performed, a transaction with non-null lease
identifier acquires the lease on (t.snd, t.lx), which is set to t.lv.

7
  Since the codomain of σ is N, the balance entry σ(Algo) represents micro-Algos.
8
  In Algorand, the actual behaviour of a transaction may depend on both its type and
  other conditions, e.g., which optional fields are set. For instance, pay transactions
  may also close accounts if the CloseRemainderTo field is set. For the sake of clarity,
  in our model we prefer to use a richer set of types; see §5 for other differences.
9
  ∆max is a global consensus parameter, set to 1000 at time of writing.
                                    A formal model of Algorand smart contracts          5

2.2      Blockchain states

We model the evolution of the Algorand blockchain as a labelled transition
system. A blockchain state Γ has the form:

                 x1 [σ 1 ] | · · · | xn [σ n ] | r | Tlv | fasst | flx | ffrz         (1)

where all addresses xi are distinct, | is commutative and associative, and:

 – r is the current round;
 – Tlv is the set of performed transactions whose “last valid” time lv has not
   expired. This set is used to avoid double spending (see Theorem 1);
 – fasst maps each asset to the addresses of its manager and creator ;
 – flx is the lease map (from pairs (address, integer) to integers), used to
   ensure mutual exclusion between transactions;
 – ffrz is a map from addresses to sets of assets, used to freeze assets.

We define the initial state Γ0 as a0 [{Algo 7→ v0 }] | 0 | ∅ | fasst | flx | ffrz , where
dom (fasst ) = dom (flx ) = dom (ffrz ) = ∅, a0 is the initial user address, and
v0 = 1016 (which is the total supply of 10 billions Algos).
    We now formalize the ASC1 state machine, by defining how it evolves by sin-
gle transactions (§2.3), and then including atomic groups of transactions (§2.4),
smart contracts (§2.5), and the authorization of transactions (§2.6).


2.3      Executing single transactions
                 t
We write Γ −   →1 Γ ′ to mean: if the transaction t is performed in blockchain
state Γ, then the blockchain evolves to state Γ ′ .10 We specify the transition
relation −→1 through a set of inference rules (see Fig. 5 in the Appendix for the
full definition): each rule describes the effect of a transaction t in the state Γ
of eq. (1). We now illustrate all cases, depending on the transaction type (t.type).
    When τ ∈ dom (σ), we use the shorthand σ + v:τ to update balance σ by
adding v units to token τ ; similarly, we write σ − v:τ to decrease τ by v units:
          σ + v:τ ≡ σ{τ 7→ σ(τ ) + v}               σ − v:τ ≡ σ{τ 7→ σ(τ ) − v}

Pay to a new account. Let t.snd = xi for some i ∈ 1..n, let t.rcv = y 6∈
{x1 , . . . , xn } (i.e., the sender account x is already in the state, while the receiver
y is not), and let t.val = v. The rule has the following preconditions:

c1. t does not cause double-spending (t 6∈ Tlv );
c2. the time interval of the transaction, and its lease, are respected (flx , r |= t);
c3. the updated balance of xi is valid (|= σi − v : Algo);
c4. the balance of the new account at address y is valid (|= {Algo 7→ v}).
                     t
10
                 →1 Γ ′ does not imply that transaction t can be performed in Γ: in fact,
     Note that Γ −
     t might require an authorization. We specify the required conditions in §2.6.
6        Bartoletti et al.

If these conditions are satisfied, the new state Γ ′ is the following:
     xi [σi − v:Algo] | y[{Algo 7→ v}] | · · · | r | Tlv ∪ {t} | fasst | upd(flx , t) | ffrz
   In the new state, the Algo balance of xi is decreased by v units, and a
new account at y is created, containing exactly the v units taken from xi . The
balances of the other accounts are unchanged. The updated lease mapping is:
                               (
                                 flx {(t.snd, t.lx) 7→ t.lv} if t.lx 6= 0
                upd(flx , t) =
                                 flx                         otherwise
   Note that all transaction types check conditions c1 and c2 above; further, all
transactions check that updated account balances are valid (as in c3 and c4).

Pay to an existing account. Let t.snd = xi , t.rcv = xj , t.val = v, and
t.asst = τ . Besides the common checks, performing t requires that xj has “opted
in” τ (formally, τ ∈ dom (σj )), and τ must not be frozen in accounts xi and xj
(formally, τ 6∈ ffrz (xi ) ∪ ffrz (xj )). If xi 6= xj , then in the new state the balance
of τ in xi is decreased by v units, and that of τ in xj is increased by v units:
       xi [σi − v:τ ] | xj [σj + v:τ ] | · · · | r | Tlv ∪ {t} | fasst | upd(flx , t) | ffrz
where all accounts but xi and xj are unchanged. Otherwise, if xi = xj , then the
balance of xi is unchanged, and the other parts of the state are as above.

Close. Let t.snd = xi , t.rcv = xj 6= xi , and t.asst = τ . Performing t has two
possible outcomes, depending on whether τ is Algo or a user-defined asset. If
τ = Algo, we must check that σi contains only Algos. If so, the new state is:
          xj [σj + σi (Algo):Algo] | · · · | r | Tlv ∪ {t} | fasst | upd(flx , t) | ffrz
where the new state no longer contains the account xi , and all the Algos in xi
are transferred to xj . Instead, if τ 6= Algo, performing t requires to check only
that xi actually contains τ , and that xj has “opted in” τ . Further, τ must not
be frozen for addresses xi and xj , i.e. τ 6∈ ffrz (xi ) ∪ ffrz (xj ). The new state is:
    xi [σi {τ 7→ ⊥}] | xj [σj + σi (τ ):τ ] | · · · | r | Tlv ∪ {t} | fasst | upd(flx , t) | ffrz
where τ is removed from xi , and all the units of τ in xi are transferred to xj .

Gen. Let t.snd = xi , t.rcv = xj , and t.val = v. Performing t requires that xi
has enough Algos to own another asset, i.e. |= σi {τ 7→ v}, where τ is the (fresh)
identifier of the new asset. In the new state, the balance of xi is extended with
{τ 7→ v}, and fasst is updated, making xj the manager of τ . The new state is:
      xi [σi {τ 7→ v}] | · · · | r | Tlv ∪ {t} | fasst {τ 7→ (xj , xi )} | upd(flx , t) | ffrz

Opt in. Let t.snd = xi and t.asst = τ . Performing t requires that τ already
occurs in Γ, and that xi has enough Algos to store it. If the balance σi does not
have an entry for τ , in the new state σi is extended with a new entry for τ :
               xi [σi {τ 7→ 0}] | · · · | r | Tlv ∪ {t} | fasst | upd(flx , t) | ffrz
Otherwise, if xi ’s balance has already an entry for τ , then σi is unchanged.
                                     A formal model of Algorand smart contracts                7

Burn. Let t.snd = xi and t.asst = τ . Performing t requires that xi is the
creator of τ , and that xi stores all the units of τ (i.e., there are no units of τ in
other accounts). In the resulting state, the token τ no longer exists:
         xi [σi {τ 7→ ⊥}] | · · · | r | Tlv ∪ {t} | fasst {τ 7→ ⊥} | upd(flx , t) | ffrz
Note that this transaction requires an authorization by the asset manager of τ ,
which is recorded in fasst . (We address this topic in §2.6.)

Revoke. Let t.snd = xi and t.rcv = xj . Performing t requires that both xi
and xj are already storing the asset τ , and that τ is not frozen for xi and xj .
In the new state, the balance of xi is decreased by v = t.val units of the asset
τ = t.asst, and the balance of xj is increased by the same amount:
       xi [σi − v:τ ] | xj [σj + v:τ ] | · · · | r | Tlv ∪ {t} | fasst | upd(flx , t) | ffrz
The effect of a rvk transaction is essentially the same as pay . The difference is
that rvk must be authorized by the manager of the asset τ , while pay must be
authorized by the sender xi (see §2.6).

Freeze and unfreeze. A frz transaction t with t.snd = xi and t.asst = τ
                                    ′               ′
updates the mapping ffrz into ffrz     , such that ffrz (xi ) = ffrz (xi ) ∪ {τ }, whenever
the asset τ is owned by xi . This effectively prevents any transfers of the asset
τ to/from the account xi . The dual transaction unfrz updates the mapping ffrz
      ′              ′
into ffrz such that ffrz (xi ) = ffrz (xi ) \ {τ }.

Delegate. A delegate transaction t with t.snd = xi , t.rcv = xj and t.asst = τ
updates the manager of τ , provided that fasst (τ ) = (xi , xi ), for some xk . In the
updated mapping fasst {τ 7→ (xj , xk )}, the manager of τ is xj .

Initiating a new round. We model the advancement to the next round of
                                        X
the blockchain as a state transition Γ −→1 Γ ′ . In the new state Γ ′ , the round
is increased, and the set Tlv is updated as Tlv′ = {t ∈ Tlv | t.lv > r}. The other
components of the state are unchanged.


2.4   Executing atomic groups of transactions

Atomic transfers allow state transitions to atomically perform sequences of
transactions. To atomically perform a sequence T = t1 · · · tn from a state Γ, we
must check that all the transactions ti can be performed in sequence, i.e. the
following precondition must hold (for some Γ1 , . . . , Γn ):
                               1t                           t
                            Γ −→ 1 Γ1        ···    Γn−1 −→
                                                          n
                                                            1 Γn

If so, the state Γ can take a single-step transition labelled T. Denoting the new
transition relation with −
                         →, we write the atomic execution of T in Γ as follows:
                                               T
                                          Γ −
                                            → Γn
8         Bartoletti et al.


      e ::= v                  constant
           |e◦e                arithmetic (◦ ∈ {+, −, <, ≤, =, ≥, >, ∗, /, %, and, or })
           | not e             negation
           | txlen             number of transactions in the atomic group
           | txpos             index of current transaction in the atomic group
           | txid(n)           identifier of n-th transaction in the atomic group
           | tx(n).f           value of field f of n-th transaction in the atomic group
           | arg(n)            n-th argument of the current transaction
           | H(e)              hash
           | versig(e, e, e)   signature verification
Syntactic sugar:       false ::= 1 = 0 true ::= 1 = 1 tx.f ::= tx(txpos).f txid ::= txid(txpos)
                       if e0 then e1 else e2 ::= (e0 and e1 ) or ((not e0 ) and e2 )

                Fig. 2: Smart contract scripts (inspired by PyTeal [7]).


2.5     Executing smart contracts
In Algorand, custom authorization policies can be defined with a smart contract
language called TEAL [8]. TEAL is a bytecode-based stack language, with an
official programming interface for Python (called PyTeal): in our formal model,
we take inspiration from the latter to abstract TEAL bytecode scripts as terms,
with the syntax in Fig. 2. Besides standard arithmetic-logical operators, TEAL
includes operators to count and index all transactions in the current atomic
group, and to access their id and fields. When firing transaction involving scripts,
users can specify a sequence of arguments; accordingly, the script language
includes operators to know the number of arguments, and access them. Further,
scripts include cryptographic operators to compute hashes and verify signatures.
    The script evaluation function JeKW            T ,i (Fig. 3) evaluates e using 3 pa-
rameters: a sequence of arguments W, a sequence of transactions T forming an
atomic group, and the index i < |T| of the transaction containing e. The script
tx(n).f evaluates to the field f of the nth transaction in group T. The size of T is
given by txlen, while txpos returns the index i of the transaction containing the
script being evaluated. The script arg(n) returns the nth argument in W. The
script H(e) applies a public hash function H to the evaluation of e. The script
versig(e1 , e2 , e3 ) verifies a signature e2 on the message obtained by concatenating
the enclosing script and e1 , using public key e3 . All operators in Fig. 3 are strict :
they fail if the evaluation of any operand fails.


2.6     Authorizing transactions, and user-blockchain interaction
                                                            t
As noted before, the mere existence of a step Γ −   →1 Γ ′ does not imply that t
can actually be issued. For this to be possible, users must provide a sequence W
of witnesses, satisfying the authorization predicate associated with t; such
                                              A formal model of Algorand smart contracts                      9

             JvKTW,i = v         Je ◦ e ′ KTW,i = JeKTW,i ◦⊥ Je ′ KTW,i        Jnot eKTW,i = ¬⊥ JeKW
                                                                                                   T ,i

         Jtx(n).fKTW,i = (T.n).f (0 ≤ n < |T|)                  Jtxid(n)KTW,i = T.n (0 ≤ n < |T|)
            JtxlenKW
                   T ,i = |T |        JtxposKW
                                             T ,i = i         Jarg(n)KTW,i = W.n (0 ≤ n < |W|)
                                                                                m = T.i.snd, Je1 KW
                                                                                                         
  JH(e)KW           W
        T ,i = H(JeKT ,i )        Jversig(e1 , e2 , e3 )KW
                                                         T ,i =  ver k (m, s)                       T ,i
                                                                                s = Je2 KW              W
                                                                                         T ,i k = Je3 KT ,i

                             Fig. 3: Evaluation of scripts in Fig. 2.


 a predicate is uniquely determined by the authorizer address of t, written
 auth(t, fasst ). For transaction types close, pay, gen, optin the authorizer address
 is t.snd; for burn, rvk , frz and unfrz on an asset τ it is the asset manager fasst (τ ).
 Intuitively, if auth(t, fasst ) = x, then W authorizes t iff:

  1. if x is a multisig address (A, n), then W contains at least n signatures of t,
     made by users in A; (if x is a single-user address a: see footnote 5)
  2. if x is a script e, then e evaluates to true under the arguments W.

     We now formalize the intuition above. Since the evaluation of scripts depends
 on a whole group of transactions T, and on the index i of the current transac-
 tion within T, we define the authorization predicate as W |= T, i (read: “W
 authorizes the ith transaction in T”). Let sig A (m) stand for the set of signatures
 containing sig a (m) for all a ∈ A; then, W |= T, i holds whenever:

  1. if auth(T.i, fasst ) = (A, n), then |set(W) ∩ sig set (A) (T, i)| ≥ n
  2. if auth(T.i, fasst ) = e, then JeKW
                                       T ,i = true

    Note that, in general, the sequence of witnesses W is not unique, i.e., it may
 happen that W |= T, i and W′ |= T, i for W 6= W′ . For instance, the Oracle
 contract in §3 accepts transactions with witnesses of the form 0 s or 1 s′ , where
 the first element of the sequence represents the oracle’s choice, and the second
 element is the oracle’s signature.
 Given a sequence of sequences of witnesses W = W0 · · · Wn−1 with n = |T|, the
 group authorization predicate W |= T holds iff Wi |= T, i for all i ∈ 0..n−1.

 User-blockchain interaction. We model the interaction of users with the
 blockchain as a transition system. Its states are pairs (Γ, K), where Γ is a
 blockchain state, while K is the set of authorization bitstrings currently known
                                   ℓ
                                   ⇒ (with ℓ ∈ {w, X, W:T}) is given by the rules:
 by users. The transition relation =
                                                  X                        T
                                              Γ −→ Γ ′                     → Γ′
                                                                          Γ−           set(W) ⊆ K         W |= T
        w                                        X                                         W:T
(Γ, K) =⇒ (Γ, K ∪ {w})                (Γ, K) =⇒         (Γ ′ , K)                (Γ, K) ===⇒ (Γ ′ , K)
    With the first two rules, users can broadcast a witness w, or advance to the
 next round. The last rule gathers from K a sequence of witnesses W, and lets
 the blockchain perform an atomic group of transactions T if authorized by W.
10      Bartoletti et al.

2.7    Fundamental properties of ASC1

We now exploit our formal model to establish some fundamental properties of
ASC1. Theorem 1 states that the same transaction t cannot be issued more
                                                                            T
than once, i.e., there is no double-spending. In the statement, we use −→∗ −→−→∗
to denote an arbitrarily long series of steps including a group of transactions T.

                                                              T          T′
Theorem 1 (No double-spending). Let Γ0 −  →∗ −
                                             →−→∗ Γ −→ Γ ′ . Then, no
                                       ′
transaction occurs more than once in TT .

   Define the value of an asset τ in a state Γ = x1 [σ 1 ] | · · · | xn [σ n ] | r | · · · as
the sum of the balances of τ in all accounts in Γ:
                                                    (
                Pn                                    σ(τ ) if τ ∈ dom (σ)
     val τ (Γ) = i=1 val τ (σi )  where val τ (σ) =
                                                      0            otherwise
   Theorem 2 states that, once an asset is minted, its value remains constant,
until the asset is eventually burnt. In particular, since Algos cannot be burnt
(nor minted, unlike in Bitcoin and Ethereum), their amount remains constant.

Theorem 2 (Value preservation). Let Γ0 −         →∗ Γ − →∗ Γ ′ . Then:
                  (
                                                                        →∗ Γ ′
                    val τ (Γ) if τ occurs in Γ and it is not burnt in Γ −
   val τ (Γ ′ ) =
                    0         otherwise

   Theorem 3 establishes that the transition systems − → and =⇒ are deterministic:
crucially, this allows reconstructing the blockchain state from the transition log.
Notably, by item 3 of Theorem 3, witnesses only determine whether a state
transition happens or not, but they do not affect the new state. This is unlike
Ethereum, where arguments of function calls in transactions may affect the state.

Theorem 3 (Determinism). For all λ ∈ {X, T} and ℓ ∈ {X, w}:

          λ                 λ
         → Γ ′ and Γ −
 1. if Γ −           → Γ ′′ , then Γ ′ = Γ ′′ ;
                ℓ                            ℓ
              ⇒ (Γ ′ , K ′ ) and (Γ, K) =
 2. if (Γ, K) =                         ⇒ (Γ ′′ , K ′′ ), then (Γ ′ , K ′ ) = (Γ ′′ , K ′′ );
               W:T                           W′ :T
 3. if (Γ, K) ===⇒ (Γ ′ , K ′ ) and (Γ, K) ===⇒ (Γ ′′ , K ′′ ), then Γ ′ = Γ ′′ and K ′ = K ′′ = K.



3     Designing secure smart contracts in Algorand

We now exploit our formal model to design some archetypal smart contracts,
and establish their security (§3.2). First, we introduce an attacker model.
                                 A formal model of Algorand smart contracts            11

3.1   Attacker model

We assume that cryptographic primitives are secure, i.e., hashes are collision
resistant and signatures cannot be forged (except with negligible probability). A
                                                                                   ℓ1
run R is a (possibly infinite) sequence of labels ℓ1 ℓ2 · · · such that (Γ0 , K0 ) =⇒
          ℓ 2
(Γ1 , K1 ) =⇒ · · · , where Γ0 is the initial state, and K0 = ∅ is the initial (empty)
knowledge; hence, as illustrated in §2.6, each label ℓi in a run R can be either
w (broadcast of a witness bitstring w), W:T (atomic group of transactions T
authorized by W), or X (advance to next round). We consider a setting where:

 – each user a has a strategy Σ, i.e. a PPTIME algorithm to select which
   label to perform among those permitted by the ASC1 transition system. A
   strategy takes as input a finite run R (the past history) and outputs a single
   enabled label ℓ. Strategies are stateful : users can read and write a private
   unbounded tape to maintain their own state throughout the run. The initial
   state of a’s tape contains a’s private key, and the public keys of all users;11
 – an adversary Adv who controls the scheduling with her stateful adversar-
   ial strategy ΣAdv : a PPTIME algorithm taking as input the current run R
   and the labels output by the strategies of users (i.e., the steps that users are
   trying to make). The output of ΣAdv is a single label ℓ, that is appended to
   the current run. We assume the adversarial strategy ΣAdv can delay users’
   transactions by at most δAdv rounds, where δAdv is a given natural number.12

A set Σ of strategies of users and Adv induces a distribution of runs; we say that
run R is conformant to Σ if R is sampled from such a distribution. We assume
that infinite runs contain infinitely many X: this non-Zeno condition ensures
that neither users nor Adv can perform infinitely many transactions in a round.


3.2   Smart contracts

We now exploit our model to specify some archetypal ASC1 contracts, and reason
about their security. To simplify the presentation, we assume δAdv = 0, i.e., the
adversary Adv can start a new round (performing X) only if all users agree.13
The table below summarises our selection of smart contracts, highlighting the
design patterns they implement.

11
   Notice that new public/private key pairs can be generated during the run, and their
   public parts can be communicated as labels w.
12
   Without this assumption, Adv could arbitrarily disrupt deadlines: e.g., ΣAdv could
   make a always lose lottery games (like the ones below) by delaying a’s transactions.
13
   All results can be easily adjusted for δAdv > 0, but this would require more verbose
   statements to account for possible delays introduced by Adv.
12      Bartoletti et al.

                                 Signed           Commit/ State Atomic Time
      Use case / Pattern                 Timeouts
                                 witness           reveal machine transfer windows
               Oracle              X        X
               HTLC                         X        X
       Mutual HTLC (§B.1)                   X        X               X
      O(n2 )-collateral lottery             X        X               X
     0-collateral lottery (§B.2)            X        X      X        X
         Periodic payment                                                     X
           Escrow (§B.3)           X                        X
     Two-phase authorization                X               X                 X
        Limit order (§B.4)                  X                        X
            Split (§B.5)                    X                        X

Oracle. We start by designing a contract which allows either a or b to withdraw
all the Algos in the contract, depending on the outcome of a certain boolean
event. Let o be an oracle who certifies such an outcome, by signing the value 1
or 0. We model the contract as the following script:
Oracle , tx.type = close and tx.asst = Algo and (tx.fv > rmax and tx.rcv = a)
            or (arg(0) = 0 and versig(arg(0), arg(1), o) and tx.rcv = a) 
            or (arg(0) = 1 and versig(arg(0), arg(1), o) and tx.rcv = b)
    Once created, the contract accepts only close transactions, using two argu-
ments as witnesses. The argument arg(0) contains the outcome, while arg(1) is
o’s signature on (Oracle , arg(0)), i.e., the concatenation between the script and
the first argument. The user b can collect the funds in Oracle if o certifies the
outcome 1, while a can collect the funds if the outcome is 0, or after round rmax .
    Theorem 4 below proves that Oracle works as intended. To state it, we define
T p as the set of transactions allowing a user p to withdraw the contract funds:
       T p = {t | t.type = close, t.snd = Oracle , t.rcv = p, t.asst = Algo}
The theorem considers the following strategies for a, b, and o:
  – Σa : wait for s = sig o (Oracle , 0); if s arrives at round r ≤ rmax , then imme-
    diately send a transaction t ∈ T a with t.fv = r and witness 0 s; otherwise,
    at round rmax + 1, send a transaction t ∈ T a with t.fv = rmax + 1;
  – Σb : wait for s′ = sig o (Oracle , 1); if s′ arrives at round r, immediately send
    a transaction t ∈ T b with t.fv = r and witness 1 s′ ;
  – Σo : do one of the following: (a) send o’s signature on (Oracle , 0) at any time,
    or (b) send o’s signature on (Oracle , 1) at any time, or (c) do nothing.
Theorem 4. Let R be a run conforming to some set of strategies Σ, such that:
(i) Σo ∈ Σ; (ii) R reaches, at some round before rmax , a state Oracle [σ] | · · · ; (iii) R
reaches the round rmax + 2. Then, with overwhelming probability:
(1) if Σa ∈ Σ and o has not sent a signature on (Oracle , 1), then R contains a
    transaction in T a , transferring at least σ(Algo) to a;
(2) if Σb ∈ Σ and o has sent a signature on (Oracle , 1) at round r ≤ rmax , then
    R contains a transaction in T b , transferring at least σ(Algo) to b.
    Notice that in item (1) we are only assuming that a and o use the strate-
gies Σa and Σo , while b and Adv can use any strategy (and possibly collude).
Similarly, in item (2) we are only assuming b’s and o’s strategies.
                                    A formal model of Algorand smart contracts             13

 Hash Time Lock Contract (HTLC). A user a promises that she will either
 reveal a secret sa by round rmax , or pay a penalty to b. More sophisticated con-
 tracts, e.g. gambling games, use this mechanism to let players generate random
 numbers in a fair way. We define the HTLC as the following contract, parame-
 terised on the two users a, b and the hash ha = H(sa ) of the secret:
HTLC (a, b, ha ) , tx.type = close and tx.asst = Algo and                             
                    (tx.rcv = a and H(arg(0)) = ha ) or (tx.rcv = b and tx.fv ≥ rmax )
 The contract accepts only close transactions with receiver a or b. User a can
 collect the funds in the contract only by providing the secret sa in arg(0), effec-
 tively making sa public.14 Instead, if a does not reveal sa , then b can collect the
 funds after round rmax . We state the correctness of HTLC in Theorem 5; first,
 let T p be the set of transactions allowing user p to withdraw the contract funds:
          
   T p = t t.type = close, t.snd = HTLC (a, b, ha ), t.rcv = p, t.asst = Algo
 We consider the following strategies for a and b:

   – Σa : at a round r < rmax , send a t ∈ T a with t.fv = r and witness sa ;
   – Σb : at round rmax , check whether any transaction in T a occurs in R. If not,
     then immediately send a transaction t ∈ T b with t.fv = rmax .

 Theorem 5. Let R be a run conforming to some set of strategies Σ, such that:
 (i) R reaches, at some round before rmax , a state HTLC (a, b, ha )[σ] | · · · ; (ii)
 R reaches the round rmax + 1. Then, with overwhelming probability:

 (1) if Σa ∈ Σ, then R contains a transaction in T a , transferring at least σ(Algo)
     to a;
 (2) if Σb ∈ Σ and R does not contain the secret sa before round rmax + 1, then
     R contains a transaction in T b , transferring at least σ(Algo) to b.

 Lotteries. Consider a gambling game where n players bet 1Algo each, and the
 winner, chosen uniformly at random among them, can redeem n Algos. A simple
 implementation, inspired by [11–13] for Bitcoin, requires each player to deposit
 n(n − 1) Algos as collateral in an HTLC contract.15 For n = 2 players a and b,
 such deposits are transferred by the following transactions:
    tHa = {type : pay , snd : a, rcv : HTLC (a, b, ha ), val : 2, asst : Algo, . . .}
    tHb = {type : pay , snd : b, rcv : HTLC (b, a, hb ), val : 2, asst : Algo, . . .}
 The bets are stored in the following contract, which determines the winner as a
 function of the secrets, and allows her to withdraw the whole pot:
Lottery , tx.type = close and tx.asst = Algo and H(arg(0)) = ha and H(arg(1)) = hb
          and if (arg(0) + arg(1))%2 = 0 then tx.rcv = a else tx.rcv = b
 with ha 6= hb .16 Players a and b start the game with the atomic transactions:
 14
    If sa is a sufficiently long bitstring generated uniformly at random, collision resistance
    of the hash function ensures that only a (who knows sa ) can provide such an arg(0).
 15
    A zero-collateral lottery is presented in (§B.2).
 16
    This check prevents a replay attack: if a chooses ha = hb , then b cannot win.
14       Bartoletti et al.

                         T a,b = tHa tHb tLa tLb where:
         tLa = {type : pay, snd : a, rcv : Lottery , val : 1, asst : Algo, . . .}
         tLb = {type : pay, snd : a, rcv : Lottery , val : 1, asst : Algo, . . .}
The transaction tLa creates the contract with a’s bet, and tLb completes it with
b’s bet. At this point, there are two possible outcomes:
(a) both players reveal their secret. Then, the winner can withdraw the pot, by
    performing a close action on the Lottery contract, providing as arguments
    the two secrets, and setting her identity in the rcv field;
(b) one of the players does not reveal the secret. Then, the other player can
    withdraw the collateral in the other player’s HTLC (and redeem her own).
   To formalise the correctness of the lottery, consider the sets of transactions:
T secr
         
  p,q = t t.type = close, t.snd = HTLC (p, q, hp ), t.rcv = p, t.asst = Algo
T tout
         
  p,q = t t.type = close, t.snd = HTLC (p, q, hp ), t.rcv = q, t.asst = Algo
T lott
   p  = {t | t.type = close, t.snd = Lottery , t.rcv = p, t.asst = Algo}
and consider the following strategy Σa for a (the one for b is analogous):
                                                  secr
 1. at some r < rmax , send a transaction t ∈ T a,b    with t.fv = r and witness sa ;
                              secr
 2. if some transaction in T b,a occurs in R at round r′ < rmax , then extract its
    witness sb and compute the winner; if a is the winner, immediately send a
    transaction t ∈ T lott
                      a    with t.fv = r′ and witness sa sb ;
 3. if at round rmax no transaction in T b,a occurs in R, immediately send a
    transaction t ∈ T tout
                      b,a with t.fv = rmax .

    Theorem 6 below establishes that the lottery is fair, implying that the ex-
pected payoff of player a following strategy Σa is at least negligible; instead, if
a does not follow Σa (e.g., by not revealing her secret), the expected payoff may
be negative; analogous results hold for player b. This result can be generalised
for n > 2 players, with a collateral of n(n − 1) Algos. As in the HTLC, we assume
that sa and sb are sufficiently long bitstrings generated uniformly at random.
Theorem 6. Let R be a run conforming to a set of strategies Σ, such that:
(i) R contains, before rmax , the label T a,b ; (ii) R reaches round rmax + 1. For
p 6= q ∈ {a, b}, if Σp ∈ Σ, then: (1) R contains a transaction in T secr
                                                                    p,q , transferring
at least 2 Algo to p; (2) the probability that R contains T q,p or T lott
                                                                tout
                                                                            p , which
transfer at least 1 Algo to p, is ≥ 12 (up-to a negligible quantity).

Periodic payment. We want to ensure that a can withdraw a fixed amount
of v Algos at fixed time windows of p rounds. We can implement this behaviour
through the following contract, which can be refilled when needed:
PP (p, d, n) , tx.type = pay and tx.val = v and tx.asst = Algo and
                 tx.rcv = a and tx.fv % p = 0 and tx.lv = tx.fv + d and tx.lx = n
The contract accepts only pay transactions of v Algos to receiver a. The condi-
tions tx.fv % p = 0 and tx.lv = tx.fv + d ensure that the contract only accepts
transactions with validity interval [k p, k p+d], for k ∈ N. The condition tx.lx = n
ensures that at most one such transactions is accepted for each time window.
                                  A formal model of Algorand smart contracts          15

Finite-state machines. Consider a set of users A who want to stipulate a
contract whose behaviour is given by a finite-state machine with states q0 , . . . , qn .
We can implement such a contract by representing each state qi as a script ei ;
the current state/script holds the assets, and each state transition qi → qj is
a clause in ei which enables a close transaction to transfer the assets to ej .
This clause requires tx.rcv = ej — except in case of loops, which cannot be
encoded directly:17 in this case, we identify the next state as tx.rcv = arg(0),
also requiring all users in A to sign arg(0) to confirm its correctness. To ensure
that any user in A can trigger a state transition (by firing the corresponding
transaction), their signatures must be exchanged before the contract starts. We
show an instance of this pattern as the two-phase authorization contract below.
     An alternative technique is based on quines. As before, a state transition
qi → qj is rendered as a transaction which closes ei and transfers the balance to
ej . Here, all such scripts ek have the same code, except for a single state constant
k which occurs at a specific offset, and which represents the current state. To
verify that tx.rcv represents a legit next state, ei requires a witness w such that:
(i) tx.rcv is equal to the hash of w, and the state constant j within w is indeed a
next state for i; (ii) tx.snd is equal to the hash of w′ , where w′ is obtained from
w by replacing the state constant j with the current state i. Performing these
checks could be possible by using concatenation and substring operators.18

Two-phase authorization. We want a contract to allow user c to withdraw
some funds, but only if authorized by a and b. We want a to give her authoriza-
tion first; if b’s authorization is not given within p ≥ ∆max rounds, then anyone
can fire a transaction to reset the contract to its initial state. We model this con-
tract with two scripts: P1 represents the state where no authorization has been
given yet, while P2 represents the state where a’s authorization has been given.
Conceptually, the contract implements a finite-state machine, looping between
two states until the contract funds are withdrawn by c.
  P1 , tx.type = close and tx.asst = Algo and versig(txid, arg(0), a) and
         tx.rcv = P2 and tx.fv % (4 ∗ p) = 0 and tx.lv = tx.fv + ∆max
  P2 , tx.type = close and tx.asst = Algo and
          (versig(txid, arg(0), b) and tx.rcv = c) or
          (versig(arg(0), arg(1), a1 ) and versig(arg(0), arg(2), b1 ) and        
           tx.rcv = arg(0) and tx.fv % (4 ∗ p) = 2 ∗ p and tx.lv = tx.fv + ∆max )
The scripts P1 and P2 use a time window with 4 frames, each lasting p rounds.
Script P1 only accepts close transactions which transfer the balance to P2 ; the
time constraint ensures that such transactions are sent in the first time frame.
The script P2 accepts two kinds of transactions: (a) transfer the balance to c,
using an authorization by b; (b) transfer the balance to P1 , in the 4th time frame.
Note that in P2 we cannot use the (intuitively correct) condition tx.rcv = P1 , as
it would introduce a circularity. Instead, we apply the state machines technique
17
   This is because Algorand contracts cannot have circular references: contract accounts
   are referenced by script hashes, and no script can depend on its own hash.
18
   In Algorand, these operators are available only for LogicSigVersion ≥ 2.
16        Bartoletti et al.


                                                  {
             {                                        " type ": " axfer " ,
                  " type ": " pay " ,                 " snd ": x ,
                  " snd ": x ,                        " asnd ": x ,
                  " rcv ": 0 ,                        " arcv ": 0 ,
                  " close ": y ,                      " a c l o s e": y ,
                  " amt ": 0                          " xaid ": tau ,
             }                                        " aamt ": 0
                                                  }

     Fig. 4: Translation of a close transaction (left: τ = Algo, right: τ 6= Algo).


described above: we require tx.rcv = arg(0), with arg(0) signed by both a and
b,19 and assume that these signatures are exchanged before the contract starts.


4      From the formal model to concrete Algorand

We now discuss how to translate transactions and scripts in our model to concrete
Algorand. We first sketch how to compile our scripts into TEAL. The compilation
of most constructs is straightforward. For instance, a script e + e ′ is compiled
by using the opcode +, and similarly for the other arithmetic and comparison
operators, and for the cryptographic primitives. The logic operators and , or
are compiled via the opcode bnz, to obtain the short-circuit semantics. The
not operator is compiled via the opcode !. The operator txid(n) is compiled as
gtxn n TxID, txlen is compiled as global GroupSize, txpos is compiled as txn
GroupIndex, and arg(n) as arg n.
    Finally, compiling the script tx(n).f depends on the field f. If f is fv, lv,
or lx, then the compilation is gtxn n i, where i is, respectively, FirstValid,
LastValid, or Lease. For the other cases of f, the compilation of tx(n).f gen-
erates a TEAL script which computes f by decoding the concrete Algorand
transaction fields, and making them available in the scratch space. This decod-
ing is detailed in Table 2 in § C. From the same table we can also infer how
to translate transactions in the model to concrete Algorand transactions. For
instance, translating a transaction of the form:
                          {type : close, snd : x, rcv : y, asst : τ }
results in the concrete transaction in Fig. 4 (where we omit the irrelevant fields).
    Our modelling approach is supported by a prototype tool, called secteal
(secure TEAL), and accessible via a web interface at:
                            http://secteal.cs.stir.ac.uk/
The core of the tool is a compiler that translates smart contracts written as
expressions, based on the script language (§2.5), into executable TEAL bytecode.
In its current form, secteal supports experimentation with our model, and is
provided with a series of examples from §3.2. Users can also compile their own
secteal contracts, paving the way to a declarative approach to contract design
19
     We use other key pairs a1 and b1 to avoid confusion with the signatures on txid.
                                    A formal model of Algorand smart contracts         17

and development. secteal is a first building block toward a comprehensive IDE
for the design, verification, and deployment of contracts on Algorand.


5      Conclusions

This work is part of a wider research line on formal modelling of blockchain-
based contracts, ranging from Bitcoin [14, 30, 35] to Ethereum [20, 25–28, 33],
Cardano [21], Tezos [19], and Zilliqa [36]. These formal models are a necessary
prerequisite to rigorously reason on the security of smart contracts, and they are
the basis for automatic verification. Besides modelling the behaviour of trans-
actions, in §3.1 we have proposed a model of attackers: this enables us to prove
properties of smart contracts in the presence of adversaries, in the spirit of long-
standing research in the cryptography area [10, 11, 15, 18, 24, 31, 32].

Differences between our model and Algorand Besides not modelling the
consensus protocol, to keep the formalization simple, we chose to abstract from
some aspects of ASC1, which do not appear to be relevant to the development of
(the majority of) smart contracts. First, we are not modelling some transaction
fields: among them, we have omitted the fee field, used to specify an amount of
Algos to be paid to nodes, and the note field, used to embed arbitrary bitstrings
into transactions. We associate a single manager to assets, while Algorand uses
different managers for different operations (e.g., the freeze manager for frz /unfrz
and the clawback manager for rvk ). We use two different transactions types, pay
and close, to perform asset transfers and account closures: in Algorand, a single
pay transaction can perform both. Note that we can achieve the same effect
by performing the pay and close transactions within the same atomic group.
Although Algorand relies on 7 transaction types, the behaviour of some trans-
actions needs to be further qualified by the combination of other fields (e.g.,
freeze and unfreeze are obtained by transactions with the same type afrz, but
with a different value of the AssetFrozen field). While this is useful as an im-
plementation detail, our model simplifies reasoning about different behaviours
by explicitly exposing them in the transaction type. In the same spirit, while
Algorand uses different transaction types to represent actions with similar func-
tionality (e.g., transferring Algos and user-defined assets are rendered with dif-
ferent transaction types, pay and axfer), we use the same transaction type (e.g.,
pay) for such actions. Our model does not encompass some advanced features of
Algorand, e.g.: rekeying accounts, key registration transactions (keyreg), some
kinds of asset configuration transaction (e.g., decimals, default frozen, different
managers), and application call transactions.20 Our script language substantially
covers TEAL opcodes with LogicSigVersion=1, but for a few exceptions, e.g.
bitwise operations, different hash functions, jumps.
20
     Application call transactions are used to implement stateful contracts, and therefore
     are outside the scope of this paper.
18     Bartoletti et al.

Related work Besides featuring an original consensus protocol based on proof-
of-stake [22], Algorand has also introduced a novel paradigm of (stateless) smart
contracts, which differs from the paradigms of other mainstream blockchains. On
the one hand, Algorand follows the account-based model, similarly to Ethereum
(and differently from Bitcoin and Cardano, which follow the UTXO model).
On the other hand, Algorand’s paradigm of stateless contracts diverges from
Ethereum’s stateful contracts: rather, it resembles Bitcoin’s, where contracts are
based upon custom transaction redeem conditions. Besides these differences, Al-
gorand natively features user-defined assets, while other platforms render them
as smart contracts (e.g., by implementing ERC20 and ERC721 interfaces in
Ethereum). Overall, these differences demand for a formal model that is sub-
stantially different from the models devised for the other blockchain platforms.
    Our formalization of the Algorand’s script language is close, with respect to
the level of abstraction, to the model of Bitcoin script developed in [14]. Indeed,
both works formalise scripts in an expression language, abstracting from the
bytecode. A main difference between Algorand and Ethereum is that Ethereum
contracts are stateful: their state can be updated by specific bytecode instruc-
tions; instead, (stateless) TEAL scripts merely authorize transactions. Conse-
quently, a difference between our model and formal models of Ethereum contracts
is that the semantics of our scripts has no side effects. In this way, our work de-
parts from most literature on the formalization of Ethereum contracts, where
the target of the formalization is either the bytecode language EVM [26, 27, 33],
or the high-level language Solidity [16, 23, 29].

Future work Our formal model of Algorand smart contracts can be expanded
depending on the evolution of the Algorand framework. In mid August 2020, Al-
gorand has introduced stateful ASC1 contracts [4], enriching contract accounts
with a persistent key-value store, accessible and modifiable through a new kind
of transaction (which can use an extended set of TEAL opcodes). To accommo-
date stateful contracts in our model, we would need to embed the key-value store
in contract accounts, and extend the script language with key-value store up-
dates. The rest of our model (in particular, the semantics of transactions and the
attacker model) is mostly unaffected by this extension. Future work could also
investigate declarative languages for stateful Algorand smart contracts, and as-
sociated verification techniques. Another research direction is the mechanization
of our formal model, using a proof assistant: this would allow machine-checking
the proofs developed by pencil-and-paper in §D. Similar work has been done e.g.
for Bitcoin [35] and for Tezos [19].

Acknowledgements The authors thank the anonymous reviewers of Financial
Cryptography 2021 for their insightful comments on a preliminary version of this
paper. Massimo Bartoletti is partially supported by Convenzione tra Fondazione
di Sardegna e Atenei Sardi project F74I19000900007 ADAM. Cristian Lepore
is partially supported by The Data Lab, Innovation Center. Alceste Scalas is
partially supported by EU Horizon 2020 project 830929 CyberSec4Europe, and
Industriens Fonds Cyberprogram 2020-0489 Security-by-Design in Digital Den-
                                 A formal model of Algorand smart contracts          19

mark (Sb3D). Roberto Zunino is partially supported by MIUR PON Distributed
Ledgers for Secure Open Communities.


References
 1. Algorand developer docs (2020), https://developer.algorand.org/docs/
 2. Algorand developer docs: Limit order (contract owner has Algos) (2020), https://
    developer.algorand.org/docs/reference/teal/templates/limit_ordera/
 3. Algorand developer docs: Split (2020), https://developer.algorand.org/docs/
    reference/teal/templates/split/
 4. Algorand developer docs: stateful smart contracts (2020), https://developer.
    algorand.org/docs/features/asc1/stateful/
 5. Algorand developer docs: Transaction Execution Approval Language (TEAL)
    (2020), https://developer.algorand.org/docs/reference/teal
 6. ASC1 coherence-checking experiments (2020), https://github.com/blockchain-
    unica/asc1-experiments
 7. PyTeal: Algorand smart contracts in Python (2020), https://github.com/
    algorand/pyteal
 8. Transaction execution approval language (TEAL) specification (2020), https://
    developer.algorand.org/docs/reference/teal/specification/
 9. Alturki, M.A., Chen, J., Luchangco, V., Moore, B.M., Palmskog, K., Peña, L.,
    Rosu, G.: Towards a verified model of the Algorand consensus protocol in Coq. In:
    Formal Methods Workshops. Lecture Notes in Computer Science, vol. 12232, pp.
    362–367. Springer (2019). https://doi.org/10.1007/978-3-030-54994-7 27
10. Andrychowicz, M., Dziembowski, S., Malinowski, D., Mazurek, L.:
    Fair two-party computations via Bitcoin deposits. In: Financial Cryp-
    tography Workshops. LNCS, vol. 8438, pp. 105–121. Springer (2014).
    https://doi.org/10.1007/978-3-662-44774-1 8
11. Andrychowicz, M., Dziembowski, S., Malinowski, D., Mazurek, L.: Secure
    multiparty computations on Bitcoin. In: IEEE S & P. pp. 443–458 (2014).
    https://doi.org/10.1109/SP.2014.35, first appeared on Cryptology ePrint Archive,
    http://eprint.iacr.org/2013/784
12. Andrychowicz, M., Dziembowski, S., Malinowski, D., Mazurek, L.: Secure
    multiparty computations on Bitcoin. Commun. ACM 59(4), 76–84 (2016).
    https://doi.org/10.1145/2896386
13. Atzei, N., Bartoletti, M., Cimoli, T., Lande, S., Zunino, R.: SoK: unraveling Bit-
    coin smart contracts. In: POST. LNCS, vol. 10804, pp. 217–242. Springer (2018).
    https://doi.org/10.1007/978-3-319-89722-6
14. Atzei, N., Bartoletti, M., Lande, S., Zunino, R.: A formal model of Bitcoin transac-
    tions. In: Financial Cryptography and Data Security. LNCS, vol. 10957. Springer
    (2018). https://doi.org/10.1007/978-3-662-58387-6
15. Banasik, W., Dziembowski, S., Malinowski, D.: Efficient zero-knowledge contingent
    payments in cryptocurrencies without scripts. In: ESORICS. LNCS, vol. 9879, pp.
    261–280. Springer (2016). https://doi.org/10.1007/978-3-319-45741-3 14
16. Bartoletti, M., Galletta, L., Murgia, M.: A minimal core calculus for Solidity con-
    tracts. In: Cryptocurrencies and Blockchain Technology. LNCS, vol. 11737, pp.
    233–243. Springer (2019). https://doi.org/10.1007/978-3-030-31500-9 15
17. Bartoletti, M., Zunino, R.: Constant-deposit multiparty lotteries on Bitcoin.
    In: Financial Cryptography Workshops. LNCS, vol. 10323. Springer (2017).
    https://doi.org/10.1007/978-3-319-70278-0
20      Bartoletti et al.

18. Bentov, I., Kumaresan, R.: How to use Bitcoin to design fair pro-
    tocols. In: CRYPTO. LNCS, vol. 8617, pp. 421–439. Springer (2014).
    https://doi.org/10.1007/978-3-662-44381-1 24
19. Bernardo, B., Cauderlier, R., Hu, Z., Pesin, B., Tesson, J.: Mi-Cho-Coq, a
    framework for certifying Tezos smart contracts. In: Sekerinski, E., Moreira,
    N., Oliveira, J.N., Ratiu, D., Guidotti, R., Farrell, M., Luckcuck, M., Marm-
    soler, D., Campos, J., Astarte, T., Gonnord, L., Cerone, A., Couto, L., Don-
    gol, B., Kutrib, M., Monteiro, P., Delmas, D. (eds.) Workshop on Formal
    Methods for Blockchains. LNCS, vol. 12232, pp. 368–379. Springer (2019).
    https://doi.org/10.1007/978-3-030-54994-7 28
20. Bhargavan, K., Delignat-Lavaud, A., Fournet, C., Gollamudi, A., Gonthier,
    G., Kobeissi, N., Rastogi, A., Sibut-Pinote, T., Swamy, N., Zanella-
    Beguelin, S.: Formal verification of smart contracts. In: PLAS (2016).
    https://doi.org/10.1145/2993600.2993611
21. Chakravarty, M.M., Chapman, J., MacKenzie, K., Melkonian, O., Jones,
    M.P., Wadler, P.: The extended UTXO model. In: Financial Cryp-
    tography Workshops. LNCS, vol. 12063, pp. 525–539. Springer (2020).
    https://doi.org/10.1007/978-3-030-54455-3 37
22. Chen, J., Micali, S.: Algorand: A secure and efficient distributed ledger. Theoretical
    Computer Science 777, 155–183 (2019). https://doi.org/10.1016/j.tcs.2019.02.001
23. Crafa, S., Pirro, M.D., Zucca, E.: Is Solidity solid enough? In: Financial
    Cryptography Workshops. LNCS, vol. 11599, pp. 138–153. Springer (2019).
    https://doi.org/10.1007/978-3-030-43725-1 11
24. Delgado-Segura, S., Pérez-Solà, C., Navarro-Arribas, G., Herrera-Joancomartı́, J.:
    A fair protocol for data trading based on bitcoin transactions. Future Generation
    Computer Systems (2017). https://doi.org/10.1016/j.future.2017.08.021
25. Grishchenko, I., Maffei, M., Schneidewind, C.: Foundations and tools for the static
    analysis of Ethereum smart contracts. In: CAV. LNCS, vol. 10981, pp. 51–78.
    Springer (2018). https://doi.org/10.1007/978-3-319-96145-3 4
26. Grishchenko, I., Maffei, M., Schneidewind, C.: A semantic framework for
    the security analysis of Ethereum smart contracts. In: Principles of Secu-
    rity and Trust (POST). LNCS, vol. 10804, pp. 243–269. Springer (2018).
    https://doi.org/10.1007/978-3-319-89722-6 10
27. Hildenbrandt, E., Saxena, M., Rodrigues, N., Zhu, X., Daian, P., Guth, D., Moore,
    B.M., Park, D., Zhang, Y., Stefanescu, A., Rosu, G.: KEVM: A complete for-
    mal semantics of the Ethereum Virtual Machine. In: IEEE Computer Security
    Foundations Symposium (CSF). pp. 204–217. IEEE Computer Society (2018).
    https://doi.org/10.1109/CSF.2018.00022
28. Hirai, Y.: Defining the Ethereum Virtual Machine for interactive theorem provers.
    In: Financial Cryptography Workshops. LNCS, vol. 10323, pp. 520–535. Springer
    (2017). https://doi.org/10.1007/978-3-319-70278-0 33
29. Jiao, J., Kan, S., Lin, S., Sanán, D., Liu, Y., Sun, J.: Semantic under-
    standing of smart contracts: Executable operational semantics of Solidity.
    In: IEEE Symposium on Security and Privacy. pp. 1695–1712. IEEE (2020).
    https://doi.org/10.1109/SP40000.2020.00066
30. Klomp, R., Bracciali, A.: On symbolic verification of Bitcoin’s script language.
    In: Workshop on Cryptocurrencies and Blockchain Technology (CBT). LNCS, vol.
    11025, pp. 38–56. Springer (2018). https://doi.org/10.1007/978-3-030-00305-0 3
31. Kumaresan, R., Bentov, I.: How to use Bitcoin to incentivize correct computations.
    In: ACM CCS. pp. 30–41 (2014). https://doi.org/10.1145/2660267.2660380
                                 A formal model of Algorand smart contracts        21

32. Kumaresan, R., Moran, T., Bentov, I.: How to use Bitcoin to
    play     decentralized   poker. In: ACM            CCS.     pp. 195–206    (2015).
    https://doi.org/10.1145/2810103.2813712
33. Luu, L., Chu, D.H., Olickel, H., Saxena, P., Hobor, A.: Mak-
    ing smart contracts smarter. In: ACM CCS. pp. 254–269 (2016).
    https://doi.org/10.1145/2976749.2978309
34. Miller, A., Bentov, I.: Zero-collateral lotteries in Bitcoin and Ethereum. In: Eu-
    roS&P Workshops. pp. 4–13 (2017). https://doi.org/10.1109/EuroSPW.2017.44
35. Rupić, K., Rozic, L., Derek, A.: Mechanized formal model of Bitcoin’s blockchain
    validation procedures. In: Workshop on Formal Methods for Blockchains
    (FMBC@CAV). OASIcs, vol. 84, pp. 7:1–7:14. Schloss Dagstuhl - Leibniz-Zentrum
    für Informatik (2020). https://doi.org/10.4230/OASIcs.FMBC.2020.7
36. Sergey, I., Nagaraj, V., Johannsen, J., Kumar, A., Trunov, A., Hao, K.C.G.: Safer
    smart contract programming with Scilla. Proc. ACM Program. Lang. 3(OOPSLA),
    185:1–185:30 (2019). https://doi.org/10.1145/3360611
22      Bartoletti et al.

A     The stateless ASC1 state machine
We assume the following sets:
 – K, the set of all users;
 – S, the set of all scripts;
 – X = (K∗ × N) ∪ S, the set of all addresses;
 – A, the set of all assets;
 – T, the set of all transactions;
 – U64 = v ∈ Z 0 ≤ v < 264 , the set of unsigned 64-bit integers.
We define the partial operator ◦ on accounts as follows:
        σ ◦ v : τ = σ{τ 7→ σ(τ ) ◦ v}          if τ ∈ dom (σ) and ◦ ∈ {+, −}
Note that the use of the ◦ operator in an instance of the rules in Fig. 5 on
a reachable state x[σ] | · · · never leads to overflows or underflows, since these
rules correctly keep track of the number of assets. In particular, overflow never
happens since the number of each asset is bounded (1016 for Algo, and the value
val in gen transactions for the other assets).
    We define a partial function auth(t, fasst ) which gives the manager of a trans-
action t:
                   (
                     t.snd                if t.type ∈ {close, pay , gen, optin}
 auth(t, fasst ) =
                     fst (fasst (t.asst)) if t.type ∈ {rvk , frz , unfrz , burn, delegate}

Let ν0 , ν1 ∈ U64 ∪ {⊥}. We define:
             
             
             
              ν0 ◦ ν1      if ◦ ∈ {+, −, ∗} and ν0 , ν1 , ν0 ◦ ν1 ∈ U64
               ⌊ν   /ν   ⌋  if ◦ = / and ν0 ∈ U64 and ν1 ∈ U64 \ {0}
             
             
             
                 0    1
             
             ν0 mod ν1 if ◦ = % and ν0 ∈ U64 and ν1 ∈ U64 \ {0}
             
             
             
             
             1             if ◦ ∈ {<, ≤, =, ≥, >} and ν0 , ν1 ∈ U64 and ν0 ◦ ν1
             
             
             
             
             0             if ◦ ∈ {<, ≤, =, ≥, >} and ν0 , ν1 ∈ U64 and ¬(ν0 ◦ ν1 )
ν0 ◦ ⊥ ν1 ≡
             
             
              0            if ◦ = and and ν0 = 0
               ν1           if ◦ = and and ν0 ∈ U64 \ {0}
             
             
             
             
             
             1             if ◦ = or and ν0 ∈ U64 \ {0}
             
             
             
             
              ν1           if ◦ = or and ν0 = 0
             
             
             
             
             ⊥             otherwise
                                    
                                    1 if ν0 = 0
                                    
                           ¬⊥ ν0 = 0 if ν0 ∈ U64 \ {0}
                                    
                                      ⊥ otherwise
                                    

A blockchain state Γ is a term with the following syntax:
            Γ ::= x[σ] | r | Tlv | fasst | flx | ffrz | Γ | Γ ′
and subject to the following conditions:
                                   A formal model of Algorand smart contracts             23

 – all the terms except x[σ] occur exactly once in a configuration;
 – r ∈ N is the current round ;
 – Tlv ⊆ T is the set of performed transactions whose “last valid” time lv has
   not expired;
 – fasst ∈ A → X × X is the asset map;
 – flx ∈ X × N → N is the lease map;
 – ffrz ∈ X → 2A is the freeze map;
 – if x[σ] and y[σ ′ ] occur in a configuration, then x 6= y.
 – configurations form a commutative monoid with respect to the composition
   operator | (with identity 0).
   We define in Fig. 5 a labelled transition relation −
                                                      → between blockchain states,
where labels are the following:
 – T performs a sequence of transactions;
 – X advances one round.


B     Additional smart contracts
B.1    Mutual HTLC
The mutual HTLC [11] is a variant of HTLC presented in §3.2: two users a, b
choose their own secrets, pay a deposit, and the contract ensures that either
(a) both users reveal their secret and get their deposits back, or (b) whoever
does not reveal the secret loses the deposit (in favour of the other user).
      Assuming that ha and hb are, respectively, the hashes of the secrets sa and
sb , we can implement the mutual HTLC by creating two HTLC contracts within
an atomic group of transactions:
        {snd : a, rcv : HTLC (a, b, ha ), . . .} {snd : b, rcv : HTLC (b, a, hb ), . . .}
      The mutual HTLC contract guarantees that once a has stipulated it, then
she will either learn b’s secret, or receive the compensation. Instead, if we create
two instances of HTLC in a non-atomic way, this property is not guaranteed,
since b could refuse to stipulate its part of the contract.
      Theorem 7 states the correctness of the mutual HTLC. For p, q ∈ {a, b}, let:
             
  T p,q = t t.type = close, t.snd = HTLC (p, q, hp ), t.rcv = p, t.asst = Algo
 T ′ p, q = t t.type = close, t.snd = HTLC (p, q, hp ), t.rcv = q, t.asst = Algo
and consider the following strategy for distinct users p 6= q ∈ {a, b}:
 – Σp : at a round r < rmax , send a transaction t ∈ T p,q with t.fv = r and
   witness sp . Then, at round rmax check whether any transaction in T q,p occurs
   in R: if not, immediately send a transaction t ∈ T ′ q,p with t.fv = rmax .
Theorem 7. Let R be a run conforming to some set of strategies Σ, such that:
(i) R reaches, before rmax , a state HTLC (a, b, ha )[σ] | HTLC (b, a, hb )[σ ′ ] | · · · ; (ii) R
reaches rmax + 1. Let p 6= q ∈ {a, b}. If Σp ∈ Σ, then with overwhelming proba-
bility: (1) R contains a transaction in T p,q ; (2) if R does not contain the secret
sq before round rmax + 1, then R contains a transaction in T ′ q,p .
24      Bartoletti et al.

B.2   Zero-collateral lottery
We show a variant of the two-players lottery in §3.2 which requires no collateral,
similarly to [17,34]. The preconditions just require the 1Algo bets and the secrets,
while the contract is the following:
    ZDL , tx.type = close and tx.asst = Algo and
                   (tx.rcv = ZDL2 and H(arg(0))
                                                  = ha ) or
                  (tx.rcv = b and tx.fv ≥ r0 )
   ZDL2 , tx.type = close and tx.asst = Algo and H(arg(0)) = ha and
               (H(arg(1)) = hb and
                if (arg(0) + arg(1))%2 = 0 then  tx.rcv = a else tx.rcv = b) or
               (tx.rcv = a and tx.fv ≥ r0 + r1 )
    Here, b must reveal first. If b does not reveal his secret by the deadline r0 ,
then a can redeem the 2Algos stored in the contract. Otherwise, a in turn must
reveal by the deadline r0 +r1 , or let b redeem 2Algos. If both a and b reveal, then
the winner is determined as a function of their secrets. As before, the rational
strategy for each player is to reveal the secret. This makes the lottery fair, even
in the absence of a collateral.

B.3   Escrow
User a wants to buy from seller b an item that costs v Algos. We want to guaran-
tee that (1) b will get paid if a authorizes the payment; (2) a will be refunded if
b authorizes it; (3) if neither a nor b give their authorization, an escrow service
c will resolve the dispute, by either fully refunding a, or partially refunding a
with va Algos and giving the remaining (v − va ) Algos to b.
Escrow , tx.type = close and tx.asst = Algo and
              versig(txid, arg(1), a) and (tx.rcv = b or tx.rcv = Resolve ) 
          or versig(txid, arg(1), b) and (tx.rcv = a or tx.rcv = Resolve )
Resolve , tx.type = pay and tx.asst = Algo and versig(arg(0), arg(1), c) and
           (tx.rcv = a and tx.val = arg(0)) or 
           (tx.rcv = b and tx.val = v − arg(0))

B.4   Limit order
The limit order contract [2] allows a user a to exchange her Algos for units
of a certain asset τ , provided by any user. The contract imposes a lower bound
ρmin to the exchange rate τ /Algo, and guarantees its operation as long as it has
enough funds, and a deadline rmax is not reached (after then, a can close it). To
this purpose, the contract accepts two kinds of actions:
 – an atomic group of two pay transactions: the first one transfers v0 Algos from
   the contract to the sender of the second one; the second transaction transfers
   v1 units of τ to user a. The contract ensures that: (i) the ratio between v1
   and v0 is greater then a given constant ρmin ; (ii) v0 is greater than a given
                               A formal model of Algorand smart contracts      25

   constant vmin . Note that such a group can be issued by any user owning
   enough units of the asset τ , without requiring any interaction from a.
 – a single transaction where a closes the contract after the deadline rmax .

The following script implements this specification:
       txlen = 2 and txpos = 0 and
       tx(0).type = pay and tx(0).asst = Algo and tx(0).rcv = tx(1).snd and
       tx(1).type = pay and tx(1).asst = τ and tx(1).rcv
                                                        = a and
       tx(1).val/tx(0).val ≥ ρmin and tx(0).val ≥ vmin
       or
       txlen = 1 and tx.fv > rmax and                       
       tx.type = close and tx.asst = Algo and tx(0).rcv = a


B.5   Split

The split contract [3] is created by a user a, who want to transfer its funds to
users b0 and b1 in a fixed ratio ρ. The contract is initially funded with some
Algos from a, and once started it accepts two kinds of actions:

 – an atomic group of two pay transactions whose sender is the split contract:
   the first transaction transfers v0 Algos to b0 , while the second one transfers
   v1 Algos to b1 . The contract ensures that: (i) the ratio between v1 and v0 is
   equal to a given constant ρ; (ii) v0 is greater than a given constant vmin .
 – a single transaction where a closes the contract after a deadline rmax .

The following script implements this specification:
          txlen = 2 and tx(0).snd = tx(1).snd and
          tx(0).type = pay and tx(0).asst = Algo and tx(0).rcv = b0 and
          tx(1).type = pay and tx(1).asst = Algo and tx(1).rcv
                                                               = b1 and
          tx(1).val = ρ ∗ tx(0).val and tx(0).val ≥ vmin
          or
          txlen = 1 and tx.fv > rmax and                       
          tx.type = close and tx.asst = Algo and tx(0).rcv = a


C     Compiling scripts from our model to concrete ASC1

Table 2 summarizes the main checks performed by the script, and the values
stored in the scratch space. For brevity, we assume a sugared syntax of TEAL
(e.g., we use comparison operators in infix notation), and we do not detail the
checks needed to ensure that certain fields are not set. Notice that some of the
TEAL operators used in Table 2, like e.g., ConfigAsset, require LogicSigVer ≥
2 (see https://developer.algorand.org/docs/reference/teal/opcodes/).
When none of the conditions in the left column of Table 2 is satisfied, we make
the script generate an error, which corresponds to requiring Jtx(n).fK = ⊥.
26     Bartoletti et al.

               TEAL checks                    Values stored in scratch space
 gtxn n TypeEnum == pay                  tx(n).type := close
 gtxn n Amount == 0                      tx(n).asst := Algo
 gtxn n CloseRemainderTo != 0            tx(n).snd := gtxn n Sender
 ···                                     tx(n).rcv := gtxn n CloseRemainderTo
                                         tx(n).type := pay
 gtxn n TypeEnum == pay                  tx(n).asst := Algo
 gtxn n CloseRemainderTo == 0            tx(n).snd := gtxn n Sender
 ···                                     tx(n).rcv := gtxn n Receiver
                                         tx(n).val := gtxn n Amount
 gtxn n TypeEnum == axfer
                                         tx(n).type := close
 gtxn n AssetSender != 0
                                         tx(n).asst := gtxn n XferAsset
 gtxn n AssetAmount == 0
                                         tx(n).snd := gtxn n AssetSender
 gtxn n AssetCloseTo != 0
                                         tx(n).rcv := gtxn n AssetCloseTo
 ···
 gtxn n TypeEnum == axfer
                                         tx(n).type := pay
 gtxn n Sender != 0
                                         tx(n).asst := gtxn n XferAsset
 gtxn n AssetSender == 0
                                         tx(n).snd := gtxn n Sender
 gtxn n AssetAmount != 0
                                         tx(n).rcv := gtxn n AssetReceiver
 gtxn n AssetCloseTo == 0
                                         tx(n).val := gtxn n AssetAmount
 ···
 gtxn n TypeEnum == acfg
 gtxn n ConfigAsset == 0
                                         tx(n).type := gen
 (gtxn n ConfigAssetManager ==
                                         tx(n).snd := gtxn n Sender
  gtxn n ConfigAssetFreeze ==
                                         tx(n).rcv := gtxn n ConfigAssetManager
  gtxn n ConfigAssetReserve ==
                                         tx(n).val := gtxn n AssetAmount
  gtxn n ConfigAssetClawback)
 ···
 gtxn n TypeEnum == axfer
 gtxn n Sender == gtxn n AssetReceiver tx(n).type := optin
 gtxn n AssetSender == 0               tx(n).asst := gtxn n XferAsset
 gtxn n AssetAmount == 0               tx(n).snd := gtxn n Sender
 ···
 gtxn n TypeEnum == acfg
 len (gtxn n ConfigAssetManager) == 0
 len (gtxn n ConfigAssetFreeze) == 0   tx(n).type := burn
 len (gtxn n ConfigAssetReserve) == 0 tx(n).asst := gtxn n ConfigAsset
 len (gtxn n ConfigAssetClawback) == 0
 ···
                                         tx(n).type := rvk
 gtxn n TypeEnum == axfer
                                         tx(n).asst := gtxn n XferAsset
 gtxn n Sender != 0
                                         tx(n).snd := gtxn n AssetSender
 gtxn n AssetSender != 0
                                         tx(n).rcv := gtxn n AssetReceiver
 ···
                                         tx(n).val := gtxn n AssetAmount
 gtxn n TypeEnum == afrz                 tx(n).type := frz
 gtxn n AssetFrozen == true              tx(n).asst := gtxn n FreezeAsset
 ···                                     tx(n).snd := gtxn n FreezeAccount
 gtxn n TypeEnum == afrz                 tx(n).type := unfrz
 gtxn n AssetFrozen == false             tx(n).asst := gtxn n FreezeAsset
 ···                                     tx(n).snd := gtxn n FreezeAccount
 gtxn n TypeEnum == acfg
 gtxn n ConfigAsset != 0
 len (gtxn n ConfigAssetManager) != 0    tx(n).type := delegate
 (gtxn n ConfigAssetManager ==           tx(n).snd := gtxn n Sender
  gtxn n ConfigAssetFreeze ==            tx(n).rcv := gtxn n ConfigAssetManager
  gtxn n ConfigAssetReserve ==           tx(n).asst := gtxn n ConfigAsset
  gtxn n ConfigAssetClawback)
 ···
         Table 2: Compilation of the script tx(n).f in TEAL (sketch).
                                   A formal model of Algorand smart contracts             27

D     Proofs

Proof of Theorem 1

By induction on the length of the run.
    Conditions c1 and c2 are required at each step.
    Condition c1 prevents the same transaction t to appear again for the next
∆max rounds (t ∈/ Tlv ). Condition c2 requires t to be valid only in a time window
of at most ∆max rounds (t.lv − t.fv ≤ ∆max ). Therefore, it is impossible for t to
appear more than once.                                                           ⊓
                                                                                 ⊔


Proof of Theorem 2

By induction on the length of the run, and by cases on the rules generating each
step.
   By inspecting the rules, we can see that they all preserve the value for all
assets, except for [Burn] which completely destroys the asset, and [Gen] which can
create a fresh asset. The rules prevent a burnt asset to be re-created later on.
    The two special cases are taken into account in the definition of val τ (Γ), so
the theorem holds.                                                                ⊓
                                                                                  ⊔


Proof of Theorem 3

By induction on the length of the run, and by cases on the rules generating each
step.
    Inspecting each pair of (different) rules, we can observe that they either have
distinct labels or they have conflicting side conditions, so that at most one of
them can apply in each case. Further, we observe that in each rule the final state
is a function of the label and of the initial state.
    For part 3 of the theorem involving different labels W:T and W′ :T, we
                            W:T                                          T
further add that (Γ, K) ===⇒ (Γ ′ , K) is possible only when Γ −
                                                               → Γ ′ holds, and
the same holds for W′ :T. We conclude that the difference between W and W′
                                        ⇒ is derived from the determinism of −
is immaterial, since the determinism of =                                    →
which does not involve witnesses.                                            ⊓
                                                                             ⊔

Lemma 1. Let e = (tx.type = close and e ′ ), and let R be a run passing through
a state (Γ, K) with Γ = e[σ] | · · · and leading to (Γ ′ , K ′ ) with Γ ′ = e[σ ′ ] | Tlv′ |
 r′ | flx′ · · · , such that all intermediate states contain the account e[· · ·]. Then:

 1. dom σ ′ = {Algo};
 2. σ ′ (Algo) ≥ σ(Algo);
 3. if t is a transaction such that t.snd = e, t.asst = Algo, t 6∈ Tlv′ , and flx′ , r′ |= t,
                                                            W:t
    and JeKW                   ′         ′   ′
                                                ==⇒.
           t = true with W in K , then (Γ , K ) =
28      Bartoletti et al.

Proof. By construction, the script e only allows close transactions, and in par-
ticular it does not accept optin or gen transactions. Therefore, it must be
dom σ ′ = {Algo}, proving item 1. Further, the value σ ′ (Algo) can only increase
until e is closed, proving item 2. For item 3, since by hypothesis e evaluates to
true, then it must be t.type = close. Then, by definition of auth, it must be
auth(t, · · ·) = e. Therefore, W |= t holds, since JeKW
                                                      t = true.

    Note that, if the script e does not constrain the lx field, the hypothesis t 6∈ Tlv′
in item 3 can always be satisfied by setting a value of t.lx not used in Tlv′ . Further,
if e does not check signatures on t, doing this does not invalidate the possibility
of appending t. Therefore, in the following proofs we will omit checking that the
hypothesis t 6∈ Tlv′ holds.


Proof of Theorem 4

For item (1), assume that Σa , Σo ∈ Σ. By hypothesis, o has not sent a signature
sig o (Oracle , 1). By Lemma 1, in any reachable state Oracle [σ ′ ] | · · · it must
be dom σ ′ = {Algo}, and the value σ ′ (Algo) can only increase until Oracle is
closed. Consequently, to prove item (1) it enough to show that there exists some
transaction t in R such that t ∈ T a , and t is the first transaction in R whose
sender is Oracle . By the monotonicity of the balance of Oracle discussed before,
this implies the thesis, i.e. that t transfers at least σ(Algo) to a. We have the
following two cases:

(a) o has sent a signature s on (Oracle , 0) at round r ≤ rmax . By contradic-
    tion, assume that Oracle has not been closed in R within round r. Since R
    conforms to Σa , at round r, a has sent a transaction t′ ∈ T a with t′ .fv = r
    and witness 0 s. Since no transactions have closed Oracle , the contract is
    still open, so let σ ′ be its balance. As observed above, dom σ ′ = {Algo}, and
    so t′ satisfies the premises of either rule [Close-Open] or [Close-Pay]. Further, t′
    satisfies the script Oracle , so by item 3 of Lemma 1 it closes Oracle at round
    r — contradiction. Therefore, R contains at least a transaction which closes
    Oracle within round r: let t be the first one of these transactions. Since t
    must satisfy the script Oracle , one of the following cases must apply:
     (i) t.fv > rmax : impossible, because t has closed Oracle within r ≤ rmax ;
    (ii) t is validated by o’s signature on (Oracle , 1): impossible, since it would
         contradict the hypothesis of item (1);
   (iii) t is validated by o’s signature on (Oracle , 0): this implies that t ∈ T a —
         which proves the thesis.
(b) o has not sent a signature on (Oracle , 0) at any round r ≤ rmax . By contra-
    diction, assume that Oracle has not been closed in R within round rmax + 1.
    Since R conforms to Σa , at round rmax + 1, a has sent a transaction t′ ∈ T a
    with t′ .fv = rmax + 1. Since no transactions have closed Oracle , the contract
    is still open, so let σ ′ be its balance. As observed above, dom σ ′ = {Algo},
    and so t′ satisfies the premises of either rule [Close-Open] or [Close-Pay]. Further,
    t′ satisfies the script Oracle , so by item 3 of Lemma 1 it closes Oracle at
                                  A formal model of Algorand smart contracts          29

     round rmax + 1 — contradiction. Therefore, R contains at least a transaction
     which closes Oracle within round rmax + 1: let t be the first one of these
     transactions. Since t must satisfy the script Oracle , one of the following cases
     must apply:
      (i) t.fv > rmax and t.rcv = a: this implies that t ∈ T a — which proves the
          thesis.
     (ii) t is validated by o’s signature on (Oracle , 1): impossible, since it would
          contradict the hypothesis of item (1);
    (iii) t is validated by o’s signature on (Oracle , 0): impossible, since it would
          contradict the hypothesis of case (b) of item (1).

For item (2), assume that Σb , Σo ∈ Σ. By Lemma 1, in any reachable state
Oracle [σ ′ ] | · · · it must be dom σ ′ = {Algo}, and the value σ ′ (Algo) can only
increase until Oracle is closed. Consequently, to prove item (2) it enough to show
that there exists some transaction t in R such that t ∈ T b , and t is the first
transaction in R whose sender is Oracle . By the monotonicity of the balance
of Oracle discussed before, this implies the thesis, i.e. that t transfers at least
σ(Algo) to b.
    By hypothesis, o has sent a signature s′ on (Oracle , 1) at round r ≤ rmax . By
contradiction, assume that Oracle has not been closed in R within round r. Since
R conforms to Σb , at round r, b has sent a transaction t′ ∈ T b with t′ .fv = r and
witness 1 s′ . Since no transactions have closed Oracle , the contract is still open,
so let σ ′ be its balance. As observed above, dom σ ′ = {Algo}, and so t′ satisfies
the premises of either rule [Close-Open] or [Close-Pay]. Further, t′ satisfies the script
Oracle , so by item 3 of Lemma 1 it closes Oracle at round r — contradiction.
Therefore, R contains at least a transaction which closes Oracle within round r:
let t be the first one of these transactions. Since t must satisfy the script Oracle ,
one of the following cases must apply:
  (i) t.fv > rmax : impossible, because t has closed Oracle within round r ≤ rmax ;
 (ii) t is validated by o’s signature on (Oracle , 1): this implies that t ∈ T b —
      which proves the thesis.
(iii) t is validated by o’s signature on (Oracle , 0): impossible, since R would not
      conform to Σo , which requires that the oracle never signs both 0 and 1. ⊓  ⊔

Proof of Theorem 5
For item (i), assume that Σa ∈ Σ. By contradiction, assume that R does not
contain a transaction in T a . Since R conforms to Σa , at round r, user a has sent
a transaction t ∈ T a with t.fv = r and witness sa . By construction, t satisfies
the script HTLC . Hence, by Lemma 1, to prove the thesis we show that HTLC
was not closed earlier in R. By inspecting the script HTLC , there are only two
conditions under which a previous transaction t′ can close the contract:
 1. t′ .fv > rmax : impossible, because t.fv = r ≤ rmax ;
 2. t′ is validated using a preimage of ha : this implies that t′ ∈ T a — contradic-
    tion.
30      Bartoletti et al.

For item (ii), assume that Σb ∈ Σ, and that sa was not revealed before round
rmax + 1. By contradiction, assume that R does not contain a transaction in T b .
Since R conforms to Σb , at round rmax , user b has sent a transaction t ∈ T b with
t.fv = rmax . By construction, t satisfies the script HTLC . Hence, by Lemma 1,
to prove the thesis we show that HTLC was not closed earlier in R. By in-
specting the script HTLC , there are only two conditions under which a previous
transaction t′ can close the contract:

 1. t′ .fv > rmax : this implies that t′ ∈ T b — contradiction.
 2. t′ is validated using a preimage of ha : this implies, with overwhelming prob-
    ability, that sa was used as the preimage. In such case, it was revealed and
    occurs in R at round rmax — contradiction.

Proof of Theorem 6
The proof for the fairness of the lottery protocol when implemented on Bitcoin
appeared in [11, 12]. This protocol relies on running, simultaneously, two timed
commitments (for which we use HTLC ) and a contract that transfers the bets
to the winner, which can be computed after the secrets have been revealed (for
which we use Lottery ).
    We already proved the security of HTLC in Theorem 5, which implies part
1 of the thesis: a honest participant p will reveal her secret in time with a
transaction in T secr
                  p,q .
    For part 2, the argument is similar to the one for the original protocol. Briefly
put, if the other participant q does not to reveal sq in time, p wins the lottery
by timeout using a transaction in T tout
                                      q,p . If instead sq is revealed in time, since
sp was chosen in a uniformly random way, independently from sq (which has a
different hash), we have that the parity of sp + sq is a random bit, uniformly
distributed. Hence, if p won, her strategy makes her send a transaction in T plott
and claim the pot.
In the argument above we neglected the case where q reveals another preimage
than sq as his secret, since that can only happen with negligible probability.
Summing up, an honest p wins with at least 1/2 probability (up-to a negligible
quantity).

Proof of Theorem 7
The proof is analogous to the one for HTLC in Theorem 5.
                                         A formal model of Algorand smart contracts                                         31

   t.type = pay       t.snd = x          t.asst = Algo            t.rcv = y               flx , r |= t      t 6∈ Tlv
                                 ′                                          ′
   |= σ − t.val : Algo       σ = {Algo 7→ t.val}                  |= σ              y[· · ·] not in Γ
                                                                                                                        [Pay-Open]
                                                      t
       x[σ] | Γ | r | Tlv | fasst | flx | ffrz −
                                               →1
       x[σ − t.val : Algo] | y[σ ′ ] | Γ | r | Tlv ∪ {t} | fasst | upd(flx , t) | ffrz

 t.type = close       t.snd = x          t.rcv = y        t.asst = Algo                   flx , r |= t      t 6∈ Tlv
 dom (σ) = {Algo}          y[· · ·] not in x[σ] | Γ
                                                                                                                        [Close-Open]
                                                                        t
                    x[σ] | Γ | r | Tlv | fasst | flx | ffrz −
                                                            →1
                    y[σ] | Γ | r | Tlv ∪ {t} | fasst | upd(flx , t) | ffrz

  t.type = close       t.snd = x         t.rcv = y        t.asst = Algo                   flx , r |= t       t 6∈ Tlv
  dom (σ) = {Algo}
                                                                                                                        [Close-Pay]
                                                                    t
        x[σ] | y[σ ′ ] | Γ | r | Tlv | fasst | flx | ffrz −
                                                          →1
        y[σ ′ + σ(Algo) : Algo] | Γ | r | Tlv ∪ {t} | fasst | upd(flx , t) | ffrz

 t.type = close       t.snd = x         t.rcv = y         t.asst = τ                flx , r |= t     t 6∈ Tlv
                                                 ′            ′
 τ 6= Algo     σ(τ ) = v         τ ∈ dom (σ )          |= σ + v : τ                     τ 6∈ ffrz (x) ∪ ffrz (y)
                                                                                                                        [Close-Asst]
                ′                                             t
     x[σ] | y[σ ] | Γ | r | Tlv | fasst | flx | ffrz −
                                                     →1
     x[σ{τ 7→ ⊥}] | y[σ ′ + v : τ ] | Γ | r | Tlv ∪ {t} | fasst | upd(flx , t) | ffrz

t.type = pay    t.snd = x            t.rcv = y       t.val = v > 0                  t.asst = τ           flx , r |= t    t 6∈ Tlv
                                                 ′
|= σ − v : τ   τ ∈ dom (σ) ∩ dom (σ )                 τ 6∈ ffrz (x) ∪ ffrz (y)
                                                                                                                                    [Pay]
                       ′                                                t
         x[σ] | y[σ ] | Γ | r | Tlv | fasst | flx | ffrz −
                                                         →1
         x[σ − v : τ ] | y[σ ′ + v : τ ] | Γ | r | Tlv ∪ {t} | fasst | upd(flx , t) | ffrz

   t.type = pay       t.snd = x          t.rcv = y 6= x           t.val = 0               flx , r |= t      t 6∈ Tlv
                                                                                                                        [Pay-Zero]
                             ′                                                      t
               x[σ] | y[σ ] | Γ | r | Tlv | fasst | flx | ffrz −
                                                               →1
               x[σ] | y[σ ′ ] | Γ | r | Tlv ∪ {t} | fasst | upd(flx , t) | ffrz

         t.type = gen        t.snd = x           t.rcv = y         val = v               flx , r |= t      t 6∈ Tlv
         |= σ{τ 7→ v}       τ next fresh asset identifier
                                                                                                                        [Gen]
                                                          t
          x[σ] | Γ | r | Tlv | fasst | flx | ffrz −
                                                  →1
          x[σ{τ 7→ v}] | Γ | r | Tlv ∪ {t} | fasst {τ 7→ (y, x)} | upd(flx , t) | ffrz

          t.type = optin             t.snd = x  t.asst = τ flx , r |= t t 6∈ Tlv
                                               (
                                                 σ{τ 7→ 0} if τ 6∈ dom (σ)
          τ occurs in x[σ] | Γ            σ′ =                                   |= σ ′
                                                 σ         otherwise
                                                                                                                   [Optin]
                                                                                t
                      x[σ] | Γ | r | Tlv | fasst | flx | ffrz −
                                                              →1
                      x[σ ′ ] | Γ | r | Tlv ∪ {t} | fasst | upd(flx , t) | ffrz
32         Bartoletti et al.

           t.type = burn           t.asst = τ        snd (fasst (τ )) = x       flx , r |= t       t 6∈ Tlv
           τ ∈ dom (σ)          for all y[σ ′ ] in Γ : τ 6∈ dom (σ ′ )
                                                                                                              [Burn]
                                                              t
              x[σ] | Γ | r | Tlv | fasst | flx | ffrz −
                                                      →1
              x[σ{τ 7→ ⊥}] | Γ | r | Tlv ∪ {t} | fasst {τ 7→ ⊥} | upd(flx , t) | ffrz

t.type = rvk       t.snd = x            t.rcv = y        t.val = v     t.asst = τ        flx , r |= t     t 6∈ Tlv
                               ′
τ ∈ dom (σ) ∩ dom (σ )                  |= σ − v : τ       τ 6∈ ffrz (x) ∪ ffrz (y)
                                                                                                                     [Revoke]
                     ′                                             t
         x[σ] | y[σ ] | Γ | r | Tlv | fasst | flx | ffrz −
                                                         →1
         x[σ − v : τ ] | y[σ ′ + v : τ ] | Γ | r | Tlv ∪ {t} | fasst | upd(flx , t) | ffrz

                t.type = frz         t.snd = x           t.asst = τ     flx , r |= t     t 6∈ Tlv
                                 ′
                τ ∈ dom (σ) ffrz    = ffrz {x 7→ ffrz (x) ∪ {τ }}
                                                                                                     [Freeze]
                                                             t
                     x[σ] | Γ | r | Tlv | fasst | flx | ffrz −
                                                             →1
                                                                            ′
                         x[σ] | Γ | r | Tlv ∪ {t} | fasst | upd(flx , t) | ffrz

             t.type = unfrz             t.snd = x        t.asst = τ     flx , r |= t     t 6∈ Tlv
                             ′
             τ ∈ dom (σ) ffrz   = ffrz {x 7→ ffrz (x) \ {τ }}
                                                                                                     [Unfreeze]
                                                           t
                   x[σ] | Γ | r | Tlv | fasst | flx | ffrz −
                                                           →1
                                                                         ′
                      x[σ] | Γ | r | Tlv ∪ {t} | fasst | upd(flx , t) | ffrz

     t.type = delegate         t.snd = x        t.rcv = y         t.asst = τ        flx , r |= t    t 6∈ Tlv
     fst (fasst (τ )) = x
                                                                                                               [Delegate]
                                                 t
           Γ | r | Tlv | fasst | flx | ffrz −
                                            →1
           Γ | r | Tlv ∪ {t} | fasst {τ 7→ (y, snd (fasst (τ )))} | upd(flx , t) | ffrz

                                                                                           [Round]
                                          X
                         Γ | Tlv | r −
                                     →1 Γ | {t ∈ Tlv | t.lv > r} | r + 1

                                                   1 t                          t
                            T = t1 · · · tn     Γ −→ 1 Γ1 · · · Γn−1 −→1 Γn
                                                                      n

                                                                                            [TxG]
                                                          T
                                                      Γ−
                                                       → Γn

                                                 w                         [Net-Wit]
                                        (Γ, K) =⇒ (Γ, K ∪ {w})

                                                     X
                                                 → Γ′
                                                Γ−
                                                                       [Net-Round]
                                                     X
                                         (Γ, K) =⇒ (Γ ′ , K)

                                    T
                                → Γ′
                               Γ−             set (W) ⊆ K              W |= T
                                                                                    [Net-TxG]
                                                     W:T
                                          (Γ, K) ===⇒ (Γ ′ , K)

                            Fig. 5: The stateless ASC1 state machine.
