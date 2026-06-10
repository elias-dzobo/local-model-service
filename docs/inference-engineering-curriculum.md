# First-Principles Inference Engineering Curriculum

This version of the curriculum is theory-heavy by design. We start from first principles, build a rigorous mental model of inference, and only introduce hands-on work when practice clarifies a concept that is otherwise too abstract.

Primary text:

- `/Users/eliasdzobo/Downloads/Inference Engineering.pdf` by Philip Kiely

Local model sandbox for later practice:

- [`/Users/eliasdzobo/Desktop/local-model-service/model`](/Users/eliasdzobo/Desktop/local-model-service/model)

Your available local models:

- `Qwen3-0.6B`
- `functiongemma-270m-it`
- `pythia-70m`
- `all-MiniLM-L6-v2`
- `whisper-tiny`

## 1. Guiding Philosophy

We will learn inference engineering in this order:

1. What inference is
2. Why inference is hard
3. Where latency and cost come from
4. How model architecture shapes serving behavior
5. How hardware constrains software
6. How runtimes and servers exploit those constraints
7. How production systems turn a fast model into a reliable service

The rule for this curriculum is simple:

- theory first
- measurement second
- implementation third

That means we do not begin with Triton commands or deployment YAML. We begin with the abstractions that make those tools make sense.

## 2. What You Should Be Able to Do by the End

By the end of this curriculum, you should be able to:

- explain inference as a systems problem rather than only a modeling problem
- reason about latency, throughput, utilization, batching, and tail behavior
- explain why different model families create different serving bottlenecks
- evaluate when Triton is the right serving layer and when a specialized LLM runtime is better
- design a simple but principled inference architecture for text, embeddings, and speech
- discuss production inference in terms of runtime, infrastructure, and developer tooling

## 3. Course Structure

This is a 10-lesson sequence. Each lesson has:

- theory goal
- core reading
- concepts to master
- discussion questions
- optional practice

The optional practice is intentionally light. It exists to ground the theory, not to dominate the learning.

## 4. Lesson Sequence

### Lesson 1: What Inference Engineering Is

Theory goal:

- build the top-level mental model for the field

Core reading:

- Chapter 0
- Preface

Concepts to master:

- training vs inference
- inference as runtime + infrastructure + tooling
- why generative AI inference is fundamentally harder than classic ML inference
- why open models make inference engineering strategically important

Discussion questions:

- Why is inference not just "running the model"?
- Why do product requirements matter before serving architecture choices?
- Why did open models make inference engineering more important rather than less?

Optional practice:

- Inspect the local model folders and classify them by modality only

Mastery checkpoint:

- You can explain inference engineering to another engineer in under three minutes without using buzzwords.

### Lesson 2: Product Constraints Before Systems Design

Theory goal:

- learn to reason from application requirements backward into serving needs

Core reading:

- Chapter 1

Concepts to master:

- online vs offline inference
- AI-native application design
- consumer vs B2B requirements
- latency budgets
- throughput needs
- cost sensitivity
- quality thresholds

Discussion questions:

- What changes when a model is user-facing and interactive instead of offline and batched?
- Why can the "best" model be the wrong deployment choice?
- How do product constraints narrow runtime choices before any implementation starts?

Optional practice:

- Write a one-page brief for a hypothetical app using one of your local models

Mastery checkpoint:

- You can argue for a model-serving choice using product constraints, not just model intelligence.

### Lesson 3: Neural Networks as Inference Workloads

Theory goal:

- understand what a model server is actually computing

Core reading:

- Chapter 2 sections 2.1 to 2.2

Concepts to master:

- linear layers
- matmul
- activations
- transformer blocks
- attention
- causal decoding
- prefill vs decode

Discussion questions:

- Why is matmul such a central operation in inference?
- Why does autoregressive generation behave differently from encoder-style inference?
- Why is prefill a different systems problem from decode?

Optional practice:

- Compare the architectures listed in your local model configs

Mastery checkpoint:

