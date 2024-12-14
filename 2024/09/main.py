import sys

class Disk:
    blocks: list[int | None]

    def __init__(self, disk_map: str):
        self.blocks = []
        for i, size in enumerate(disk_map):
            if i % 2 != 0:
                self.blocks += [None] * int(size)
            else:
                self.blocks += [int(i/2)] * int(size)

    def __iter__(self):
        return self.blocks.__iter__()

    def __getitem__(self, index: int) -> int | None:
        return self.blocks[index]

    def __setitem__(self, index: int, value: int | None) -> None:
        self.blocks[index] = value

    def __len__(self) -> int:
        return len(self.blocks)

    def move(self, src: int, dest: int, size: int) -> None:
        for i in range(size):
            self.blocks[dest + i] = self.blocks[src + i]
            self.blocks[src + i] = None

    def checksum(self) -> int:
        checksum = 0
        for position, file_id in enumerate(self.blocks):
            if file_id is not None:
                checksum += position * file_id
        return checksum

    def gaps(self) -> list[range]:
        gaps = []
        gap_start = None
        for i, block in enumerate(self.blocks):
            # We have reached the start of a gap.
            if block is None and gap_start is None:
                gap_start = i
            # We have reached the end of a gap.
            elif block is not None and gap_start is not None:
                gaps.append(range(gap_start, i))
                gap_start = None

        # Check if there is a final gap at the end of the disk.
        if gap_start is not None:
            gaps.append(range(gap_start, len(self.blocks)))

        return gaps

    def files(self) -> list["File"]:
        files = []
        file = None
        for i, id in enumerate(self.blocks):
            if file is None:
                # Skip all null values if we haven't yet found a file.
                if id is None:
                    continue
                file = File(i, 1, id)
            else:
                # If we just finished looping through a set of blocks from the same
                # file.
                if id != file.id:
                    # Move the blocks into the gap, as long as it will fit.
                    files.append(file)

                    if id is not None:
                        # Create a new file if both files are lined up with no gap.
                        file = File(i, 1, id)
                    else:
                        file = None
                else:
                    file.size += 1

        # Check if there is a final file at the end of the disk.
        if file is not None:
            files.append(file)

        return files


class File:
    position: int
    size: int
    id: int

    def __init__(self, position: int, size: int, id: int) -> None:
        self.position = position
        self.size = size
        self.id = id

    def move(self, disk: Disk, target: int) -> None:
        disk.move(self.position, target, self.size)


def main():
    disk_map = sys.stdin.readline().strip()

    # Rearrange the blocks on the disk.
    disk = Disk(disk_map)
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

    print("[Part one] Filesystem checksum:", disk.checksum())

    disk = Disk(disk_map)
    gaps = list(reversed(disk.gaps()))
    while gaps:
        gap = gaps.pop()

        files = reversed(disk.files())
        for file in files:
            # Skip all files the start before the end of this gap.
            if file.position < gap.stop:
                break
            # The file will fit into the gap with room to spare. The remaining
            # room can be used as a future gap.
            elif file.size < len(gap):
                file.move(disk, gap.start)
                gaps.append(range(gap.start + file.size, gap.stop))
                break
            # The file will fit into the gap exactly.
            elif file.size == len(gap):
                file.move(disk, gap.start)
                break

    print("[Part two] Filesystem checksum:", disk.checksum())


if __name__ == "__main__":
    main()
