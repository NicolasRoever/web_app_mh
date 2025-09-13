create table if not exists app_user (
  user_id text primary key,
  created_at timestamptz default now()
);

create table if not exists session_login (
  id bigserial primary key,
  user_id text references app_user(user_id) on delete cascade,
  first_login_at timestamptz not null default now()
);

create table if not exists visit (
  id bigserial primary key,
  user_id text references app_user(user_id) on delete cascade,
  started_at timestamptz not null default now(),
  ended_at timestamptz,
  duration_seconds integer
);

create index if not exists visit_user_started_idx on visit (user_id, started_at);
