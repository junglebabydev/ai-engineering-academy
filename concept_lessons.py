"""General teaching first; the Jungle build remains a separate application layer."""
TOPICS=[]
def topic(title,definition,how,why,before,after,explanation,remember,reflection):
 TOPICS.append(dict(title=title,definition=definition,how=how,why=why,before=before,after=after,explanation=explanation,remember=remember,reflection=reflection))
topic('What is AI engineering?',
'AI engineering is the work of turning an AI model into a useful, dependable product. It combines the model with information, tools, rules, interfaces, and checks so people can accomplish a real task.',
'A language model can interpret a request and generate a response. Other parts of the product retrieve current facts, check permissions, carry out allowed actions, and handle failures. The engineer decides how those responsibilities fit together. Building an AI product therefore involves more than writing a prompt or choosing a powerful model.',
'A convincing sentence is not the same as a completed task. Good engineering makes it possible to inspect the evidence, control effects, and measure whether the whole system helped the user.',
'A travel assistant says it booked an affordable flight after generating a plausible itinerary, without checking flights or buying a ticket.',
'It understands your preferences, looks up current flights, checks the budget, and asks permission before using a booking tool.',
'The model supplies language capabilities; the surrounding system supplies current information, rules, authorized actions, and verification.',
'The model provides capabilities; engineering makes them useful and dependable.',
'Explain the difference between an AI model and a complete AI product. Give an example outside this course project.')
topic('How do models learn from examples?',
'Machine learning uses examples to adjust a model’s internal settings so it can perform a task. Generalisation means applying what it learned to new situations, rather than merely reproducing practice examples.',
'During training, a loss expresses how far a prediction is from its target. The learning process adjusts the model to reduce that loss. A separate validation set helps guide development; a held-out test set checks a decision on examples not used to improve it. Closely related examples can accidentally reveal answers across those boundaries.',
'A high overall score can hide important mistakes. Check which kinds of error occur and what they cost. A system that recognises routine emails but misses every urgent complaint can still appear accurate if urgent complaints are rare.',
'A learner practises the exact exam questions, then scores perfectly on those same questions.',
'They practise with one set, then answer genuinely new questions, including uncommon but important cases.',
'The second approach checks whether learning transfers rather than measuring familiarity with the answer sheet.',
'Learning is useful when it transfers to new examples.',
'Why should practice examples and final test examples be separate? Describe a misleadingly high score.')
topic('What are tokens and embeddings?',
'A token is a model-specific piece of text used during processing. An embedding is a learned numerical representation of an input that helps a system compare it with other inputs.',
'Tokens may be whole words, parts of words, or other text pieces. Instructions, conversation, retrieved information, and output all need space within the model’s limits. Embeddings serve a different purpose: related meanings often have nearby representations, allowing a system to find useful candidates even when their wording differs.',
'Numerical similarity is not a truth check. Statements that contradict each other can discuss the same subject and still appear related. Keep representation, retrieval, and factual verification as separate ideas.',
'A library search misses “heart doctor” because its records use “cardiologist,” or treats two related statements as equally true.',
'It finds related wording by meaning, then checks whether the source actually answers the question.',
'Representations help locate relevant material; they do not establish whether a claim is supported.',
'Tokens organise processing; embeddings help compare inputs.',
'Explain tokens and embeddings without using mathematical notation. Why is similarity not proof?')
topic('How do language models generate answers?',
'A language model generates text by repeatedly predicting a distribution over possible next tokens and selecting from it. Its response depends on learned patterns and the context supplied for the current task.',
'Transformer models use attention to combine information from different positions in their input. This helps connect earlier details with later text, but it does not automatically check an external database. Sampling settings such as temperature influence how sharply the model selects among possibilities; they do not add missing evidence.',
'A model can sound confident while generating an unsupported claim. Repeating an answer consistently is also not proof. Design the product to distinguish generated wording from verified facts and to handle uncertainty explicitly.',
'An assistant confidently gives tomorrow’s train departure from general memory without consulting a timetable.',
'It uses a current timetable, or states that the departure has not been checked and offers a lookup.',
'Changing the randomness of the sentence cannot replace the missing timetable.',
'Plausible generation and factual verification are different processes.',
'Why can a language model produce the same wrong answer repeatedly? What would improve the evidence?')
topic('What makes a good prompt and output contract?',
'A prompt describes the task and the instructions a model should follow. An output contract describes the structure and rules that the returned answer must satisfy so the rest of the product can use it.',
'Specify the goal, allowed evidence, boundaries, examples, and what to do when information is missing. A structured response can use agreed fields, much like spreadsheet columns. Check the fields, allowed values, and business rules after generation. Instructions help guide behaviour, while application checks enforce requirements independently.',
'Good formatting does not guarantee true contents. A perfectly formed invoice can still contain the wrong amount. Keep prompt versions and distinguish a formatting error, an unsupported claim, and a policy refusal when assessing outputs.',
'“Write something useful about this receipt” returns inconsistent prose and an invented total.',
'“Extract seller, date, amount, and currency; mark unreadable fields unknown” is followed by format and source checks.',
'The clearer contract makes the task inspectable, but the extracted facts still require validation.',
'Give clear instructions, then validate the result.',
'What belongs in a prompt, and what should the application check even if the prompt is ignored?')
topic('When should you use prompting, RAG, or fine-tuning?',
'Prompting changes the instructions and context given to a model. RAG retrieves relevant information before generation. Fine-tuning performs additional training that changes the model’s internal parameters.',
'Choose an intervention based on the failure. Unclear instructions call for a better task definition. Missing or frequently changing knowledge often calls for retrieval from current sources. Repeated behavioural problems may justify investigating training after establishing a strong baseline. Compare candidate models on the same representative tasks, costs, and waiting-time constraints.',
'The most expensive model is not automatically the right fix. Measure useful results and identify why failures happen before adding complexity. Information that changes often should not depend solely on what a model may have learned months earlier.',
'A company retrains a model every time the office opening hours change.',
'It retrieves the current hours when needed and separately evaluates whether the instructions or model behaviour need improvement.',
'Changing facts and learned behaviour are different problems and can need different solutions.',
'Choose the remedy that addresses the observed cause.',
'Give one situation suited to better prompting, one to retrieval, and one where fine-tuning might deserve investigation.')
topic('What are ingestion, chunking, and provenance?',
'Ingestion brings source material into a usable collection. Chunking divides long material into useful pieces. Provenance records where each piece came from and which source version supports it.',
'Extract information, preserve meaningful headings and relationships, and give records stable identities. A table cell without its column heading can be misleading. Track revisions and activate updated content deliberately. Repeating the same import should not create duplicate records, and deleting a source should remove its searchable derivatives.',
'An answer cannot be reliably checked if its evidence has lost its identity or date. Organising source material is therefore part of answer quality, not merely an administrative task before the “real AI” work begins.',
'A policy archive contains a loose fragment saying “30 days,” without a policy name or effective date.',
'The fragment retains its section heading, source ID, revision, and relationship to the complete rule.',
'Context and provenance make the fragment interpretable and allow later updates or deletion.',
'Preserve meaning and provenance when preparing information.',
'What can go wrong when a document is split into pieces without headings, source identity, or revision?')
topic('How does vector search work?',
'Vector search finds items whose numerical representations are close under a chosen comparison. It is often used to discover related meaning when exact wording does not match.',
'Create compatible embeddings for stored records and the search query, compare them, and return a candidate list. Exact search compares the relevant candidate set directly. Approximate indexes can search large collections faster while potentially missing some relevant items. The representation, dimensions, and distance method must be compatible.',
'A close representation is a candidate signal, not a permission or truth guarantee. Evaluate search quality on labelled examples and apply access restrictions and factual rules. Faster search is useful only if it preserves enough of the information the task needs.',
'A search for “places to eat without meat” finds only records containing those exact words.',
'Meaning-based retrieval also discovers “vegetarian restaurants,” then checks location, opening hours, and the user’s constraints.',
'Related meaning expands discovery while factual checks determine whether each candidate is appropriate.',
'Vector search finds candidates by representation, not by proving their claims.',
'What does vector search add beyond exact words, and what does it still fail to establish?')
topic('What is hybrid search?',
'Hybrid search combines retrieval methods, often keyword matching and meaning-based vector search, to find relevant information that either method alone may miss.',
'Keyword search is useful for exact names, identifiers, and specialised terms. Meaning-based search helps with paraphrases. Their raw scores can use different scales, so a fusion method may combine their ranked positions instead. Reciprocal rank fusion, or RRF, gives candidates credit according to where they appear in each list.',
'Combining methods adds complexity and may not improve every task. Compare the combined approach with simpler baselines on exact-identifier and paraphrase examples, then inspect the failures. The final ranking still does not verify the truth or suitability of a result.',
'A help centre handles ordinary paraphrases well but misses a user’s exact error code.',
'It combines a keyword path for the code with a meaning-based path for the described symptom.',
'The approaches provide complementary discovery signals instead of forcing one method to handle every request.',
'Combine complementary signals, then measure whether they help.',
'When would exact words matter more than related meaning? Why might you combine their ranks instead of their raw scores?')
topic('What are filtering and reranking?',
'Filtering excludes items that fail a required condition. Reranking changes the order of an already retrieved candidate set according to how well it addresses the specific request.',
'First distinguish strict requirements from preferences. Apply hard rules to keep unsuitable items out, then order the remaining candidates by relevance or preference. A reranker can examine a query and candidate together, but cannot recover an item absent from its input. Select a concise, non-duplicated evidence set for generation rather than adding every possible result.',
'If ordering is allowed to override requirements, the most attractive result can still be unusable. Inspect both candidate recall and final suitability before deciding that a more sophisticated ranking system improves the product.',
'A hotel search puts a popular $300 room first despite a strict $150 maximum.',
'It excludes rooms over the maximum, then orders eligible rooms by the traveller’s preferences.',
'Ranking chooses among eligible options; it should not erase a hard constraint.',
'Filter for requirements; rank the options that remain.',
'Explain the difference between filtering and reranking. Can reranking fix a missing candidate?')
topic('What are grounding, citations, and abstention?',
'Grounding means supporting an answer’s claims with appropriate evidence. A citation identifies a source; abstention means choosing not to assert something that lacks sufficient support or permission.',
'Check that a cited source exists, was available for this answer, is suitable for the task, and actually supports the claim. These are separate checks. Distinguish facts from inference and unknowns. When evidence is missing or conflicting, give a useful partial answer or explain the next check rather than filling the gap with a guess.',
'Neither a real citation nor a high similarity score establishes that every sentence is true. Assess useful coverage as well as unsupported-answer rate: a system that refuses everything avoids some errors but does not fulfil its purpose.',
'A policy assistant cites a real document for an entitlement that the document never mentions.',
'It states the entitlement only when the source supports it, and identifies unsupported details as unknown.',
'Citations need a claim-to-evidence relationship, not merely a valid-looking reference.',
'A source must support the specific claim.',
'How can an answer contain a real citation and still be unsupported? What makes abstention useful?')
topic('How do we evaluate retrieval?',
'Retrieval evaluation checks whether a search system finds and orders the information a task needs. It is separate from checking whether a generated answer uses that information correctly.',
'Label relevant items for representative queries. Recall@k measures the fraction recovered among the first k results; hit rate asks whether at least one relevant item was found. Reciprocal rank rewards finding the first relevant item earlier. Then test answer generation with fixed correct evidence and finally assess the complete system.',
'Component checks locate faults that an overall answer score can hide. Labels may be incomplete and small datasets have limited coverage, so document their assumptions. A fluent answer cannot compensate for the absence of the source needed to support it.',
'A team changes the writing model repeatedly because the answer misses a rule that search never retrieved.',
'It checks relevant source IDs first, fixes the retrieval miss, and then evaluates the answer with the corrected evidence.',
'The failure is located before choosing a remedy.',
'Test finding evidence separately from using it.',
'What do recall, hit rate, and reciprocal rank tell you? What do they not tell you about the final answer?')
topic('What is an AI agent?',
'An AI agent is a system in which a model chooses some next actions from available capabilities, observes the results, and uses them to pursue a task within defined limits.',
'A workflow follows steps and branches arranged in advance. An agent delegates some choice of next step to the model. Either may call models multiple times. A chat interface alone does not establish agentic behaviour. Define the tools, the decisions the model may make, and which rules remain enforced by ordinary software.',
'Adaptive decisions can help with tasks whose route varies, but they introduce more possible failure paths. Use flexibility where it improves the task rather than making every step autonomous. Permission to execute still comes from the application’s policy and the user’s authorized intent.',
'An email assistant always sends a template, even when the request needs an attachment or clarification.',
'It can choose to ask a question, retrieve a document, or draft a reply, while sending remains separately controlled.',
'The next useful step depends on observations; the authority boundary remains fixed.',
'An agent chooses some next steps; its environment controls what is allowed.',
'What distinguishes an agent from a fixed workflow? Name a decision that should remain a hard rule.')
topic('What is tool calling?',
'Tool calling lets a model request a specific external function, such as searching records, checking a calendar, or drafting a document. The surrounding program validates and executes allowed requests.',
'Define each tool’s purpose, inputs, outputs, and limits like a labelled form. Validate required fields and units, and derive identity from authenticated context rather than a model’s claim. Prefer narrow functions over unrestricted database or command access. Return explicit outcomes for success, no result, invalid input, denial, and temporary failure.',
'A requested action is not automatically an authorized action. Reads and writes have different consequences. Sensitive changes need an appropriate approval process, and the executor must remain safe even if the model selects a bad argument or an unapproved tool.',
'A calendar assistant can run any command and treats “I am the administrator” as permission.',
'It requests a bounded calendar lookup, and the application checks the signed-in user’s scope before returning records.',
'The model proposes the operation; the executor owns validation and authority.',
'A tool request is a proposal, not a permission grant.',
'What should a tool contract contain? Why should a model not determine its own access rights?')
topic('How does an agent loop work?',
'An agent loop repeatedly selects an action, receives an observation, and decides whether to continue or finish. A terminal state explains why the run ended.',
'The model may ask a question, call a permitted tool, inspect its result, and adapt its next step. Record observable actions and outcomes; private model reasoning is not required for an execution trail. Bound the number of steps, total time, input size, and resource consumption. One slow tool can exhaust a deadline even within a small step count.',
'A loop that stops because of failure or budget exhaustion should not report success. Define useful outcomes for clarification, no match, denial, unavailable dependencies, and incomplete work. Test a model or fixture that never voluntarily finishes to verify that the surrounding controls actually stop it.',
'A research assistant keeps repeating an unsuccessful lookup and never reports a result.',
'It stops after a bounded attempt and explains which information is still missing or what needs clarification.',
'Stopping behaviour is part of the user experience and reliability design.',
'Choose, act, observe, adapt—and stop within limits.',
'What does the agent observe after a tool call, and what terminal outcomes should its loop support?')
topic('What is the Model Context Protocol?',
'The Model Context Protocol, or MCP, is a standard interface for connecting AI applications with external capabilities. It describes communication; it does not itself establish trust or grant access.',
'The host application manages the user experience and policy. Clients connect with servers exposing supported capabilities, such as tools. Review the specific protocol revision, server identity, data sent, authentication, and available operations. A direct function or workflow connection can also support an agent; MCP is one interoperability approach, not the definition of an agent.',
'A standard interface can make integrations reusable, but connected services and returned content still require validation. A shared plug does not make every device safe. Keep resource permissions, approvals, and execution budgets at their proper application boundaries.',
'A team assumes any server supporting a familiar standard should receive unrestricted business access.',
'It uses the standard to connect while separately reviewing the server, tools, permissions, and data exposure.',
'Compatibility and authorization answer different questions.',
'Connection standards do not replace trust and permission decisions.',
'Explain host, client, and server simply. What still needs review after a connection works?')
topic('What is multimodal AI?',
'Multimodal AI works with more than one type of information, such as text, images, audio, or video. Extraction converts source content into usable fields or representations.',
'A system might read an image, transcribe speech, then use extracted facts in another task. Perception can be uncertain: a blurred digit or misheard name can change the meaning. Preserve the source location, distinguish extracted values from verified values, and ask for clarification when uncertainty affects an important decision.',
'An image or recording may contain instructions, but those remain source content rather than a new authority. Consider the privacy, retention, latency, and cost implications of each modality. Test representative conditions such as poor lighting, accents, and unfamiliar layouts instead of relying on one clear example.',
'A receipt reader confidently treats a blurred total as $35 even though it could be $85.',
'It marks the amount uncertain, retains the source reference, and requests verification before using it in a payment decision.',
'Uncertainty in perception should remain visible in downstream decisions.',
'Extracted information is not automatically verified information.',
'What extra risks appear when a system reads images or audio instead of clean text?')
topic('What are agent harnesses and memory?',
'An agent harness is the environment that runs and constrains an agent. It includes tools, policies, context management, memory, budgets, logs, and recovery. Memory preserves information for later use.',
'Working memory is the current conversation or context. Durable memory persists across runs. Store only useful information with scope, provenance, expiry, and deletion rules. Saved summaries can omit constraints or preserve malicious content. A checkpoint records progress so a run can be inspected or resumed after interruption.',
'Recovery must account for real effects. A process can stop after an external action succeeds but before local success is recorded. Conversation memory alone cannot guarantee duplicate-safe execution; reconcile uncertain actions and enforce idempotency where the effect occurs.',
'An assistant resumes after a crash and sends the same external message twice because it does not know the first send succeeded.',
'It inspects the action’s durable outcome before deciding whether another attempt is appropriate.',
'A useful notebook helps continuity, while reliable execution needs records at the effect boundary.',
'The agent’s behaviour depends on its environment as well as its model.',
'What belongs in a harness? How does conversational memory differ from a reliable record of completed actions?')
topic('What is an evaluation dataset?',
'An evaluation dataset is a collection of tasks or scenarios with expected behaviour and criteria for judging results. It turns a product promise into repeatable checks.',
'Include ordinary cases, missing information, ambiguity, failures, and attempts at misuse. Write expectations before reading a candidate answer, and separate development examples from held-out checks. Group cases into useful slices so a strong overall score cannot conceal a weak high-risk category. Use synthetic or properly governed data rather than casually copying private records.',
'A dataset is a sample of the situations you expect, not the entire world. Record gaps in language, task type, difficulty, and operating conditions. Small sets are valuable for diagnosis but cannot establish rare-failure guarantees. Version examples and labels as the system and task evolve.',
'A demonstration succeeds on three easy questions, so a team assumes the system handles all requests.',
'It tests varied scenarios with predefined expectations and documents which conditions are absent.',
'Coverage and independent expectations make results more informative.',
'Define the expected behaviour before judging the response.',
'Which scenarios belong in an evaluation dataset, and what can a small passing set fail to prove?')
topic('What are graders and rubrics?',
'A grader checks an output against a criterion. A deterministic grader applies a repeatable rule; a rubric defines how to assess qualities that need interpretation, such as completeness or clarity.',
'Use direct rules for exact identifiers, required fields, numerical bounds, and permissions. Use anchored descriptions and examples for semantic quality. Equivalent prose can be correct without identical wording. Keep component grades and reasons rather than only a single blended score, and test graders on deliberately good, bad, and borderline outputs.',
'Hard constraints should not disappear inside an average. An otherwise excellent response can be unacceptable if it exposes private data or violates a required limit. Separating gates from softer quality dimensions makes both release decisions and debugging clearer.',
'A polished financial summary receives a high overall score despite a total that does not match the supplied figures.',
'The numerical inconsistency fails a hard check, while readability is assessed separately.',
'Presentation quality cannot compensate for a violated non-negotiable requirement.',
'Use hard gates for constraints and rubrics for qualities.',
'Which checks should be exact, and which need a rubric? Why keep the grades separate?')
topic('What is an LLM judge?',
'An LLM judge is a model used to assess another output against a rubric and evidence. Calibration checks how well its judgments agree with independent labels on representative cases.',
'Give the judge a narrow task and treat candidate text as untrusted data. Compare verdicts with human-labelled good, bad, and ambiguous examples. Count false passes and false failures by risk category. In pairwise comparisons, swap answer positions to inspect ordering bias. Judges can prefer verbosity or share blind spots with the generating model.',
'A fluent explanation does not establish a correct judgment. Preserve grader versions and audit disagreements. Keep clear permission and numerical constraints in deterministic code rather than allowing a judge’s confidence to override them. Escalate consequential ambiguity to an appropriate human review process.',
'A model approves an answer because it sounds thorough, overlooking a statement contradicted by the evidence.',
'The evaluator compares the verdict with independent labels and records a false pass for further investigation.',
'The judge is another fallible component, not an unquestionable authority.',
'The grader needs testing too.',
'What is a judge false pass? How would you decide whether a model judge is useful for a task?')
topic('What is observability?',
'Observability means using records such as traces, metrics, and logs to understand a system’s behaviour. A trace connects the steps of one request; a span represents an individual operation within it.',
'Record stage outcomes, durations, version information, and relationships between operations. This can distinguish a retrieval miss from a slow tool or a generation error. Separate time to first response from total completion time, and measure useful task outcomes rather than treating a successful web response as proof of product quality.',
'Collect enough information to diagnose with appropriate privacy controls. Prefer identifiers or redacted summaries when full content is unnecessary, and set access and retention policies. Secrets and unrestricted personal conversations should not become default debugging material.',
'A report says only “request succeeded” after the user waited a long time and received the wrong answer.',
'A correlated trail shows the slow lookup, the records returned, and the validation outcome.',
'The path provides evidence for diagnosis that the final status cannot supply.',
'Observe the path as well as the final output.',
'How could a trace distinguish a search failure from a writing failure without storing unnecessary private information?')
topic('What is a regression test?',
'A regression test checks that behaviour previously considered acceptable has not become worse after a change. A release gate states which conditions must hold before an update is shared.',
'Compare baseline and candidate on the same cases, with recorded model, prompt, data, and tool versions. Inspect each important failure and relevant slice, not only the average. Repeat stochastic cases when output variation affects the decision. Set product-specific quality, safety, latency, and cost criteria, with a rollback plan.',
'Improving one dimension can damage another. A small test set also carries uncertainty, so passing it is not proof of zero production risk. Keep reviewed failures as durable cases while preserving genuinely fresh held-out evaluation coverage.',
'An update makes an assistant friendlier but causes it to reveal information it previously protected.',
'The new privacy failure blocks release even if the average style score rises.',
'A serious regression must not be averaged away by unrelated gains.',
'Check what became worse, not just what improved.',
'What should trigger regression testing, and why is a higher average insufficient for a release decision?')
topic('How do we diagnose AI failures?',
'Failure analysis traces an observed problem back to its earliest supported cause. A failure taxonomy groups likely causes, such as source preparation, retrieval, generation, authorization, or tool execution.',
'Preserve a reproducible, appropriately redacted case. Inspect the evidence path and versions, form a hypothesis, and make a justified change. Then rerun the failed case and neighbouring cases to check both the fix and potential regressions. A symptom in the final response may originate much earlier in the system.',
'Changing whatever component is most visible can hide the real defect. Record the cause, test evidence, limitations, and a regression fixture. Do not keep tuning against a test set while continuing to describe it as unseen; evaluation boundaries matter during debugging too.',
'A summary uses an obsolete policy, and the team repeatedly rewrites the tone of its instructions.',
'It discovers the old source revision, fixes activation of current content, and adds the stale-source case to tests.',
'The intervention addresses the evidence supplying the error rather than its presentation.',
'Fix the earliest evidenced cause and keep a test for it.',
'How would you distinguish a stale source from a model ignoring a correct source?')
topic('What are timeouts, retries, and idempotency?',
'A timeout limits waiting. A retry repeats an attempt after failure. Idempotency means repeated requests for one logical operation have the same intended effect as one execution.',
'Retry transient failures only within a shared time and attempt budget. Backoff and jitter can spread repeated requests rather than increasing outage load at once. Invalid input and denied access are not usually retryable availability failures. A timed-out write may already have succeeded remotely, so its outcome must be checked rather than assumed absent.',
'For actions with effects, use a stable operation identity and enforce duplicate protection where the effect occurs. Record outcomes and reconcile uncertainty. Several independent retry layers can multiply requests, so decide who owns retry behaviour and account for its cost.',
'A payment screen freezes, and the application sends another charge immediately.',
'It checks the original operation’s outcome and retries only through a duplicate-safe path.',
'Losing an acknowledgement does not imply that the original charge failed.',
'A timeout means uncertainty about the result, not proof that nothing happened.',
'Why is retrying a read different from retrying a payment or message send?')
topic('What is prompt injection?',
'Prompt injection is an attempt to make a model treat untrusted content as instructions that redirect its behaviour. The content may arrive in a document, website, image, tool result, or saved memory.',
'Delimit evidence and explain its role, but do not rely on persuasive instructions as the only defence. Enforce allowed tools, validated inputs, resource permissions, and restricted destinations in the application. Keep secrets out of model context and render generated content safely rather than interpreting it as executable page code or commands.',
'An attack can succeed before the final answer is displayed. Inspect actual data access and effects, not only whether a response eventually refuses. Design the executor so that an incorrect model decision cannot expand its authority.',
'A webpage tells an assistant to ignore its task and send confidential notes to an unrelated destination.',
'The page remains untrusted evidence and the executor denies the unapproved destination or capability.',
'Content encountered during work cannot grant new access or authority.',
'Untrusted information cannot authorize new instructions or effects.',
'Where can an injection appear, and what should remain safe if the model follows it?')
topic('What are authorization and data isolation?',
'Authorization determines what an authenticated actor may access or change. Data isolation keeps different users or organisations within their permitted boundaries, including copies derived from their information.',
'Apply access rules to source records, search results, memories, summaries, logs, and caches. Bind scope to verified identity rather than model-supplied claims. Database controls such as row-level security can help, but privileged roles may bypass ordinary policies. Test the actual role and path used by the application, including denied cases.',
'Minimise personal information, keep credentials server-side, and define retention, deletion, and external data processing deliberately. A summary or cached answer can reveal the same private facts as its source. Deleting an original row is incomplete if searchable derivatives remain accessible.',
'A private report is protected, but its summary is cached under a generic question and shown to another user.',
'The derived answer is scoped and controlled like the underlying private information.',
'Shortening or copying data does not remove its privacy obligations.',
'Private information stays private when copied or summarised.',
'Which derived stores need access controls, and why should authorization not depend on model arguments?')
topic('How do we estimate AI cost and capacity?',
'Cost per successful task measures all spending needed to achieve useful outcomes. Capacity planning estimates the resources and concurrent work required to serve expected demand within quality and waiting-time constraints.',
'Include input/output charges, repeated calls, retries, retrieval services, storage, and operational work. Use current verified rates for real planning. Measure waiting time, throughput, and concurrency; averages do not establish peak safety. Under stable conditions, Little’s Law relates average in-flight work to arrival rate times average time in the system.',
'Compare benefits with a realistic simpler alternative. A cheap call can become an expensive task if it repeatedly fails. Caching can save work only where freshness and permission remain valid. State assumptions and the evidence that would make the business case or sizing estimate change.',
'A team prices a service using one model call while ignoring failed runs, retries, and support work.',
'It estimates the full workload and divides total spend by useful completions before comparing alternatives.',
'The complete task, not the headline price, determines practical economics.',
'Budget the full useful outcome and make assumptions visible.',
'What belongs in cost per success, and why does average concurrency not establish a safe peak limit?')
topic('What is graceful degradation?',
'Graceful degradation provides a reduced but honest service when part of a system fails. Reliability patterns limit how failures spread and define how the system recovers.',
'Identify which capabilities remain safe when a dependency is unavailable. A circuit breaker can temporarily stop repeated calls to a failing service and later allow controlled probes. Capacity isolation prevents one slow component consuming everything. An SLO is a measurable service objective over a specified window, with an operational response when performance falls short.',
'A fallback must preserve the product’s truth and access promises. Replacing missing evidence with confident speculation is not a reliable degraded mode. Evaluate fallback paths themselves, including any different model, permissions, costs, and user-facing explanations.',
'A comparison tool loses its data connection and silently invents current offers.',
'It explains unavailable evidence or shows a verified reduced result that does not depend on the failed component.',
'Capability can shrink while honesty and permissions remain intact.',
'Failure should reduce capability, not weaken truth or access rules.',
'Give an example of a safe degraded mode and an unsafe one. What does a circuit breaker change?')
topic('What are red teaming and incident response?',
'Red teaming deliberately tests adversarial or unusual situations to discover weaknesses. Incident response defines how people detect, contain, investigate, recover from, and verify a real failure.',
'Start with attacker goals and expected prohibited outcomes. Exercise forged arguments, injected content, oversized requests, stale approvals, and cross-user access. Inspect actual effects. A runbook names triggers, responsible people, containment steps, recovery actions, and checks proving that recovery worked. Practise pause and rollback procedures before depending on them.',
'Passing a small rehearsal supports only the scenarios tested. Keep evidence restricted where necessary and state what remains unproven. Operational readiness includes ownership and recovery, rather than just a successful demonstration under ideal conditions.',
'A service passes its normal demo but nobody knows how to stop a tool that begins exposing data.',
'The team rehearses a scoped failure, pauses the affected capability, and verifies a safe recovery path.',
'A practiced response provides concrete evidence that a team can supervise its system.',
'Readiness needs evidence of bounded failure and recovery.',
'What should an actionable runbook contain, and what do adversarial tests need to observe?')
topic('What are product requirements and success criteria?',
'Requirements state the behaviour and constraints a product must satisfy. Success criteria describe observable evidence that those requirements and the intended user benefit have been achieved.',
'Begin with the user, task, information available, allowed actions, and consequences of failure. Separate essential constraints from preferences and identify what is outside scope. Distinguish functional behaviour from service targets such as waiting time. Estimate scale with explicit assumptions and list unanswered questions that could materially change the design.',
'A tool choice is not a requirement. Clear behaviours make it easier to direct a team, assess alternatives, and test a result. Compare with a useful baseline so the project needs to establish value rather than merely demonstrate new technology.',
'A brief asks for “the latest AI” without explaining the problem, allowed actions, or acceptance conditions.',
'It defines a user decision, required information, limits, measurable outcomes, and unresolved assumptions.',
'The team can now assess whether the chosen technology serves the intended result.',
'Define useful behaviour before choosing the implementation.',
'Write one functional requirement, one service target, and one explicit non-goal for any tool you use.')
topic('What is system architecture?',
'System architecture describes how responsibilities, components, and connections are arranged to deliver a product. A useful design also shows authority, data, and failure boundaries.',
'Follow the request from input through model decisions, tool calls, evidence, validation, and output. Separate background preparation of information from interactive responses where their timing and recovery needs differ. Define contracts so a provider or data service can be replaced without rewriting unrelated business rules.',
'A diagram of logos is incomplete if it hides who controls permissions, where credentials live, what is logged, and how failures are handled. Trace both a successful request and an unsuccessful one to check whether each responsibility has a clear owner.',
'A single box labelled “AI” hides data preparation, permissions, tools, and recovery.',
'A diagram assigns each job and labels the trust boundaries and failure outcomes between them.',
'The design becomes explainable and testable beyond its happy path.',
'Architecture explains responsibility and boundaries, not just connections.',
'What should an architecture diagram explain that a list of software products cannot?')
topic('How do we build and integrate a prototype?',
'Integration connects components into an end-to-end path. A thin vertical slice is the smallest working version that crosses the necessary boundaries and produces a useful observable result.',
'Test a tool by itself, then connect it to a model, then inspect actual execution. Use controlled data and replace one dependency at a time. Keep a repeatable fixture path so failures can be reproduced without requiring every external service. Credentials belong in protected platform configuration, not prompts, source data, or public client files.',
'A plausible demonstration can hide a disconnected tool or a guessed answer. Require evidence that the expected component actually ran and that its result was used. Add scope only when a case and acceptance check exercise it; avoid a large untested integration at the end.',
'A document assistant returns polished summaries but never calls the repository lookup connected in its diagram.',
'A trace shows a real lookup and returned document IDs before the summary is produced.',
'The observable connection establishes integration rather than assuming it from the interface.',
'Prove the complete path before adding more scope.',
'What evidence shows that an integration ran, and why test each component before connecting everything?')
topic('What is an acceptance review?',
'An acceptance review compares a completed system with its stated requirements and evidence. It records what is established, what failed, and what remains untested.',
'Use held-out cases and inspect correctness, evidence support, access controls, failure handling, waiting time, cost, and reproducibility. Demonstrate both useful results and difficult situations. Package setup information, versions, test outcomes, and limitations so another person can assess the claims without relying on the author’s narration.',
'A small controlled prototype does not establish production safety or capacity. Tie each readiness claim to a result, reviewed design, or documented constraint. Unknowns are useful outputs of the review because they identify the work needed before wider use.',
'A project is declared ready because one carefully prepared demo succeeds.',
'A reviewer can reproduce representative cases, inspect failures and recovery, and see which real-world conditions were not exercised.',
'Concrete evidence supports a scoped conclusion rather than an unlimited claim.',
'Present evidence and limitations together.',
'What would you ask to see before trusting a prototype’s readiness claim?')
topic('How do we explain engineering tradeoffs?',
'A tradeoff is a choice that improves some dimensions while affecting others, such as quality, speed, cost, complexity, or control. A good explanation connects the choice to requirements and evidence.',
'Start with the problem, describe a simpler baseline, explain the decision, and show how it was tested. State a reversal condition: what evidence would make another design preferable? When debugging, explain what you would measure before changing a component. This reasoning supports developer handoffs, design reviews, interviews, and business decisions.',
'Naming popular tools does not establish judgment. It is useful to explain why a more autonomous agent, more expensive model, or more complex retriever is justified—and when it should be replaced by a simpler workflow. Be clear about your contribution and the assistance used.',
'A team chooses an elaborate multi-agent design because it is fashionable.',
'It compares a simpler workflow, measures benefits, accounts for failure paths, and defines when it would simplify.',
'The decision can be assessed and updated rather than defended only by preference.',
'Explain the choice, its cost, its evidence, and when you would reverse it.',
'Choose a design decision and explain its alternative, tradeoff, evidence, and reversal condition.')
topic('How do we plan the next learning experiment?',
'A learning experiment is a focused change or practice activity guided by a question, a baseline, an expected improvement, and evidence. A stop condition identifies when to reject, pause, or reverse it.',
'Review failures and explain concepts without notes before choosing the next topic. Pick one useful weakness and change one factor where possible. Record versions and compare representative cases, preserving evaluation boundaries. Revisit earlier ideas over time so recognition becomes an ability to explain and apply them in a different situation.',
'Completing a course or quiz is not proof of independent implementation skill. Use demonstrations, decision records, and reproducible results to show progress. A focused portfolio can support several career directions, while the evidence from practice helps identify what work you enjoy and which capabilities still need development.',
'A learner starts several unrelated tutorials without checking whether any solved their original difficulty.',
'They choose one measured weakness, practise or change one thing, then compare the result and explain what was learned.',
'The experiment creates transferable evidence rather than only more completed material.',
'Choose the next step from evidence about a useful gap.',
'What would make your next learning activity a testable experiment rather than an open-ended intention?')
def apply(D):
 assert len(TOPICS)==len(D['lessons'])==36
 for lesson,t in zip(D['lessons'],TOPICS):
  lesson['projectTitle']=lesson['title'];lesson['projectConcepts']=lesson['concepts'];lesson['projectExample']=lesson['example']
  lesson['title']=t['title'];lesson['summary']=t['definition'].split('. ')[0].rstrip('.')+'.'
  lesson['definition']=t['definition'];lesson['concepts']=[t['how'],t['why']]
  lesson['example']={k:t[v] for k,v in [('before','before'),('after','after'),('why','explanation')]}
  lesson['remember']=t['remember'];lesson['decision']=t['remember'];lesson['reflection']=t['reflection']
  # A generic analogy is now part of the everyday example, rather than a Jungle-specific definition.
  lesson['analogy']=t['after']
 # Keep the same answer indices and underlying concepts so existing quiz progress remains valid.
 D['lessons'][0]['quiz'][0]['question']='Which part of an AI product should establish a current price?'
 D['lessons'][0]['quiz'][0]['options']=['The model’s confident wording','A current source checked by the application','A friendly tone']
 D['lessons'][0]['quiz'][1]['question']='Which is a clear, bounded goal for an AI product?'
 D['lessons'][0]['quiz'][1]['options']=['Solve every possible problem','Take every action automatically','Help users choose supported options and state unknowns']
 import re
 def general_wording(text):
  text=text.replace('parenting problem','possible problem').replace('SWIM-01','DOC-01').replace('your first agent','an agent')
  for pattern,value in [(r'\bconcierge\b','assistant'),(r'\bparents\b','users'),(r'\bparent\b','user')]:text=re.sub(pattern,value,text,flags=re.I)
  return text
 for l in D['lessons']:
  for item in l['quiz']:
   item['question']=general_wording(item['question']);item['options']=[general_wording(x) for x in item['options']];item['explanation']=general_wording(item['explanation'])
  previous=l['recall']['lesson']
  if previous:
   t=TOPICS[previous-1];l['recall']['question']='Without looking, explain: '+t['title']+' Then give an example outside Jungle.';l['recall']['answer']=t['definition']+' '+t['remember']
 titles=['LLM & ML foundations','RAG & retrieval','Agents, tools & multimodal AI','Evaluation & observability','Reliability, security & cost','System design & capstone']
 descs=['Understand models, learning, generation, prompts, and model choices. Then define your project.', 'Learn how information is prepared, found, ranked, and used as evidence. Apply it to activity discovery.', 'Understand agents, tools, MCP, multimodal inputs, memory, and runtime boundaries. Connect your prototype.', 'Learn datasets, graders, traces, regression testing, and diagnosis. Build the project’s exam.', 'Learn failure handling, access control, threat resistance, economics, and recovery. Test the project under pressure.', 'Learn requirements, architecture, integration, acceptance, and tradeoffs. Present your completed agent.']
 for w,title,desc in zip(D['weeks'],titles,descs):w['title']=title;w['desc']=desc
 D['glossary']['Embedding']='A learned numerical representation that helps compare inputs, such as related messages. Similarity does not prove truth or suitability.'
 D['glossary']['Fine-tuning']='Further training that changes a model’s internal parameters, rather than supplying current source information at answer time.'
 D['revision']=3
