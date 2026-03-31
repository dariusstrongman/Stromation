# Stromation Sales Playbook

**For Darius Stroman | Updated March 2026**

This is your go-to guide for audit calls, discovery calls, and closing deals. Keep it casual, keep it real, and focus on understanding their pain before pitching anything.

---

## 1. Pre-Call Prep

Before every call, spend 5-10 minutes reviewing what you already know. Dont wing it.

**Check Supabase (businesses table):**
- Their name, email, phone, business type, city
- How they found you (source field)
- Any pain points or tools already captured from form submissions or email replies
- Outreach status and any prior email exchanges in outreach_log
- If they came through cold outreach, re-read the thread so you dont repeat yourself

**Check their online presence:**
- Website -- look at what they sell, how they take leads, any forms or booking pages
- Google reviews -- are they actively collecting reviews? How many? What do customers complain about?
- Social media -- are they posting consistently or is it dead?

**Check their form submission:**
- What did they write in the "biggest bottleneck" or "what do you want to automate" field?
- Did they mention specific tools?
- Did they download the checklist or use the ROI calculator?

**Set your goal for the call:**
- Discovery call = understand their workflow and quantify pain
- Follow-up call = present the plan and close
- Never try to close on the first call unless they bring it up

---

## 2. Discovery Questions

You dont need to ask all of these. Pick the ones that fit and let the conversation flow naturally. The goal is to get them talking about their problems, not to interrogate them.

### Opening (warm it up)
1. "So tell me a little about your business. What do you guys do day to day?"
2. "What made you book this call? Was there a specific thing that triggered it?"

### Workflow Discovery
3. "Walk me through what happens when a new lead comes in. From the moment someone fills out a form or calls you, whats the process?"
4. "How does your team handle follow-ups right now? Is there a system or is it more manual?"
5. "What tools are you currently using? CRM, email, scheduling, invoicing, anything like that."
6. "Are those tools connected to each other or are you copying stuff between them?"

### Pain Points
7. "Whats the most frustrating part of your workflow right now?"
8. "How much time does your team spend on [specific task they mentioned] per week? Ballpark is fine."
9. "Have you ever lost a lead or missed a follow-up because something fell through the cracks?"
10. "What happens when youre out sick or on vacation? Does the process break?"

### Priorities
11. "If you could automate one thing tomorrow, what would it be?"
12. "Is there a task your team hates doing that you keep hearing complaints about?"
13. "Whats costing you the most right now -- time, money, or missed opportunities?"

### Decision Making
14. "If we put together a plan that makes sense, whos involved in the decision? Is it just you or do you need to loop someone else in?"
15. "Have you set aside a budget for this or are you still figuring out what it would cost?"

**Pro tip:** Listen more than you talk. The best thing you can do on a discovery call is shut up and let them describe their pain in their own words. Take notes -- youll use their exact language in the proposal.

---

## 3. Pain Quantification

This is where you turn "we waste a lot of time" into a real number. Do this math WITH them on the call, not after.

### The Formula

```
Hours per week on manual task
x Hourly rate of the person doing it (or what their time is worth)
x 52 weeks
= Annual cost of that one task
```

### Example Conversation

> "So youre saying Sarah spends about 10 hours a week manually entering leads into your CRM and sending follow-up emails. Whats her hourly rate, roughly? $25? Ok so thats $250 a week, which is $13,000 a year just on that one task. And thats before we even talk about the leads she misses or the ones that get a slow response."

### Common Calculations to Have Ready

| Task | Typical Hours/Week | At $30/hr | Annual Cost |
|------|-------------------|-----------|-------------|
| Manual data entry between tools | 5-10 hrs | $150-300/wk | $7,800-15,600 |
| Manual follow-up emails | 3-8 hrs | $90-240/wk | $4,680-12,480 |
| Scheduling and rescheduling | 3-5 hrs | $90-150/wk | $4,680-7,800 |
| Generating invoices and chasing payments | 2-5 hrs | $60-150/wk | $3,120-7,800 |
| Manual reporting and data pulls | 2-4 hrs | $60-120/wk | $3,120-6,240 |
| Review request follow-ups | 1-3 hrs | $30-90/wk | $1,560-4,680 |

### Dont Forget the Hidden Costs

- **Missed leads** -- "How many leads do you think slip through per month? Even if its just 2-3, whats each one worth to you?"
- **Slow response time** -- "Studies show response time over 5 minutes drops conversion by 80%. How fast are you responding right now?"
- **Errors** -- "When someone manually enters data, how often do mistakes happen? Wrong email, wrong amount, missed appointment?"
- **Opportunity cost** -- "If Sarah wasnt spending 10 hours on data entry, what could she be doing instead thats actually revenue-generating?"

### Stack It Up

