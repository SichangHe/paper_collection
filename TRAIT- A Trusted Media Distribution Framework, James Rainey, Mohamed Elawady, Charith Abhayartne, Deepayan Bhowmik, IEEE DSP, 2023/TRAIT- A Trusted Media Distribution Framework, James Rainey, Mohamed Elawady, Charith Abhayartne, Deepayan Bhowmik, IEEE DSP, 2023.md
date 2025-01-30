   

1 Paper

# Trait: A Trusted Media Distribution **Framework**

Publisher: IEEE Cite This  PDF
James Rainey ; Mohamed Elawady ; Charith Abhayartne ; Deepayan Bhowmik All **Authors** 
Cites in 88 Full Text Views Alerts Manage Content Alerts Add to Citation Alerts 

#### Abstract

Downl Document Sections I. Introduction II. JPEG standardisation on Fake Media III. The framework IV. Use Cases V. Conclusions Authors Figures References Citations Keywords Metrics More Like This Footnotes Abstract: Trusted distribution and consumption of media content has become a challenging issue, especially with the advancement of machine learning-based techniques such as deep fa... **View more**

|  Metadata Abstract:   |
|------------------------|

Trusted distribution and consumption of media content has become a challenging issue, especially with the advancement of machine learning-based techniques such as deep fake. To address such challenges, this paper proposes a new metadata schema which is embedded within a larger framework that facilitates trusted media distribution. This schema is realised through a distributed media blockchain core in conjunction with algorithms to detect media modifications. Such a framework is expected to improve trust in media consumption, ensuring media integrity, authenticity and provenance.

Published in: 2023 24th International Conference on Digital Signal Processing (DSP)
Date of Conference: 11-13 June 2023 Date Added to IEEE *Xplore*: 05 July 2023 ISBN Information:
 ISSN Information:
DOI: 10.1109/DSP58604.2023.10167909 Publisher: IEEE Conference Location: Rhodes (Rodos), Greece Contents

## Section I. Introduction

The emergence of machine learning-based image manipulation opens up new possibilities in the creative sector, as it is now possible to produce near-realistic media assets. A recent example includes 'For All Mankind', which uses deepfake technology to bring back well-known characters such as Johnny Carson, John Lennon, and Ronald Reagan [1]. However, it equally causes the creation of fake media that spreads misinformation and plays havoc in many aspects of human society, from political unrest to financial harm
[2]. As a result, public trust is being diminished in any media they consume. Therefore, it is necessary to create a solution, even better, a framework that can help media distribution to be transparent and trusted. In an attempt to address such gaps, this paper proposes a TRusted MediA DIsTribution (TRAIT) framework that provides a metadata schema in Extensible Markup Language (XML) and its implementation using Extensible Metadata Platform (XMP). An example of image manipulation and detection using the TRAIT framework is shown in Fig. 1.

PDF
In achieving trust in media distribution, information such as ownership, copyright, intellectual property rights (IPR), provenance, integrity, authenticity etc. **are crucial. Literature suggests individual tools, techniques and** software are available both in academia we well as the industry. For example, ownership, copyright, and IPR are available through 1) XIF (eXtended Image Format), JPEG Systems Part 4: Privacy and Security [3] or other metadata formats; 2) digital watermarking [4] and 3) Digital Right Management software, **e.g.**,
Imagen , VdoCipher **. Tracing back the previous history or even the origin, in short, the provenance of an**
image is important, especially in relation to media distribution and has been a topic of recent interest [5],
[6]. The integrity of an image is commonly verified using content hashing and file hashing. Recently, content authenticity has generated significant interest in the community, especially due to the advancement of photo editing tool sets and machine learning-based models such as *deep fake.* **A significant number of detection** algorithms are available in the literature, and we briefly discuss the notable ones here.

1 2

![1_image_0.png](1_image_0.png)

3

Fig. 1:
Examples of fake media (image manipulation): object modification, cropping and blur. 1st and 2nd columns are the original and the modified versions of images, and 3rd column represents the output of TRAIT framework. The modified regions have been highlighted in green (2nd column) and red colors (3rd column).

