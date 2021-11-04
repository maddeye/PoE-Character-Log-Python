import base64
import json
import re
import zlib

from typing import Dict, List
from xml.dom import minidom

from utils.config import CONFIG

TREE_VERSION = "3_16"

socketTrans = {
    "Weapon": "Weapon 1",
    "Offhand": "Weapon 2",
    "Weapon2": "Weapon 1 Swap",
    "Offhand2": "Weapon 2 Swap",
    "Amulet": "Amulet",
    "Gloves": "Gloves",
    "Boots": "Boots",
    "Ring": "Ring 1",
    "Ring2": "Ring 2",
    "Belt": "Belt",
    "BodyArmour": "Body Armour",
    "Helm": "Helmet",
    "Flask": "Flask",
}

rarity = ("NORMAL", "MAGIC", "RARE", "UNIQUE")


class POB:
    def __init__(self):
        pass

    def buildskills(self, items: Dict):
        gemgroups = {}
        for item in items:
            slot = item["inventoryId"]
            if (
                slot
                and slot != "MainInventory"
                and slot != "Flask"
                and slot != "Weapon2"
                and slot != "Offhand2"
            ):
                gemobjs: List[Dict] = []
                for g in range(0, 6):
                    gemobjs.append({"gems": [], "supports": []})
                gemgroups[slot] = gemobjs
                if "socketedItems" in item:
                    for gem in range(0, len(item["socketedItems"])):
                        gqual = "0"
                        glvl = "1"
                        for prop in item["socketedItems"][gem]["properties"]:
                            if prop["name"] == "Quality":
                                gqual = re.findall(
                                    r"-?\d+\.?\d*", prop["values"][0][0]
                                )[0]
                            elif prop["name"] == "Level":
                                glvl = re.findall(r"-?\d+\.?\d*", prop["values"][0][0])[
                                    0
                                ]
                        group = item["sockets"][gem]["group"]
                        if (
                            item["socketedItems"][gem]["colour"]
                            and item["socketedItems"][gem]["typeLine"]
                        ):
                            gemstr = {
                                "color": item["socketedItems"][gem]["colour"],
                                "name": item["socketedItems"][gem]["typeLine"],
                                "quality": gqual,
                                "level": glvl,
                            }
                            if " Support" in item["socketedItems"][gem]["typeLine"] or (
                                "support" in item["socketedItems"][gem]
                                and item["socketedItems"][gem]["support"]
                            ):
                                gemgroups[slot][group]["supports"].append(gemstr)
                            else:
                                gemgroups[slot][group]["gems"].append(gemstr)
        return gemgroups

    def getname(self, gem: Dict) -> str:
        gem_name = gem["name"]
        gem_name = gem_name.replace(" Support", "")
        gem_name = gem_name.replace("Anomalous ", "")
        gem_name = gem_name.replace("Divergent ", "")
        gem_name = gem_name.replace("Phantasmal ", "")

        return gem_name

    def getbyname(self, attrs, attr, name):
        if attr in attrs:
            for at in attrs[attr]:
                if "name" in at and at["name"] == name:
                    return at["values"][0][0]

    def abbrev(self, gem: str) -> str:
        abb = gem.split()
        if len(abb) > 2:
            return abb[0][:1] + abb[1][:1] + abb[2][:1]
        elif len(abb) > 1:
            return abb[0][:2] + abb[1][:2]
        else:
            return abb[0][:4]

    def fixspec(self, strin: str):
        strin = strin.replace(chr(246), "o")  # diaresis 'o' as in Maelstrom
        strin = strin.replace(chr(228), "a")  # umlaut 'a' as in Doppelganger
        specchar = re.search(r"...[\x80-\xff]...", strin)

        if specchar:
            strin = re.sub(r"[\x80-\xff]", "?", strin)

        return strin

    def make_xml(self, character_history: List[dict]) -> str:
        config = CONFIG()

        character_data = character_history[0]

        root = minidom.Document()
        pob = root.createElement("PathOfBuilding")
        root.appendChild(pob)

        build = root.createElement("Build")
        build.setAttribute("targetVersion", "3_0")

        build.setAttribute("level", str(character_data["level"]))
        build.setAttribute("className", str(character_data["classId"]))
        build.setAttribute("ascendClassName", str(character_data["ascendancyClass"]))
        build.setAttribute("viewMode", "ITEMS")

        # add a dummy playerstat node because PoB's XML parser doesn't read "empty" Build nodes correctly
        dummyplayerstat = root.createElement("PlayerStat")
        build.appendChild(dummyplayerstat)
        pob.appendChild(build)

        tree = root.createElement("Tree")
        tree.setAttribute("activeSpec", "1")
        pob.appendChild(tree)

        items = root.createElement("Items")
        items.setAttribute("activeItemSet", "1")
        items.setAttribute("useSecondWeaponSet", "nil")
        pob.appendChild(items)

        skills = root.createElement("Skills")
        pob.appendChild(skills)

        # For each level
        for e in range(0, len(character_history)):

            level = character_history[e]["level"]

            # ========================================================================================
            # Passive Tree
            # ========================================================================================
            lltree = 0

            # last_nodes = ",".join(str(node) for node in json.loads(character_history[e - 1]["passives"]))
            nodes = ",".join(
                str(node) for node in json.loads(character_history[e]["passives"])
            )

            if (
                level - lltree >= config.get("levelstep")
                or len(character_history) - e <= 1
            ):
                id = root.createElement("Spec")
                lltree = level

                id.setAttribute("title", f"{e} - Level {level}")
                id.setAttribute(
                    "ascendClassId", str(character_history[e]["ascendancyClass"])
                )
                id.setAttribute("nodes", nodes)
                id.setAttribute("treeVersion", TREE_VERSION)
                id.setAttribute("classId", str(character_history[e]["classId"]))
                tree.appendChild(id)

            isn = 1
            skilldb: Dict = {}

            # ========================================================================================
            # Skills
            # ========================================================================================
            character_items = json.loads(character_history[e]["items"])

            gemgroups = self.buildskills(character_items)
            mainskills = []
            for slot in gemgroups:
                skill = root.createElement("Skill")
                skillset = ""
                for group in gemgroups[slot]:
                    if len(group["supports"]) > 0:
                        for gm in group["gems"]:
                            mainskills.append(
                                "["
                                + str(len(group["supports"]))
                                + "] "
                                + self.getname(gm)
                            )
                    if len(group["gems"]) > 0:
                        for mg in sorted(group["gems"], key=lambda k: k["name"]):
                            skillset += "," + self.getname(mg)
                        for sg in sorted(group["supports"], key=lambda k: k["name"]):
                            skillset += "+" + self.abbrev(self.getname(sg))
                        for gm in group["gems"] + group["supports"]:
                            gem = root.createElement("Gem")
                            gem.setAttribute("level", gm["level"])
                            gem.setAttribute("nameSpec", self.getname(gm))
                            gem.setAttribute("quality", gm["quality"])
                            gem.setAttribute("enabled", "true")
                            skill.appendChild(gem)

                if skillset != "" and (
                    slot not in skilldb or skillset not in skilldb[slot]
                ):
                    skill.setAttribute("label", f"Level {level} - {skillset}")
                    skill.setAttribute("slot", socketTrans[slot])
                    skill.setAttribute("enabled", "true")
                    skills.appendChild(skill)
                    skilldb[slot] = skillset

                itemset = root.createElement("ItemSet")
                itemset.setAttribute("id", str(isn))
                itemset.setAttribute("useSecondWeaponSet", "nil")
                itemset.setAttribute(
                    "title", f'{isn} - Level {character_history[e]["level"]}'
                )

                # ========================================================================================
                # Items
                # ========================================================================================
                fln = 1
                itn = 1
                itemdb: Dict = {}
                lastset: Dict = {}

                for itm in character_items:
                    if itm["inventoryId"] in socketTrans and itm["frameType"] < 4:
                        itemkey = f"{itm['name']}{itm['typeLine']}"
                    itemno = str(itn)
                    if itemkey in itemdb:
                        itemno = itemdb[itemkey]
                    else:
                        itemdb[itemkey] = str(itn)
                        item = root.createElement("Item")
                        item.setAttribute("id", itemno)
                        itemtext = f"\nRarity: {rarity[itm['frameType']]}\n{itm['name']}\n{itm['typeLine']}\n"
                        if "id" in itm:
                            itemtext += f'Unique ID:{itm["id"]}\n'
                        if "ilvl" in itm:
                            itemtext += f'Item Level: {itm["ilvl"]}\n'
                        lvlreq = self.getbyname(itm, "requirements", "Level")
                        if "sockets" in itm:
                            itemtext += "Sockets: "
                            for gem in range(0, len(itm["sockets"])):
                                if (
                                    gem > 0
                                    and itm["sockets"][gem - 1]["group"]
                                    != itm["sockets"][gem]["group"]
                                ):
                                    itemtext += " "
                                elif gem > 0:
                                    itemtext += "-"
                                itemtext += itm["sockets"][gem]["sColour"]
                            itemtext += "\n"
                        if lvlreq:
                            itemtext += f"LevelReq: {lvlreq}\n"
                        if "implicitMods" in itm:
                            itemtext += f'Implicits: {len(itm["implicitMods"])}\n'
                            for imp in itm["implicitMods"]:
                                itemtext += imp + "\n"
                        if "explicitMods" in itm:
                            for exp in itm["explicitMods"]:
                                itemtext += exp + "\n"
                        itemtext = self.fixspec(itemtext)
                        text = root.createTextNode(itemtext)
                        item.appendChild(text)
                        items.appendChild(item)
                        itn = itn + 1
                    iid = socketTrans[itm["inventoryId"]]
                    if iid == "Flask":
                        iid += f" {fln}"
                        fln = fln + 1
                    islot = root.createElement("Slot")
                    islot.setAttribute("name", iid)
                    islot.setAttribute("itemId", itemno)
                    itemset.appendChild(islot)
                    if itemset.parentNode is None and (
                        iid not in lastset or lastset[iid] != itemno
                    ):
                        items.appendChild(itemset)
                        isn = isn + 1
                    lastset[iid] = itemno

            # Mainskill
            mainskill = re.sub(
                "\\[[0-9]*\\] ", "", "  ".join(sorted(set(mainskills), reverse=True))
            )
            if len(mainskill) > 75:
                mainskill = mainskill[0:75] + "..."

        return root.toxml(encoding="ascii")

    def pob_code(self, xml: str) -> str:
        try:
            return base64.b64encode(zlib.compress(xml), altchars=b"-_").decode("ascii")
        except Exception as err:
            raise err

    def pob_code_from_char(self, char: dict) -> str:
        return self.pob_code(self.make_xml([char]))
