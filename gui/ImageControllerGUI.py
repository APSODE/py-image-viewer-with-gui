import json
from tkinter import Tk, Frame, LabelFrame, Radiobutton, StringVar, Button, Label
from tkinter.ttk import Combobox
from typing import Dict, TYPE_CHECKING, Tuple, Optional

from PIL.Image import Image

from core.PyImageViewerCore import PyImageViewerCore
from core.manager.ImageManager import ImageManager
from core.type_annotation.CustomTypes import CHANNEL_TYPE_LITERAL
from gui.ImageViewerGUI import ImageViewerGUI
from gui.ComponentManager import ComponentManager
from gui.RenderParamWrapper import RenderParamWrapper


_FRAME_NAME_LIST = ["image_select", "image_func", "etc", "button"]
_LABEL_FRAME_NAMES = ["이미지 파일 선택", "기능 선택", "기타"]
_LABEL_FRAME_DATA: Dict[str, str] = {_FRAME_NAME_LIST[idx]: value for idx, value in enumerate(_LABEL_FRAME_NAMES)}


class ImageControllerGUI(Tk):
    def __init__(self):
        super().__init__()
        self._component_manager = ComponentManager.create_manager()
        self._core = PyImageViewerCore.create_core()
        self._image_viewer_window = self._create_image_viewer_window()
        self._set_initial_window()
        self._render_component()
        with open("test.json", "w") as test_file:
            json.dump(
                {key: str(value) for key, value in self._component_manager.component_container.__dict__.items()},
                test_file,
                indent = 4,
                ensure_ascii = False
            )
        self.mainloop()

    @staticmethod
    def create_gui() -> "ImageControllerGUI":
        return ImageControllerGUI()

    def _create_image_viewer_window(self):
        return ImageViewerGUI.create_window(self)

    def _set_initial_window(self):
        width = 500
        height = 400
        center_x = (self.winfo_screenwidth() // 2) - (width // 2)
        center_y = (self.winfo_screenheight() // 2) - (height // 2)
        self.title("PyImageViewer v1.0 - Image Controller")
        self.geometry(f"{width}x{height}+{center_x}+{center_y}")
        # self.resizable(False, False)

    def _render_component(self):
        self._set_component_variable()
        self._set_frame()
        self._set_label_frame()
        self._set_inner_frame()
        self._set_inner_label_frame()
        self._set_combobox()
        self._set_radiobutton()
        self._set_button()
        self._set_event_binder()

    def _set_component_variable(self):
        self._component_manager.component_container.add_string_var("color_mode_string_var")
        self._component_manager.component_container.set_string_var_value("color_mode_string_var", "NORMAL")
        self._component_manager.component_container.add_string_var("other_func_string_var")
        self._component_manager.component_container.set_string_var_value("other_func_string_var", "None")

    def _set_event_binder(self):
        component = self._component_manager.get_component("image_select", Combobox)
        component.bind("<<ComboboxSelected>>", self._load_image_on_gui)

    def _set_frame(self):
        self._component_manager.add_component(
            name = "base",
            component = Frame(self),
            with_render = True,
            render_type = "pack",
            render_param = RenderParamWrapper(side = "top", anchor = "center")
        )

        base_frame = self._component_manager.get_component("base", Frame)
        for idx, name in enumerate(_FRAME_NAME_LIST):
            self._component_manager.add_component(
                name = name,
                component = Frame(base_frame),
                with_render = True,
                render_type = "grid",
                render_param = RenderParamWrapper(row = idx, pady = 10)
            )

    def _set_inner_frame(self):
        self._component_manager.add_component(
            name = "image_select_inner",
            component = Frame(self._component_manager.get_component("image_select", LabelFrame)),
            with_render = True,
            render_type = "pack",
            render_param = RenderParamWrapper(anchor = "center", padx = 10, pady = 10)
        )

        image_select_inner_frame = self._component_manager.get_component("image_select_inner", Frame)
        for idx, frame_name in enumerate(["image_select_combobox", "image_select_refresh_button"]):
            self._component_manager.add_component(
                name = frame_name,
                component = Frame(image_select_inner_frame),
                with_render = True,
                render_type = "grid",
                render_param = RenderParamWrapper(row = 0, column = idx)
            )

        self._component_manager.add_component(
            name = "image_func_inner",
            component = Frame(self._component_manager.get_component("image_func", LabelFrame)),
            with_render = True,
            render_type = "pack",
            render_param = RenderParamWrapper(anchor = "center")
        )

        image_func_inner_frame = self._component_manager.get_component("image_func_inner", Frame)
        for idx, inner_frame_name in enumerate(["color_mode_inner", "other_func_inner"]):
            self._component_manager.add_component(
                name = inner_frame_name,
                component = Frame(image_func_inner_frame),
                with_render = True,
                render_type = "grid",
                render_param = RenderParamWrapper(row = idx, column = 0)
            )

    def _set_inner_label_frame(self):
        self._component_manager.add_component(
            name = "color_mode_inner",
            component = LabelFrame(
                self._component_manager.get_component("color_mode_inner", Frame),
                text = "컬러 모드 설정  -  # filp, crop에는 적용 X"
            ),
            with_render = True,
            render_type = "pack",
            render_param = RenderParamWrapper(anchor = "center", padx = 10, pady = 10)
        )
        self._component_manager.add_component(
            name = "other_func_inner",
            component = LabelFrame(
                self._component_manager.get_component("other_func_inner", Frame),
                text = "기타 기능 설정"
            ),
            with_render = True,
            render_type = "pack",
            render_param = RenderParamWrapper(anchor = "center", padx = 10, pady = 10)
        )

    def _set_label_frame(self):
        for frame_name, label_frame_name in _LABEL_FRAME_DATA.items():
            self._component_manager.add_component(
                name = frame_name,
                component = LabelFrame(
                    self._component_manager.get_component(frame_name, Frame),
                    text = label_frame_name
                ),
                with_render = True,
                render_type = "pack",
                render_param = RenderParamWrapper(anchor = "center")
            )

    def _set_combobox(self):
        self._component_manager.add_component(
            name = "image_select",
            component = Combobox(
                self._component_manager.get_component("image_select_combobox", Frame),
                values = self._core.get_image_file_dirs(),
                width = 48,
                height = 2
            ),
            with_render = True,
            render_type = "pack",
            render_param = RenderParamWrapper(anchor = "center", padx = 10, pady = 10)
        )

    def _set_radiobutton(self):
        for idx, color_mode in enumerate(["RGB", "YUV", "GRAY", "NORMAL"]):
            self._component_manager.add_component(
                name = f"color_mode_select_{color_mode}",
                component = Radiobutton(
                    master = self._component_manager.get_component("color_mode_inner", LabelFrame),
                    text = color_mode,
                    variable = self._component_manager.get_component("color_mode", StringVar),
                    value = color_mode,
                    state = "disabled",
                    command = self._check_and_change_radiobtn_and_btn_status
                ),
                with_render = True,
                render_type = "grid",
                render_param = RenderParamWrapper(row = 0, column = idx, padx = 10, pady = 10)
            )

        for idx, func_name in enumerate(["ud_flip", "lr_flip", "half_crop", "None"]):
            self._component_manager.add_component(
                name = f"{func_name.lower()}_func",
                component = Radiobutton(
                    self._component_manager.get_component("other_func_inner", LabelFrame),
                    variable = self._component_manager.get_component("other_func", StringVar),
                    value = func_name,
                    text = func_name.replace("_", " ").upper(),
                    state = "disabled",
                    command = self._check_and_change_radiobtn_and_btn_status
                ),
                with_render = True,
                render_type = "grid",
                render_param = RenderParamWrapper(row = 0, column = idx, padx = 10, pady = 10)
            )

    def _set_button(self):
        self._component_manager.add_component(
            name = "apply",
            component = Button(
                master = self._component_manager.get_component("button", Frame),
                text = "적용",
                command = self._load_image_by_channel_on_gui,
                width = 8,
                height = 2,
                state = "disabled"
            ),
            with_render = True,
            render_type = "grid",
            render_param = RenderParamWrapper(row = 0, column = 0, padx = 10, pady = 10)
        )

        self._component_manager.add_component(
            name = "refresh",
            component = Button(
                master = self._component_manager.get_component("image_select_refresh_button", Frame),
                text = "⟳",
                width = 4,
                command = self._update_image_list
            ),
            with_render = True,
            render_type = "pack",
            render_param = RenderParamWrapper(anchor = "center", padx = 10, pady = 10)
        )

    def _load_image_on_gui(self, *args):
        self._image_viewer_window.component_manager.update_component(
            name = "default",
            component_class = Label,
            **{"text": "현재 이미지를 로드하는 중입니다. 잠시만 기다려주십시오."}
        )

        selected_image_name = self._component_manager.get_component("image_select", Combobox).get()
        self._core.create_manager(
            image_dir = self._core.get_image_file_dir(
                image_name = selected_image_name
            )
        )

        loaded_image = self._core.image_manager.convert_to_photoimage(
            image = self._resize_image_by_gui_size(
                image = self._core.image_manager.loaded_image
            )
        )

        self._image_viewer_window.geometry(f"{loaded_image.width() + 50}x{loaded_image.height() + 100}")

        self._image_viewer_window.set_image(
            image_datas = {"original_image": ("NORMAL", loaded_image)}
        )

        for color_mode in ["RGB", "YUV", "GRAY", "NORMAL"]:
            self._component_manager.update_component(
                name = f"color_mode_select_{color_mode}",
                component_class = Radiobutton,
                **{"state": "normal"}
            )

        for other_func_name in ["ud_flip", "lr_flip", "half_crop", "none"]:
            self._component_manager.update_component(
                name = f"{other_func_name}_func",
                component_class = Radiobutton,
                **{"state": "normal"}
            )

    def _load_image_by_channel_on_gui(self, *args):
        image_container_frame = self._image_viewer_window.component_manager.get_component(
            name = "image_container",
            component_class = Frame
        )
        for child_widget in image_container_frame.winfo_children():
            child_widget.destroy()

        current_color_mode = self._component_manager.get_component("color_mode", StringVar).get()
        current_other_func = self._component_manager.get_component("other_func", StringVar).get()

        if current_color_mode != "NORMAL":
            if current_color_mode == "RGB":
                splited_images = self._core.image_manager.optimized_image_split_by_channel(
                    channel_type = "RGB"
                )

            elif current_color_mode == "YUV":
                splited_images = self._core.image_manager.optimized_image_split_by_channel(
                    channel_type = "YUV"
                )

            else:
                splited_images = self._core.image_manager.optimized_image_split_by_channel(
                    channel_type = "GRAY"
                )

            if current_color_mode != "NORMAL" and current_color_mode != "GRAY":
                self._image_viewer_window.set_image(
                    image_datas = {
                        f"{channel.lower()}_image": (channel, ImageManager.convert_to_photoimage(
                            self._resize_image_by_gui_size(splited_images[idx], divide = 6, image_amount = 3)
                        ))
                        for idx, channel in enumerate(current_color_mode)
                    }
                )

            elif current_color_mode == "GRAY":
                self._image_viewer_window.set_image(
                    image_datas = {
                        "gray_image": ("GRAY", ImageManager.convert_to_photoimage(
                            self._resize_image_by_gui_size(splited_images[0])
                        ))
                    }
                )

        if current_other_func != "None":
            # "ud_flip", "lr_flip", "half_crop"
            result_image: Optional[Image] = None

            if current_other_func == "ud_flip":
                result_image = self._core.image_manager.optimized_rotate_image(rotate_type = "vertical")

            elif current_other_func == "lr_flip":
                result_image = self._core.image_manager.optimized_rotate_image(rotate_type = "horizontal")

            elif current_other_func == "half_crop":
                result_image = self._core.image_manager.crop_image()

            if result_image is not None:
                self._image_viewer_window.set_image(
                    {"other_func_result": (
                        current_other_func.replace("_", " ").upper(), ImageManager.convert_to_photoimage(
                            image = self._resize_image_by_gui_size(
                                image = result_image
                            )
                        )
                    )}
                )

    def _resize_image_by_gui_size(self, image: Image, divide: int = 2, image_amount: int = 1) -> Image:
        original_width, original_height = self._core.image_manager.loaded_image.size
        window_width = self.winfo_screenwidth()
        window_height = self.winfo_screenheight()

        window_width_half = window_width // divide
        window_height_half = window_height // divide

        resized_size: Optional[Tuple[int, int]] = None

        if window_width_half <= original_width or window_height_half <= original_height:
            if original_width > window_width_half:
                resized_width = window_width_half
                resized_height = int((window_width_half / original_width) * original_height)
                resized_size = (resized_width, resized_height)

            if original_height > window_height_half:
                resized_height = window_height_half
                resized_width = int((window_height_half / original_height) * original_width)
                resized_size = (resized_width, resized_height)

        if resized_size is not None:
            self._image_viewer_window.geometry(f"{image_amount * (resized_size[0] + 50)}x{resized_size[1] + 100}")
            return image.resize(resized_size)
        else:
            return image

    def _check_and_change_radiobtn_and_btn_status(self, *args):
        color_mode_value = self._component_manager.get_component("color_mode", StringVar).get()
        other_func_value = self._component_manager.get_component("other_func", StringVar).get()

        for func_name in ["ud_flip", "lr_flip", "half_crop"]:
            self._component_manager.update_component(
                name = f"{func_name}_func",
                component_class = Radiobutton,
                **{"state": "normal" if color_mode_value == "NORMAL" else "disabled"}
            )

        for color_mode in ["RGB", "YUV", "GRAY"]:
            self._component_manager.update_component(
                name = f"color_mode_select_{color_mode}",
                component_class = Radiobutton,
                **{"state": "normal" if other_func_value == "None" else "disabled"}
            )

        radio_select_check = (color_mode_value != "NORMAL") ^ (other_func_value != "None")

        self._component_manager.update_component(
            name = "apply",
            component_class = Button,
            **{"state": "normal" if radio_select_check else "disabled"}
        )

    def _update_image_list(self, *args):
        self._component_manager.update_component(
            name = "image_select",
            component_class = Combobox,
            **{"values": self._core.get_image_file_dirs()}
        )

    @property
    def core(self) -> PyImageViewerCore:
        return self._core

    @core.setter
    def core(self, value: PyImageViewerCore):
        self._core = value


if __name__ == '__main__':
    IC = ImageControllerGUI.create_gui()