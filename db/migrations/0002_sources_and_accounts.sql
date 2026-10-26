-- Sources are stored with each assistant turn, so citations still work after a reload.
alter table milo_v2.turns add column if not exists sources jsonb not null default '[]'::jsonb;

-- Accounts. Passwords are stored only as salted scrypt hashes. Roles: 'admin' (the owner) and 'customer'.
create table if not exists milo_v2.users (
    id            bigserial   primary key,
    login_id      text        not null unique,
    display_name  text        not null,
    password_hash text        not null,
    role          text        not null check (role in ('admin', 'customer')),
    created_at    timestamptz not null default now()
);
