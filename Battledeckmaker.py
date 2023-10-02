import json

dic_name = 'card_info_dic2.1.json'
deck1_name = 'Akatan.json'
deck2_name = 'Aoma.json'
file_name = "use_cardlist"

def makelist(dic_name,deck1_name,deck2_name,file_name):
    with open(dic_name) as f:
        dic_data = json.load(f)
    with open(deck1_name) as f:
        deck1_data = json.load(f)
    with open(deck2_name) as f:
        deck2_data = json.load(f)

    use_cardlist = {}
    cnt = 1
    for deck_info in deck1_data.values():
        card_name = deck_info['name']
        for list_info in dic_data.values():
            if list_info["name"] == card_name:
                print(list_info.keys())
                del list_info["id"], list_info["flavor"], list_info["rare"], list_info["illust"]
                use_cardlist[str(cnt)] = list_info
                cnt += 1
    for deck_info in deck2_data.values():
        card_name = deck_info['name']
        for list_info in dic_data.values():
            if list_info["name"] == card_name:
                del list_info["id"], list_info["flavor"], list_info["rare"], list_info["illust"]
                use_cardlist[str(cnt)] = list_info
                cnt += 1

    with open(file_name + '.json', 'w') as f:
        json.dump(use_cardlist, f, indent=4, ensure_ascii=False)