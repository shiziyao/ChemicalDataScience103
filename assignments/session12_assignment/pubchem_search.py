import pubchempy as pcp
import pandas as pd
from tqdm import tqdm
import time
from pathlib import Path


# Define ROOT directory (folder containing this .py file)
ROOT = Path(__file__).resolve().parent

<<<<<<< HEAD
# Define data directory
DATA = ROOT / "data"

# Create data directory if it does not exist
DATA.mkdir(parents=True, exist_ok=True)


# Load ChEMBL dataset using relative path
input_file = DATA / "coli_200_400.csv"

chembl_df = pd.read_csv(input_file)

# Extract SMILES
smiles_list = chembl_df["smiles"].dropna().tolist()
=======
# Load your ChEMBL dataset
chembl_df = pd.read_csv(DATA / "mics_raw.csv")  # use your actual filename and path
smiles_list = chembl_df["smiles"].dropna().tolist() # use the column tag with the "smiles"
>>>>>>> acd0cca796f511f6e43438ad80e2d2666207235c

records = []

# Retrieve molecular descriptors from PubChem
for smi in tqdm(smiles_list, desc="Processing compounds"):

    try:
<<<<<<< HEAD
        compounds = pcp.get_compounds(smi, namespace="smiles")

=======
        compounds = pcp.get_compounds(smi, namespace='canonical_smiles') # look for each smiles-code in the list sliced from the ChEMBL data
>>>>>>> acd0cca796f511f6e43438ad80e2d2666207235c
        if not compounds:
            continue

        c = compounds[0]

        records.append({
<<<<<<< HEAD
            "smiles": smi,
=======
            "canonical_smiles": smi, # make sure that the column name for the smiles code matches the chembl dataframe!
>>>>>>> acd0cca796f511f6e43438ad80e2d2666207235c
            "CID": c.cid,
            "MolecularWeight": c.molecular_weight,
            "XLogP": c.xlogp,
            "TPSA": c.tpsa,
            "HBondDonorCount": c.h_bond_donor_count,
            "HBondAcceptorCount": c.h_bond_acceptor_count,
            "RotatableBondCount": c.rotatable_bond_count,
            "HeavyAtomCount": c.heavy_atom_count
        })

    except Exception as e:
        print(f"Failed for {smi[:20]}...: {e}")

    # Delay to avoid flooding PubChem servers
    finally:
        time.sleep(0.2)


# Convert records into DataFrame
pubchem_df = pd.DataFrame(records)
<<<<<<< HEAD

# Save output in data folder
output_file = DATA / "antibio_pubchem_descr.csv"

pubchem_df.to_csv(output_file, index=False)

print(f"Saved {len(pubchem_df)} entries.")
print(f"Output location: {output_file}")
=======
pubchem_df.to_csv(DATA / "antibio_pubchem_descr.csv", index=False) # use your path and specified filename
print(f"Saved {len(pubchem_df)} entries.")
>>>>>>> 18281d6aa167361f4356789b09c97c8a311ff7ea
