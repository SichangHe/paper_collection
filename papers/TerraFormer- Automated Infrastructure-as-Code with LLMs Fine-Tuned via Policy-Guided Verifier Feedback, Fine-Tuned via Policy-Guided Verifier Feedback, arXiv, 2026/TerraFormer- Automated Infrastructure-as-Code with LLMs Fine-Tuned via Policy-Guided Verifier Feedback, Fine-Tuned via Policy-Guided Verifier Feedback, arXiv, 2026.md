                                               TerraFormer: Automated Infrastructure-as-Code with LLMs
                                                    Fine-Tuned via Policy-Guided Verifier Feedback
                                                          Prithwish Jana∗                                            Sam Davidson                           Bhavana Bhasker
                                                      pjana7@gatech.edu                                          ssdavid@amazon.com                        Amazon Web Services
                                                 Georgia Institute of Technology                                 Amazon Web Services                          Seattle, USA
                                                          Atlanta, USA                                                Seattle, USA

                                                             Andrey Kan                                              Anoop Deoras                             Laurent Callot
                                                        Amazon Web Services                                      Amazon Web Services                       Amazon Web Services
                                                           Seattle, USA                                             Seattle, USA                              Seattle, USA
arXiv:2601.08734v1 [cs.SE] 13 Jan 2026




                                         Abstract                                                                            1   Introduction
                                         Automating Infrastructure-as-Code (IaC) is challenging, and large                   Cloud computing has become the backbone of modern IT systems,
                                         language models (LLMs) often produce incorrect configurations                       with over 96% of organizations using public cloud services and the
                                         from natural language (NL). We present TerraFormer, a neuro-                        market projected to exceed $940 billion by 2026 [34]. Cloud-native
                                         symbolic framework for IaC generation and mutation that combines                    development involves orchestrating diverse infrastructure compo-
                                         supervised fine-tuning with verifier-guided reinforcement learn-                    nents such as compute, storage, networking, databases, and identity
                                         ing, using formal verification tools to provide feedback on syntax,                 management, across multiple environments. To ensure reproducibil-
                                         deployability, and policy compliance. We curate two large, high-                    ity and support iterative changes, these resources must be provi-
                                         quality NL-to-IaC datasets, TF-Gen (152k instances) and TF-Mutn                     sioned consistently and automatically. As a result, Infrastructure-
                                         (52k instances), via multi-stage verification and iterative LLM self-               as-Code (IaC) [35] has emerged as a core DevOps practice, en-
                                         correction. Evaluations against 17 state-of-the-art LLMs, including                 abling infrastructure to be deployed and managed via high-level,
                                         ∼50× larger models like Sonnet 3.7, DeepSeek-R1, and GPT-4.1,                       machine-readable code (configuration). Broadly, IaC tools fall into
                                         show that TerraFormer improves correctness over its base LLM by                     two categories: configuration management systems (e.g., Puppet,
                                         15.94% on IaC-Eval, 11.65% on TF-Gen (Test), and 19.60% on TF-                      Chef, Ansible) that manage already-provisioned systems’ state,
                                         Mutn (Test). It outperforms larger models on both TF-Gen (Test)                     and infrastructure provisioning frameworks (e.g., CloudFormation,
                                         and TF-Mutn (Test), ranks third on IaC-Eval, and achieves top                       Terraform, Pulumi) that declaratively define, provision, and man-
                                         best-practices and security compliance.                                             age resources. Among these, Terraform [17] is one of the most
                                                                                                                             widely used IaC tools on GitHub, with its declarative HashiCorp
                                         CCS Concepts                                                                        Configuration Language (HCL) experiencing over 30% growth every
                                         • Software and its engineering → Orchestration languages; For-                      year [6, 12]. Backed by a strong community, Terraform’s modular,
                                         mal software verification; • Computing methodologies → Natural                      platform-agnostic definitions and plugin system enable integration
                                         language processing; Reinforcement learning.                                        with major cloud providers like AWS, Azure, and Google Cloud.
                                                                                                                                Although Terraform’s HCL offers a readable, declarative syn-
                                                                                                                             tax, authoring IaC configurations requires deep knowledge of cloud
                                         Keywords
                                                                                                                             provider APIs, provider-specific attributes, and complex inter-resource
                                         Infrastructure as Code (IaC), IaC generation, IaC mutation, Neuro-                  dependencies. Experienced engineers typically spend around 100
                                         symbolic AI, Large language models, Formal Verification                             minutes creating a moderately complex multi-cloud setup [41], and
                                         ACM Reference Format:                                                               human-written configurations often contain critical security vul-
                                         Prithwish Jana, Sam Davidson, Bhavana Bhasker, Andrey Kan, Anoop Deo-               nerabilities [4]. These challenges highlight the need to automate
                                         ras, and Laurent Callot. 2026. TerraFormer: Automated Infrastructure-as-            IaC generation from high-level goals to reduce manual effort and se-
                                         Code with LLMs Fine-Tuned via Policy-Guided Verifier Feedback. In 2026              curity risks. Large language models (LLMs) are well-suited, having
                                         IEEE/ACM 48th International Conference on Software Engineering (ICSE-SEIP           shown strong code generation across benchmarks. Notable exam-
                                         ’26), April 12–18, 2026, Rio de Janeiro, Brazil. ACM, New York, NY, USA,            ples include Claude 3.7 [2], GPT-4.1 [36], DeepSeek-R1 [14], LLaMA-
                                         12 pages. https://doi.org/10.1145/3786583.3786898                                   4 [33], and Qwen-3 [55], which rank highly on HumanEval+ [29],
                                                                                                                             MMLU-Pro [50], Open LLM v2 [10], and Polyglot [1]. However,
                                         ∗ Work carried out while affiliated to Amazon Web Services, Seattle, USA.
                                                                                                                             applying LLMs to IaC automation involves unique challenges.
                                                                                                                                In this paper, we address two fundamental tasks in IaC automa-
                                                                                                                             tion using LLMs, focusing on Terraform and its native language
                                                                                                                             HCL: (a) IaC generation, creating configurations from scratch
                                         This work is licensed under a Creative Commons Attribution-NonCommercial-
                                         NoDerivatives 4.0 International License.
                                                                                                                             given natural language (NL) prompts, and (2) IaC mutation, modi-
                                         ICSE-SEIP ’26, Rio de Janeiro, Brazil                                               fying existing configurations based on NL instructions (Figure 1).
                                         © 2026 Copyright held by the owner/author(s).                                       These use cases pose several challenges that limit the effective-
                                         ACM ISBN 979-8-4007-2426-8/2026/04                                                  ness of current LLMs in the IaC domain. First, there is a lack of
                                         https://doi.org/10.1145/3786583.3786898
ICSE-SEIP ’26, April 12–18, 2026, Rio de Janeiro, Brazil                                                                                                                               Jana et al.


                                                                      terraform {
                                                                        required_providers {                             policy compliance. Using these verifiers, we curate a high-quality
                                                                          docker = {
                                                                            source = "kreuzwerker/docker"
                                                                            version = "2.13.0"                           NL-to-IaC dataset by processing a large collection of erroneous
                                                                          }
                                                                        }
                                                                        required_version = "~> 1.12.0"                   Terraform configurations from open-source repositories through
                                                      𝐍𝐋 → 𝐈𝐚𝐂        }
     Deploy a Docker container with NGINX latest
        image using Terraform that maps a local                       provider "docker" { }
                                                                                                                         multi-stage verification. Crucially, those failing verification enter a
       directory to a container path and forwards
     internal port 8080 to external port 8090 with        LLM
                                                                      resource "docker_image" "nginx" {
                                                                        name         = "nginx:latest"
                                                                                                                         multi-turn repair loop, where an LLM iteratively refines them using
                                                                        keep_locally = true
               automatic restart enabled.                             }
                                                                                                                         verifier-generated error certificates. This self-correction process
       NL Prompt (𝐩𝐫𝐨𝐦𝐩𝐭 𝐍𝐋 )                        IaC Generation   resource "docker_container" "test_cont" {
                                                                        image = docker_image.nginx.latest                yields a large set of verified IaC, from which we derive NL prompts
                                                                        restart = "always"
                                                                        ...
                                                                        ports {
                                                                          internal = 8080
                                                                                                                         and policies that capture infrastructure intent. Though focused
                                                                          external = 8090

                                                                      }
                                                                        }                                                on Terraform, our automated data curation pipeline extends to
          Modify the S3 bucket to enable                               Terraform configuration (𝐭̂)                      other IaC tools (e.g., Pulumi, Ansible, CloudFormation) and general
      force_destroy and enhance security by
        implementing AWS KMS encryption
                                                                                                                         code generation or mutation. We use this dataset to fine-tune open-
     instead of AES256. Add a dedicated KMS                           terraform {

      key with key rotation enabled and a 30-
                                                                      ...
                                                                        required_version = "~> 1.12.0"
                                                                                                                         source LLMs for IaC generation and mutation. We warm-start with
      day deletion window for the S3 bucket                           }

                    encryption.                      𝐍𝐋, 𝐈𝐚𝐂 → 𝐈𝐚𝐂
                                                                      ...
                                                                      resource "aws_s3_bucket_server" "demo" {
                                                                        bucket = aws_s3_bucket.demo.id
                                                                                                                         supervised fine-tuning (SFT), then apply reinforcement learning
      NL Prompt (𝐩𝐫𝐨𝐦𝐩𝐭 𝐦                                                                                                (RL) guided by fine-grained verifier feedback with progressively
                                                                        rule {

                        𝐍𝐋 )
                                                                          apply_server_side_encryption_by_default {
                                                                            sse_algorithm     = "aws:kms"

    terraform {
                                                          LLM             }
                                                                            kms_master_key_id = aws_kms_key.s3_key.arn
                                                                                                                         structured rewards, enabling the LLM to move beyond pattern
    ...                                                                 }
      required_version = "~> 1.12.0"                                  }
    }
                                                                      resource "aws_kms_key" "s3_key" {                  imitation and produce deployable, functionally correct IaC.
                                                      IaC Mutation
    ...
    resource "aws_s3_bucket_server" "demo" {                            description             = "KMS key, S3 encryp"
      bucket = aws_s3_bucket.demo.id                                    deletion_window_in_days = 30


                                                                                                                         Contributions:
      rule {                                                            enable_key_rotation     = true
        apply_server_side_encryption_by_default {                     }
          sse_algorithm = "AES256"                                    ...
        }

    }
      }

    ...                                                               Mutated Terraform config. (𝐭*
                                                                                                  𝐦)                     • We present an automated data curation pipeline leveraging LLMs
   Initial Terraform config. (𝐭 𝐢𝐧𝐢𝐭 )
                                                                                                                           and formal verification to construct large-scale NL-to-IaC datasets:
                                                                                                                           TF-Gen (152,475 generation instances; 330× IaC-Eval [27], 1000×
Figure 1: Learning Objectives. Task definitions for IaC gen-                                                               DPIaC-Eval [57], 150× CloudEval-YAML [54]) and TF-Mutn
eration, i.e., creating Terraform configurations from scratch,                                                             (52,516 mutation instances, the first IaC mutation dataset), both
and IaC mutation, i.e., modifying existing configurations,                                                                 with more complex infrastructures than IaC-Eval. We validate
both taking natural language (NL) prompts as input.                                                                        prompt–IaC–policy semantic alignment and mutation complex-
                                                                                                                           ity via a cloud-expert survey, and curate test sets TF-Gen (Test)
high-quality labeled datasets, hindering model evaluation and the
                                                                                                                           and TF-Mutn (Test) with 704 and 740 instances. (Sections 4, 7)
development of specialized ones. Due to privacy restrictions, real-
                                                                                                                         • We develop a training pipeline to create TerraFormer for IaC gen-
world IaCs are rarely shared, limiting LLMs’ exposure to diverse
                                                                                                                           eration and mutation, fine-tuning Qwen2.5-Coder (3B and 14B)
conventions and usage patterns in production. Second, general-
                                                                                                                           on TF-Gen and TF-Mutn. Following an SFT warm-start, we apply
purpose LLMs struggle to satisfy the strict syntactic and semantic
                                                                                                                           RL with a fine-grained verifier-based reward that incorporates
constraints of formal languages [21, 49] like HCL, frequently pro-
                                                                                                                           syntax, deployability, and policy compliance. (Section 5)
ducing hallucinated or invalid code. This stems from their stochastic
                                                                                                                         • We extensively evaluate TerraFormer against 17 SoTA LLMs,
