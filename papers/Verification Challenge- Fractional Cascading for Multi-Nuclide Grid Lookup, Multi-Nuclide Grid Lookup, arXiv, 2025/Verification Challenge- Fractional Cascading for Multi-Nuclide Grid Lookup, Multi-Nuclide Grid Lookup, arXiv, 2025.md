            Verification Challenge: Fractional Cascading for
                       Multi-Nuclide Grid Lookup

                                               Andrew R. Siegel
                                            Argonne National Laboratory
                                                 Lemont, IL, USA
                                              siegela@mcs.anl.gov



       We present a verification challenge based on the fractional cascading (FC) technique for accelerating
       repeated searches across a collection of sorted arrays. The specific context is nuclear cross section
       lookup in a simulation code, where a material consists of many nuclides, each with its own sorted
       energy grid. A naive search performs a binary search in each array individually. The FC-based
       cascade grid structure reduces this cost by performing a single binary search followed by constant-
       time refinements. The challenge consists of verifying the correctness of the FC algorithm with respect
       to the naive approach and validating its structural properties.


1     Problem Description
In particle transport simulations—used to model how particles such as neutrons move through and in-
teract with materials—accurate predictions depend on data known as nuclear cross sections. A nuclear
cross section represents the probability of a specific interaction (e.g., scattering or absorption) between a
particle and a nucleus, and this probability depends on the particle’s energy.
    To compute these interactions, codes like OpenMC (https://openmc.org, [1]) store cross section
data as numerical values tabulated on a sorted energy grid. Each nuclide (i.e., a specific type of atomic
nucleus, such as uranium-235 or hydrogen-1) has its own energy grid, which provides microscopic cross
sections—the interaction probabilities for individual nuclei—as a function of incident particle energy
(the energy of a particle as it enters the material).
    During a simulation, when a particle with a given energy interacts with a material (which may be
composed of many nuclides), the code must find where that energy lies in each nuclide’s grid in order to
interpolate the corresponding microscopic cross section. This results in repeated searches across multiple
similar sorted arrays—one per nuclide.
    A straightforward method performs a binary search in each of the k sorted arrays, leading to a total
query cost of O(k log(n)), where n is the average size of each grid. This challenge proposes an optimized
data structure based on fractional cascading1 (FC), which reduces the per-query cost to O(log(n) + k) by
reusing information between searches.


2     Cascade Grid Algorithm
The FC technique, summarized in Algorithm 1, constructs a cascade grid structure consisting of k aug-
mented energy grids M1 , M2 , . . . , Mk , derived from the original nuclide energy grids L1 , L2 , . . . , Lk . Each
Mi is a sorted array containing all elements of Li and every second element of Mi+1 . Each entry E ∈ Mi is
    1 https://en.wikipedia.org/wiki/Fractional_cascading


S.F. Siegel and G. Gopalakrishnan (Eds.):                                    © UChicago Argonne, LLC,
International Workshop on Verification of                                    Operator of Argonne National Laboratory
Scientific Software (VSS 2025)                                               This work is licensed under the
EPTCS 432, 2025, pp. 106–111, doi:10.4204/EPTCS.432.12                       Creative Commons Attribution License.
     Andrew R. Siegel                                                                                       107


     associated with two integer indices: p1 gives the location of E in Li , and p2 gives the approximate index
     of E in Mi+1 , accurate up to ±1.
          The cost of constructing Li and Mi is fixed and considered amortized over many (typically billions of
     searches). Once constructed, the search procedure begins with a binary search in M1 , then uses index p2
     to locate the position in M2 , correcting with one comparison if needed, and continues cascading down to
     Mk . Index p1 in each grid provides the lookup location in the corresponding original grid Li .

     Algorithm 1 Cascade Grid Cross Section Lookup
      1: for i ← 1 to k do
      2:     if i = 1 then
      3:          j ← binary search(Mi , E)
      4:     else
      5:          j ← p2 (correct if needed by comparing with Mi [p2 − 1])
      6:     end if
      7:     p1 , p2 ← indices associated with Mi [ j]
      8:     σi ← Li [p1 ]                                                ⊲ Microscopic cross section lookup
      9: end for



     3    Implementation and Properties to Verify
     A C implementation of the algorithm is provided in Appendix A. It uses standard data structures and
     binary search. A main function performs a small concrete test. For full verification, one could instead
     write a driver that initializes a set of sorted arrays, constructs the cascade structure, and compares the
     results of naive and FC-based lookup routines for a range of energies.
         We propose the following properties:
         • Correctness: For any energy value E, the FC-based cascade lookup returns the same indices in
           L1 , . . . , Lk as k independent binary searches.
         • Structural bound: The total size of the cascade data structure is bounded above by 2 ∑i |Li |.
         • Efficiency (optional): The lookup procedure performs exactly one binary search and at most one
           comparison per subsequent grid.


     A    Implementation

 1 # include      < stdlib .h >
 2 # include      < stdio .h >
 3 # include      < math .h >
 4 # include      < s t d b o o l.h >
 5

 6 static      float * M = NULL ;
 7 static      int * P1 = NULL , * P2 = NULL ;
 8 static      int * L _ s t a r t s = NULL , * M _ s t a r t s = NULL , * M _ s i z e s = NULL ;
 9 static      int n _ g l o b a l;
10

11   // Binary search on a float array
     108                         Verification Challenge: Fractional Cascading for Multi-Nuclide Grid Lookup


12 int b i n a r y _ s e a r c h ( const float * arr , int size , float key ) {
13     int lo = 0 , hi = size - 1 , mid , result = 0;
14     while ( lo <= hi ) {
15             mid = ( lo + hi ) / 2;
16             if ( arr [ mid ] <= key ) {
17                     result = mid ;
18                     lo = mid + 1;
19             } else {
20                     hi = mid - 1;
21             }
22     }
23     return result ;
24 }

25

26 // Setup the f r a c t i o n a l c a s c a d i n g s t r u c t u r e
27 void f c _ s e t u p( const float * arrays , const int * sz , int n ) {
28     n_global = n;
29     L _ s t a r t s = malloc ( n * sizeof ( int ) ) ;
30     M _ s t a r t s = malloc ( n * sizeof ( int ) ) ;
31     M _ s i z e s = malloc ( n * sizeof ( int ) ) ;
32

33         int t o t a l _ L = 0;
34         for ( int i = 0; i < n ; ++ i ) {
35             L _ s t a r t s[ i ] = t o t a l _ L;
36             t o t a l _ L += sz [ i ];
37         }
38

39         int m a x _ t o t a l _ M = 2 * t o t a l _ L;
40         M = malloc ( m a x _ t o t a l _ M * sizeof ( float ) ) ;
41         P1 = malloc ( m a x _ t o t a l _ M * sizeof ( int ) ) ;
42         P2 = malloc ( m a x _ t o t a l _ M * sizeof ( int ) ) ;
43

44         int t o t a l _ M _ s i z e = 0;
45         for ( int i = n - 1; i >= 0; --i ) {
46             const float * Li = arrays + L _ s t a r t s[ i ];
47             int L i _ s i z e = sz [ i ];
48             int t a i l _ s t a r t = ( i < n - 1) ? M _ s t a r t s[ i + 1] : 0;
49             int t a i l _ s i z e = ( i < n - 1) ? ( M _ s i z e s[ i + 1] + 1) / 2 : 0;
50
51              int M i _ s t a r t = t o t a l _ M _ s i z e ;
52              M _ s t a r t s[ i ] = M i _ s t a r t;
53              int li = 0 , ti = 0 , mi = 0;
54

55              while ( li < L i _ s i z e && ti < t a i l _ s i z e) {
56                  float lv = Li [ li ];
57                  float tv = M [ t a i l _ s t a r t + 2 * ti ];
58                  if ( lv <= tv ) {
59                       M [ M i _ s t a r t + mi ] = lv ;
60                       P1 [ M i _ s t a r t + mi ] = li ;
61                       P2 [ M i _ s t a r t + mi ] = -1;
62                       li ++; mi ++;
63                  } else {
      Andrew R. Siegel                                                                           109


 64                        M [ M i _ s t a r t + mi ] = tv ;
 65                        P1 [ M i _ s t a r t + mi ] = -1;
 66                        P2 [ M i _ s t a r t + mi ] = 2 * ti ;
 67                        ti ++; mi ++;
 68                     }
 69             }
 70             while ( li < L i _ s i z e) {
 71                     M [ M i _ s t a r t + mi ] = Li [ li ];
 72                     P1 [ M i _ s t a r t + mi ] = li ;
 73                     P2 [ M i _ s t a r t + mi ] = -1;
 74                     li ++; mi ++;
 75             }
 76             while ( ti < t a i l _ s i z e) {
 77                     float tv = M [ t a i l _ s t a r t + 2 * ti ];
 78                     M [ M i _ s t a r t + mi ] = tv ;
 79                     P1 [ M i _ s t a r t + mi ] = -1;
 80                     P2 [ M i _ s t a r t + mi ] = 2 * ti ;
 81                     ti ++; mi ++;
 82             }
 83             M _ s i z e s[ i ] = mi ;
 84             t o t a l _ M _ s i z e += mi ;
 85        }
 86   }
 87

 88 int * f c _ l o o k u p( const float * arrays , int n , const int * sz , float key ) {
 89      int * i n d i c e s = malloc ( n * sizeof ( int ) ) ;
 90      int j = b i n a r y _ s e a r c h ( M + M _ s t a r t s [0] , M _ s i z e s [0] , key ) ;
 91
 92        for ( int i = 0; i < n ; ++ i ) {
 93            int pos = M _ s t a r t s[ i ] + j ;
 94            const float * L = arrays + L _ s t a r t s[ i ];
 95            int L_size = sz [ i ];
 96            if ( P1 [ pos ] != -1) {
 97                 // If key is beyond the end of the array , return last index
 98                 if ( key >= L [ L_size - 1]) {
 99                         i n d i c e s[ i ] = L_size - 1;
100                 } else {
101                         i n d i c e s[ i ] = P1 [ pos ];
102                 }
103            } else {
104                 int idx = 0;
105                 while ( idx + 1 < L_size && L [ idx + 1] <= key ) idx ++;
106                 i n d i c e s[ i ] = idx ;
107            }
108

109             if ( i <   n - 1) {
110                  int   guess = P2 [ pos ];
111                  int   n e x t _ s t a r t = M _ s t a r t s[ i + 1];
112                  int   n e x t _ s i z e = M _ s i z e s[ i + 1];
113
114                  if ( guess >= 1 && guess < n e x t _ s i z e &&
115                       M [ n e x t _ s t a r t + guess ] > key &&
      110                         Verification Challenge: Fractional Cascading for Multi-Nuclide Grid Lookup


116                         M [ n e x t _ s t a r t + guess - 1] <= key ) {
117                         j = guess - 1;
118                     } else if ( guess >= 0 && guess < n e x t _ s i z e) {
119                         j = guess ;
120                     } else {
121                         // F a l l b a c k: re - search if guess is i n v a l i d
122                         j = b i n a r y _ s e a r c h ( M + next_start , next_size , key ) ;
123                     }
124             }
125         }
126         return i n d i c e s;
127   }
128

129 // Naive lookup to v a l i d a t e f c _ l o o k u p
130 int * n a i v e _ l o o k u p ( const float * arrays , const int * sz , int n , float key )
        {
131       int * i n d i c e s = malloc ( n * sizeof ( int ) ) ;
132       int offset = 0;
133       for ( int i = 0; i < n ; ++ i ) {
134             int s = sz [ i ];
135             int idx = 0;
136             while ( idx + 1 < s && arrays [ offset + idx + 1] <= key )
137                     idx ++;
138             i n d i c e s[ i ] = idx ;
139             offset += s ;
140      }
141       return i n d i c e s;
142 }
143

144 int main ( void ) {
145     int n = 3;
146     int sz [] = {5 , 6 , 4};
147     float arrays [] = {
148          1.0 , 2.0 , 3.0 , 4.0 , 5.0 ,
149          1.5 , 2.5 , 3.5 , 4.5 , 5.5 , 6.5 ,
150          0.5 , 1.5 , 2.5 , 3.5
151     };
152

153         // Setup the f r a c t i o n a l c a s c a d e s t r u c t u r e
154         f c _ s e t u p( arrays , sz , n ) ;
155

156         // Run m u l t i p l e tests
157         float t e s t _ k e y s [7] = {0.0 , 1.4 , 2.0 , 3.2 , 4.7 , 6.0 , 7.0};
158         int n u m _ t e s t s = sizeof ( t e s t _ k e y s ) / sizeof ( t e s t _ k e y s [0]) ;
159

160         for ( int t = 0; t < n u m _ t e s t s ; ++ t ) {
161             float key = t e s t _ k e y s[ t ];
162             int * f c _ r e s u l t = f c _ l o o k u p( arrays , n , sz , key ) ;
163             int * n a i v e _ r e s u l t = n a i v e _ l o o k u p ( arrays , sz , n , key ) ;
164
165               printf ( " Key = %.2 f \ n " , key ) ;
166               bool ok = true ;
      Andrew R. Siegel                                                                                        111


167               for ( int i = 0; i < n ; ++ i ) {
168                    printf ( " Array % d : fc = % d , e x p e c t e d = % d \ n " ,
169                                i , f c _ r e s u l t[ i ] , n a i v e _ r e s u l t [ i ]) ;
170                    if ( f c _ r e s u l t[ i ] != n a i v e _ r e s u l t [ i ])
171                          ok = false ;
172               }
173               if (! ok )
174                    printf ( " M I S M A T C H D E T E C T E D\ n " ) ;
175               else
176                    printf ( " Match \ n " ) ;
177               printf ( " \ n " ) ;
178
179               free ( f c _ r e s u l t) ;
180               free ( n a i v e _ r e s u l t ) ;
181         }
182

183         // Clean up
184         free ( M ) ;
185         free ( P1 ) ;
186         free ( P2 ) ;
187         free ( L _ s t a r t s) ;
188         free ( M _ s t a r t s) ;
189         free ( M _ s i z e s) ;
190   }


      Acknowledgment. This publication is based on work supported by the U.S. Department of Energy
      under contract DE-AC02-06CH11357.


      References
      [1] Paul K. Romano, Nicholas E. Horelik, Bryan R. Herman, Adam G. Nelson, Benoit Forget & Kord Smith
          (2015): OpenMC: A state-of-the-art Monte Carlo code for research and development. Annals of Nuclear
          Energy 82, pp. 90–97, doi:10.1016/j.anucene.2014.07.048. Joint International Conference on Supercomputing
          in Nuclear Applications and Monte Carlo 2013, SNA + MC 2013. Pluri- and Trans-disciplinarity, Towards
          New Modeling and Numerical Simulation Paradigms.
