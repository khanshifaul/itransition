import glob
import hashlib
import os


# Function to compute SHA3-256 hash of a file
def compute_sha3_256(file_path):
    sha3_256 = hashlib.sha3_256()
    with open(file_path, "rb") as file:
        while chunk := file.read(8192):
            sha3_256.update(chunk)
    return sha3_256.hexdigest()


# Directory containing the extracted files
directory = r"D:\Github\itransition\task2"  # Replace with your actual directory path

# List to store all hash values
hash_values = []

# Iterate over all files in the directory and compute their SHA3-256 hash
for file_path in glob.glob(os.path.join(directory, "*")):
    hash_value = compute_sha3_256(file_path)
    hash_values.append(hash_value)

# Sort hashes in ascending order
hash_values.sort()
print(hash_values)
print("\n\n")
# Concatenate sorted hashes without any separator
sorted_hashes = "".join(hash_values)
print(sorted_hashes)
print("\n\n")

# Your email address (replace with your actual email)
email = "khanshifaul@gmail.com"

# Concatenate sorted hashes with email
concatenated_string = sorted_hashes + email.lower()

# Compute SHA3-256 hash of the concatenated string
final_hash = hashlib.sha3_256(concatenated_string.encode()).hexdigest()

# Print the final 64 hex digits in lowercase
print(final_hash)
