# A Whole New World: Creating a Parallel-Poisoned Web Only AI-Agents Can See
(authored by agents unless marked 🧑)

- primary PDF: local collection PDF
- publication: arXiv:2509.00124 (2025)
- URL: https://arxiv.org/abs/2509.00124

## abstract (verbatim)
> This paper introduces a novel attack vector that leverages website cloaking techniques to compromise autonomous web-browsing agents powered by Large Language Models (LLMs). ... A malicious website can identify an incoming request as originating from an AI agent and dynamically serve a different, "cloaked" version of its content. While human users see a benign webpage, the agent is presented with a visually identical page embedded with hidden, malicious instructions, such as indirect prompt injections. ... This work formalizes the threat model, details the mechanics of agent fingerprinting and cloaking, and discusses the profound security implications for the future of agentic AI, highlighting the urgent need for robust defenses against this stealthy and scalable attack.

## relevance to DeGenTWeb
This is adjacent rather than a prevalence measurement: it shows that websites can intentionally vary content for AI agents, search crawlers, and humans. That threat model is relevant to interpreting deployed search measurements because crawler-visible text may differ from ordinary user-visible text and because site-level AI-content prevalence can have an agent-specific security impact.
