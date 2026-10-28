import json, pathlib, zipfile
ROOT=pathlib.Path(__file__).parent
weeks=[
{'title':'Foundations, without the fog','short':'LLM & ML foundations','desc':'Build the mental models and typed contracts behind a reliable AI feature.','project':'A typed support-answer service','deliver':'A versioned prompt, validated answer contract, 20-case fixture set, and model-selection decision record.','icon':'01','color':'#e8efcc'},
{'title':'Give your model a library','short':'RAG & retrieval','desc':'Turn your Supabase knowledge base into a permission-aware evidence pipeline.','project':'A cited knowledge assistant','deliver':'A document ingestion pipeline, hybrid search, citation checks, and a retrieval benchmark.','icon':'02','color':'#d9e8ee'},
{'title':'From answers to actions','short':'Agents, MCP & multimodal','desc':'Build bounded tool loops, inspect agent harnesses, and add multimodal evidence.','project':'A bounded support agent','deliver':'A read-only agent, tool contracts, approval-bound action mock, checkpoint log, and multimodal intake.','icon':'03','color':'#f3dfcb'},
{'title':'Make quality measurable','short':'Evals & observability','desc':'Replace demo confidence with datasets, traces, and regression gates.','project':'An evaluation workbench','deliver':'A stratified dataset, deterministic and judge graders, a trace viewer design, and a release gate.','icon':'04','color':'#e5dff0'},
{'title':'Ship under real constraints','short':'Reliability, security & cost','desc':'Design for failure, tenant boundaries, token budgets, and operational recovery.','project':'A hardened service boundary','deliver':'Timeout and retry policies, adversarial tests, tenant isolation tests, a cost model, and an operations runbook.','icon':'05','color':'#f1e4b6'},
{'title':'Build it. Defend it. Explain it.','short':'System design & capstone','desc':'Integrate the system, demonstrate tradeoffs, and practice engineering interviews.','project':'A production design portfolio','deliver':'A reproducible support copilot demo, architecture document, eval report, threat model, and interview walkthrough.','icon':'06','color':'#d5e6dd'}]
refs={
'ml':['Google · Machine Learning Crash Course','https://developers.google.com/machine-learning/crash-course','ML fundamentals, loss, generalization and data splits.'],
'attention':['Vaswani et al. · Attention Is All You Need','https://arxiv.org/abs/1706.03762','The original Transformer paper; read architecture and attention before the experimental details.'],
'pg':['pgvector · Project documentation','https://github.com/pgvector/pgvector','Distance operators, exact versus approximate search and index behavior.'],
'hybrid':['Supabase · Hybrid search','https://supabase.com/docs/guides/ai/hybrid-search','Postgres full-text search, vectors and reciprocal rank fusion.'],
'rls':['Supabase · Row Level Security','https://supabase.com/docs/guides/database/postgres/row-level-security','Database-enforced authorization and policy behavior.'],
'agents':['Anthropic · Building effective agents','https://www.anthropic.com/research/building-effective-agents','Foundational workflow patterns; tooling details may evolve.'],
'mcp':['MCP · Architecture overview','https://modelcontextprotocol.io/docs/learn/architecture','Protocol roles and primitives. Select the spec version used by your implementation.'],
'evals':['OpenAI · Evaluation best practices','https://developers.openai.com/api/docs/guides/evaluation-best-practices','Dataset construction and evaluation process.'],
'otel':['OpenTelemetry · Traces','https://opentelemetry.io/docs/concepts/signals/traces/','Spans, parent-child relationships and request context.'],
'owasp':['OWASP · GenAI security project','https://owasp.org/www-project-top-10-for-large-language-model-applications/','Threat taxonomy and mitigation starting points.'],
'next':['Next.js · Data security','https://nextjs.org/docs/app/guides/data-security','Server boundaries, data access and minimizing exposed information.'],
'pages':['GitHub · Pages quickstart','https://docs.github.com/en/pages/quickstart','Static publishing from a repository.'],
'vercel':['Vercel · Deployments','https://vercel.com/docs/deployments','Deploying and managing a static project.'],
'netlify':['Netlify · Create deploys','https://docs.netlify.com/deploy/create-deploys/','Manual and repository-driven static deployments.']}
lessons=[]
def add(w,title,summary,concepts,decision,steps,check,code,q,refs_,lang='TypeScript'):
 lessons.append(dict(id=len(lessons)+1,week=w,title=title,summary=summary,concepts=concepts,decision=decision,steps=steps,check=check,code=code,quiz=q,refs=refs_,lang=lang))
