class JsonEncoder:
    def __init__(self) -> None:
        pass

    def make_json(self, item_seq: dict) -> dict:
        item_seq = sorted(item_seq.items(), key=lambda x: x[1], reverse=True)

        drugData = {
            "success": True,
            "data": [],
            "message": "success"
        }

        for (item, _) in item_seq:
            drugData['data'].append({"item_seq": item.split('_')[0]})

        return drugData
