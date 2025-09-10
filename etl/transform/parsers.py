def parse_plays(plays):
    results = []

    num_bases = {
        "1B": 1,
        "2B": 2,
        "3B": 3,
        "4B": 4,
        "score": 4
    }
    inning = 0
    for play in plays:
        batter_id = play.get("matchup",{}).get("batter",{}).get("id")
        pitcher_id = play.get("matchup",{}).get("pitcher",{}).get("id")
        if batter_id is None or pitcher_id is None:
            continue
        if play.get("about",{}).get("inning") != inning:
            inning = play.get("about",{}).get("inning")
        event_type = play.get("result",{}).get("eventType")
        # should never ever happen but maybe add if event_type is None, continue and log an error for play number in gamePk
        
        # determine if at-bat
        if any([event_type in ["balk","catcher_interf","hit_by_pitch","walk","intent_walk","other_out","wild_pitch"],"caught_stealing" in event_type, "pickoff" in event_type, "stolen" in event_type, "sac" in event_type]):
            is_at_bat = False
        else:
            is_at_bat = True
            
        is_sac = True if "sac" in event_type else False
        is_walk = True if event_type in ["walk","intent_walk","hit_by_pitch"] else False

        #loop through runners and calculate if hit, number of outs, and number of bases
        outs = 0
        bases = 0
        is_hit = False
        earned_runs = 0
        runners = play.get("runners")
        if runners:
            for runner in runners:
                movement = runner.get("movement")
                details = runner.get("details",{})
                if movement is None:
                    continue
                if movement.get("isOut"):
                    outs += 1
                #if runner is batter and current item is batter's movement from home plate, we can calculate if hit and number of bases
                elif details.get("runner",{}).get("id") == batter_id and movement.get("start") is None and event_type!="field_error" and "fielders_choice" not in event_type and is_walk==False and runner.get("details",{}).get("eventType") not in ["wild_pitch", "passed_ball"] and movement.get("end") is not None:
                    bases = num_bases[movement["end"]]
                    is_hit = True

                if movement.get("end")=="score" and details.get("earned")==True:
                    responsible_pitcher = details.get("responsiblePitcher",{}).get("id")
                    if responsible_pitcher==pitcher_id:
                        earned_runs += 1
                    else: # else the run is earned by a previous pitcher. go find that pitcher's last play and add an extra earned run. Won't matter that the earned run is on the correct play or not.
                        for i in range(-1,-1-len(results),-1):
                            if responsible_pitcher == results[i]["pitcher_id"]:
                                results[i]["earned_runs"] += 1
                                break
                    
        results.append({
            "batter_id": batter_id,
            "pitcher_id": pitcher_id,
            "inning":inning,
            "event_type":event_type,
            "outs":outs,
            "is_at_bat":is_at_bat,
            "is_walk":is_walk,
            "is_sac":is_sac,
            "is_hit":is_hit,
            "bases":bases,
            "earned_runs":earned_runs
        })
    return results