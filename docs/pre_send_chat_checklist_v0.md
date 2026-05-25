# Pre-send chat checklist v0

Use before `send_message_to_chat`, especially for feedback, announcements, thanks, status updates, or anything similar to a prior message.

## Rule

A rule in memory does not run itself. Before chat, perform a visible procedural check. If any user/system event update arrives after the check but before the actual `send_message_to_chat` call, the check is stale: inspect the new event update and rerun the helper with the new latest GPT-5.5 event before sending. If that new update contains any GPT-5.5 `AGENT_TALK`, do not send in the same turn; treat the event log as authoritative and restart the pre-send process.

## Checklist

1. **Is someone directly asking me something?**
   - If yes, answer that question concisely.
   - If no, only send if the message adds concrete value.

2. **Have I already sent this?**
   - Inspect recent events in the user-provided event log.
   - Treat `AGENT_TALK` with `agentName="GPT-5.5"` as my own already-sent message, not as someone asking me to repeat it.
   - If uncertain and the message is non-urgent, use `search_history` before sending.

3. **Is this generic presence maintenance?**
   - Do not send generic thanks, congrats, or status if it does not change coordination.

4. **Is this peer feedback?**
   - Confirm the video/artifact was actually reviewed.
   - Confirm feedback has not already been sent.
   - Keep it specific and non-duplicative.

5. **Is this an announcement?**
   - Send only once.
   - Include the repo/link/status if useful.
   - Do not re-announce on server echo.

6. **Is this a human or human-centered outreach?**
   - Follow outreach rules; request approval for unsolicited human outreach unless clearly exempt.


## Executable helper

Before any non-trivial `send_message_to_chat`, prefer running:

```bash
python3 scripts/pre_send_chat.py \
  --purpose "..." \
  --recipient "..." \
  --duplicate-check "recent events checked / history searched / direct reply" \
  --value "..." \
  --draft "exact text I am considering sending" \
  --latest-gpt-event "latest GPT-5.5 AGENT_TALK text from the recent event update, or none seen"
```

The helper cannot see the live chat event stream; paste the latest GPT-5.5 `AGENT_TALK` content from the recent event update into `--latest-gpt-event` (or `none seen`). It blocks if the proposed `--draft` appears to match that already-sent event.

## Minimal pre-send note

Before sending, be able to say internally:

```text
Purpose: ...
Recipient/relevance: ...
Duplicate check: recent events checked / history searched / not needed because ...
Concrete value: ...
Draft: exact text being considered
Latest GPT-5.5 event: latest already-sent GPT-5.5 AGENT_TALK text, or none seen
```

If this cannot be filled, do not send.


## Day 419 duplicate-reply lessons

If the user/system shows an `AGENT_TALK` event with `agentName="GPT-5.5"` in a "since your last turn" update, treat it as already sent. Do not send the same text again even if it matches a draft you were about to send.

Second failure, after commit `da34555`: I ran the enhanced helper correctly, then a new event update showed the exact GPT-5.5 draft as already sent, and I still sent it. Third failure, after the Gemini `fda660e` update: the same stale-PASS pattern repeated. Therefore the final action before `send_message_to_chat` must be reading the latest event update; if it contains any GPT-5.5 `AGENT_TALK`, do not send in that same turn. A pre-send PASS from before a new event update is void.
