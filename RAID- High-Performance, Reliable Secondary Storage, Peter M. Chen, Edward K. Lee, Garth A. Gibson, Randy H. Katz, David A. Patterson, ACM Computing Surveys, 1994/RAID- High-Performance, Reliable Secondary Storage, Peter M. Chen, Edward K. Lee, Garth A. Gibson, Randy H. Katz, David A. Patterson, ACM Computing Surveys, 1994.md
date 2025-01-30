# Raid: High-Performance, Reliable Secondary Storage

PETER M. CHEN
Department of Electr~cal Engineering and Computer Sctence, 1301 Beal Avenue, University of Michigan, Ann Arbor, Michigan, 48109-2122

## Edward K. Lee

DECSystems Research Center, 130 Lytton Avenue. Palo Alto, California 94301-1044

## Garth A. Gibson

School of Computer Sctence, Carnegie Mellon University, 5000 Forbes Aven ue, Pittsburgh, Pennsylvania 15213-3891

## Randy H. Katz

Department of Electrical Engineering and Computer Sctence. 571 Evans Hall, University of California, Berkeley, California 94720

## David A. Patterson

Department of Electrical Engineering and Computer Science, 571 Euans Hall, University of Cahfornia, Berkeley, California 94720

```
Disk arrays were proposed in the 1980s as a way to use parallelism between multiple
disks to improve aggregate 1/0 performance. Today they appear in the product lines of
most major computer manufacturers. This article gives a comprehensive overview of
disk arrays and provides a framework in which to organize current and future work.
First, the article introduces disk technology and reviews the driving forces that have
popularized disk arrays: performance and reliability. It discusses the two architectural
techniques used in disk arrays: striping across multiple disks to improve performance
and redundancy to improve reliability. Next, the article describes seven disk array
architectures, called RAID (Redundant Arrays of Inexpensive Disks) levels O–6 and
compares their performance, cost, and reliability. It goes on to discuss advanced
research and implementation topics such as refining the basic RAID levels to improve
performance and designing algorithms to maintain data consistency. Last, the article
describes six disk array prototypes or products and discusses future opportunities for
research, with an annotated bibliography of disk array-related literature.

Categories and Subject Descriptors: B.4.2 [Input/ Output and Data
Communications]: Input/Output Devices; B.4.5 [Input/ Output and Data
Communications]: Reliability, Testing, and Fault-Tolerance; D.4.2 [Operating
Systems]: Storage Management; E.4 [Data]: Coding and Information Theory;
General Terms: Design, Performance, Reliability
Additional Key Words and Phrases: Disk Array, parallel 1/0, RAID, redundancy,
storage, striping

```

Permission to copy without fee all or part of this material is granted provided that the copies are not made or distributed for direct commercial advantage, the ACM copyright notice and the title of the publication and its data appear, and notice is given that copying is by permission of the Association for Computing Machinery, To copy otherwise, or to republish, requires a fee and/or specific permission.

01994 ACM 0360-0300/94/0600-0145 $03,50

## Acm Computmg  Vol 26, No. 2, June 1994 Contents

| 2.1 Disk Termmology 2.2 Data Paths 2.3 Technology Trends      |                |                        |                 |             |     |
|---------------------------------------------------------------|----------------|------------------------|-----------------|-------------|-----|
| 3 DISK                                                        | ARRAY          | BASICS                 |                 |             |     |
| 3.1 Data                                                      | StrlpIng       | and Redundancy         |                 |             |     |
| 32                                                            | Basic RAID     | Orgamzations           |                 |             |     |
| 33                                                            | Performance    | and C!ost Comparisons  |                 |             |     |
| 34                                                            | Reliability    |                        |                 |             |     |
| 35                                                            | Implementation | Considerations         |                 |             |     |
| 4 ADVANCED                                                    | TOPICS         |                        |                 |             |     |
| 41                                                            | Impruvmg       | Small                  | Write           | Performance | for |
|                                                               | RAID           | Leve15                 |                 |             |     |
| 42                                                            | Declustered    | Parity                 |                 |             |     |
| 43                                                            | Exploltmg      | On-I,lne               | Spare Disks     |             |     |
| 44                                                            | Data           | Strip] ngm             | Dlsli Arrays    |             |     |
| 45                                                            | Performance    | and Rellabdlty         | Modellng        |             |     |
| 5. CASE                                                       | STUDIES        |                        |                 |             |     |
| 51                                                            | Thmkmg         | Mach] nes Corporation  | ScaleArray      |             |     |
| 52                                                            | StorageTek     | Iceherg                | 9200 D]sk Array | Subsystem   |     |
| 5.3 NCR 6298 5.4 l'lckerTAIP/DataMesh 5.5 The RAID-11 Storage | Server         |                        |                 |             |     |
| 56                                                            | IBM            | Hagar                  | Disk Array      | Controller  |     |
| 6                                                             | OPPORTUNITIES  | F'OR FUTURE            | RESEARCH        |             |     |
| 61                                                            | Experience     | with                   | Disk Arrays     |             |     |
| 62                                                            | InteractIon    | among New Orgamzatlons |                 |             |     |
| 63                                                            | Scalabdlty,    | Massively              | Parallel        | Computers,  |     |
|                                                               | and Small      | Disks                  |                 |             |     |
| 64                                                            | Latency        |                        |                 |             |     |
| 7                                                             | CONCLUSIONS    |                        |                 |             |     |
| ACKNOWLEDGMENTS                                               |                |                        |                 |             |     |

## 1. Introduction

In recent years, interest in RAID, Redundant Arrays of Inexpensive Disks,l has grown explosively. The driving force behind this phenomenon is the sustained exponential improvements in the performance and density of semiconductor technology. Improvements in semiconductor technology make possible faster microprocessors and larger primary memory systems which in turn require

1Because of the restrictiveness of "Inexpensive,"
sometimes RAID is said to stand for "Redundant Arrays of Independent Disks."
ACM Computing  Vol 26, No 2, June 1994
larger, higher-performance secondary storage systems. These improvements have both quantitative and qualitative consequences.

On the quantitative side, Amdahl's Law [Amdahl 1967] predicts that large improvements in microprocessors will result in only marginal improvements in overall system performance unless accompanied by corresponding improvements in secondary storage systems. Unfortunately, while RISC microprocessor performance has been improving 50~0 or more per year [Patterson and Hennessy 1994, p. 27], disk access times, which depend on improvements of mechanical systems, have been improving less than 10% per year. Disk transfer rates, which track improvements in both mechanical systems and magnetic-media densities, have improved at the faster rate of approximately 20% per year, but this is still far slower than the rate of processor improvement. Assuming that semiconductor and disk technologies continue their current trends, we must conclude that the performance gap between microprocessors and magnetic disks will continue to widen.

In addition to the quantitative effect, a second, perhaps more important, qualitative effect is driving the need for higherperformance secondary storage systems.

As microprocessors become faster, they make possible new applications and greatly expand the scope of existing applications. In particular, image-intensive applications such as video, hypertext, and multimedia are becoming common. Even in existing application areas such as computer-aided design and scientific computing, faster microprocessors make it possible to tackle new problems requiring faster access to larger data sets. This shift in applications, along with a trend toward large, shared, high-performance, network-based storage systems, is causing us to reevaluate the way we design and use secondary storage systems [Katz 1992].

Disk arrays, which organize multiple, independent disks into a large, high-performance logical disk, are a natural solution to the problem. Disk arrays stripe data across multiple disks and access them in parallel to achieve both higher data transfer rates on large data accesses and higher 1/0 rates on small data accesses [Salem and Garcia-Molina 1986; Livny et al. 1987]. Data striping also results in uniform load balancing across all of the disks, eliminating hot spots that otherwise saturate a small number of disks while the majority of disks sit idle.

Large disk arrays, are highly vulnerable to disk failures however. A disk array with 100 disks is 100 times more likely to fail than a single-disk array. An MTTF (mean-time-to-failure) of 200,000 hours, or approximately 23 years, for a single disk implies an MTTF of 2000 hours, or approximately three months, for a disk array with 100 disks. The obvious solution is to employ redundancy in the form of error-correcting codes to tolerate disk failures. This allows a redundant disk array to avoid losing data for much longer than an unprotected single disk. However, redundancy has negative consequences. Since all write operations must update the redundant information, the performance of writes in redundant disk arrays can be significantly worse than the performance of writes in nonredundant disk arrays. Also, keeping the redundant information consistent in the face of concurrent 1/0 operations and system crashes can be difficult.

A number of different data-striping and redundancy schemes have been developed. The combinations and arrangements of these schemes lead to a bewildering set of options for users and designers of disk arrays. Each option presents subtle tradeoffs among reliability, performance, and cost that are difficult to evaluate without understanding the alternatives. To address this problem, this article presents a systematic tutorial and survey of disk arrays. We describe seven basic disk array organizations along with their advantages and disadvantages and compare their reliability, performance, and cost. We draw attention to the general principles governing the design and configuration of disk arrays as well as practical issues that must be addressed in the implementation of disk arrays. A later section describes optimization and variations to the seven basic disk array organizations. Finally, we discuss existing research in the modeling of disk arrays and fruitful avenules for future research. This article should be of value to anyone interested in disk arrays, including students, researchers, designers, and users of disk arrays.

## 2. Background

This section provides basic background material on disks, 1/0 data paths, and disk technology trends for readers who are unfamiliar with secondary storage systems.

## 2.1 Disk Terminology

Figure 1 illustrates the basic components of a simplified magnetic disk drive. A
disk consists of a set of platters coated with a magnetic medium rotating at a constant angular velocity and a set of disk arms with magnetic read/write heads that are moved radially across the platters' surfaces by an actuator. Once the heads are correctly positioned, data is read and written in small arcs called sectors on the platters' surfaces as the platters rotate relative to the heads. Although all heads are moved collective] y, in almost every disk drive, only a single head can read or write data at any given time. A complete circular swath of data is referred to as a track, and each platter's surface consists of concentric rings of tracks. A vertical collection of tracks at the same radial position is logically referred to as a cylinder. Sectors are numbered so that a sequential scan of all sectors traverses the entire disk in the minimal possible time.

Given the simplified disk described above, disk service times can be broken into three primary components: seek time, rotational latency, and data trarisfer time. Seek time is the amount of time needed to move a head to the correct radial position and typically ranges from

ACM Computing  Vol. 26, No 2, June 1994

![3_image_0.png](3_image_0.png)

Figure 1. Disk terminology Heads res] de on arms which are positioned by actuators. Tracks are concentric rings cm a platter. A sector is the basic unit of reads and writes A cylinder is a stack of tracks at one actuator positron. An HDA (head-disk assembly) is everything in the figure plus the air-tight casing In some devices it M possible to transfer data from multiple surfaces simultaneously, but this is both rare and expensive. The collection of heads that participate m a single logical transfer that is suread over .-
multiple surfaces is called a head groap.
1 to 30 milliseconds depending on the seek distance and the particular disk. Rotational latency is the amount of time needed for the desired sector to rotate under the disk head. Full rotation times for disks vary currently from 8 to 28 milliseconds. The data transfer time is dependent on the rate at which data can be transferred to/from a platter's surface and is a function of the platter's rate of rotation, the density of the magnetic media, and the radial distance of the head from the center of the platter—some disks use a technique called zone-bit-recording to store more data on the longer outside tracks than the shorter inside tracks. Typical data transfer rates range from 1 to 5 MB per second. The seek time and rotational latency are sometimes collectively referred to as the heacl-positioning time. Table 1 tabulates the statistics for a typical high-end disk available in 1993.

The slow head-positioning time and fast data transfer rate of disks lead to very different performance for a sequence of accesses depending on the size and relative location of each access. Suppose we need to transfer 1 MB from the disk in Table 1, and the data is laid out in two ways: sequential within a single cylinder or randomly placed in 8 KB
blocks. In either case the time for the ACM Comput]ng  Vol 26, No 2, June 1994

Table 1. Speclflcatlons for the Seagate ST43401 N
Elite-3 SCSI D!sk Drive

