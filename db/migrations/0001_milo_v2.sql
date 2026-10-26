-- MILO v2: conversation, facts and diagnoses. Own schema, so nothing touches other projects in the same database.
create schema if not exists milo_v2;

create table if not exists milo_v2.threads (
    owner_id    text        not null,
    thread_id   text        not null,
    created_at  timestamptz not null default now(),
    primary key (owner_id, thread_id)
);

create table if not exists milo_v2.turns (
    id          bigserial   primary key,
    owner_id    text        not null,
    thread_id   text        not null,
    role        text        not null check (role in ('user', 'assistant')),
    content     text        not null,
    created_at  timestamptz not null default now(),
    foreign key (owner_id, thread_id) references milo_v2.threads (owner_id, thread_id) on delete cascade
);
create index if not exists turns_thread_idx on milo_v2.turns (owner_id, thread_id, id);

create table if not exists milo_v2.facts (
    id            bigserial   primary key,
    owner_id      text        not null,
    field_id      text        not null,
    value         jsonb       not null,
    unit          text,
    status        text        not null check (status in ('reported', 'conflicting', 'unknown')),
    evidence_text text        not null,
    created_at    timestamptz not null default now()
);
create index if not exists facts_owner_idx on milo_v2.facts (owner_id, field_id);

create table if not exists milo_v2.diagnoses (
    id          bigserial   primary key,
    owner_id    text        not null,
    area_id     text        not null,
    card        jsonb       not null,
    created_at  timestamptz not null default now()
);
create index if not exists diagnoses_owner_idx on milo_v2.diagnoses (owner_id);
