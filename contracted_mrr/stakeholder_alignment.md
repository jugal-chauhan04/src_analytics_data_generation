# Contracted MRR Stakeholder Alignment  

*This case demonstrates how clear stakeholder communication and precise metric definition are the foundation of every good data model*  

## SRC Analytics - Metric Definition Phase    

### Preface  

This project is built around a synthetic SaaS billing dataset hosted in BigQuery, designed to simulate the data environment of a growing subscription-based company. The fictional organization, SRC Analytics, serves as a sandbox for practicing how analysts build scalable, accurate, and reliable data pipelines as data volume and business complexity increase.

Most analytics portfolios focus on queries and dashboards. This one focuses on what happens before that - *the conversations, clarifications, and agreements that define how a metric should exist in the first place.*

The first use case centers on defining **Contracted Monthly Recurring Revenue (Contracted MRR)** a key financial metric that reflects predictable revenue commitments from active subscriptions. The scenario begins with a request from the company’s CFO, sparking a back-and-forth alignment process to clarify definitions, assumptions, and data limitations before any SQL is written. And after reviewing data capture process of the organization, it becomes clear that the business case aligns better with **Committed Monthly Recurring Revenue** instead, the process of realignment - from initial stakeholder request to refined metric definition - is captured below in this article.

The goal is simple but essential: demonstrate how the analytical process behind metric design: confirming definitions, documenting logic, ensuring reproducibility, and communicating with business stakeholders before a single query runs.

By simulating this workflow, the project highlights not only technical skills in dbt, SQL, and BI development, but also the business fluency and process discipline that define strong analysts.  

### Contracted MRR Request  

Let's assume a scenario, we get following request from SRC Analytics CFO:  

> CFO Request (Stakeholder Prompt)
> From: CFO, SRC Analytics
> Subject: MRR for Board Deck
>
> Hi Jugal,
>
> I need your help pulling together our MRR numbers for the upcoming board meeting. Specifically:
>
> - Show contracted MRR for the current month and the prior month.  
> - Break down any changes so I can explain whether they came from new customers, expansions, or churn.
> - Keep it clean. I want a single number for contracted MRR, but I also need the bridge that explains why it moved month over month.
>  
> This will be going in the board deck next week, so accuracy matters more than speed. Let me know if you need me to clarify the definition of “contracted” we use here.
>
> Thanks,
> CFO, SRC Analytics  

### Analyst Perspective  

At first glance, this looks like a straightforward reporting request but it’s actually a test of **analytical judgment**. Before pulling any data, an analyst must ensure the metric definition is fully aligned with the business context.  

This begins with **requirements gathering** and asking targeted questions that uncover how the organization defines and tracks “contracted” revenue. The objective isn’t just to find the number, but to clarify what *that number means.*

An analyst must also assess whether the request is an **ad-hoc analysis** or a **recurring business metric** that will influence long-term strategy. The decision depends on both the **urgency of the request** and the **organization’s growth stage**. Quick insights matter, but opportunities for *scalable analysis* should never be ignored. Based on this assessment, the analyst defines scope: does the metric warrant a dedicated data model with validation, testing, and transformation steps, or can it be handled as a one-off report?

Considering the CFO’s request, the next step is to open a dialogue not to code yet, but to align.  

### Analyst Response (Clarification & Alignment)

> From: Jugal Chauhan, Data Analyst
> Subject: Clarifying Contracted MRR Definition and Proposal for Monthly Dashboard
>
> Hi SRC Analytics CFO,
>
> Before I finalize the contracted MRR report for this month and the previous one, I’d like to confirm a few details to ensure the calculations align fully with Finance’s definitions and expectations.
> 
> 1. Definition of Contracted MRR:  
> - Should discounted subscriptions be included at their discounted value?  
> - For annual contracts, should they be normalized to a monthly equivalent?
> - Should mid-cycle changes be prorated, or should I use the full monthly amount as of the reporting date?
>
> 2. Data Capture Limitation
> Our current data source records subscriptions only once the first invoice is generated. Contracts that haven’t yet started billing aren’t captured. Given this, I plan to include only non-expired, active subscriptions in the contracted MRR calculation.
> 
> 3. Within-Month Changes
> To reflect accurate activity during the month, I’ll handle changes as follows:  
> - Expired subscriptions: exclude  
> - Upgrades/downgrades: include with updated MRR value  
> - Active unchanged subscriptions: include at current MRR
>
> 4. Month-to-Month Movement Tracking
> In addition to MRR totals, I’ll generate separate views for:  
> - Churned MRR (revenue lost from cancellations)  
> - Expansion MRR (revenue gained from plan upgrades)  
> - Downgrade MRR (revenue lost with plan downgrade)  
> - New MRR (revenue generated by new subscriptions)
> - Reactivating MRR (MRR from returning user) - however this present data limitations as current dataset doesn't capture it and will require collaboration of data engineering team. 
> - Plan performance overview (plans driving the most MRR changes)  
> - Discounts or offers impacting contracted MRR  
> - Seasonality or external factors if visible in the data
>
> 5. Dashboard Proposal
> Since month-over-month comparison of contracted MRR is a recurring topic during board meetings, would you like me to create an interactive dashboard that updates automatically each month?
> 
> Once definitions are confirmed, I’ll document the agreed logic and reflect it in dbt for consistency.
>
> Best regards,
> Jugal Chauhan
> Data Analyst, SRC Analytics  
>  

