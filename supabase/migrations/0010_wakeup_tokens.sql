-- Prompt caching is the largest single lever on this company's costs, and
-- until now the numbers that prove whether it is working were buried in a
-- text summary. A check-in whose cacheable prefix falls below the model's
-- minimum caches NOTHING and says nothing about it: cache_read stays 0 and
-- there is no error. Store the counts so the question is answerable with a
-- query instead of an argument.
alter table wakeups add column if not exists input_tokens bigint;
alter table wakeups add column if not exists output_tokens bigint;
alter table wakeups add column if not exists cache_read_tokens bigint;
alter table wakeups add column if not exists cache_write_tokens bigint;
