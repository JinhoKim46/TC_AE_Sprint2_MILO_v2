-- The tool calls of each answer are kept with its turn, so a reloaded conversation shows the same steps as the live one.
alter table milo_v2.turns add column if not exists tools jsonb not null default '[]'::jsonb;