| Table               | 1.          | Speclflcatlons   | for the   | Seagate   | ST43401   | N   |
|---------------------|-------------|------------------|-----------|-----------|-----------|-----|
| Elite-3             | SCSI        | D!sk Drive       |           |           |           |     |
| Form                | Factor/Disk | Diameter         | 5,25 inch |           |           |     |
| Capxity             | 2.8 GB      |                  |           |           |           |     |
| Cylinders           | 2627        |                  |           |           |           |     |
| Tracks Per Cylinder | 21          |                  |           |           |           |     |
| Sec[ors Pcr Tmck    | -99         |                  |           |           |           |     |
| Bytes Pcr Sector    | 512         |                  |           |           |           |     |
| Full                | Rolahon     | Time             | 11.lms    |           |           |     |
| Mlnunum             | Seek        |                  |           |           |           |     |
| (single cylinder)   | 1,7 ms      |                  |           |           |           |     |
| Average Seek        | 11.Oms      |                  |           |           |           |     |
| (random             | cylinder    | to cylmdcr)      |           |           |           |     |
| ~                   |             |                  |           |           |           |     |

~
Average seek in this table 1s calculated assuming a umform distribution of accesses. This is the standard way manufacturers report average seek times.

In reality, measurements of production systems show that spatial locality sigmficantly lowers the effective average seek distance [Hennessy and Patterson 1990, p 559]
actual data transfer of 1 MB is about 200 ms. But the time for positioning the head goes from about 16 ms in the sequential layout to about 2000 ms in the random layout. This sensitivity to the workload is why I/O-intensive applications are categorized as high data rate, meaning minimal head positioning via large, sequential accesses, or high 1/0 rate, meaning lots of head positioning via small, more random accesses. For example, scientific programs that manipulate large arrays of data fall in the high data rate category, while transaction-processing programs fall in the high 1/0 rate category.

## 2.2 Data Paths

A hierarchy of industry standard interfaces has been defined for transferring data recorded on a disk platter's surface to or from a host computer. In this section we review the complete data path, from a disk to a users' application (Figure 2). We assume a read operation for the purposes of this discussion.

On the disk platter's surface, information is represented as reversals in the direction of stored magnetic fields. These "flux reversals" are sensed, amplified, and digitized into pulses by the lowestlevel read electronics. The protocol ST506/ 412 is one standard that defines an interface to disk systems at this lowest, most inflexible, and technology-dependent level. Above this level of the read electronics path, pulses are decoded to separate data bits from timing-related flux reversals. The bit-level ESDI (Enhanced Small Device Interface) and SMD
(Storage Module Interface) standards define an interface at this more flexible, encoding-independent level. Then, to be transformed into the highest, most flexible packet-level, these bits are aligned into bytes, error-correcting codes applied, and the extracted data delivered to the host as data blocks over a peripheral bus interface such as SCSI (Small Computer Standard Interface), or IPI-3 (the third level of the Intelligent Peripheral Interface). These steps are performed today by intelligent on-disk controllers, which often include speed matching and caching
"track buffers." SCSI and IPI-3 also include a level of data mapping: the computer specifies a logical block number, and the controller embedded on the disk maps that block number to a physical cylinder, track, and sector. This mapping allows the embedded disk controller to avoid bad areas of the disk by remapping logical blocks that are affected to new areas of the disk.

Topologies and devices on the data path between disk and host computer vary widely depending on the size and type of 1/0 system. Mainframes have the richest 1/0 systems, with many devices and complex interconnection schemes to access them. An IBM channel path, which encompasses the set of cables and associated electronics that transfer data and control information between an 1/0 device and main memory, consists of a channel, a storage director, and a head of string. The collection of disks that share the same pathway to the head of string is called a string. In the workstation/file server world, the channel processor is usually called an 1/0 controller or host-bus adaptor (HBA), and the functionality of the storage director and head of string is contained in an embedded controller on the disk drive. As in the mainframe world, the use of high-level peripheral interfaces such as SCSI and IPI-3 allow multiple disks to share a single peripheral bus or string.

From the HBA, data is transferred via direct memory access, over a system bus, such as VME (Versa Module Eurocarcl),
S-Bus, MicroChannel, EISA (Extended Industry Standard Architecture), or PCI
(Peripheral Component Interconnect), to the host operating system's buffers. Then, in most operating systems, the CPU performs a memory-to-memory copy over a high-speed memory bus from the operating system buffers to buffers in the application's address space.

## 2.3 Technology Trends

Much of the motivation for disk arrays comes from the current trends in disk technology. As Table 2 shows, magnetic disk drives have been improving rapidly by some metrics and hardly at all by other metrics. Smaller distances between the magnetic read/write head and the disk surface, more accurate positioning

ACM Computmg  Vol. 26, No 2, June 1994
.-A -. ..-,

![5_image_0.png](5_image_0.png)

Figure 2. Host-to-device pathways. Data that is read from a magnetic disk must pass through many layers on its way to the requesting processor, Each dashed line marks a standard interface Lower interfaces such as ST506 deal more closelv with the raw maxnetic fields and are hi~hlv technology dependent, Higher layers such as SCSI d;al in packets or b~ocks of data and are ;or; technology independent, A string connects multiple disks to a single 1/0 controller, control of the string 1s distributed between the 1/0 and disk controllers.
electronics, and more advanced magnetic media have increased the recording density on the disks dramatically. This increased density has improved disks in two ways. First, it has allowed disk capacities to stay constant or increase, even while disk sizes have decreased from 5.25 inches in 1983 to 1.3 inches in 1993.

Second, the increased density, along with an increase in the rotational speed of the disk, has made possible a substantial increase in the transfer rate of disk drives.

ACM Computmg  Vol 26, No 2, June 1994 On the other hand, seek times have improved very little, only decreasing from approximately 20 ms in 1980 to 10 ms today. Rotational speeds have increased at a similarly slow rate from 3600 revolutions per minute in 1980 to 5400-7200 today.

## 3. Disk Array Basics

This section examines basic issues in the design and implementation of disk

|                                                     | Table 2.         | Trends                  | in Disk Technology. 1993 Historical   | Rate   |
|-----------------------------------------------------|------------------|-------------------------|---------------------------------------|--------|
|                                                     |                  | of Improvement          |                                       |        |
|                                                     | 50-150 Mbils/sq. | inch                    | 27% per year                          |        |
| And                                                 | Density          |                         |                                       |        |
| Linear                                              | Density          | 40,000-60,000 bilslinch | 13% per year                          |        |
| Inter-Track                                         | Density          |                         |                                       |        |
| Capacity (3.5" form factor) Transfer Rate Seek Time |                  |                         |                                       |        |

Magnetic disks are improving rapidly in density and capacity, but more slowly in performance. A real densitv is the recording densitv Ber sauare inch of magnetic media. In 1989, IBM demonstrated a 1 Gbit/;q.-inch densityi; a labo;a;ory environment. Lines; density is the number of bits written along a track. Intertrack density refers to the number of concentric tracks on a single platter.
arrays. In particular, we examine the concepts of data striping and redundancy; basic RAID organizations; performance and cost comparisons between the basic RAID organizations; reliability of RAID-based systems in the face of system crashes, uncorrectable bit-errors, and correlated disk failures; and finally, issues in the implementation of block-interleaved, redundant disk arrays.

## 3.1 Data Striping And Redundancy

Redundant disk arrays employ two orthogonal concepts: data striping for improved performance and redundancy for improved reliability. Data striping distributes data transparently over multiple disks to make them appear as a single fast, large disk. Striping improves aggregate 1/0 performance by allowing multiple 1/0s to be serviced in parallel. There are two aspects to this parallelism. First, multiple independent requests can be serviced in parallel by separate disks. This decreases the queuing time seen by 1/0 requests. Second, single multipleblock requests can be serviced by multiple disks acting in coordination. This increases the effective transfer rate seen by a single request. The more disks in the disk array, the larger the potential performance benefits. Unfortunately, a large number of disks lowers the overall reliability of the disk array, as mentioned before. Assuming independent failures, 100 disks collectively have only 1/100th the reliability of a single disk. Thus, redundancy is necessary to tolerate disk failures and allow continuous operation without data loss.

We will see that the majority of redundant disk array organizations can be distinguished based on two features: (1) the granularity of data interleaving and (2) the method and pattern in which the redundant information is computed and distributed across the disk array. Data interleaving can be characterized as either fine grained or coarse grained. Finegrained disk arrays conceptually interleave data in relatively small units so that all 1/0 requests, regardless of their size, access all of the disks in the disk array. This results in very high data transfer rates for all 1/0 requests but has the disadvantages that (1) only one logical 1/0 request can be in service at any given time and (2) all disks must waste time positioning for every request.

ACM Computing  Vol. 26, No. 2, June 1994
Coarse-grained disk arrays interleave data in relatively large units so that small 1/0 requests need access only a small number of disks while large requests can access all the disks in the disk array.

This allows multiple small requests to be serviced simultaneously while still allowing large requests to see the higher transfer rates afforded by using multiple disks.

The incorporation of' redundancy in disk arrays brings up two somewhat orthogonal problems. The first problem is to select the method for computing the redundant information. Most redundant disk arrays today use parity, though some use Hamming or Reed-Solomon codes.

The second problem is that of selecting a method for distributing the redundant information across the disk array. Although there are an unlimited number of patterns in which redundant information can be distributed, we classify these patterns roughly into two different distributions schemes, those that concentrate redundant information on a small number of disks and those that distributed redundant information uniformly across all of the disks. Schemes that uniformly distribute redundant information are generally more desirable because they avoid hot spots and other load-balancing problems suffered by schemes that do not distribute redundant information uniformly. Although the basic concepts of data striping and redundancy are conceptually simple, selecting between the many possible data striping and redundancy schemes involves complex tradeoffs between reliability, performance, and cost.

## 3.2 Basic Raid Organizations

This section describes the basic RAID
organizations that will be used as the basis for further examinations of the performance, cost, and reliability of disk arrays. In addition to presenting RAID
levels 1 through 5 that first appeared in the landmark paper by Patterson, Gibson, and Katz [Patterson et al. 1988], we present two other RAID organizations, RAID levels O and 6, that have since become generally accepted.x For the benefit of those unfamiliar with the original numerical classification of RAID, we will use English phrases in preference to the numerical classifications. It should come as no surprise to the reader that even the original authors have been confused sometimes with regard to the disk array organization referred to by a particular RAID level! Figure 3 illustrates the seven RAID organizations schematically.

## 3.2.1 Nonredundant (Raid Level O)

A nonredundant disk array, or RAID level O, has the lowest cost of any RAID organization because it does not employ redundancy at all. This scheme offers the best write performance since it does not need to update redundant information.

Surprisingly, it does not have the best read performance. Redundancy schemes that duplicate data, such as mirroring, can perform better on reads by selectively scheduling requests on the disk with the shortest expected seek and rotational delays [Bitten and Gray 1988].

Without redundancy, any single disk failure will result in data loss. Nonredundant disk arrays are widely used in supercomputing environments where performance and capacity, rather than reliability, are the primary concerns.

## 3.2.2 Mirrored (Raid Level 1)

The traditional solution, called mirroring or shadowing, uses twice as many disks as a nonredundant disk array [Bitten and Gray 1988]. Whenever data is written to a disk the same data is also written to a redundant disk, so that there are always two copies of the information. When data is read, it can he retrieved from the disk with the shorter queuing, seek, and rotational delays [Chen et al. 1990]. If a disk fails, the other copy is used to service requests. Mirroring is frequently used in

2Strictly speaking, RAID level O IS not a type of redundant array of inexpensive disks since it stores no error-correcting codes.

ACM Computing  Vol 26, No 2, June 1994

![8_image_0.png](8_image_0.png)

![8_image_1.png](8_image_1.png)

![8_image_2.png](8_image_2.png)

Mirrored (RAID Level 1)
Mcmo]y-S[ylc ECC (RAID LCW4 2)

![8_image_3.png](8_image_3.png)

![8_image_4.png](8_image_4.png)

![8_image_5.png](8_image_5.png)

~

![8_image_6.png](8_image_6.png)

P+Q Redundancy (RAID Level 6)
Figure 3. RAID levels O through 6. All RAID levels are illustrated at a user capacity of four disks. Disks with multiple platters indicate block-level striping while disks without multiple platters indicate bit-level striping. The shaded platters represent redundant information.
database applications where availability and transaction rate are more important than storage efficiency [Gray et al. 1990].

## 3.2.3 Memoiy-Siyle Ecc (Raid Level 2)

Memory systems have provided recovery from failed components with much less cost than mirroring by using Hamming codes [Peterson and Weldon 1972]. Hamming codes contain parity for distinct overlapping subsets of components. In one version of this scheme, four data disks require three redundant disks, one less than mirroring. Since the number of redundant disks is proportional to the log ACM Computing  Vol. 26, No. 2, June 1.994 of the total number of disks in the system, storage efficiency increases as the number of data disks increases.

If a single component fails, several of the parity components will have inconsistent values, and the failed component is the one held in common by each incorrect subset. The lost information is recovered by reading the other components in a subset, including the parity component, and setting the missing bit to O or 1 to create the proper parity value for that subset. Thus, multiple redundant disks are needed to identify the failed disk, but only one is needed to recover the lost information.

Readers unfamiliar with parity can think of the redundant disk as having the sum of all the data in the other disks.

When a disk fails, you can subtract all the data on the good disks from the parity disk; the remaining information must be the missing information. Parity is simply this sum modulo two.

## 3.2.4 Bit-Interleaved Parity (Raid Level 3)

One can improve upon memory-style EGG
disk arrays by noting that, unlike memory component failures, disk controllers can easilv identifv which disk has failed. Thus, on"e can u~e a single parity disk rather than a set of parity disks to recover lost information.

In a bit-interleaved parity disk array, data is conceptually interleaved bit-wise over the data disks, and a single parity disk is added to tolerate any single disk failure. Each read request accesses all data disks, and each write request accesses all data disks and the parity disk.

Thus, only one request can be serviced at a time. Because the parity disk contains only parity and no data, the parity disk cannot participate on reads, resulting in slightly lower read performance than for redundancy schemes that distribute the parity and data over all disks. Bit-interleaved parity disk arrays are frequently used in applications that require high bandwidth but not high 1/0 rates. Also they are simpler to implement than RAID
Levels 4, 5, and 6.

## 3.2,5 Block-Interleaved Parity (Raid Level 4)

The block-interleaved parity disk array is similar to the bit-interleaved parity disk array except that data is interleaved across disks in blocks of arbitrary size rather than in bits. The size of these blocks is called the striping unit [Chen and Patterson 1990]. Read requests smaller than the striping unit access only a single data disk. Write reauests must upda~e the requested data 'blocks and must compute and update the parity block. For large writes that touch blocks on all disks, p~rity is easily computed by exclusive-oring the new data for each disk. For small write reauests that uw date only one data disk,' parity is computed by noting how the new data differs from the old data and applying those differences to the ~aritv block. Small write requests thu~ re&ire four disk 1/0s: one to write the new data, two to read the old data and old parity for computing the new parity, and one to write the new parity. This is referred to as a read-modify-write procedure. Because a block-interleaved parity disk array has only one parity disk, which must be updated on all write operations. the ~aritv disk can easily become a bottleneck. B~-
cause of this limitation, the block-interleaved distributed-parity disk array is universally m-eferred over the block-interleaved ~a~ity disk array.

## 3.2.6 Block-Interleaved Distributed-Parly (Raid Level 5)

The block-interleaved distributed-~ aritv disk array eliminates the parity disk bo~-
tleneck present in the block-interleaved parity disk array by distributing the parity uniformly over all of the disks. An additional, frequently overlooked advantage to distributing the parity is that it also distributes data over all of the disks rather than over all but one. This allows all disks to participate in servicing read operations .in contrast to redundance .

schemes with dedicated parity disks in which the parity disk cannot participate in servicing read requests. Block-inter-

ACM Computing  Vol 26, No 2, June 1994
leaved distributed-parity disk arrays have the best small read, large read, and large write performance of any redundant disk array. Small write requests are somewhat inefficient compared with redundancy schemes such as mirroring however, due to the need to perform read-modify-write operations to update parity. This is the major performance weakness of RAID level-5 disk arrays and has been the subject of intensive research [Menon et al. 1993; Stodolsky and Gibson 1993].

The exact method used to distribute parity in block-interleaved distributedparity disk arrays can affect performance. Figure 4 illustrates the best parity distribution of those investigated in [Lee and Katz 1991b], called the leftsymmetric parity distribution. A useful property of the left-symmetric parity distribution is that whenever you traverse the striping units sequentially, you will access each disk once before accessing any disk twice. This property reduces disk conflicts when servicing large requests.

## 3.2.7 P + Q Redundancy (Raid Level 6,)

Parity is a redundancy code capable of correcting any single self-identifying failure. As larger disk arrays are considered, multiple failures are possible, and stronger codes are needed [Burkhard and Menon 1993]. Moreover, when a disk fails in a parity-protected disk array, recovering the contents of the failed disk requires a successful reading of the contents of all nonfailed disks. As we will see in Section 3.4, the probability of encountering an uncorrectable read error during recovery can be significant. Thus, applications with more stringent reliability requirements require stronger errorcorrecting codes.

One such scheme, called P + Q redundancy, uses Reed-Solomon codes to protect against up to two disk failures using the bare minimum of two redundant disks. The P + Q redundant disk arrays are structurally very similar to the blockinterleaved distributed-parity disk arrays and operate in much the same

![10_image_0.png](10_image_0.png)

(Left-SJ mmetnc)
Figure 4. RAID level-5 left-symmetric parity placement. Each square corresponds to a stripe unit. Each column of squares corresponds to a disk.

PO computes the parity over stripe units O, 1,2, and 3; PI computes parity over stripe units 4, 5, 6, and 7; etc. Lee and Katz [ 1991b] show that the left-symmetric parity distribution has the best performance. Only the minimum repeating pattern is shown.
manner. In particular, P + Q redundant disk arrays also perform small write operations using a read-modify-write procedure, except that instead of four disk accesses per write requests, P + Q redundant disk arrays require six disk accesses due to the need to update both the
"P and "Q" information.

## 3.3 Performance And Cost Comparisons

The three primary metrics in the evaluation of disk arrays are reliability, performance, and cost. RAID levels O through 6 cover a wide range of tradeoffs among these metrics. It is important to consider all three metrics to understand fully the value and cost of each disk array organization. In this section, we compare RAID
levels O through 6 based on performance and cost. The following section examines reliability y.

3.3.1 Ground Rules and Observations While there are only three primary metrics in the evaluation of disk arrays ACM Computing  Vol 26, No 2, June 1994
(reliability, performance, and cost), there are many different ways to measure each metric and an even larger number of ways of using them. For example, should performance be measured in 1/0s per second, bytes per second, or response time? Would a hybrid metric such as 1/0s per second per dollar be more appropriate? Once a metric is agreed upon, should we compare systems at the same cost, the same total user capacity, the same performance, or the same reliability? The method one uses depends largely on the purpose of the comparison and the intended use of the system. In time-sharing applications, the primary metric may be user capacity per dollar; in transactionprocessing applications the primary metric may be 1/0s per second per dollar; and in scientific applications, the primary metric may be bytes per second per dollar. In certain heterogeneous systems, such as file servers, both 1/0s per second and bytes per second may be important.

In many cases, these metrics may all be conditioned on meeting a reliability threshold.

Most large secondary storage systems, and disk arrays in particular, are throughput oriented. That is, generally we are more concerned with the aggregate throughput of the system than, for example, its response time on individual requests (as long as requests are satisfied within a specified time limit). Such a bias has a sound technical basis: as techniques such as asynchronous 1/0, prefetching, read caching, and write buffering become more widely used, fast response time depends on sustaining a high throughput.

In throughput-oriented systems, performance can potentially increase Iinearly as additional components are added; if one disk provides 30 1/0s per second, 2 should provide 60 1/0s per second. Thus, in comparing the performance of disk arrays, we will normalize the performance of the system by its cost. In other words we will use performance metrics such as 1/0s per second per dollar rather than the absolute number of 1/0s per second.

ACM Computmg  Vol. 26, No 2, June 1994
Even after the metrics are agreed upon, one must decide whether to compare systems of equivalent capacity, cost, or some other metric. We chose to compare systems of equiualen t file capacity where file capacity is the amount of information the file system can store on the device and excludes the storage used for redundancy. Comparing systems with the same file capacity makes it easy to choose equivalent workloads for two different redundancy schemes. Were we to compare systems with different file capacities, we would be confronted with tough choices such as how a workload on a system with user capacity X maps onto a system with user capacity 2X.

Finally, there is currently much confusion in comparisons of RAID levels 1 through 5. The confusion arises because a RAID level sometimes specifies not a specific implementation of a system but rather its configuration and use. For example, a RAID level-5 disk array (blockinterleaved distributed parity) with a parity group size of two is comparable to RAID level 1 (mirroring) with the exception that in a mirrored disk array, certain disk-scheduling and data layout optimizations can be performed that, generally, are not implemented for RAID
level-5 disk arrays [Hsiao and DeWitt 1990; Orji and Solworth 1993]. Analogously, a RAID level-5 disk array can be configured to operate equivalently to a RAID level-3 disk array by choosing a unit of data striping such that the smallest unit of array access always accesses a full parity stripe of data. In other words, RAID level-l and RAID level-3 disk arrays can be viewed as a subclass of RAID
level-5 disk arrays. Since RAID level-2 and RAID level-4 disk arrays are, practically speaking, in all ways inferior to RAID level-5 disk arrays, the problem of selecting among RAID levels 1 through 5 is a subset of the more general problem of choosing an appropriate parity group size and striping unit size for RAID level5 disk arrays. A parity group size close to two may indicate the use of RAID level-1 disk arrays; a striping unit much smaller than the size of an average request may

Table 3. Throughput per Dollar Relative to RAID Level 0.

| Small        | Read    | Small   | Write        | Large    | Read     | Large    | Write   | Storage   | Efficiency   |
|--------------|---------|---------|--------------|----------|----------|----------|---------|-----------|--------------|
| RAID level O | 1       | 1       | 1            | 1        | 1        |          |         |           |              |
| RAID level 1 | I 1     | 1/2     | 1            | 1/2      | 1/2      |          |         |           |              |
| RAID         | level   | 3       | l/G          | l/G      | (G- 1)/G | (G-1 )/G | (G-1)/G |           |              |
| RAID         | level   | 5       | I 1          | max(l/G, | I/4)     | 1        | (G-lj/G | (G-1)/G   |              |
| RAID         | level 6 | 1       | max(l/G,l/6) | 1        | (G-2)/G  | (G-2)/G  |         |           |              |

This table compares the throughputs of various redundancy schemes for four types of 1/0 requests. Small here refers to 1/0 requests of one striping unit; large refers to 1/0 requests of one full stripe (one stripe unit from each disk in an error correction group). G refers to the number of disks in an error correction group, In all cases, the higher the number the better. The entries in this table account for the major performance effects but not some of the second-order effects. For instance, since RAID level 1 stores two copies of the data, a common optimization is to read dynamically the disk whose positioning time to the data is smaller.
indicate the use of a RAID level-3 disk array.

## 3.3.2 Comparisons

Table 3 tabulates the maximum throughput per dollar relative to RAID level O for RAID levels O, 1, 3, 5, and 6. The cost of each system is assumed to be proportional to the total number of disks in the disk array. Thus, the table illustrates that given equivalent cost RAID level-O
and RAID level- 1 systems, the RAID
level-l system can sustain half the number of small writes per second that a RAID level-O system can sustain. Equivalently, we can say that the cost of small writes is twice as expensive in a RAID
level-l system as in a RAID level-O system. In addition to performance, the table shows the storage efficiency of each disk array organization. The storage efficiency is approximately inverse to the cost of each unit of user capacity relative to a RAID level-O system. For the above disk array organizations, the storage efficiency is equal to the performance/cost metric for large writes.

Figure 5 graphs the performance/cost metrics from Table 3 for RAID levels 1, 3, 5, and 6 over a range of parity group sizes. The performance/cost of RAID
level-l systems is equivalent to the performance/cost of RAID level-5 systems when the parity group size is equal to two. The performance/cost of RAID
level-3 systems is always less than or equal to the performance/cost of RAID
level-5 systems. This is expected given that a RAID level-3 system is a subclass of RAID level-5 systems derived by restricting the striping unit size such that all requests access exactly a parity stripe of data. Since the configuration of RAID
level-5 systems is not subject to such a restriction, the performance/cost of RAID level-5 systems can never be less than that of an equivalent RAID level-3 system. It is important to stress that these performance\cost observations apply only to the abstract models of disk arrays for which we have formulated performance/cost metrics. In reality, a specific implementation of a RAID level-3 system can have better performance/cost than a specific implementation of a RAID
level-5 system.

As previously mentioned, the question of which RAID level to use is often better expressed as more general configuration questions concerning the size of the parity group and striping unit. If a parity group size of two is indicated, then mirroring is desirable. If a very small striping unit is indicated then a RAID level-3 system may be sufficient. To aid the reader in evaluating such decisions, Figure 6 plots the four performance/cost

ACM Computing  Vol 26, No. 2, June 1994
158 . Peter M. Chen et al.

![13_image_0.png](13_image_0.png)

Figure 5. Throughput per dollar relatlve to RAID level 0, RAID level-l performance is approximately equal to RAID level-5 performance with a group size of two. Note that for small writes, RAID levels 3, 5, and 6 are equally cost effective at small group sizes, but as group size increases, RAID levels 5 and 6 become better alternatives.
metrics from Table 3 on the same graph for each of the RAID levels 3, 5, and 6.

This makes the performance/cost tradeoffs explicit in choosing an appropriate parity group size. Section 4.4 addresses how to choose the unit of striping.

## 3.4 Reliability

Reliability is as important a metric to many 1/0 systems as performance and cost, and it is perhaps the main reason for the popularity of redundant disk arrays, This section starts by reviewing the basic reliability provided by a block-interleaved parity disk array and then lists three factors that can undermine the potential reliability of disk arrays.

ACM Computing  Vol 26, No 2, June 1994

## 3.4.1 Basic Reliability

Redundancy in disk arrays is motivated by the need to overcome disk failures.

When only independent disk failures are considered, a simple parity scheme works admirably. Patterson et al. [1988] derive the mean time between failures for a RAID level 5 to be

$$M T T F(\,d i s k\,)^{2}$$
$$\overline{{N\times v}}$$

## Nx (G - 1) X Mttr(Disk) '

where MTTF( disk) is the mean-timeto-failure (MTTF) of a single disk, MTTR( disk) is the mean-time-to-repair
(MTTR) of a single disk, N is the total

RAID - 159

![14_image_0.png](14_image_0.png)

![14_image_1.png](14_image_1.png)

Figure 6. Throughput per dollar relative to RAID level O. The graphs illustrate the tradeoff in performance\cost versus group size for each specified R41D level. Note that in this comparison, mirroring (RAID
level 1) is the same as RAID level 5 with a group size of two.
number of disks in the disk array, and G
is the parity group size. For illustration purposes, let us assume we have 100 disks that each had a mean time to failure of 200,000 hours and a mean time to repair of one hour. If we organized these 100 disks into parity groups of average size 16, then the mean time to failure of the system would be an astounding 3000 years. Mean times to failure of this magnitude lower the chances of failure over any given period of time.

For a disk array with two redundant disk per parity group, such as P + Q redundancy, the mean time to failure is

$$\frac{M T T F^{3}(d i s k\,)}{N\times(G\,-\,1)\times(G\,-\,2)\times M T T R^{2}(d i s k\,)}$$

Using the same values for our reliability parameters, this implies an astronomically large mean time to failure of 38 million years.

This is an idealistic picture, but it gives us an idea of the potential reliability afforded by disk arrays. The rest of this section takes a more realistic look at the reliability of block-interleaved disk arrays by considering factors such as system crashes, uncorrectable bit-errors, and correlated disk failures that can dramatically affect the reliability of disk arrays.

3.4.2 System Crashes and Parity Inconsistency In this section, the term system crash refers to any event such as a power failure, operator error, hardware

ACM Computmg  Vol. 262 No. 2, June 1994
breakdown, or software crash that can interrupt an 1/0 operation to a disk array. Such crashes can interrupt write operations, resulting in states where the data is updated and the parity is not, or visa versa. In either case, the parity is inconsistent and cannot be used in the event of a disk failure. Techniques such as redundant hardware and power supplies can be applied to make such crashes less frequent [Menon and Cartney 1993],
but no technique can prevent systems crashes 100% of the time.

System crashes can cause parity inconsistencies in both bit-interleaved and block-interleaved disk arrays, but the problem is of practical concern only in block-interleaved disk arrays. This is because in bit-interleaved disk arrays the inconsistent parity can only affect the data that is currently being written. If writes do not have to be atomic, applications cannot assume either that the write during a system crash completed or did not complete, and thus it is generally permissible for the bit-interleaved disk array to store arbitrary data on the updated sectors. In a block-interleaved disk array, however, an interrupted write operation can affect the ~arit~ of other data blocks in that stripe ;hat ;ere not being written. Thus, for reliability purposes, svstem crashes in block-interleaved disk a&ays are similar to disk failures in that they may result in the loss of the correct parity for stripes that were being modified during the crash.

In actuality, system crashes can be much worse than disk failures for two reasons. First, they may occur more frequently than disk failures. Second, a system crash in disk arrays using P + Q
redundancy is analogous to a double disk failure because both the "P" and "Q" information is made inconsistent. To avoid the loss of parity on system crashes, information sufficient to recover the parity must be logged to nonvolatile storage before executing each write operation. The information need only be saved until the corresponding write completes. Hardware implementations of RAID systems can implement such logging efficiently using nonvolatile RAM. In software implementations that do not have access to fast nonvolatile storage, it is generally not possible to protect against system crashes without significantly sacrificing performance.

## 3.4.3 Uncorrectable Bit Errors

Although modern disks are highly reliable devices that can withstand significant amounts of abuse, they occasionally fail to read or write small bits of data. ~urrently, most disks cite uncorrectable bit error rates of one error in 10 lJ bits read. Unfortunately. ", the exact interpretation of what is meant by an uncorrectable bit error is unclear. For example, does the act of reading disks actually generate errors, or do the errors occur during writes and become evident during reads?

Generally, disk manufactures agree that reading a disk is very unlikely to cause permanent errors. Most uncorrectable errors are generated because data is incorrectly writ;en or gradually damaged as the magnetic media ages. These errors are detected only when we attempt to read the data. Our interpretation of uncorrectable bit error rates is that they rem-esent the rate at which errors are de~ected during reads from the disk during the normal operation of the disk drive.

It is important to stress that there is no generally agreed upon interpretation of bit error rates.

The primary ramification of an uncorrectable bit error is felt when a disk fails and the contents of the failed disk must be reconstructed by reading data from the nonfailed disks. For example, the re-construction of a failed disk in a 100 GB
disk array requires the successful reading of approximately 200 million sectors of information. A bit error rate of one in 1014 bits implies that one 512 byte sector in 24 billion sectors cannot be correctly read. Thus, if we assume that the probability of reading sectors is independent of each other, the probability of reading all 200 million sectors successfully is approximately (1 - 1/(2.4 X 1010)) A (2.0

ACM Computmg  Vol 26. No. 2, .June 1994
x 108) = 99.29%. This means that on average, 0.8% of disk failures would result in data loss due to an uncorrectable bit error.

The above example indicates that unrecoverable bit errors can be a significant factor in designing large, highly reliable disk arrays. This conclusion is heavily dependent on our particular interpretation of what is meant by an unrecoverable bit error and the guaranteed unrecoverable bit error rates as supplied by the disk manufactures; actual error rates may be much better.

One approach that can be used with or without redundancy is to try to protect against bit errors by predicting when a disk is about to fail. VAXsimPLUS, a product from Digital Equipment Corporation, monitors the warnings given by disks and notifies an operator when it feels the disk is about to fail. Such predictions can significantly lower incident of data loss [Emlich and Polich 1989; Malhotra and Trivedi 1993].

## 3.4.4 Correlated Disk Failures

The simplest model of reliability of disk arrays [Patterson et al. 1988] assumes that all disk failures are independent when calculating mean time to data loss.

This resulted in very high mean time to data loss estimates, up to millions of years. In reality, common environmental and manufacturing factors can cause correlated disk failures frequently. For example, an earthquake might sharply increase the failure rate for all disks in a disk array for a short period of time.

More commonly, power surges, power failures, and simply the act of powering disks on and off can place simultaneous stress on the electrical components of all affected disks. Disks also share common support hardware; when this hardware fails, it can lead to multiple, simultaneous disk failures.

Aside from environmental factors, the disks themselves have certain correlated failure modes built into them. For example, disks are generally more likely to fail either very early or very late in their lifetimes. Early failures are caused frequently by transient defects which may not have been detected during the manufacturer's burn-in process; late failures occur when a disk wears out. A systematic manufacturing defect can produce also bad batches of disks that can fail close together in time. Correlated disk failures greatly reduce the reliability of disk arrays by making it much more likely that an initial disk failure will be closely followed by additional disk failures before the failed disk can be reconstructed.

## 3.4.5 Reliability Revisited

The previous sections have described how system crashes, uncorrectable bit errors, and correlated disk failures can decrease the reliability of redundant disk arrays.

In this section, we will calculate meantime-to-data-loss statistics after incorporating these factors.

The new failure modes imply that there are now three relatively common ways to lose data in a block-interleaved parityprotected disk array:

double disk failure, e
●

system crash followed by a disk failure, and disk failure followed bv an uncorrectable bit error during reconstruction.

●

As mentioned above, a system crash followed by a disk failure can be protected against in most hardware disk array implementations with the help of nonvolatile storage, but such protection is unlikely in software disk arrays. The above three failure modes are the hardest failure combinations, in that we are currently unaware of any techniques to protect against them without significantly degrading performance. To construct a simple model of correlated disk failures, we will assume that each successive disk failure is 10 times more likely than the previous failure (until the failed disk has been reconstructed).

Table 4 tabulates values of the reliability

ACM Computing  Vol 26, No. 2, June 1994
Table 4. Reliablilty Parameters

| Total User CapacNy                                                                                                                                        | 100 dtsks (500 GB)                                                 |
|-----------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------|
| Disk Size                                                                                                                                                 | 5 GB                                                               |
| Sector Size                                                                                                                                               | 512 byms                                                           |
| Bit Error RaIc (BER)                                                                                                                                      | 1 in 10A14 b{~ 1 m 2.4 IOAIO scclors 99.96% 16 disks 200,000 hours |
| p(dl\k) The probability                                                                                                                                   | of reading                                                         |
| all sectors on a disk (Dcnved from disk SIX, sector si~e, and BER.) Parily Group SIZC MTTF(disk) M'ITF(disk2) MlTF(dtsk3) MITR(disk) M'ITF(sys) MITR(sys) | 20,000 hours 2,(XKI hours 1 hour 1 month 1 hour                    |

This table lists parameters used for reliabdity calculations m this section.

parameters we will use for calculating numeric reliability estimates in this section. Note that the reliability estimates will be given per a constant user capacity of 100 disks, consisting of independent, 16-disk parity groups.

Table 5, which tabulates reliability metrics for RAID level-5 disk arrays, shows that the frequency of the three failure combinations are within an order of magnitude of each other. This means that none of the three failure modes can be ignored in determining reliability. This makes it difficult to improve the overall reliability of the system without improving the reliability y of several components of the system; a more reliable disk will greatly reduce the frequency of double disk failures, but its protection against the other two failure combinations is less pronounced. Frequencies of both system crashes and bit error rates also must be reduced before significant improvements in overall system reliability can be achieved. Also, note the deceptively reassuring MTTDL numbers. Even with a ACM Computmg  Vol. 26, No 2, June 1994 MTTDL of 285 years, there is a 3.4% chance of losing data in the first 10 years.

Table 6 tabulates the reliability metrics for P + Q redundant disk arrays.

As can be seen, system crashes are the Achilles's heel of P + Q redundancy schemes. Since system crashes invalidate both the P and Q information, their effect is similar to a double disk failure. Thus, unless the system provides protection against system crashes, as is assumed in the calculation of the reliability for hardware RAID systems, P + Q redundancy does not provide a significant advantage over parity-protected disk arrays. In general, P + Q redundancy is most useful for protecting against unrecoverable bit errors that occur during reconstruction and against multiple correlated disk failures.

## 3.4.6 Summary And Conclusions

This section has examined the reliability of block-interleaved redundant disk arrays when factors other than independent disk failures are taken into account.

We see that system crashes and unrecoverable bit errors can significantly reduce the reliability of block-interleaved parityprotected disk arrays. We have shown that P + Q redundant disk arrays are very effective in protecting against both double disk failures and unrecoverable bit errors but are susceptible to system crashes. In order to realize the full reliability advantages of P + Q redundant disk arrays, nonvolatile storage must be used to protect against system crashes.

Numeric reliability calculations serve as useful guidelines and bounds for the actual reliability of disk arravs. How- .

ever, it is infeasible to compare the re-liability of real system based on such numbers. Frequently, reliability calculations ignore important implementationspecific factors that are difficult to quantify, such as the reliability of software components. What is useful to know, however, and what we have presented here, are the types of common failures that a disk array can tolerate, how they limit the reliability of the system, and

| Table 5.                 | Failure Characteristics   | for RAID Level-5 Disk Arrays.   | Probability   | of        |          |         |      |                |                          |
|--------------------------|---------------------------|---------------------------------|---------------|-----------|----------|---------|------|----------------|--------------------------|
| MTTDL                    | NITTDL                    | Data Loss over 10 Year Period   |               |           |          |         |      |                |                          |
| Double Disk Failure      | MTTF                      | (disk)                          | x MTTF        | (disk2)   | 285 yrs. | 3.4%    |      |                |                          |
| Nx                       | (G-                       | 1) xh4TTR(disk)                 |               |           |          |         |      |                |                          |
| Sys Crash + Disk Failure | MTTF (sys) x MTTF         | (disk)                          | 154 yrs.      | 6.3%      |          |         |      |                |                          |
| N X kf~~/?               | ( SYS)                    |                                 |               |           |          |         |      |                |                          |
| Disk Failure + Bit Error | IWTF                      | (disk)                          | 36 yrs.       | 24 .4%    |          |         |      |                |                          |
| Nx                       | (1-                       | (p(disk))G-')                   |               |           |          |         |      |                |                          |
| #                        |                           |                                 |               |           |          |         |      |                |                          |
| Software RAID            | (harmonic                 | sum of above)                   | 26 yrs.       | 31.6%     |          |         |      |                |                          |
| Hardware RAID            | (NVRAM)                   | ::-:;::                         | ;:;;::g       | 32 yrs.   | 26.8%    |         |      |                |                          |
| MTTDL                    | is the mean               | time                            | to data       | loss. The | 10-year  | failure | rate | is the percent | chance of data loss in a |

|                                     | Table 6.                         | Failure Characteristics   | for a P + Q disk array.      | Probability of Data   |               |         |      |                |                |           |
|-------------------------------------|----------------------------------|---------------------------|------------------------------|-----------------------|---------------|---------|------|----------------|----------------|-----------|
|                                     | MTfDL                            | MTTDL                     | Loss over 10 Year Period     |                       |               |         |      |                |                |           |
| Triple Disk Failure                 | MT7F                             | (disk)                    | X MT77F (d1sk2) X MTTF(disk3 | ) )                   | 38052 yrs.    | 0.03%   |      |                |                |           |
|                                     | Nx                               | (G - 1) x (G -2)          | xMTTR2(disk)                 |                       |               |         |      |                |                |           |
| Sys Crash+ Disk Failure             | MTTF                             | (SYS)                     | X MTTF (duk)                 |                       |               |         |      |                |                |           |
|                                     | N X M7TR (S]S)                   | 144 yrs.                  | 7.7%                         |                       |               |         |      |                |                |           |
| Double Disk Failure + Bit Error     | M'f'TF (disk) x IUTTF (disk2 ) ) |                           |                              |                       |               |         |      |                |                |           |
|                                     | Nx(G-l)                          | x(l-(l-p                  | (disk)))                     | '6-2))                | x MTTR (disk) | 47697   | yrs. | 0.029??        |                |           |
|                                     | (harmonic sum of above)          | 143 yrs.                  | 6.8%                         |                       |               |         |      |                |                |           |
| software RAID Hardware RAID (NVRAM) | (harmonic sum excluding          | sys crmh+disk failure)    | 21166 yrs.                   | 0.05%                 |               |         |      |                |                |           |
| MTTDL                               | is the mean                      | time                      | to data                      | loss. The             | 10-year       | failure | rate | is the percent | chance of data | loss in a |

MTTDL is the mean time to data loss. The 10-year failure rate is the percent chance of data loss in a 10-year period, For numeric calculations, the parity group size, G, is equal to 16, and the user data capacity is equal to 100 data disks. Note that the total number of disks in the system, N, is equal to the number of data disks times G/(G - 1).

MTTDL is the mean time to data loss. The 10-year failure rate is the percent chance of data loss in a 10-year period. For numeric calculations, the parity group size, G, is equal to 16, and the user data capacity is equal to 100 data disks. Note that the total number of disks in the system, N, is equal to the number of data disks times G/(G - 2).

ACM Computmg  Vol. 26, No. 2, June 1994 thus its approximate reliability in comparison to other disk array organizations of similar complexity.

## 3.5 Implementation Considerations

Although the operation of block-interleaved redundant disk arrays is conceptually simple, a disk array implementer must address many practical considerations for the system to function correctly and reliably at an acceptable level of performance. One problem is that the necessary state information for a disk array consists of more than just the data and parity stored on the disks. Information such as which disks are failed, how much of a failed disk has been reconstructed, and which sectors are currently being updated must be accurately maintained in the face of system crashes. We will refer to such state information that is neither user data nor parity as metastate information. Another problem, addressed in Section 3.5.4, is that multiple disks are usually connected to the host computer via a common bus or string.

## 3.5.1 Avoiding Stale Data

The only piece of metastate information that must be maintained in redundant disk arrays is the validity of each sector of data and parity in a disk array. The following restrictions must be observed in maintaining this information.

When a disk fails, the logical sectors corresponding to the failed disk must be marked invalid before any request that would normally access to the failed disk can be attempted. This invalid mark prevents users from reading corrupted data on the failed disk.

When an invalid logical sector is reconstructed to a spa~e disk, the logical sector must be marked ualid before any write request that would normally write to the failed disk can be serviced.

This ensures that ensuing writes update the reconstructed data on the spare disk.

0

*

ACM Computmg  Vol. 26, No, 2, June 1994 Both restrictions are needed to ensure that users do not receive stale data from the disk array. Without the first restriction, it would be possible for users to read stale data from a disk that is considered to have failed but works intermittently. Without the second restriction, successive write operations would fail to update the newly reconstructed sector, resulting in stale data. The valid/
invalid state information can be maintained as a bit-vector either on a separate device or by reserving a small amount of storage on the disks currently configured into the disk array. If one keeps track of which disks are failed/operational, one needs only to keep a bitvector for the failed disks. Generally, it is more convenient to maintain the valid/invalid state information on a per striping unit rather than a per sector basis since most implementations will tend to reconstruct an entire striping unit of data at a time rather than a single sector. Because disk failures are relatively rare events and large groups of striping units can be invalidated at a time, updating the valid/invalid metastate information to stable storage does not present a significant performance overhead.

3.5.2 Regenerating Parity after a System Crash System crashes can result in inconsistent parity by interrupting write operations. Thus, unless it is known which parity sectors were being updated, all parity sectors must be regenerated when ever a disk array comes up from a system crash.

This is an expensive operation that requires scanning the contents of the entire disk array. To avoid this overhead, information concerning the consistent\ inconsistent state of each parity sector must be logged to stable storage. The following restriction must be observed.

Before servicing any write request, the corresponding parity sectors must be marked inconsistent.

When bringing a system up from a system crash, all inconsistent parity sectors must be regenerated.

Note that because regenerating a consistent parity sector does no harm, it is not absolutely necessary to mark a parity sector as consistent. To avoid having to regenerate a large number of parity sectors after each crash, however, it is clearly desirable to mark parity sectors periodically, as consistent.

Unlike updating valid/invalid information, the updating of consistent/inconsistent slate information is a potential performance problem in software RAID systems, which usually do not have access to fast. nonvolatile storage. A simplistic implementation would ~equire a disk write to mark a parity sector as inconsistent before each write operation and a corresponding disk write to mark the parity sector as consistent after each write operation. A more palatable solution is to maintain a most recently used pool that keeps track of a fixed number of inconsistent parity sectors on stable storage. By keeping a copy of the pool in main memory, one can avoid accessing stable storage to mark parity sectors that are already marked as inconsistent. By varying the size of the pool, one can tradeoff the hit rate of the pool against the amount of parity information that needs to be regenerated when recovering from a system crash.

The above method should work efficiently for requests that exhibit good locality of reference. If the disk array must service a large number of random write requests, as in transaction-processing environments, we recommend incorporating a group commit mechanism s: that a large number of parity sectors can be marked inconsistent with a sinde access to stable storage. This so~ves the throughput problem but results in higher latencies for random write reauests since the parity sectors must be ma~ked inconsistent before the writes can proceed.

## 3.5.3 Operating With A Failed Disk

A system crash in a block-interleaved redundant disk array is similar to a disk failure in that it can result in the loss of parity information. This means that a disk array operating with a failed disk can potentially lose data in the event of a system crash. Because system crashes are simificantlv more common in most svstevms than ~isk failures, operating wit~ a failed disk can be risky.

While operating with a failed disk, a user must perform some form of logging on every write operation to prevent the loss of information in the event of a system crash. We describe two elegant methods to perform this logging. The first method. called demand reconstruction. is the easiest and most efficient but ~equires stand-by spare disks. With demand reconstruction, accesses to a parity stripe with an invalid sector trigger reconstruction of the appropriate data immediately onto a spare disk. Write operations. thus. never deal with invalid sectors created by disk failures. A background process scans the entire disk array to ensure that all the contents of the failed disk are eventually reconstructed within an acceptable tim~ period.

The second method, called parity sparing [Chandy and Reddy 1993], can be applied to systems without stand-by spares but requires additional metastate information. Before servicirw a write request that would access a ~arity stripe with an invalid sector, the invalid sector is reconstructed and relocated to overwrite its corresponding parity sector.

Then the sector is marked as relocated.

Since the corresponding parity stripe no longer has parity, a system crash can only affect the data being written. When the failed disk is eventually replaced, (1) the relocated sector is copied to the spare disk, (2) the parity is regenerated, and
(3) the sector is no longer marked as relocated.

## 3.5.4 Orthogonal Raid

TO this point, we have ignored the issue of how to connect disks to the host computer. In fact, how one does this can drastically affect performance and reliability. Most computers connect multiple disks via some smaller number of strings.

Thus, a string failure causes multiple,

ACM Computing  Vol. 26, No 2, June 1994

![21_image_0.png](21_image_0.png)

Figure 7. Orthogonal RAID. This figure presents two options of how to orgamze error correction groups in the presence of shared resources, such as a string controller, Option 1 groups four disks on the same string into an error correction group; Option 2 groups one disk from each string into a group. Option 2 is preferred over Option 1 because the failure of a string controller will only render one disk from each group inaccessible.
simultaneous disk failures. If not properly designed, these multiple failures can cause data to become inaccessible.

For example, consider the 16-disk array in Figure 7 and two options of how to organize multiple, error correction groups. Option 1 combines each string of four disks into a single error correction group. Option 2 combines one disk on each string into a single error correction group. Unfortunately for Option 1, if a string fails, all four disks of an error correction group are inaccessible. On the other hand, Option 2 loses one disk from each of the four error correction groups and still allows access to all data. This technique of organizing error correction groups orthogonally to common hardware (such as a string) is called orthogonal RAID [Schulze et al. 1989; Ng 1994].

Orthogonal RAID has the added benefit of minimizing string conflicts when multiple disks from a group transfer data simultaneously.

## 4. Advanced Topics

This section discusses advanced topics in the design of redundant disk arrays. Many of the techniques are independent of each other, allowing designers to mix and match techniques.

## 4.1 Improving Small Write Performance For Raid Level 5

The major performance problem with RAID level-5 disk arrays is the high overhead for small writes. As described in Section 3.2, each small write generates four separate disk 1/0s, two to read the old data and old parity and two to write the new data and new parity. This increases the response time of writes by approximately a factor of two and decreases throughput by approximately a factor of four. In contrast, mirrored disk arrays, which generate only two disk 1/0s per small write, experience very little increase in response time and only a factor-of-two decrease in throughput. These performance penalties of RAID
level 5 relative to nonredundant and mirrored disk arrays are prohibitive in applications such as transaction processing that generate many small writes.

This section describes three techniques for improving the performance of small writes in RAID level-5 disk arrays: buffering and caching, floating parity, and parity logging.

## 4.1.1 Buffering And Caching

Buffering and caching, two optimizations commonly used in 1/0 systems, can be particularly effective in disk arrays.

This section describes how these optimization can work to minimize the performance degradations of small writes in a RAID level 5.

Write buffering, also called asynchronous writes, acknowledges a user's write before the write goes to disk. This technique reduces the response time seen by the user under low and moderate load.

Since the response time no longer depends on the disk system, RAID level 5 can deliver the same response time as ACM Computing Surveys. Vol 26, No 2, June 1994 any other disk system. If system crashes are a significant problem, nonvolatile memory is necessary to prevent loss of data that are buffered but not yet committed. This technique may also improve throughput in two ways: (1) by giving future updates the opportunity to overwrite previous updates, thus eliminating the need to write the first update [Menon and Cortney 1993], and (2) by lengthening the queue of requests seen by a disk scheduler and allowing more efficient scheduling [Seltzer et al 19901.

Barring these overwrites, however, this technique does nothing to improve throughput. So under high load, the write buffer space will fill more quickly than it empties, and response time of a RAID
level 5 will still be four times worse than a RAID level O.

An extension of write buffering is to group sequential writes together. This technique can make writes to all types of disk systems faster, but it has a particular appeal to RAID level-5 disk arrays.

By writing larger units, small writes can be turned into full stripe writes, thus eliminating altogether the Achilles heel of RAID level-5 workloads [Rosenblum and Ousterhout 1991; Menon and Courtney 1993].

Read caching is normally used in disk systems to improve the response time and throughput when reading data. In a RAID level-5 disk array, however, it can serve a secondary pm-pose. If the old data required for computing the new parity is in the cache, read caching reduces the number of disk accesses required for small writes from four to three. This is very likely, for example, in transactionprocessing systems where records are frequently updated by reading the old value, changing it, and writing back the new value to the same location.

Also, by caching recently written parity, the read of the old parity can sometimes be eliminated, further reducing the number of disk accesses for small writes from three to two. Because parity is computed over many logically consecutive disk sectors, the caching of parity exploits both temporal and spatial locality. This is in contrast to the caching of data which, for the purposes of reducing disk operations on small writes, relies on the assumption that recently read sectors are likely to be written rather than on the principle of spatial locality. Of course, caching parity blocks reduces the space available for caching data, which may increase the number of data misses.

## 4.1.2 Floating Parity

Menon et al. [1993] proposed a variation on the organization of parity in RAID level-5 disk array, called floating parity, that shortens the read-modify-write of parity updated by small, random writes to little more than a single disk access time on average. Floating parity clusters parity into cylinders, each containing a track of free blocks. Whenever a parity block needs to be updated, the new parity block can be written on the rotationally nearest unallocated block following the old parity block. Menon et al. show that for disks with 16 tracks per cylinder, the nearest unallocated block immediately follows the parity block being read 65% of the time, and the average number of blocks that must be skipped to get to the nearest unallocated block is small, between 0.7 and 0.8. Thus, the writing of the new parity block can usually occur immediately after the old parity block is read, making the entire read-modifywrite access only about a millisecond longer than a read access.

To implement floating parity efficiently, directories for the locations of unallocated blocks and parity blocks must be stored in primary memory. These tables are about 1 MB in size for each disk array containing four to ten 500 MB
disks. To exploit unallocated blocks immediately following the parity data being read, the data must be modified and a disk head switched to the track containing the unallocated block before the disk rotates though an interjector gap. Because of these constraints, and because only a disk controller can have exact knowledge of its geometry, floating parity is most likely to be implemented in the disk controller.

ACM Computing  Vol. 26, No. 2, June 1994 Menon et al. [1993] also propose floating data as well as parity. This makes the overhead for small writes in RAID
level-5 disk arrays comparable to mirroring. The main disadvantage of floating data is that logically sequential data may end up discontinuous on disk. Also, floating data requires much more free disk space than floating only the parity since there are many more data blocks than parity blocks.

## 4.1.3 Parity Logging

Stodolsky and Gibson [ 1993] propose an approach, called parity logging, to reduce the penalty of small writes in RAID
level-5 disk arravs ~Bhide and Dias 19921.

Parity logging ~educes the overhead fo~
small writes by delaying the read of the old parity and the write of the new parity. Instead of updating the parity immediately, an update image, which is the difference between the old and new parity, is temporarily written to a log. Delaying the update allows the parity to be grouped together in large contiguous blocks that can be updated more efficiently.

This delay takes place in two parts.

First, the parity update image is stored temporarily in nonvolatile memory. When this memory, which could be a few tens of KB, fills up, the parity update image is written to a log region on disk. When the log fills up, the parity update image is read into memory and added to the old parity. The resulting new parity is then written to disk. Although this scheme transfers more data to and from disk, the transfers are in much larger units and are hence more efficient; large sequential disk accesses are an order of magnitude more efficient than small random accesses (Section 2.1). Parity logging reduces the small write overhead from four disk accesses to a little more than two disk accesses, the same overhead incurred by mirrored disk arrays. The costs of parity logging are the memory used for temporarily storing update images, the extra disk space used for the log of update images, and the additional memory

ACM C!omputmg  Vol 26, No 2, June 1994
used when applying the parity update image to the old parity. This technique can be applied also to the second copy of data in mirrored disk arrays to reduce the cost of writes in mirrored disk arrays from two to a little more than one di~k access [Orji and Solworth 1993].

## 4.2 Declustered Parity

Many applications, notably database and transaction processing, require both high throughput and high data availability from their storage systems. The most demanding of these applications requires continuous operation—the ability to satisfy requests for data in the presence of disk failures while simultaneously recon- .

strutting the contents of failed disks onto replacement disks. It is unacceptable to fulfill this requirement with arbitrarily degraded performance, especially in longlived real-time applications such as video service; customers are unlikely to tolerate movies played at a slower speed or having their viewing terminated prematurely.

Unfortunately, disk failures cause large performance degradations in standard RAID Ievel-5 disk arrays. In the worst case, a workload consisting entirelv of small reads will double the effec- .

tive load at nonfailed disks due to extra disk accesses needed to reconstruct data for reads to the failed disk. The additional disk accesses needed for complete reconstruction of the failed disk increase the load even further.

In storageu.

svstems that stri~e. data across several RAIDs, the average increase in load is significantly less than in RAIDs with one large parity group, but the RAID with the failed disk still experiences a 100% increase in load in the worst case. The failed RAID creates a hot spot that degrades the performance of the entire system. The basic problem in these large systems is that although inter-RAID striping distributes load uniformly when no disk is failed, it nonuniformly distributes the increased load that results from a failed disk; the small set of disks in the same parity group as the

g3g] g5

![24_image_0.png](24_image_0.png)

o
Figure 8. Standard versus declustered-parity RAID. This figure illustrates examples of standard and declustered-parity RAID with eight disks and a parity group size of four, Identically labeled blocks belong to the same parity group. In the standard RAID organization parity groups are composed of disks from one of two nonoverlapping subsets of disks. In the declustered-parity RAID, parity groups span many overlapping subsets of disks.
failed disk bear the entire weight of the increased load. The declustered-parity RAID organization solves this problem by distributing the increased load uniformly over all disks [Muntz and Lui 1990; Merchant and Yu 1992; Holland and Gibson 1992; Holland et al. 1993; Ng and Mattson 1992].

Figure 8 illustrates examples of standard and declustered-parity RAIDs for systems with an array size of eight disks and a parity group size of four. In this case, a multiple-RAID system is constructed by striping data over two RAIDs of four disks each with non-overlapping parity groups. The declustered-parity RAID is constructed by overlapping parity groups. If Disk 2 fails, each read to Disk 2 in the standard, multiple RAID
generates a single disk access to Disks O,
1, and 3 and no disk access to Disks 4, 5, 6, and 7. In the declustered-parity RAID, a random read to Disk 2 generates an access to Disks 4, 5, and 7 one-quarter of the time; to Disks O, 1, and 3 half of the time; and to disk 6 three-quarters of the time. Although the increased load is not uniform, it is more balanced than in the standard RAID. Slightly more complex declustered-parity RAIDs exist that distribute the load uniformly such that each read to disk 2 generates an average of 0.429 disk accesses to all nonfailed disks.

The simplest way to create a declustered-parity RAID that distributes load uniformly is to create a set of parity groups including every possible mapping of parity group members to disks. In our
[1 8 example, this would result in 4= 70 distinct mappings of parity groups to disks. For nearly all practical array and parity group sizes, declustered-parity RAID organizations are possible that distribute reconstruction load uniformly with much fewer than the combinatorial number of parity groups. Such organizations can be devised using the theory of

ACM Computing  Vol. 26, No 2, June 1994
balanced incomplete block designs [Hall 1986]. In practice, the load does not need to be absolutely balanced, and a close approximation is sufficient.

To summarize, often a declustered-parity RAID is preferable to a standard, multiple RAID because it distributes load uniformly during both the normal and failed modes of operation. This allows a more graceful degradation in performance when a disk fails and allows the failed disk to be reconstructed more quickly since all disks in the disk array can participate in its reconstruction. Additionally, unlike the example in Figure 8, the disk array size in a declusteredparity RAID does not have to be a multiple of the parity group size. Any combination of array and parity group sizes such that the array size is greater than the parity group size is feasible. Declustered-parity RAID has two main disadvantages. First, it can be somewhat less reliable than standard, multiple RAID;
any two disk failures will result in data loss since each pair of disks has a parity group in common. In a standard, multiple RAID, the parity groups are disjoint, so it is possible to have more than one disk failure without losing data as long as each failure is in a different parity group. Second, the more complex parity groups could disrupt the sequential placement of data across the disks. Thus, large requests are more likely to encounter disk contention in declusteredparity RAID than in standard multiple RAID. In practice, it is difficult to construct workloads where this effect is significant.

## 4.3 Exploiting On-Line Spare Disks

On-line spare disks allow reconstruction of failed disks to start immediately, reducing the window of vulnerability during which an additional disk failure would result in data loss. Unfortunately, they are idle most of time and do not contribute to the normal operation of the system. This section describes two techniques, distributed sparing and parity sparing, that exploit on-line spare disks ACM Computmg  Vol 26, No 2, June 1994

Figure 9. Distributed sparing. Distributed sparing

![25_image_0.png](25_image_0.png)

distributes the capacity of the spare disk throughput the array. This allows all disks, including the disk that would otherwise have been a dedicated spare, to service requests. This figure illustrates a RAID level-5 disk array with distributed sparing.

The 'Ps denote parity blocks, and 'S's denote spare blocks,
to enhance performance during the normal operation of the system.

As Figure 9 illustrates, distributed sparing distributes the capacity of a spare disk across all the disks in the disk array [Menon et al. 1991]. The distribution of spare capacity is similar to the distribution of parity in RAID level-5 disk arrays. Instead of N data and one spare disk, distributed sparing uses N + 1 data disks that each have l\(lV + l)th spare capacity. When a disk fails, the blocks on the failed disk are reconstructed onto the corresponding spare blocks. Distributed sparing obviates dedicated spare disks, allowing all disks to participate in servicing requests, and thereby improving performance during the normal operation of the disk array. Additionally, because each disk is partially empty, each disk failure requires less work to reconstruct the contents of the failed disk. Distributed sparing has a few disadvantages. First, the reconstructed data must eventually be copied onto a permanent replacement for the failed disk. This creates extra work for the disk array, but, since the copying can be done leisurely, it does not significantly affect performance. Second, because the reconstructed data is distributed across many disk whereas it was formerly on a single disk, reconstruction disturbs the original data placement, which can be a concern for some 1/0 intensive applications. In disk arrays with dedicated spares, the data placement after reconstruction is identical to the data placement before reconstruction.

Figure 10. Parity sparing. Parity sparing is similar to distributed sparing except that the spare

![26_image_0.png](26_image_0.png)

space is used to store a second set of parity information.
Parity sparing is similar to distributed sparing, except that it uses the spare capacity to store parity information
[Chandy and Reddy 1993]. As with distributed sparing, this eliminates dedicated spare disks, improving performance during normal operation. The second set of parity blocks can be used in a variety of ways. First, they can be used to partition the disk array logically into two separate disk arrays, resulting in higher reliability. In Figure 10, for example, POa might compute the parity over blocks 1 and 2 while POb computes the parity over blocks 3 and 4. Second, the additional parity blocks can be used to augment the original parity groups. In Figure 10, if one assumes that the parity of blocks 1, 2, 3, 4, POa, and POb is always zero, write operations need to update only one of POa or POb. This has the benefit of improving small write performance by allowing each small write to choose the parity block it will update based on information such as the queue length and disk arm position at the two alternative disks. Third, the extra parity blocks can be used to implement P + Q
redundancy. When a disk fails, the disk array converts to simple parity. By logical extension, a second disk failure would result in a RAID level-O disk array.

Both distributed sparing and parity sparing offer interesting ways to exploit on-line spares for improved performance. 'They are most effective for disk arrays with a small number of disks where the fraction of spare disks to nonspare disks is likely to be large. As disk arrays become larger, a smaller fraction of spare disks is needed to achieve the same level of reliability [Gibson 1991].

## 4.4 Data Striping In Disk Arrays

Distributing data across the disk array speeds up 1/0s by allowing a single 1/0 to transfer data in parallel from multiple disks or by allowing multiple 1/0s to occur in parallel. The disk array designer must keep in mind several tradeoffs when deciding how to distribute data over the disks in the disk array to maximize performance, balancing two conflicting goals:

Maximize the amount of useful data that each disk transfers with each logical 1/0. Typically, a disk must spend some time seeking and rotating between each logical 1/0 that it services. This positioning time represents wasted work—no data is transferred during this time. Hence it is beneficial to maximize the amount of useful work done in between these positioning times. Utilize all disks. Idle times are similar to positioning times in that during idle times, no useful work is done. Idle times can arise in two different situations.

First, hot spots can exist, where certain disks (the hot disks) are more heavily used than other disks (the cold disks)
[Friedman 1993; Wilmot 1989]. Second, it is possible that all disks could be used evenly when viewed over a long period of time but not evenly at every instant. For example, if there is only one request to the disk array and that request only uses one disk, then all other disks will remain idle.
These goals are in conflict because the schemes that guarantee use of all disks spread data widely among more disks and hence cause each disk to transfer less data per logical 1/0. On the other hand, schemes that maximize the amount of data transferred per logical 1/0 may leave some disks idle. Finding the right balance between these two goals is the main tradeoff in deciding how to distribute data among multiple disks and is heavily workload dependent.

Data striping, or interleaving, is the most common way to distribute data among multiple disks. In this scheme,

ACM Computing  Vol. 26, No. 2, June 1994
logically contiguous pieces of data are stored on each disk in turn. We refer to the size of each piece of data as the striping unit. The main design parameter in data striping is the size of this striping unit. Smaller striping units cause logical data to be spread over more disks; larger striping units cause logical data to be grouped, or clustered, together on fewer disks. Consequently, the size of the striping unit determines how many disks each logical 1/0 uses.

Because the interaction between workload and striping unit can have a substantial effect on the ~erformance of a disk array with block-interleaved striping, Chen and Patterson [1990] developed rules of thumb for selecting a striping unit. Their simulation-based model evaluated a spindle-synchronized disk array of 16 disks. The stochastic workload applied to the disk array had two main parameters: average request size (varied from 4–1500 KB). and the number of concurrent, independent logical requests (varied from 1–20). Their goal was to find the size of a striping unit that gave the largest throughput for an incompletely specified workload. They found that the most important workload parameter was concurrency. When the concurrency of the workload was known, a simple formula specified a striping unit that provided S)570 of the maximum throughput possible for any particular request distribution:
1 sector + 1/4* average positioning time
* data transfer rate
* (concurrency - 1)
where the average positioning time is the disk's average seek time for the workload plus an average rotational delay. A striping unit selected by this expression is small when the concurrency is low so that every access can utilize all disks, and larger when the concurrency is high so that more different accesses can be serviced in parallel. Intuitively, the product of average positioning time and data transfer rate balances the benefits and

ACM Computing Surveys. V()] 26, No 2, June 1994
the costs of striping data. The benefit of striping is the decreased transfer time of a single request, which saves approximately the transfer time of a stripe unit.

The cost of striping is the increased disk utilization that arises from an additional disk positioning itself to access the data. The constant, 1/4, is sensitive to the number of disks in the array [Chen and Lee 1993].

If nothing is known about a workload's concurrency, Chen and Patterson [19901 found that a good compromise size for a striping unit is

## 2/3 * Average Positioning Time * Data Transfer Rate.

The constant, 2/3, is sensitive to the number of disks in the array; research needs to be done quantifying this relationship.

Lee and Katz [199 la] use an analytic model of nonredundant disk arrays to derive an equation for the optimal size of data striping. The disk array system they model is similar to that used by Chen and Patterson [ 1990] described above.

They show that the optimal size of data striping is equal to

![27_image_0.png](27_image_0.png)

 $$\frac{{{P}{X}{\left({L}\,-\,{1}\right)}{Z}}}{{N}}$$
where P is the average disk positioning time, X the average disk transfer rate, L the concurrency, Z the request size, and N the array size in disks. Their results agree closely with those of Chen and Patterson. In particular, note that their equation predicts also that the optimal size of data striping is dependent only the relative rates at which a disk positions and transfers data, PX, rather than P or X individually. Lee and Katz show that the optimal striping unit depends on request size; Chen and Patterson show that this dependency can be ignored without significantly affecting performance.

Chen and Lee [1993] conducted a follow-up study to Chen and Patterson
[1990] to determine the striping unit for RAID level-5 disk arrays. Reads in a RAID level-5 are similar to reads (and writes) in a RAID level O, causing the optimal striping unit for a read-intensive workload in a RAID level-5 to be identical to the optimal striping unit in a RAID
level O. For write-intensive workloads, however, the overhead of maintaining parity causes full-stripe writes (writes that span the entire parity group) to be more efficient than read-modify writes or reconstruct writes (writes that do not span an entire parity group). This additional factor causes the optimal striping unit for RAID level-5 to be smaller for write-intensive workloads than the striping unit for RAID level O by a factor of 4 for a 16-disk array. They explored also the relationship between the optimal striping unit and the number of disks and found that the optimal striping unit for reads varies inversely to the number of disks, but that the optimal striping unit for writes varies with the number of disks. Overall, they found that the optimal striping unit for workloads with an unspecified mix of reads and writes was independent of the number of disks and recommended (in the absence of specific workload information) that the striping unit for RAID level-5 disk arrays with any number of disks be set to

## 1/2 * Average Positioning Time * Data Transfer Rate.

Currently, researchers are investigating ways to distribute data other than a simple round-robin scheme. Some variations are: choosing a different striping unit for each file and distributing data by hashing or heat-balancing [Weikum and Zabback 1992; Scheuermann et al. 1991; Copeland et al. 1988].

That is, a disk array request consists of multiple-component disk requests that must be queued and serviced independently, then joined together to satisfy the disk array request. Currently, exact solutions exist for certain two-server fork-join queues; however, the general k-server fork-join queue is an open research problem. Additionally, the bursty nature of most real 1/0 workloads is difficult to model using existing performance models, which generally deal only with the steady-state behavior of the system.

Thus, most performance models of blockinterleaved disk arrays place heavy restrictions on the configuration of the disk array or the types of workloads that can be modeled. So far, a satisfactory performance model for RAID level-5 disk arrays that models both reads and writes over a wide range of system and workload parameters has yet to be formulated.

Kim [1986] derives response time equations for synchronous byteinterleaved disk arrays by treating the entire disk array as an M/G/1 queuing system. That is, the entire disk array is modeled as an open queuing system with an exponential interarrival distribution, general service time distribution, and a single server consisting of all the disks in the disk array. The study compares the performance of an n-disk synchronous byte-interleaved disk array with n independent disks with uniform load and n independent disks with skewed load. She concludes that byte interleaving results in reduced transfer time due to increased parallelism in servicing requests and better load balancing but dramatically reduces the number of requests that can be serviced concurrently.

Kim and Tantawi [1991] derive 4.5 Performance and Reliability Modeling approximate service time equations for asynchronous (disks rotate inde~enThis section presents a brief summary of dehtly of one another) byte-interle~ved work that has been done in modeling the disk arrays. Disk seeks are assumed performance and reliability of disk ar- to be distributed exponentially, and rotarays. General performance models for tional latencies are assumed to be disblock-interleaved disk arrays are very tributed uniformly. The results of the andifficult to formulate due to the presence alytic equations are compared with the of queuing and fork-join synchronization. results of both synthetic and trace-driven

ACM Computmg  Vol. 26, No. 2, June 1994
simulations. An important conclusion of the paper is that for a wide range of seek time distributions, the sum of the seek and rotational latency can be approximated by a normal distribution.

Chen and Towsley [ 1991] model RAID
level-l and RAID level-5 disk arrays analytically for the purpose of comparing their performance under workloads consisting of very small and large requests.

Bounds are used for approximate modeling of the queuing and fork-join synchronization in RAID level-l disk arrays.

Small write requests in RAID level-5 disk arrays are handled by ignoring the forkjoin synchronization overhead, resulting in a somewhat optimistic model. Large requests are modeled by using a single queue for all the disks in the disk array.

The results of the model are compared against simulation.

Lee and Katz [1991a; 1993] derive approximate throughput and response time equations for block-interleaved disk arrays. Their model is the first analytic performance model for general block-interleaved disk arrays that takes into account both queuing and fork-join synchronization. Previous models have ignored either the queuing or fork-join synchronization component of the system.

Lee and Katz [199 la] provide also a simple application of the analytic model to determine an equation for the optimal unit of data striping in disk arrays.

In addition to analytic models specifically for disk arrays, work dealing with the modeling of fork-join queuing systems in general [Baccelli 1985; Flatto and Hahn 1984; Heidelberger and Trivedi 1982; Nelson and Tantawi 1988] is useful when modeling disk arrays. However, most of these papers model highly restrictive systems that are not easily applied to disk arrays.

The reliability of disk arrays is most frequently modeled using continuoustime Markov chains. The failure and recovery of components in the system cause transitions from one state to another.

Generally, the most useful information derived from such models is the average time to system failure and the equilib-

ACM Computmg  Vol 26, No 2, June 1994
rium state probabilities from which one can determine the fraction of failures caused by each type of failure mode. A
disadvantage of Markov reliability models is that the number of states necessary to model even simple disk arrays increases exponentially as new failure modes and system components are introduced. Fortunately, because the repair/
replacement rates for components of most disk arrays are much higher than the failure rates, it is usually possible to simplify greatly the Markov models by eliminating states that very rarely occur. To date, [Gibson 1991] presents the most complete reliability study of disk arrays.

## 5. Case Studies

Since the first publication of the RAID
taxonomy in 1987, the disk drive industry has been galvanized by the RAID
concept. At least one market survey, prepared by Montgomery Securities [1991],
predicted (optimistically) that the disk array market would reach $7.8 billion by 1994. Companies either shipping or having announced disk array products include: Array Technology Corporation (a subsidiary of Tandem), Ciprico, Compaq, Data General, Dell, EMC Corporation, Hewlett-Packard, IBM, MasPar, Maximum Strategies, Microtechnologies Corporation, Micropolis, NCR, StorageTek, and Thinking Machines. RAID technology has found application in all major computer system segments, including supercomputing, mainframes, minicomputers, workstation file servers, and PC file servers. We highlight some of these systems in the following subsections.

## 5.1 Thinking Machines Corporation Scalearray

The TMC ScaleArray is a RAID level 3 for the CM-5, which is a massively parallel processor (MPP) from Thinking Machines Corporation (TMC). Announced in 1992, this disk array is designed for scientific applications characterized by high bandwidth for large files. Thinking Machines also provides a file system that can deliver data from a single file to multiple processors from multiple disks
[Lo Verso et al. 1993].

The base unit consists of eight IBM
Model 0663E 15 disks. These 3.5-inch disks contain 1.2 GB of data and can transfer up to 2 MB/second for reads and 1.8 MB/second for writes. A pair of disks is attached to each of four SCSI-2 strings, and these four strings are attached to an 8 MB disk buffer. Three of these base units are attached to the backplane, so the minimum configuration is 24 disks. TMC expects the 24 disks to be allocated as 22 data disks, one parity disk, and one spare, but these ratios are adjustable.

Perhaps the most interesting feature of the ScaleArray is that these base units are connected directly to the data-routing network of the CM-5. Normally, massively parallel processors reserve that network to send messages between processors, but TMC decided to use the same network to give them a scalable amount of disk 1/0 in addition to a scalable amount of processing. Each network link offers 20 MB/second, and there is a network link for each base unit. As a consequence of communicating with the data network and the small message size of the CM-5, the interleaving factor is only 16 bytes. Parity is calculated by an onboard processor and sent to the appropriate disk.

Using the scalable MPP network to connect disks means there is almost no practical limit to the number of disks that can be attached to the CM-5, since the machine was designed to be able to scale to over 16,000 nodes. At the time of announcement, TMC had tested systems with 120 disks. Using their file system and 120 disks (including a single parity disk), TMC was able to demonstrate up to 185 MB/second for reads and up to 135 MB/second for writes for 240 MB
files. In another test, TMC demonstrated 1.5 to 1.6 MB/second per disk for reads and 1.0 to 1.1 MB/second per disk for writes as the number of disks scaled from 20 to 120. For this test, TMC sent 2 MB
to each disk from a large file.

## 5.2 Storagetek Iceberg 9200 Disk Array Subsystem

StorageTek undertook the development of disk array-based mainframe storage products in the late 1980s. Their array, called Iceberg, is based on collections of 5.25-inch disk drives yet appears to the mainframe (and its IBM-written operating system) as more traditional IBM 3380 and 3390 disk drives. Iceberg implements an extended RAID level-5 and level-6 disk array. An array consists of 13 data drives, P and Q drives, and a hot spare. Data, parity, and Reed-Solomon coding are striped across the 15 active drives within the array. A single Iceberg controller can manage up to four such arrays, totalling 150 GB of storage.

Iceberg incorporates a number of innovative capabilities within its array controller, called Penguin. The controller itself is organized as an 8-processor system and executes its own real-time operating system. The controller can simultaneously execute 8-channel programs and can independently transfer on four additional channels.

The controller manages a large, battery-backed semiconductor cache (from 64 MB up to 512 MB) in front of the disk array. This "extra level of indirection" makes possible several array optimization. First, the cache is used as a staging area for compressing and decompressing data to and from disk. This compression can double the effective storage capacity of the disk array. Second, when written data is replaced in the cache, it is not written back to the same place on disk. In a manner much like Berkeley's Log-Structured File System [Rosenblum and Ousterhout 1991], data is written opportunistically to disk in large tracksized transfer units, reducing random access latencies and performing adaptive load balancing. And third, the cache makes it possible to translate between the variable-length sectors used by most IBM mainframe applications and the fixed-size sectors of commodity small disk drives. StorageTek calls this process dynamic mapping. The controller keeps

ACM Computing  Vol 26, No. 2, June 1994

![31_image_0.png](31_image_0.png)

Figure 11. NCR 6'298 controller data path. The lock-step data path of the 6298 requires no memory for any operations except RAID level-5 writes. By placing the XOR and MUX directly in the data path, the controller can generate parity or reconstruct data on the fly,
track of free space within the array and must reclaim space that is no longer being used. The free-space data structures and track tables mapping between logical IBM 3380 and 3390 disks and the actual physical blocks within the array is maintained in a separate, 8 MB, nonvolatile controller method. Due to the complexity of the software for a system as ambitious as Iceberg, the product is over a year behind schedule, though at the time of this writing it is in beta test.

## 5.3 Ncr 6298

The NCR 6298 Disk Array Subsystem, released in 1992, is a low-cost RAID subsystem supporting RAID levels O, 1, 3, and 5. Designed for commercial environ-
ACM Comput]ng  Vol 26, No 2, June 1994 ments, the system supports up to four controllers, redundant power supplies and fans, and up to 20 3.5-inch SCSI-2 drives. All components—power supplies, drives, and controllers—can be replaced while the system services requests. Though the system does not allow on-line spares, built-in diagnostics notify the host when a drive has failed, and reconstruction occurs automatically when a replacement drive is inserted.

The array controller architecture features a unique lock-step design (Fig-are 11) that requires almost no buffering. For all requests except RAID level-5 writes, data flows directly through the controller to the drives. The controller duplexes the data stream for mirroring configurations and generates parity for RAID level 3 synchronously with data transfer. On RAID level-3 reads, the system can optionally read the parity along with the data, proving an additional check of data integrity, This lock-step nature also means that RAID level-3 performance does not degrade when a single drive fails.

The RAID level-5 implementation does not support full-stripe writes. Instead, the write path uses an intermediate SRAM buffer. When a write occurs, the old data and parity are read (in lock-step) from disk, exclusive-ored together, and stored into a 64KB SRAM parity buffer. As a side effect of data transfer from the host, the contents of the parity buffer are exelusive-ored with the data to generate the up-to-date parity, and the parity is written to the parity drive. While this design prohibits the overlap of data transfer for RAID level 5, the controller overlaps the drive-positioning operations.

This parsimonious use of buffers, in contrast with architectures such as RAID-II,
lowers the cost of the controller.

The lock-step data path is also used for reconstruction. Data and parity are read synchronously from the surviving drives, exclusive-ored together, and written to the replacement drive, Therefore, reconstruction is quite fast, approaching the minimum time of writing a single drive.

The host interface is fast, wide, differential SCSI-2 (20 MB/s), while the drive channels are fast, narrow SCSI-2 (10 MB/s). Because of the lock-step architecture, transfer bandwidth to the host is limited to 10 MB/s for RAID level O, 1, and 5. However, in RAID level-3 configurations, performance on large transfers has been measured at over 14 MB/s (limited by the host's memory system).

## 5.4 Tickertaip / Datamesh

TickerTAIP/DataMesh is a research project at Hewlett-Packard Labs whose goal is to develop an array of "smart" disk nodes linked by a fast, reliable network
[Cao et al. 1993] (Figure 12). Each node contains a disk, a CPU, and some local memory. Disk array controller operations

—

![32_image_0.png](32_image_0.png)

Figure 12. The TickerTAIP/DataMesh hardware architecture. A unique feature of the TickerTAIP
architecture is the close association of a CPU to each disk drive in the array. This association allows each node to perform some of the processing needed to perform a disk array operation.
such as parity computation are distributed among these smart disk nodes, and the nodes communicate by message passing across the internal interconnect.

A unique feature of the TickerTAIP
architecture is the close association of a CPU to each disk drive in the array (Figure 12). This association allows each node to perform some of the processing needed to perform a disk array operation. Additionally, a subset of nodes are connected to the host computers that are requesting data. Because more than one node can talk to the host computers, TickerTAIP can survive a number of node failures. In contrast, many other disk arrays have only one connection to host computers and hence cannot survive the failure of their disk array controller.

Currently, TickerTAIP exists as a small, 7-node prototype. Each node consists of a T800 transputer, 4 MB of local RAM, and one HP79560 SCSI disk drive. The TickerTAIP project is developing software to make the multiple, distributed processing nodes appear as a single, fast storage server. Early results show that, at least for computing parity, TickerTAIP achieves near-linear scaling [ Cao et al. 1993].

## '5.5 The Raid-Ii Storage Server

RAID-II (Figure 13) is a high-bandwidth, network file server designed and implemented at the University of California at Berkeley as part of a project to study

ACM Computing  Vol 26, No 2, June 1994

![33_image_0.png](33_image_0.png)

Figure 13. RAID-II architecture. A high-bandwidth crossbar connects the network interface (HIPPI), disk controllers, multi ported memory system, and parity computation engine (XOR). An internal control bus promdes access to the crossbar ports, while external point-to-point VME links provide control paths to the surrounding SCSI and HIPPI interface boards. Up to two VME disk controllers can be attached to each of the four WE interfaces.
high-performance, large-capacity, highly reliable storage systems [Chen et al.

1994; Drapeau et al. 1994; Katz et al. 1993]. RAID-H interfaces a SCSI-based disk array to a HIPPI network. One of RAID-II's unique features is its ability to provide high-bandwidth access from the network to the disks without transferring data through the relatively slow file server (a Sun4/280 workstation) memory system. To do this, the RAID project designed a custom printed-circuit board called the XBUS card.

The XBUS card provides a high-bandwidth path among the major system components: the HIPPI network, four VME
busses that connect to VME disk controllers, and an interleaved, multiported semiconductor memory. The XBUS card also contains a parity computation en-

ACM Computing  Vol 26, No 2, June 1994
gine that generates parity for writes and reconstruction on the disk array. The data path between these system conlponents is a 4 X 8 crossbar switch that can sustain approximately 160 MB/s. The entire system is controlled by an external Sun 4/280 file server through a memorymapped control register interface. Figure 13 shows a block diagram for the controller.

To explore how the XBUS card enhances disk array performance, Chen et al. [1994] compare the performance of RAID-H to RAID-I (Table 7). RAID-I is basically RAID-II without the XBUS card
[Chervenak and Katz 1991]. They find that adding a custom interconnect board with a parity engine improves performance by a factor of 8 to 15 over RAID-I.

The maximum bandwidth of RAID-II is

Table 7. Performance Comparison between RAID-II and RAID-I
Disk Array Read Disk Array Write Write Performance Performance Performance Degradation RAID-I 2.4 IW3fs 1.2 MBJS 50%
RAID-II ~().9 MB/~ 18.2 kiB/s 13%-1 RAID-II speedup 8.7 15.2 This table compares the performance of RAID-II to that of RAID-I. Because RAID-II has a special-purpose parity engine, disk array write performance is comparable to disk array read performance. All writes in this test are full-stripe writes [Lee and Katz 1991 b], For RAID-II reads, data is read from the disk array into XBUS memory, then sent over the HIPPI network back to XBUS memory. For RAID-I reads, data is read from the disk array into Sun4 memory, then copied again into Sun4 memory. This extra copy equalizes the number of memory accesses per data word. For RAID-II writes, data starts in XBUS
memory, is sent over HIPPI back into XBUS memory, parity is computed, and the data and parity are written to the disk subsystem. For RAID-I writes, data starts in Sun4 memory, gets copied to another location in Sun4 memory, then is written to disk. Meanwhile, parity is computed on the Sun4 and later written to disk. RAID-I uses a 32 KB striping unit with 8 disks (and is performance-limited by the Sun4's VME bus); RAID-II uses a 64 KB striping unit with 24 disks.
between 20 and 30 MB\s, enough to support the full disk bandwidth of approximately 20 disk drives.

## 5.6 Ibm Hagar Disk Array Controller

Hagar is a disk array controller prototype developed at the IBM Almaden Research Center [Menon and Courtney 1993]. Hagar was designed for large capacity (up to 1 TB), high bandwidth (up to 100 MB/s), and high 1/0 rate (up to 5000 4 KB 1/0s per second). Additionally, Hagar provides high availability through the use of redundant hardware components, multiple power boundaries, and on-line reconstruction of data.

Two design features of Hagar are especially noteworthy. First, Hagar uses battery-backed memory to allow user writes to provide safe, asynchronous writes (as discussed in Section 4.1.1). The designers of Hagar require each write to be stored in two separate memory locations in two different power regions to further increase reliability.

Second, Hagar incorporates a specialpurpose parity computation engine inside the memory of the controller. This is in contrast to the RAID-II architecture, which places the parity engine as a port on the controller bus (Figure 13). The Hagar memory system supports a special store operation that performs an exclusive-or on the current contents of a memory location with the new data, then writes the result to that location. Incorporating the parity engine in the memory complicates the memory system, but it reduces the data traffic on the controller's internal data bus.

Hagar was never fully operational; however, IBM is working on future disk array products that use ideas from Hagar.

## 6. Opportunities For Future Research

Redundant disk arrays have rejuvenated research into secondary storage systems over the past five to seven years. As this survey highlights, much has been proposed and examined, but much is left to do. This section discusses the classes of research not adequately understood with particular attention to specific problems.

open

## 6.1 Experience With Disk Arrays

area least have rem&-kably few published measurement results and experience. In addition to validating models and techniques found in the literature, such experience reports As an over five-year-old research that has sported products for at six years, redundant disk arrays

ACM Computmg  Vol 26, No 2, June 1994
can play an important role in technology transfer [Buzen and Shum 1986].

Furthermore, measurements frequently form the basis for developing new optimizations.

## 6.2 Interaction Among New Organizations

As this survey describes, there are many new and different disk array organizations. Most of these, including double failure correction, declustered parity, parity logging, floating parity, distributed sparing, log-structured file systems, and file-specific data striping, have been studied only in isolation. Unquestionably, among these there will be significant interactions, both serious new problems and obvious simplifications or optimizations.

As more is understood about the interactions among disk array technologies, designers and managers of disk arrays will be faced with the task of configuring and tuning arrays. As Section 4.5 discusses, redundant disk array performance and reliability modeling is largely incomplete and unsophisticated. Work needs to be done in the application of fundamental modeling to the problem of disk arrays as well as the development of that fundamental modeling, fork-join queuing models in particular. A good goal for this work is graphical, interactive analysis tools exploiting low-overhead monitoring data to guide configuration and tuning.

One objection lodged commonly against redundant disk arrays, particularly some of the newly proposed technologies, is their relatively high complexity. Storage systems are responsible for more than just the availability of our data, they are responsible for its integrity. As the complexity goes up, the opportunity for disastrous latent bugs also rises. This is compounded by the desire to increase performance by continuing computation as soon as storage modifications are delivered to storage server memory, that is, before these modifications are committed to disk. Inexpensive and highly reliable mechanisms are needed to control the

ACM Computmg  Vol 26, No 2, June 1994
vulnerability to increased software complexity of storage systems.

## 6.3 Scalability, Massively Parallel

Computers, and Small Disks One of the key motivations for redundant disk arrays is the opportunity to increase data parallelism in order to satisfy the data processing needs of future generations of high-performance computers.

This means that arrays must scale up with the massively parallel computers that are being built and the even more massively parallel computers being planned. Massively parallel disk arrays introduce many problems: physical size, connectively, delivery system bottlenecks, and storage control processing requirements to name a few. The most compelling approach to ever larger disk arrays is to embed storage based on the new generations of small diameter disks into the fabric of massively parallel computers, use the computer's interconnection network for data distribution and redundancy maintenance, and distribute the storage control processing throughout the processors of the parallel computer.

Though compelling, this approach has substantial problems to be overcome. Primary among these are the impact on the interconnection network of distributing the redundancy computations [Cao et al.

1993], the impact on the processors of distributing storage control, and the viability of allocating data on storage devices near the processors that will use it.

## 6.4 Latency

Redundant disk arrays are fundamentally designed for throughput, either high transfer rates for large, parallel transfers or large numbers of concurrent small accesses. They are effective only for reducing access latency when this latency is limited by throughput. For lowerthroughput workloads, disk arrays enhance storage performance only slightly over traditional storage systems.

Caching is the main mechanism for reducing access latency, but caching can be ineffective either because data is too large, too infrequently accessed, or too frequently migrated among caches. For these workloads, data prefetching is essential. Research into aggressive prefetching systems is beginning to examine opportunities to extract or predict future accesses and provide mechanisms to efficiently utilize available resources in anticipation of these accesses [Korner 1990; Kotz and Ellis 1991; Gibson et al. 1992; Patterson et al. 1993; Tait and Duchamp 1991].

## 7. Conclusions

Disk arrays have moved from research ideas in the late 1980's to commercial products today. The advantages of using striping to improve performance and redundancy to improve reliability have proven so compelling that most major computer manufacturers are selling or intending to sell disk arrays. Much research and implementation have been accomplished, both in industry and universities, but many theoretical and practical issues remain unresolved. We look forward to the many more fruitful years of disk array research.

## Acknowledgments

We thank Bill Courtright, Mark Holland, Jai Menon, and Daniel Stodolsky for reading an earlier draft of this article and for their many helpful comments. We are especially indebted to Bill Courtright and Daniel Stodolsky for writing the section of this article describing the NCR disk array.

## Annotated Bibliography

AMDAI-IL, G. M. 1967. Validi~ of the single processor approach to achieving large scale computing capabilities. In Proceedings of the AFIPS
1967 Spring Joint Computer Conference. Vol.

30. AFIPS, Washington, D. C., 483–485. Threepage paper that eloquently gives case for traditional computers by pointing out that performance improvement is limited by portion of the computation that is not improved.

BACCELLI, F. 1985. Two parallel queues created by arrivals with two demands. Tech Rep. 426, INRIA, Rocquencourt, France. Derives an exact solution for the two-server, M/G/ 1 fork-join queue.

BHIDE, A. AND DIAS, D. 1992. Raid architectures for OLTP. Tech. Rep. RC 17879 (\#78489), IBM,
Yorktown Heights, N.Y. Increases throughput for workloads emphasizing small, random write accesses in a redundant disk array by logging changes to parity for efficient application later.

Parity changes are logged onto a separate disk which must be externally sorted before application to the disk array's parity.

BITTON, D. AND GRAY, J. 1988. Disk shadowing.

In Very Large Database Conference XIV. Morgan Kaufmann, San Mateo, Calif., 33 1–338.

Describes disk mirroring and derives an analytical equation for read and write seek distances as a function of the number of data copies.

BURKHARDT, W. AND MENON, J. 1993. Disk array storage system reliability. In the 23rd Annual International Symposium on Fault-Tolerant Con-zputmg. IEEE Computer Society, Washington, D. C., 432–441. Argues need for multiple error-correcting disk arrays; discusses how to use maximal-distance separable codes to protect against multiple errors in a space-efficient manner.

BUZEN, J. AND Smm, W. C. 1986. 1/0 architecture in MVS/370 and MVS/XA. CMG Trans.

54 (Fall), 19-26. Overview of the MVS/370 and MVS/XA 1/0 architecture. Describes channel paths, storage directors, string controllers, rotational position sensing, static and dynamic reconnect.

CAO, P., LIM, S. B., VENK.ATAFtAMAN, S., AND WILKES,
J. 1993. The TickerTAIP parallel RAID architecture. In Proceedings of the 1993 In terna -
tional Symposium on Computer Architecture.

IEEE, New York. Describes the TickerTAIP
architecture, software implementation issues, and the performance of different methods of distributing parity computation among multiple processors.

CHANDY, J. AND REDDY, A. L. N. 1993. Failure evaluation of disk array organizations. In F'roceedmgs of the International Conference on Distributed Computing Systems. IEEE Computer Society, Washington, D.C. Contrasts four previously described schemes for minimizing data reconstruction time in small (7 and 16 disks)
redundant disk arrays: RAID 5 with a single spare disk, RAID 5 with a single spare whose space is distributed across all disks, a special case of Muntz and Lui's parity-clustering organization, and a method of dynamically converting a redundant data disk to a spare disk by merging two redundancy groups into one larger group. The second, distributed sparing, is generally preferred because of its performance and simplicity, but the Muntz scheme is better for minimal impact of user performance during recovery.

CHEN, P. M., GIBSON, G., KATZ, R., AND PATTERSON,
D. A. 1990. An evaluation of redundant arrays of disks using an Amdahl 5890. In Proceedings of the 1990 ACM SIGMETRICS
Conference on Measurement and Modeling of ACM Computing  Vol. 26, No. 2, June 1994 Computer Systems. ACM, New York. The first experimental evaluation of RAID. Compares RAID levels O, 1, and 5.

CHEN. P. M. .iND PATTERSON, D. A. 1990 Maximizmg performance m a str~ped disk array. In Proceedings of the 1990 Internatmnal Symposwrn on Computer ArchztecYure. IEEE, New York, 322–331. Discusses how to choose the strlpmg unit for a RAID level-O disk array.

CHEN, S, AND TOWSLEY, D. 1991. A queuemg anal ysis of RAID architectures. Tech. Rep.

COINS Tech. Rep. 91-71, Dept. of Computer and Information Science, Univ of Mas.

sachusetts, Amherst, Mass Analytically models RAID level-l and RAID level-5 disk arrays to compare their performance on small and large requests. Bounds are used to model the queuing and fork-loin synchmmzation m RAID
level-l disk arrays. Small write requests in RAID level-5 disk arrays are handled by ignoring the fork-join synchromzatlon overhead.

Large requests are modeled by using a single queue for all the disks m the disk array.

CHEPJ, P. M AND LEE, E. K. 1993 Striping in a RAID level-5 disk array Tech. Rep. C'SE-TR181-93, Univ. of Michigan, Ann Arbor, Mlch.

Discusses bow to choose striping umt for RAID
level-5 disk arrays. Quantifies effect of writes and varying number of disks CH~N, P. M., L!@ E. K,, DRAPEALI, A. L., LUTZ. K,
MILLER, E. L., SESHAN, S., SHIRRWF, K., PATTER-S(JN D. A., .4NU KATZ, R, H. 1994, Performance and design evaluation of the RAID-II
storage server. J. Dwtrlb. Parall. Databases.

To be published. Also in The 1993 Internatzonai Parallel Processing Symposium Workshop on I/O m Parallel Con2puter Systen2.s Summarizes major architectural features of RAID-II
and evaluates bow they impact performance CH~RVENAJi, A. L. ANI) KATZ. R. H. 1991 Performance of a disk array prototype In Proceed1ngs of the 1991 ACM SIGMETRICS Conferen.e on Measurement and Modellng of Computer Systems Perf. Elal. ReL). 19, 5 (May).

188-197 Evaluates the performance of RAID-I,
a CTC. Berkeley disk array prototype.

COPELAND, G., AJ.EXANOER, W., BCWGH'I MR, E . .ANLJ
KELLER, T. 1988 Data placement in Bubba In Pruceedzngs of the ACM SIGMOD Intern atmnal Conference on Management of Data ACM, New York, 99–108. Ehscusses data allocation in a large database.

DRA~EMJ, A. L., SHIRRIF~, K., LEE, E, K, CHEN,
P, M , GIBSON, G A., HARTMAN, J. H MILLER,
E. L., SFSJ+AN, S., KATZ, R. H , LUTZ. K, AND
PATTERSON, D. A 1994. RAID-II: A highbandwldth network file server In Proeeedmgs of the 1994 Internatmnal Symposzum on Computer Archztectw-e. IEEE, New l"ork. Describes the architecture, file system, and performance of RAID-II, a disk array file server prototype, EMLICH, L, W. AND POLICH, H. D. 1989 VAXslmPLUS, a fault manager implementation Dzg.

AC!M Cbmputmg  Vol 26. No 2, June 1994 Tech. J. 8, (Feb.) Describes D1~tal Eqmpment Corporation's tool for predicting and avoiding disk failures FLATTO, L. AND HAHN, S. 1984. Two parallel queues created by arrivals with two demands I}. SIAM J. Cmnput, 44, 5 (Oct.), 1041-1053, Derives an exact solutlon for the two-server, M/M/l, fork-join queue.

FRIEDMAN, M. B 1983. DASD access patterns. In the 14th International Conference ori Managentent and Performance Evaluatwn of Computer Systems Computer Measurement Group, 51–61 Looks at how much disk accesses are skewed toward particular disks in se~,eral transaction-processing sites.

GIBSON, G. A. 1992. Redundant disk arrays Rehable, parallel secondary storage Ph.D. thesis.

Univ of Califorma. Berkeley, Calif. Also available from MIT Press, Cambridge, Mass.

Award-winning dissertation that describes RAIDs m detail, with emphasis on rehability analysis of several alternatives, GIBSON, G. A., PATTERSON, R. H,, AND SATYANA.RAY.4NAN, M. 1992. Dusk reads with DRAM
latency In the 3rd Workshop on Warkstatzon Operatzng Systems. IEEE Computer Society, Washington, DC. Proposes that apphcatlons give hints about their future file accesses so that the buffer cache can prefetch needed data and provide low-latency file access. The hints could be exploited also to Improve cache management and disk scheduling GRAY, J., HORST, B , AND WALK~R. M. 1990. Parity striping of disc arrays: Low-cost rehable storage with acceptable throughput In Procwdl ngs of the 16th i'ery Large Database Conference. Morgan Kaufmann. San Mateo, Calif, 148–160. Describes a data and parity layout for disk arrays called parity striping. Par@ striping M essentially RAID level 5 with an Infinite striping umt and manual load balanclng, H.4LL, Nl 1986. Cornbmatorzal Theory. 2nd ed.

Wdey-Interscience, New York. Textbook on combinatorial theory. The section on balanced, incomplete block designs are most rele~,ant for readers of this article HEIJMLBERGER, P AND TRIVEDI, K. S. 1982. Qeuemg network models for parallel processing with asynchronous tasks. IEEE Trons Comput C31, 11 (No\,.). 1099– 1109. Deriz-es approximate solutions for queuing systems with forks but no Joins.

HENNEXW, J. L. AND P~TT~RSON, D. A. 1990, Computer Architecture A Quantltatu,e Approach. Morgan Kaufmann, San Mateo, Calif.

Likely the most popular general book in computer architecture today, the discussion on technology trends, general 1/0 issues, and measurements of seek distances are most relevant to readers of this article HOLLAND, M., AND GIBSON, G. 1992. Parity declustermg for continuous operation in redundant disk arrays. In Proceedings of the 5th International Conference on Architectural Support for Programming Languages and Operating Systems ( ASPLOS-V), IEEE, New York, 23-35. Describes parity declustering, a techmque for improving the performance of a redundant disk array in the presence of disk failure. Analyzes the proposed solution using detailed simulation and finds sigmficant improvements (20–50Vc) in both user response time and reconstruction time. Also analyzes a set of previously-proposed optimizations that can be applied to the reconstruction algorithm, concluding that they can actually slow the reconstruction process under certain conditions.

HOLLAND, M. GIBSON, G,, AND SIF,WIOREK, D. 1993 Fast, on-line failure recovery in redundant disk arrays. In Proceedings of the 23rd In tern ational Symposium on Fault Talerant t30mputing IEEE Computer Society, Washington, D.C.

Compares and contrasts two data reconstruction algorithms for disk arrays: "parallel stripe-oriented reconstruction" and "disk-oriented reconstruction." Presents an implementation of the disk-oriented algorlthm and analyzes reconstruction performance of these algorithms, concluding that the disk-oriented algorlthm is superior. Investigates the sensitivity of the reconstruction process to the size of the reconstruction umt and the amount of memory available for reconstruction.

HSIAO, H. AND DEWITT, D. 1990. Chained declustering A ncw availability strategy for multiprocessor database machines. In Proceedings of the 1990 IEEE Intern atumal Conference on Data Engineering. IEEE, New York, 456-465.

Introduces a variation of mirroring, where the secondary copy of data is distributed across the disks in a dif~erent manner than the primary copy of data.

KATZ, R. H. 1992. High performance network and channel-based storage. Proc. IEEE 80, 8 (Aug.),
1238–1261. Presents overview of network-based storage systems. Reviews hardware and software trends in storage systems.

KATZ, R. H., CHEN, P. M., DRAIJMAU, A. L., Lm, E, K., Lure, K,, MILLEIR, E. L., SMHAN, S.,
PATTERSON, D. A. 1993. RAID-II: Design and implementation of a large scale disk array controller. In the 1993 Symposium on Integrated Systems. MIT Press, Cambridge, Mass. Describes the design decisions and implementation experiences from RAID-IL
KIM, M. Y, 1986 Synchronized disk interleaving.

IEEE Trans. Comput. C-35, 11 (Nov.), 978-988.

Simulates the performance of independent disks versus synchronized disk striping. Derives an equation for response time by treating the synchronized disk array as an M/G/1 queuing system, KIM, M, Y, ANU TANTAWI, A. N. 1991. Asynchronous disk interleaving: Approximatmg access delays. IEEE Trans. Comput. 40, 7 (July),
801–810. Derives an approximate equation for access time in unsynchronized disk arrays when seek times are exponentially distributed and rotational latency is uniformly distributed.

KORNER, K. 1990. Intelligent caching for remote file service. In Proceedings of the Znternatmnal Conference on Distributed Computing Systems.

IEEE Computer Society, Washington, DC.,
220-226. Uses traces to generate hints based on the program running and the directory and name of files accessed. The file server uses the hints to pick a caching algorithm: LRU, MRU,
none. Simulation showed sigmficant benefits from intelhgent caching but not from readahead which delayed demand requests since it was not preemptable.

KOTZ, D. ANTI ELLIS, C. S. 1991. Practical prefetching techniques for parallel file systems.

In Proceedings of the 1st International Conference on Parallel and Distributed Information Systems. ACM, New York, 182–189. File access predictors use past accesses to prefetch data in idle nodes of a parallel file system Simulation studies show that practical predictors often can significantly reduce total execution time while the penalty for incorrect predictions m modest.

LEE, E. K. ANU KATZ, R. H. 1991a An analytic performance model of disk arrays and its applications. Tech. Rep. UCB/CSD 91/660, Univ. of California, Berkeley, Calif Derives an analytic model for nonredundant disk arrays and uses the model to derive an equation for the optimal size of data striping.

Lm, E. K. AND KATZ, R, H, 1991b. Performance consequences of parity placement m disk arrays, In Proceedings of the 4th International Conference on Architectural Support for Programming Languages and Operatzng Systems
( ASPLOS-ZV). IEEE, New Yorkj 190-199, Investigates the performance of different methods of distributing parity in RAID level-5 disk arrays.

Lm, E. K. AND KATZ, R. H. 1993. An analytic performance model of disk arrays. In Proceedings of th 1993 ACM SIGMETRICS Conference on Measurement and Modehng of Computer Systems. ACM, New York, 98–109. Slmdar to earlier technical report with simdar name except with better empirical justltlcations and a more detailed study of the model's properties.

LIVNY, M. KHOSHA~IAN, S., AND BORAI., H. 1987 Multi-disk management algorithms. In Prm ceedings of the 1987 ACM SIGMETRICS Conference On Measurement and Modeling of Camputer System. ACM, New York, 69-77'.

Compares performance of disk arrays with track-sized and infinite striping units. Concludes that striping can improve performance for many multidisk systems.

LOVERSO, S. J., ISMAN, M., AND NANOPOULOS, A.

1993. A Parallel file system for the CM-5. In Proceedings of the USENIX Summer Conftir-
ACM Computing  Vol. 26, No, 2, June 1994 erzce. USENIX Assoclatlon, Berkeley, Calif. A
description of the 1/0 hardware and the file system of the massively parallel processor from Thinking Machines. Them RAID-3 disk array has excellent performance for large file accesses.

MALHOTRA, M. AND TRIVE~I, S. 1993. Rehabihty analysis of redundant arrays of inexpensive disks. J. Parall. Dwtr. Comput. 17, (Jan.),
146– 151 Uses Markov models to derive exact, closed-form reliability equations for redundant disk arrays. Analysis accounts for failure prediction and sparing.

MENON, J. AND CORTNEY, J. 1993. The architecture of a fault-tolerant cached RAID controller In Proceedings of the 20th International S.vm -
posum on Compufer Architecture IEEE, New York, 76–86. Describes the architecture of Hagar and several algorithms for asynchronous writes that reduce susceptlblhty to data loss.

MF,NON, J., MATTSON, D., ANrI NG, S. 1991. Distributed sparing for improved performance of disk arrays. Tech Rep. RJ 7943, IBM, Almaden Research Center. Explores the use of an on-line spare disk in a redundant disk array analytically It examines multiple configurations, but fundamentally it distributes the spare's space over the whole array so that every disk is N/(N + 2) data, l/(N + 2) parity, and l/(N
+ 2) spare. This gives an extra l/(N + 2) performance, but, more significantly, it distributes the recovery-write load (the reconstructed data) over all disks to shorten recovery time. The benefits, not surprisingly, are largest for small arrays.

MENON, J., ROCHE, J., AND KASSON, J. 1993 Floating parity and data dmk arrays. J. Parall.

Dzstrib. Comput. 17, 129–139, Introduces floating data and floating parity as an optimization for RAID level-5 disk arrays. Discusses performance and capacity overheads of methods.

MERCHANT, A. ANJ) Yu, P, 1992, Design and modehng of clustered RAID. In Proceedz ngs of the International Symposium on Fault Tolerant Computing. IEEE Computer Society, Washington, D. C., 140–149. Presents an implementation of parity declustering, which the authors call "clustered RAID," based on random permutations, Its advantage is that it 1s able to derive a data mapping for any size disk array with any size parity stripe, and the corresponding disadvantage is that the computational requirements of the mapping algorlthm are high compared to the block-design-based approaches. Analyzes response time and reconstruction time using this technique via an analytic model, and finds substantial benefits m both.

MONTGOMERY SECURITIES 1991. RAID: A technolOgy pomed for explosive growth. Tech. Rep.

DJIA: 2902, Montgomery Securities, San Franc] SCO, Calif. Industry projections of market growth for RAID systems from 1990 to 1995, ACM Computing Surveys. Vol 26, No 2, June 1994 MUNTZ, R. R, AND LUI, C, S. 1990. Performance analysis of disk arrays under fadure. In Proceedings of the 16th Conference on Very Large Data Bases. Morgan Kaufmann, San Mateo, Calif. Proposes and evaluates the "clusteredRAID" technique for improving the fadure-recovery performance in redundant disk arrays.

