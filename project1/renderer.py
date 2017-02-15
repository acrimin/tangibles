import math

from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.resources import resource_find
from kivy.graphics.transformation import Matrix
from kivy.graphics.opengl import *
from kivy.graphics import *
from objloader import ObjFile

class Renderer(Widget):
    def __init__(self, **kwargs):
        self.canvas = RenderContext(compute_normal_mat=True)
        self.canvas.shader.source = resource_find('simple.glsl')
        self.scene = ObjFile(resource_find("monkey.obj"))
        super(Renderer, self).__init__(**kwargs)
        with self.canvas:
            self.cb = Callback(self.setup_gl_context)
            PushMatrix()
            self.setup_scene()
            PopMatrix()
            self.cb = Callback(self.reset_gl_context)
        Clock.schedule_interval(self.update_glsl, 1 / 60.)

        # self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        # self._keyboard.bind(on_key_down=self._on_keyboard_down)
        # self._touches = []

    def setup_gl_context(self, *args):
        glEnable(GL_DEPTH_TEST)

    def reset_gl_context(self, *args):
        glDisable(GL_DEPTH_TEST)

    def update_glsl(self, *largs):
        asp = self.width / float(self.height)
        proj = Matrix().view_clip(-asp, asp, -1, 1, 1, 100, 1)
        self.canvas['projection_mat'] = proj
        self.canvas['diffuse_light'] = (1.0, 1.0, 0.8)
        self.canvas['ambient_light'] = (0.1, 0.1, 0.1)

    def setup_scene(self):
        Color(1, 1, 1, 1)
        PushMatrix()
        Translate(0, 0, -3)
        self.rotx = Rotate(0, 0, 1, 0)
        self.roty = Rotate(0, 1, 0, 0)
        m = list(self.scene.objects.values())[0]
        UpdateNormalMatrix()
        self.mesh = Mesh(
            vertices=m.vertices,
            indices=m.indices,
            fmt=m.vertex_format,
            mode='triangles',
        )
        PopMatrix()


    # def _keyboard_closed(self):
    #     self._keyboard.unbind(on_key_down=self._on_keyboard_down)
    #     self._keyboard = None

    # def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
    #     if keycode[1] == 'left':
    #         self.rotx.angle += 5
    #     elif keycode[1] == 'right':
    #         self.rotx.angle -= 5
    #     if keycode[1] == 'up':
    #         self.roty.angle += 5
    #     elif keycode[1] == 'down':
    #         self.roty.angle -= 5
    #     elif keycode[1] == 'n':
    #         self.rotx.angle = 0
    #         self.roty.angle = 0

    #     return True

    
    # def define_rotate_angle(self, touch):
    #     x_angle = (touch.dx/self.width)*360
    #     y_angle = -1*(touch.dy/self.height)*360
    #     return x_angle, y_angle

    # def on_touch_down(self, touch):
    #     self._touch = touch
    #     touch.grab(self)
    #     self._touches.append(touch)

    # def on_touch_up(self, touch): 
    #     touch.ungrab(self)
    #     self._touches.remove(touch)

    # def on_touch_move(self, touch):
    #     self.update_glsl
    #     if touch in self._touches and touch.grab_current == self:
    #         if len(self._touches) == 1:
    #             ax, ay = self.define_rotate_angle(touch)

    #             self.rotx.angle += ax
    #             self.roty.angle += ay