### Why this matters  

This communication shows how an analyst transforms a vague business request into a structured, verifiable plan. It demonstrates several critical behaviors that separate effective analysts from reactive ones:

1. Breaking the request into clear components that clarify the metric logic.  
2. Flagging data limitations early, avoiding downstream surprises.  
3. Handling edge cases upfront and transparently.  
4. Introducing scalable solutions (dashboard, standardized model) instead of short-term fixes.  
5. Pivoting the final definition decision to the CFO ensuring accountability and alignment.  

The next email finalizes this alignment, turning a discussion into a formal agreement.

### CFO Confirmation (Final Definition Agreement)  

> From: CFO, SRC Analytics
> Subject: Re: Clarifying Contracted MRR Definition and Next Steps
>
> Hi Jugal,
> 
> Appreciate the thoroughness here. Let’s lock in a few points:
> 
> 1. Discounted subscriptions: Report them at the discounted value.  
> 2. Annual contracts: Normalize to monthly equivalent.  
> 3. Mid-cycle changes: Use the contracted value as of the month-end snapshot (no proration).  
> 4. Exclude contracts that haven’t started billing yet. If you think that significantly impacts totals, flag it and we’ll involve Sales Ops.  
> 
> For the monthly movement breakdown, include new, expansion, downgrade, churn, and reactivation/returning MRR as separate categories. If reactivation data isn’t currently tracked, coordinate with the engineering team to assess whether it can be added in future iterations. 
> 
> Also, prepare a metric definition document for Contracted MRR in the Finance Metric Glossary and review it with me and [Senior Analyst’s Name] before finalizing. This should be completed before implementing any data model or dashboard work.
> 
> I like the idea of a recurring dashboard. Build it off the standardized metric.  
> 
> Best,
> CFO, SRC Analytics  
>  

### Metric Realignemnt  

After finalizing the definition with the CFO, I revisited how SRC Analytics actually captures data in the warehouse. During that review, I realized that the synthetic data generation function only records subscriptions after their first invoice is generated, meaning we don’t have visibility into contracts that have been signed but haven’t started billing yet.

Because of this, the metric I initially labeled as Contracted MRR doesn’t fully align with our data reality. To maintain clarity and accuracy, I have to follow up with the CFO to realign the terminology. What we’re truly measuring is Committed MRR - a recurring revenue from active, billing subscriptions and not future contracted deals that haven’t yet gone live.

This clarification demonstrates how definitions evolve as analysts better understand the systems behind their metrics, ensuring that business logic and data logic stay perfectly in sync.  

> Subject: MRR Definition Update — Contracted vs. Committed
> 
> Hi [CFO’s Name],
>
> After reviewing how our data is captured in the warehouse, I realized our pipeline only records subscriptions once billing begins. Since we don’t capture pre-billing contracts, the metric we’ve been calling Contracted MRR more accurately reflects active, billing subscriptions.
> 
> To stay consistent with what our data represents, I recommend renaming it to Committed MRR. The calculation logic remains the same, it still measures predictable recurring revenue but the new name aligns better with our system’s scope.
> 
> If we later include pre-billing data from Sales Ops or a CRM, we can reintroduce Contracted MRR as a distinct forward-looking metric. I’ll update the metric glossary to reflect this clarification.
> 
> Best,
> Jugal Chauhan
> Data Analyst, SRC Analytics  

### The Analyst's Next Step  

Following this confirmation, the analyst’s task is to formalize the agreement into a data dictionary effectively, a contract that the entire organization can reference. The document should capture:

- **Metric definition**  
- **Calculation logic**  
- **Data sources and required fields**  
- **Known limitations or assumptions**

All written in plain, accessible language so business and technical teams share a single understanding. Once drafted, it’s reviewed with the stakeholders involved (Senior Analyst, CFO etc). This becomes the **single source of truth** for Contracted MRR, forming the foundation for the dbt model and any downstream dashboards. Maintaining this documentation whether in **dbt docs**, **Confluence**, or an internal finance glossary that ensures transparency, trust, and long-term consistency.  

### Reflection & Key Takeaway  

Misalignment on metric meaning causes more confusion than bad queries ever will. By pausing to clarify, document, and communicate, analysts transform from data providers into trusted business partners. Like in this example, initially the focus was to define Contracted MRR and after reviewing the data capture process it was decided that Committed MRR aligns better with what the goal of business case is. The process isn’t just to deliver numbers but it’s to make sure everyone believes in what those numbers represent. 

This project is a simplified demonstration of how stakeholder alignment fits into the analytical cycle, the phase where definitions are clarified and expectations are set before any data work begins. In larger organizations, this process often involves multiple stakeholders across Finance, Sales, Product, and Engineering, each shaping how a metric is defined and maintained.  

 

