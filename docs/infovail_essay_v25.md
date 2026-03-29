**They were the result, not the cause.**

*What twelve weeks of building a vaccine hesitancy surveillance system
taught me about trust, data, and institutional design*

**I. Hook**

**On the morning of February 23, 2026, I had just pressed submit.**

Not on a paper. On a Kaggle challenge --- the medGemma Impact Challenge
--- where I'd spent weeks designing a system architecture for
pharmacovigilance. The premise of the design was simple: Korea's active
vaccine safety surveillance had a structural gap, and someone needed to
think about what filling it might look like. I was building for the
future. The submission was in. I opened LinkedIn.

The news was already there. South Korea's Board of Audit and Inspection
had just released findings that government officials had procured
COVID-19 vaccines without adequate safety review protocols. Within
hours, comment sections on Naver --- Korea's dominant social media
platform --- were flooding with posts about foreign contaminants,
institutional cover-ups, and betrayed trust.

I kept scrolling. A few posts down: a paper published that same day in
npj Digital Medicine --- local LLMs built for public health
infoveillance, multilingual, fine-tuned for real-time monitoring. I read
the abstract. The pieces were there. A system architect's instinct is to
ask: what could you build with this?

I closed the Kaggle tab. I opened a new Python file.

*What if I tried to analyze the present?*

**II. The Paradox**

Here is a fact about South Korea that tends to surprise people outside
the field.

South Korea compensates vaccine-injured citizens at one of the highest
rates in the world. And then, in October 2025, the government went
further still --- enacting a Special Act on COVID-19 Vaccine Injury
Compensation, expanding eligibility beyond an already expansive system.

And yet, in the weeks following two discrete public events in early
2026, the country's largest social media platform was flooded with
conspiracy-coded language about government cover-ups, suppressed
evidence, and institutional betrayal. The comments weren't fringe. They
were mainstream. They were angry.

Which brought me back to a question I'd been circling for years. I work
for KDCA. That sentence deserves its own line. It was the same question
that had driven the pharmacovigilance design in the first place --- and
now demanded something more immediate: not a system for the future, but
an attempt to understand what was already happening, in real time, on
the platform where the public was doing its own analysis without
institutional guidance.

*How far is South Korea from where it thinks it is on vaccine safety?*

Not geographically. Not even policy-wise. But epistemically --- in the
gap between what the system produces and what the public believes about
what the system produces. The compensation infrastructure had been
built. The numbers were there. But somewhere between the policy and the
public, something had broken.

The paradox isn't a contradiction to be resolved. It is a symptom --- of
a system that had been generating both the compensation numbers and the
distrust through the same structural logic. That architecture is what I
set out to examine. Not with a large institutional team and NIH funding.
With Python, a SQLite database, and the conviction that understanding
the problem mattered more than solving it quickly.

**III. The Build**

The first decision wasn't technical. It was conceptual.

I kept coming back to the 7C model. Geiger and colleagues had extended
Betsch's original 5C framework into something that accommodated a wider
range of hesitancy types, including Conspiracy and Compliance --- two
dimensions I suspected would be central to the Korean discourse I was
seeing. Conspiracy, because the audit news had immediately activated a
pre-existing narrative about institutional cover-up. Compliance, because
a significant segment of Korean vaccine discourse didn't fit the Western
template of hesitancy --- it was people who had complied under social
and institutional pressure, experienced adverse events they believed
were caused by the vaccine, and felt abandoned by the very system that
had asked for their compliance.

I needed a labeled dataset to benchmark the system. CAVES --- COVID
vaccine concern tweets annotated by Poddar and colleagues for SIGIR 2022
--- was the closest available resource. Its taxonomy didn't map directly
to 7C; I had to hand-map each category. That process, like most of the
work, was less about code than about concept. The Naver API collected
data once a week. Claude Code handled the pipeline. What took time ---
what always takes time in any system that has to mean something --- was
understanding the domain well enough to know what the data was actually
saying.

