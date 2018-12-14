import json
import sys


def main():
    relax_limit = 1
    topk = 3
    result_file = "./results/woz_tracking.json"
    with open(result_file, 'r') as fin:
        dialogues = json.loads(fin.read())

    num_dialogues = len(dialogues)
    num_turns = 0

    num_relax = {}

    for dialogue in dialogues:
        turns = dialogue['dialogue']
        num_turns += len(turns)

        for turn in turns:

            relax_count = 0
            true_state = turn[1]['True State']
            pred_state = turn[2]['Prediction']
            lattice = turn[3]['Lattice']

            for slot_type, slot_value in true_state.items():
                pred_slot_value = pred_state[slot_type]
                lattice_top_values = lattice[slot_type][:topk]
                if slot_type == "request":
                    assert isinstance(slot_value, list)
                    relax_count += abs(len(slot_value) - len(pred_slot_value))
                else:
                    if slot_value == pred_slot_value:
                        pass
                    elif slot_value in lattice_top_values:
                        relax_count += 1
                    else:
                        relax_count = -1
                        break

            if relax_count not in num_relax:
                num_relax[relax_count] = 0
            num_relax[relax_count] += 1

    print('num_turns', num_turns)
    print('num_relax', num_relax)


if __name__ == "__main__":
    main()
