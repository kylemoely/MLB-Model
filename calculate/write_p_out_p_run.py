from db.db import engine
from queries import get_new_fieldable_plays
from models.p_out.model import get_model as get_p_out
from models.p_run.model import get_model as get_p_run
from sqlalchemy import text

p_out = get_p_out()
p_run = get_p_run()

def write_p_out_p_run():
    with engine.begin() as conn:
        df = get_new_fieldable_plays(conn)

        df["p_out"] = p_out.predict(df[[col for col in p_out.feature_name()]])
        df["p_run"] = p_run.predict(df[[col for col in p_run.feature_name()]])

        updates = df[["id","p_out","p_run"]]

        updates.to_sql("_fieldable_plays_updates", conn, if_exists="replace", index=False)

        conn.execute(text("""
            INSERT INTO fieldable_plays (id, p_out, p_run)
            SELECT id, p_out, p_run FROM _fieldable_plays_updates
            ON CONFLICT (id) DO UPDATE
            SET p_out = EXCLUDED.p_out,
                p_run = EXCLUDED.p_run;
         """))

        conn.execute(text("DROP TABLE _fieldable_plays_updates"))
