# Below Import is Only Required for Printing Beautifuly Using Rich Module
# from rich import print


def read_file(file_name: str):
    """
    Read a file containing cloth types, styles, and pieces information.

    Args:
        file_name (str): The path to the file to be read.

    Returns:
        tuple: A tuple containing the following information:
            - number_of_cloth_types (int): The number of cloth types.
            - number_of_styles (int): The number of styles.
            - compatible (dict[str, list[str]]): A dictionary mapping cloth types to compatible styles and vice versa.
            - pieces (list[list[str, int]]): A list of pieces, where each piece is represented as a list containing the cloth type and the number of pieces.

    """
    number_of_cloth_types: int
    number_of_styles: int
    with open(file_name, "r") as file:
        number_of_cloth_types, number_of_styles = [
            int(x) for x in file.readline().split()
        ]

        compatible: dict[str, list[str]] = {}

        for line in file:
            if line in ("\n", ""):
                break
            cloth_type, styles = line.split()
            compatible[cloth_type] = compatible.get(cloth_type, []) + [styles]
            compatible[styles] = compatible.get(styles, []) + [cloth_type]

        pieces = []

        for line in file:
            pieces.append(line.split())
            pieces[-1][-1] = int(pieces[-1][-1])

    return number_of_cloth_types, number_of_styles, compatible, pieces


def get_remaining_cloth(pieces):
    remaining_cloth = []
    for piec in pieces:
        if piec[-1] != 0:
            remaining_cloth.append(piec)
    return remaining_cloth


def process_piece(piece, remaining_cloth, compatible, box, cod):
    for idx1, pcd in enumerate(remaining_cloth):
        if pcd[-1] == 0:
            continue
        if piece[1] in compatible[pcd[1]]:
            count = 0
            for itm in box:
                if itm[0] == pcd[0]:
                    count += 1
            if count < 3:
                box.append(pcd[:-1])
                cod.append(idx1)
                pcd[-1] -= 1
    return box, cod


def pack_box(
    number_of_cloth_types: int,
    number_of_styles: int,
    compatible: dict[str, list],
    pieces: list[list],
):
    """
    Pack the given pieces of cloth into boxes based on certain criteria.

    Args:
        number_of_cloth_types (int): The total number of cloth types.
        number_of_styles (int): The total number of styles.
        compatible (dict[str, list]): A dictionary containing compatibility information between cloth types.
            The keys represent the cloth types, and the values are lists of compatible cloth types.
        pieces (list[list]): A list of pieces of cloth to be packed into boxes.
            Each piece is represented as a list, where the last element represents the quantity of that piece.

    Returns:
        tuple[list[list], list]: A tuple containing two elements:
            - boxes (list[list]): A list of boxes, where each box is represented as a list of cloth pieces.
            - remaining_cloth (list): A list of remaining cloth pieces that could not be packed into boxes.
    """

    boxes = []

    remaining_cloth = get_remaining_cloth(pieces)

    last_iteration = []
    while remaining_cloth != last_iteration:
        last_iteration = remaining_cloth
        for idx, piece in enumerate(remaining_cloth):
            if piece[-1] == 0:
                continue
            box = []
            cod: list[int] = []
            box.append(piece[:-1])
            piece[-1] -= 1
            cod.append(idx)
            box, cod = process_piece(piece, remaining_cloth, compatible, box, cod)
            box, cod = process_piece(piece, remaining_cloth, compatible, box, cod)
            box, cod = process_piece(piece, remaining_cloth, compatible, box, cod)
            if len(box) >= number_of_cloth_types:
                boxes.append(box)
            else:
                for c in cod:
                    remaining_cloth[c][-1] += 1

        remaining_cloth = get_remaining_cloth(pieces)

    return boxes, remaining_cloth


def main(PATH_TO_FILE):
    return read_file(PATH_TO_FILE), pack_box(*read_file(PATH_TO_FILE))


if __name__ == "__main__":
    x = main(r"d:\soham_code\vidiopy\dump\input.txt")
    print("Data: -", end=" ")
    print(x)
    y = 0
    for i in x[1][0]:
        y += len(i)
    print("Items Which Are Packed: -", end=" ")
    print(y)
    o = 0
    for i in x[1][1]:
        y += i[2]
        o += i[2]
    print("Items Which Are Remain: -", end=" ")
    print(o)
    print("Total Items: -", end=" ")
    print(y)
