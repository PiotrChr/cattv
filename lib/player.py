import pyglet


class Player:
    def __init__(self):
        self.window = None
        self.player = None
        self.source = None
        self.media = None

        self.init()

    def init(self):
        self.window = pyglet.window.Window()
        self.player = pyglet.media.Player()
        self.source = pyglet.media.StreamingSource()

    def load(self, media):
        self.media = pyglet.media.load(media)

    def play(self, media):
        if not self.media:
            self.load(media)

        self.player.queue(self.media)
        self.player.play()

    @window.event
    def on_draw(self):
        if self.player.source and self.player.source.video_format:
            self.player.get_texture().blit(50, 50)
