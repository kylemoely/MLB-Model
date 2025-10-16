from db.db import engine
from calculate.queries import get_new_fieldable_plays
from models.p_out.model import get_model as get_p_out
from models.p_run.model import get_model as get_p_run
from sqlalchemy import text


def write_p_out_p_run():
    p_out = get_p_out()
    p_run = get_p_run()

    with engine.begin() as conn:
        df = get_new_fieldable_plays(conn)

        df["p_out"] = p_out.predict(df[[col for col in p_out.feature_name()]])
        df["p_run"] = p_run.predict(df[[col for col in p_run.feature_name()]])

        updates = df[["id","p_out","p_run"]]

        updates.to_sql("_fieldable_plays_updates", conn, if_exists="replace", index=False)

        conn.execute(text("""
            UPDATE fieldable_plays AS f
            SET
                p_out = COALESCE(u.p_out, f.p_out),
                p_run = COALESCE(u.p_run, f.p_run)
            FROM _fieldable_plays_updates AS u
            WHERE u.id = f.id
              AND (
                    (u.p_out IS NOT NULL  AND u.p_out IS DISTINCT FROM f.p_out)
                 OR (u.p_run IS NOT NULL  AND u.p_run IS DISTINCT FROM f.p_run)
              );
        """))

        conn.execute(text("DROP TABLE _fieldable_plays_updates"))