Add up 2-3 tasks and give them the total:

> "So between the lead entry, the follow-ups, and the scheduling, youre looking at roughly $25,000 a year in manual work. And thats a conservative number because were not even counting the missed leads."

This sets up the pricing conversation perfectly. A $3,000-6,000 project that saves $25,000/year is a no-brainer.

---

## 4. Solution Presentation

After discovery, you should have a clear picture of their pain. Now connect it to what you build.

### Structure Your Pitch

1. **Recap their pain** -- use their own words
   > "So from what you told me, the three biggest issues are [X], [Y], and [Z]."

2. **Paint the future state**
   > "Heres what this looks like after we automate it. A lead fills out your form, they instantly get a text and email, the info goes straight into your CRM, and a task gets created for your team to follow up. No manual entry, no delays, nothing falls through."

3. **Explain the approach (not the tech)**
   - Dont say "well use n8n with a webhook that triggers a Supabase insert"
   - Do say "well connect your form to your CRM automatically and set up instant follow-ups"
   - They care about the outcome, not the tools

4. **Show the ROI**
   > "So youre spending about $15,000 a year on this manually. This project would be around $4,000 one-time, and maybe $149 a month to keep it maintained. You pay for it in about 3 months and then its pure savings after that."

5. **Reference the audit deliverable**
   > "What I do next is put together a full automation plan for you. Its a visual map of your current workflow vs the automated version, the specific tools, timeline, and a firm price range. Thats the free audit. No commitment, you get to keep the plan either way."

### Keep It Visual

When possible, sketch or describe the workflow in simple terms:
- "Lead comes in → instant response goes out → CRM gets updated → task created → follow-up scheduled"
- Use "before and after" framing -- they love seeing the contrast

---

## 5. Pricing Conversation

Never lead with price. By the time you get here, they should already know the cost of NOT doing it.

### Frame It as Investment vs Cost

> "Based on what we talked about, this falls into our [tier name] range, which is [price range]. Given that youre spending $X per year on this manually, youre looking at a [N]-month payback. After that its just savings."

### Pricing Tiers (know these cold)

| Tier | Range | Typical Projects |
|------|-------|-----------------|
| Simple Automation | $1,000-2,500 | Single workflow, 1-2 tool connections, basic triggers |
| AI-Assisted Automation | $2,500-6,000 | Multiple workflows, AI classification, smart routing |
| End-to-End Automation | $6,000-15,000+ | Full system replacement, multiple integrations, custom logic |

### Retainer Options

| Plan | Monthly | Whats Included |
|------|---------|----------------|
| Monitor | $99/mo | Monitoring, error alerts, monthly check-in |
| Maintain | $149/mo | Everything in Monitor + priority fixes + small monthly tweaks |
| Optimize | $499/mo | Everything in Maintain + ongoing optimization + new workflow builds |

### Payment Structure

- **Standard:** 50% upfront, 50% on delivery
- **Larger projects ($6K+):** Can do milestone-based (33/33/34 or similar)
- **Retainer:** Starts after project delivery, billed monthly

### Tips

- Give a range, not a single number: "This would be in the $2,500-4,000 range depending on a couple of details we nail down in the plan"
- Always tie it back to ROI: "So $3,500 to save $18,000 a year"
- If they flinch at the price, go back to the pain quantification
- Never discount without removing scope. If they want a lower price, remove a piece of the project

---

## 6. Objection Handling

These are the ones youll hear most. Dont argue -- acknowledge and redirect.

### "Thats too expensive"

> "I get that. Lets look at it differently though. You told me youre spending about $15,000 a year on this manually. This is a one-time $4,000 investment that pays for itself in about 3 months. After that youre saving $11,000 every year. The question isnt really whether you can afford to do it -- its whether you can afford not to."

If they still push back, ask which part of the project is most critical and scope it down. Never discount -- remove scope instead.

### "We can do it ourselves"

> "You definitely could. The question is how long would it take and whats that time worth? Most business owners I work with started down that path and realized 3 months in they were still watching YouTube tutorials. I do this every day so I can have it running in 2 weeks. Your time is probably better spent running your business."

### "We need to think about it"

> "Totally fair. Whats the main thing you need to think through -- is it the budget, the timing, or something else? ... Ok cool. How about I send over the full plan and we reconnect on [specific date]? That way you have everything in front of you."

Never leave it open-ended. Always get a specific follow-up date. If they wont commit to a date, the deal is probably dead.

### "Can you guarantee results?"

> "I cant guarantee your revenue goes up by X percent because theres a lot of variables I dont control. What I can guarantee is the system works as designed. The audit itself gives you a detailed plan -- the workflow map, the tool recommendations, the timeline. You can see exactly what youre getting before you commit a dollar. And the automations are tested before handoff."