nature and is compounded by the lack of domain-specific supervi-
                                                                                                                           drawn from six model families (Anthropic, DeepSeek, Llama,
sion. The challenge is amplified in IaC, where tools like Terraform
                                                                                                                           OpenAI, Mistral, Qwen), on IaC generation and mutation, mea-
use a highly declarative, stateful language, and correctness depends
                                                                                                                           suring correctness, deployability, syntactic validity, best practices,
on both syntax and semantic consistency with cloud provider APIs
                                                                                                                           and security compliance. TerraFormer significantly improves cor-
and inter-resource dependencies. Third, IaC mutation poses a dis-
                                                                                                                           rectness over its base LLM (+15.94% on IaC-Eval, +11.65% on
tinct challenge from IaC generation, as it requires LLMs to accu-
                                                                                                                           TF-Gen (Test), +19.60% on TF-Mutn (Test)). It outperforms ≈50×
rately interpret existing infrastructure and make precise updates
                                                                                                                           larger foundation LLMs such as Sonnet 3.7, DeepSeek-R1, and
while preserving critical dependencies. Although a few recent stud-
                                                                                                                           GPT-4.1 on TF-Gen (Test) and TF-Mutn (Test), while achieving
ies [27, 28, 37, 57] have explored NL-to-IaC generation from scratch,
                                                                                                                           third-best performance on IaC-Eval. It also leads in best practices
the task of mutating or incrementally updating existing IaC via
                                                                                                                           and security compliance. (Section 6)
NL prompts (arguably more reflective of real-world development)
remains largely underexplored. Fourth, automated evaluation of
IaC correctness is a major bottleneck. Actual cloud deployment                                                           2   Related Work
is prohibitively slow [40], cannot reliably verify user intent, and                                                      LLM-based IaC Generation for Terraform. Despite Terraform’s
often requires credentials unavailable to the LLM, necessitating                                                         prominence in DevOps, LLM-based NL-to-Terraform generation
manual post-processing. Pre-deployment testing remains an open                                                           remains underexplored, and no prior work has addressed the task
problem [45], so prior IaC research relies on proxies like BLEU,                                                         of mutation. Srivatsa et al. [46] evaluate GPT-3.5-turbo (59% accu-
exact match [46], CodeBERTScore, LLM judges [27], linters [37],                                                          racy) and CodeParrot-110M (8%) on a small, unreleased 49-task AWS
and static analyzers [4]. Without formal verifiers, these provide                                                        benchmark, using exact-match correctness against human-authored
minimal guarantees for deployability or preservation of user intent.                                                     configurations. The challenges of Terraform generation are more
   To address the challenges of reliable IaC generation and muta-                                                        evident on real-world datasets such as IaC-Eval [27], which consists
tion from NL prompts, we present TerraFormer, a neuro-symbolic                                                           of 458 human-curated, AWS-specific examples. To our knowledge,
framework that leverages an LLM fine-tuned with feedback from                                                            it is the only publicly available benchmark for this task. Contempo-
formal verification tools. We employ a comprehensive suite of veri-                                                      rary LLMs perform poorly on IaC-Eval; the best-performing model,
fiers that assess Terraform IaC for compilability, deployability, and                                                    GPT-4, achieves under 20% pass@1 accuracy. This aligns with Grant
TerraFormer: Automated Infrastructure-as-Code with LLMs Fine-Tuned via Policy-Guided Verifier Feedback            ICSE-SEIP ’26, April 12–18, 2026, Rio de Janeiro, Brazil


[13], who reports that SoTA LLMs struggle with Terraform synthe-
sis, often hallucinating resource types and attribute names due to
the relative scarcity of Terraform’s HCL in LLM training data.
LLM-based IaC Generation in Popular Formats (YAML/JSON).
In contrast to Terraform, LLMs perform better on IaC tools that use
widely adopted general-purpose data formats like YAML and JSON,
such as Ansible, Kubernetes, and AWS CloudFormation, owing to
their fewer syntactic elements and greater presence in training
data [13]. For instance, Pujar et al. [39] pre-trained CodeGen-350M-
Multi on YAMLs from BigQuery and fine-tuned it on Ansible Galaxy                       Figure 2: Terraform Example. IaC with 2 providers (AWS,
data, raising functional correctness from 54.5% (few-shot) to 70.8%,                   Docker) and 2 resources (S3, container) with a dependency.
though evaluation was limited by a 1024-token context. Xu et al.                      [FV-iii] opa eval: We express infrastructure intent as machine-verifiable
[54] benchmarked 13 models on CloudEval-YAML for 1011 NL-to-                                   policies in Rego [47], a declarative language for specifying
Kubernetes tasks, with GPT-4-Turbo at 56.7% functional correctness                             rules over structured data like execution DAGs. A Rego pol-
and LLaMA-2-70B-Chat leading among open-source models at 8.9%.                                 icy acts as a unit-test for the DAG from FV-ii. Given this DAG
On DPIaC-Eval [57], Claude-3.5 achieved 30.2% deployment success                               and a policy, the oracle checks policy compliance, verifying
on 153 NL-to-CloudFormation tasks, rising to 95.5% with 15 rounds                              conformance with user intent, security best practices, orga-
of human feedback. Yet such feedback is often noisy and unreliable,                            nizational standards, and regulatory constraints. This adds a
yielding just 25.2% intent satisfaction and poor security compliance.                          formal verification layer beyond syntax and deployability.
Neuro-Symbolic Code Generation. Prior works on LLM-based                               Crucially, FV-i, FV-ii, and FV-iii produce detailed error certificates upon
formal language generation, such as code or proofs, leveraged sym-                     failure, aiding diagnosis and debugging. Leveraging these certifi-
bolic feedback from compilers [8, 30], static analysis [22], and for-                  cates, we apply the oracles for two purposes. First, we construct
mal reasoning systems like LEAN [23, 53], typically via RL. How-                       large-scale verified datasets (TF-Gen, TF-Mutn) by passing config-
ever, in data-scarce domains like Terraform IaC, existing methods                      urations through the oracles, enabling a leading commercial-scale
rely on zero- or few-shot prompting without domain-specific su-                        LLM to iteratively repair errors via inference-time feedback. Second,
pervision [7]. This gap stems from a lack of high-quality data and                     we use these oracles in RL-based fine-tuning of open-source LLMs,
effective feedback; cloud deployments provide only Boolean signals,                    where the error certificates are converted into fine-grained reward
yielding sparse and inefficient rewards [24], and are slow. While                      signals to guide learning. In the following sections, we address two
linters improve NL-to-CloudFormation generation [37], LLMs still                       core learning objectives (Figure 1) in IaC automation using LLMs,
struggle with errors and introduce new ones, exposing their hallu-                     with a focus on Terraform and its native declarative language, HCL:
cination tendencies and the limitations of linters as weak verifiers.                      IaC Generation as a Learning Problem. Given an NL prompt
                                                                                       (prompt NL ), the goal is to generate a Terraform configuration (𝑡ˆ) by
3    Preliminaries and Problem Formulation                                             learning a function 𝑓gen (prompt NL ) ↦→ 𝑡ˆ such that 𝑡ˆ is (a) compilable,
Terraform configurations are written in HCL, a declarative domain-                     (b) deployable, and (c) aligned with the intent of prompt NL .
 specific language (DSL) for specifying infrastructure state via blocks.                   IaC Mutation as a Learning Problem. Given an existing Ter-
 Key block types include provider (e.g., aws, azurerm, google) for                     raform configuration (𝑡 init ) and an NL prompt (prompt m     NL ), the goal
 target clouds and resource (e.g., aws_s3_bucket) for infrastructure                                                                                             init ,
                                                                                                                                                         mutn (𝑡
                                                                                       is to generate an updated configuration (𝑡c     m ) by learning 𝑓
 components. Terraform supports complex multi-provider, multi-                                   m
                                                                                       prompt NL ) ↦→ 𝑡 such that 𝑡 is (a) compilable, (b) deployable, and
                                                                                                         m
                                                                                                         c               cm
 resource setups, allowing cross-cloud deployments. Inter-resource                     (c) faithful to the modification intent of prompt m    NL .
 relations are expressed implicitly via references (e.g., a resource
 using another’s attributes) or explicitly with depends_on, to guide                   4    TF-Gen and TF-Mutn: A Systematic Dataset
 execution order. Figure 2 shows a Terraform configuration example.
We define three formal verification oracles for Terraform: FV-i checks
                                                                                            Curation Pipeline with LLMs and Verification
 compilability (syntactic correctness), FV-ii verifies deployability (se-              We present an automated pipeline for constructing datasets for
 mantic validity), and FV-iii ensures correctness (policy compliance). FV-             formal language (e.g., code) generation and mutation tasks based on
 i and FV-ii are implemented via Terraform commands from HashiCorp                     NL prompts. Using this framework, we create two comprehensive
 [17] whereas, FV-iii is implemented by Open Policy Agent (OPA) [47].                  datasets: TF-Gen and TF-Mutn, for training and evaluating LLMs
 Note that each stage is strictly stronger than the previous: correct-                 on IaC Generation and IaC Mutation tasks respectively. In both
 ness requires deployability, which requires compilability.                            datasets, each infrastructure scenario includes a target Terraform
 [FV-i] terraform validate: Given a Terraform configuration, it                        configuration that is verified as deployable, along with an FL policy
        performs static checks for syntax and structural consistency.                  that the target configuration satisfies. The FL policy acts as a unit-
        It ensures required fields and references are correctly defined,               test (or verifier function), enabling reliable, automated evaluation
        catching errors early before involving external systems.                       of LLM-generated IaC. We summarize both datasets below:
[FV-ii] terraform plan: Given a configuration, it generates an ex-                     • TF-Gen includes 152,475 infrastructure scenarios, each structured
        ecution DAG simulating deployment. It assesses semantic                           as a triplet {prompt NL, 𝑡, policy FL }, comprising: (i) an NL prompt,
        correctness and runtime feasibility by validating provider com-                  (ii) a target Terraform configuration, and (iii) a FL policy codifying
        patibility, resource dependencies, and runtime constraints.                       the constraints expected to hold in the target configuration.
ICSE-SEIP ’26, April 12–18, 2026, Rio de Janeiro, Brazil                                                                                                                                                                                             Jana et al.


                                                                                                                                                                                LLM Judge                                     Open Policy
            : AI Model for Repair or Generation
                                                                                                                                                                                                                              Agent (OPA)
                                                                                                                                                                                LLM
            : Strong Formal Verification Oracle                        Error Certificate                     Error Certificate                                   Issues                            Error Certificate
                                                                                       Multi-Turn                            Multi-Turn
            : Weak Verification Engine                                                Repair Loop                           Repair Loop                                 Multi-Turn
                                                                                                                                                                                                                Multi-Turn
                                                                                                                                                                       Repair Loop
                                                                            LLM                                     LLM                                                                                        Repair Loop

                                              main.tf
                                                        infra-1.tf

                                         providers.tf                                                                                                                                                                                        SEEDCORPUS
                                                                        terraform                              terraform                                                             Prompt in
                               main.tf
                                                                         validate                                 plan                                           LLM                  Natural
                                                                                                                                                                                     Language
                               identity.tf
                                                        infra-2.tf
                                                                                                                                                                                       (NL)
                                                                                                                                                                                                                                  Policy
                               variables.tf                                                                                                                                                                                     in Formal
                                                                                                                                                                                                                                Language
                                                                                                                                                                                                                                   (FL)
                                                                                                                                                                                                                                              promptNL ,
                                                                                                                                                                                                        LLM                                      t,
                                                        infra-N.tf
                                                                                                                                                                                                                                               policyFL


                            STEP-1:                                                STEP-2:                                  STEP-3:                                     STEP-4:                                STEP-5:
                        Data Collection                                    Cloud Provider Filtering,                 Deployability Validation                     NL Prompt Generation                   FL Policy (Unit-Test)
                                                                           Syntax Correction, and                        and Correction                                                                      Generation
                                                                                Deduplication




                                                                                               (a) Pipeline to construct the SeedCorpus

    CONFIGURATION                                                                                                                   CONFIGURATION
      CLONING:                                                                                                                        MUTATION:
                               𝒄
                              𝒕 ⊢ policyFL                                                                                                                                            𝒎
                                                                                                                                                                          𝒕𝒎 ⊢ policyFL                                                             prompt NL  𝒎
                                                                                                                                                                                                                                                                 ,
                               & 𝒕𝒄 ≠ t ?                                                                                                                                  𝒎
                                                                                                                                                                  & policyFL          𝒊𝒏𝒊𝒕
                                                                                                                                                                             ≠ policyFL    ?                                                           𝒕𝒊𝒏𝒊𝒕 ,
                                                                                                    promptNL ,t , policyFL ,                                                                                                                             𝒎,
                                                                                                                                                                                                                                                        𝒕
                                                    Multi-Turn       terraform
                                                                        plan
                                                                                 Open Policy
                                                                                 Agent (OPA)
                                                                                                    promptNL , 𝒕𝒄 , policyFL                                                                                                                        policyFL𝒊𝒏𝒊𝒕
                                                                                                                                                                                                                                                                   ,
                                                                                                                                                                                                                                                               𝒎
                                                     Repair                                                                                                                                        terraform    Open Policy      LLM Judge           policyFL
                  Error Certificate                                                                                                                                                   Multi-Turn      plan      Agent (OPA)
                                                      Loop                                             TF-GEN                                                                          Repair                                    LLM
                                                                                                                                                           Error Certificate                                                                   TF-MUTN
                                         LLM
                                                              𝒕𝒄                                                                                                                        Loop
                                                                                                                                                promptNL ,
           promptNL ,
                                                                                                                                                   𝒕𝒊𝒏𝒊𝒕 ,
              t,                                                                 policyFL                                                        policyFL 𝒊𝒏𝒊𝒕                 LLM
            policyFL
                                                                                                                                                                                                                 𝒎          𝒎
                                                                                                                                       SEEDCORPUS                                                    (𝒕𝒎, policyFL , prompt NL )
     SEEDCORPUS
           (b) Curation of TF-Gen dataset from SeedCorpus                                                                                       (c) Curation of TF-Mutn dataset from SeedCorpus
