# Simple parser I made because there's so many dbs with this disgusting format
# Definitely could have done this way better but I wanted to do it with a queue system

from queue import Queue
from time import time

to_parse = "database.txt"
parsed_file = f"{to_parse[:-4]}_parsed.txt"

parse_queue = Queue()


def load_queue():
    start = time()

    # Open database, Strip by line, then add to a queue
    with open(to_parse) as f:
        content = f.readlines()
        content = [x.strip() for x in content]

        [parse_queue.put(non_parsed) for non_parsed in content]

    end = time()
    print(f"[DONE] Finished adding {parse_queue.qsize()} entries to queue in {format(end - start, str(.2))} seconds!")


def parse():
    start = time()

    # Keep going while queue has more than 1 task left
    while parse_queue.qsize() > 0:
        line = parse_queue.get()
        line_splitter = line.split("|", 6)

        # Skip over any useless lags
        if line.startswith("+"):
            continue

        # Skip lines with less than 1 character
        elif len(line_splitter) > 1:
            username, uuid, ip = line_splitter[3].strip(), line_splitter[4], line_splitter[5]
            print(f"{uuid},{username},{ip}")
            open(parsed_file, "a").write(f"{uuid},{username},{ip}\n")
            continue

        # Remove task from queue after finished
        parse_queue.task_done()

    end = time()
    print(f"[DONE] Finished parsing in {format(end - start, str(.2))} seconds!")


if __name__ == "__main__":
    load_queue()
    parse()
