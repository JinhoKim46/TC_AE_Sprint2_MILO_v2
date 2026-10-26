# Design references for the MILO front end

36 pages, each opened with a web fetch during the research (2026-10-26). Each line gives the source, what it shows, and the pattern adopted or considered for MILO. Generic W3C accessibility pages are included as-is; none of the sources are chat-specific W3C guidance.

## Chat interfaces: sources, explanations, confidence, feedback (18)

1. NN/g, AI hallucinations: what designers need to know, https://www.nngroup.com/articles/ai-hallucinations/ — show source lists with counts and mark unsupported claims. Adopted: sources per answer; "not enough information" when nothing is retrieved.
2. Google PAIR, Explainability and trust, https://pair.withgoogle.com/chapter/explainability-trust/ — categorical confidence tied to an action. Adopted: High / Partial / Weak match wording.
3. Google PAIR, Mental models, https://pair.withgoogle.com/chapter/mental-models/ — state capabilities early, hide detail behind progressive disclosure. Adopted: "How MILO works" sidebar and starter questions.
4. Google PAIR, Errors and graceful failure, https://pair.withgoogle.com/chapter/errors-failing/ — give a path forward when output is weak. Adopted: "not enough information" state with next steps.
5. Google PAIR, Feedback and control, https://pair.withgoogle.com/chapter/feedback-controls/ — mutually exclusive feedback options. Considered: thumbs with reason chips (not built yet).
6. Microsoft HAX, Guideline 11: make clear why the system did what it did, https://www.microsoft.com/en-us/haxtoolkit/guideline/make-clear-why-the-system-did-what-it-did/ — local explanation per answer, global explanation on a separate page. Adopted: "How this answer was made" and the sidebar page.
7. Microsoft HAX, Guideline 2: make clear how well the system can do what it can do, https://www.microsoft.com/en-us/haxtoolkit/guideline/make-clear-how-well-the-system-can-do-what-it-can-do/ — match hedging words to confidence. Adopted: wording tied to the confidence level.
8. Microsoft HAX, Guideline 1: make clear what the system can do, https://www.microsoft.com/en-us/haxtoolkit/guideline/make-clear-what-the-system-can-do/ — intro blurb and example inputs. Adopted: starter questions from the fictional data.
9. Microsoft HAX, Guideline 9: support efficient correction, https://www.microsoft.com/en-us/haxtoolkit/guideline/support-efficient-correction/ — edit a chip and re-run. Considered, not built.
10. NN/g, Prompt controls in GenAI chatbots, https://www.nngroup.com/articles/prompt-controls-genai/ — follow-up chips under answers. Adopted: follow-up chips.
11. NN/g, AI: first new UI paradigm in 60 years, https://www.nngroup.com/articles/ai-paradigm/ — structured result cards beside chat text. Adopted: the answer card with stages, sources and steps.
12. NN/g, Progressive disclosure, https://www.nngroup.com/articles/progressive-disclosure/ — at most two levels. Adopted: a chip, then one expandable panel.
13. Anthropic, Citations, https://platform.claude.com/docs/en/build-with-claude/citations — passage-level citation records. Considered: numbered markers that open the quoted passage.
14. OpenAI, Web search tool, https://developers.openai.com/api/docs/guides/tools-web-search — clearly visible, clickable citations. Considered for the sources list.
15. Perplexity, Search API guide, https://docs.perplexity.ai/guides/search-guide — show retrieved results before the answer. Adopted: the "Found passages" stage.
16. W3C ARIA APG, Disclosure pattern, https://www.w3.org/WAI/ARIA/apg/patterns/disclosure/ — accessible show/hide controls. Adopted: native details element for technical details.
17. W3C WCAG 2.2, Status messages (4.1.3), https://www.w3.org/WAI/WCAG22/Understanding/status-messages.html — announce progress without moving focus. Adopted: the progress line uses role status.
18. W3C ARIA APG, Alert pattern, https://www.w3.org/WAI/ARIA/apg/patterns/alert/ — alerts only for failures. Adopted: errors are announced as alerts; progress stays polite.

## Monitoring and status dashboards (18)

19. Google SRE book, Monitoring distributed systems, https://sre.google/sre-book/monitoring-distributed-systems/ — the four golden signals. Considered for the status card.
20. Google SRE book, Practical alerting, https://sre.google/sre-book/practical-alerting/ — black-box probes next to internal counters. Considered: a live probe of the database and model.
21. NN/g, Dashboards: making charts easier to understand, https://www.nngroup.com/articles/dashboards-preattentive/ — bars for quantities, colour reserved for status. Adopted: the spend bar.
22. Grafana, Dashboard best practices, https://grafana.com/docs/grafana/latest/dashboards/build-dashboards/best-practices/ — one question per dashboard. Adopted: the status card separate from the flow view.
23. Grafana, Stat visualization, https://grafana.com/docs/grafana/latest/panels-visualizations/visualizations/stat/ — big-number tiles with thresholds. Considered for the counts.
24. Grafana, Bar gauge, https://grafana.com/docs/grafana/latest/panels-visualizations/visualizations/bar-gauge/ — bar against a limit with thresholds. Adopted: spend against the course cap.
25. Grafana, State timeline, https://grafana.com/docs/grafana/latest/panels-visualizations/visualizations/state-timeline/ — rows of state over time. Considered for database and model health over time.
26. Wikipedia, Sparkline, https://en.wikipedia.org/wiki/Sparkline — small inline trend lines. Considered beside cost figures.
27. Atlassian Statuspage, https://www.atlassian.com/software/statuspage — components and uptime strips. Considered for the three components.
28. Datadog, Service level objectives, https://docs.datadoghq.com/service_management/service_level_objectives/ — burn rate against a budget. Considered for the spend cap.
29. GOV.UK Design System, Summary list, https://design-system.service.gov.uk/components/summary-list/ — key and value rows. Adopted: the status card layout.
30. GOV.UK Design System, Tag, https://design-system.service.gov.uk/components/tag/ — status labels with text, not colour alone. Adopted: status labels carry words.
31. Langfuse, Token and cost tracking, https://langfuse.com/docs/observability/features/token-and-cost-tracking — cost per request by model and day. Considered for the spend breakdown.
32. Langfuse, Observability overview, https://langfuse.com/docs/observability/overview — a trace of nested steps with timing. Adopted: the per-answer timeline.
33. LangSmith, Dashboards, https://docs.langchain.com/langsmith/dashboards — a fixed row of trace counts, latency, errors and cost. Considered for the overview row.
34. Arize Phoenix, LLM traces, https://arize.com/docs/phoenix/tracing/llm-traces — a waterfall of pipeline steps. Considered for the flow view.
35. Helicone, Custom properties, https://docs.helicone.ai/features/advanced-usage/custom-properties — tags for filtering cost by feature. Considered for the trace list.
36. OpenRouter, API limits and credits, https://openrouter.ai/docs/api-reference/limits — a provider-side key limit. Considered: read the remaining limit alongside the local counter.
