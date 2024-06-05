from datetime import datetime
import os
import sys
import shutil
import json

verbose = False

ITEM_DATA = {}
ITEM_DATA_INDEX = "matchItems"
ITEM_MODEL_INDEX = "model"
# ITEM_DATA_INDEX = "items"
ITEM_FOLDER = os.path.join("assets", "minecraft", "optifine", "cit")
# ITEM_FOLDER = os.path.join("assets", "minecraft", "optifine", "cit", "items")
TEXTURE_FOLDER = os.path.join("assets", "minecraft", "textures")
VANILLA_FOLDER = os.path.join("VanillaDefault-Resource-Pack-1.20", "assets", "minecraft")
PROGRESSION = 0
PROGRESSION_TOTAL = 0
ITEMS_TO_GET = [
    "Black Microwave",
    "Black Toaster",
    "White Stove",
    "Cauldron_6",
    "Silver Faucet",
    "White Fridge",
    "Silver Silver Towel Rack Empty",
    "Silver Towel Rack w/ Towel",
    "Silver Shower Faucet",
    "Painting_8",
    "Painting_6f",
    "Painting_4a",
    "Painting_4g",
    "Painting_1b",
    "Painting_1d",
    "Painting_2a",
    "Shelf0",
    "Shelf1",
    "Toilet",
    "Paper Rolls",
    "Silver Roll Holder",
    "Counter4",
    "Red Plaid Blanket",
    "Round Kiddie Pool",
    "Popcorn Machine",
    "Popcorn Bucket",
    "Canvas Tent",
    "Stacked Pizza Boxes",
    "Cat Tree",
    "Light Blue Record Player",
    "Light Retro Jukebox",
    "Easel",
    "Wicker Boho Pillow",
    "Paints",
    "Plantstand",
    "Clothesline 3",
    "Clothesline 1",
    "Chest_2a",
    "Ikea Shelf",
    "Astronaut Statue",
    "MistieDawn",
    "Pet Crate",
    "Weeping Angel",
    "ClackBoard",
    "Crag Trophy",
    "Comedy and Tragedy",
    "Stacked Pizza Boxes",
    "Veggie Pizza Slice",
    "Single Pizza Box",
    "Hawaiian Pizza",
    "Pepperoni Pizza",
    "Keroppi Doll",
    "Teddy Bear",
    "Double Bed purple",
    "Solo Cup",
    "Stacked Cups",
    "Candy Bowl",
    "Pink Jewel Crown",
    "Blue Gaming Chair",
    "Purple Triple Monitor",
    "Small Hanging Monitor",
    "Large Hanging Monitor",
    "Black Laptop",
    "Monokuma",
    "Swingset",
    "Merry Go Round",
    "Slide",
    "Picnic Table",
    "Seesaw",
    "Blockade 1",
    "Red Open Cooler",
    "Eyeball CakePop Tray",
]


def get_usage():
    return """
    Usage ->{0} [<options>] <optifine_folder>
    Options:
        -o <output_file> --output <output_file> Write the output to the specified file
        -v --verbose Wite all log output to console
    """.format(sys.argv[0])


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def _log(message: str, color: str = ''):
    sys.stderr.write('{0}{1}- {2}{3}{4}'.format(color, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), message, bcolors.RESET, os.linesep))


def debug(message: str):
    if verbose:
        _log('DEBUG: {0}'.format(message), bcolors.OKGREEN)


def info(message: str):
    _log('INFO: {0}'.format(message), bcolors.OKBLUE)


def warn(message: str):
    _log('WARNING: {0}'.format(message), bcolors.WARNING)


def error(message: str, code: int = -1):
    _log('ERROR: {0}'.format(message), bcolors.FAIL)
    exit(code)


def parse_properties_file(file_path):
    properties = {}
    with open(file_path, "r") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                properties[key.strip()] = value.strip()
    return properties


def init_new_resource_pack(output: str):
    shutil.rmtree(output, ignore_errors=True)
    os.mkdir(output)
    shutil.copy(os.path.join("images", "pack.png"), os.path.join(output, "pack.png"))
    with open(os.path.join(output, "pack.mcmeta"), "w") as f:
        f.write("""{
  "pack": {
    "pack_format": 15,
    "description": "Custom Model Data Vanilla Resource Pack"
  }
}
""")
    folders: list[str] = [
        ["assets", "minecraft", "models", "item", "custom"],
        ["assets", "minecraft", "textures", "item", "custom"],
    ]
    for folder in folders:
        path: str = output
        for subfolder in folder:
            path = os.path.join(path, subfolder)
            if not os.path.exists(path):
                os.mkdir(path)
    # shutil.copytree(os.path.join(VANILLA_FOLDER, "models"), os.path.join(output, "assets", "minecraft", "models"))
    # shutil.copytree(os.path.join(VANILLA_FOLDER, "textures"), os.path.join(output, "assets", "minecraft", "textures"))
    # shutil.copytree(os.path.join(VANILLA_FOLDER, "particles"), os.path.join(output, "assets", "minecraft", "particles"))