Figure 3: Dataset Curation Pipeline. (a) Multi-turn repair loops with LLMs and verifiers produce verified Terraform configu-
rations, NL prompts, and FL policies. (b) TF-Gen extends SeedCorpus by cloning triplets to produce multiple implementations
for an infrastructure. (c) TF-Mutn augments SeedCorpus with mutated configurations, mutation prompts, and FL policies.
• TF-Mutn includes 52,516 infrastructure scenarios, each repre-                                                                      code generation and mutation datasets. It involves simply swapping
   sented as a quintuplet {prompt m       init , 𝑡 m , policy init , policy m }, con-                                                language-specific components, provided the target language has
                                   NL , 𝑡                     FL            FL
   sisting of: (i) an NL prompt, (ii) an initial Terraform configura-                                                                the notion of syntactic validity, semantic correctness, and testability.
   tion, (iii) a modified configuration (target) that implements the                                                                 Moreover, the pipeline can accommodate future versions of Ter-
   changes, and (iv-v) the initial and target FL policies.                                                                           raform by updating the associated formal verification oracles (listed
Table 1 presents a statistical comparison with IaC-Eval [27], which                                                                  in Section 3). Essentially, our pipeline relies on three key compo-
to our knowledge is the only benchmark for NL-to-Terraform gener-                                                                    nents: (a) an initial corpus of code in the target language, possibly
ation (458 instances). Our proposed TF-Gen dataset is ∼330× larger                                                                   containing errors; (b) a general-purpose LLM capable of reasoning
and rigorously validated using formal verification tools. It also far                                                                about and generating code in that language; and (c) syntax-aware
surpasses datasets for other IaC tools, being 1000× larger than                                                                      compilers and formal verifiers that validate code both structurally
DPIaC-Eval [57] for AWS CloudFormation and 150× CloudEval-                                                                           and semantically, including against test cases.
YAML [54] for Kubernetes. For IaC mutation task, TF-Mutn is the                                                                         Stage-Wise Multi-Turn Repair Loops: Our pipeline for curating
first dataset of its kind. Our datasets feature more complex infras-                                                                 SeedCorpus (Figure 3a) forms the basis of TF-Gen (Figure 3b)
tructure scenarios than IaC-Eval, with more providers, resources,                                                                    and TF-Mutn (Figure 3c). Starting with an initial collection of
and longer configurations on average (Table 1). An expert survey                                                                     Terraform configurations (step-1), many with errors, we verify them
(Section 7) on a subset of TF-Gen and TF-Mutn confirms overall                                                                       through three increasingly stringent stages: compilability (step-
quality. Together, we believe that the scale, complexity, and verifi-                                                                2), deployability (step-3), and policy compliance (step-5). Crucially,
cation rigor of TF-Gen and TF-Mutn provide a strong foundation                                                                       verification is not used solely for filtering. At each stage, failed
for advancing research in LLM-based IaC generation and mutation.                                                                     configurations enter an automated multi-turn repair loop, where
    Modular, Extensible Dataset Curation Pipeline. While our dataset                                                                 the verifier’s diagnostic report (error certificate) and the current
curation pipeline is implemented for Terraform, it is readily adapt-                                                                 configuration are given as in-context input to an LLM for revision
able to other IaC tools (e.g., Pulumi, Ansible) and general-purpose                                                                  (see prompt template in Appendix B). The loop runs up to five
programming languages [20] (e.g., C++, Python) for curating similar                                                                  turns, with the verifier rechecking each revision and issuing an
TerraFormer: Automated Infrastructure-as-Code with LLMs Fine-Tuned via Policy-Guided Verifier Feedback                        ICSE-SEIP ’26, April 12–18, 2026, Rio de Janeiro, Brazil

Table 1: Statistics for TF-Gen and TF-Mutn. Datasets of IaC configurations in Terraform, showing min/median/max counts
of providers, resources, configuration size (lines), and prompt length (words). IaC-Eval is included for comparison.
                                                                          # Instances                Terraform Configuration Stats                 NL Prompt Stats
                                                           # Source
                 Dataset               Task        Split    Github       Total %with       # Providers        # Resources        # Lines of Code    Length (words)
                                                            Repos.             policy
                                                                                         Min Med Max         Min Med Max       Min Med      Max    Min Med      Max

                 IaC-Eval [27]    IaC Generation   Full        N/A         458   100%     0      1       4    0     3   27        3    30   294       3   17    215
                                                   Train     27,980    151,771    83%     0      1    35      0     4   199       1   111 4,496     10    44    134
                 TF-Gen (Ours)    IaC Generation
                                                   Test         704        704   100%     0      1     3      0     6    44       1   138 814       10    46    105
                                                   Train     19,427     51,776   100%     0      1    18      0     4   59        1   107   934     14    63    229
                 TF-Mutn (Ours)    IaC Mutation
                                                   Test         740        740   100%     0      1     5      0     5   41        1   134   704     18    66    190

updated certificate, so both evolve together as feedback guides                               an LLM judge compares the prompt to the Terraform code, pro-
repairs toward the stage’s verification criteria. We use a leading                            vides structured feedback, and guides revisions until alignment
commercial-scale foundation LLM that demonstrates strong zero-                                is achieved. We provide prompts at three levels of abstraction: (i)
shot IaC performance and can reason over in-context feedback.                                 high-level (broad overview), (ii) mid-level (moderate detail), and (iii)
    Data Collection. We start with TerraDS [4], a large corpus of                             low-level (closely aligned with the configuration). Our mid-level
real-world Terraform configurations in HCL, collected from 62,406                             prompts balance abstraction and detail to closely match human
GitHub repositories under permissive licenses. Each repository con-                           instructions, and thus we use them for all subsequent tasks.
tains one or more modules, defined as subdirectories with at least                                Formal Language Policy (Unit-Test) Generation. For each
one .tf file. As HCL is declarative, we concatenate all .tf files                             deployable Terraform configuration and its NL prompt, we ask the
within each module into a single configuration, yielding 279,410                              LLM to generate an FL policy2 in Rego that captures the prompt’s
unified configurations. But, TerraDS lacks built-in validation, and                           intent. The FL policy acts as a verification mechanism for the in-
analysis using Checkov [3] revealed widespread misconfigurations                              frastructure. We validate each configuration against the gener-
and security issues [4]. These raise concerns about the reliability                           ated policy using FV-iii (Section 3) and apply a multi-turn repair
of using such unverified configurations for training or evaluating                            loop to iteratively refine policies that fail validation. From 89,843
LLMs. To address this, we apply formal verification oracles to pro-                           configuration-prompt pairs, we generate valid policies for ∼71%,
gressively validate and repair configurations, then augment them                              yielding 63,576 triplets {prompt NL, 𝑡, policy FL }.
with NL prompts and FL policies, as detailed below.                                               TF-Gen Construction. Since any prompt NL is inherently am-
    Cloud Provider Filtering, Syntax Correction, and Dedupli-                                 biguous, it can yield multiple configuration variants (clones) that are
cation. Our cloud-agnostic pipeline supports all major providers,                             semantically equivalent modulo policy FL . To capture this diversity,
including AWS, Azure, and Google Cloud. In this work, we fo-                                  we extend each triplet {prompt NL, 𝑡, policy FL } in SeedCorpus, by
cus on AWS due to its wide adoption [48] and abundance of well-                               prompting the LLM to generate a configuration clone 𝑡 𝑐 . We apply
documented public configurations. We retain those using AWS and                               our multi-turn repair loop to 𝑡 𝑐 , using FV-ii and FV-iii (Section 3) to
other HashiCorp-supported utility providers (random, null, local,                             verify that it is deployable, satisfies policy FL , and is distinct from
template, tls, time, external, http, archive, docker, terraform), yielding                    𝑡 (Figure 3b). We generate at most one clone per configuration,
117,520 configurations (42% of the step-1 corpus). Syntax validation                          resulting in 153,175 IaC generation tasks in TF-Gen.
is then applied via our multi-turn repair loop using FV-i (Section 3)                             TF-Mutn Construction. For {prompt NL, 𝑡 init, policy init             FL } in Seed-
as verifier. To handle variables requiring user input, the LLM inserts                        Corpus, we prompt the LLM to produce a mutated configuration
plausible defaults during repair. This yields 101,751 syntax-validated                        𝑡 m , an updated policy (policy mFL ) and an NL prompt (prompt NL ) de-
                                                                                                                                                                              m

configurations, 58% repaired and the rest passing unchanged. After                            scribing the mutation. Mutations alter or add resources, providers,
deduplication, we retain 97,645 unique configurations.                                        or variables, while keeping all artifacts consistent. A multi-turn
    Deployability Validation and Correction. We next evaluate                                 repair loop with FV-ii and FV-iii ensures 𝑡 m is deployable and satisfies
each syntax-validated configuration for deployability using FV-ii as                          policy m                               m                              init
                                                                                                      FL , while confirming policy FL differs from policy FL (Figure 3c).
the verifier, which checks for semantic correctness. Configurations                           The loop also checks prompt faithfulness via an LLM judge. We
failing this check undergo iterative fixes via the multi-turn repair                          generate at most one mutation per SeedCorpus instance, yielding
loop guided by error certificates from FV-ii; those still failing after                       52,516 quintuplets {prompt m          init , 𝑡 m , policy init , policy m }.
                                                                                                                             NL , 𝑡                     FL            FL
these attempts are discarded. This stage yields 89,843 deployable                                 Train/Test Splits. To ensure out-of-distribution evaluation, we
configurations, with ∼59% recovered through automated repair.                                 create test splits for both TF-Gen and TF-Mutn by randomly se-
    NL Prompt Generation. Next, we invoke the LLM to generate                                 lecting instances that are traced back (during the Data Collection
NL prompts that allow for faithful reconstruction of each configu-                            step) to GitHub repositories containing exactly one module. This
ration. The LLM is instructed to begin each prompt with directive                             prevents related modules from the same repository appearing in
verbs (e.g., Generate, Set up, Deploy) and adopt a concise, goal-                             both training and test sets, avoiding data leakage and enabling eval-
oriented tone that emphasizes what to provision rather than how.                              uation on unseen module contexts. Table 1 summarizes the dataset
Prompt quality is refined1 via a multi-turn repair loop in which                              statistics for these splits.
                                                                                              2 LLMs generating test cases from code is an active research area [5, 42, 56]. To avoid
