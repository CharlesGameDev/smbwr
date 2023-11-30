import os
import byml
import random
import zstandard
from info import ENEMY_LIST

def randomize_level_content(print, randomize_enemies, randomize_wonder_effects):
    strs = []

    if not randomize_enemies and not randomize_wonder_effects: return
    
    if randomize_enemies: strs.append("Enemies")
    if randomize_wonder_effects: strs.append("Wonder Effects")
    
    print(f"Randomizing level content with {'and'.join(strs)}...")

    print("Decompiling BYML...")
    arr = os.listdir("levels")
    levels = {}

    for fpath in arr:
        f = open(f'levels/{fpath}', "rb").read()
        decompressed = zstandard.decompress(f)
        file = byml.Byml(decompressed)
        document = file.parse()

        levels[fpath] = document

    wonder_types = [1, 3, 4, 5, 6, 7, 8, 9, 11]
    min_wonder_time = 60
    max_wonder_time = 120

    print("Assigning new values...")
    for levelname in levels:
        level = levels[levelname]
        if "Actors" in level:
            for actor in level["Actors"]:
                if randomize_enemies:
                    if actor["Gyaml"].startswith("Enemy"):
                        actor["Gyaml"] = random.choice(ENEMY_LIST).replace("\n", "")
                if randomize_wonder_effects:
                    if actor["Gyaml"] == "ObjectWonderTag":
                        time = random.randrange(min_wonder_time, max_wonder_time)
                        effect = random.choice(wonder_types)

                        actor["Dynamic"]["WonderTime"] = byml.Float(time)
                        actor["Dynamic"]["PlayerWonderType"] = byml.Int(effect)

    if not os.path.exists("randomized/romfs/BancMapUnit/"):
        os.makedirs("randomized/romfs/BancMapUnit/")

    print("Compiling BYML...")
    byml_levels = {}
    for levelname in levels:
        level = levels[levelname]
        writer = byml.Writer(level, be=False, version=7)
        b = writer.get_bytes()

        compressed = zstandard.compress(b)


        fpath = f"randomized/romfs/BancMapUnit/{levelname}"
        with open(fpath, "+wb") as f:
            f.write(compressed)

    print("Randomized level content!")