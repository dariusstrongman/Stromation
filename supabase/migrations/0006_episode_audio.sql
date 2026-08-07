-- Episodes get a voice: a public bucket for narration mp3s.
alter table narrations add column if not exists audio_url text;

insert into storage.buckets (id, name, public)
values ('episodes', 'episodes', true)
on conflict (id) do update set public = true;

drop policy if exists "episodes are public" on storage.objects;
create policy "episodes are public" on storage.objects
  for select using (bucket_id = 'episodes');