1 Determining whether an NL description is equivalent to a formal language (FL) object        trivial policies, we prompt the LLM to generate rule sets that cover all configuration
is generally undecidable. However, generating NL from FL (informalization) is usually         elements in the NL prompt. An expert survey (Section 7) confirms that the resulting
tractable and sufficiently accurate [25] as FL objects contain rich semantic detail.          multi-rule policies offer meaningful verification of each infrastructure scenario.
ICSE-SEIP ’26, April 12–18, 2026, Rio de Janeiro, Brazil                                                                                                                                                         Jana et al.


                                                                                                                                     satisfies the policy and that semantic alignment between the prompt
                         𝐩𝐫𝐨𝐦𝐩𝐭 𝐍𝐋                    SFT            𝐭̂                               𝐭
                                                                                                                                     and its policy is validated via an LLM judge (Section 4) and a cloud-
                                                                                  Cross-
                             or                                                   Entropy                                            expert survey (Section 7); this verifier is then used to compute a
                                                      LLM                          Loss
                    𝐩𝐫𝐨𝐦𝐩𝐭 𝐦
                           𝐍𝐋 , 𝐭
                                  𝐢𝐧𝐢𝐭
                                                                   𝐭#
                                                                    𝐦                               𝐭𝐦                               fine-grained reward. In the RL setting for IaC generation, the LLM
                            Input                               Generated                        Target
                                                                                                                                     acts as a policy 𝜋𝜃 , taking prompt NL as input and producing a con-
                                                             Terraform config.             Terraform config.                         figuration 𝑡ˆ as an action. This action is evaluated by verifiers FV-i,
(a) SFT via cross-entropy loss of generated and target configurations                                                                FV-ii, and FV-iii (Section 3) to compute a fine-grained reward ∈ [0, 2]:

                                                                                                             Reward
                                                                                                                                                                  1 + # rules of policy FL passed , deployable,
                                                                                                                                                                        # total rules in policy FL
                                                                                                                                                                 
                                                                                                            Function
                                                                                                                                                                 
                                                                                                                                                                 
                                                                                                                                                                 
                                                                                                                                                                 
                                                                                         is_compilable
                                                                                         is_deployable
                                                                                                                                             𝑟 (𝑡ˆ, policy FL ) = 0.5,                               compilable, (2)
                                                                                         is_valid_configuration                                                  
                                                                                             ├─ is_valid_vpc                                                     
                                                                                             ├─ is_valid_subnet
                                                                                             ├─ is_valid_security_group
                                                                                             ...
                                                                                                                                                                  0,
                                                                                                                                                                 
                                                                                                                                                                                                     otherwise.
                                                                                             ├─ is_valid_key_pair
                                                                             Error           └─ is_valid_private_key
                                                                                                                                                                 
                                                                          Certificates
                                                                                                                                     Illustrated in Figure 4b, we fine-tune the LLM via Group Relative
      𝐩𝐫𝐨𝐦𝐩𝐭 𝐍𝐋             GRPO            𝐭̂                                                                            𝐩𝐨𝐥𝐢𝐜𝐲𝐅𝐋   Policy Optimization (GRPO) [44] using the fine-grained verifier
                                                            terraform         terraform              Open Policy
                                                             validate            plan                Agent (OPA)
           or                                                                                                                        reward, with a KL-divergence penalty [38], as follows:
                             LLM
    𝐩𝐫𝐨𝐦𝐩𝐭 𝐦
           𝐍𝐋 , 𝐭
                  𝐢𝐧𝐢𝐭
                                           𝐭#
                                            𝐦                                                                                   𝐦
                                                                                                                          𝐩𝐨𝐥𝐢𝐜𝐲𝐅𝐋                                        h                                           i
                                                                                                                                                  = E𝑡ˆ∼𝜋𝜃 (· |prompt NL ) 𝜋 𝜋𝜃 (𝑡(|prompt NL )
                                                                                                                                                                                  ˆ
         Input                           Generated                                                                         Target          LGRPO
                                                                                                                                             𝜃
                                                                                                                                                                                                  𝑟 (𝑡,policy
                                                                                                                                                                                                     ˆ        FL ) −𝑏
                                                                                                                                                                            𝜃 SFT 𝑡ˆ |prompt NL )
                                  Terraform configuration                                                                  Policy                                                                                        (3)
                                                                                                                                                     − 𝛽 × KL 𝜋𝜃 ∥ 𝜋𝜃 SFT ,
                                                                                                                                                                                
    (b) RL via fine-grained verifier feedback from FV-i, FV-ii, and FV-iii
Figure 4: Learning Objectives. Instruction-tuning LLMs                                                                               where 𝜋𝜃 is the current policy, 𝜋𝜃 SFT the SFT reference, 𝑟 (𝑡ˆ, policy FL )
for the tasks of IaC generation and mutation via SFT and RL                                                                          the fine-grained verifier reward (Eq. 2), 𝑏 the group-relative baseline,
                                                                                                                                     𝛽 the KL penalty coefficient, and KL(𝜋𝜃 ∥ 𝜋𝜃 SFT ) regularizes the pol-
5       Fine-Tuning Methodology                                                                                                      icy toward the SFT model. The verifier feedback in Eq. 2 produces a
Supervised Fine-Tuning (SFT). For IaC generation, the LLM takes                                                                      gradual progression of reward, encouraging the model to iteratively
prompt NL as input and outputs configuration 𝑡ˆ. For SFT, it is trained                                                              generate better configurations through training, from syntactic cor-
to minimize the cross-entropy loss between 𝑡ˆ and target 𝑡 (Figure 4a):                                                              rectness to deployability, and ultimately to functional correctness.
                                                                                                                                     For the IaC mutation task, the LLM takes ⟨prompt m    NL , 𝑡
                                                                                                                                                                                                  init ⟩ as input

                                                 𝑇    |𝑉 |                                                                           and outputs a mutated configuration 𝑡c     𝑚 , on which 𝑟 (𝑡c 𝑚 , policy m )
                                         1 ∑︁ ∑︁                                                                                                                                                              FL
                 LCE
                  𝜃
                     (𝑡, 𝑡ˆ) = −                 1𝑡 𝑗 =𝑉𝑘 × log 𝑃𝜃 (𝑡ˆ𝑗 = 𝑉𝑘 )                                                (1)    is computed. Crucially, the model is rewarded for syntactic correct-
                                         𝑇 𝑗=1
                                                     𝑘=1                                                                             ness, deployability, and the extent of functional correctness, rather
where 𝜃 are the trainable parameters, 𝑇 is the maximum tokenized                                                                     than for textual similarity to a finite set of target configurations.
length of 𝑡 and 𝑡ˆ, 𝑉 is the vocabulary, 1𝑡 𝑗 =𝑉𝑘 equals 1 if the 𝑗 th token
of 𝑡 is the 𝑘 th token in 𝑉 and 0 otherwise, and 𝑃𝜃 (𝑡ˆ𝑗 = 𝑉𝑘 ) is the                                                               6    Experimental Results
probability that the model predicts the 𝑘 th token of 𝑉 at position 𝑗 in                                                             We evaluate a diverse suite of LLMs across two tasks: IaC generation
𝑡ˆ. For the IaC mutation task, the LLM takes ⟨prompt m   NL , 𝑡
                                                                init ⟩ as input
                                                                                                                                     and IaC mutation. For IaC generation (Table 2), we use the IaC-Eval
and outputs a mutated configuration 𝑡 , minimizing L𝐶𝐸
                                          c𝑚                      𝜃 (𝑡 𝑚 , 𝑡c
                                                                            𝑚 ).                                                     dataset [27], which contains 458 instances, as well as our TF-Gen
     We ensure that SFT is effective for IaC generation and mutation                                                                 (Test) dataset with 704 instances. For IaC mutation (Table 3), evalua-
as follows. First, in Section 4, all target Terraform configurations                                                                 tion is performed on our TF-Mutn (Test) dataset, which comprises
in TF-Gen and TF-Mutn are verified as syntactically correct and                                                                      740 instances. Dataset statistics are summarized in Table 1, with
deployable, and semantic alignment between each prompt and its                                                                       reproducibility details in Appendix A.
target is checked using an LLM judge. This alignment is confirmed                                                                       State-of-the-art (SoTA) Baselines. As noted in Section 2, there
via a cloud-expert survey on a sample set (Section 7), ensuring a                                                                    are currently no LLMs or tools specifically tailored for Terraform
high-quality training dataset. Second, through cloning, TF-Gen                                                                       IaC. To fill this gap, our evaluation covers 17 LLMs across four cate-
includes multiple diverse configurations for the same NL prompt,                                                                     gories: (i) large-scale foundation models with over 100B param-
capturing the many valid ways to realize an infrastructure. All                                                                      eters: Claude Sonnet 3.7 [2], DeepSeek-R1 [14], and GPT-4.1 [36].
variants are formally verified to be equivalent modulo a policy that                                                                 We exclude Gemini [11] due to subscription restrictions and its
encodes the prompt’s infrastructure intent. This design enables the                                                                  low Terraform performance (11.96%) on IaC-Eval reported by Kon
LLM to learn robust mappings from high-level prompts to valid,                                                                       et al. [27], below GPT-3.5-turbo. (ii) distilled variants of founda-
deployable configurations across a broad solution space.                                                                             tion models on smaller backbone LLMs, including DeepSeek-
     Reinforcement Learning (RL) via Policy-Guided Verifier                                                                          R1-Distill-Llama-70B, DeepSeek-R1-0528-Qwen3-8B, DeepSeek-R1-
Feedback. Even with a high-quality dataset and increasing di-                                                                        Distill-Llama-8B [14], evaluated alongside their backbones Llama-
versity through configuration cloning, SFT remains limited by its                                                                    3.3-70B-Instruct [32], Qwen3-8B [55] and Llama-3.1-8B [9]; (iii)
reliance on pattern imitation. To address this, we apply RL after                                                                    instruction-tuned LLMs across varying sizes, such as Llama-3.3-
an SFT warm-start. Training examples in TF-Gen (Train) and TF-                                                                       70B-Instruct [32], Llama-3.2-Instruct (11B and 3B) [31], and Mistral-
Mutn (Train) have an associated target policy, making it suitable                                                                    7B-Instruct [26]; and (iv) code-specialized instruction-tuned
for RL-based fine-tuning. We ensure that this policy serves as a                                                                     LLMs, including DeepSeek-Coder-33B-Instruct [15], Qwen2.5-Coder
reliable verifier function by checking that the target configuration                                                                 (14B and 3B) [19], and CodeLlama-13B-Instruct [43]. All models
TerraFormer: Automated Infrastructure-as-Code with LLMs Fine-Tuned via Policy-Guided Verifier Feedback                                                      ICSE-SEIP ’26, April 12–18, 2026, Rio de Janeiro, Brazil

Table 2: Evaluation of IaC Generation. Comparison of SoTA LLMs and TerraFormer on IaC-Eval and TF-Gen (Test).
TerraFormer* and TerraFormer† are fine-tuned from Qwen2.5-Coder-3B (*) and -14B (†), respectively. Reported improvements
(in parentheses) are relative to these base models. Bold and underline denote the best and second-best performance per column.
                  Tool/LLM                                                       Evaluation on IaC-Eval                                                                 Evaluation on TF-Gen (Test)
                                             Correctness       Deployability        Compilability        Linter          Security        Correctness      Deployability     Compilability        Linter          Security
Method    Model                     #Params.     (%)                (%)                 (%)           Pass Rate (%)    Compliance (%)        (%)               (%)              (%)           Pass Rate (%)    Compliance (%)
          Claude Sonnet 3.7           UNK        35.37              70.09               76.64             99.34             67.22            16.90            78.69             85.23             99.86             55.49
          DeepSeek(DS)-R1             671B       33.84              72.27               75.55             99.13             63.67            11.65            61.93             79.69             98.72             53.41
          OpenAI GPT 4.1              UNK        25.98              56.99               59.17            100.00             62.87            10.37            51.99             61.36             99.86             52.79
          Llama-3.3-70B-Instruct      70B        20.96              50.00               51.75            100.00             66.59            7.95             40.63             49.43             98.15             53.50
          DS-R1-Distill-Llama-70B     70B        13.54              32.31               35.59             99.34             61.22            7.10             23.86             31.53             99.43             53.84
          DS-Coder-33B-Instruct       33B        14.63              40.39               42.14             70.52             40.22            7.10             34.38             44.46             76.99             39.00