File-based cryptographic/hashing algorithms are commonly used to verify the integrity and authenticity of a file by generating a unique digital fingerprint. The most popular hashing algorithms are SHA1 (1995), MD5 (1995), SHA256 (2002) and Blake3 (2020), which are different in security levels and computation time. However, file hashing is not always suitable for media files as often media contains remain the same, but file hashes change due to file format conversion or compression. Considering image-based contextual information, perceptual hashing algorithms are introduced to focus on pixel changes inside an image by looking into visual features (*i.e.*, color, texture etc.**) in order to generate a unique hash value. In the pre-deep** learning era, there were traditional/hand-crafted approaches for perceptual hashing: Average Hash (A-Hash)
[7], Perceptual Hash (P-Hash) [8], Singular Value Decomposition Hash (SVD-Hash) [9], Wavelet Hash (W- Hash) [10] and Laplace-based Hash (L-Hash) [11]. More recently, the learning-based (deep) hashing approaches have become popular [12]– **[14].**
Although the perceptual hashing is robust against clearly visible image manipulation (*i.e.***, cropping, rotation**
etc.), it is vulnerable to barely visible / illusion-based attacks (*i.e.***, splicing, local region removal/editing). In**
overcoming that, literature proposed recent deep-based approaches for fake media/tampering detection such as ManTra-Net [15], SPAN [16], MVSS [17], [18] and EMT-Net [19].

While techniques for individual components are generally available, there is no/very little existing mechanism that holistically provides means to transparently communicate such information to the end user in a comprehensive manner. To the best knowledge of the authors, the closest and current attempt is made by an industry consortium C2PA (Coalition for Content Provenance and Authenticity) led by Adobe Inc. **. C2PA** provides a metadata schema and an implementation mechanism (through JPEG universal metadata box format (JUMBF) [20]). However, notable exclusions in C2PA include the ability to detect tampering or other modifications in the media and the availability of metadata in a centralised or decentralised repository. To address these gaps, TRAIT framework is proposed (see Section III) in this paper. Main contributions are:
4 5 formats) implementation for metadata embedding. Development of a modular framework that uses blockchain and IPFS (InterPlanetary File System) as its core components to facilitate secure and transparent means to manage and share relevant information and store the assets in a distributed file server.

Demonstration of TRAIT framework capability through two real-life inspired use cases.

In this context, it is worth noting that JPEG is making a substantial effort to address the challenges of **media**
trust **through an upcoming international standard. Among others, the proposed TRAIT framework is actively** engaged in this process and envisages contributing in a significant manner.

6

## Section Ii. Jpeg Standardisation On Fake Media

As part of the international standardisation body Joint Photographic Experts Group (JPEG) committee

![2_image_0.png](2_image_0.png)

(ISO/IEC JTC 1/SC 29/WG 1) initiated a standardisation effort called JPEG Fake Media in order to provide a mechanism that facilitates a secure and reliable annotation of media asset creation. The standardisation aims to support both use cases that are in good faith, *e.g.***, media creation for entertainment or marketing, as well as**
those with malicious intent, *e.g.*, spreading misinformation. As part of this initiative, JPEG published a Use Cases and Requirements **document [21] and issued a call for proposals [22] in April 2022. In response to this**
call, the proposed TRAIT framework was submitted, which complies with most of the requirements outlined in the call issued by JPEG. The TRAIT framework builds upon and extends the utility of the JPEG standard by proposing a metadata schema, its implementation, and example use cases that use this framework.

Fig. 2:
Overview of the TRAIT Framework.

## Section Iii. The Framework

#### A. **Overview**

The proposed framework consists of four components as depicted in Fig. 2: 1) Graphical Web Interface, 2) Media Blockchain, 3) Manipulation Detection engine and 4) Distributed File Server.

1) Graphical Web Interface **provides an interface by which users can register new images, verify existing**
images and add modified versions of images to the TRAIT repository. For the implementation, REACT
(a front-end JavaScript library) is used for the interface and backend connectivity.

