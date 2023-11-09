import argparse
import os
import sys
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from synthetic_knowledge_graphs import UserItemAttrDataset

# Step 2: Define command-line arguments
parser = argparse.ArgumentParser(
    description="Generate and save the UserItemAttr dataset."
)

parser.add_argument(
    "--num_attrs",
    type=int,
    default=10,
    help="Number of attributes in the dataset",
)
parser.add_argument(
    "--num_items",
    type=int,
    default=100,
    help="Number of items in the dataset",
)
parser.add_argument(
    "--num_users",
    type=int,
    default=50,
    help="Number of users in the dataset",
)
parser.add_argument(
    "--lambda_a",
    type=float,
    default=0.0,
    help="The average number of attributes that an item possesses.",
)
parser.add_argument(
    "--lambda_i",
    type=float,
    default=3.0,
    help="The average number of items that a user has bought.",
)
parser.add_argument(
    "--percentages",
    nargs="+",
    type=float,
    default=[0.8, 0.2],
    help="Train/Valid/Test split percentages",
)
parser.add_argument("--seed", type=int, default=0, help="Random seed")
parser.add_argument("--name", type=str, default="FTREE", help="Name for the dataset")
parser.add_argument(
    "--only_train", action="store_true", help="Save only training triples"
)
args = parser.parse_args()

# Step 3: Create an instance of FTREEDataset with provided arguments
dataset = UserItemAttrDataset(
    num_attrs=args.num_attrs,
    num_items=args.num_items,
    num_users=args.num_users,
    lambda_a=args.lambda_a,
    lambda_i=args.lambda_i,
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
