import pygame
from Setings import SCREEN_WIDTH, SCREEN_HEIGHT, BG, TEXT_COL, FONT_SIZE

pygame.init()

# create game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Text Input")


# define font
font = pygame.font.SysFont("Futura", FONT_SIZE)

# create empty string
text = [""]


# function for outputting text onto the screen
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x + (FONT_SIZE // 2) * 1.5, y))


def draw_line_numbers(line_no, font, text_col, x, y):
    img = font.render(str(line_no) + ". ", True, text_col)
    screen.blit(img, (x, y))


line_no = 0
pos_no = 0

# game loop
run = True
while run:

    # update background
    screen.fill(BG)

    # display typed input
    for row, line in enumerate(text):
        draw_line_numbers(row, font, TEXT_COL, 0, row * FONT_SIZE)
        draw_text(line, font, TEXT_COL, 0, row * FONT_SIZE)

    # event handler
    for event in pygame.event.get():
        # handle text input
        if event.type == pygame.TEXTINPUT:
            text[line_no] = text[line_no][:pos_no] + event.text + text[line_no][pos_no:]
            pos_no += len(event.text)

        # handle special keys
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                if pos_no > 0:
                    text[line_no] = text[line_no][: pos_no - 1] + text[line_no][pos_no:]
                    pos_no -= 1
                elif line_no > 0:
                    pos_no = len(text[line_no - 1])
                    text[line_no - 1] += text[line_no]
                    text.pop(line_no)
                    line_no -= 1
            elif event.key == pygame.K_DELETE:
                if pos_no < len(text[line_no]):
                    text[line_no] = text[line_no][:pos_no] + text[line_no][pos_no + 1 :]
                elif line_no < len(text) - 1:
                    text[line_no] += text[line_no + 1]
                    text.pop(line_no + 1)
            elif event.key == pygame.K_RETURN:
                text.insert(line_no + 1, text[line_no][pos_no:])
                text[line_no] = text[line_no][:pos_no]
                line_no += 1
                pos_no = 0
            elif event.key == pygame.K_LEFT:
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
        if event.type == pygame.QUIT:
            run = False

    # calculate the x position of the cursor
    x = font.size(text[line_no][:pos_no])[0] + (FONT_SIZE // 2) * 1.5
    # calculate the y position of the cursor
    y = line_no * FONT_SIZE
    # create a pygame Rect at (x, y, 2, FONT_SIZE)
    cursor_rect = pygame.Rect(x, y, 2, FONT_SIZE)
    # fill the Rect with a color
    pygame.draw.rect(screen, TEXT_COL, cursor_rect)

    # update display
    pygame.display.flip()

pygame.quit()
