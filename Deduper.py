#!/usr/bin/env python
# coding: utf-8

# ## Imports
import hashlib
from pathlib import Path
import logging
from collections import defaultdict
from typing import List, Dict


# ## Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


# ## Functions
def hash_file(path: Path, chunk_size: int = 1024*1024) -> str:
    """Gets the hash of a file
    Inputs: path
    Output: hash
    """
    h = hashlib.sha256()
    with path.open('rb') as f:
        while chunk := f.read(chunk_size):
            h.update(chunk)
    return h.hexdigest()

def collect_files(folder:Path) -> list[Path]:
    """Collect all files in folder and subfolders
    Input: path
    Output: list of path of each file"""
    files = [p for p in folder.rglob("*") if p.is_file()]
    logger.debug(f"found {len(files)} in {folder} and its subfolders")
    return files

def find_duplicates(hash_map: Dict[str, List[Path]]) -> List[dict]:
    """Creates duplicates objct
    Inputs: hash map
    Outputs: duplicates and paths"""
    duplicates = []
    for hash, paths in hash_map.items():
        if len(paths) > 1:
            ## take earliest time as original if there are duplicates
            ##TODO: add in more handling since its not perfect.  look for '(2)' and '- copy' in filenames
            original = min(paths, key=lambda p: p.stat().st_ctime)
            duplicate_files = [p for p in paths if p!=original]
            
            duplicates.append({
                'hash': hash,
                'first_find': original,
                'size': original.stat().st_size,
                "duplicates": duplicate_files})
    return duplicates

def scan_for_duplicates(folder: Path) -> List[Dict]:
    """Scan folder and subfolders for duplicates
    Input: path
    Output: """

    files = collect_files(folder)

    hash_map = defaultdict(list)
    skipped_count = 0
    for path in files:
        try:
            file_hash = hash_file(path)
            hash_map[file_hash].append(path)
        except Exception as e:
            logger.debug(f"skipped {path}: {e}")
            skipped_count += 1
    
    if skipped_count >0:
        logger.debug(f"skipped {skipped_count} files due to errors")
    logger.debug(f"skipped {skipped_count} files due to errors")

    duplicates = find_duplicates(hash_map)

    originals_with_duplicates = len(duplicates)
    duplicates_with_originals = sum(len(entry['duplicates']) for entry in duplicates)
    logger.debug(f'{originals_with_duplicates} files have a total of {duplicates_with_originals} duplicate files')

    total_size_of_duplicates = sum(f.stat().st_size for entry in duplicates for f in entry['duplicates'])
    if total_size_of_duplicates >=1024**3:
        total_size_of_duplicates_output = f"{total_size_of_duplicates / 1024**3:.2f} GB of duplicates found"
    else:
        total_size_of_duplicates_output = f"{total_size_of_duplicates / 1024**2:.2f} MB of duplicates found"
    logger.debug(total_size_of_duplicates_output)
    
    return duplicates

def delete_duplicates(duplicates_list: List[Dict]) -> None:
    """ Deletes all duplicates found
    Inputs: duplicates list from scan_for_duplicates
    Outputs: deletes files"""

    total_files_deleted = 0
    total_size_deleted = 0
    skipped_files = 0

    for entry in duplicates_list:
        for duplicate_file in entry['duplicates']:
            try:
                size = duplicate_file.stat().st_size

                duplicate_file.unlink()
                logger.debug(f"deleted  {duplicate_file} of size {size/1024**2:.2f} MB")
                total_files_deleted += 1
                total_size_deleted += size

            except Exception as e:
                logger.debug(f"skipped {duplicate_file} with exception {e}")
                skipped_files += 1

    logger.debug(f'Deleted {total_files_deleted} files')
    if total_size_deleted >=1024**3:
        logger.debug(f"{total_size_deleted / 1024**3:.2f} GB of duplicates deleted")
    else:
        logger.debug(f"{total_size_deleted / 1024**2:.2f} MB of duplicates deleted")
    logger.debug(f' {skipped_files} files could not be deleted')