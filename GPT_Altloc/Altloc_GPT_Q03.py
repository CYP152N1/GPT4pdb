import sys

def process_pdb_file(input_filename, output_filename, specified_char=None, replace_17th_char=False):
    with open(input_filename, "r") as input_file:
        lines = input_file.readlines()

    filtered_lines = []
    for line in lines:
        if line[:4] == "ATOM":
            if len(line) >= 17:
                if specified_char is None:
                    if line[16] == " ":
                        if replace_17th_char:
                            filtered_lines.append(line[:16] + " " + line[17:])
                        else:
                            filtered_lines.append(line)
                    elif line[16] == "A":
                        if replace_17th_char:
                            filtered_lines.append(line[:16] + " " + line[17:])
                        else:
                            filtered_lines.append(line)
                else:
                    if line[16] == specified_char:
                        if replace_17th_char:
                            filtered_lines.append(line[:16] + " " + line[17:])
                        else:
                            filtered_lines.append(line)
                    elif line[16] == " ":
                        if replace_17th_char:
                            filtered_lines.append(line[:16] + " " + line[17:])
                        else:
                            filtered_lines.append(line)
            else:
                filtered_lines.append(line)
        elif line[:6] == "HETATM":
            filtered_lines.append(line)

    write_pdb(filtered_lines, output_filename)

def write_pdb(lines, output_filename):
    with open(output_filename, "w") as output_file:
        for line in lines:
            output_file.write(line)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python script.py <input_pdb_file> <output_pdb_file> [specified_char] [replace_17th_char]")
        sys.exit(1)

    input_filename = sys.argv[1]
    output_filename = sys.argv[2]
    specified_char = None
    replace_17th_char = False

    if len(sys.argv) >= 4:
        specified_char = sys.argv[3]
    if len(sys.argv) == 5:
        replace_17th_char = bool(int(sys.argv[4]))

    process_pdb_file(input_filename, output_filename, specified_char, replace_17th_char)
