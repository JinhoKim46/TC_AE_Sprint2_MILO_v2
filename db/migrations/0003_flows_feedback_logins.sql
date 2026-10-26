-- Every question's flow (steps, timings, tokens, cost, errors) is stored per account, so the overview can follow the account.
create table if not exists milo_v2.flows (
    id          bigserial   primary key,
    owner_id    text        not null,
    thread_id   text        not null,
    created_at  timestamptz not null default now(),
    total_ms    double precision not null default 0,
    cost_usd    double precision not null default 0,
    error       text,
    steps       jsonb       not null default '[]'::jsonb,
    question_chars integer  not null default 0
);
create index if not exists flows_owner_idx on milo_v2.flows (owner_id, id);

-- Thumbs votes: rating and a reason from a fixed list. No text.
create table if not exists milo_v2.feedback (
    id          bigserial   primary key,
    owner_id    text        not null,
    rating      text        not null check (rating in ('up', 'down')),
    reason      text        not null default '',
    created_at  timestamptz not null default now()
);

-- When each account last signed in.
alter table milo_v2.users add column if not exists last_login_at timestamptz;