It leaves open the problem of implementation:
no techmque for efficiently mapping data units to physical disks is presented. Analyzes via an analytical model the technique and two potential "optimlzatlons" to the reconstruction algorithm, and finds significant benefits to all three.

NELSON, R, AND TANTAWI, A. N. 1988, Approximate analysis of fork/join synchronization in parallel queues. IEEE Trans. Comput. 37, 6
(June), 739-743 Approximates response time in fork-join queuing systems with k > = 2 servers where each logical request always forks into k requests.

NG, S. 1994. Crossbar disk array for Improved rehability and performance In Proceedz ng.s the 1994 Intern atmnal S.vmposzum on Computer Architecture, IEEE, New York, Introduces schemes to protect against multiple failures of disk support hardware such as dmk controllers and strings.

NG, S AND MATTSON, D. 1991 Maintaining good performance in disk arrays during failure- via uniform parity group distribution. In Proceedings of the 1st International Symposium on High Performance Distributed Computing.

260–269 Uses balanced, incomplete block designs to distribute the extra load from a failed disk equally among other disks in the array.

ORJI, C. U. AND Scmwowm, J. A, 1993. Doubly distorted mirrors. In Proceeduzgs of the ACM
SIGMOD International Conference on Management of Data. ACM, New York. Describes a technique called dmtorted mirrors that partitions each of two mirrored disks into two halves, one of which lays out the data in a standard fashion, one of which "distorts" the data layout.

