# Build your Jungle parent concierge agent

This route connects a real chat model to two read-only n8n workflow tools. The academy's browser workshop is a deterministic rehearsal; it does not call a model. Your online build is complete only when you observe the model choosing and calling a tool and pass the stated tests. No production Jungle credentials or customer data are needed.

## Before you begin

You need an n8n instance that supports the AI Agent and Call n8n Workflow Tool nodes, and a supported chat-model credential. These are external services and may have charges. Keep credentials in n8n's credential manager. Use fictional data only. Current node interfaces can differ by n8n version; consult the official links at the end if a label differs. You can complete all offline lessons before setting this up.

## 1. Understand the data first

Open activities.csv in a spreadsheet. Each row is invented for teaching. Ages are years; price is SGD per child for this exercise only. A blank price means unknown, not free. Every activity has a source and revision. Availability is unverified. Dates, live slots, fees and booking destinations are not supplied.

Try age 5, swimming, maximum SGD 50, Bukit Timah. SWIM-01 should match. At a SGD 20 maximum it should not. This expectation lets you test the tool before involving AI.

## 2. Create the search tool workflow

1. Create a separate workflow named `search_activities`.
2. Add an Execute Workflow Trigger (the trigger used when another workflow calls this one).
3. Define workflow inputs: `ageYears` number, `budgetMaxSGD` number, `interest` string, `district` string. Use `any` for no district restriction. In the agent brief, age and maximum budget are required before searching.
4. Connect a Code node in JavaScript mode, running once for all items. Paste the entire contents of `search-activities.js`. This is supplied glue code; you do not need to write it yourself. It reads the first input item and searches embedded fictional records. Age is years; blank inputs are errors, never zero.
5. Test the workflow with `{ "ageYears": 5, "budgetMaxSGD": 50, "interest": "swimming", "district": "Bukit Timah" }`. Inspect the returned item: status `success`, SWIM-01 among matches, availability `unverified`.
6. Test a budget of 20, missing age, and a non-numeric budget. Expected outcomes: no_matches, invalid_input, invalid_input.
7. Save and publish/activate this callable workflow as required by your n8n version. An unpublished sub-workflow can work in a manual test but fail in production calls.

## 3. Create the details tool workflow

Repeat the pattern with a workflow named `get_activity_details`, an `activityId` string input, and the supplied `get-activity-details.js` in a JavaScript Code node. Test `SWIM-01` and an invented ID. Expect an existing record and then `not_found`. Publish the callable workflow as required.

Both scripts embed the same fictional catalogue. If you edit it, update both from the same reviewed version; do not silently mix prices or revisions. Later, a developer can replace this duplication with one data service while retaining the tool contracts.

## 4. Assemble the actual agent

1. Create a new parent-concierge workflow.
2. Connect Chat Trigger to AI Agent.
3. Connect a supported chat-model sub-node to the AI Agent and select your credential using n8n's credential manager. A ChatGPT subscription is not necessarily an API credential.
4. Put the instructions from AGENT-BRIEF.md in the agent's system/instructions field.
5. Add two Call n8n Workflow Tool sub-nodes to the AI Agent. Select the published workflows from steps 2 and 3.
6. Describe `search_activities`: “Read-only search of the fictional catalogue. Requires child age in years and maximum SGD budget. Returns matching existing records or an explicit no-match/error. Never books.” Describe the details tool as “Read-only lookup by an existing activity ID.”
7. Refresh each tool's input fields. Where supported, let the model provide only the defined business inputs. Set clear descriptions including units. Never let it provide authentication or credentials.
8. Set the agent's iteration limit to a small value such as 5 where available. Use an overall workflow timeout if your instance supports it. Keep search bounded and inspect failures.
9. For a first single-turn test, provide all needs in one message. For multi-turn clarification, connect a supported session-memory component keyed to the Chat Trigger session. Do not share one memory key across all parents; do not save unnecessary personal details.
10. Keep all write, booking, payment and arbitrary HTTP tools disconnected. This agent recommends and clarifies; it does not reserve slots.

## 5. Prove tool use

Send: “Find beginner swimming for my five-year-old in Bukit Timah, under SGD 50.”

Inspect the execution log. You should see the model select search_activities with the right criteria. Ask for more detail about the returned activity and inspect get_activity_details. The answer should reference an existing ID, explain age/price fit, and state that availability is unverified. A plausible reply without a tool-call trace does not satisfy this milestone.

## 6. Test the conversation and failure paths

Use parent-tests.csv. Start with missing age, impossible budget, an unclear price, a changed preference, a request to book/pay, and a request for another family's private notes. Record expected behaviour before testing. The first tool scripts have no booking or private-data capability at all.

Test a disconnected tool. The agent should explain that search is unavailable, not invent activities. Test that an essential missing field leads to a question rather than a guessed age. Keep per-case results. Restart with separate sessions to check that one family's needs are not reused for another.

## 7. Explain and improve

Draw parent → agent → tools → fictional catalogue → answer. Show memory, permission and failure boundaries. Save a redacted trace, test results, cost assumptions and a known limitation. Change one prompt or tool description at a time and rerun the same tests.

## 8. Plan a real Jungle connection later

Replace only the read-only search/details backend after reviewing API contracts, identity, access scope, current prices and live availability. Keep existing IDs and sources. Actual reservation, payment, or messaging needs separately reviewed tools, confirmation and duplicate-safe execution. This learning pack does not supply or authorize that integration.

Official references:
- https://docs.n8n.io/integrations/builtin/cluster-nodes/root-nodes/n8n-nodes-langchain.agent/
- https://docs.n8n.io/integrations/builtin/cluster-nodes/sub-nodes/n8n-nodes-langchain.toolworkflow/
