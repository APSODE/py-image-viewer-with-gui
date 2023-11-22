from tkinter import Frame, LabelFrame, Label, Toplevel
from typing import TYPE_CHECKING, List, Dict, Tuple

from PIL.Image import Image
from PIL.ImageTk import PhotoImage

from core.type_annotation.CustomTypes import CHANNEL_TYPE_LITERAL
from gui.ComponentManager import ComponentManager
from gui.RenderParamWrapper import RenderParamWrapper

if TYPE_CHECKING:
    from gui.ImageControllerGUI import ImageControllerGUI


class ImageViewerGUI(Toplevel):
    def __init__(self, master: "ImageControllerGUI"):
        super().__init__(master = master)
        self._master = master
        self._component_manager = ComponentManager.create_manager()
        self._set_initial_window()
        self._render_component()

    @staticmethod
    def create_window(master: "ImageControllerGUI"):
        return ImageViewerGUI(master = master)

    def _set_initial_window(self):
        width = 500
        height = 300
        center_x = (self.winfo_screenwidth() // 2) - (width // 2)
        center_y = (self.winfo_screenheight() // 2) - (height // 2)
        self.title("PyImageViewer v1.0")
        self.geometry(f"{width}x{height}+{center_x}+{center_y}")
        # self.resizable(False, False)

    def _render_component(self):
        self._set_frame()
        self._set_default_label()

        # input_channel: CHANNEL_TYPE_LITERAL = "GRAY"
        # self._set_frame_by_image_channel(channel = input_channel),
        # self._set_label_frame_by_image_channel(channel = input_channel),
        # self._set_label_by_image_channel(channel = input_channel)

    def _set_frame(self):
        self._component_manager.add_component(
            name = "base",
            component = Frame(self),
            with_render = True,
            render_type = "pack",
            render_param = RenderParamWrapper(side = "top", anchor = "center")
        )
        self._component_manager.add_component(
            name = "image_container",
            component = Frame(self),
            with_render = True,
            render_type = "pack",
            render_param = RenderParamWrapper(side = "top", anchor = "center")
        )

    def _set_default_label(self):
        self._component_manager.add_component(
            name = "default",
            component = Label(
                self._component_manager.get_component("base", Frame),
                text = "현재 로드된 이미지가 존재하지 않습니다."
            ),
            with_render = True,
            render_type = "pack",
            render_param = RenderParamWrapper(anchor = "center")
        )

    def set_image(self, image_datas: Dict[str, Tuple[str, PhotoImage]]):
        self._component_manager.update_component(
            name = "default",
            component_class = Label,
            **{"text": ""}
        )

        for idx, component_name in enumerate(image_datas):
            label_text_and_image = image_datas.get(component_name)
            print(label_text_and_image)

            self._component_manager.add_component(
                name = component_name,
                component = LabelFrame(
                    self._component_manager.get_component("image_container", Frame),
                    text = label_text_and_image[0]
                ),
                with_render = True,
                render_type = "grid",
                render_param = RenderParamWrapper(row = 0, column = idx, padx = 10, pady = 10)
            )

            self._component_manager.add_component(
                name = component_name,
                component = Label(
                    self._component_manager.get_component(component_name, LabelFrame),
                    text = "",
                    image = label_text_and_image[1]
                ),
                with_render = True,
                render_type = "pack",
                render_param = RenderParamWrapper(anchor = "center", padx = 10, pady = 10)
            )
            self._component_manager.get_component(component_name, Label).image = label_text_and_image[1]

    @staticmethod
    def _get_component_amount_by_image_channel(channel: CHANNEL_TYPE_LITERAL) -> int:
        return 1 if channel == "GRAY" else 3

    @staticmethod
    def _get_label_frame_text_by_channel(channel: CHANNEL_TYPE_LITERAL) -> str:
        return channel.split() if channel != "GRAY" else "GRAY"

    @property
    def component_manager(self) -> ComponentManager:
        return self._component_manager


# class ImageViewerGUI_NEW(Toplevel):
#     def __init__(self, master: "ImageControllerGUI", title: str):
#         super().__init__(master = master)
#         self._master = master
#         self._component_manager = ComponentManager.create_manager()
#         self._set_initial_window(title = title)
#         self._render_component()
#
#     @staticmethod
#     def create_window(master: "ImageControllerGUI", title: str):
#         return ImageViewerGUI(master = master)
#
#     def _set_initial_window(self, title: str):
#         width = 500
#         height = 300
#         center_x = (self.winfo_screenwidth() // 2) - (width // 2)
#         center_y = (self.winfo_screenheight() // 2) - (height // 2)
#         self.title(f"PyImageViewer v1.0 - {title}")
#         self.geometry(f"{width}x{height}+{center_x}+{center_y}")
#         self.resizable(False, False)
#
#     def _render_component(self):
#         pass
#
#     def _set_frame(self):
#         self._component_manager.add_component(
#             name = "base",
#             component = Frame(self),
#             with_render = True,
#             render_type = "pack",
#             render_param = ""
#         )