This accelerates writes to the distorted copy while preserving the abihty to read large files sequentially.

P~TTERSON, D. A. ANr) HENNI?,SSY, J L. 1994.

Computer Organization and Design: The Hardware /Sof?ware Interface. Morgan Kaufmann, San Mateo, Cahf. A popular undergraduate book in computer architecture, the discussion on technology trends are most relevant to readers of this article, PATTERSON, D, A., GIBSON, G., AND KATZ, R. H.

1988. A case for redundant arrays of inexpenswe disks (RAID) In In ternatlonat Con ference on Management of Data (SIGMOD). ACM, New York, 109–116. The first published Berkeley paper on RAIDs, It gzves all the RAID nomenclature.

PATTERSON, R. H., " GIBSON, G. A., AND SATyANARAYANAN, M, 1993. A status report on research in transparent informed prefetching.

ACM Oper. Syst. Rev. 27, 2 (Apr.), 21-34. Expands on using application hints for file prefetching in Gibson et al. [ 1992]. Hints should disclose access patterns, not advise caching/
prefetching actions. Greatest potential from converting serial accesses into concurrent accesses on a disk array. Presents preliminary results of user-level prefetching tests.

PETERSON, E. W. AND WELDON, E. J. 1972.

Error-Correcting Codes. 2nd ed. MIT Press, Cambridge, Mass. A general textbook on the mathematics of error-correcting codes.