7 2) Media Blockchain **is the core of the TRAIT framework which uses Hyperledger Fabric [23], [24] as its**
core technology. This is an extension of our previous work on *Multimedia Blockchain* **[25] and is** responsible for recording the transactions of media assets and verifying the integrity of the assets. Each transaction registered on the TRAIT framework consists of a number of fields as defined in the TRAIT
schema shown in Fig. 3. Newly registered images are given a Media Unique ID (MUID), which is generated from a hash of the asset. Basic details such as *Name* and *Location* **are entered by the user on**
the registration page of the web interface.

Details of any modifications are added automatically, including the probability, the method used, regions of interest, the type and category of the modifications along with a user-defined text field to provide a purpose for modification. Each uploaded image is assigned an ImageID and a Parent ID. The ImageID is unique to that image, the ParentID is the ImageID of the parent image, and both IDs are distinct from the MUID, except for the root image in which all 3 IDs are identical.

The inclusion of the Image ID and ParentID allows multiple distinct modified versions of an image to exist in

![3_image_0.png](3_image_0.png) parallel, even if they have the same parent image. This also allows the full transaction history of an image, including all modified child images, to be retrieved using a single ID. The metadata is embedded to the image file head using a new set of XMP tags as defined in the TRAIT metadata schema (Fig. 3).

Fig. 3:

TRAIT Metadata Schema.

3) Manipulation Detection Engine **accepts input by uploading images with existing metadata, which**
results in a search using the embedded ID, after which images that have previously been registered are scanned for modifications using an image manipulation detection algorithm such as MVSS [18]. A probability (currently derived through MVSS) that the image contains modification is produced as well as a binary mask showing any modified areas detected in the image.

4) Distributed File Server **manages the storage of registered images via the Inter Planetary File System**
[26]. Each subsequent modified version of an image is also stored on the file server and a link to the file is retained within the metadata stored in the image and on the related blockchain transaction.

#### B. Image **Registration**

Image registration is performed when a user uploads a new image that does not contain TRAIT metadata or does not have a hash matching any previously registered image. To successfully register a new image the user is also required to input their name and location. A new unique ID will be generated for the image from a hash of the image, using SHA256, and will be used for the MUID and ImageID. The modification data is initialised, with all fields set to "None". For a modified version of a previously registered image, the existing information from the previous transaction is used to initialise many of the data fields, other than the ImageID which is calculated for that specific image and the purpose field which is provided by the user. The metadata is then embedded into the XMP tags of the image file and a new transaction is created on the blockchain, both using the schema defined in figure 3. The image is now registered and ready for verification.

#### C. Image **Verification**

Image verification is performed when a user searches with, or tries to register, an image containing existing TRAIT metadata. The image hash is calculated and compared to the stored hash, if there is a difference the image is passed through the modification detection algorithm. The modification detection algorithm returns a probability that the image has been modified as well as a binary mask showing the likely areas in which the modifications occur. Alongside the modification results there is a list of each transaction that has occurred for the selected image, this allows the user to trace the asset modification history and to verify the authenticity and provenance of the image.

An image that has a transaction history and has produced a probability of modification over a threshold is flagged and can be registered as a new modified version of the image. Only the original creator of the image will have the ability to add this new transaction.

## Section Iv. Use Cases

We provide two real-life inspired use cases that demonstrate the application of the TRAIT framework. Use case 1 presents an example of a photographer using the framework to prevent copyright violations of their work. Use case 2 presents an example of an art collector verifying the authenticity and provenance of a physical artwork before purchasing it. Both of these use cases make use of the proposed TRAIT framework workflow consisting of the web interface, media blockchain, IPFS distributed file system and REST (Representational state transfer) API (to link the blockchain and IPFS) along with the choice of MVSS [18] algorithm for image modification detection.

#### A. Use Case 1: Photography Copyright **Infringement**

Photographers own the copyright on any original photographs that they create. Having a copyright gives them the exclusive right to distribute and sell their images; users of the images will need permission from the creator to use them in any capacity. Nowadays, throughout the digital world, copyright infringement cases have been prominent since the last decade [27] (*i.e.***, Shepard Fairey vs The Associated Press, Cariou vs**
Prince).