Few-shot                     †
inference Qwen2.5-Coder-14B           14B        15.50              42.58               43.89             96.94             58.89            6.39             30.54             40.20             93.32             48.24
of SoTA   Qwen3-14B                   14B        11.14              25.98               30.35             99.78             57.23            5.97             29.12             38.78             99.86             52.64
LLMs      CodeLlama-13B-Instruct      13B         0.22               7.64               36.03             96.29             36.14            3.55             20.17             33.95             93.61             44.44
          Llama-3.2-11B-Instruct      11B         8.08              31.44               35.37             98.03             59.53            5.54             23.44             29.97             96.16             50.64
          Qwen3-8B                    8B          4.80              14.63               18.12             98.91             52.42            4.97             17.47             23.01             98.01             49.98
          DS-R1-0528-Qwen3-8B         8B          1.97              5.46                11.57             75.76             40.98            2.27             4.97               9.52             81.82             48.59
          Llama-3.1-8B                8B          1.97              12.23               31.00             99.13             46.27            5.26             19.74             29.55             95.74             49.52
          DS-R1-Distill-Llama-8B      8B          0.22              0.87                 1.53             80.79             47.27            0.57             0.99               1.14             94.60             60.64
          Mistral-7B-Instruct         7B          3.06              8.30                10.26             97.38             60.88            2.70             5.11               6.68             95.03             65.68
          Qwen2.5-Coder-3B*           3B          6.55              18.78               20.96             97.38             57.39            4.55             18.18             20.45             94.89             48.14
          Llama-3.2-3B-Instruct       3B          1.53              5.68                10.26             89.30             62.44            2.41             6.82               9.80            100.00             56.33
         TerraFormer* (SFT)           3B      12.45 (+5.90)     36.96 (+21.18)       43.23 (+22.27)   100.00 (+2.62)     62.12 (+4.73)    8.95 (+4.40)     40.62 (+22.44)    44.89 (+24.44)   100.00 (+5.11)     61.79 (+13.65)
Our      TerraFormer* (SFT+RL)        3B      19.43 (+12.88)    44.10 (+25.32)       48.03 (+27.07)   100.00 (+2.62)     64.29 (+6.90)   10.51 (+5.96)     49.01 (+30.83)    53.13 (+32.68)   100.00 (+5.11)     62.98 (+14.84)
approach TerraFormer† (SFT)           14B     24.23 (+8.73)     56.99 (+14.41)       60.70 (+16.81)   100.00 (+3.06)     65.00 (+6.11)    11.93 (+5.54)    56.96 (+26.42)    61.08 (+20.88)   100.00 (+6.68)     58.11 (+9.87)
         TerraFormer† (SFT+RL)        14B     31.44 (+15.94)    72.93 (+30.35)       75.11 (+31.22)   100.00 (+3.06)    69.34 (+10.45)   18.04 (+11.65)    70.17 (+39.63)    79.97 (+39.77)   100.00 (+6.68)    66.98 (+18.74)


are evaluated on few-shot inference, each given three in-context                                                       deployment. (iii) Correctness, the strictest of the three, demands
examples for IaC generation or mutation (prompts in Appendix B).                                                       both syntactic and semantic validity, additionally ensuring the con-
Overall, models evaluated span 3B-671B parameters. Sonnet 3.7,                                                         figuration is functionally correct modulo a policy encoding the
DeepSeek-R1, and Mistral models were run via Amazon Bedrock,                                                           prompt’s infrastructure intent. These are evaluated using verifiers
GPT-4.1 via the OpenAI API, and other models from Huggingface                                                          FV-i, FV-ii, and FV-iii (Section 3), with a Boolean pass/fail outcome. (iv)
were hosted on a server with 8×40GB NVIDIA A100 GPUs.                                                                  Linter Pass Rate is a Boolean metric assessing whether a configu-
   Experimental Setup for TerraFormer. We build two vari-                                                              ration complies with TFLint [51] best-practice checks. (v) Security
ants of TerraFormer by fine-tuning Qwen2.5-Coder (3B and 14B)                                                          Compliance uses Checkov [3] to scan for vulnerabilities, measured
models (marked with * and † in Tables 2, 3). The models are task-                                                      as the percentage of passed checks per instance, averaged across the
specific, trained for IaC generation and IaC mutation using the                                                        dataset. All metrics are evaluated using the strict pass@1 protocol,
TF-Gen (Train) and TF-Mutn (Train) datasets, respectively. The                                                         where LLMs are allowed only one generation (𝑘=1) per instance.
process begins with a warm-start SFT phase to create TerraFormer                                                          Result Analysis and Ablation Studies. Tables 2 and 3 demon-
(SFT), followed by RL-based fine-tuning to produce TerraFormer                                                         strate that, for both IaC generation and mutation, accuracy tends to
(SFT+RL). We implement SFT and the GRPO-based RL algorithm us-                                                         increase with larger LLM parameter sizes. Several broad trends are
ing Huggingface’s trl library [52], and train the models on 8×80GB                                                     identified. First, among the SoTA LLMs, Sonnet 3.7 and DeepSeek-R1
NVIDIA A100 GPUs. For the 3B model, we perform full-parameter                                                          achieve the highest Correctness across all three datasets, followed by
fine-tuning with bfloat16 precision. The 14B model is fine-tuned                                                       GPT-4.1. Specifically, Sonnet 3.7 attains Correctness of 35.37% on
with 4-bit NF4 quantization using LoRA [18] applied to all linear                                                      IaC-Eval, 16.90% on TF-Gen (Test), and 52.03% on TF-Mutn (Test).
layers in the self-attention and FFN modules, with both rank and                                                       DeepSeek-R1 shows comparable performance, with Correctness of
alpha set to 16. SFT uses a learning rate of 5e-6 with cosine schedul-                                                 33.84%, 11.65%, and 42.03% on the same datasets, respectively. Sec-
ing and a 0.05 warmup ratio, while RL uses a learning rate of 1e-6,                                                    ond, the distilled DeepSeek-R1 variants underperform their backbone
a 0.05 warmup ratio, and DeepSpeed ZeRO-2 optimization.                                                                models. While these variants show good reasoning, they struggle
   Evaluation Metrics. We evaluate LLM-generated IaC using                                                             with instruction-following and often hallucinate resource names or
five metrics, covering basic syntax, functional correctness, security,                                                 attributes. For example, on TF-Mutn (Test), Llama-3.3-70B-Instruct
and adherence to best practices. Together, these provide a holistic                                                    achieves Correctness 38.38% and Deployability 77.70%, whereas its
and practical framework, addressing the shortcomings of prior IaC                                                      DeepSeek-R1 distilled counterpart attains 31.49% and 62.97%, respec-
evaluation approaches such as LLM Judge, CodeBLEU, and Code-                                                           tively. A similar trend appears for Qwen3-8B (Correctness 4.97% on
BERTScore [27] (which often overstate the quality of uncompilable                                                      TF-Gen (Test)) versus DeepSeek-R1-0528-Qwen3-8B (2.27%), and
code), exact string match [46] (too rigid to capture multiple valid                                                    Llama-3.1-8B (5.26%) versus DeepSeek-R1-Distill-Llama-8B (2.27%).
configurations), and sole reliance on static analyzers [4, 37] (which                                                  Third, LLMs trained on programming languages outperform simi-
fail to capture functional correctness). The first three of our metrics,                                               larly sized models that are not. For example, Qwen2.5-Coder-14B
Compilability, Deployability, and Correctness, form a hierarchy of                                                     achieves Correctness of 6.39% and 35.54% on TF-Gen (Test) and
increasingly strict requirements. (i) Compilability ensures syntactic                                                  TF-Mutn (Test), respectively, compared with Qwen3-14B at 5.97%
validity, confirming the configuration parses without error. (ii) De-                                                  and 30.95%. This improvement likely stems from prior exposure
ployability builds on this with semantic validation of cloud-specific                                                  to Terraform-like syntax during training. Fourth, LLMs perform
constraints, checking whether the configuration is feasible for cloud                                                  better on IaC mutation than generation, as mutation provides the
ICSE-SEIP ’26, April 12–18, 2026, Rio de Janeiro, Brazil                                                                                                                                                                                                                                                     Jana et al.

                                              Instances Rated (%)
TF-Gen



                 Policy ↔ Prompt                                                91%                    8% 1%                       Table 3: Evaluation of IaC Mutation. Comparison of SoTA LLMs and Ter-
                                                                                                                                   raFormer on TF-Mutn (Test). Best per column bolded, 2nd-best underlined.
                      Prompt ↔ IaC                                              96%                        4%

                                                                                                                                                      Tool/LLM                                                                              Evaluation on TF-Mutn (Test)
TF-Mutn




                  ΔPolicy ↔ ΔIaC                                                96%                        4%
                                                                                                                                                                                          Correctness             Deployability                    Compilability           Linter                    Security
                  ΔIaC ↔ Prompt                                                  99%                     1%                        Method     Model                              #Params.     (%)                      (%)                             (%)              Pass Rate (%)              Compliance (%)

                                      0       20                         40       60         80        100                                    Claude Sonnet 3.7                    UNK          52.03                               93.51              94.73                           99.86                59.78
                                                                                                                                              DeepSeek(DS)-R1                      671B         42.03                               80.41              84.86                           95.00                55.93
                                Significant                          Moderate                Slight                                           OpenAI GPT 4.1                       UNK          41.62                               81.62              84.46                           99.32                60.21
                                                                                                                                              Llama-3.3-70B-Instruct               70B          38.38                               77.70              81.08                           99.86                60.64
                      Inter-Rater Agreement (IRA) by Gwet’s AC1 (%)                                                                           DS-R1-Distill-Llama-70B              70B          31.49                               62.97              65.95                           99.59                61.81
TF-Gen




                                                                                             89.87%                                          DS-Coder-33B-Instruct                 33B          28.78                               63.92              67.57                           94.46                56.75
                 Policy ↔ Prompt                                                                                                   Few-shot                     †
                                                                                                                                   inference Qwen2.5-Coder-14B                     14B          35.54                               69.86              73.38                           99.32                59.72
                                                                                               91.71%                                        Qwen3-14B                             14B          30.95                               55.14              57.30                           99.59                59.47
                      Prompt ↔ IaC                                                                                                 of SoTA
                                                                                                                                             CodeLlama-13B-Instruct                13B          24.32                               52.43              55.41                           96.22                57.37
                                                                                                                                   LLMs
                                                                                                  94.47%                                     Llama-3.2-11B-Instruct                11B          18.65                               37.84              50.54                           99.46                60.62
TF-Mutn




                  ΔPolicy ↔ ΔIaC
                                                                                                                                              Qwen3-8B                             8B           26.49                               47.43              49.19                           99.05                59.57
                                                                                                  97.30%                                      DS-R1-0528-Qwen3-8B                  8B           20.81                               38.24              40.00                           89.46                53.65
                  ΔIaC ↔ Prompt                                                                                                               Llama-3.1-8B                         8B           20.95                               40.68              42.84                           97.84                61.41
                                      40                             60                80               100                                   DS-R1-Distill-Llama-8B               8B           13.92                               21.35              22.03                           98.78                63.86
                                  Coefficient                                 Confidence Interval                                             Mistral-7B-Instruct                  7B           7.57                                14.59              16.08                           95.95                61.74
                                                                                                                                              Qwen2.5-Coder-3B*                    3B           19.73                               33.51              35.27                           94.19                59.44
Figure 5: Survey on Semantic Alignment.                                                                                                       Llama-3.2-3B-Instruct                3B           1.35                                2.03               20.68                           74.19                47.83
                                                                                                                                            TerraFormer* (SFT)                     3B       32.03 (+12.30)                 61.76 (+28.25)           63.38 (+28.11)             99.59 (+5.40)             66.38 (+6.94)
Cloud-expert ratings for prompt–IaC–policy                                                                                         Our      TerraFormer* (SFT+RL)                  3B       37.97 (+18.24)                 68.11 (+34.60)           70.00 (+34.73)             99.89 (+5.70)             67.21 (+7.77)
alignment on sampled TF-Gen and TF-Mutn                                                                                            approach TerraFormer† (SFT)                     14B       43.91 (+8.37)                 72.16 (+2.30)            78.38 (+5.00)          100.00 (+0.68)            66.23 (+6.51)
                                                                                                                                            TerraFormer† (SFT+RL)                  14B      55.14 (+19.60)                 82.57 (+12.71)           83.92 (+10.54)         100.00 (+0.68)            67.89 (+8.17)
