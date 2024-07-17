from postgres import Postgres
from decouple import config


DB_USER = config("DB_USER", "test")
DB_PASSWD = config("DB_PASSWD", "test")
DB_NAME = config("DB_NAME", "test")
DB_HOST = config("DB_HOST", "postgres")
DB_PORT = config("DB_PORT", 5432)


db = Postgres(f"postgres://{DB_USER}:{DB_PASSWD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
rate_config = {
    "dev": {"rate_limit_count": 10, "rate_limit_window": 60},
    "staging": {"rate_limit_count": 10, "rate_limit_window": 60},
    "default:rate-limit": {"rate_limit_count": 60, "rate_limit_window": 60},
}


def get_project_environment(name):
    project_env = None
    for environment in rate_config.keys():
        if environment in name:
            project_env = environment
    return project_env if project_env else "default:rate-limit"


def set_rate_limit():
    projectkeys = db.all(
        "select k.id, p.name from sentry_projectkey k join sentry_project p on k.project_id = p.id"
    )
    for key in projectkeys:
        name = key.name
        id = key.id
        limits = rate_config.get(get_project_environment(name))

        rate_limit_count = limits.get("rate_limit_count")
        rate_limit_window = limits.get("rate_limit_window")

        print(
            f"Updating key {id} for project {name} to rate_limit_count={rate_limit_count} and rate_limit_window={rate_limit_window}"
        )

        query = "UPDATE public.sentry_projectkey k SET rate_limit_count=%(rate_limit_count)s, rate_limit_window=%(rate_limit_window)s from public.sentry_project where k.id = %(id)s"
        db.run(
            query,
            rate_limit_count=rate_limit_count,
            rate_limit_window=rate_limit_window,
            id=id,
        )


if __name__ == "__main__":
    set_rate_limit()
