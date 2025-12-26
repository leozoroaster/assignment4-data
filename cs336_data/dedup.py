from pathlib import Path
import hashlib

def hash_line(line: str) -> str:
    return hashlib.sha256(line.encode("utf-8")).hexdigest()

def exact_deduplication(list_of_paths, output_dic):
    filenames=[]
    new_files=[]
    hash2count = dict()

    for path in list_of_paths:
        filename=Path(path).name
        filenames.append(filename)

        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line=line.rstrip("\r\n")
                hashed_line = hash_line(line)
                if hashed_line not in hash2count:
                    hash2count[hashed_line] = 1
                else:
                    hash2count[hashed_line] += 1

    for path in list_of_paths:
        new_lines = []

        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.rstrip("\r\n")
                hashed_line = hash_line(line)
                if hash2count[hashed_line]==1:
                    new_lines.append(line)

        new_files.append(new_lines)

    for i in range(len(filenames)):
        new_name=filenames[i]
        new_lines=new_files[i]
        new_path = Path(output_dic) / new_name
        print(new_path)
        with open(new_path, "w", encoding="utf-8") as f:
            for line in new_lines:
                f.write(line + "\n")

