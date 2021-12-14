import sys
import os
import subprocess as sub
import pickle

class InputOutput():
    def __init__(self, inp, outp):
        self.input = inp
        self.output = outp

def test_file(dire):
    if not dire in results_dict:
        print(f"[ERROR] {dire} has not been recorded")
        return False
    inp = results_dict[dire].input
    output = str(sub.run("python3.10 interpreter.py " + "./tests/" + dire, shell=True, input = inp, stdout=sub.PIPE, stderr=sub.STDOUT).stdout, 'utf-8')
    #print(output, results_dict[dire].output)
    if output == results_dict[dire].output:
        print(f"[INFO] {dire} passed")
        result = True
    else:
        print(f"[ERROR] {dire} failed")
        print(f"[INFO] got:\n{output}")
        print(f"[INFO] expected:\n{results_dict[dire].output}")
        result = False
    return result

def test():
    result = True
    for file in os.listdir("./tests"):
        if file.endswith(".PNL"):
            if not test_file(file):
                result = False
    return result

def record_file(dire):
    if dire in results_dict:
        inp = results_dict[dire].input
    else:
        inp = ''

    output = str(sub.run("python3.10 interpreter.py " + "./tests/" +  dire, shell=True, input = inp, stdout=sub.PIPE, stderr=sub.STDOUT).stdout, 'utf-8')

    results_dict[dire] = InputOutput(inp, output)
    print(f'[INFO] recorded {dire}')

def record():
    for file in os.listdir("./tests"):
        if file.endswith(".PNL"):
            record_file(file)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == 'record':
            try:
                with open('./tests/results.pickle', 'rb') as f:
                    results_dict = pickle.load(f)
            except:
                results_dict = {}
            record()
            with open('./tests/results.pickle', 'wb') as f:
                pickle.dump(results_dict, f)
            print('[INFO] Successfully recorded all files')
        else:
            print('[ERROR] Unrecognized command')
            exit()
    else:
        try:
            with open('./tests/results.pickle', 'rb') as f:
                results_dict = pickle.load(f)
        except FileNotFoundError:
            print("[ERROR] file not found, try to record first")
            exit()
        global all_passed
        all_passed = test()
        if all_passed:
            print('[INFO] All files passed')
        else:
            print('[ERROR] Not all files passed')
    
