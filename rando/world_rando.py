import os
import byml
import random

def randomize_world_map(print):
    print("Randomizing world map...")

    print("Decompiling BYML...")
    arr = os.listdir("worlds")
    worlds = {}

    for fpath in arr:
        f = open(f'worlds/{fpath}', "rb").read()
        file = byml.Byml(f)
        document = file.parse()

        worlds[fpath] = document

    all_courses = []

    print("Gathering all courses...")
    for worldname in worlds:
        world = worlds[worldname]
        for course in world["CourseTable"]:
            all_courses.append(course["StagePath"])

    print("Shuffling...")
    random.shuffle(all_courses)

    print("Assigning new values...")
    index = 0
    for worldname in worlds:
        world = worlds[worldname]
        for course in world["CourseTable"]:
            course["StagePath"] = all_courses[index]
            index += 1

    if not os.path.exists("randomized/romfs/Stage/WorldMapInfo/"):
        os.makedirs("randomized/romfs/Stage/WorldMapInfo/")

    print("Compiling BYML...")
    byml_worlds = {}
    for worldname in worlds:
        world = worlds[worldname]
        writer = byml.Writer(world, be=False, version=7)

        fpath = f"randomized/romfs/Stage/WorldMapInfo/{worldname}"
        with open(fpath, "+wb") as f:
            writer.write(f)

    print("Randomized world map!")