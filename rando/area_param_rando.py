import os
import byml
import random

def randomize_area_params(print):
    print("Randomizing area params...")

    print("Decompiling BYML...")
    arr = os.listdir("areaparams")
    area_params = {}

    for fpath in arr:
        f = open(f'areaparams/{fpath}', "rb").read()
        file = byml.Byml(f)
        document = file.parse()

        area_params[fpath] = document

    all_music = []
    all_environment_sound = []
    all_environment_sound_efx = []
    all_wonder_bgm_type = []
    all_palettes = []
    all_skins = []

    print("Gathering all data...")
    for areaparamname in area_params:
        aparam = area_params[areaparamname]
        if "BgmType" in aparam:
            if aparam["BgmType"] not in all_music:
                all_music.append(aparam["BgmType"])
        if "EnvironmentSound" in aparam:
            if aparam["EnvironmentSound"] not in all_music:
                all_environment_sound.append(aparam["EnvironmentSound"])
        if "EnvironmentSoundEfx" in aparam:
            if aparam["EnvironmentSoundEfx"] not in all_music:
                all_environment_sound_efx.append(aparam["EnvironmentSoundEfx"])
        if "WonderBgmType" in aparam:
            if aparam["WonderBgmType"] not in all_music:
                all_wonder_bgm_type.append(aparam["WonderBgmType"])
        if "EnvPaletteSetting" in aparam:
            if "InitPaletteBaseName" in aparam["EnvPaletteSetting"]:
                if aparam["EnvPaletteSetting"]["InitPaletteBaseName"] not in all_palettes:
                    all_palettes.append(aparam["EnvPaletteSetting"]["InitPaletteBaseName"])
        if "SkinParam" in aparam:
            if "FieldA" in aparam["SkinParam"]:
                if aparam["SkinParam"]["FieldA"] not in all_skins:
                    all_skins.append(aparam["SkinParam"]["FieldA"])
            if "FieldB" in aparam["SkinParam"]:
                if aparam["SkinParam"]["FieldB"] not in all_skins:
                    all_skins.append(aparam["SkinParam"]["FieldB"])
            if "Object" in aparam["SkinParam"]:
                if aparam["SkinParam"]["Object"] not in all_skins:
                    all_skins.append(aparam["SkinParam"]["Object"])

    print("Assigning new values...")
    for areaparamname in area_params:
        aparam = area_params[areaparamname]
        if "BgmType" in aparam:
            aparam["BgmType"] = random.choice(all_music)
        if "EnvironmentSound" in aparam:
            aparam["EnvironmentSound"] = random.choice(all_environment_sound)
        if "EnvironmentSoundEfx" in aparam:
            aparam["EnvironmentSoundEfx"] = random.choice(all_environment_sound_efx)
        if "WonderBgmType" in aparam:
            aparam["WonderBgmType"] = random.choice(all_wonder_bgm_type)
        if "EnvPaletteSetting" in aparam:
            if "InitPaletteBaseName" in aparam["EnvPaletteSetting"]:
                aparam["EnvPaletteSetting"]["InitPaletteBaseName"] = random.choice(all_palettes)
        if "SkinParam" in aparam:
            if "FieldA" in aparam["SkinParam"]:
                aparam["SkinParam"]["FieldA"] = random.choice(all_skins)
            if "FieldB" in aparam["SkinParam"]:
                aparam["SkinParam"]["FieldB"] = random.choice(all_skins)
            if "Object" in aparam["SkinParam"]:
                aparam["SkinParam"]["Object"] = random.choice(all_skins)

    if not os.path.exists("randomized/romfs/Stage/AreaParam/"):
        os.makedirs("randomized/romfs/Stage/AreaParam/")

    print("Compiling BYML...")
    byml_areaparams = {}
    for areaparamname in area_params:
        areaparam = area_params[areaparamname]
        writer = byml.Writer(areaparam, be=False, version=7)

        fpath = f"randomized/romfs/Stage/AreaParam/{areaparamname}"
        with open(fpath, "+wb") as f:
            writer.write(f)

    print("Randomized area params!")