"""

    """

import math
import os
import shutil
from pathlib import Path

import zstandard as zstd


def get_half_cores() :
    """
    Return half of the available CPU cores, rounded up.
    """
    try :
        cores = os.cpu_count() or 1
    except :
        cores = 1
    return max(1 , math.ceil(cores / 2))


def compress_and_split_parallel(input_file_path ,
                                chunks_max_size_mb = 90 ,
                                remove_original = True ,
                                remove_oversized_compressed = True ,
                                threads = None
                                ) :
    """
    Compress a file using Zstandard and split it into chunks if the compressed size exceeds chunks_max_size_mb.

    Parameters:
        input_file_path (str): Path to the file to be compressed.
        chunks_max_size_mb (int): Maximum size of each chunk in MB (default: 90MB).
        remove_original (bool, optional): If True, removes the original uncompressed file after compression.
        remove_oversized_compressed (bool, optional): If True, removes the oversized compressed file after splitting.
        threads (int, optional): Number of threads to use for compression (default: half of available cores).
    """
    if threads is None :
        threads = get_half_cores()

    max_size = chunks_max_size_mb * 1024 * 1024
    input_file = Path(input_file_path)
    original_filename = input_file.name
    compressed_file = input_file.with_name(f"{original_filename}.zst")

    print(f"Compression started with {threads} threads...")

    cctx = zstd.ZstdCompressor(level = 22 , threads = threads)

    try :
        with input_file.open('rb') as f_in , compressed_file.open('wb') as f_out :
            with cctx.stream_writer(f_out) as writer :
                while True :
                    chunk = f_in.read(1 * 1024 * 1024)  # Read in 1MB chunks
                    if not chunk :
                        break
                    writer.write(chunk)
    except Exception as e :
        compressed_file.unlink(missing_ok = True)
        raise RuntimeError(f"Compression failed: {e}")

    print("\nCompression done.")
    print(f"Output file: {compressed_file}")

    if remove_original :
        input_file.unlink(missing_ok = True)
        print(f"Original file '{input_file}' removed.")

    compressed_size = compressed_file.stat().st_size
    if compressed_size > max_size :
        print(f"Compressed size ({compressed_size / (1024 * 1024):.2f} MB) exceeds max size ({chunks_max_size_mb} MB). Splitting...")
        print(f"Splitting into chunks with max size {chunks_max_size_mb} MB...")

        parts_dir = compressed_file.with_name(f"{compressed_file.name}_parts")
        parts_dir.mkdir(exist_ok = True)

        part_num = 0
        try :
            with compressed_file.open('rb') as f_in :
                while True :
                    chunk = f_in.read(max_size)
                    if not chunk :
                        break
                    part_num += 1
                    part_file = parts_dir / f"{compressed_file.name}_part_{part_num:02d}"
                    part_file.write_bytes(chunk)
                    print(f"Created part {part_num}: {part_file} ({len(chunk) / (1024 * 1024):.2f} MB)")
        except Exception as e :
            shutil.rmtree(parts_dir)
            raise RuntimeError(f"Splitting failed: {e}")

        print(f"\nCompressed File split into {part_num} parts in directory: {parts_dir}")

        if remove_oversized_compressed :
            compressed_file.unlink(missing_ok = True)
            print(f"Oversized compressed file '{compressed_file}' removed.")
    else :
        print(f"Compressed file size ({compressed_size / (1024 * 1024):.2f} MB) is within the limit ({chunks_max_size_mb} MB).")


def decompress_and_combine_parallel(input_path ,
                                    remove_original = True ,
                                    threads = None
                                    ) :
    """
    Decompress a compressed file or, if given a parts directory, combine the parts into a .zst file and decompress it.

    If input_path is a directory, the function assumes it contains split parts named like "part_*.zst". It combines
    these parts (in sorted order) into a single compressed file (with a .zst suffix) and then recursively calls itself
    to decompress that file.

    If input_path is a file, the file is decompressed using a streaming decompressor.

    Parameters:
      input_path (str or Path): Path to the compressed file or directory containing parts.
      remove_original (bool, optional): If True, removes the original compressed file after decompression, or
                                        removes the parts directory and the oversized compressed file.
      threads (int, optional): Number of threads for parallel decompression (unused in this version).

    Returns:
      None. The decompressed file is written to disk.

    Example:
      decompress_and_combine_parallel("myfile.zst")
      decompress_and_combine_parallel("myfile_parts/")
    """
    if threads is None :
        threads = get_half_cores()

    input_path = Path(input_path)

    if input_path.is_dir() :
        # Combine parts into a single .zst file.
        combined_file = input_path.parent / (
                input_path.name.replace('_parts' , '') + '')
        parts = sorted(input_path.glob('*_part_*'))
        total_parts = len(parts)
        print(f"Found {total_parts} parts. Combining into {combined_file} ...")

        for idx , part in enumerate(parts , 1) :
            data = part.read_bytes()
            with open(combined_file , 'ab') as f_out :
                f_out.write(data)
            progress = (idx / total_parts) * 100
            print(f"Combining part {idx}/{total_parts} ({progress:.1f}%)")

        print(f"Combined file size: {combined_file.stat().st_size / (1024 * 1024):.2f} MB")
        print(f"Combined file created: {combined_file}")
        print("Decompressing combined file...\n")

        if remove_original :
            shutil.rmtree(input_path , ignore_errors = True)
            print(f"Removed parts directory '{input_path}' after decompression.")

        # Recursively call self on the combined file.
        decompress_and_combine_parallel(combined_file ,
                                        remove_original = remove_original ,
                                        threads = threads)

        return

    else :
        # Input is a file; decompress it.
        output_file = input_path.with_suffix('')
        print(f"Decompressing file: {input_path}")

        dctx = zstd.ZstdDecompressor()
        with open(input_path , 'rb') as f_in , open(output_file ,
                                                    'wb') as f_out :
            with dctx.stream_reader(f_in) as reader :
                shutil.copyfileobj(reader , f_out)

        output_size = output_file.stat().st_size
        print("Decompression done.")
        print(f"Final file size: {output_size / (1024 * 1024):.2f} MB")
        print(f"Output file: {output_file}")

        if remove_original :
            input_path.unlink(missing_ok = True)
            print(f"Removed original compressed file '{input_path}' after decompression.")
