def fill_hit_data_na(df, ref_df):
    angle_means = ref_df.groupby("trajectory")["launch_angle"].mean()
    speed_means = ref_df.groupby("hardness")["launch_speed"].mean()
    distance_means = ref_df.groupby("location")["total_distance"].mean()

    df.loc[df["launch_angle"].isna(), "launch_angle"] = df.loc[df["launch_angle"].isna(), "trajectory"].map(angle_means)
    df.loc[df["launch_speed"].isna(), "launch_speed"] = df.loc[df["launch_speed"].isna(), "hardness"].map(speed_means)
    df.loc[df["total_distance"].isna(), "total_distance"] = df.loc[df["total_distance"].isna(), "location"].map(distance_means)

    return df