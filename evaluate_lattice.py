import argparse
import json
import sys
from collections import defaultdict


def main(opt):
    topk = opt["top"]
    result_file = opt["result"]
    with open(result_file, 'r') as fin:
        dialogues = json.loads(fin.read())

    print("Number of dialogues:", len(dialogues))
    num_turns = 0

    num_relax = defaultdict(int)
    num_request = defaultdict(int)

    for dialogue in dialogues:
        turns = dialogue['dialogue']
        num_turns += len(turns)

        # For every turn in dialogue
        for turn in turns:

            relax_count = 0
            request_count = 0

            true_state = turn[1]['True State']
            pred_state = turn[2]['Prediction']
            lattice = turn[3]['Lattice']

            # Iterate through slots of Belief State
            for slot_type, slot_value in true_state.items():
                pred_slot_value = pred_state[slot_type]
                lattice_top_values = lattice[slot_type][:topk]
                if slot_type == "request":
                    request_count += abs(len(slot_value) -
                                         len(pred_slot_value))
                else:
                    if relax_count == -1:
                        continue
                    elif slot_value == pred_slot_value:
                        pass
                    elif slot_value in lattice_top_values:
                        relax_count += 1
                    else:
                        relax_count = -1  # Not in top k
                        break

            if relax_count == 2:
                print("True state", true_state)
                print("Prediction", pred_state)
                print("Lattice", lattice)

            num_relax[relax_count] += 1
            num_request[request_count] += 1

    assert sum(num_relax.values()) == num_turns

    print('num_turns', num_turns)
    print('num_relax', num_relax)
    print('num_request', num_request)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--result', type=str,
                        default="./results/woz_tracking.json")
    parser.add_argument('--top', type=int, default=5, help="Top K slot values")
    args = parser.parse_args()
    opt = vars(args)
    main(opt)