The question was a public health question. That it happened to implicate
the institution I work for was not the reason to ask it --- it was the
reason to be careful about how. The analysis relied entirely on publicly
available data: Naver posts collected through the public API, classified
against an open benchmark dataset. Every analytical decision was
pre-registered before the data spoke. That is what public health
surveillance requires.

Six weeks of data. Two before the event, to establish a baseline. Four
after, to watch what changed. A SQLite database that grew from zero to
8,694 posts, collected while I slept — of which 4,870 met relevance
criteria and entered the analysis. A classification pipeline built
with Claude Code, checked weekly --- guided, not ground out. The machine
ran. I studied CAVES the way an epidemiologist studies VAERS: not as a
dataset, but as a lens. Learning what questions it could and couldn't
answer. Learning where the signal ends and the noise begins.

The point was never the pipeline. It was what the data could be made to
reveal.

There is one thing I would do differently.

I collected data manually, once a week. It seemed sufficient at the
time --- the pipeline was running, the database was growing. What I did
not account for was a structural property of the Naver Search API:
results are capped at 1,000 per query, sorted by recency. By the time
I thought to look back at early February, March had already happened.
The API window had moved on. The posts I needed were still there,
somewhere on Naver's servers --- but the API could no longer reach them.

This is not a technical footnote. It is a design principle that took me
several weeks to learn: infoveillance systems cannot be built
retrospectively. The data exists in the present tense only. Miss a day,
and it is gone --- not deleted, but inaccessible, buried under the
volume of everything that came after. The irony is not lost on me: I
was building a system to study how institutional failures create gaps in
public trust, while quietly creating a gap in my own data.

Daily automated collection. That is the lesson. Not because the
analysis failed --- the core findings held. But because when I do this
again, the baseline will be the first thing I build, not the last thing
I fix.

**IV. What the Data Said**

I had three hypotheses going in.

The audit disclosure would activate Confidence and Conspiracy discourse.
The court ruling coverage would add Compliance --- the voice of people
who had followed the rules, experienced what they believed were vaccine
injuries, and were now watching the legal system weigh their claims
against state interest --- and felt that the outcome was predetermined.
And underneath both events, the Chronic group --- posts about vaccine
injury compensation, side effects, victim communities --- would amplify
whatever the trigger events produced, functioning as a kind of
pre-charged background current.

The condition at the center of that ruling --- myocardial infarction ---
had not been recognized as a risk of COVID-19 vaccination by any major
regulatory or public health authority, a conclusion stable in the
scientific literature for years by the time the court ruled. The ruling
did not assert causation. It asserted only that causation could not be
excluded --- without the scientific basis to make even that claim. KDCA
appealed. The broadcaster reported the appeal as confirmation that
something was being suppressed. By the time the story reached Naver, the
distinction between "cannot be excluded" and "likely caused" had been
lost entirely.

The data confirmed the first two hypotheses. The Chronic group behaved
as expected --- a pre-charged background current, amplifying whatever
the trigger events produced. And then, in the Court group, it showed me
something I hadn't expected.

Conspiracy coding decreased after the trigger event. Not dramatically,
but measurably. I spent two days checking. Nothing was wrong. The
pattern was real. When the SBS broadcast gave people a concrete, named,
legally-adjudicated event to respond to, the discourse specificized. The
conspiracy signal didn't disappear --- it diluted, surrounded by a much
larger volume of specific, event-reactive content. I called it discourse
specificization.

A reminder that surveillance systems that only look forward will
systematically misread what they find downstream.

*Before asking what should be done, a surveillance system has to answer
a prior set of questions: What is this system actually measuring? What
is it structurally blind to? And how long has the signal been there
before anyone thought to look?*

And yet, underneath everything, something was there before either event
began. The C1 signal --- Confidence, or more precisely, the absence of
it --- was already elevated at baseline: 40 to 50 percent of posts
across all three groups before the audit, before the broadcast, before
anyone had a trigger to react to. The events amplified it further ---
dramatically, in some groups --- but they did not create it. It had
been sitting there, like a vital sign that had been abnormal for so
long it no longer registered as a finding. In statistical terms, a
pre-existing elevated baseline. In practical terms, the signal had been
there before the study began. The events didn't generate the distrust.
They revealed its depth.