instances, and inter-rater agreement.
                                              # Resource Relations




                                                                                                                                                                                                             # Resource Relations
                 60                                              400                                                                                                        60                                                  400
                                                                                                           # Lines of Code




                                                                                                                                                                                                                                                                     # Lines of Code
                                                                                                                        1,000                                                                                                                                                     1,000
   # Resources




                                                                                                                                                              # Resources


                 40                                                                                                                                                         40
                                                                 200                                                         500                                                                                                200                                                    500
                 20                                                                                                                                                         20
                                                                                                                                        136         100                                            7                                                        48                                    126               178
                          5            2                                         35               25                                                                                    4                                                     33
                  0                                                  0                                                         0                                            0                                                       0                                                    0
                      Success     Failure                                 Success           Failure                                 Success     Failure                          Success     Failure                                    Success       Failure                                  Success        Failure
                       Repair Outcome                                         Repair Outcome                                        Repair Outcome                               Repair Outcome                                         Repair Outcome                                         Repair Outcome
                      (a) Policy generation outcome vs. input IaC complexity                                                                                                 (b) Mutation generation outcome vs. input IaC complexity
Figure 6: Effectiveness analysis of multi-turn repair loops. Box-plot of outcomes for verifiable policy and mutation
generation versus input IaC complexity (# resources, # inter-resource relations, # lines). In (a), median success exceeds failure; in
(b), median failure exceeds success, showing policy generation improves while mutation generation worsens with complexity.
initial configuration and clear edit instructions, reducing ambiguity.                                                                                               (Test), while ranking third on IaC-Eval. It achieves a perfect Linter
As noted in Section 1, code mutation also better reflects real-world                                                                                                 Pass Rate of 100% and the highest Security Compliance across all
development practices than generating code from scratch.                                                                                                             three benchmarks, demonstrating strong adherence to best prac-
   For the IaC generation task on IaC-Eval, our TerraFormer†                                                                                                         tices. These are attributed to SFT on our rigorously verified dataset,
(SFT) improves Qwen2.5-Coder-14B by +8.73% in Correctness,                                                                                                           combined with RL via a fine-grained verifier-guided reward.
+14.41% in Deployability, and +16.81% in Compilability. On TF-
Gen (Test), the gains are +5.54%, +26.42%, and +20.88%, respectively.
For the IaC mutation task on TF-Mutn (Test), TerraFormer† (SFT)                                                                                                      7           Quality Assessment of TF-Gen & TF-Mutn
improves Qwen2.5-Coder-14B by +8.37%, +2.30%, and +5.00%. Sim-                                                                                                       We ensure and evaluate the quality of our datasets through multi-
ilar trends hold for TerraFormer* (SFT) over Qwen2.5-Coder-3B.                                                                                                       ple measures. First, the initial pool of Terraform configurations is
Our TerraFormer† (SFT+RL) achieves further gains. For IaC gen-                                                                                                       sourced from real GitHub repositories, ensuring human-authored
eration on IaC-Eval, it improves Qwen2.5-Coder-14B by +15.94%,                                                                                                       style. Second, for each instance {prompt NL, 𝑡, policy FL } in TF-Gen: 𝑡
                                                                                                                                                                     is deployable and 𝑡 ⊢ policy FL ; for each {prompt m      init , 𝑡 m , policy init ,
+30.35%, and +31.22% in Correctness, Deployability, and Compilabil-                                                                                                                                                     NL , 𝑡                     FL
                                                                                                                                                                            m
ity, respectively; on TF-Gen (Test), the improvements are +11.65%,                                                                                                   policy FL } in TF-Mutn: both 𝑡 and 𝑡 are deployable and 𝑡 init ⊢
                                                                                                                                                                                                       init      m

+39.63%, and +39.77%. For IaC mutation on TF-Mutn (Test), the                                                                                                        policy init
                                                                                                                                                                            FL ,𝑡
                                                                                                                                                                                  m ⊢ policy m . In this section, we analyze the total cost
                                                                                                                                                                                             FL
gains are +19.60%, +12.71%, and +10.54%. Overall, TerraFormer†                                                                                                       and effectiveness of the multi-turn repair loops. Third, we conduct
(SFT+RL) achieves top rankings: on IaC-Eval (IaC generation), it                                                                                                     a survey to verify that LLM-judged prompt–IaC–policy alignment
ranks highest in Deployability and third in Correctness and Compi-                                                                                                   (Section 4) strongly correlates with cloud experts. Fourth, combin-
lability; on TF-Gen (Test) (IaC generation), highest in Correctness                                                                                                  ing expert ratings with edit distance analysis shows that TF-Mutn
and second in Deployability and Compilability; on TF-Mutn (Test)                                                                                                     predominantly contains medium- and high-complexity mutations.
(IaC mutation), highest in Correctness and second in Deployability.                                                                                                  Cost and Effectiveness Analysis of Multi-Turn Repair Loops.
   The results show that, despite being ≈50× smaller, TerraFormer†                                                                                                   Given the LLM pricing of $0.003 per 1,000 input tokens and $0.015
(SFT+RL) outperforms foundation LLMs such as Sonnet 3.7, DeepSeek-                                                                                                   per 1,000 output tokens on Amazon Bedrock, creating the dataset
R1, and GPT-4.1 in Correctness on TF-Gen (Test) and TF-Mutn                                                                                                          through repair loops costed us approximately $15,000. Instead of
                              TerraFormer: Automated Infrastructure-as-Code with LLMs Fine-Tuned via Policy-Guided Verifier Feedback                                    ICSE-SEIP ’26, April 12–18, 2026, Rio de Janeiro, Brazil


                                                                                                                                                  The results, summarized in Figure 5, show strong semantic align-




                                                                Edit Distance of 𝑡 init and 𝑡 m
Edit Distance of 𝑡 init and 𝑡 m




                                  4,000                                                           4,000
                                                                                                                  TF-Mutn (Train)
                                                                                                                                               ment. For the two TF-Gen questions, 91% and 96% of raters rate the
                                  3,500                                                           3,500           TF-Mutn (Test)
                                                                                                                                               alignment as Significant, and for TF-Mutn, 96% and 99%. IRA re-
                                  3,000                                                           3,000
                                                                                                                                               mains high, with Gwet’s AC1 coefficients of 89.87%, 91.71%, 94.47%,
                                  2,500                                                           2,500
                                                                                                                                               and 97.30% across the four questions. Furthermore, all instances
                                  2,000                                                           2,000
                                                                                                                                               in the datasets and effectively all in the survey are approved by
                                  1,500                                                           1,500
                                                                                                                                               the LLM judge during dataset construction. This ensures that the
                                  1,000                                                           1,000                                        results directly reflect cloud experts’ agreement with the LLM judge,
                                   500                                                             500                                         demonstrating its effectiveness in validating semantic alignment.
                                     0                                                               0
                                           Low Medium High                                                0      20    40    60     80   100   Mutation Complexity in TF-Mutn. From the expert survey, we
                                          Mutation Complexity                                                 Cumulative %age of TF-Mutn       measure the mutation complexity by asking raters to first iden-
                                             (a)                                                                      (b)                      tify differences between (𝑡 init and 𝑡 m ), then rate 𝚫IaC complexity:
                                                                                                                                               “How challenging would it be for a cloud expert to mutate 𝑡 init into 𝑡 m
                              Figure 7: Mutation Complexity in TF-Mutn. (a) Correla-                                                           given the significance of differences?”. Responses use a three-point
                              tion between edit distance and human-rated complexity for                                                        scale: Low, Medium, High. Although subjective, the ratings show
                              100 survey samples; estimated thresholds for low [0, 160),                                                       clear patterns: minor edits (e.g., tag or feature-toggle updates) were
                              medium [160, 1200), and high [1200, ∞) are shown with thick                                                      rated low; additions or adjustments of resources without chang-
                              dashed lines. (b) Cumulative distribution of edit distances                                                      ing the overall architecture were rated medium; and substantial
                              for all TF-Mutn instances by complexity, clipped at 4200 for                                                     redesigns (e.g., adding multiple components or restructuring inter-
                              visualization (actual maxima: Train 13205, Test 4619).                                                           actions) were rated high. To quantify this, we compute the Leven-
                                                                                                                                               shtein (edit) distance between 𝑡 init and 𝑡 m for all survey samples and
                              using Mechanical Turk, which would have required about 30 min-
                                                                                                                                               correlate them with expert ratings (Figure 7a). Thresholds minimiz-
                              utes per instance at $50/hour, totaling nearly $5 million to curate
                                                                                                                                               ing disagreement suggest distances below 160 generally correspond
                              200,000 instances, this method is far more economical. In addition,
                                                                                                                                               to low complexity, 160–1200 to medium, and above 1200 to high.
                              sustaining such a large-scale human effort with cloud experts over
                                                                                                                                                  Extending this analysis, we compute the edit distances for all
                              an extended period would have been practically infeasible.
                                                                                                                                               51,776 instances in TF-Mutn (Train) and 740 in TF-Mutn (Test),
                                 We conduct an effectiveness analysis of the repair loops to study
                                                                                                                                               and plot the cumulative distribution (Figure 7b). Using survey-
                              how policy and mutation generation (Section 4) are affected by
                                                                                                                                               derived thresholds, mutations are categorized by complexity: in
                              input configuration complexity, measured by the number of re-
                                                                                                                                               TF-Mutn (Train), 20.35% are low-complexity mutations, 56.82%
                              sources, inter-resource relations, and lines of code. We assess how
                                                                                                                                               medium, and 22.83% high; in TF-Mutn (Test), 20% are low, 52.57%
                              these factors relate to success rates, defined as cases where the LLM
                                                                                                                                               medium, and 27.43% high. Both datasets thus contain a balanced
                              can successfully produce a verifiable policy or mutation within
                                                                                                                                               mix, with medium and high predominating, providing a diverse
                              the threshold of five repair iterations. Figure 6 shows that policy
                                                                                                                                               and challenging set for validating and training IaC mutation tools.
                              generation success rises with complexity, suggesting smaller con-
                              figurations lack sufficient intent or cloud primitives. In contrast,
                                                                                                                                               8    Conclusion
                              mutation success falls with complexity, as more resources and de-
                              pendencies make it harder to generate deployable configurations.                                                 We present TerraFormer, a framework for automated IaC generation
                                                                                                                                               and mutation using LLMs fine-tuned with policy-guided verifier
                           Expert Survey on Semantic Alignment of Prompt, IaC, and
                                                                                                                                               feedback. It addresses key IaC automation challenges: scarce high-
                           Policy. For an infrastructure instance, the policy should act as a
                                                                                                                                               quality datasets, difficulty generating syntactically and function-
                           verifier of the prompt’s intent, while the target IaC should faithfully
                                                                                                                                               ally correct IaC, and lack of reliable evaluation metrics. It is also
                           implement it. To evaluate this semantic alignment, we conduct a
                                                                                                                                               among the first to tackle IaC mutation. Our automated data cura-
                           survey in which we uniformly sample 100 instances each from TF-
                                                                                                                                               tion pipeline produces large NL-to-IaC datasets, TF-Gen and TF-
                           Gen and TF-Mutn. We then partition the instances into 20 groups
                                                                                                                                               Mutn, via multi-stage verification and iterative LLM self-correction.
                           of 10 and assign each group to a rater with expertise in cloud in-
                                                                                                                                               Combining SFT with RL guided by fine-grained verifier feedback,
                           frastructures. For each TF-Gen instance, we pose two questions: (a)
                                                                                                                                               TerraFormer significantly improves syntax correctness, deployabil-
                           Policy↔Prompt: “To what extent does policy FL capture the intent
                                                                                                                                               ity, policy compliance, and security over its base LLM. Evaluations
                           of prompt NL (treating the former as a test-case for the latter)?” and
                                                                                                                                               against 17 state-of-the-art LLMs, including models nearly 50× larger
                           (b) Prompt↔IaC: “To what extent is the intent of prompt NL cor-
                                                                                                                                               such as Sonnet 3.7, DeepSeek-R1, and GPT-4.1, show TerraFormer
                           rectly realized by 𝑡?”. For TF-Mutn, we define ΔIaC = diff 𝑡 init, 𝑡 m
                                                                                                                                               outperforms them on TF-Gen (Test) and TF-Mutn (Test), achieves
                           and ΔPolicy = diff policyFLinit , policy m , and ask: (a) 𝚫Policy↔𝚫IaC:
                                                                   FL                                                                          third-best on IaC-Eval, and attains highest best-practices and se-
                           “To what extent does ΔPolicy reflect the ΔIaC changes?” and (b)
                                                                                                                                               curity compliance rates. These results demonstrate that verifier-
                           𝚫IaC↔Prompt: “To what extent does ΔIaC match prompt m             NL ’s in-                                         guided fine-tuning on formally verified datasets produces more
                           tent?”. Responses use a three-point scale: Significant, Moderate, and
                                                                                                                                               intent-aligned, deployable IaC. Overall, TerraFormer provides a
                           Slight. To address subjectivity, three raters independently evaluated
                                                                                                                                               scalable foundation for automating cloud infrastructure and other
                           25 instances each from TF-Gen and TF-Mutn, and we measure
                                                                                                                                               code generation tasks, highlighting the potential of combining LLM
                           inter-rater agreement using Gwet’s AC1 [16], which provides stable
                                                                                                                                               reasoning with formal verification for IaC automation.
                           estimates even for skewed response distributions.
ICSE-SEIP ’26, April 12–18, 2026, Rio de Janeiro, Brazil                                                                                                             Jana et al.


A      Reproducibility                                                                  Prompt Template for few-shot inference of IaC generation.
All experiments in this work, including dataset construction, model                     The following prompt is used to obtain the results of all the LLM-
training (both supervised fine-tuning and reinforcement learning),                      based tools reported in Table 2 for the IaC generation task.
inference, and evaluation, are performed using Python 3.12.10 and                       You are an expert Infrastructure - as - Code ( IaC ) developer with deep expertise in
                                                                                        Terraform .
Terraform v1.12.0. Our full codebase, including scripts for dataset
generation, model fine-tuning, and inference across both GPU- and                       Your task is to :
                                                                                        Given an user prompt , generate a ** single ** , ** fully self - contained ** , and **
API-based setups, can be shared upon request.                                           valid ** Terraform configuration written in HCL . Your configuration must :
                                                                                        - Satisfy the intent of the user prompt .
                                                                                        - Be compatible with ** Terraform v1 .12.0**.

B     Description of LLM Prompts                                                        - Pass both ` terraform validate ` and ` terraform plan `.
                                                                                        - Include a valid ` provider ` block .
                                                                                        - Contain no undeclared variables or references .
Prompt Template for Multi-Turn Repair Loop. We present the                              - Avoid the use of ` assume_role `, custom ` profile ` values , or external
                                                                                        dependencies .
prompt used in step-3 of Figure 3a, where FV-ii (terraform plan)                        - Use only the following providers : `aws `, `random `, `null `, `local `, ` template
                                                                                        `, `tls `, `time `, ` external `, `http `, ` archive `, `docker `, ` terraform `.
acts as the verifier. Given a Terraform configuration, FV-ii produces
                                                                                        Here are a few examples :
an error certificate if the configuration fails the deployability test.
This certificate guides iterative repairs in a multi-turn loop, with                    ### Example -1
                                                                                        Prompt : { prompt_example1 }
each round updating both the certificate and the configuration                          Configuration :
                                                                                        ``` hcl
until the configuration passes the deployability test. Similar prompt                   { TF_gen_example1 }
                                                                                        ```
templates are employed for repair loops with other verifiers, FV-i                      ...

and FV-iii, with adjustments in task description and requirements.                      Here is the ** actual ** user prompt :
                                                                                        < user_prompt >
                                                                                        { request }
You are an expert Infrastructure - as - Code ( IaC ) developer with deep expertise in
                                                                                        </ user_prompt >
Terraform .
                                                                                        Now respond to the actual user prompt by returning ** one single ** Terraform
You will be given :
                                                                                        configuration . Do not repeat or revise the configuration . Importantly , enclose
( a ) A Terraform configuration written in HCL , intended for Terraform v1 .12.0.
                                                                                        the final configuration inside the following tags :
This code currently fails the terraform plan command .
( b ) The error message output from running terraform plan .
                                                                                        < final_terraform_config >
                                                                                        ( Provide your entire Terraform configuration within these tags )
Your task is to :
                                                                                        </ final_terraform_config >
( a ) Clearly explain the cause of the error in your own words .
( b ) Describe how you will fix the issue .
( c ) Provide a fully corrected version of the Terraform configuration ( in HCL )
that ensures terraform plan completes successfully .
                                                                                        Prompt Template for few-shot inference of IaC mutation. The
Requirements :
( i ) If the error indicates " timed out " , it is possibly because Terraform waits
                                                                                        following prompt is used to obtain the results of all the LLM-based
for interactive input to fill a variable with no default value .
      Ensure that you add reasonable default values for all input variables for
                                                                                        tools reported in Table 3 for the IaC mutation task.
      non - interactive execution .
( ii ) You are permitted to modify any aspect of the Terraform code , including         You are an expert Infrastructure - as - Code ( IaC ) developer with deep expertise in
adding or removing entire blocks , arguments , or resources . Apply changes as          Terraform .
rigorously as necessary to ensure that terraform plan completes successfully .
( iii ) You must ensure compatibility with Terraform version 1.12.0.                    Your task is to :
( iv ) You may remove problematic elements such as assume_role blocks or profile =      Given an existing Terraform configuration and an user prompt requesting changes ,
  " admin -1" if they can cause permission errors .                                      generate a ** single ** , ** modified ** Terraform configuration written in HCL that
( v ) Terraform will rely on default credentials ( e . g . , EC2 instance metadata or    is ** fully self - contained ** and ** valid **. Your configuration must :
environment variables ) , so explicit credential configuration should be removed        - Be a modified version of the existing Terraform configuration .
if problematic .                                                                        - Satisfy the intent of the changes requested in the user prompt .
( vi ) You are only allowed to change the Terraform code . Do not assume access to      - Be compatible with ** Terraform v1 .12.0**.
other configuration files or systems .                                                  - Pass both ` terraform validate ` and ` terraform plan `.
                                                                                        - Include a valid ` provider ` block .
Here are three examples of correct Terraform HCL codes :                                - Contain no undeclared variables or references .
                                                                                        - Avoid the use of ` assume_role `, custom ` profile ` values , or external
### Example -1                                                                          dependencies .
``` hcl                                                                                 - Use only the following providers : `aws `, `random `, `null `, `local `, ` template
{ TF_example1 }                                                                         `, `tls `, `time `, ` external `, `http `, ` archive `, `docker `, ` terraform `.
```
                                                                                        Here are a few examples :
### Example -2
``` hcl                                                                                 ### Example -1
{ TF_example2 }                                                                         Initial Configuration :
```                                                                                     ``` hcl
                                                                                        { TF_init_example1 }
### Example -3                                                                          ```
``` hcl                                                                                 Prompt : { prompt_example1 }
{ TF_example3 }                                                                         Mutated Configuration :
```                                                                                     ``` hcl
                                                                                        { TF_mutn_example1 }
Here is the incorrect configuration ( in Terraform HCL ) :                              ```
< incorrect_terraform_config >                                                          ...
``` hcl
{ config }                                                                              Here is the ** initial Terraform configuration **:
```                                                                                     < initial_terraform_config >
</ incorrect_terraform_config >                                                         ``` hcl
                                                                                        { TF_init }
Here is the error message obtained by running terraform plan command or a               ```
timeout notice if the command does not complete within 30 seconds :                     </ initial_terraform_config >
< error_message >
{ error_message_TFplan }                                                                Here is the ** user prompt ** requesting changes :
</ error_message >                                                                      < user_prompt >
                                                                                        { prompt }
Return the correct Terraform configuration within the following tags . Do not           </ user_prompt >
return empty code .
< corrected_terraform_config >                                                          Now respond by returning ** a single ** , ** modified ** Terraform configuration .
( Your entire Terraform configuration goes here )                                       Importantly , enclose the final configuration inside the following tags :
</ corrected_terraform_config >
                                                                                        < mutated_terraform_config >
                                                                                        ( Provide your entire modified Terraform configuration within these tags )
                                                                                        </ mutated_terraform_config >
TerraFormer: Automated Infrastructure-as-Code with LLMs Fine-Tuned via Policy-Guided Verifier Feedback                   ICSE-SEIP ’26, April 12–18, 2026, Rio de Janeiro, Brazil


References                                                                                 [25] Albert Q Jiang, Wenda Li, and Mateja Jamnik. 2024. Multi-language Diversity
 [1] Aider. 2024. O1 Tops Aider’s New Polyglot Leaderboard. https://aider.chat/2024/            benefits Autoformalization. In Proceedings of the 38th International Conference on
     12/21/polyglot.html#the-polyglot-benchmark Accessed: September, 2025.                      Neural Information Processing Systems (Vancouver, BC, Canada), Vol. 37. Curran
 [2] Anthropic. 2025. Claude 3.7 Sonnet and Claude Code. https://www.anthropic.                 Associates Inc., Red Hook, NY, USA, 83600–83626.
     com/news/claude-3-7-sonnet Accessed: September, 2025.                                 [26] Albert Q. Jiang, Alexandre Sablayrolles, Arthur Mensch, Chris Bamford, De-
 [3] Bridgecrew. 2024. Checkov. https://www.checkov.io/ Prisma Cloud, Accessed:                 vendra Singh Chaplot, Diego de las Casas, Florian Bressand, Gianna Lengyel,
     September, 2025.                                                                           Guillaume Lample, Lucile Saulnier, Lélio Renard Lavaud, Marie-Anne Lachaux,
 [4] Christoph Buehler, David Spielmann, Roland Meier, and Guido Salvaneschi. 2025.             Pierre Stock, Teven Le Scao, Thibaut Lavril, Thomas Wang, Timothée Lacroix,
     TerraDS: A Dataset for Terraform HCL Programs. In Proceedings of the 22nd                  and William El Sayed. 2023. Mistral 7B. arXiv:2310.06825
     International Conference on Mining Software Repositories (MSR), Data and Tool         [27] Patrick T Kon, Jiachen Liu, Yiming Qiu, Weijun Fan, Ting He, Lei Lin, Haoran
     Showcase Track (Ottawa, Canada). IEEE/ACM, 654–658.                                        Zhang, Owen M Park, George S Elengikal, Yuxin Kang, et al. 2024. IaC-Eval:
 [5] Yinghao Chen, Zehao Hu, Chen Zhi, Junxiao Han, Shuiguang Deng, and Jianwei                 A Code Generation Benchmark for Cloud Infrastructure-as-Code Programs. In
     Yin. 2024. ChatUniTest: A Framework for LLM-based Test Generation. In Com-                 Proceedings of the 38th International Conference on Neural Information Processing
     panion Proceedings of the 32nd ACM International Conference on the Foundations             Systems (Vancouver, BC, Canada), Vol. 37. Curran Associates Inc., Red Hook, NY,
     of Software Engineering (Porto de Galinhas, Brazil). ACM, 572–576.                         USA, 134488–134506.
 [6] Kyle Daigle. 2023. Octoverse: The State of Open Source and Rise of AI in 2023.        [28] Junhee Lee, SungJoo Kang, and In-Young Ko. 2024. An LLM-driven Framework
     https://github.blog/news-insights/octoverse/octoverse-2024/ GitHub, Accessed:              for Dynamic Infrastructure as Code Generation. In Proceedings of the 25th Inter-
     September, 2025.                                                                           national Middleware Conference: Demos, Posters and Doctoral Symposium. 9–10.
 [7] Matthew DeLorenzo, Kevin Tieu, Prithwish Jana, Piyush Jha, Dileep Kalathil,           [29] Jiawei Liu, Chunqiu Steven Xia, Yuyao Wang, and Lingming Zhang. 2023. Is
     Vijay Ganesh, and Jeyavijayan Rajendran. 2025. Abstraction-of-Thought: Interme-            Your Code Generated by ChatGPT Really Correct? Rigorous Evaluation of Large
     diate Representations for LLM Reasoning in Hardware Design. arXiv:2505.15873               Language Models for Code Generation. In Proceedings of the 37th International
 [8] Shihan Dou, Yan Liu, Haoxiang Jia, Limao Xiong, Enyu Zhou, Wei Shen, Junjie                Conference on Neural Information Processing Systems.
     Shan, Caishuang Huang, Xiao Wang, Xiaoran Fan, et al. 2024. StepCoder: Im-            [30] Jiate Liu, Yiqin Zhu, Kaiwen Xiao, Qiang Fu, Xiao Han, Wei Yang, and Deheng Ye.
     prove Code Generation with Reinforcement Learning from Compiler Feedback.                  2023. RLTF: Reinforcement Learning from Unit Test Feedback. arXiv:2307.04349
     arXiv:2402.01391                                                                      [31] Meta AI. 2024. Llama 3.2: Revolutionizing Edge AI and Vision with Open, Cus-
 [9] Abhimanyu Dubey, Abhinav Jauhri, Abhinav Pandey, Abhishek Kadian, Ahmad                    tomizable Models. https://ai.meta.com/blog/llama-3-2-connect-2024-vision-
     Al-Dahle, Aiesha Letman, Akhil Mathur, Alan Schelten, Amy Yang, Angela Fan,                edge-mobile-devices/ Blog post, Meta AI, Accessed: September, 2025.
     et al. 2024. The Llama 3 Herd of Models. arXiv:2407.21783                             [32] Meta AI. 2024. LLaMA 3.3: Model Card and Prompt Formats. https://www.llama.
[10] Clémentine Fourrier, Nathan Habib, Alina Lozovskaya, Konrad Szafer, and                    com/docs/model-cards-and-prompt-formats/llama3_3/ Accessed: September,
     Thomas Wolf. 2024. Open LLM Leaderboard v2. https://huggingface.co/spaces/                 2025.
     open-llm-leaderboard/open_llm_leaderboard HuggingFace, Accessed: Septem-              [33] Meta AI. 2025. Llama 4: Multimodal Intelligence. https://ai.meta.com/blog/llama-
     ber, 2025.                                                                                 4-multimodal-intelligence/ Accessed: September, 2025.
[11] G-Team, Rohan Anil, Sebastian Borgeaud, Jean-Baptiste Alayrac, Jiahui Yu, Radu        [34] Mariusz Michalowski. 2025. 55 Cloud Computing Statistics for 2025. https:
     Soricut, Johan Schalkwyk, Andrew M Dai, Anja Hauth, Katie Millican, et al. 2023.           //spacelift.io/blog/cloud-computing-statistics Spacelift, Accessed: September,
     Gemini: A Family of Highly Capable Multimodal Models. arXiv:2312.11805                     2025.
[12] GitHub. 2024. The State of Open Source: The 2024 Octoverse Report. https://github.    [35] Kief Morris. 2020. Infrastructure as Code. O’Reilly Media.
     blog/news-insights/octoverse/octoverse-2024/ GitHub, Accessed: September,             [36] OpenAI. 2025. Introducing GPT-4.1 in the API. https://openai.com/index/gpt-4-1/
     2025.                                                                                      Accessed: September, 2025.
[13] Brian Grant. 2024. The Status of LLM-based Terraform Generation at the End            [37] Mayur Amarnath Palavalli, Mark Santolucito, et al. 2024. Using a Feedback Loop
     of 2024. https://itnext.io/the-status-of-llm-based-terraform-generation-at-the-            for LLM-based Infrastructure as Code Generation. arXiv:2411.19043
     end-of-2024-e31639068318 ITNEXT, Medium, Accessed: September, 2025.                   [38] Daniel Palenicek. 2021. A Survey on Constraining Policy Updates using the KL
[14] Daya Guo, Dejian Yang, Haowei Zhang, Junxiao Song, Ruoyu Zhang, Runxin Xu,                 Divergence. In Reinforcement Learning Algorithms: Analysis and Applications.
     Qihao Zhu, Shirong Ma, Peiyi Wang, Xiao Bi, et al. 2025. DeepSeek-R1: Incentiviz-          Springer, 49–57.
     ing Reasoning Capability in LLMs via Reinforcement Learning. arXiv:2501.12948         [39] Saurabh Pujar, Luca Buratti, Xiaojie Guo, Nicolas Dupuis, Burn Lewis, Sahil
[15] Daya Guo, Qihao Zhu, Dejian Yang, Zhenda Xie, Kai Dong, Wentao Zhang,                      Suneja, Atin Sood, Ganesh Nalawade, Matt Jones, Alessandro Morari, et al. 2023.
     Guanting Chen, Xiao Bi, Yu Wu, YK Li, et al. 2024. DeepSeek-Coder: When                    Automated Code Generation for Information Technology Tasks in YAML through
     the Large Language Model Meets Programming–The Rise of Code Intelligence.                  Large Language Models. In Proceedings of the 2023 60th ACM/IEEE Design Au-
     arXiv:2401.14196                                                                           tomation Conference (DAC). IEEE, 4 pages.
[16] Kilem Gwet. 2001. Handbook of Inter-Rater Reliability: How to Estimate the Level      [40] Yiming Qiu, Patrick Tser Jern Kon, Jiarong Xing, Yibo Huang, Hongyi Liu, Xinyu
     of Agreement Between Two or Multiple Raters. Gaithersburg, MD: STATAXIS                    Wang, Peng Huang, Mosharaf Chowdhury, and Ang Chen. 2023. Simplifying
     Publishing Company (2001).                                                                 Cloud Management with Cloudless Computing. In Proceedings of the 22nd ACM
[17] HashiCorp. 2014. Terraform. https://developer.hashicorp.com/terraform Ac-                  Workshop on Hot Topics in Networks. 95–101.
     cessed: September, 2025.                                                              [41] Hariharan Ragothaman, Saai Krishnan Udayakumar, et al. 2024. Optimizing
[18] Edward J Hu, Yelong Shen, Phillip Wallis, Zeyuan Allen-Zhu, Yuanzhi Li, Shean              Service Deployments with NLP based Infrastructure Code Generation - An Au-
     Wang, Lu Wang, Weizhu Chen, et al. 2022. LoRA: Low-Rank Adaptation of Large                tomation Framework. In Proceedings of the 2024 IEEE 2nd International Conference
     Language Models. In Proceedings of the 2022 International Conference on Learning           on Electrical Engineering, Computer and Information Technology (ICEECIT). IEEE,
     Representations (ICLR).                                                                    216–221.
[19] Binyuan Hui, Jian Yang, Zeyu Cui, Jiaxi Yang, Dayiheng Liu, Lei Zhang, Tianyu         [42] Musfiqur Rahman, Sayed Hassan Khatoonabadi, Ahmad Abdellatif, and Emad
     Liu, Jiajun Zhang, Bowen Yu, Keming Lu, et al. 2024. Qwen2.5-Coder Technical               Shihab. 2024. Automatic Detection of LLM-generated Code: A Case Study of
     Report. arXiv:2409.12186                                                                   Claude 3 Haiku. arXiv:2409.01382
[20] Debasish Jana. 2014. C++ and Object-Oriented Programming Paradigm. PHI                [43] Baptiste Roziere, Jonas Gehring, Fabian Gloeckle, Sten Sootla, Itai Gat, Xiao-
     Learning Pvt. Ltd.                                                                         qing Ellen Tan, Yossi Adi, Jingyu Liu, Romain Sauvestre, Tal Remez, et al. 2023.
[21] Prithwish Jana. 2024. NeuroSymbolic LLM for Mathematical Reasoning and                     Code Llama: Open Foundation Models for Code. arXiv:2308.12950
     Software Engineering. In Proceedings of the 33rd International Joint Conference on    [44] Zhihong Shao, Peiyi Wang, Qihao Zhu, Runxin Xu, Junxiao Song, Xiao Bi,
     Artificial Intelligence (IJCAI), Doctoral Consortium. IJCAI, 8492–8493.                    Haowei Zhang, Mingchuan Zhang, YK Li, Yang Wu, et al. 2024. DeepSeek-
[22] Prithwish Jana, Piyush Jha, Haoyang Ju, Gautham Kishore, Aryan Mahajan, and                Math: Pushing the Limits of Mathematical Reasoning in Open Language Models.
     Vijay Ganesh. 2024. CoTran: An LLM-based Code Translator using Reinforcement               arXiv:2402.03300
     Learning with Feedback from Compiler and Symbolic Execution. In Proceedings           [45] Daniel Sokolowski, David Spielmann, and Guido Salvaneschi. 2024. Automated In-
     of the 27th European Conference on Artificial Intelligence (ECAI). IOS Press, 4011–        frastructure as Code Program Testing. IEEE Transactions on Software Engineering
     4018.                                                                                      (2024).
[23] Prithwish Jana, Kaan Kale, Ahmet Ege Tanriverdi, Cruise Song, Sriram Vish-            [46] Kalahasti Ganesh Srivatsa, Sabyasachi Mukhopadhyay, Ganesh Katrapati, and
     wanath, and Vijay Ganesh. 2025. ProofBridge: Auto-Formalization of Natural                 Manish Shrivastava. 2023. A Survey of using Large Language Models for Gener-
     Language Proofs in Lean via Joint Embeddings. arXiv:2510.15681                             ating Infrastructure as Code. In Proceedings of the 20th International Conference
[24] Piyush Jha, Prithwish Jana, Pranavkrishna Suresh, Arnav Arora, and Vijay                   on Natural Language Processing (ICON), Jyoti D. Pawar and Sobha Lalitha Devi
     Ganesh. 2025. RLSF: Fine-tuning LLMs via Symbolic Feedback. In Proceedings of              (Eds.). 523–533.
     the 28th European Conference on Artificial Intelligence (ECAI). IOS Press, 1687–      [47] Styra, Inc. 2023. Open Policy Agent (OPA). https://www.openpolicyagent.org/
     1694.                                                                                      Accessed: September, 2025.
ICSE-SEIP ’26, April 12–18, 2026, Rio de Janeiro, Brazil                                                                                                      Jana et al.


[48] Synergy Research. 2024. Cloud Market Growth Stays Strong in Q2 While Amazon,           huggingface/trl Huggingface, Accessed: September, 2025.
     Google and Oracle Nudge Higher. https://www.srgresearch.com/articles/cloud-       [53] Huajian Xin, ZZ Ren, Junxiao Song, Zhihong Shao, Wanjia Zhao, Haocheng
     market-growth-stays-strong-in-q2-while-amazon-google-and-oracle-nudge-                 Wang, Bo Liu, Liyue Zhang, Xuan Lu, Qiushi Du, et al. 2024. Deepseek-Prover-
     higher Press release, Accessed: September, 2025.                                       v1. 5: Harnessing Proof Assistant Feedback for Reinforcement Learning and
[49] Shubham Ugare, Tarun Suresh, Hangoo Kang, Sasa Misailovic, and Gagan-                  Monte-Carlo Tree Search. arXiv:2408.08152
     deep Singh. 2024. SynCode: LLM Generation with Grammar Augmentation.              [54] Yifei Xu, Yuning Chen, Xumiao Zhang, Xianshang Lin, Pan Hu, Yunfei Ma,
     arXiv:2403.01632                                                                       Songwu Lu, Wan Du, Zhuoqing Mao, Ennan Zhai, et al. 2024. CloudEval-YAML:
[50] Yubo Wang, Xueguang Ma, Ge Zhang, Yuansheng Ni, Abhranil Chandra,                      A Practical Benchmark for Cloud Configuration Generation. In Proceedings of
     Shiguang Guo, Weiming Ren, Aaran Arulraj, Xuan He, Ziyan Jiang, et al. 2024.           Machine Learning and Systems (MLSys), Vol. 6. 173–195.
     MMLU-Pro: A More Robust and Challenging Multi-Task Language Understand-           [55] An Yang, Anfeng Li, Baosong Yang, Beichen Zhang, Binyuan Hui, Bo Zheng,
     ing Benchmark. In Proceedings of the 38th International Conference on Neural           Bowen Yu, Chang Gao, Chengen Huang, Chenxu Lv, et al. 2025. Qwen3 Technical
     Information Processing Systems (Vancouver, BC, Canada). Curran Associates Inc.,        Report. arXiv:2505.09388
     25 pages.                                                                         [56] Quanjun Zhang, Chunrong Fang, Siqi Gu, Ye Shang, Zhenyu Chen, and Liang
[51] Kazuma Watanabe, Ben Drucker, John Reese, Aleksa Cukovic, et al. 2024. TFLint:         Xiao. 2025. Large Language Models for Unit Testing: A Systematic Literature
     A Pluggable Terraform Linter. https://github.com/terraform-linters/tflint Ac-          Review. arXiv:2506.15227
     cessed: September, 2025.                                                          [57] Tianyi Zhang, Shidong Pan, Zejun Zhang, Zhenchang Xing, and Xiaoyu Sun.
[52] Leandro von Werra, Younes Belkada, Lewis Tunstall, Edward Beeching, Tris-              2025. Deployability-Centric Infrastructure-as-Code Generation: An LLM-based
     tan Thrush, Nathan Lambert, Shengyi Huang, Kashif Rasul, and Quentin Gal-              Iterative Framework. arXiv:2506.05623
     louédec. 2020. TRL: Transformer Reinforcement Learning. https://github.com/
