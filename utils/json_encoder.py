from typing import Dict

class JsonEncoder:
    def __init__(self) -> None:
        pass

    def make_json(self, ITEM_SEQ: Dict) -> Dict:
        ITEM_SEQ = sorted(ITEM_SEQ.items(), key=lambda x: x[1], reverse=True)

        drugData = {
            "success": True,
            "data": [],
            "message": "success"
        }

        for (item, _) in ITEM_SEQ:
            drugData['data'].append({"ITEM_SEQ": item.split('_')[0]})

        return drugData
