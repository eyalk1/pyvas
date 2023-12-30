import pygame.sprite
import pygame.draw
import pygame.font

# from consts import SLACK, CODE_HEADER_COLOR

# TODO: import this lol wtf
SLACK = 5
CODE_HEADER_COLOR = pygame.color.Color(0, 0, 0)


class Block:
    def __init__(self, header: str, body: str, size: int = 40):
        self.header = header
        self.body = body
        self.header_font = pygame.font.SysFont("arial", size)
        self.body_font = pygame.font.SysFont("arial", size // 2)
        self.header_rendered = self.header_font.render(header, True, CODE_HEADER_COLOR)
        self.body_rendered = [
            self.body_font.render(line, True, CODE_HEADER_COLOR)
            for line in self.body.split("\n")
        ]
        self.color = pygame.color.Color(0, 0, 0)
        self.thickness = 1

        self.rect_surf: pygame.Surface = self._calculate_rect()
        self.rect_pos: tuple[int] = [0, 0]

    def draw(self, screen: pygame.Surface):
        header_top = self.rect_pos[1] + SLACK
        text_left = self.rect_pos[0] + SLACK
        body_top = header_top + self.header_rendered.get_height() + SLACK

        screen.blit(self.header_rendered, (text_left, header_top))

        for idx, rendered_line in enumerate(self.body_rendered):
            screen.blit(
                rendered_line,
                (
                    text_left,
                    body_top + rendered_line.get_height() * idx,
                ),
            )

        screen.blit(self.rect_surf, self.rect_pos)
        pygame.draw.rect(screen, self.color, self.rect, self.thickness)

    @property
    def rect(self):
        return pygame.Rect(*self.rect_pos, *self.rect_surf.get_size())

    def setPosition(self, top, left):
        self.move(top - self.rect_pos[0], left - self.rect_pos[1])

    def move(self, top, left):
        print(self.rect_pos)
        self.rect_pos[0] += top
        self.rect_pos[1] += left

    def decorate(
        self, *, highlight: bool = None, hover: bool = None, select: bool = None
    ):
        if highlight is not None:
            if highlight:
                self.color = pygame.color.Color(255, 0, 0)
            else:
                self.color = pygame.color.Color(0, 0, 0)

        if hover is not None:
            if hover:
                self.rect_surf.set_alpha(120)
            else:
                self.rect_surf.set_alpha(0)

        if select is not None:
            if select:
                self.thickness = 5
            else:
                self.thickness = 1

    def _calculate_rect(self) -> pygame.Rect:
        header_width, header_height = self.header_rendered.get_size()

        # the longest line is the width of the rect,
        # the height of all the lines is the height of the rect
        widths_heights = list(map(lambda x: x.get_size(), self.body_rendered))
        body_width = max(map(lambda x: x[0], widths_heights))
        body_height = sum(map(lambda x: x[1], widths_heights))

        width = max(header_width, body_width) + 2 * SLACK
        height = header_height + body_height + 2 * SLACK

        ret = pygame.Surface((width, height))
        ret.fill(self.color)
        ret.set_alpha(50)

        return ret
