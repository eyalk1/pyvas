from Blocks import BlockManager as BM
from pygame.event import Event as GE
from pygame import KEYDOWN, KEYUP, MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION, QUIT
import pygame.constants as pgc
import pygame.key
import event as CEvent
from enum import Enum
from dataclasses import fields


class Surface(Enum):
    canvas = 0
    block = 1
    selected_block = 2


class Canvas:
    def __init__(self) -> None:
        self._m_block_manager = BM.BlockManager()
        self.m_curr_hover: set[int] = set()
        self.m_selected_blocks: set[int] = set()
        self.m_highlight_block: set[int] = set()

    def draw(self, screen):
        self._m_block_manager.draw(screen)

    def parseEvent(self, event: GE) -> CEvent:
        print(event.type)
        print(pygame.KEYDOWN)
        match event.type:
            case pygame.KEYDOWN:  # key, mod(alt/shift/etc...)
                print("key!")
                return self.handleKeypress(event.key, event.mod)
            case pygame.KEYUP:  # key, mod(alt/shift/etc...)
                return self.handlekeRelease(event.key, event.mod)
            case pygame.MOUSEBUTTONDOWN:  # pos, button
                return self.handleMousepress(event.button, event.pos)
            case pygame.MOUSEBUTTONUP:  # pos, button
                return self.handleMouserelease(event.button, event.pos)
            case pygame.MOUSEMOTION:  # pos, rel, buttons
                return self.handleMousemove(event.buttons, event.pos, event.rel)
            case pygame.QUIT:
                return CEvent.CloseApp()

    def handleEvent(self, event: CEvent) -> None:
        match event:
            case CEvent.NewWindow(): # header, body
                print("here")
                self._m_block_manager.newBlock(event.header, event.body)
            case CEvent.CloseApp():
                return
            case CEvent.Decorate(): # select, deselect, hover, dehover, highlight, dehighlight

                for s in select:
                    
                for s in deselect:
                    pass
                for s in hover:
                    pass
                for s in dehover:
                    pass
                for s in highlight:
                    pass
                for s in dehighlight:
                    pass
                


    def handleKeypress(self, key, mod):
        match key:
            case pgc.K_ESCAPE:
                print("escape!")
                return CEvent.CloseApp()
            case pgc.K_SPACE:
                print("new!")
                return CEvent.NewWindow("bulbul", "akabulbul\nbabakulkul")

    def handleMousepress(self, button, pos):
        clicked_block = self._m_block_manager.blockUnderMouse(*pos)
        on = self._getSurface(clicked_block)
        is_ctrl = pygame.key.get_mods() & pgc.KMOD_CTRL
        last_highlight = self.m_highlight_block

        match (is_ctrl, on):
            case (True, Surface.block):
                self.m_selected_blocks += clicked_block
                self.m_highlight_block = clicked_block
                return CEvent.Decorate(
                    select=clicked_block,
                    highlight=clicked_block,
                    dehighlight=last_highlight,
                )
            case (True, Surface.selected_block):
                self.m_selected_blocks -= clicked_block
                self.m_highlight_block = clicked_block
                return CEvent.Decorate(
                    deselect=clicked_block, dehighlight=last_highlight
                )
            case (False, Surface.canvas):
                # two lines just to merge two bit_sets wtf
                ret = clicked_block
                ret += self.m_selected_blocks
                return CEvent.Decorate(deselect=ret, dehighlight=True, highlight=False)
            case (False, Surface.selected_block):
                to_deselect = self.m_selected_blocks - clicked_block
                self.m_selected_blocks = clicked_block
                last_highlight = self.m_highlight_block
                self.m_highlight_block = clicked_block
                return CEvent.Decorate(
                    select=clicked_block,
                    deselect=to_deselect,
                    highlight=self.m_highlight_block,
                    dehighlight=last_highlight,
                )

            case [(False, Surface.block), (True, Surface.canvas)]:
                pass

    def handleMouserelease(self, button, pos):
        pass

    def handleMousemove(self, buttons, pos, rel):
        hovered_block = self._m_block_manager.blockUnderMouse(*pos)
        last_hovered = None if hovered_block in self.m_curr_hover else self.m_curr_hover
        self.m_curr_hover = hovered_block
        return CEvent.Decorate(hover=self.m_curr_hover, dehover=last_hovered)

    def _getSurface(self, clicked_block):
        if clicked_block == []:
            return Surface.canvas
        elif len(clicked_block & self.m_selected_blocks) == 0:
            return Surface.block
        else:
            return Surface.selected_block
