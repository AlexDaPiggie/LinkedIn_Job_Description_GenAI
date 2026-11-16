-- Credit ledger, idempotent Stripe events and one-time free grants.
-- Run once in the Supabase SQL editor. Safe to re-run.
-- Existing balances in profiles.credits are NOT changed.

create table if not exists public.credit_ledger (
    id bigserial primary key,
    user_id uuid not null,
    delta integer not null,
    reason text not null,
    idempotency_key text not null unique,
    created_at timestamptz not null default now()
);
create index if not exists credit_ledger_user_idx on public.credit_ledger (user_id, created_at desc);

create table if not exists public.stripe_events (
    event_id text primary key,
    created_at timestamptz not null default now()
);

-- One free grant per normalized email (Gmail dots and +tags removed).
create table if not exists public.free_grants (
    email_normalized text primary key,
    user_id uuid not null,
    created_at timestamptz not null default now()
);

-- Click events used to learn which refine chips people use (no personal data).
create table if not exists public.usage_events (
    id bigserial primary key,
    event text not null,
    detail text,
    created_at timestamptz not null default now()
);

-- Server code uses the service role key, so lock these tables for everyone else.
alter table public.credit_ledger enable row level security;
alter table public.stripe_events enable row level security;
alter table public.free_grants enable row level security;
alter table public.usage_events enable row level security;

-- Spend credits atomically. Returns the new balance, or -1 if not enough credits.
-- Calling again with the same key does nothing and returns the current balance.
create or replace function public.spend_credits(p_user uuid, p_cost integer, p_key text)
returns integer language plpgsql security definer as $$
declare new_balance integer;
begin
    if exists (select 1 from public.credit_ledger where idempotency_key = p_key) then
        select credits into new_balance from public.profiles where id = p_user;
        return coalesce(new_balance, -1);
    end if;
    update public.profiles set credits = credits - p_cost
        where id = p_user and credits >= p_cost
        returning credits into new_balance;
    if new_balance is null then
        return -1;
    end if;
    insert into public.credit_ledger (user_id, delta, reason, idempotency_key)
        values (p_user, -p_cost, 'spend', p_key);
    return new_balance;
end $$;

-- Give back a spend (failed refine). Only works once per original key.
create or replace function public.refund_credits(p_user uuid, p_amount integer, p_key text)
returns integer language plpgsql security definer as $$
declare new_balance integer;
begin
    if not exists (select 1 from public.credit_ledger where idempotency_key = p_key and user_id = p_user) then
        select credits into new_balance from public.profiles where id = p_user;
        return coalesce(new_balance, 0);
    end if;
    begin
        insert into public.credit_ledger (user_id, delta, reason, idempotency_key)
            values (p_user, p_amount, 'refund', 'refund:' || p_key);
    exception when unique_violation then
        select credits into new_balance from public.profiles where id = p_user;
        return coalesce(new_balance, 0);
    end;
    update public.profiles set credits = credits + p_amount where id = p_user
        returning credits into new_balance;
    return coalesce(new_balance, 0);
end $$;

-- Add credits once per key (Stripe purchases). Returns the new balance.
create or replace function public.grant_credits(p_user uuid, p_amount integer, p_key text, p_reason text)
returns integer language plpgsql security definer as $$
declare new_balance integer;
begin
    begin
        insert into public.credit_ledger (user_id, delta, reason, idempotency_key)
            values (p_user, p_amount, p_reason, p_key);
    exception when unique_violation then
        select credits into new_balance from public.profiles where id = p_user;
        return coalesce(new_balance, 0);
    end;
    update public.profiles set credits = credits + p_amount where id = p_user
        returning credits into new_balance;
    return coalesce(new_balance, 0);
end $$;

-- Record a Stripe event id. Returns true the first time, false for duplicates.
create or replace function public.claim_stripe_event(p_event_id text)
returns boolean language plpgsql security definer as $$
begin
    insert into public.stripe_events (event_id) values (p_event_id);
    return true;
exception when unique_violation then
    return false;
end $$;

-- Give the one-time signup grant. Returns the granted amount (0 if this email already got one).
create or replace function public.claim_free_grant(p_user uuid, p_email_normalized text, p_amount integer)
returns integer language plpgsql security definer as $$
begin
    begin
        insert into public.free_grants (email_normalized, user_id) values (p_email_normalized, p_user);
    exception when unique_violation then
        return 0;
    end;
    perform public.grant_credits(p_user, p_amount, 'free_grant:' || p_user::text, 'free_grant');
    return p_amount;
end $$;

-- New profiles start with 0 credits; the free grant is given after email confirmation.
alter table public.profiles alter column credits set default 0;

revoke all on function public.spend_credits(uuid, integer, text) from public, anon, authenticated;
revoke all on function public.refund_credits(uuid, integer, text) from public, anon, authenticated;
revoke all on function public.grant_credits(uuid, integer, text, text) from public, anon, authenticated;
revoke all on function public.claim_stripe_event(text) from public, anon, authenticated;
revoke all on function public.claim_free_grant(uuid, text, integer) from public, anon, authenticated;
