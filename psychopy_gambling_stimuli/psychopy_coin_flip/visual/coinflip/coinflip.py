from pathlib import Path
from PIL import Image as pil
from numpy.random import choice as randchoice

from psychopy import core, layout
from psychopy.localization import _translate
from psychopy.tools.attributetools import attributeSetter
from psychopy.tools import animationtools as at
from psychopy.visual import ImageStim


class CoinFlipStim(ImageStim):
    """
    Coin stimulus with a command to "flip", which will play a flip animation.

    Parameters
    ================
    win : visual.Window
        Window to draw coin to.
    name : str
        Name to refer to coin by.
    startValue : "heads", "tails" or None
        Value of the coin before flipping. If None, then face will display blank until flipped.
    weight : float
        How the coin is weighted. This can be any value between 0 and 1
        0 = Always tails
        0.5 = Even chances
        1 = Always heads
    color : tuple, list, str, colors.Color
        Color of the coin. Will be applied to the base (white) coin image as a color overlay.
    colorSpace : str
        Color space within which to interpret the coin color. If None, will use color space of
        the window.
    size : int, float, layout.Size
        Size of the coin when not flipping. Use `None` to represent the image at 1x scale (97x79px).
    pos : int, float, layout.Pos
        Position of the coin when not flipping.
    units :
    flipHeight : float, int, layout.Size
        How high the coin should travel while flipping. Values should be in the unit space of
        the object, or can be a `layout.Size` object. If the latter, only the height will be used.
    flipDuration : int, float
        How long the animation takes to complete, will be rounded to the nearest full loop. The
        animation is 6 frames long, so this means rounding to the closest `6 / fps` seconds
    fps : int
        How many frames of the animation elapse in a single second. The animation is 6 frames long.

    Acknowledgements
    ================
    Coin sprite by cazwolf via itch.io: https://cazwolf.itch.io/pixel-coinflip
    """
    def __init__(
            self, win, name="flip",
            startValue=None, weight=0.5,
            color="gold", colorSpace=None,
            size=(None, None), pos=(0, 0), units=None,
            flipHeight=0.5, flipDuration=1, fps=18,
            autoLog=False
    ):
        # Initialise parent
        ImageStim.__init__(
            self, win, name=name,
            color=color, colorSpace=colorSpace,
            size=size, pos=pos, units=units,
            autoLog=autoLog
        )

        # Attributes for managing animation loop
        self.frameClock = core.Clock()
        self.frameIndex = None
        self.animationClock = core.Clock()

        # Load and store frames
        self.animationFrames = []
        folder = Path(__file__).parent
        for file in (
            "frame1.png",
            "frame2.png",
            "frame3.png",
            "frame4.png",
            "frame5.png",
            "frame6.png"
        ):
            self.animationFrames.append(
                pil.open(str(folder / file))
            )

        # Load and store faces
        self.faces = {
            "heads": pil.open(str(folder / "heads.png")),
            "tails": pil.open(str(folder / "tails.png")),
            None: pil.open(str(folder / "frame1.png"))
        }

        # Store attributes
        self.flipHeight = flipHeight
        self.fps = fps
        self.flipDuration = flipDuration
        self.weight = weight

        # Starting state
        self.value = startValue
        self.isFlipping = False
        self.image = self._settledFace

    @property
    def pos(self):
        # Do base getting
        return ImageStim.pos.fget(self)

    @pos.setter
    def pos(self, value):
        # Do base setting
        ImageStim.pos.fset(self, value)
        # Store resting position
        self._restingPos = self._pos

    @property
    def flipHeight(self):
        return getattr(self._flipHeight, self.units)[1]

    @flipHeight.setter
    def flipHeight(self, value):
        if isinstance(value, layout.Vector):
            value = getattr(value, self.units)[1]
        self._flipHeight = layout.Size((0, value), units=self.units, win=self.win)

    @attributeSetter
    def value(self, value):
        # Make sure value is heads of tails (or None)
        allowed = ("heads", 1, True, "tails", 0, False, None)
        assert value in allowed, _translate(
            "Value for CoinFlipStim must be one of: %s. Got: %s"
        ) % (allowed, value)
        # Alias numeric values for strings
        if value in (0, False):
            value = "tails"
        if value == (1, True):
            value = "heads"
        # Store value
        self.__dict__['value'] = value
        # Set face image
        self._settledFace = self.faces[value]

    def flipCoin(self):
        # If already flipping, do nothing
        if self.isFlipping:
            return
        # Mark as flipping so the animation plays
        self.isFlipping = True
        # Set value at random according to weight
        self.value = randchoice(
            ("heads", "tails"),
            p=(self.weight, 1-self.weight)
        )

    def draw(self, win=None):
        if self.isFlipping:
            if self.frameIndex is None:
                # If starting animation, reset clocks to 0
                self.frameClock.reset(0)
                self.animationClock.reset(0)
                self.frameIndex = 0

            if self.frameClock.getTime() > 1/self.fps:
                # If sufficient time has passed since last new frame, move to next frame
                self.frameIndex = (self.frameIndex + 1) % len(self.animationFrames)
                self.image = self.animationFrames[self.frameIndex]
                # Reset frame timer
                self.frameClock.reset(0)
                # Work out where we should be in the air
                animPos = at.sinusoidalMovement(
                    startPos=self._restingPos,
                    apexPos=self._restingPos + self._flipHeight,
                    duration=self.flipDuration / 2,
                    time=self.animationClock.getTime())
                ImageStim.pos.fset(self, animPos)

            if self.animationClock.getTime() > self.flipDuration:
                # If animation has completed, end
                self.isFlipping = False
                self.frameIndex = None
                # Settle on value
                self.image = self._settledFace
                ImageStim.pos.fset(self, self._restingPos)

        # Do base drawing
        ImageStim.draw(self, win=win)

    @attributeSetter
    def flipDuration(self, value):
        # Make sure animation will complete during flip duration
        oneLoop = len(self.animationFrames) / self.fps
        value += oneLoop - (value % oneLoop)

        self.__dict__['flipDuration'] = value
