from . import Block
from queue import SimpleQueue

# from ..consts import SLACK
from pygame import rect

# TODO: import this lol wtf
SLACK = 5


class BlockManager:
    def __init__(self):
        self.Blocks: list[Block.Block] = []

    def newBlock(self, header, body):
        to_add = Block.Block(header, body)
        where = self.findOpenSpace(
            to_add.rect_surf.get_width(), to_add.rect_surf.get_height()
        )
        print(f"{where=}")
        to_add.move(*where)
        print(f"{(to_add.rect_pos[1],to_add.rect_pos[0])=}")
        self.Blocks.append(to_add)

    def deleteBlock(self, Blocks_idx):
        for idx in Blocks_idx:
            self.Blocks.pop(idx)

    def applyIf(self, pred, action):
        for idx in [idx for idx, Block in enumerate(self.Blocks) if pred(Block)]:
            action(self.Blocks[idx])

    def blockUnderMouse(self, top, left):
        return self.findBlock(lambda blk: blk.rect.collidepoint(top, left))

    def findBlock(self, lamb):
        return {idx for idx, Block in enumerate(self.Blocks) if lamb(Block)}

    def apply(self, action, blocks_idx):
        blocks_idx = blocks_idx if blocks_idx is list else [blocks_idx]
        for idx in blocks_idx:
            action(self.Blocks[idx])

    def draw(self, screen):
        for Block in self.Blocks:
            Block.draw(screen)

    def findOpenSpace(self, width, height):
        # TODO: optimize this to oblivian - cache locationsm maybe use R-tree, segment the canvas to squares, ana'aref
        if not self.Blocks:
            return (0, 0)

        min_left = float("inf")
        min_top = float("inf")
        for Block in self.Blocks:
            min_left = min(min_left, Block.rect.left)
            min_top = min(min_top, Block.rect.top)
        print(f"{min_left=} {min_top=}")

        candidates = SimpleQueue()
        candidates.put((min_left, min_top))

        while True:
            popped = candidates.get()
            print(f"looking {popped=}")
            candidate = rect.Rect(*popped, width, height)
            print(f"{candidate=}")

            # TODO: optimize to check only necessary Blocks
            collides = candidate.collidelistall(self.Blocks)
            print(f"{collides=}")
            if not collides:
                return popped

            max_left = -float("inf")
            max_top = -float("inf")
            for collider in collides:
                max_left = max(
                    max_left,
                    self.Blocks[collider].rect.left + self.Blocks[collider].rect.width,
                )
                max_top = max(
                    max_top,
                    self.Blocks[collider].rect.top + self.Blocks[collider].rect.height,
                )
            print(f"{max_left=} {max_top=}")
            candidates.put((candidate.left, max_top + SLACK))
            candidates.put((max_left + SLACK, candidate.top))
            print(f"putting {(candidate.left, max_top + SLACK)=}")
            print(f"putting {(max_left + SLACK, candidate.top)=}")
