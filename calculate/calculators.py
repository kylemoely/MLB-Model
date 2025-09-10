def calculate_OPS(df):
    at_bats = df["is_at_bat"].sum()
    walks = df["is_walk"].sum()
    sacs = df["is_sac"].sum()
    hits = df["is_hit"].sum()
    bases = df["bases"].sum()

    if at_bats + walks + sacs == 0:
        return None
    obp = (hits + walks) / (at_bats + walks + sacs)
    if at_bats==0:
        return obp
    slg = bases / at_bats

    return obp + slg

def calculate_AVG(df):
    hits = df["is_hit"].sum()
    at_bats = df["is_at_bat"].sum()

    if at_bats==0:
        return None

    return hits / at_bats

def calculate_ERA(df):
    earned_runs = df["earned_runs"].sum()
    outs = df["outs"].sum()
    innings = outs / 3

    if innings == 0:
        if earned_runs > 0:
            return float("inf")
        else:
            return None
        
    return (earned_runs * 9) / innings

def calculate_WHIP(df):
    outs = df["outs"].sum()
    hits = df["hits_allowed"].sum()
    walks = df["walks_allowed"].sum()
    innings = outs / 3

    if innings == 0:
        if hits + walks > 0:
            return float('inf')
        else:
            return None

    return (hits + walks) / innings