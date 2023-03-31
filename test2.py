import os
import sys
import time
import random
import string
import re
import argparse

# Add the directory containing the 'inference' module to the Python path
rf_diffusion_path = os.path.abspath("RFdiffusion")
if rf_diffusion_path not in sys.path:
    sys.path.append(rf_diffusion_path)

from colabdesign.rf.utils import fix_contigs, fix_partial_contigs, fix_pdb
from inference.utils import parse_pdb

def get_pdb(pdb_path=None):
    if pdb_path is None or pdb_path == "":
        print("Please provide a PDB file path.")
        return None
    elif os.path.isfile(pdb_path):
        return pdb_path
    elif len(pdb_path) == 4:
        os.system(f"wget -qnc https://files.rcsb.org/view/{pdb_path}.pdb")
        return f"{pdb_path}.pdb"
    else:
        os.system(f"wget -qnc https://alphafold.ebi.ac.uk/files/AF-{pdb_path}-F1-model_v3.pdb")
        return f"AF-{pdb_path}-F1-model_v3.pdb"

def run_diffusion(contigs, path, pdb=None, iterations=50,
                  symmetry="cyclic", copies=1, hotspot=None):
  # determine mode
  contigs = contigs.replace(","," ").replace(":"," ").split()
  is_fixed, is_free = False, False
  for contig in contigs:
    for x in contig.split("/"):
      a = x.split("-")[0]
      if a[0].isalpha():
        is_fixed = True
      if a.isnumeric():
        is_free = True
  if len(contigs) == 0 or not is_free:
    mode = "partial"
  elif is_fixed:
    mode = "fixed"
  else:
    mode = "free"

  # fix input contigs
  if mode in ["partial","fixed"]:
    pdb_filename = get_pdb(pdb)
    parsed_pdb = parse_pdb(pdb_filename)
    opts = f" inference.input_pdb={pdb_filename}"
    if mode in ["partial"]:
      partial_T = int(80 * (iterations / 200))
      opts += f" diffuser.partial_T={partial_T}"
      contigs = fix_partial_contigs(contigs, parsed_pdb)
    else:
      opts += f" diffuser.T={iterations}"
      contigs = fix_contigs(contigs, parsed_pdb)
  else:
    opts = f" diffuser.T={iterations}"
    parsed_pdb = None  
    contigs = fix_contigs(contigs, parsed_pdb)

  if hotspot is not None and hotspot != "":
    opts += f" ppi.hotspot_res=[{hotspot}]"

  # setup symmetry
  if copies > 1:
    sym = {"cyclic":"c","dihedral":"d"}[symmetry] + str(copies)
    sym_opts = f"--config-name symmetry  inference.symmetry={sym} \
    'potentials.guiding_potentials=[\"type:olig_contacts,weight_intra:1,weight_inter:0.1\"]' \
    potentials.olig_intra_all=True potentials.olig_inter_all=True \
    potentials.guide_scale=2 potentials.guide_decay=quadratic"
    opts = f"{sym_opts} {opts}"
    if symmetry == "dihedral": copies *= 2
    contigs = sum([contigs] * copies,[])

  opts = f"{opts} 'contigmap.contigs=[{' '.join(contigs)}]'"

  print("mode:", mode)
  print("output:", f"outputs/{path}")
  print("contigs:", contigs)

  cmd = f"./RFdiffusion/run_inference.py {opts} inference.output_prefix=outputs/{path} inference.num_designs=1"
  print(cmd)
  return contigs, copies

def main():
    parser = argparse.ArgumentParser(description="Run RFdiffusion with specified arguments.")
    parser.add_argument("--contigs", type=str, required=True, help="Contigs for the run_diffusion function")
    parser.add_argument("--path", type=str, required=True, help="Path for the run_diffusion function")
    parser.add_argument("--pdb", type=str, help="PDB file path")
    parser.add_argument("--iterations", type=int, default=50, help="Number of iterations for the run_diffusion function")
    parser.add_argument("--symmetry", type=str, default="cyclic", choices=["cyclic", "dihedral"], help="Symmetry for the run_diffusion function")
    parser.add_argument("--copies", type=int, default=1, help="Number of copies for the run_diffusion function")
    parser.add_argument("--hotspot", type=str, help="Hotspot for the run_diffusion function")

    args = parser.parse_args()

    contigs, copies = run_diffusion(args.contigs, args.path, pdb=args.pdb, iterations=args.iterations,
                                    symmetry=args.symmetry, copies=args.copies, hotspot=args.hotspot)
    print("contigs:", contigs)
    print("copies:", copies)

if __name__ == "__main__":
    main()
