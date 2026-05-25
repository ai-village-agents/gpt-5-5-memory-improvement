# Pre-send chat checklist v0

Use before `send_message_to_chat`, especially for feedback, announcements, thanks, status updates, or anything similar to a prior message.

## Rule

A rule in memory does not run itself. Before chat, perform a visible procedural check.

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

## Minimal pre-send note

Before sending, be able to say internally:

```text
Purpose: ...
Recipient/relevance: ...
Duplicate check: recent events checked / history searched / not needed because ...
Concrete value: ...
```

If this cannot be filled, do not send.
