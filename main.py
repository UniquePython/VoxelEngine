from settings import *
from shader_program import ShaderProgram
from scene import Scene

import moderngl as mgl
import pygame as pg
import sys

class VoxelEngine():
    def __init__(self):
        pg.init()
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        # The profile mask specifies which version of OpenGL should be used by your application.
        # CORE profile only includes the modern, streamlined features of OpenGL
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)
        # The depth buffer is used to handle depth calculations in 3D rendering, ensuring closer object obscure farther ones.
        pg.display.gl_set_attribute(pg.GL_DEPTH_SIZE, 24)
        
        # Uses two buffers (front and back) to reduce flickering and tearing, enhancing the rendering smoothness.
        pg.display.set_mode(WIN_RES, flags=pg.OPENGL | pg.DOUBLEBUF)
        # Creates a ModernGL context, which is an interface between the application and the GPU. This context handles rendering operations, resource management, and more.
        self.ctx = mgl.create_context()
        
        # Enables depth testing, which ensures that pixels are drawn in the correct order based on their depth.
        # Enables face culling, which helps optimize rendering by discarding faces of polygons that are not visible (e.g., the back face of a cube).
        # Enables blending, allowing for transparent or semi-transparent rendering of objects.
        self.ctx.enable(flags=mgl.DEPTH_TEST | mgl.CULL_FACE | mgl.BLEND)
        # This sets the garbage collection mode for resources in the ModernGL context to automatic, ensuring that unused resources are cleaned up automatically to manage memory efficiently.
        self.ctx.gc_mode = 'auto'
        
        self.clock = pg.time.Clock()
        self.delta_time = 0
        self.time = 0
        
        self.is_running = True
        self.on_init()
        
        
    def on_init(self):
        self.shader_program = ShaderProgram(self)
        self.scene = Scene(self)
    
    
    def update(self):
        self.shader_program.update()
        self.scene.update()
        self.delta_time = self.clock.tick()
        self.time = pg.time.get_ticks() * 0.001 
        pg.display.set_caption(f"{self.clock.get_fps() :.0f}")
    
    
    def render(self):
        # Clears the current frame buffer, which essentially wipes the screen clean and prepares it for the next frame to be drawn.
        self.ctx.clear(color=BG_COLOR)
        self.scene.render()
        # This function updates the entire screen with what has been rendered since the last `flip`.
        pg.display.flip()
    
    
    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.type == pg.K_ESCAPE):
                self.is_running = False
    
    
    def run(self):
        while self.is_running:
            self.handle_events()
            self.update()
            self.render()
        pg.quit()
        sys.exit()


if __name__ == "__main__":
    app = VoxelEngine()
    app.run()