import sys
import argparse

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
    parser = argparse.ArgumentParser(description="Process a PDB file and apply filters based on the 17th character.")
    parser.add_argument("input_pdb_file", help="Path to the input PDB file.")
    parser.add_argument("output_pdb_file", help="Path to the output PDB file.")
    parser.add_argument("-s", "--specified_char", help="The specified character to filter on.")
    parser.add_argument("-r", "--replace_17th_char", action="store_true", help="Replace the 17th character with a space.")

    args = parser.parse_args()

    process_pdb_file(args.input_pdb_file, args.output_pdb_file, args.specified_char, args.replace_17th_char)