def find_file(input_folder: str, output_folder: str, output_item_texture: str):
    print(f"Searching for files in {input_folder}")
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if file.endswith(".properties"):
                process_model(input_folder.replace(".\\", "").split(os.path.sep)[0], os.path.join(root, file), output_folder, output_item_texture)
                global PROGRESSION
                PROGRESSION += 1
                # print(f"Progression: {PROGRESSION}/{PROGRESSION_TOTAL}")


def count_properties_file(input_folder):
    for root, dirs, files in os.walk(input_folder):
        print(f"Processing {root}")
        for file in files:
            if file.endswith(".properties"):
                global PROGRESSION_TOTAL
                PROGRESSION_TOTAL += 1


def find_file_recursive(folder, target_file):
    found_files = []
    # Iterate over all the contents of the current folder
    for root, dirs, files in os.walk(folder):
        # Check if the target file is in the current folder
        if target_file.lower().replace(" ", "_") in [f.lower().replace(" ", "_") for f in files]:
            found_files.append(os.path.join(root, target_file))
        # Recursively search subfolders
        for directory in dirs:
            found_files.extend(find_file_recursive(os.path.join(root, directory), target_file))
    return found_files


def process_model(input_folder: str, properties_model_path: str, output_item: str, output_item_texture: str):
    properties: dict = parse_properties_file(properties_model_path)
    if ITEM_MODEL_INDEX not in properties:
        warn(f"Model not found in {properties_model_path}")
        return
    found: bool = False
    displayed_name: str = ""
    for item in ITEMS_TO_GET:
        if item.lower() in properties["nbt.display.Name"].lower():
            found = True
            displayed_name = item
            break
    if not found:
        return
    print(f"Processing {properties['nbt.display.Name']}")
    item: str = properties[ITEM_DATA_INDEX].replace("minecraft:", "")
    item_folder = os.path.join(output_item, item)
    item_texture_folder = os.path.join(output_item_texture, item)

    if not os.path.exists(item_folder):
        os.mkdir(item_folder)
    if not os.path.exists(item_texture_folder):
        os.mkdir(item_texture_folder)

    properties[ITEM_MODEL_INDEX] = properties[ITEM_MODEL_INDEX].replace("optifine/cit/", "")
    json_path = os.path.join(os.path.dirname(properties_model_path), properties[ITEM_MODEL_INDEX])
    if not os.path.exists(json_path):
        warn(f"Model {properties[ITEM_MODEL_INDEX]} not found in {json_path}")
        return
    with open(json_path, 'r') as file:
        data = json.load(file)
        data.pop("parent", None)
    for texture in data["textures"]:
        textures_org_name = data["textures"][texture].replace("./", "")
        textures_name = data["textures"][texture].replace("./", "").lower().replace(" ", "_")
        data["textures"][texture] = f"minecraft:item/custom/{item}/{textures_name}"

        texture_path = os.path.dirname(textures_name)
        new_texture_path = ""
        for path in texture_path.split("/"):
            new_texture_path = os.path.join(new_texture_path, path).lower().replace(" ", "_")
            if not os.path.exists(os.path.join(item_texture_folder, new_texture_path)):
                os.mkdir(os.path.join(item_texture_folder, new_texture_path))
        texture_path = new_texture_path
        textures_name = os.path.basename(textures_name) + ".png"
        textures_org_name = os.path.basename(textures_org_name) + ".png"
        input_texture_path = os.path.join(input_folder, TEXTURE_FOLDER, texture_path)
        output_texture_path = os.path.join(item_texture_folder, texture_path).lower().replace(" ", "_")
        texture_file_path = os.path.join(input_texture_path, textures_name)
        if not os.path.exists(texture_file_path):
            input_texture_path = find_file_recursive(os.path.join(input_folder, TEXTURE_FOLDER), textures_name)
            if len(input_texture_path) == 0:
                info(f"Texture {textures_name} not found in. Search in Vanilla folder")
                input_texture_path = find_file_recursive(os.path.join(VANILLA_FOLDER, "textures"), textures_name)
                if len(input_texture_path) == 0:
                    warn(f"Texture {textures_name} not found in {input_texture_path}")
                    return
            input_texture_path = os.path.dirname(input_texture_path[0])
        if not os.path.exists(output_texture_path):
            os.mkdir(output_texture_path)
        print(textures_org_name)
        if not os.path.exists(os.path.join(output_texture_path, textures_org_name)):
            shutil.copy(os.path.join(input_texture_path, textures_org_name), os.path.join(output_texture_path, textures_name))

    with open(os.path.join(item_folder, properties[ITEM_MODEL_INDEX]), 'w') as file:
        file.write(json.dumps(data, indent=4))

    if item not in ITEM_DATA:
        ITEM_DATA[item] = {
            "parent": "minecraft:item/generated",
            "textures": {
                "layer0": f"minecraft:item/{item}"
            },
            "overrides": []
        }

    custom_model_data_count: int = len(ITEM_DATA[item]["overrides"]) + 100
    # print(f"custom:item/{item}/{properties[ITEM_MODEL_INDEX].replace('.json', '')}")
    ITEM_DATA[item]["overrides"].append({
        "predicate": {
            "custom_model_data": custom_model_data_count
        },
        "model": f"minecraft:item/custom/{item}/{properties[ITEM_MODEL_INDEX].replace('.json', '')}".lower().replace(" ", "_"),
        "displayed_name": displayed_name
    })


