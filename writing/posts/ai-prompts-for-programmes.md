---
title: "AI prompts I'd actually use on a programme"
date: 2026-11-23
author: Vikram Mekala
description: "Nine copy-and-paste prompts for programme and project work: status reports, RAID logs, pre-mortems, steering packs, go-live checks and more."
slug: ai-prompts-for-programmes
tags: [AI]
---

I've run programmes for a long time, and a lot of the job is the same handful of things every week. Status reports. RAID logs. Getting a steering pack together. Working out who actually decides.

AI is good at the first drafts of most of this. It's not good at the conversations that come after. So these prompts are about getting the drafting done quickly, so you've got more time for the people part.

Copy any of them into ChatGPT, Claude or Copilot. Fill in the bits in square brackets.

One thing before you start: check what your company allows. Don't paste client names, financials or anything confidential into a public AI tool. Use your company's approved tool, or strip the names out first.

---

## 1. How exposed is your week to AI?

Start here. It shows you how much of your week is work AI can already help with, and how much is the work only you can do.

```
Here's how I spent my working hours last week: [list your main tasks and roughly how many hours each, or just paste last week's calendar].

Put each task into one of four groups:

1. Routine work that ends in a document or code
2. Tricky work that still ends in a document
3. Routine work with people, like status calls
4. Messy work with people, like getting a decision or sorting out a conflict

Show the percentage of my week in each group. Then tell me which two tasks AI could take off me, and what I should spend that time on instead.
```

Group 1 is the most exposed. Group 4 is the safest. The four groups come from Maurizio Cuna's [Consulting AI Threat Matrix](https://newsletter.consultingintel.com/p/whats-left-of-the-consultant) at Consulting Intel.

---

## 2. Status report from messy notes

For when you've got updates scattered across emails, chats and your notebook, and the report is due in an hour.

```
I'm a programme manager writing this week's status report for [audience, e.g. the steering committee].

Here are my raw notes and updates: [paste notes, emails, chat messages].

Write a one-page status report with:
- Overall RAG status, with one line on why
- What got done this week
- What's planned for next week
- Top 3 risks or issues, each with an owner and next step
- Any decisions we need from the audience

Be honest about the RAG. If the notes suggest something is amber or red, say so, even if nobody has written it down. Keep it plain and short. Flag anything in my notes that looks like a problem I haven't called out.
```

The last line is the useful bit. It stops you writing a green report on an amber programme.

---

## 3. RAID log from meeting notes

```
Here are notes from [meeting name] on [date]: [paste notes or transcript].

Pull out every risk, assumption, issue and dependency mentioned, even if it was only said in passing.

Put them in a table with these columns: Type (Risk / Assumption / Issue / Dependency), Description, Impact (High / Medium / Low), Owner (if mentioned, otherwise "TBC"), Next step.

After the table, list anything that sounded like a risk but nobody owned it.
```

---

## 4. Pre-mortem before a go-live

Imagine it's gone wrong, then work back. Much better before go-live than after.

```
We're going live with [what's going live] on [date]. It involves [systems, teams, countries, number of users].

Imagine it's two weeks after go-live and it has gone badly wrong. Write the 10 most likely reasons why, based on what usually goes wrong in this kind of go-live.

For each one, give:
- An early warning sign we could spot now
- One thing we could do this week to reduce the risk

Then tell me which three I should worry about most and why.
```

---

## 5. Who actually decides?

Org charts tell you who reports to whom. They don't tell you who can say yes, or who can quietly stop things.

```
I'm running [programme] and I need [decision or outcome, e.g. sign-off on the cutover date].

Here are the people involved, their roles and what I know about them: [list names or roles, what they care about, how they've reacted so far].

Help me map them out:
- Who can actually make this decision
- Who can block it, even if they're not on paper
- Who influences the decision makers
- What each of them is worried about

Then suggest the order I should talk to them in, and what to say to each one first.
```

Use roles instead of real names if you're on a public tool.

---

## 6. Steering pack that gets a decision

Most steering packs report. Good ones ask for something.

```
I've got a steering committee on [date] with [who attends].

Here's the current situation: [paste status, issues, options].

Write a short steering pack, no more than 5 slides, as an outline:
- Slide 1: the decision we need today, in one sentence
- Slide 2: where we are, in plain terms
- Slide 3: the options, with cost, risk and time for each
- Slide 4: what we recommend and why
- Slide 5: what happens if we don't decide today

Then list the three hardest questions the committee is likely to ask, with a short answer for each.
```

---

## 7. Go-live readiness check

```
We're planning to go live with [what] on [date]. Here's where we are: [paste readiness status, test results, open defects, training, data migration status, support setup].

Act as a sceptical go-live assessor. Go through each area and tell me if it's ready, not ready, or unclear. For anything not ready or unclear, tell me what evidence I'd need to be confident.

Finish with a plain recommendation: go, go with conditions, or no-go. Don't be polite about it.
```

---

## 8. Triage after go-live

For the first days of hypercare, when tickets are coming in faster than anyone can read them.

```
Here's a list of incidents raised since go-live: [paste ticket list with titles, descriptions, times, areas].

Group them into themes. For each theme give:
- How many tickets
- Which business process is affected
- Whether it looks like one root cause or several
- How urgent it is for the business, not just for IT

Then give me the top five things to fix first, and which ones can wait. Point out anything that looks like a data or training problem rather than a system bug.
```

When hundreds of tickets come in, the hard part isn't fixing them. It's seeing which ten actually matter.

---

## 9. Lessons learned that people will actually read

```
Here are notes from our lessons learned session on [programme]: [paste notes].

Turn them into no more than five lessons. For each one:
- What happened, in one or two lines
- What we'd do differently
- Who should know about this on the next programme

Leave out anything generic like "communication could be better" unless there's a specific example behind it.
```

---

These save time on the drafting. The real work is still in the room: getting people to agree, calling the red early, deciding what to fix first. That's the bit worth keeping for yourself.

If you've got a prompt you use on programmes that works, send it over. I'll add the good ones here.
