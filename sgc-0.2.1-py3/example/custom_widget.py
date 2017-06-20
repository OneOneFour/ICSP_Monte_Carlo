import pygame
from pygame.locals import *

from sgc.widgets._locals import *
from sgc.widgets.base_widget import Simple

class MyBasicWidget(Simple):
    _default_size = (100,100)

class MyWidget(Simple):
    _default_size = (100,100)
    _available_images = ("over",)
    _extra_images = {"thing": ((0.3, 0), (1, -4))}
    _can_focus = True
    _settings_default = {"label": "Text", "label_col": (255,255,255)}

    _on = False

    def _draw_base(self):
        for img, col in zip(self._available_images,
                            (Color("red"), Color("green"))):
            self._images[img].fill(Color("black"))
            pygame.draw.circle(self._images[img], col,
                               (self.rect.w//2, self.rect.h//2), self.rect.w//2)

    def _draw_thing(self, image, size):
        image.fill(Color("darkolivegreen4"))

    def _draw_final(self):
        text = Font["widget"].render(self._settings["label"], True,
                                     self._settings["label_col"])
        x = self.rect.w//2 - text.get_width()//2
        y = self.rect.h//2 - text.get_height()//2
        for img in self._available_images:
            self._images[img].blit(text, (x,y))

    def update(self, time):
        self._images["thing"].rect.centerx = (pygame.mouse.get_pos()[0] -
                                              self.rect_abs.x)

    def _event(self, event):
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                self._on = not self._on
                self.on_click()
                self._switch("over" if self._on else "image")
            else:
                self._images["thing"]._show = not self._images["thing"]._show

    def _config(self, **kwargs):
        if "init" in kwargs:
            self._images["thing"].rect.y = 2

        for key in ("label", "label_col"):
            if key in kwargs:
                self._settings[key] = kwargs[key]

    def on_click(self):
        pygame.event.post(self._create_event("click", on=self._on))

    def _focus_enter(self, focus):
        if focus == 1:
            self._draw_rect = True
            self._switch()

    def _focus_exit(self):
        self._draw_rect = False
        self._switch()


if __name__ == "__main__":
    import sgc
    from sgc.locals import *

    pygame.display.init()
    pygame.font.init()

    screen = sgc.surface.Screen((640,480))
    clock = pygame.time.Clock()


    # Basic widget, inherits behaviours from Simple
    widget = MyBasicWidget((200,100), pos=(10,50),
                           label="Free label", label_side="top")
    widget.add()

    other = MyWidget(pos=(200,250), label="Custom")
    other.add(0)


    running = True
    while running:
        time = clock.tick(20)

        for event in pygame.event.get():
            if event.type == GUI:
                print("State: ", event.on)
            sgc.event(event)
            if event.type == QUIT:
                running = False

        screen.fill((0,0,100))
        sgc.update(time)
        pygame.display.flip()
