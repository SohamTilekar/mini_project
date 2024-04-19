import pygame
from Settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    BG,
    TEXT_COL,
    FONT_SIZE,
    LINE_NO_COL,
    TAB_SPACING,
)
from tkinter import Tk, filedialog


def draw_text(text, font, text_col, x, y, text_canvas):
    img = font.render(text, True, text_col)
    text_canvas.blit(img, (x + FONT_SIZE * 1.6, y))


def draw_line_numbers(line_no, font, x, y, text_canvas):
    line_number = str(line_no + 1)
    padding = " " * round(8 - len(line_number) * 2.5)
    img = font.render(padding + line_number + ". ", True, LINE_NO_COL)
    text_canvas.blit(img, (x, y))


def open_file_dialog():
    root = Tk()
    root.withdraw()
    filename = filedialog.askopenfilename()
    root.destroy()
    return filename


def handle_text_input(event, text, line_no, pos_no):
    text[line_no] = text[line_no][:pos_no] + event.text + text[line_no][pos_no:]
    pos_no += len(event.text)
    return text, pos_no


def handle_backspace(text, line_no, pos_no):
    if pos_no > 0:
        text[line_no] = text[line_no][: pos_no - 1] + text[line_no][pos_no:]
        pos_no -= 1
    elif line_no > 0:
        pos_no = len(text[line_no - 1])
        text[line_no - 1] += text[line_no]
        text.pop(line_no)
        line_no -= 1
    return text, line_no, pos_no


def handle_delete(text, line_no, pos_no):
    if pos_no < len(text[line_no]):
        text[line_no] = text[line_no][:pos_no] + text[line_no][pos_no + 1 :]
    elif line_no < len(text) - 1:
        text[line_no] += text[line_no + 1]
        text.pop(line_no + 1)
    return text


def handle_enter(text, line_no, pos_no):
    text.insert(line_no + 1, text[line_no][pos_no:])
    text[line_no] = text[line_no][:pos_no]
    line_no += 1
    pos_no = 0
    return text, line_no, pos_no


def handle_arrow_keys(event, line_no, pos_no, text):
    if event.key == pygame.K_LEFT:
        if pos_no > 0:
            pos_no -= 1
    elif event.key == pygame.K_RIGHT:
        if pos_no < len(text[line_no]):
            pos_no += 1
    elif event.key == pygame.K_UP:
        if line_no > 0:
            line_no -= 1
            if pos_no > len(text[line_no]):
                pos_no = len(text[line_no])
    elif event.key == pygame.K_DOWN:
        if line_no < len(text) - 1:
            line_no += 1
            if pos_no > len(text[line_no]):
                pos_no = len(text[line_no])
    return line_no, pos_no


def calculate_canvas_y(y, canvas_y) -> int:
    if 0 < y <= SCREEN_HEIGHT:
        ...
    elif y >= SCREEN_HEIGHT:
        canvas_y = SCREEN_HEIGHT - y - FONT_SIZE
    else:
        canvas_y = 0 - y

    return canvas_y


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Text Input")
    font = pygame.font.SysFont("Futura", FONT_SIZE)
    text = [""]
    filename = ""
    line_no = 0
    pos_no = 0
    canvas_y = 0
    run = True

    while run:
        # screen.fill(BG)
        bg_rect = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
        pygame.draw.rect(screen, BG, bg_rect)
        text_canvas = pygame.Surface((SCREEN_WIDTH, len(text) * FONT_SIZE))
        text_canvas.fill(BG)

        x = font.size(text[line_no][:pos_no])[0] + (FONT_SIZE) * 1.6
        y = line_no * FONT_SIZE
        cursor_rect = pygame.Rect(x, y, 2, FONT_SIZE)
        pygame.draw.rect(text_canvas, TEXT_COL, cursor_rect)

        for row, line in enumerate(text):
            draw_line_numbers(row, font, 0, row * FONT_SIZE, text_canvas)
            draw_text(line, font, TEXT_COL, 0, row * FONT_SIZE, text_canvas)

        for event in pygame.event.get():
            if event.type == pygame.TEXTINPUT:
                text, pos_no = handle_text_input(event, text, line_no, pos_no)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_o and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    filename = open_file_dialog()
                    if filename:
                        try:
                            with open(filename, "r") as file:
                                text = file.read().split("\n")
                                line_no = len(text) - 1
                                pos_no = 0
                            canvas_y = calculate_canvas_y(line_no * FONT_SIZE, canvas_y)
                        except IOError:
                            print("Error: Could not open file")
                if event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    if filename:
                        with open(filename, "w") as file:
                            file.write("\n".join(text))
                    else:
                        filename = filedialog.asksaveasfilename()
                        if filename:
                            with open(filename, "w") as file:
                                file.write("\n".join(text))
                # Save as using ctrl + shift +s
                if event.key == pygame.K_s and (
                    pygame.key.get_mods() & pygame.KMOD_CTRL
                    and pygame.key.get_mods() & pygame.KMOD_SHIFT
                ):
                    filename = filedialog.asksaveasfilename()
                    if filename:
                        with open(filename, "w") as file:
                            file.write("\n".join(text))
                if event.key == pygame.K_TAB:
                    text[line_no] = (
                        text[line_no][:pos_no]
                        + (" " * TAB_SPACING)
                        + text[line_no][pos_no:]
                    )
                    pos_no += 1 * TAB_SPACING
                elif event.key == pygame.K_BACKSPACE:
                    text, line_no, pos_no = handle_backspace(text, line_no, pos_no)
                    canvas_y = calculate_canvas_y(line_no * FONT_SIZE, canvas_y)
                elif event.key == pygame.K_DELETE:
                    text = handle_delete(text, line_no, pos_no)
                    canvas_y = calculate_canvas_y(line_no * FONT_SIZE, canvas_y)
                elif event.key == pygame.K_RETURN:
                    text, line_no, pos_no = handle_enter(text, line_no, pos_no)
                    canvas_y = calculate_canvas_y(line_no * FONT_SIZE, canvas_y)
                else:
                    line_no, pos_no = handle_arrow_keys(event, line_no, pos_no, text)
                    canvas_y = calculate_canvas_y(line_no * FONT_SIZE, canvas_y)
            elif event.type == pygame.QUIT:
                run = False

        screen.blit(text_canvas, (0, canvas_y))

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
