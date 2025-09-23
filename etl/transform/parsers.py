def det_base_runners(runners, batter_id, pitch_index):
    base_runners = {}
    for runner in runners:
        details = runner.get("details",{})
        movement = runner.get("movement",{})
        runner_id = details.get("runner",{}).get("id")
        start = movement.get("start","")
        end = movement.get("end")
        is_out = movement.get("isOut")
        play_index = details.get("playIndex")
        if runner_id!=batter_id:
            if runner_id not in base_runners:
                base_runners[runner_id] = start
            elif start < base_runners[runner_id]:
                base_runners[runner_id] = start
            if play_index!=pitch_index and not is_out:
                base_runners[runner_id] = end
    vals = base_runners.values()
    first_base = "1B" in vals
    second_base = "2B" in vals
    third_base = "3B" in vals

    return first_base, second_base, third_base
            

def det_earned_runs(runners,pitcher_id,results):
    earned_runs = 0
    for runner in runners:
        end = runner.get("movement",{}).get("end")
        details = runner.get("details",{})
        earned = details.get("earned")
        if end=="score" and earned==True:
            responsible_pitcher = details.get("responsiblePitcher",{}).get("id")
            if responsible_pitcher == pitcher_id:
                earned_runs += 1
            else: # else the run is earned by a previous pitcher. go find that pitcher's last play and add an extra earned run. Won't matter that the earned run is on the correct play or not.
                for i in range(-1, -1 - len(results), -1):
                    if responsible_pitcher == results[i]["pitcher_id"]:
                        results[i]["earned_runs"] += 1
                        break
    return earned_runs

def det_is_at_bat(event_type):
    if any([event_type in ["balk","catcher_interf","hit_by_pitch","walk","intent_walk","other_out","wild_pitch"],"caught_stealing" in event_type, "pickoff" in event_type, "stolen" in event_type, "sac" in event_type]):
        return False
    else:
        return True

def process_fielding(runners, has_out, pitch_index):
    fielder=  None
    errer = None
    outer = None
    fielder_id = None
    errer_id = None
    outer_id = None
    out = False

    for runner in runners:
        details = runner.get("details",{})
        movement = runner.get("movement",{})
        play_index = details.get("playIndex")
        is_out = movement.get("isOut")
        if play_index==pitch_index:
            credits = runner.get("credits",[])
            for credit in credits:
                credit_type = credit.get("credit","")
                position_code = int(credit.get("position",{}).get("code",0))
                player_id = credit.get("player",{}).get("id",0)
                if "error" in credit_type:
                    errer = position_code
                    errer_id = player_id
                if fielder is None and credit_type in ["f_assist","f_fielded_ball"]:
                    fielder = position_code
                    fielder_id = player_id
                elif credit_type=="f_putout":
                    outer = position_code
                    outer_id = player_id
                    out = True
        if (fielder is not None or outer is not None) and has_out==out:
            break

    return fielder,fielder_id,errer,errer_id,outer,outer_id,out

def det_is_hit(runners, pitch_index, batter_id, event_type):
    base_dict = {
        "1B": 1,
        "2B": 2,
        "3B": 3,
        "score": 4
    }
    pickoff_out = False
    is_hit = False
    bases = 0

    for runner in runners:
        details = runner.get("details",{})
        movement = runner.get("movement",{})
        play_index = details.get("playIndex")
        is_out = movement.get("isOut")
        if play_index!=pitch_index and is_out:
            pickoff_out = True
        if details.get("runner",{}).get("id")==batter_id and movement.get("start") is None:
            batter_end = movement.get("end")
            if is_out==False and event_type!="field_error" and "fielders_choice" not in event_type:
                is_hit = True
                bases = base_dict[batter_end]
            break

    return pickoff_out, is_hit, bases

def parse_plays(plays,gamePk):
    results = []

    
    for play in plays:

        # references
        matchup = play.get("matchup")
        about = play.get("about")
        result = play.get("result")
        last_pitch = play.get("playEvents",[{}])[-1]
        pitch_index = play.get("pitchIndex",[-1])
        if len(pitch_index)==0:
            pitch_index = -1
        else:
            pitch_index = pitch_index[-1]
        runners = play.get("runners",[])
        description = result.get("description","")
        hit_data = last_pitch.get("hitData",{})
        is_in_play = last_pitch.get("details",{}).get("isInPlay")

        # quick facts
        batter_id = matchup.get("batter",{}).get("id")
        pitcher_id = matchup.get("pitcher",{}).get("id")
        if batter_id is None or pitcher_id is None:
            continue
        inning = about.get("inning")
        event_type = result.get("eventType")
        num_outs = last_pitch.get("count",{}).get("outs")
        has_out = about.get("hasOut")
        has_score = about.get("isScoringPlay")
        location = int(hit_data.get("location",0))

        # play status
        if any(["fan interference" in description,"catcher interference" in description,event_type=="home_run",location==0]):
            fieldable_play = False
        else:
            fieldable_play = is_in_play
        is_sac = True if "sac" in event_type else False
        is_walk = True if event_type in ["walk","intent_walk","hit_by_pitch"] else False
        is_at_bat = det_is_at_bat(event_type)

        # play data
        outs = sum([True if runner.get("movement",{}).get("isOut") else False for runner in runners])
        earned_runs = det_earned_runs(runners, pitcher_id, results)
        
        if not is_in_play:
            location,launch_speed,launch_angle,total_distance,trajectory,hardness,coord_x,coord_y,first_base_runner,second_base_runner,third_base_runner,fielder,fielder_id,outer,outer_id,errer,errer_id,out,pickoff_out = [None] * 19
            is_hit = False
            bases = 0
            
        else:
            launch_speed = hit_data.get("launchSpeed")
            launch_angle = hit_data.get("launchAngle")
            total_distance = hit_data.get("totalDistance")
            trajectory = hit_data.get("trajectory")
            hardness = hit_data.get("hardness")
            coordinates = hit_data.get("coordinates", {})
            coord_x = coordinates.get("coordX")
            coord_y = coordinates.get("coordY")

            first_base_runner, second_base_runner, third_base_runner = det_base_runners(runners, batter_id, pitch_index)
            fielder,fielder_id,errer,errer_id,outer,outer_id,out = process_fielding(runners, has_out, pitch_index)
            pickoff_out, is_hit, bases = det_is_hit(runners, pitch_index, batter_id, event_type)


        if fieldable_play:
            if (fielder is None and errer is not None):
                fielder = errer
                fielder_id = errer_id
        results.append({
            "batter_id": batter_id,
            "pitcher_id": pitcher_id,
            "inning":inning,
            "event_type":event_type,
            "is_at_bat":is_at_bat,
            "is_walk":is_walk,
            "is_sac":is_sac,
            "num_outs":num_outs,
            "has_out":has_out,
            "has_score":has_score,
            "fieldable_play":fieldable_play,
            "outs":outs,
            "earned_runs":earned_runs,
            "launch_speed":launch_speed,
            "launch_angle":launch_angle,
            "trajectory":trajectory,
            "hardness":hardness,
            "total_distance":total_distance,
            "hit_location":location,
            "coord_x":coord_x,
            "coord_y":coord_y,
            "first_base_runner":first_base_runner,
            "second_base_runner":second_base_runner,
            "third_base_runner":third_base_runner,
            "is_hit":is_hit,
            "bases":bases,
            "fielder":fielder,
            "fielder_id":fielder_id,
            "putouter":outer,
            "putouter_id":outer_id,
            "errer":errer,
            "errer_id":errer_id,
            "in_play_out":out,
            "pickoff_out":pickoff_out
        })
    return results
