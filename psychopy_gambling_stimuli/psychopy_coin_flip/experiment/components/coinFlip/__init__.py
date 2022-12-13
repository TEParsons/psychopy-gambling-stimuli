#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
from psychopy.experiment.components import Param, _translate, getInitVals
from psychopy.experiment.components.image import ImageComponent
from psychopy import prefs


class CoinFlipComponent(ImageComponent):
    """This is used by Builder to represent a component that was not known
    by the current installed version of PsychoPy (most likely from the future).
    We want this to be loaded, represented and saved but not used in any
    script-outputs. It should have nothing but a name - other params will be
    added by the loader
    """
    targets = ['PsychoPy']

    categories = ['Stimuli']
    targets = ['PsychoPy']
    iconFile = Path(__file__).parent / 'coin.png'
    tooltip = _translate('Unknown: A component that is not known by the current '
                         'installed version of PsychoPy\n(most likely from the '
                         'future)')

    def __init__(self, exp, parentName, name='coin',
                 value=None, weight=0.5, triggers="keyboard", keys="space",
                 size=(0.5, 0.5), pos=(0, 0), anchor="center", units='from exp settings',
                 color='gold', colorSpace='rgb',
                 flipHeight=0.5, flipDuration=1, fps=18,
                 startType='time (s)', startVal=0.0,
                 stopType='duration (s)', stopVal=1.0,
                 startEstim='', durationEstim=''):
        self.type = 'Unknown'
        self.exp = exp  # so we can access the experiment if necess
        self.parentName = parentName  # to access the routine too if needed
        self.params = {}
        self.depends = []
        super(CoinFlipComponent, self).__init__(
            exp, parentName, name=name,
            size=size, pos=pos, anchor=anchor, units=units,
            color=color, colorSpace=colorSpace,
            startType=startType, startVal=startVal,
            stopType=stopType, stopVal=stopVal,
            startEstim=startEstim, durationEstim=durationEstim
        )
        self.order += []

        self.exp.requireImport(importName="coinflip", importFrom='psychopy.visual')

        # Basic
        self.order += ["value", "weight", "triggers", "keys"]

        self.params['value'] = Param(
            value, valType="code", inputType="choice", categ="Basic",
            allowedVals=("'heads'", "'tails'", "None"), allowedLabels=("Heads", "Tails", "Blank"),
            updates='constant', allowedUpdates=[],
            label=_translate("Start value"),
            hint=_translate("Starting value of the coin before flipping"),
        )
        self.params['weight'] = Param(
            weight, valType="code", inputType="single", categ="Basic",
            updates='constant', allowedUpdates=[],
            label=_translate("Weighting"),
            hint=_translate("How the coin is weighted: 0 = always tails, 1 = always heads, 0.5 = even chances")
        )
        self.params['triggers'] = Param(
            triggers, valType="code", inputType="choice", categ="Basic",
            allowedVals=("keyboard", "click", "clickedon"), allowedLabels=("Keyboard", "Any click", "Clicked on"),
            updates='constant', allowedUpdates=[],
            label=_translate("Triggers"),
            hint=_translate("Events which trigger a coin flip."),
            direct=False
        )
        self.depends.append(
            {
                "dependsOn": "triggers",  # if...
                "condition": "=='keyboard'",  # meets...
                "param": "keys",  # then...
                "true": "show",  # should...
                "false": "hide",  # otherwise...
            }
        )
        self.params['keys'] = Param(
            keys, valType="list", inputType="single", categ="Basic",
            updates='constant', allowedUpdates=[],
            label=_translate("Allowed keys"),
            hint=_translate("Which keyboard keys trigger a coin flip?"),
            direct=False
        )

        # Animation
        self.order += ["flipHeight", "flipDuration", "fps"]

        self.params['flipHeight'] = Param(
            flipHeight, valType="code", inputType="single", categ="Animation",
            updates='constant', allowedUpdates=['constant', 'set every repeat'],
            label=_translate("Flip height"),
            hint=_translate("How high the coin travels when flipping."),
        )

        self.params['flipDuration'] = Param(
            flipDuration, valType="code", inputType="single", categ="Animation",
            updates='constant', allowedUpdates=['constant', 'set every repeat'],
            label=_translate("Flip duration"),
            hint=_translate("How long the animation takes to complete, will be rounded to the nearest full loop."),
        )

        self.params['fps'] = Param(
            fps, valType="code", inputType="single", categ="Animation",
            updates='constant', allowedUpdates=['constant', 'set every repeat'],
            label=_translate("Frame rate (fps)"),
            hint=_translate("How many frames of the animation elapse in a single second. The animation is 6 frames "
                            "long."),
        )

        # Delete unused params from Image
        del self.params['image']
        del self.params['interpolate']
        del self.params['mask']
        del self.params['texture resolution']
        del self.params['ori']
        del self.params['flipVert']
        del self.params['flipHoriz']

    def writeInitCode(self, buff):
        inits = getInitVals(self.params, target="PsychoPy")
        # Make object
        code = (
            "# Create %(name)s object\n"
            "%(name)s = coinflip.CoinFlipStim(\n"
            "    win, name='%(name)s',\n"
            "    startValue=%(value)s, weight=%(weight)s,\n"
            "    color=%(color)s, colorSpace=%(colorSpace)s,\n"
            "    size=%(size)s, pos=%(pos)s, units=%(units)s,\n"
            "    flipHeight=%(flipHeight)s, flipDuration=%(flipDuration)s, fps=%(fps)s\n"
            ")\n"
        )
        buff.writeIndentedLines(code % inits)
        # Add control handlers
        code = (
            "# add flip control handlers for %(name)s\n"
            "%(name)s.mouse = event.Mouse()\n"
            "%(name)s.kb = keyboard.Keyboard()\n"
        )
        buff.writeIndentedLines(code % inits)

    def writeFrameCode(self, buff):
        # Write start code
        indented = self.writeStartTestCode(buff)
        if indented:
            code = (
                "%(name)s.setAutoDraw(True)\n"
            )
            buff.writeIndentedLines(code % self.params)
            buff.setIndentLevel(-indented, relative=True)
        # Write active code
        indented = self.writeActiveTestCode(buff)
        if indented:
            # Check for keyboard
            if self.params['triggers'].val == "keyboard":
                code = (
                    "if %(name)s.kb.getKeys(%(keys)s):\n"
                    "    %(name)s.flipCoin()\n"
                )
                buff.writeIndentedLines(code % self.params)
            # Check for clicks
            if self.params['triggers'].val == "clicks":
                code = (
                    "if %(name)s.mouse.getPressed()[0]:\n"
                    "    %(name)s.flipCoin()\n"
                )
                buff.writeIndentedLines(code % self.params)
            # Check for clicked on
            if self.params['triggers'].val == "clickedon":
                code = (
                    "if %(name)s.mouse.isPressedIn(%(name)s):\n"
                    "    %(name)s.flipCoin()\n"
                )
                buff.writeIndentedLines(code % self.params)

            buff.setIndentLevel(-indented, relative=True)
        # Write stop code
        indented = self.writeStopTestCode(buff)
        if indented:
            code = (
                "%(name)s.setAutoDraw(False)\n"
            )
            buff.writeIndentedLines(code % self.params)
            buff.setIndentLevel(-indented, relative=True)
