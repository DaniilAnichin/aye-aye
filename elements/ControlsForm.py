#!/usr/bin/python
# -*- coding: utf-8 -*- #
from functools import partial
from PyQt4 import QtGui, QtCore
from translate import fromUtf8
from tools import Logger
logger = Logger()


stylesheet = '''
    border: 1px solid #8f8f91;
    color: #000000;
    font-weight: 500;
    background-color: %s;
    min-width: 80px;
    min-height: 25px;
'''


class ControlsForm(QtGui.QFormLayout):
    edited = QtCore.pyqtSignal()

    def __init__(self, *args):
        super(ControlsForm, self).__init__(*args)

        labels = ['width_label', 'angle_label', 'move_label', 'time_label']
        for name in labels:
            setattr(self, name, QtGui.QLabel())

        self.width_spin = QtGui.QSpinBox()
        self.width_spin.setRange(4, 20)
        self.width_spin.setSingleStep(1)
        self.width_spin.valueChanged.connect(lambda: self.edited.emit())

        self.angle_spin = QtGui.QDoubleSpinBox()
        self.angle_spin.setRange(1, 10)
        self.angle_spin.setSingleStep(0.5)

        self.step_spin = QtGui.QSpinBox()
        self.step_spin.setRange(1, 20)
        self.step_spin.setSingleStep(1)

        self.time_spin = QtGui.QDoubleSpinBox()
        self.time_spin.setRange(0.1, 1)
        self.time_spin.setSingleStep(0.1)

        color_buttons = ['scene_button', 'bot_button', 'ray_button', 'staff_button']
        action_buttons = ['move_button', 'turn_button', 'reset_button', 'defaults_button']
        for name in color_buttons + action_buttons:
            button = QtGui.QPushButton()
            button.setStyleSheet(stylesheet % QtGui.QColor('lightGrey').name())
            setattr(self, name, button)

        for name in color_buttons:
            getattr(self, name).clicked.connect(
                partial(self.color_picker, name)
            )

        self.addRow(self.width_label, self.width_spin)
        self.addRow(self.angle_label, self.angle_spin)
        self.addRow(self.move_label, self.step_spin)
        self.addRow(self.time_label, self.time_spin)

        self.addRow(self.scene_button, self.bot_button)
        self.addRow(self.ray_button, self.staff_button)

        last_number = 6
        for name in action_buttons:
            self.setWidget(
                last_number, QtGui.QFormLayout.SpanningRole, getattr(self, name)
            )
            last_number += 1

        # self.move_button.clicked.connect(lambda a: self.colors())
        self.defaults_button.clicked.connect(self.set_defaults)

        self.set_defaults()
        self.retranslateUi()

    def retranslateUi(self):
        self.width_label.setText(fromUtf8('Ширина'))
        self.angle_label.setText(fromUtf8('Шаг поворота'))
        self.move_label.setText(fromUtf8('Шаг движения'))
        self.time_label.setText(fromUtf8('Шаг времени'))

        self.scene_button.setText(fromUtf8('Цвет сцены'))
        self.bot_button.setText(fromUtf8('Цвет робота'))
        self.ray_button.setText(fromUtf8('Цвет луча'))
        self.staff_button.setText(fromUtf8('Цвет преград'))

        self.move_button.setText(fromUtf8('Двигаться'))
        self.turn_button.setText(fromUtf8('Поворачиваться'))
        self.reset_button.setText(fromUtf8('Сброс сцены'))
        self.defaults_button.setText(fromUtf8('Сброс параметров'))

    def colors(self):
        colors = {
            'bot': self.bot_color,
            'ray': self.ray_color,
            'scene': self.scene_color,
            'staff': self.staff_color
        }
        return colors

    def set_color(self, button_name, color):
        destination = button_name.replace('button', 'color')
        getattr(self, button_name).setStyleSheet(
            stylesheet % color.name()
        )
        setattr(self, destination, color)
        self.edited.emit()

    def color_picker(self, button_name):
        color = QtGui.QColorDialog().getColor()
        self.set_color(button_name, color)

    def bot_params(self):
        kwargs = {
            'width': self.width_spin.value(),
            'step': self.step_spin.value(),
            'color': self.bot_color,
            'ray_color': self.ray_color,
            'time_step': self.time_spin.value(),
            'angle': self.angle_spin.value()
        }
        return kwargs

    def set_defaults(self):
        self.width_spin.setValue(5)
        self.angle_spin.setValue(3)
        self.step_spin.setValue(10)
        self.time_spin.setValue(0.3)

        self.set_color('scene_button', QtGui.QColor(255, 255, 255))
        self.set_color('bot_button', QtGui.QColor(127, 127, 127))
        self.set_color('ray_button', QtGui.QColor(0, 255, 0))
        self.set_color('staff_button', QtGui.QColor(255, 0, 0))
