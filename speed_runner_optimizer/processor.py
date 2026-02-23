import pandas as pd

def read_file_generator(file_path, chunk_size=1000):
    """Generator to read CSV in chunks"""
    for chunk in pd.read_csv(file_path, chunksize=chunk_size):
        yield chunk

def process_file(file_path):
    """Process one file"""
    total = 0
    count = 0

    try:
        for chunk in read_file_generator(file_path):
            total += chunk["marks"].sum()
            count += len(chunk)

        avg = total / count if count else 0
        return avg

    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return 0