I had been asking: what do these events do to public trust? But the data
was answering a different question:

*What does it look like when trust has already been gone for a long
time, and a single event can only confirm what people already believed?*

I want to be precise about what the data actually shows. I measured
discourse --- the language people used on a public platform, classified
against a validated framework. The C1 baseline was elevated. The events
amplified it. That is what the data says. What it does not say --- what
no discourse study can say --- is why the baseline was elevated. The
structural argument that follows is mine. It is grounded in the
institutional context, consistent with the pattern, and I believe it is
correct. But it is an interpretation, not a measurement. The data
points. The explanation is my responsibility.

**V. What Infoveillance Can and Cannot See**

This was my first infoveillance study. I want to be honest about what
that means.

I measured discourse --- the language people used on a public platform,
classified against a validated framework. The system told me which
dimensions of vaccine hesitancy were activated, when, and through which
channels. That is what it is designed to do, and within those boundaries,
it worked.

What it cannot do is explain origin. The C1 baseline was elevated before
either trigger event. That is a fact the data supports. Why it was
elevated --- what built that baseline over the years before I started
collecting --- is a question that lives outside the measurement. I can
describe the pattern. I cannot diagnose its cause from the signal alone.

There is a temptation, when you see a pattern this consistent, to reach
for the structural explanation. I have my own. Korea's compensation
paradox --- the highest vaccine injury compensation rate in the world,
and persistent organized distrust --- points toward something
architectural: an agency that simultaneously runs the vaccination
program, adjudicates injury claims, and receives adverse event reports
is not structurally positioned to generate evidence the public will
trust. That argument is consistent with the data. But it is mine, not
the data's.

What the data does say --- plainly, and I think importantly --- is this:
the distrust was not created by the events of February and March 2026.
It was revealed by them. The politicians and the headlines did not build
it. They found it waiting.

**They were the result, not the cause.**

**VI. What This Tool Can Do Next**

Here is what I find genuinely interesting about the method.

If the architecture changes --- if KDCA's surveillance and compensation
functions are separated, if independent review pathways are created ---
the discourse will change too. Or it won't. Either way, infoveillance
can see it. The C1 baseline, tracked continuously, becomes a leading
indicator of whether structural reform is actually reaching public
perception. Japan reinstated its HPV vaccination recommendation in 2022,
nearly a decade after suspending it. What happened to the discourse
afterward? That is a measurable question. So is the Korean equivalent,
if and when the moment comes.

I cannot tell you whether the distrust is justified, or what originally
built it. What I can tell you is this: if the architecture changes, the
discourse will change too. And if it doesn't, the signal will still be
there --- measurable, trackable, impossible to ignore. That is what
infoveillance is for. Not to answer the question of origin. But to hold
the system accountable to its own trajectory.

The study I wanted to do when I opened that Python file in February was
simpler than the one I ended up with. I wanted to measure a reaction.
What I found instead was a baseline --- and the baseline turned out to
be the finding.

**VII. Close**

Korea in early 2026 was, in some ways, an ideal natural experiment. A
high-compensation system, a well-documented institutional failure, two
discrete trigger events, and a platform where millions of people
processed it all in public, in real time. I didn't design the
experiment. I just built a system to listen to it.

What the system heard was this: the events mattered less than the
baseline. The trigger events didn't create the distrust --- they
revealed it. The classification framework didn't judge the discourse ---
it mapped it. And the map, it turned out, had more to say about
institutional architecture than about public irrationality.

*The analysis presented here did not generate new recommendations. It
generated something prior to recommendation: a structural diagnosis,
rendered in the present tense, of a system that had been producing
distrust long before anyone thought to measure it.*

Sentiment analysis can tell you that people are angry. Infoveillance
asks why --- which dimension of hesitancy is activated, by which event,
through which channel. That classification is what enables root cause
analysis. And root cause analysis is what enables intervention that
actually addresses the problem, rather than the symptom.