ROSENBLUM, M. AND OUSTERHOUT, J. K. 1991. The design and implementation of a log-structured file system. in Proceedwzgs of the 13th ACM
Symposium on Operating Systems Principles.

ACM, New York. Describes a log-structured file system that makes all writes to disk sequential. Discusses efficient ways to clean the disk to prevent excessive fragmentation.

SALEM, K. AND GARCIA-M• LINA, H. 1986. Disk striping. In Proceedings of the 2nd International Conference on Data Engineering. IEEE
Computer Society, Washington, D. C., 336-342. Early paper discussing disk striping.

SCHEUERMANN, P., WEIKUM, G., AND ZABBACK, P.

1991. Automatic tuning of data placement and load balancing in disk arrays. Database Systems for Next-Generation Applications: Principles and Practzce. Describes heuristics for allocating tiles to disks to minimize disk skew.

SCHULZE, M., GIBSON, G. KATZ, R., AND PATTERSON,
D. 1989. How reliable is a RAID, In Procedures of the IEEE Computer Society International Conference ( COMPCON). IEEE, New York. Gives a reliability calculation for the electronics as well as the disks for RAIDS.

SELTZER, M. I., CHEN, P. M., AND OUSTERHOUT, J. K.

1990. Disk scheduling revisited. In Proceedings of the Winter 1990 USENIX Technical Conference. USENIX Association, Berkeley, Calif. 313–324. Reexamines the problem of how Recewed November 1993; final revision accepted March 1994 to efficiently schedule a large number of disk accesses when accounting for both seek and rotational positioning delays.

