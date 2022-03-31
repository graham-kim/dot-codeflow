import typing as tp

class DotLink:
    def __init__(self, src: str, dst: str, tags: str=None, label: str=None):
        self.src = src
        self.dst = dst
        self.tags = tags
        self.label = label

    def __str__(self) -> str:
        ans = f"    {self.src} -> {self.dst}"
        if self.tags and self.label:
            ans += f' [{self.tags} label={self.label}]'
        elif self.tags:
            ans += f" [{self.tags}]"
        elif self.label:
            ans += f' [label="{self.label}"]'

        return f"{ans}\n"