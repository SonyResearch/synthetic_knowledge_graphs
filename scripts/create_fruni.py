import argparse
import os
import sys
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from synthetic_knowledge_graphs import FRUNIDataset

# Step 2: Define command-line arguments
parser = argparse.ArgumentParser(description="Generate and save the FRUNI dataset.")
parser.add_argument(
    "--n_u", type=int, required=True, help="Number of universities in the dataset."
)
parser.add_argument(
    "--lambda_f",
    type=float,
    required=True,
    help=" Average number of friends per student",
)
parser.add_argument(
    "--alpha_u",
    type=float,
    required=True,
    help="Probability of collaborative relationships between universities",
)
parser.add_argument(
    "--n_f",
    type=int,
    required=True,
    help="Number of universities that foster friendship.",
)
parser.add_argument(
    "--percentages",
    nargs="+",
    type=float,
    default=[0.8, 0.2],
    help="Train/Valid/Test split percentages",
)
parser.add_argument("--seed", type=int, default=0, help="Random seed")
parser.add_argument("--name", type=str, default="FRUNI", help="Name for the dataset")
parser.add_argument(
    "--only_train", action="store_true", help="Save only training triples"
)
args = parser.parse_args()

# Step 3: Create an instance of FTREEDataset with provided arguments
dataset = FRUNIDataset(
    n_u=args.n_u,
    lambda_f=args.lambda_f,
    alpha_u=args.alpha_u,
    n_f=args.n_f,
    percentages=args.percentages,
    seed=args.seed,
)

# Step 4: Generate a unique hash for the dataset (if needed)
my_hash = dataset.get_hash()

# Step 5: Create a folder for saving the dataset
if args.name == "":
    folder = os.path.join("data", my_hash)
else:
    folder = os.path.join("data", args.name)

# Step 6: Save the dataset and optionally save triples
dataset.save(root=folder)
dataset.save_triples(
    root=folder,
    only_train=args.only_train,
    use_hash=True if args.name == "" else False,
    save_random_test_triples=50,
)

# Step 7: Get the current timestamp in a human-readable format
now = datetime.now()
timestamp = now.strftime("%Y%m%d_%H%M%S")

# Step 8: Print the hash and timestamp
print(f"Hash: {my_hash}")
print(f"Timestamp: {timestamp}")