def Q(question,options,answer,explanation):return dict(question=question,options=options,answer=answer,explanation=explanation)
add(1,'The AI engineering stack','Locate the model inside a system you can test, secure, and operate.',[
'An AI feature is a software pipeline with a probabilistic component. The model proposes text or actions; your application owns identity, authorization, retrieval, validation, execution and recovery. A fluent answer is an observation, not proof of correctness. Define what a useful result means before selecting a provider.',
'For your existing stack, keep the browser as the interaction layer, a Next.js server boundary as the policy layer, and Supabase as the source of authorized business data. An adapter translates your internal request contract to a model API. That separation lets you replay stored fixtures and change providers without rewriting the product.',
'Start with a narrow support question: explain a refund policy using approved documents. Track grounded correctness, refusal on unsupported questions, latency and cost per successful answer. Compare against a keyword-search page; an LLM is justified only if it improves an actual user task.'
], 'Use a deterministic workflow until there is evidence that model-directed branching is necessary.',
['Sketch browser → authenticated route → retriever → model adapter → validator → response.','Write 10 supported and 10 unsupported refund questions as JSON fixtures.','Define success, failure and abstention for each case.'], 'You can trace every output to a source and name the component responsible for each failure.',
'''type Answer = { text: string; citations: string[]; abstained: boolean };
type Ask = { question: string; userId: string };
interface ModelPort {
  answer(input: { question: string; evidence: string[] }): Promise<Answer>;
}
// An offline fixture implements the same port as an online provider.
const fixture: ModelPort = {
  async answer() {
    return { text: "No supporting evidence.", citations: [], abstained: true };
  }
};''', [Q('Who must enforce permission to read a document?',['The model prompt','The application and database','The user’s browser only'],1,'Authorization must hold even if the model ignores instructions or requests an unexpected document.'),Q('What is the best first baseline?',['A useful deterministic solution','A multi-agent system','The largest available model'],0,'A simple baseline establishes whether added model complexity creates measurable value.')],['next','evals'])
add(1,'ML essentials: loss, splits & leakage','Understand learning and generalization without needing to train a frontier model.',[
'Supervised learning fits parameters to minimize a loss over examples. For classification, cross-entropy penalizes assigning low probability to the correct class. Training loss measures fit to observed data; validation loss estimates behavior on held-out examples used during development. A final test split should remain untouched until a decision is ready.',
'Generalization is performance on the population you will actually serve. Random splits can hide leakage: near-duplicate tickets, later messages from the same conversation, or a document created after a question was asked. Split by customer, conversation or time when those boundaries match deployment.',
'Accuracy alone can hide costly failures. If only 2% of tickets require escalation, predicting “no escalation” always achieves 98% accuracy. Inspect precision, recall and false-negative cost. Fine-tuning, prompting and retrieval experiments all need the same separation between examples used to design the system and examples used to judge it.'
], 'Choose splits and metrics to mirror the production decision, not to maximize a headline score.',
['Create a 30-row ticket dataset with ticketId, customerId, date and escalation label.','Split by customer, then compare with a random split. Identify possible leakage.','Compute precision and recall for an always-negative baseline and a simple rule.'], 'Your report explains why an apparently high accuracy can still fail the business requirement.',
'''function metrics(tp: number, fp: number, fn: number) {
  return {
    precision: tp + fp ? tp / (tp + fp) : 0,
    recall: tp + fn ? tp / (tp + fn) : 0
  };
}
console.log(metrics(8, 2, 4)); // precision .8; recall .667''', [Q('Why split by conversation?',['It makes training faster','To keep related messages out of both train and test','To guarantee perfect accuracy'],1,'Related messages can leak answers across splits and inflate measured generalization.'),Q('Which metric highlights missed escalations?',['Recall for escalation','Token count','Overall accuracy alone'],0,'Recall is true positives divided by all actual positives; low recall means escalations are missed.')],['ml'])
add(1,'Tokens, embeddings & vector intuition','Connect text representations to limits, similarity and retrieval.',[
'Tokenizers map text to integer identifiers, often using subword pieces. Tokens are neither words nor characters. Code, unusual names and non-English text can have different token-to-character ratios. Context budgets include instructions, tool schemas, history, retrieved text and the output allowance; count with the selected model’s tokenizer when precision matters.',
'An embedding maps an input into a numeric vector optimized for a training objective. Similar meaning often produces nearby vectors, but similarity is not entailment or permission. Two contradictory statements can be semantically close. Never treat a high similarity score as proof that a chunk answers the question.',
'Cosine similarity is the dot product divided by the product of vector norms. Dot product also reflects vector magnitude unless embeddings are normalized. Store embedding model identifier, dimensions and content version with each vector. Switching models generally requires re-embedding the corpus, even if the dimensions happen to match.'
], 'Use embedding similarity to generate candidates; evaluate answer support separately.',
['Calculate cosine similarity for [1,0], [1,1] and [-1,0].','Budget a 16,000-token request with 2,000 output tokens and 3,000 instruction/history tokens.','Write migration steps for changing an embedding model without mixing vector spaces.'], 'You reserve 11,000 tokens for evidence and other input, and can explain why a contradictory chunk may rank highly.',
'''function cosine(a: number[], b: number[]) {
  if (a.length !== b.length) throw new Error("dimension mismatch");
  const dot = a.reduce((s, x, i) => s + x * b[i], 0);
  const norm = (v: number[]) => Math.hypot(...v);
  const denom = norm(a) * norm(b);
  return denom === 0 ? 0 : dot / denom;
}
console.log(cosine([1, 0], [1, 1])); // ~0.707''', [Q('Can equally sized vectors from different models be mixed safely?',['Yes, dimensions are all that matter','No, the learned spaces can differ','Only if both are JSON arrays'],1,'Matching dimensions does not align the embedding spaces.'),Q('A high similarity score proves what?',['The document is authorized','The answer is true','The candidate is close under a learned metric'],2,'Similarity helps rank candidates but does not establish truth, access rights or answer support.')],['pg','ml'])
add(1,'Transformers & generation','Explain attention, inference and sampling at an engineer’s level.',[
'A Transformer builds contextual representations through attention and feed-forward layers. In attention, queries compare with keys to determine a weighted combination of values. A causal decoder cannot attend to future tokens during generation. Positional information helps distinguish sequences that contain the same tokens in a different order.',
'An autoregressive language model predicts a distribution over the next token given the preceding context, emits a token and repeats. Pretraining learns broad statistical structure; later instruction and preference training shape behavior. None of these stages turns generation into a database lookup or a guarantee of factual accuracy.',
'Temperature changes how sharply probabilities are sampled; top-p truncates the candidate distribution by cumulative probability. Lower randomness can improve repeatability but cannot fix missing evidence. A KV cache reuses intermediate attention keys and values while decoding, trading memory for less recomputation. Longer context and longer output can both affect latency and memory.'
], 'Fix task specification and evidence before treating sampling settings as a quality solution.',
['Draw one generation step with context, logits, sampling and appended token.','Explain a KV cache using the analogy of saved intermediate computation.','Use three fixture outputs with different wording to design a grader that accepts equivalent meanings.'], 'You distinguish model parameters, context, sampling controls and runtime caches.',
'''function softmax(logits: number[], temperature = 1) {
  if (temperature <= 0) throw new Error("use argmax for greedy decoding");
  const scaled = logits.map(x => x / temperature);
  const max = Math.max(...scaled);
  const exps = scaled.map(x => Math.exp(x - max));
  const sum = exps.reduce((a, b) => a + b, 0);
  return exps.map(x => x / sum);
}
console.log(softmax([2, 1, 0], 0.5));''', [Q('What does a causal mask prevent?',['Access to future sequence positions','All attention to user text','Use of cached states'],0,'Autoregressive decoding must not use tokens that have not been generated yet.'),Q('Does low temperature guarantee factual answers?',['Yes','No','Only on short requests'],1,'Sampling sharpness does not supply missing knowledge or prevent confidently repeated errors.')],['attention'])
add(1,'Prompt contracts & structured output','Turn an informal instruction into a versioned software interface.',[
'A prompt contract specifies the task, allowed evidence, output structure, refusal behavior and examples. Delimit user input and retrieved documents as untrusted data. State how the assistant should handle unsupported or conflicting evidence. Version prompts alongside code so a behavior change can be attributed and rolled back.',
'Structured generation can constrain syntax, but a syntactically valid object can still contain false statements, nonexistent citations or unsafe actions. Parse the response and validate types, bounds and business rules at the server boundary. Distinguish parse failure, policy refusal and lack of evidence instead of collapsing everything into an empty answer.',
'In a Next.js route, authenticate first, bound request size, retrieve authorized evidence, call a server-side provider adapter and return a minimal response object. Do not send provider credentials to a client component. Treat every model-generated field as untrusted input to later application code.'
], 'A schema is a necessary interface check; domain validation is a separate obligation.',
['Write a prompt with task, evidence, output and abstention sections.','Build a validator for text, citations and abstained; reject unexpected keys.','Test missing fields, fabricated citation IDs and a refusal fixture.'], 'Malformed and unsupported outputs produce explicit typed failures rather than plausible success.',
'''type Answer = { text: string; citations: string[]; abstained: boolean };
function validAnswer(x: unknown, allowed: Set<string>): x is Answer {
  if (!x || typeof x !== "object") return false;
  const a = x as Record<string, unknown>;
  return Object.keys(a).sort().join() === "abstained,citations,text" &&
    typeof a.text === "string" && a.text.length <= 8000 &&
    typeof a.abstained === "boolean" && Array.isArray(a.citations) &&
    a.citations.every(id => typeof id === "string" && allowed.has(id));
}''', [Q('A valid JSON answer contains a nonexistent citation. What failed?',['Nothing; JSON was valid','Domain validation','Tokenization'],1,'Shape validation cannot establish whether citation IDs refer to authorized evidence.'),Q('Where does a provider API key belong?',['In a server-side secret store/environment','In localStorage','In a public client bundle'],0,'Provider credentials must remain behind the server boundary in the application you build.')],['next','evals'])
add(1,'Model selection, RAG or fine-tuning?','Choose the smallest intervention that fixes the observed failure.',[
'Model selection is a constrained experiment: compare candidate configurations on the same held-out tasks, latency budget and cost accounting. Record model identifier, prompt version, parameters and date. Do not choose by a generic leaderboard alone; your distribution may emphasize citations, tool use or specific languages.',
'Prompting clarifies the task. RAG supplies changing or private knowledge at inference time. Fine-tuning adjusts learned behavior from examples, and is useful when repeated behavioral or formatting failures remain after a strong baseline. Fine-tuning is not a reliable replacement for a permission-aware source of frequently changing facts.',
'Build a small Pareto table: quality, p95 latency, cost per successful task and operational constraints. A smaller model may be sufficient for classification while a stronger one handles ambiguous cases. Routing introduces its own classifier errors and maintenance cost; evaluate the complete route, not each model in isolation.'
], 'If the failure is missing current policy text, improve retrieval before collecting tuning examples.',
['Compare three fixture configurations across your 20 support cases.','Classify each error as knowledge, instruction, reasoning, retrieval or validation.','Write a one-page decision record including rejected alternatives and a re-evaluation trigger.'], 'Your week-one service contract and baseline report identify evidence for the next improvement.',
'''type Trial = { name: string; passed: number; total: number; dollars: number };
function summarize(t: Trial) {
  return { name: t.name, passRate: t.passed / t.total,
    costPerSuccess: t.passed ? t.dollars / t.passed : Infinity };
}
console.table([
  summarize({ name: "fixture-A", passed: 16, total: 20, dollars: 0.04 }),
  summarize({ name: "fixture-B", passed: 18, total: 20, dollars: 0.09 })
]);''', [Q('A refund policy changes every week. What is usually the first knowledge strategy?',['Retrieval from versioned current documents','Fine-tune every answer into weights','Increase temperature'],0,'Retrieval can refresh changing knowledge and preserve provenance without retraining.'),Q('Why compare cost per success?',['It includes the impact of failed attempts','It always favors a large model','It replaces safety evaluation'],0,'Cheap failed answers may cost more per useful task once retries and failures are accounted for.')],['evals','hybrid'])
add(2,'Ingestion, chunking & provenance','Make every piece of evidence reproducible and independently addressable.',[
'An ingestion pipeline converts source documents into retrievable units. Preserve source ID, revision, section path, tenant, effective date and extraction method before chunking. A chunk without provenance can be retrieved but cannot support trustworthy citations, deletion or audits. Use stable chunk IDs tied to content version rather than row order.',
'Chunk boundaries should preserve meaning: headings, paragraphs, tables and code fences are better starting points than arbitrary character cuts. Overlap reduces boundary loss but increases duplicate retrieval and embedding cost. Tables often need repeated headers. Measure whether your actual questions can be answered from the resulting chunks.',
'Make ingestion idempotent. Hash normalized content, process only changed revisions, and atomically activate a new document version after its chunks and embeddings are ready. Deleting a source must invalidate both stored chunks and derived caches. Avoid mixing old and new policy versions in a single answer.'
], 'Treat chunking as a retrieval experiment with a version, not a one-time text utility.',
['Prepare three policy documents including a table and a superseded revision.','Chunk by section; store source, revision, section and content hash.','Replay ingestion twice and then delete one source.'], 'The second ingestion creates no duplicates; deletion removes all searchable derived records.',
r'''type Chunk = { id: string; source: string; revision: string;
  section: string; text: string; tenantId: string };
async function contentHash(text: string) {
  const bytes = new TextEncoder().encode(text.replace(/\r\n/g, "\n").trim());
  const digest = await crypto.subtle.digest("SHA-256", bytes);
  return Array.from(new Uint8Array(digest), x => x.toString(16).padStart(2,"0")).join("");
}
// In production: upsert by (source, revision, contentHash).''', [Q('What makes ingestion idempotent?',['Re-running creates the same effective records','Using a larger embedding','Removing source IDs'],0,'Stable version and content keys let retries converge without duplicate chunks.'),Q('Why preserve a section path?',['For meaningful provenance and citations','To improve temperature','To avoid authorization'],0,'A section path connects extracted evidence to its location in the original source.')],['hybrid'])
add(2,'Vector search with Postgres','Understand exact search before adding an approximate index.',[
'Vector search ranks candidate chunks by a distance function. In pgvector, cosine distance uses <=>; smaller distance means closer vectors. Choose an operator and matching operator class consistently. Embedding dimensions must match the model output, and query embeddings must use the same embedding configuration as indexed documents.',
'Exact search compares against the candidate set and provides a useful quality baseline. Approximate indexes such as HNSW trade additional memory and construction work for faster retrieval, with a possible recall loss. Filtered approximate search can return fewer useful candidates if relevant rows are excluded after candidate exploration; inspect plans and recall under real tenant filters.',
'Your SQL function must preserve access policies. A service-role client can bypass RLS; do not assume database policies will filter results in that case. Use an appropriately scoped caller or explicit trusted authorization logic, and test cross-tenant requests against the actual role used in production.'
], 'Benchmark exact search first; choose an approximate index only after measuring scale and recall.',
['Create a small local pgvector table and insert three known vectors.','Run an exact cosine ranking with a tenant predicate.','Compare exact and indexed top-k on 20 fixture queries when a database is available.'], 'Operator, dimensions and access role are documented, and another tenant’s rows never appear.',
'''-- SQL sketch: choose dimensions to match YOUR embedding model.
create extension if not exists vector;
create table chunks (
  id text primary key, tenant_id uuid not null,
  content text not null, embedding vector(3)
);
-- The tenant parameter must come from trusted server authorization.
select id, content, 1 - (embedding <=> '[1,0,0]'::vector) as similarity
from chunks where tenant_id = '00000000-0000-0000-0000-000000000001'
order by embedding <=> '[1,0,0]'::vector limit 5;
-- Teaching schema only: add RLS and policies before exposing it.''', [Q('For cosine distance, which is closer?',['0.1','0.9','Both are probabilities'],0,'Distance is smaller for nearer vectors; it is not a calibrated probability of correctness.'),Q('What should you measure when adding HNSW?',['Recall and latency under real filters','Only table size','Only output length'],0,'Approximate search and filtering can change the candidate set, so compare against an exact baseline.')],['pg','rls'],'SQL')
add(2,'Hybrid search & rank fusion','Recover exact identifiers as well as semantically related questions.',[
'Keyword retrieval excels at exact strings such as invoice IDs, error codes and product names. Dense embeddings help with paraphrases that share little vocabulary. A hybrid system runs both retrieval paths over the authorized corpus and combines candidates before optional reranking.',
'Reciprocal rank fusion combines ranks rather than raw, incompatible score scales. A common form sums 1/(k + rank) across lists, with ranks starting at one. The smoothing constant k controls how much top positions dominate. Deduplicate by stable chunk ID before building the final context.',
'Hybrid retrieval is not automatically better. Tune candidate counts, fusion weights and smoothing on held-out questions. Inspect cases where keyword search should win, where semantic search should win, and where neither can answer. Log rank positions and chunk versions so you can diagnose why a source was selected.'
], 'Fuse ranks when scoring scales differ; validate gains on exact-code and paraphrase slices separately.',
['Create two ranked lists with overlapping IDs and compute fusion scores.','Build six exact-identifier and six paraphrase questions.','Compare keyword, vector and fused recall@5; record the failures.'], 'Your report shows per-slice gains or explains why the simpler retriever should remain.',
'''function rrf(lists: string[][], k = 60) {
  const scores = new Map<string, number>();
  for (const list of lists) {
    [...new Set(list)].forEach((id, i) =>
      scores.set(id, (scores.get(id) ?? 0) + 1 / (k + i + 1)));
  }
  return [...scores].sort((a, b) => b[1] - a[1]);
}
console.log(rrf([["A","B","C"], ["B","D","A"]]));''', [Q('Why fuse ranks instead of raw scores?',['Keyword and vector score scales differ','Ranks guarantee truth','It removes the need for access checks'],0,'Ranks provide a common basis when score magnitudes are not comparable.'),Q('Which query especially benefits from keyword search?',['ERR_AUTH_041','An open-ended paraphrase','Every query equally'],0,'Rare exact identifiers are often strong lexical matches and weak semantic signals.')],['hybrid'])
add(2,'Query planning, reranking & context','Improve candidate selection without losing the user’s original intent.',[
'Query rewriting can expand abbreviations or turn a follow-up into a standalone question, but can also erase constraints. Keep the original query, preserve identifiers and tenant filters, and evaluate rewrites separately. A rewrite is another probabilistic step that can fail before retrieval begins.',
'A reranker scores a smaller candidate set using the query and document together. This can improve relevance after broad retrieval, at a latency and cost penalty. Retrieval recall sets an upper bound: reranking cannot recover an answer-bearing document that never entered the candidate pool.',
'Context assembly is a packing problem. Select diverse, relevant chunks under a token budget, collapse overlap and carry citation IDs. Put policy instructions outside untrusted evidence and label evidence boundaries. More context can add contradictions and distraction; compare answer quality rather than assuming that a full window is always better.'
], 'Improve candidate recall before spending on reranking, then measure final answer quality.',
['Write a follow-up query that loses a product ID when naively rewritten.','Pack ranked chunks into a fixed budget; remove duplicate source spans.','Compare a top-3 and top-8 context using the same answer fixtures.'], 'You can explain a missed answer as retrieval, reranking or context-packing failure.',
'''type Hit = { id: string; tokens: number; source: string };
function pack(hits: Hit[], budget: number): Hit[] {
  const chosen: Hit[] = [], seen = new Set<string>();
  let used = 0;
  for (const hit of hits) {
    if (seen.has(hit.id) || used + hit.tokens > budget) continue;
    chosen.push(hit); seen.add(hit.id); used += hit.tokens;
  }
  return chosen;
} // Greedy baseline: extend with diversity and span deduplication.''', [Q('Can reranking recover a missing candidate?',['Yes, always','No','Only with temperature zero'],1,'A reranker orders available candidates; it cannot rank an absent document.'),Q('Why retain the original query?',['To audit rewrite drift and preserve constraints','To double all costs','To bypass context limits'],0,'A rewritten question can accidentally alter identifiers, scope or intent.')],['hybrid','evals'])
add(2,'Grounding, citations & abstention','Make evidence support observable rather than cosmetic.',[
'A citation is a link between a claim and an authorized source span. Validate that the referenced chunk exists, was supplied to this generation, is current and actually supports the claim. Existence checks are deterministic; support may require manual review or an evaluated entailment grader. A correct citation ID can still decorate a fabricated statement.',
'Grounded answers should distinguish what the evidence says from inference. For conflicting revisions, prefer a documented effective-date policy or abstain and surface the conflict. When evidence is missing, an explicit “I cannot determine this from the available sources” is a successful outcome if the task requires groundedness.',
'Do not choose a universal similarity threshold and call it confidence. Retrieval scores vary by model, corpus and query. Calibrate abstention on representative supported and unsupported questions, and measure both unsupported-answer rate and unnecessary refusal rate. A system that refuses every question is safe on one axis and useless on another.'
], 'Evaluate answer support and useful coverage together.',
['Label 10 answer claims with supporting spans, including two misleading citations.','Add unsupported and contradictory questions to your dataset.','Define an abstention policy and measure both false answers and avoidable refusals.'], 'Every factual claim in a sample answer has support, or the answer clearly abstains.',
'''function citationIdsValid(ids: string[], supplied: Set<string>) {
  return ids.length > 0 && ids.every(id => supplied.has(id));
}
const supplied = new Set(["refund-v3:section2"]);
console.log(citationIdsValid(["refund-v2:section2"], supplied)); // false
// Passing this check does NOT prove the cited text entails the answer.
// Keep a separate claim-to-span support evaluation.''', [Q('Does a real citation ID prove support?',['No; the cited content may not support the claim','Yes','Only if it is a UUID'],0,'Citation validity and claim entailment are distinct checks.'),Q('Why measure avoidable refusals?',['A system can appear safe by refusing everything','Refusals are always errors','To remove source checking'],0,'Useful coverage matters alongside the rate of unsupported answers.')],['evals','hybrid'])
add(2,'RAG evaluation & weekly build','Separate search quality from generation quality.',[
'Retrieval recall@k is the fraction of relevant items recovered in the top k, assuming your relevance labels are sufficiently complete. Hit rate asks whether at least one relevant item was found. MRR rewards placing the first relevant item early. None of these directly measures whether the final answer is correct or appropriately grounded.',
'Build a question-to-source benchmark with answerable, unanswerable, ambiguous, exact-code and cross-tenant cases. Score retrieval first using fixed labels, then generation using fixed evidence, then the end-to-end pipeline. This decomposition prevents you from blaming a model for an ingestion bug or a poor retriever for an answer that ignores good evidence.',
'For the weekly project, combine your Next.js boundary, Supabase search design, context packer and answer validator. The offline version can use JSON fixtures for every component; switching to live embeddings and a database is an optional integration step. Record limitations of a small benchmark and keep some questions held out.'
], 'Use component tests to locate failure, and end-to-end tests to decide whether users benefit.',
['Label 20 questions with relevant source IDs; keep five held out.','Compute hit rate@5 and MRR for your retrieval fixtures.','Deliver five cited answers, three abstentions and one denied cross-tenant query.'], 'Your week-two report includes component metrics, final answer review and a list of known failure cases.',
'''function reciprocalRank(ranked: string[], relevant: Set<string>) {
  const index = ranked.findIndex(id => relevant.has(id));
  return index < 0 ? 0 : 1 / (index + 1);
}
const cases = [
  reciprocalRank(["x","a","b"], new Set(["a"])),
  reciprocalRank(["z"], new Set(["b"]))
];
console.log(cases.reduce((s, v) => s + v, 0) / cases.length); // MRR .25''', [Q('Retrieval finds good evidence but the answer invents a policy. Inspect what first?',['Generation and grounding','Embedding dimensions only','CSS'],0,'The evidence was available; the failure occurs in using or validating it.'),Q('MRR emphasizes what?',['The rank of the first relevant result','All output tokens','Database size'],0,'Reciprocal rank is 1 divided by the position of the first relevant item, or zero if none exists.')],['evals','hybrid'])
add(3,'Workflows versus agents','Choose where the model may decide what happens next.',[
'A workflow follows code-defined steps and branches. An agent uses a model to choose some next actions from available tools based on observations. Both can call models multiple times. The practical distinction is who controls the route through the task, not whether the product has a chat interface.',
'Use workflows when the sequence is known: classify a ticket, retrieve policy, draft an answer, validate it. Introduce a bounded agent when tasks need variable investigation, such as deciding which read-only account lookup to perform next. More autonomy increases the number of possible failure paths and complicates evaluation.',
'Start by writing the allowed state transitions. Separate planning, tool proposal, authorization, execution and result interpretation. A model proposal is never permission. For support, permit reading authorized ticket metadata and policy search; require explicit application approval before a refund or outbound message.'
], 'Grant autonomy only to the part of the task that benefits from adaptive decisions.',
['Draw a fixed ticket-triage workflow and a variable investigation loop.','List allowed tools and mark each read-only or mutating.','Create a case where a fixed workflow is cheaper and easier to audit.'], 'Your design identifies who chooses each transition and which actions require approval.',
'''type State = "retrieve" | "draft" | "validate" | "done";
const next: Record<State, State[]> = {
  retrieve: ["draft"], draft: ["validate"],
  validate: ["done", "retrieve"], done: []
};
function transition(from: State, to: State) {
  if (!next[from].includes(to)) throw new Error("invalid transition");
  return to;
}''', [Q('What distinguishes an agent here?',['The model selects some next actions','A chat window','Use of TypeScript'],0,'Agentic control lets the model decide the next action within a bounded tool and policy environment.'),Q('Does a model requesting a refund authorize it?',['No','Yes','Only if JSON is valid'],0,'Execution permission must come from the application’s policy and approval process.')],['agents'])
add(3,'Tool contracts & safe execution','Treat tool calls as untrusted requests to a typed API.',[
'A tool definition needs an unambiguous name, a narrow purpose, argument schema, permissions and a predictable result format. Prefer get_ticket over a generic run_sql tool. Descriptions should explain when a tool is appropriate, but server code must enforce constraints independently of that description.',
'Validate all arguments, derive user and tenant identity from the authenticated execution context, and authorize each resource. Bound result sizes so a tool cannot fill the context window with irrelevant data. Return explicit typed errors such as not_found, denied and retryable_unavailable so the agent can respond appropriately.',
'Mutating tools need idempotency keys, a preview of exact effects and a commit boundary. Bind approval to the action arguments and resource version; changing the amount or target invalidates it. Tool outputs may contain attacker-controlled content, so they remain evidence rather than instructions.'
], 'Use narrow capabilities and enforce policy inside the executor.',
['Define get_ticket with one bounded ticket ID argument.','Test invalid IDs, unauthorized IDs and oversized responses.','Design a refund preview whose approval is invalidated if the target or amount changes.'], 'A forged tenantId in tool arguments cannot change the authenticated scope.',
'''type Context = { tenantId: string; userId: string };
function parseTicketArgs(x: unknown): { ticketId: string } {
  if (!x || typeof x !== "object") throw new Error("invalid args");
  const a = x as Record<string, unknown>;
  if (Object.keys(a).length !== 1 || typeof a.ticketId !== "string" ||
      !/^T-[0-9]{1,8}$/.test(a.ticketId)) throw new Error("invalid args");
  return { ticketId: a.ticketId };
}
// Executor: authorize(ctx, ticketId), then query using ctx.tenantId.
// Never accept a tenant identifier supplied by the model as authority.''', [Q('Which tool is easier to constrain?',['get_ticket(ticketId)','run_arbitrary_sql(sql)','execute_anything(command)'],0,'A narrow API exposes less authority and has clearer validation and evaluation boundaries.'),Q('What should determine tenant scope?',['Authenticated execution context','Model arguments','A document instruction'],0,'Model-generated identity fields are not trusted authorization context.')],['agents','rls','owasp'])
add(3,'Build a bounded agent loop','Implement stopping conditions, typed failures and a traceable trajectory.',[
'An agent loop alternates model decisions with tool observations until it returns an answer or reaches a boundary. Bound steps, wall-clock duration, token usage, tool result size and allowed tools. A step cap alone cannot prevent one slow call from exhausting the user’s deadline.',
'Keep a trajectory containing decision metadata, tool name, validated arguments, observation summary and terminal reason. Do not depend on private reasoning text; observable actions and outputs are enough to audit the system. Feed tool results back using the provider’s required message identifiers and schema in a live implementation.',
'Stopping is a product behavior. If the budget is exhausted, return a partial result with a clear limitation or escalate. Do not silently treat exhaustion as success. Test repeated identical tool calls, hallucinated tool names, malformed arguments, unavailable dependencies and a model that never chooses to finish.'
], 'Budget the whole run and make every terminal state explicit.',
['Implement the loop with a deterministic fixture decision function.','Use a fixture that requests the same tool forever.','Inject one tool timeout and verify a bounded terminal result.'], 'All scenarios terminate and the trace distinguishes completion, denial, budget exhaustion and failure.',
'''// Pseudocode: decide and execute are your validated adapters.
async function run(decide: Function, execute: Function, signal: AbortSignal) {
  const history: unknown[] = [];
  for (let step = 0; step < 6; step++) {
    signal.throwIfAborted();
    const decision = await decide(history, signal);
    if (decision.kind === "final") return { status: "done", value: decision.value };
    const observation = await execute(decision, signal);
    history.push({ decision, observation });
  }
  return { status: "budget_exhausted" };
} // Pass a deadline signal through ALL adapters.''', [Q('Why is a step limit insufficient?',['A single call can hang','It forbids tools','It guarantees low cost'],0,'Wall-clock and per-call deadlines are also needed to bound execution time.'),Q('What is budget exhaustion?',['An explicit terminal outcome','Automatically a successful answer','A reason to loop forever'],0,'Clients and evaluators need to distinguish completed work from an incomplete run.')],['agents','otel'])
add(3,'MCP architecture & trust boundaries','Understand the protocol without mistaking interoperability for authorization.',[
'MCP standardizes interaction between an AI application and external capabilities. The host manages the user experience and policy; protocol clients connect to servers exposing capabilities such as tools and other supported primitives. A server description helps discovery but does not establish that its code or returned content is trustworthy.',
'Pin the protocol revision and SDK version used by your integration. Protocol details evolve, so use the official architecture and specification for the selected revision. Negotiate supported capabilities and validate messages instead of assuming every server behaves like a local function.',
'For a support copilot, expose a read-only policy-search capability behind authenticated server access. Review server identity, scopes, transport security, data egress and tool descriptions. Keep authorization at the resource boundary and treat server results as untrusted input. MCP supplies a connection contract; your harness still owns approvals, budgets and policy.'
], 'Review an MCP server as a new integration with its own authority and data exposure.',
['Map host, client and server in your support architecture.','Write a capability inventory including data sent to each server.','Create a mock tool result containing an instruction to leak data; verify it is treated as data.'], 'Your integration review pins a spec revision and identifies both authorization and content trust boundaries.',
'''// Conceptual capability adapter, NOT an MCP wire implementation.
type SearchInput = { query: string; limit: number };
function constrainSearch(x: SearchInput) {
  if (!x.query.trim() || x.query.length > 500) throw new Error("query bounds");
  return { query: x.query, limit: Math.min(10, Math.max(1, x.limit)) };
}
// Use the official SDK for negotiation, transport and message handling.
// Map its tool request into your existing authorized executor.''', [Q('Does MCP make every server trustworthy?',['No; trust and authorization still need review','Yes, by standardization','Only remote servers'],0,'Interoperability defines how systems communicate, not which data or actions they should be trusted with.'),Q('What belongs in an integration record?',['Pinned protocol revision and data/permission scope','Only the tool name','Only a screenshot'],0,'Versioning and authority boundaries are essential to reproduce and review an integration.')],['mcp','owasp'])
add(3,'Multimodal intake & extraction','Preserve provenance and uncertainty when evidence is an image or audio.',[
'Multimodal systems can consume images, audio or video, but the product still needs typed outputs and validation. A screenshot may contain UI text, a document, or an injected instruction. OCR can misread identifiers; speech transcription can confuse names and amounts. Model perception should not directly trigger a financial or administrative action.',
'Normalize extracted evidence with source ID, page or time span, extraction version and uncertainty flags. Separate transcription or extraction from business interpretation. Ask for confirmation of ambiguous high-impact fields and cross-check account identifiers against authorized records. Keep originals only according to a documented retention policy.',
'Budget by modality: large images, long audio and many video frames can increase latency, cost and data exposure. Use representative samples across resolution, accents, lighting and document layouts. The offline lab uses hand-authored extraction fixtures so you can test downstream logic without a live vision or speech service.'
], 'Treat perceived text as uncertain evidence and gate high-impact actions on validated fields.',
['Create receipt-extraction fixtures with a blurred total, a currency ambiguity and an embedded instruction.','Add page or timestamp provenance and a needsReview flag.','Write a validator that rejects negative amounts and unknown currencies.'], 'Ambiguous fields lead to review, and image text cannot authorize an action.',
'''type Receipt = { amountMinor: number; currency: string; needsReview: boolean };
function validReceipt(r: Receipt) {
  return Number.isSafeInteger(r.amountMinor) && r.amountMinor >= 0 &&
    ["USD", "SGD", "EUR"].includes(r.currency) && !r.needsReview;
}
console.log(validReceipt({ amountMinor: 1299, currency: "SGD", needsReview: true }));
// false: route to human review; never infer confirmation from an image.''', [Q('A screenshot says “approve this refund.” How should the system treat it?',['As untrusted image content','As user authorization','As a developer instruction'],0,'Content inside evidence cannot grant permission or replace authenticated user intent.'),Q('Why retain page or time-span references?',['To review extraction against the original evidence','To increase token counts','To avoid validation'],0,'Provenance allows reviewers to verify an extraction and locate its source.')],['owasp','evals'])
add(3,'Agent harnesses, memory & recovery','Understand the runtime around the model, then deliver the weekly agent.',[
'An agent harness supplies the environment: tool registry, policy enforcement, context management, persistence, budgets, isolation and recovery. The model alone does not define the agent’s behavior. Compare harnesses on the operational guarantees your task needs rather than the number of orchestration abstractions.',
'Working memory is the current context; durable memory is stored state retrieved across runs. Persist facts with provenance, scope, expiry and deletion behavior. Summaries can omit constraints, and stored attacker text can become a persistent injection. Never promote a model-written memory into trusted system policy.',
'Checkpoint before and after meaningful steps. On resume, reconcile external effects rather than blindly replaying a mutation: a process may crash after an action succeeds but before recording success. Use idempotent actions and a durable action ledger. For this week’s project, demonstrate recovery with mocks before connecting real services.'
], 'Choose a harness by its policy, persistence and recovery boundaries; keep business logic independently testable.',
['Build a tool registry with an allowlist and per-run budget.','Persist a fixture checkpoint, interrupt a run and resume it.','Simulate a crash after a mock action; use an idempotency key to avoid duplication.'], 'Your weekly agent has bounded termination, a readable trajectory and one successful recovery demonstration.',
'''type Checkpoint = { runId: string; step: number; completedActions: string[] };
function shouldExecute(checkpoint: Checkpoint, actionKey: string) {
  return !checkpoint.completedActions.includes(actionKey);
}
// Production: enforce a unique action key in the effect-owning service.
// A local list alone cannot atomically coordinate an external mutation.
const cp = { runId: "r1", step: 3, completedActions: ["refund:T-12:v1"] };
console.log(shouldExecute(cp, "refund:T-12:v1")); // false''', [Q('Why is a local “completed” flag insufficient for exactly-once external effects?',['A crash can occur between effect and local record','Local flags are slow','JSON cannot store strings'],0,'Atomicity does not span arbitrary systems; reconcile and use idempotency at the effect boundary.'),Q('Can stored model memory become trusted policy?',['No','Always','Only after summarization'],0,'Persistence does not make generated or retrieved content authoritative.')],['agents','otel','owasp'])
add(4,'Design an evaluation dataset','Turn product requirements and observed failures into representative cases.',[
'An evaluation case contains input, environment or evidence, expected properties and metadata for analysis. For support, include answerable questions, missing evidence, ambiguous policies, unauthorized resources and adversarial documents. Use synthetic examples to expand coverage, but validate that they resemble real tasks and do not only reflect the generator’s assumptions.',
'Stratify cases by risk and behavior, not just topic. Keep development cases separate from a held-out set, and track dataset versions. Production failures can become regression cases after redaction and labeling. Review consent and retention before copying real customer data into test fixtures.',
'A small dataset is a diagnostic instrument, not a statistical guarantee. Ten perfect cases cannot establish a rare failure rate. Record what is absent: languages, tenant sizes, unusual documents and long conversations. Add cases based on failures and distribution shifts while preserving a stable benchmark for comparison.'
], 'Write expected properties before looking at a candidate system’s answers.',
['Create 30 cases with slice, risk, expected source and expected refusal fields.','Reserve 10 held-out cases and document how they were selected.','Review labels with a second pass that ignores candidate outputs.'], 'Every required behavior has a case, and the report explicitly states coverage gaps.',
'''type EvalCase = {
  id: string; input: string; slice: "answerable" | "missing" | "denied";
  expectedSources: string[]; shouldAbstain: boolean;
};
const testCase: EvalCase = {
  id: "missing-01", input: "What is next year's refund policy?",
  slice: "missing", expectedSources: [], shouldAbstain: true
};''', [Q('Why label expectations before reading candidate outputs?',['To reduce anchoring to the model’s answer','To improve latency','To remove all human judgment'],0,'Candidate answers can bias the expected answer and conceal systematic failures.'),Q('What does 10/10 passing establish?',['Performance on those 10 cases','A guaranteed zero failure rate','Universal production quality'],0,'A small sample has limited coverage and uncertainty, especially for rare events.')],['evals'])
add(4,'Deterministic graders & rubrics','Use exact checks where exact checks are meaningful.',[
'Deterministic graders check observable invariants: valid schema, allowed citation IDs, no forbidden tools, tenant isolation, terminal state and budget bounds. They are cheap, reproducible and easy to debug. Exact string equality is appropriate for IDs or enum values but brittle for natural-language answers with many valid phrasings.',
'A rubric defines quality dimensions with anchored examples. Score correctness, groundedness, completeness and tone separately so one high score does not hide a severe failure. For a refund answer, a fabricated deadline may be a hard fail even if the rest of the response is polished.',
'Compose grading as a policy: first hard safety and contract checks, then semantic quality. Store each result and reason rather than just a composite number. Test graders themselves using deliberately good, bad and borderline outputs; an incorrect grader can produce false confidence faster than a model can.'
], 'Keep hard constraints separate from soft quality scores.',
['Write graders for allowed citations, abstention and tool allowlists.','Create three semantically equivalent correct answers to expose brittle exact matching.','Add two intentionally broken outputs and confirm the appropriate grader fails.'], 'The report explains which requirement failed, rather than returning a single unexplained score.',
'''function grade(a: { citations: string[]; abstained: boolean }, expected: {
  allowed: Set<string>; shouldAbstain: boolean
}) {
  return {
    citationsAllowed: a.citations.every(x => expected.allowed.has(x)),
    abstentionCorrect: a.abstained === expected.shouldAbstain
  };
} // Add separate claim-support review for non-abstaining answers.''', [Q('When is exact matching appropriate?',['A required enum or identifier','Every natural-language answer','A tone judgment'],0,'Exact matching is reliable for discrete contracts and often unsuitable for equivalent prose.'),Q('Why retain component grades?',['To diagnose a hidden safety or correctness failure','To inflate the average','To avoid reviewing failures'],0,'Averages can hide a severe failure on a critical dimension.')],['evals'])
add(4,'LLM judges & human calibration','Use model grading as a measured instrument with known failure modes.',[
'A model judge can assess semantic properties such as whether claims follow from supplied evidence. It can also favor verbosity, exhibit position bias, miss subtle errors or follow malicious instructions inside an answer. Give the judge a narrow rubric, evidence and a structured verdict; candidate text remains untrusted data.',
'Calibrate against independently labeled examples. Measure false passes and false failures for each risk slice, not just agreement on easy cases. Randomize answer order for pairwise comparisons and test whether swapping positions changes the verdict. Where possible, use a judge distinct from the generating configuration, while recognizing that models can share biases.',
'Human review is essential for ambiguous or high-impact disagreements. Preserve rubric and judge versions and audit samples over time. Judge rationales are useful review artifacts but are not proof of correctness. Hard authorization and action constraints should remain deterministic, regardless of judge confidence.'
], 'Trust a judge only to the extent supported by calibration on your task.',
['Label 12 answer/evidence pairs yourself before running a judge or mock judge.','Compute a confusion matrix with “bad answer passed” as a key error.','Swap pairwise answer positions and record verdict changes.'], 'You report judge error types and a policy for human escalation.',
'''type Verdict = { humanPass: boolean; judgePass: boolean };
function judgeErrors(rows: Verdict[]) {
  return {
    falsePass: rows.filter(r => !r.humanPass && r.judgePass).length,
    falseFail: rows.filter(r => r.humanPass && !r.judgePass).length
  };
}
// Calibrate separately on injection, unsupported claims and ambiguity.''', [Q('A judge explains its verdict fluently. Is the verdict proven?',['No; it still needs calibration','Yes','Only if it is long'],0,'A plausible explanation can accompany an incorrect judgment.'),Q('Which error is especially important for a safety gate?',['Bad answers receiving a pass','The number of commas','Only false failures'],0,'False passes let unsafe or incorrect outputs through the gate.')],['evals','owasp'])
add(4,'Trace the complete request','Connect evidence, tool calls, versions, latency and outcomes.',[
'A trace represents one request or run as related spans. Create spans for authentication, retrieval, reranking, model calls, tool execution and validation. Correlate asynchronous work with the same run identity. Record durations, status, token usage and version metadata so a slow or incorrect answer can be traced to its cause.',
'Telemetry should explain behavior without collecting everything. Store chunk IDs or redacted summaries rather than unrestricted customer text. Use access controls, retention limits and sampling; never log API keys or approval secrets. A hash can help correlate artifacts but is not a universal anonymization method.',
'Distinguish user-perceived latency, time to first token and full completion time. Streaming may improve responsiveness while total work remains expensive. Observe p50 and p95, error rates and useful completion rate by model and slice. A successful HTTP status alone does not mean the task succeeded.'
], 'Instrument business outcomes and boundaries, not only provider call durations.',
['Draw a trace tree for one RAG answer and one tool-using run.','Add version fields for prompt, model, corpus and retriever.','Write a redaction and retention policy for each recorded attribute.'], 'A single request ID can explain both a quality failure and a latency spike.',
'''type Span = { name: string; ms: number; ok: boolean };
async function timed<T>(name: string, fn: () => Promise<T>, sink: Span[]) {
  const start = performance.now(); let ok = false;
  try { const value = await fn(); ok = true; return value; }
  finally { sink.push({ name, ms: performance.now() - start, ok }); }
}
// Teaching helper: use OpenTelemetry for real distributed propagation.''', [Q('What does HTTP 200 guarantee about answer quality?',['Nothing by itself','The answer is grounded','All tools succeeded'],0,'Transport success and task success are different outcomes.'),Q('Which trace field supports reproducibility?',['Prompt and corpus versions','An API key','Only browser width'],0,'Version metadata links observations to the exact behavior and evidence configuration.')],['otel','evals'])
add(4,'Regression gates & experiment design','Make changes accountable before they reach users.',[
'Compare baseline and candidate on paired cases using the same dataset and environment. Repeat stochastic runs when variability matters. Inspect changes by slice and failure severity: a small average gain can conceal a new cross-tenant leak or a collapse on unsupported questions.',
'A release gate can combine zero tolerance for observed critical violations, a minimum grounded-answer score, an allowed regression band and latency/cost budgets. These are policy choices for your product, not universal thresholds. Small test sets have uncertainty; report counts and intervals where appropriate instead of presenting decimal precision as certainty.',
'Freeze configuration while comparing, preserve artifacts and review changed cases. If the candidate fails, identify whether the cause is prompt, model, retrieval or environment. A regression case should remain after the fix. Plan a canary release and rollback because offline evals cannot capture every production condition.'
], 'A release decision must include severe regressions, not just a higher mean.',
['Create baseline and candidate result files for the same 20 cases.','Add a candidate with higher mean quality but one permission leak.','Write a gate that rejects it and prints the blocking case ID.'], 'A reviewer can reproduce the decision from versioned inputs and per-case results.',
'''type Report = { critical: number; quality: number; p95ms: number; cost: number };
function releaseGate(base: Report, candidate: Report) {
  return candidate.critical === 0 && candidate.quality >= base.quality - 0.01 &&
    candidate.p95ms <= 4000 && candidate.cost <= 0.03;
}
// Illustrative budgets only: set thresholds from your product requirements.''', [Q('Quality rises but a new tenant leak appears. Release?',['No; the critical constraint fails','Yes; average improved','Only if the UI looks good'],0,'Hard safety constraints must not be averaged away by unrelated quality gains.'),Q('Why pair cases across experiments?',['To compare configurations on the same task mix','To guarantee identical outputs','To eliminate all variance'],0,'Paired comparisons reduce noise caused by differing test sets.')],['evals'])
add(4,'Failure analysis & evaluation workbench','Close the loop from a production symptom to a regression fixture.',[
'A useful failure taxonomy locates the earliest causal defect: ingestion, authorization, retrieval, context assembly, generation, tool execution or presentation. The visible symptom may appear later. A wrong answer caused by a stale document is not fixed reliably by a more forceful prompt.',
'For each failure, preserve a redacted reproducible case, classify severity, assign a component and document a hypothesis. Change one factor when possible and rerun the relevant slice plus the release gate. Avoid tuning repeatedly to the held-out set; promote reviewed failures to development data and maintain fresh evaluation coverage.',
'Your workbench can be simple JSON plus a TypeScript runner and an HTML report. Include version metadata, per-case grades, traces, latency and cost. For the weekly project, show one failure moving through diagnosis, fix and regression protection, with evidence that the change did not break another slice.'
], 'Fix the earliest supported cause and preserve the failure as a durable test.',
['Choose a stale-policy error and trace it back to ingestion or version filtering.','Create a minimal reproduction fixture and a component-level check.','Produce a before/after report with one adjacent slice tested for regression.'], 'Your workbench demonstrates a reproducible failure-to-fix loop rather than only a pass percentage.',
'''type Failure = { caseId: string; component: string; severity: string };
function groupFailures(rows: Failure[]) {
  return rows.reduce<Record<string, number>>((acc, r) => {
    const key = `${r.component}:${r.severity}`;
    acc[key] = (acc[key] ?? 0) + 1; return acc;
  }, {});
}
console.log(groupFailures([{caseId:"r7",component:"ingestion",severity:"high"}]));''', [Q('A stale source causes an incorrect answer. First fix?',['Document versioning and activation','Answer font size','Sampling randomness'],0,'The earliest evidenced cause is the wrong source version entering the pipeline.'),Q('What should happen after fixing a production failure?',['Add a redacted regression fixture','Delete all evidence of it','Only rewrite the demo'],0,'A durable fixture protects against recurrence and documents the expected behavior.')],['evals','otel'])
add(5,'Deadlines, retries & idempotency','Bound failure instead of amplifying it.',[
'Every remote dependency can be slow, unavailable or partially successful. Allocate an end-to-end deadline across retrieval, model and tool calls, propagate cancellation, and bound concurrency. A timeout means you stopped waiting; it does not prove that a remote mutation did not occur.',
'Retry only transient failures, with bounded exponential backoff and jitter, and honor provider retry guidance when applicable. Do not retry invalid input or permission denial. Retries at several layers can multiply load during an outage. Assign retry ownership and count attempts in both latency and cost budgets.',
'For writes, use an idempotency key bound to one logical operation and its arguments. Enforce uniqueness where the effect occurs, persist outcomes and reconcile uncertain states. Never retry a non-idempotent refund blindly after a timeout. Test successful-but-unacknowledged actions using mocks.'
], 'A retry policy is safe only when the operation’s effects and total budget are understood.',
['Simulate 429, invalid input, permission denial and a timeout after a mock write.','Define which component owns retries and cap the attempt count.','Demonstrate one logical refund across three repeated requests.'], 'Transient reads retry within budget; uncertain writes reconcile without duplicate effects.',
'''async function retryRead<T>(fn: () => Promise<T>, retryable: (e: unknown) => boolean) {
  for (let attempt = 0; ; attempt++) {
    try { return await fn(); }
    catch (error) {
      if (attempt >= 2 || !retryable(error)) throw error;
      const delay = Math.random() * Math.min(2000, 200 * 2 ** attempt);
      await new Promise(resolve => setTimeout(resolve, delay));
    }
  }
} // Add a shared deadline/cancellation signal in the production adapter.''', [Q('A timed-out refund definitely failed. True?',['False; its effect may have completed','True','Only if it used JSON'],0,'The acknowledgement can be lost after the external effect succeeds.'),Q('Should a permission denial be retried?',['No, fix authorization or surface denial','Yes, indefinitely','Only with a larger model'],0,'Denial is not a transient availability failure.')],['next','otel'])
add(5,'Prompt injection & output security','Place the safety boundary in application capabilities, not persuasive wording.',[
'Prompt injection occurs when untrusted content attempts to redirect model behavior. Retrieved documents, web pages, tool outputs and images can carry instructions. Delimiters and explicit prompts may help behavior, but do not create an enforceable security boundary. Assume the model may follow malicious content and limit what execution can do.',
'Use tool allowlists, least privilege, resource authorization, constrained network access and approvals for sensitive effects. Do not place secrets in model context. Validate destinations and file paths in executors. Render model output as text or sanitized allowed markup; never insert untrusted output as executable HTML or run generated SQL directly.',
'Test attacks in context: a policy chunk asks for secrets, a ticket requests a different tenant’s data, and an image suggests an unauthorized action. Success means no prohibited data access or external effect, even if the generated answer is confused. Log the policy denial without recording secrets.'
], 'Design the executor to remain safe when the model makes the wrong decision.',
['Create three injected evidence fixtures with explicit prohibited goals.','Run them against a mock executor that checks scope and allowed tools.','Check that your UI renders an HTML attack payload as text.'], 'No injection can expand authority, and rendered output cannot execute scripts.',
'''// Safe text rendering; never use innerHTML with model output.
function renderModelText(node: HTMLElement, output: string) {
  node.textContent = output;
}
const allowedTools = new Set(["search_policy", "get_ticket"]);
function checkTool(name: string) {
  if (!allowedTools.has(name)) throw new Error("tool denied");
}
// Pair allowlists with per-resource authorization inside each tool.''', [Q('Do delimiters alone stop prompt injection?',['No','Yes','Only in a system prompt'],0,'They are behavioral cues; tool and data boundaries must be enforced in code.'),Q('How should raw model prose enter a web page?',['As text or sanitized allowed markup','Through unrestricted innerHTML','As a script'],0,'Untrusted generated content must not become executable page code.')],['owasp','next'])
add(5,'Tenant isolation, privacy & secrets','Apply the Supabase security model to every derived AI artifact.',[
'Authorization must cover documents, chunks, embeddings, conversations, memories, traces and caches. A derived summary can leak the same sensitive information as its source. Bind tenant scope to authenticated identity and enforce it at every lookup. Test with the real database role; privileged server credentials can bypass ordinary RLS policies.',
'In Supabase, enable RLS and write policies tied to verified membership or ownership. An owner-only policy is not a complete organization membership model. Prefer invoker-scoped query functions when suitable, audit any security-definer function and control its search path and grants. Never let the model choose SQL or override a tenant filter.',
'Keep provider and service credentials server-side. Define retention, deletion and allowed data egress for every external provider. A deletion request should invalidate searchable vectors and caches as well as original rows. Use synthetic data for this course unless you have a valid basis for processing real customer content.'
], 'Treat every derived artifact as tenant-scoped data with a lifecycle.',
['List all data stores and caches in your architecture, including traces.','Write a two-user isolation test against your intended production role.','Simulate deletion and confirm sources, chunks and cache entries become unavailable.'], 'Your test demonstrates both allowed access and denied cross-user access.',
'''-- Minimal owner-only example, NOT an organization policy.
-- Assumes a UUID owner_id column on your chunks table.
alter table chunks enable row level security;
create policy "owner can read chunks" on chunks
for select to authenticated
using (owner_id = (select auth.uid()));
-- Add separately reviewed write policies if writes are needed.
-- Service-role access bypasses RLS: constrain it explicitly on the server.''', [Q('Should a tenant key be included in an answer-cache key?',['Yes, along with authorization/version context','No, questions are universal','Only for large customers'],0,'Shared cache entries can leak answers across tenant or permission boundaries.'),Q('Does enabling RLS protect service-role queries automatically?',['No','Yes','Only with embeddings'],0,'Privileged roles can bypass RLS, so actual execution roles and explicit scope need testing.')],['rls','next','owasp'],'SQL')
add(5,'Cost, latency & capacity planning','Budget the full successful task, including retries and tools.',[
'For token-priced models, estimate input and output charges separately using the selected provider’s current rates. Add embeddings, rerankers, tool services, storage and retries. Divide total spend by successful tasks to compare configurations; a cheap model that requires repeated repair may not be cheap in practice.',
'Latency comes from both sequential dependencies and resource queues. Parallel independent reads can help, while unbounded concurrency can overwhelm your database or provider quota. Use per-user quotas, request size bounds and a concurrency limiter. For sustained arrival rate λ and average time in system W, Little’s Law gives average in-flight work L = λW under stable conditions.',
'Cache only where correctness and authorization permit it. Include tenant, permission scope, model, prompt and corpus version in keys as appropriate. Expire or invalidate when policies or memberships change. Cached prompts and semantic answer caches are different mechanisms with different risks; measure each rather than assuming equal savings.'
], 'Optimize cost per useful task under quality, privacy and latency constraints.',
['Calculate cost for 1,500 input and 400 output tokens using hypothetical rates.','Estimate average concurrency at 5 requests/sec and 3 seconds average duration.','Design an answer-cache key and its invalidation triggers.'], 'Your worksheet includes retries and explains why average concurrency is 15, not a peak capacity guarantee.',
'''function tokenCost(input: number, output: number, inPerM: number, outPerM: number) {
  return (input * inPerM + output * outPerM) / 1_000_000;
}
// Hypothetical rates, not a provider quote.
console.log(tokenCost(1500, 400, 1, 4)); // $0.0031
console.log(5 * 3); // average in-flight work = 15 in a stable system''', [Q('What costs belong in cost per success?',['Retries, failed attempts and dependencies too','Only the final successful output','Only embedding costs'],0,'End-to-end economics include all work spent to achieve successful tasks.'),Q('Little’s Law gives what here?',['Average concurrency under stable conditions','A guaranteed safe peak limit','A model’s context size'],0,'Average in-flight work is not a bound on burst load or tail behavior.')],['otel','evals'])
add(5,'Reliability patterns & graceful degradation','Define what the user sees when a dependency is unavailable.',[
'A reliable AI feature has explicit degraded modes: show authorized search results if generation fails, offer a saved draft if a tool is unavailable, or escalate a high-impact task. Do not silently switch to an ungrounded answer when retrieval fails. Communicate partial completion and uncertain external effects clearly.',
'A circuit breaker stops calling a failing dependency after a threshold and later allows limited probes. Bulkheads isolate capacity so a slow tenant or tool does not consume every worker. Queues help absorb bursts for asynchronous tasks, but need expiry, deduplication, poison-message handling and user-visible status.',
'Fallback models can differ in capabilities, context limits, data-processing terms and failure behavior. Evaluate the complete fallback path and preserve policy checks. Define SLOs such as grounded useful completion rate and p95 latency over a time window, with an error budget that triggers action rather than a decorative dashboard.'
], 'Choose a degraded mode that remains truthful and within the original permission boundary.',
['Write user-facing outcomes for retrieval, generation and action failures.','Simulate a circuit opening and a limited recovery probe.','Define an SLO and a response when its error budget is exhausted.'], 'A dependency outage yields a clear, safe result and does not cause unlimited retries.',
'''type Health = "closed" | "open" | "half-open";
function fallback(retrievalOk: boolean, generationOk: boolean) {
  if (!retrievalOk) return "Knowledge search unavailable; please try later.";
  if (!generationOk) return "Show authorized source snippets without a generated answer.";
  return "Show validated answer.";
}
console.log(fallback(false, false));
// Never fabricate evidence to hide a retrieval outage.''', [Q('Retrieval is down. Safest default for a grounded-answer product?',['Report unavailability or an approved degraded mode','Generate from memory silently','Invent source IDs'],0,'The product’s evidence promise must hold during failures as well as normal operation.'),Q('Why use a circuit breaker?',['To reduce repeated load on a failing dependency','To guarantee model accuracy','To disable authentication'],0,'Stopping repeated failing calls can protect capacity and allow controlled recovery.')],['otel','next'])
add(5,'Red-team tests & operational readiness','Deliver an incident-ready service design.',[
'Red teaming explores how the system fails under adversarial conditions: injected evidence, forged tool arguments, oversized input, repeated calls, stale approvals and cross-tenant requests. Define attacker goals and test observable outcomes. A blocked answer is insufficient if a prohibited tool effect already occurred.',
'An operations runbook identifies detection, containment, investigation, recovery and follow-up. For a suspected leak, disable affected capabilities, preserve appropriately restricted evidence, assess scope and follow the organization’s incident process. For cost spikes, cap concurrency and suspend optional tool paths while keeping authenticated access intact.',
'For this week’s project, collect the threat model, adversarial fixture results, isolation checks, failure-mode matrix and cost worksheet. Include kill switches for tool execution and model generation, tested rollback instructions and ownership. Avoid claiming production readiness solely because a small lab passed.'
], 'Readiness is demonstrated by bounded failure and practiced recovery, with limitations stated.',
['Run six attacks: injection, forged tenant, unknown tool, stale approval, huge input and duplicate write.','Draft a runbook with trigger, owner, containment, recovery and verification.','Practice one rollback with fixtures and record what remains untested.'], 'Your release packet includes evidence of blocked effects and a reproducible recovery drill.',
'''const scenarios = [
  "injected evidence", "forged tenant", "unknown tool",
  "stale approval", "oversized input", "duplicate mutation"
];
type Result = { scenario: string; prohibitedEffects: number; terminal: boolean };
function safeRun(r: Result) { return r.prohibitedEffects === 0 && r.terminal; }
console.log(scenarios.map(scenario => ({ scenario, expected: "deny or bounded safe result" })));''', [Q('A malicious answer is blocked after a refund executes. Did the defense succeed?',['No; the prohibited effect already happened','Yes, the text was blocked','Only if logs are empty'],0,'Security must be enforced before the external effect, not just at the final response.'),Q('What should a runbook include?',['Triggers, owners, containment, recovery and verification','Only a diagram','Only provider marketing links'],0,'An actionable runbook specifies who acts, when, how to contain harm and how to verify recovery.')],['owasp','otel','rls'])
add(6,'System design: requirements before boxes','Translate an AI product brief into measurable constraints.',[
'Begin a system design with users, tasks, data sensitivity, freshness, load and acceptable failure. For the support copilot, ask whether it drafts for a human or sends directly, whether actions are reversible, how tenant membership works, and whether evidence must be current to the minute or the day. These answers change the architecture more than a framework choice.',
'Define functional requirements and SLOs separately. “Answer policy questions with citations” is a behavior; “95% of supported questions complete within four seconds under expected load” is an illustrative service target. Specify how correctness and availability will be measured, and what happens when the target cannot be met.',
'Size the problem with explicit assumptions: requests per day, peak arrival rate, document revisions, chunks per revision and retention. Distinguish average from peak and account for repeated model/tool calls per request. Record uncertainty and the experiment that would reduce it.'
], 'Make assumptions visible before optimizing an architecture around them.',
['Write a one-page brief for a human-reviewed support copilot.','Estimate vector count and request concurrency with stated assumptions.','List three unresolved requirements that would materially change the design.'], 'A reviewer can trace each major architectural decision to a requirement or measured constraint.',
'''const sizing = {
  tenants: 100, docsPerTenant: 200, chunksPerDoc: 8,
  peakRequestsPerSec: 4, meanSeconds: 3
};
console.log({
  chunks: sizing.tenants * sizing.docsPerTenant * sizing.chunksPerDoc,
  averageInflightAtPeakRate: sizing.peakRequestsPerSec * sizing.meanSeconds
}); // 160,000 chunks; 12 average in-flight under stable assumptions''', [Q('What should be clarified first?',['Whether the assistant drafts or autonomously acts','The button color','The agent framework logo'],0,'Action authority affects approval, risk, evaluation and recovery architecture.'),Q('What makes a sizing estimate useful?',['Explicit assumptions and uncertainty','Many unexplained digits','A guarantee of future load'],0,'Visible assumptions let reviewers update the estimate when requirements change.')],['evals','next'])
add(6,'Architecture & data contracts','Design component boundaries you can test and replace.',[
'Separate synchronous user requests from asynchronous ingestion. The request path authenticates, retrieves authorized current evidence, generates, validates and returns. The ingestion path extracts, versions, chunks, embeds and activates documents. Share explicit schemas and version metadata rather than hidden assumptions between the two.',
'For your stack, Next.js handles interaction and server routes, Supabase handles authenticated relational data and vectors, and a worker processes long-running ingestion. Keep provider access behind an adapter. A job queue or durable orchestration layer may be needed for work that cannot fit the hosting platform’s execution limits.',
'Draw trust and failure boundaries on the architecture. Show which service has privileged credentials, where user-scoped queries run, and where data leaves your infrastructure. Include version rollout, document deletion, cache invalidation and rollback. The architecture is incomplete if it only shows the happy path.'
], 'Use contracts to isolate model providers, retrieval and business authorization.',
['Draw request and ingestion paths separately.','Define request, chunk, answer, tool result and eval result schemas.','Annotate each boundary with identity, timeout and failure behavior.'], 'The design supports fixture adapters and identifies how a corpus version becomes active atomically.',
'''interface Retriever {
  search(input: { query: string; actorId: string; limit: number }):
    Promise<{ id: string; text: string; revision: string }[]>;
}
interface Generator {
  generate(input: { question: string; evidence: { id: string; text: string }[] }):
    Promise<unknown>;
}
// Authenticate actorId server-side, retrieve, generate, then validate unknown.
// Do not let provider-specific types leak into business authorization.''', [Q('Why separate ingestion from the request path?',['Long-running versioned processing has different failure and latency needs','It removes security checks','It guarantees free hosting'],0,'Asynchronous processing needs its own retries, activation and recovery semantics.'),Q('What belongs on an architecture diagram?',['Trust and failure boundaries as well as components','Only provider logos','Only database tables'],0,'Operational behavior and authority determine whether component connections are safe and reliable.')],['next','rls','otel'])
add(6,'Capstone implementation plan','Build a thin end-to-end slice before broadening scope.',[
'The capstone is a support copilot that answers from versioned policy documents, looks up authorized tickets and drafts a recommended next step. Keep real refunds and external messages disabled in the initial build. Implement the entire path for one tenant and a few documents, then add scale and operational constraints.',
'Create a repository with typed core logic, fixture adapters, optional live provider/database adapters, a test dataset and an evaluation runner. Pin dependencies, document environment variables and keep secrets out of the repository. The academy does not execute these snippets or install dependencies; its offline labs validate the same concepts with embedded fixtures.',
'Deliver in milestones: grounded answers, hybrid retrieval, bounded read-only tools, eval gates and hardened execution. Each milestone should preserve a runnable fixture mode. Add features only when you have a case that exercises them and a clear acceptance check; avoid a large untested integration at the end.'
], 'Maintain a reproducible fixture path while adding live integrations one at a time.',
['Create core/, adapters/, fixtures/, evals/ and docs/ in a project repository.','Implement one cited answer end-to-end with fixtures.','Swap only the retrieval adapter for a local database, then only the model adapter if desired.'], 'A fresh checkout can run fixture tests without credentials and describes every optional live dependency.',
'''// Suggested project boundaries; filenames are a plan, not generated files.
const milestones = [
  { name: "Grounded answer", check: "valid citation + explicit abstention" },
  { name: "Retrieval", check: "held-out hit rate and no tenant leaks" },
  { name: "Tools", check: "bounded loop and authorized reads only" },
  { name: "Release", check: "eval gate, budgets and recovery drill" }
];
console.table(milestones);''', [Q('What is a good first implementation milestone?',['One complete fixture-backed cited answer','Every framework integration at once','A production refund tool'],0,'A thin end-to-end slice reveals interface mistakes early and remains reproducible.'),Q('Why preserve fixture mode?',['To test without credentials or nondeterministic services','To replace every real-world evaluation','To hide failures'],0,'Fixture mode enables repeatable local checks while live integration tests remain a separate responsibility.')],['evals','next'])
add(6,'Capstone acceptance & design review','Make the portfolio inspectable, not just impressive in a demo.',[
'Acceptance should include supported answers, unsupported questions, current-versus-stale documents, cross-tenant attempts, tool failures and cancellation. Evaluate the complete system with held-out cases and show per-slice results. Demonstrate that approval and idempotency checks exist before enabling any real side effect.',
'Use a review scorecard across correctness, evidence, security, reliability, observability, cost and reproducibility. Require explicit evidence for each claim: a test result, trace, benchmark or documented limitation. A small portfolio project should state scale assumptions and what has not been load-tested rather than claiming production guarantees.',
'Package the repository with setup instructions, sample data, architecture, decision records, eval report and a short demo script. Rehearse one successful answer, one abstention, one denial and one recovery. A reviewer should be able to reproduce the fixture run and understand the tradeoffs without your narration.'
], 'Every readiness claim should point to evidence or an explicit limitation.',
['Run your held-out suite and inspect all failures.','Complete a seven-dimension scorecard with evidence links.','Record a five-minute walkthrough including denial and recovery.'], 'The capstone passes its stated gates and its README makes unfinished or untested areas explicit.',
'''const review = ["correctness", "evidence", "security", "reliability",
  "observability", "cost", "reproducibility"];
type Evidence = { dimension: string; artifact: string; limitation: string };
function covered(items: Evidence[]) {
  return review.every(d => items.some(x => x.dimension === d && x.artifact.trim()));
}
// Evidence can be a report, trace, test or reviewed design document.''', [Q('Which demo best supports readiness?',['Success, abstention, denial and recovery','Only the best answer','Only a slide of the architecture'],0,'Failure behavior and permission boundaries matter as much as the happy path.'),Q('What should a portfolio say about untested scale?',['State the assumptions and limits','Claim unlimited scalability','Omit the subject'],0,'Explicit limitations let reviewers assess the evidence accurately.')],['evals','otel','owasp'])
add(6,'Interview drills & tradeoff practice','Explain decisions using evidence, alternatives and failure modes.',[
'A strong engineering answer starts with requirements, proposes a baseline, names tradeoffs and describes validation. For “design a RAG assistant,” discuss corpus freshness, tenant isolation, retrieval labels, abstention and operational budgets before listing libraries. Use concrete examples from your capstone to show depth.',
'Practice debugging as causal analysis. If answer quality drops after a release, segment by model, prompt, corpus and query slice, inspect traces and compare paired cases. If latency spikes, separate queue time, retrieval, model decode and tools. State what you would measure before changing parameters.',
'Prepare short explanations for RAG versus fine-tuning, workflow versus agent, exact versus approximate search, and deterministic versus model-based grading. Include a situation where each preferred choice would be wrong. Interviewers can assess judgment more easily when you explain both the decision and its reversal conditions.'
], 'Answer with requirement → baseline → tradeoff → evidence → failure response.',
['Give a two-minute RAG design answer with no framework names.','Debug a hypothetical quality regression using three discriminating checks.','Record a ten-minute mock interview and score specificity, correctness and clarity.'], 'You can defend an alternative design and identify the evidence that would change your choice.',
'''const interviewPrompts = [
  "Design a tenant-aware policy assistant for 100 organizations.",
  "Recall improved but grounded answer quality fell. Diagnose it.",
  "A tool timed out after a refund. What happens next?",
  "When would you replace an agent with a workflow?",
  "How would you compare two models under a fixed cost budget?"
];
// Answer each with one concrete capstone artifact and one failure mode.''', [Q('Quality drops after a corpus update. First approach?',['Segment versions and inspect paired failing traces','Immediately fine-tune','Increase temperature'],0,'Versioned traces and paired cases help identify the changed component before choosing a remedy.'),Q('What makes a tradeoff explanation strong?',['A reversal condition backed by evidence','A list of popular tools','Always selecting the most complex design'],0,'Good judgment includes knowing when a decision would stop being appropriate.')],['evals','agents','pg'])
add(6,'Your next 90 days','Turn a six-week foundation into sustained engineering practice.',[
'Consolidate before expanding: revisit failed quizzes, reproduce labs without looking at snippets, and clean up the capstone’s weakest boundary. Passing a knowledge quiz is not the same as implementing a reliable system. Keep a list of open questions and attach each to a concrete experiment or reading.',
'For the next month, deepen one axis: retrieval quality, agent recovery, evaluation statistics or inference systems. In the second month, add a realistic integration with reviewed privacy and operational constraints. In the third, run a measured improvement cycle and publish a reproducible technical write-up using non-sensitive data.',
'Maintain a change log of models, prompts, dependencies and protocol revisions. Re-run the benchmark when any changes. Read original research to understand mechanisms, official docs for interfaces and incident reports for failure patterns. Keep your operating principle: measurable useful behavior under explicit constraints, rather than collecting abstractions.'
], 'Choose the next experiment from your weakest measured capability.',
['Rank your capstone’s top three remaining risks and choose one experiment.','Schedule four weekly review sessions with a measurable deliverable.','Write a 90-day plan with baseline, target, evidence and a stop condition.'], 'You have an evidence-backed improvement plan and an exported backup of your academy progress.',
'''type Experiment = { hypothesis: string; metric: string;
  baseline: number; target: number; stopCondition: string };
const nextExperiment: Experiment = {
  hypothesis: "Section-aware chunks improve exact-policy retrieval",
  metric: "held-out hit rate@5", baseline: 0.75, target: 0.9,
  stopCondition: "Reject if groundedness or tenant isolation regresses"
};
console.log(nextExperiment);''', [Q('What should determine your next learning topic?',['The weakest measured capability or risk','Only current hype','The longest framework tutorial'],0,'Targeted practice closes an evidenced gap and produces a useful improvement.'),Q('When should you re-run the benchmark?',['After relevant model, prompt, corpus or dependency changes','Only once ever','Only after changing colors'],0,'Behavior can change at multiple layers, so version changes need regression checks.')],['evals','attention','mcp'])
glossary={
'Abstention':'An explicit decision not to answer or act when evidence, permission or confidence is insufficient.',
'Agent':'A system in which a model selects some next actions from allowed capabilities based on observations.',
'Agent harness':'The runtime around an agent: tools, policies, context, budgets, persistence, isolation and recovery.',
'Attention':'A mechanism that combines value vectors using weights derived from query-key comparisons.',
'Calibration':'Checking how a score or judgment corresponds to observed correctness on representative data.',
'Chunk':'An independently indexed piece of source content with provenance and version metadata.',
'Circuit breaker':'A mechanism that temporarily stops calls to a failing dependency and later probes recovery.',
'Context window':'The model’s bounded working sequence; the exact accounting depends on the selected model.',
'Cosine similarity':'Dot product divided by vector norms; compares vector direction rather than raw magnitude.',
'Cross-entropy':'A loss that penalizes low assigned probability to the observed target.',
'Data leakage':'Information crossing an evaluation or access boundary in a way that invalidates results or privacy.',
'Embedding':'A learned numeric representation used to compare or process input features.',
'Eval':'A repeatable assessment of system behavior on specified tasks, environments and grading criteria.',
'Fine-tuning':'Additional training that adjusts model parameters using a task or behavior-specific objective.',
'Groundedness':'The extent to which an answer’s claims are supported by the supplied evidence.',
'HNSW':'A graph-based approximate nearest-neighbor index with recall, latency and memory tradeoffs.',
'Hybrid search':'Retrieval that combines lexical and semantic candidate signals.',
'Idempotency':'Repeated execution of one logical operation has the same intended effect as one execution.',
'Inference':'Running a trained model to compute outputs for new inputs.',
'KV cache':'Cached attention key/value states reused during autoregressive generation.',
'LLM judge':'A model used to grade outputs against a rubric; requires calibration and bias checks.',
'MCP':'Model Context Protocol: an interface standard for connecting AI applications to external capabilities.',
'MRR':'Mean reciprocal rank: average inverse position of the first relevant result, with zero for misses.',
'Observability':'Using traces, metrics and logs to infer system behavior and diagnose failures.',
'Precision':'True positives divided by all predicted positives.',
'Prompt injection':'Untrusted content attempting to redirect model behavior or induce unauthorized actions.',
'Provenance':'The source, location, transformation and version history of a piece of evidence.',
'RAG':'Retrieval-augmented generation: using retrieved evidence as context for generation.',
'Recall':'True positives divided by all actual positives; retrieval recall@k measures relevant items recovered at k.',
'Reranker':'A model or algorithm that reorders a candidate set using additional relevance signals.',
'RLS':'Row Level Security: database policies controlling which rows a role may access.',
'RRF':'Reciprocal rank fusion: combining ranked lists by summing inverse smoothed ranks.',
'SLO':'Service-level objective: a measurable reliability or performance target over a defined window.',
'Span':'A timed operation within a trace, with attributes and parent/child relationships.',
'Structured output':'Generated content constrained to a schema; syntax constraints do not guarantee factual truth.',
'Temperature':'A sampling control that changes distribution sharpness; it does not guarantee accuracy.',
'Token':'A tokenizer-defined unit such as a subword, character sequence or special marker.',
'Trace':'A correlated record of operations involved in one request or agent run.',
'Workflow':'Code-defined steps and branches, which may include model calls.',
'Zero-shot':'Performing a task from instructions without task demonstrations in the immediate prompt.'}
data=dict(weeks=weeks,lessons=lessons,refs=refs,glossary=glossary)
assert len(lessons)==36
(ROOT/'curriculum.json').write_text(json.dumps(data,ensure_ascii=False,indent=2))
template=(ROOT/'template.html').read_text()
(ROOT/'index.html').write_text(template.replace('/*__CURRICULUM__*/', 'const DATA='+json.dumps(data,ensure_ascii=False).replace('</','<\\/')+';'))
print(f'Built {len(lessons)} lessons, {sum(len(l["quiz"]) for l in lessons)} quiz questions, {len(glossary)} glossary terms')