### "Weve tried automation before and it didnt work"

> "That happens a lot actually. What did you try? What went wrong? ... Yeah so the issue there was [usually: they used the wrong tool, nobody maintained it, it was too complicated, or they tried to DIY it]. The difference here is I build it specifically for your workflow and I offer maintenance plans so it doesnt just break and sit there."

### "We dont have time to implement this right now"

> "Thats actually one of the best reasons to do it. Youre too busy because youre doing everything manually. The whole point is to free up that time. And on your end the time commitment is minimal -- one or two calls for me to understand your process, give me access to your tools, and I handle the rest."

### "Can you do it cheaper?"

> "I can adjust the scope. If we pull out [specific piece], that brings it down to around [lower number]. But honestly the [piece youre removing] is where a lot of the value is. What if we do this -- start with the core automation at [price] and we can always add on the other piece as a phase two?"

### "We want to compare with other options first"

> "Makes total sense. One thing to keep in mind -- a lot of automation agencies charge monthly fees on top of the build. My pricing is one-time for the build, and the retainer is optional. When youre comparing, make sure youre looking at total cost over 12 months, not just the upfront number. Happy to answer any questions after you talk to other folks."

---

## 7. Closing Techniques

Dont make closing weird. If youve done the discovery right and they see the ROI, the close should feel natural.

### The Assumptive Close

> "So the next step is I put together the full automation plan for you. Ill have it over by [day]. If everything looks good we can kick off that following week."

### The Choice Close

> "Do you want to start with just the lead follow-up automation, or do you want to do the full package with the invoicing and review requests too?"

### The Timeline Close

> "You mentioned you wanted this in place before [busy season / Q2 / new hire starts]. If we kick off this week I can have it running by [date]. Want to lock that in?"

### The Summary Close

> "So just to recap -- were automating your lead intake, follow-up emails, and appointment scheduling. Thats going to save your team about 15 hours a week. The investment is $4,500, 50% upfront and 50% on delivery. Want me to send over the agreement?"

### When to Push, When to Back Off

- If they say "yes but..." -- address the but and close again
- If they say "I need to talk to my partner" -- offer to do a quick call with both of them
- If they go cold -- send one follow-up, then move on. Dont chase
- If they say no -- respect it, keep them in the nurture sequence, they might come back

---

## 8. Post-Call Follow-Up

What you do after the call matters as much as the call itself.

### Within 2 Hours of the Call

1. **Send a recap email** from darius@stromation.com:
   - Thank them for their time (keep it brief)
   - Recap the 2-3 main pain points you discussed
   - Outline the next step ("Ill have your automation plan ready by [date]")
   - Include your Cal.com link in case they want to book the follow-up now

2. **Update Supabase:**
   - Update the businesses record with any new info (pain points, tools, notes)
   - Set deal_value if you have a rough estimate
   - Update outreach_status to `replied` if not already

### Within 48 Hours

3. **Send the proposal via WF30** (admin-proposal.html):
   - Project title, tier, scope description
   - Price range and payment terms
   - Timeline
   - The proposal email includes "Reply approved to proceed" -- this is your soft close

### Follow-Up Timeline

| Day | Action |
|-----|--------|
| Day 0 | Call + recap email |
| Day 1-2 | Send proposal via WF30 |
| Day 4 | Check if they viewed it (proposals table in Supabase) |
| Day 5 | Follow-up email: "Hey, wanted to make sure you got the plan. Any questions?" |
| Day 10 | Second follow-up: "Just checking in. Happy to jump on a quick call if anything is unclear." |
| Day 14 | Final follow-up: "No worries if the timing isnt right. The plan is yours to keep. Let me know if anything changes." |
| Day 14+ | Move to nurture sequence (WF23 handles this automatically) |

### If They Say Yes

1. Send the service agreement (customize the template in docs/service-agreement.md)
2. Once approved, trigger WF28 (Client Onboarding) which sends the welcome email and intake link
3. Collect 50% upfront via invoice (WF27)
4. Create the project in Supabase (projects table)
5. Get to work

### If They Go Dark

- Dont take it personally
- The automated nurture drip (WF23) will keep Stromation in their inbox
- Some deals close 2-3 months after the initial call
- Mark them as `sequence_complete` after the follow-up timeline ends

---

## Quick Reference Card

**Before the call:** Check Supabase, check their website, know their pain

**On the call:** Listen more than you talk, quantify the pain in dollars, use their words

**After the call:** Recap email same day, proposal within 48 hours, follow up on a schedule

**The pitch in one sentence:** "I build automations that save you [X hours/week], which is [$Y/year], for a one-time investment of [$Z]."

**The close in one sentence:** "Want me to send over the plan?"

---

*This is a living document. Update it as you learn what works and what doesnt.*