def redefine_custom_model_data(json_data, items_to_get):
    overrides = json_data["overrides"]
    item_map = {item: idx for idx, item in enumerate(items_to_get)}

    overrides.sort(key=lambda x: item_map.get(x.get("display", ""), len(items_to_get)))

    for idx, override in enumerate(overrides, start=1):
        override["predicate"]["custom_model_data"] = idx + 100

    return json_data


def main(input: str, output: str):
    info('Input file: {0}'.format(input))
    init_new_resource_pack(output)

    output_item = os.path.join(output, "assets", "minecraft", "models", "item", "custom")
    output_item_texture = os.path.join(output, "assets", "minecraft", "textures", "item", "custom")
    count_properties_file(os.path.join(input, ITEM_FOLDER))
    find_file(os.path.join(input, ITEM_FOLDER), output_item, output_item_texture)

    for item in ITEM_DATA:
        with open(os.path.join(os.path.join(output, "assets", "minecraft", "models", "item"), item + ".json"), 'w') as file:
            vanilla_file = find_file_recursive(os.path.join(VANILLA_FOLDER, "models", "item"), item + ".json")
            if len(vanilla_file) == 0:
                warn(f"Vanilla model {item}.json not found")
                file.write(json.dumps(ITEM_DATA[item], indent=4))
            else:
                with open(vanilla_file[0], 'r') as vanilla:
                    vanilla_data = json.load(vanilla)
                    vanilla_data["overrides"] = ITEM_DATA[item]["overrides"]
                    modified_json = redefine_custom_model_data(vanilla_data, ITEMS_TO_GET)
                    ITEM_DATA[item]["overrides"] = modified_json["overrides"]
                    file.write(json.dumps(modified_json, indent=4))
        for item_override in ITEM_DATA[item]["overrides"]:
            custom_model_data = item_override["predicate"]["custom_model_data"]
            print(f"Name: {item_override['displayed_name']}")
            print(f"/give norphiil minecraft:{item} 1 {{CustomModelData:{custom_model_data}}}")


if __name__ == "__main__":
    input = None
    output = None
    if len(sys.argv) == 1:
        info(get_usage())
        exit(0)
    else:
        output = "minecraft_vanilla"
        for arg in range(1, len(sys.argv), 1):
            if sys.argv[arg].startswith('-'):
                if sys.argv[arg] in ['-o', '--output']:
                    arg += 1
                    output = sys.argv[arg]
                elif sys.argv[arg] in ['-v', '--verbose']:
                    verbose = True
                elif sys.argv[arg] in ['-h', '--help']:
                    _log('HELP: {0}'.format(get_usage()), bcolors.OKBLUE)
                    exit(0)
                else:
                    error('Unkown argument {0}'.format(sys.argv[arg]), 2)
            else:
                input = sys.argv[arg]

    if input is None:
        error('You must specify the input folder.{0}\t See help for more info'.format(os.linesep))

    main(input, output)