- You can explain the difference between encoder inference and autoregressive decoding clearly.

### Lesson 4: Bottlenecks, Arithmetic Intensity, and Why Latency Happens

Theory goal:

- move from architecture vocabulary to performance reasoning

Core reading:

- Chapter 2 sections 2.3 to 2.5

Concepts to master:

- arithmetic intensity
- ops-to-byte ratio
- memory bandwidth
- compute-bound vs memory-bound workloads
- attention bottlenecks
- why sequence length matters

Discussion questions:

- Why do some optimizations reduce compute but not wall-clock latency?
- Why can a model with fewer parameters still feel slow?
- Why does long context change serving economics?

Optional practice:

- Estimate which of your local models are likely to be memory-bound vs compute-bound

Mastery checkpoint:

- You can reason about bottlenecks without needing to run a benchmark first.

### Lesson 5: Hardware as the Shape of the Problem

Theory goal:

- understand how hardware defines the feasible optimization space

Core reading:

- Chapter 3

Concepts to master:

- GPU compute
- memory hierarchy
- bandwidth
- accelerator generations
- instance sizing
- local vs datacenter inference

Discussion questions:

- Why is memory capacity not the same as memory bandwidth?
- Why can a faster accelerator fail to improve user experience if the workload is mismatched?
- How do hardware constraints shape model selection?

Optional practice:

- Build a simple placement table for your local models: CPU, laptop GPU, server GPU

Mastery checkpoint:

- You can explain why hardware choice is a first-order inference decision.

### Lesson 6: Software Layers From CUDA to Serving Engines

Theory goal:

- understand the stack that turns weights into a service

Core reading:

- Chapter 4 sections 4.1 to 4.3

Concepts to master:

- CUDA as the low-level execution layer
- frameworks vs runtimes
- model formats
- ONNX Runtime
- TensorRT
- vLLM
- SGLang
- TensorRT-LLM
- Triton as a serving layer

Discussion questions:

- What is the difference between a framework, an inference engine, and an inference server?
- Why are there multiple serving stacks instead of one universal stack?
- Why might Triton be excellent for some workloads and awkward for others?

Optional practice:

- Draw a stack diagram showing where Triton, TensorRT, PyTorch, and vLLM sit

Mastery checkpoint:

- You can place Triton correctly in the software stack and explain its role without oversimplifying it.

### Lesson 7: Why Triton Exists

Theory goal:

- learn Triton conceptually before touching deployment details

Core reading:

- Chapter 4 sections 4.3 to 4.5
- revisit Chapter 0 with Triton in mind

Concepts to master:

- model repository abstraction
- backend abstraction
- request scheduling
- batching
- multi-model serving
- observability surface
- why a general inference server is useful

Discussion questions:

- What problem does Triton solve that plain Python model serving does not?
- Why is Triton often a better educational tool for systems thinking than a hand-written Flask server?
- Why do LLM-focused teams still sometimes bypass Triton in favor of specialized runtimes?

Optional practice:

- Read Triton docs later, but only after you can answer the questions above from first principles

Mastery checkpoint:

- You can defend when you would and would not choose Triton.

### Lesson 8: Core Optimization Techniques

Theory goal:

- understand the major levers used to improve inference

Core reading:

- Chapter 5

Concepts to master:

- quantization
- batching
- cache reuse
- speculative decoding
- tensor and expert parallelism
- disaggregation

Discussion questions:

- Which techniques target latency, which target throughput, and which target capacity?
- Why do optimization techniques create tradeoffs instead of free wins?
- Why is quality evaluation inseparable from performance optimization?

Optional practice:

- For each technique, write one sentence on when it helps and one sentence on what it risks

Mastery checkpoint:

- You can explain optimization tradeoffs, not just list optimization names.

### Lesson 9: Modalities Beyond Text

Theory goal:

- understand that inference is not one workload but a family of workloads

Core reading:

- Chapter 6

Concepts to master:

- embeddings
- ASR
- VLMs
- TTS
- image generation
- modality-specific latency patterns

Discussion questions:

- Why are embeddings often a very different serving problem from autoregressive LLMs?
- Why does ASR need different optimization thinking than chat inference?
- Why is it dangerous to generalize from LLM serving to all inference engineering?

Optional practice:

- Map your local models to likely serving patterns and failure modes

Mastery checkpoint:

- You can compare text generation, embeddings, and speech inference without collapsing them into the same design.

### Lesson 10: Production as Systems Thinking

Theory goal:

- connect runtime speed to service reliability and operational reality

Core reading:

- Chapter 7

Concepts to master:

- containerization
- autoscaling
- concurrency
- cold starts
- routing
- load balancing
- observability
- client overhead
- deployment safety

Discussion questions:

- Why is a fast model not necessarily a good production service?
- Why does client behavior matter to end-to-end latency?
- Why are reliability and rollback part of inference engineering rather than just DevOps?

Optional practice:

- Draft a production checklist for one hypothetical inference API

Mastery checkpoint:

- You can describe production inference as a reliability discipline, not only a speed discipline.

## 5. Triton-Specific Theory Track

Since you explicitly want to learn Triton, here is the order I recommend for understanding it conceptually.

### Stage 1: Triton in the Stack

Learn:

- Triton is a serving system, not the model itself
- Triton separates model packaging from request handling
- Triton exposes scheduling, batching, metrics, and backend integration as first-class concepts

Questions to answer:

- What does Triton abstract away?
- What does Triton deliberately leave exposed?

### Stage 2: Triton as a General-Purpose Inference Server

Learn:

- Triton is strongest when multiple model types and backends need one serving surface
- Triton shines for embeddings, ASR, CV, and ensemble-style pipelines
- Triton can host LLM-related workflows, but LLM-specialized runtimes often outperform generic paths

Questions to answer:

- Why is Triton a better fit for some modalities than others?
- What does "general-purpose" buy you operationally?

### Stage 3: Triton Scheduling Model

Learn:

- request concurrency
- dynamic batching
- instance groups
- throughput vs latency tradeoffs

Questions to answer:

- Why does batching help some workloads more than others?
- Why can batching damage interactivity?

### Stage 4: Triton and Specialized LLM Engines

Learn:

- Triton is not the whole LLM story
- vLLM and TensorRT-LLM exist because LLM serving has unique runtime needs
- a mature inference engineer compares layers instead of treating tools as mutually exclusive religions

Questions to answer:

- When is Triton the right front door?
- When is a specialized engine the real core of the system?

## 6. Minimal Practice Policy

Practice enters only when theory needs grounding.

We will use your local models for these limited checkpoints:

- `pythia-70m` to illustrate autoregressive decoding
- `Qwen3-0.6B` and `functiongemma-270m-it` to compare small LLM serving choices
- `all-MiniLM-L6-v2` to study embedding inference and batching
- `whisper-tiny` to study modality differences and pipeline design

Hands-on work should answer theory questions such as:

- What is different about embedding inference versus generation?
- Why does batching help one workload more than another?
- Why would Triton be a strong fit for one model and not another?

## 7. Reading Order

Use this sequence:

1. Preface
2. Chapter 0
3. Chapter 1
4. Chapter 2
5. Chapter 3
6. Chapter 4
7. Chapter 5
8. Chapter 6
9. Chapter 7

Do not rush into external tooling until Chapters 0 through 4 feel conceptually solid.

## 8. What We Should Do Next

The best next step is not to build Triton infrastructure yet.

The best next step is:

- Lesson 1 as a real theory lesson

That means our next session should cover:

- what inference engineering is
- why it emerged as a distinct field
- the three-layer model of runtime, infrastructure, and tooling
- why open models changed the economics and strategy of serving

If you want, I can turn the next reply into `Lesson 1` and teach it like an actual class: explanation first, then a short set of reflection questions, then a tiny optional exercise. 
