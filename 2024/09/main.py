import sys

def main():
    disk_map = sys.stdin.readline().strip()

    # Unpack the disk map into a list of IDs in each block.
    disk = []
    for i, size in enumerate(disk_map):
        if i % 2 != 0:
            disk += [None] * int(size)
        else:
            disk += [int(i/2)] * int(size)

    # Rearrange the blocks on the disk.
    i = 0
    j = len(disk) - 1
    while i < j:
        if disk[i] != None:
            i += 1
            continue

        if disk[j] == None:
            j -= 1
            continue

        disk[i] = disk[j]
        disk[j] = None
        i += 1
        j -= 1

    checksum = 0
    for position, block_id in enumerate(disk):
        if block_id is not None:
            checksum += position * block_id

    print("[Part one] Filesystem checksum:", checksum)


if __name__ == "__main__":
    main()