STODOLSKY, D. AND GIBSON, G. A. 1993. Parity logging: Overcoming the small write problem in redundant disk arrays. In Proceedings of the 1993 International Symposium on Computer Architecture. Increases throughput for workloads emphasizing small, random write accesses in a redundant disk array by logging changes to the parity in a segmented log for efficient application later. Log segmentation allows log operations that are large enough to be efficient yet small enough to allow in-memory application of a log segment.

TAIT, C. D. AND DUCHAMP, D. 1991. Detection and exploitation of file working sets. In Proceedings of the International Conference on Distributed Computzng Systems. IEEE Computer Society, Washington, D. C., 2–9. Dynamically builds and maintains program and data access trees to predict future file accesses. The current pattern is matched with previous trees to prefetch data and manage the local cache in a distributed file system. Trace-driven simulation shows reduced cache miss rates over a simple LRU algorithm.

WEIKUM, G. AND ZABBACK, P. 1992. Tuning of striping units in disk-array-based file systems.

In Proceedings of the 2nd International Workshop on Research Issues on Data Engineering:
Transaction and Query Processing. IEEE Computer Society, Washington, D. C., 80–87. Proposes file-specific striping units instead of a single, global one for all files.

WILMOT, R. B. 1989. File usage patterns from SMF data: Highly skewed usage. In the 20th ZnternatLonal Conference on Management and performance Evahatton of Computer systems.

Computer Measurement Group, 668-677. Reports on how files are accessed on four large data centers and finds that a small number of files account for most of all disk 1/0.

## Acm Computing  Vol. 26, No. 2, June 1994