In this use case, User A, a photographer, takes a photograph with their camera and becomes the copyright

![4_image_0.png](4_image_0.png)

owner for the image produced. They register the image using the TRAIT framework; a new set of metadata is generated containing a unique ID. The metadata is embedded in the image, a transaction containing the metadata is added to the blockchain and a copy of the image is stored on IPFS.

User B obtains the image and modifies it, applying a median filter to the image. They try to register the image claiming to be the original photographer and infringing on the original creator's copyright. When they attempt to register the modified image on the TRAIT framework, the existing metadata is detected and the unique ID
is found. This is used to look up the transaction history of the original image on the blockchain. The image is scanned by the image manipulation detection algorithm, which highlights the modifications to the image and subsequently registration of the image as a new media asset is stopped. Infringement of the original photographer's copyright is prevented. This is shown in Fig. 4.

However, with permission of the copyright holder, this modified image can be registered as a modification of the existing asset which would create a new transaction in the existing transaction tree and a new modification to the history of the asset.

B. Use Case 2: Art **forgery**
Buying and selling art can be a very lucrative business, however, this makes it a target for forgery. Tracking the authenticity and provenance of an artwork is an important stage in preventing forgeries and reproductions of artworks being maliciously or accidentally mistaken for original pieces. Several incidents of art forgery have occurred over the last century and have been sold for significant sums of money [29], [30],
including Han van Meegeren's Vermeer and Elmyr de Hory's Matisse & Modigliani.

In this use case, User A, an art collector, takes a digital photograph of an artwork and registers it on the TRAIT framework. New metadata is generated for the image and is recorded in both the XMP tags of the image and a blockchain transaction. This allows the authenticity and provenance of the artwork to be verified if the collector wishes to sell it.

User B, a second art collector, wishes to buy the same artwork owned by user A that is being displayed in an

![5_image_0.png](5_image_0.png)

art gallery. However, before making the purchase they want to verify the authenticity of the artwork. A digital photograph of the artwork is taken and a search is performed on the TRAIT framework. Unfortunately, User B
received a *forged artwork* **and the results show distinct differences and areas of modification compared to the** original, as shown in Fig. 5, and the transaction history presented does not match the history suggested by the seller.

Fig. 5:

Use Case 2 search result, using Fragonard's Young Woman [31].

The differences between the images and the discrepancy in the provenance of the artwork indicate that it may not be authentic. As the collector is unable to verify that the artwork that they wanted to acquire is the original and not a reproduction, they do not complete the purchase.

# Section V. Conclusions

We have presented a new framework which promotes improved trust and transparency in media distribution by ensuring the integrity, authenticity and provenance of media assets. The TRAIT framework provides a metadata schema which is implemented using a media blockchain and integrates media manipulation detection to allow the verification of the integrity of media assets. The use of file hashing combined with fake media detection facilitates the recognition of local changes between images. We provide two use cases to show the capabilities of the current TRAIT framework.

TRAIT framework expects to be expanded significantly in future to accommodate various needs in different industries, including but not limited to the creative industry, news syndicates, GLAM sector (galleries, libraries, archives, and museums), and insurance services. The framework will be made open-sourced to support the community and to build upon usable applications.

| Authors    |    |
|------------|-----|
| Figures    |    |
| References |    |
| Citations  |    |
| Keywords   |    |
| Metrics    |    |
| Footnotes  |    |

#### Ieee Account

» Change Username/Password
» Update Address Purchase Details
»Payment Options
»Order History
»View Purchased Documents Profile Information
» Communications Preferences
»Profession and Education
»Technical Interests Need Help?

» **US & Canada:** +1 800 678 4333
»**Worldwide:** +1 732 981 0060
» Contact & Support About IEEE *Xplore* | Contact Us | Help | Accessibility | Terms of Use | Nondiscrimination Policy | Sitemap | Privacy & Opting Out of Cookies A not-for-profit organization, IEEE is the world's largest technical professional organization dedicated to advancing technology for the benefit of humanity. © Copyright 2024 IEEE - All rights reserved. Use of this web site signifies your agreement to the terms and conditions.