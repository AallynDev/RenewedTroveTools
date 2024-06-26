from flet import Image


class RTTImage(Image):
    def __init__(self, src=None, is_fallback=False, **kwargs):
        if is_fallback:
            super().__init__(src, **kwargs)
            return
        if isinstance(src, str) and src.startswith("assets/"):
            src = "https://kiwiapi.aallyn.xyz/v1/misc/" + src
        kwargs["src"] = src
        if kwargs.get("error_content") is None:
            error_content = RTTImage(
                src="https://kiwiapi.aallyn.xyz/v1/misc/assets/images/construction.png",
                is_fallback=True,
                width=kwargs.get("width"),
            )
            kwargs["error_content"] = error_content
        super().__init__(**kwargs)
