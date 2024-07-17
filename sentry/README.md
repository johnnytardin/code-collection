# Query para aplicar um rate limit por key

```
UPDATE public.sentry_projectkey SET rate_limit_count=60, rate_limit_window=60
```

```
UPDATE public.sentry_projectkey k 
SET rate_limit_count=10, rate_limit_window=60
from public.sentry_project p
where k.project_id = p.id
and p.name like '%dev%'

UPDATE public.sentry_projectkey k 
SET rate_limit_count=10, rate_limit_window=60
from public.sentry_project p
where k.project_id = p.id
and p.name like '%staging%'

UPDATE public.sentry_projectkey k 
SET rate_limit_count=60, rate_limit_window=60
from public.sentry_project p
where k.project_id = p.id
and name not like '%dev%' and name not like '%staging%'

select k.rate_limit_count, k.rate_limit_window, p.name from sentry_projectkey k  
join sentry_project p on k.project_id = p.id
```

## Gerar a migracao do clickhouse manualmente (recriar/criar tabelas)

docker-compose run --rm snuba-api migrations migrate -g search_issues --force

### migracao das tabelas
docker-compose run --rm web upgrade

