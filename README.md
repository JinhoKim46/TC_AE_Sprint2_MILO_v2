# MILO v2

A RAG diagnosis chatbot for B2B IT-maintenance and office-equipment service businesses (PC, printer, copier and
network maintenance for schools, offices and clinics), built milestone by milestone to learn the stack: LangChain
(`ChatOpenAI` on OpenRouter, `create_agent`), Chroma, Flask.

Status: T0 scaffold. The plan is issue #2; one issue per milestone (T0, M0 to M7). Each milestone has a lesson in
`docs/lessons/`.

## Run

```bash
uv sync
make check          # lint, format check, offline tests (no network, no spend)
make kit-sync       # copy the course project kit's contract tests in (KIT_SRC=<path> if it is elsewhere)
make contract       # run the kit's contract suite against milo.app:build_app
```

Live model calls need `MILO_LIVE=1` and a key in `.env` (see `.env.example`); nothing else spends.

All companies, people and figures in this repository are fictional.

## License

MIT. See [LICENSE](LICENSE).
