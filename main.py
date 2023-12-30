import pygame
import Canvas
import event as CEvent

BODIES = ["a + b = c;\neyal is king", "suckmycock\nnigga"]
HEADERS = ["FUcn number 1", "function secondus"]


def main():
    pygame.init()
    screen = pygame.display.set_mode([500, 500])
    screen.fill((70, 70, 70))
    can = Canvas.Canvas()
    running = True

    while running:
        # Did the user click the Block close button?
        for event in pygame.event.get():
            # gather events
            cevent: CEvent.Event = can.parseEvent(event)
            # distribute events
            can.handleEvent(cevent)
            # if event.type == pygame.QUIT:
            #     running = False
            # elif event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_RETURN:
            #         wm.newBlock(HEADERS[i % 2], BODIES[i % 3 % 2])
            #         wm.apply(lambda blk: blk.decorate(highlight=((i % 3)==0), hover=(((i+1)%3)==0), select=((i+2)%3)==0), -1)
            #     elif event.key == pygame.K_ESCAPE:
            #         running = False
            # elif event.type == pygame.MOUSEBUTTONDOWN:
            #     selected = wm.findBlock(lambda pred: pred.rect.collidepoint(event.pos))
            #     # wm.applyIf(
            #     #     lambda pred: pred.rect.collidepoint(event.pos),
            #     #     lambda Block: Block.move(10, 40),
            #     # )
            # elif event.type == pygame.MOUSEMOTION and selected is not None:
            #     wm.apply(lambda Block: Block.move(*event.rel), selected)
            # elif event.type == pygame.MOUSEBUTTONUP:
            #     selected = None

        screen.fill((70, 70, 70))
        can.draw(screen)
        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    main()
