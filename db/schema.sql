CREATE TABLE IF NOT EXISTS plate_appearances(
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    batter_id BIGINT,
    pitcher_id BIGINT,
    inning INTEGER,
    event_type VARCHAR(255),
    is_at_bat BOOLEAN,
    is_walk BOOLEAN,
    is_sac BOOLEAN,
    is_hit BOOLEAN,
    bases INTEGER,
    gamepk BIGINT,
    FOREIGN KEY gamepk REFERENCES game_catalog(gamepk)
);

CREATE TABLE IF NOT EXISTS pitcher_innings(
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    pitcher_id BIGINT,
    inning INTEGER,
    hits_allowed INTEGER,
    walks_allowed INTEGER,
    earned_runs INTEGER,
    outs INTEGER,
    gamepk BIGINT,
    FOREIGN KEY gamepk REFERENCES game_catalog(gamepk)
);

CREATE TYPE status_enum AS ENUM ('NEW', 'PROCESSED', 'FAILED');

CREATE TABLE IF NOT EXISTS game_catalog(
    gamepk BIGINT PRIMARY KEY,
    game_date DATE,
    status status_enum NOT NULL DEFAULT 'NEW',
    tries INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS game_features(
    gamepk BIGINT PRIMARY KEY REFERENCES game_catalog(gamepk),
    away_pitcher_era DOUBLE PRECISION,
    away_pitcher_whip DOUBLE PRECISION,
    home_pitcher_era DOUBLE PRECISION,
    home_pitcher_whip DOUBLE PRECISION,
    away_batter1_ops DOUBLE PRECISION,
    away_batter1_avg DOUBLE PRECISION,
    away_batter2_ops DOUBLE PRECISION,
    away_batter2_avg DOUBLE PRECISION,
    away_batter3_ops DOUBLE PRECISION,
    away_batter3_avg DOUBLE PRECISION,
    away_batter4_ops DOUBLE PRECISION,
    away_batter4_avg DOUBLE PRECISION,
    away_batter5_ops DOUBLE PRECISION,
    away_batter5_avg DOUBLE PRECISION,
    home_batter1_ops DOUBLE PRECISION,
    home_batter1_avg DOUBLE PRECISION,
    home_batter2_ops DOUBLE PRECISION,
    home_batter2_avg DOUBLE PRECISION,
    home_batter3_ops DOUBLE PRECISION,
    home_batter3_avg DOUBLE PRECISION,
    home_batter4_ops DOUBLE PRECISION,
    home_batter4_avg DOUBLE PRECISION,
    home_batter5_ops DOUBLE PRECISION,
    home_batter5_avg DOUBLE PRECISION
);

CREATE TABLE IF NOT EXISTS game_labels(
    gamepk BIGINT PRIMARY KEY REFERENCES game_catalog(gamepk),
    label BOOLEAN
);

CREATE TYPE outs_enum AS ENUM ('0','1','2');

CREATE TABLE IF NOT EXISTS fieldable_plays(
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    gamepk BIGINT,
    launch_speed DOUBLE PRECISION,
    launch_angle DOUBLE PRECISION,
    total_distance DOUBLE PRECISION,
    trajectory VARCHAR(255),
    hardness VARCHAR(255),
    hit_location INTEGER,
    coord_x DOUBLE PRECISION,
    coord_y DOUBLE PRECISION,
    fielder INTEGER,
    fielder_id BIGINT,
    putouter INTEGER,
    putouter_id BIGINT,
    errer INTEGER,
    errer_id BIGINT,
    made_out BOOLEAN,
    pickoff_out BOOLEAN,
    has_out BOOLEAN,
    has_score BOOLEAN,
    first_base_runner BOOLEAN,
    second_base_runner BOOLEAN,
    third_base_runner BOOLEAN,
    num_outs outs_enum,
    FOREIGN KEY gamepk REFERENCES game_catalog(gamepk)
)