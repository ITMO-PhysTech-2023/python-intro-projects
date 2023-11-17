import abc
import typing

from .reader import Reader


class Component(abc.ABC):
    def __init__(self, owner: Reader, *, style: dict | None = None):
        """
        Constructor
        :param owner: object handling the corresponding Application
        :param style: additional style options
        """
        self.owner = owner
        if style is None:
            style = dict()
        self.style = style
        self.connect()

    @abc.abstractmethod
    def connect(self):
        """
        Method to connect the component to main Application
        """
        pass


class ButtonComponent(Component):
    def __init__(self, owner: Reader, title: str, action: typing.Callable, *, style: dict | None = None):
        """
        :param owner: object handling the corresponding Application
        :param title: title to draw on a button
        :param action: action to perform on pressing the button
        :param style: additional style options
        """
        super().__init__(owner, style=style)
        self.title = title
        self.action = action
        # TODO реализовать создание объекта кнопки и добавление стиля

    def connect(self):
        pass  # TODO реализовать 1. отрисовку, 2. настройку выполнения действия при нажатии


class DropdownComponent(Component):
    def __init__(
            self, owner: Reader, options: list, *,
            display: typing.Callable[..., str] = repr, style: dict | None = None
    ):
        """
        :param owner: object handling the corresponding Application
        :param options: options to select from
        :param display: how to display the options (default = `repr`)
        :param style: additional style options
        """
        super().__init__(owner, style=style)
        self.options = options
        self.display = display
        self.selected_id = 0
        # TODO реализовать создание объекта кнопки и добавление стиля

    @property
    def selected_option(self):
        return self.options[self.selected_id]

    def connect(self):
        pass  # TODO реализовать 1. отрисовку 2. сохранение выбранной опции


class TextComponent(Component):
    def __init__(self, owner: Reader, text: str | None, *, style: dict | None = None):
        """
        :param owner: object handling the corresponding Application
        :param text: text to display
        """
        super().__init__(owner)
        self.text = text

    def show(self):
        pass  # TODO отобразить компоненту

    def hide(self):
        pass  # TODO спрятать компоненту

    def connect(self):
        pass  # TODO реализовать отрисовку
