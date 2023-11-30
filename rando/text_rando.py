import zstandard
import sarc
import random
import os
from pymsyt import Msbt

def randomize_text(print):
    print("Randomizing text content...")

    print("Decompressing MALS packs...")
    mals = os.listdir("mals")

    all_text = []
    msbt_files = {}

    all_text = []

    if not os.path.exists("randomized/romfs/Mals/"):
        os.makedirs("randomized/romfs/Mals/")

    for mal in mals:
        archive_bytes = open(f"mals/{mal}", "rb").read()
        archive_bytes = zstandard.decompress(archive_bytes)

        archive = sarc.SARC(archive_bytes)
        writer = sarc.make_writer_from_sarc(archive)
        
        all_text = []

        print("Compiling all text...")

        for file in archive.list_files():
            data = archive.get_file_data(file).tobytes()

            try:
                msbt = Msbt.from_binary(data)
            except:
                continue

            msbt_data = msbt.to_dict()
            # this is an absolute mess
            for data in msbt_data:
                if type(msbt_data[data]) == dict:
                    for entryname in msbt_data[data]:
                        entry = msbt_data[data][entryname]
                        if "contents" in entry:
                            for c in entry["contents"]:
                                if "text" in c:
                                    all_text.append(c["text"])

        random.shuffle(all_text)
        print(f"{len(all_text)} text strings")

        print("Shuffling...")
        for file in archive.list_files():
            data = archive.get_file_data(file).tobytes()

            try:
                msbt = Msbt.from_binary(data)
            except:
                continue

            msbt_data = msbt.to_dict()

            for data in msbt_data:
                if type(msbt_data[data]) == dict:
                    for entryname in msbt_data[data]:
                        entry = msbt_data[data][entryname]
                        if "contents" in entry:
                            for c in entry["contents"]:
                                if "text" in c:
                                    c["text"] = all_text.pop()

            bin = Msbt.from_dict(msbt_data).to_binary(big_endian=False)
            writer.add_file(file, bin)

        print("Writing new data...")

        path = f"randomized/romfs/Mals/{mal}"
        if not os.path.exists(path):
            open(path, "x").write("")

        writer.write(open(path, "wb"))
        data = open(path, "rb").read()
        compressed = zstandard.compress(data)
        open(path, "wb").write(compressed)

    print("Randomized text!")