import os
import pathlib
from string import Template


class Builder:
    def build(self, name: str, src_dir: str, dest_dir: str) -> None:
        for src_path in pathlib.Path(src_dir).glob("**/*.txt"):
            content = src_path.read_text()
            new_content = Template(content).substitute(
                {"flow_name": name, "class_name": self.__class__.to_title_case(name)}
            )

            relative_path = src_path.relative_to(src_dir).with_suffix("")
            if str(relative_path) == "__main__.py":
                dest_path = pathlib.Path(dest_dir).joinpath(
                    os.path.normpath(f"{name}.py")
                )
            else:
                dest_path = pathlib.Path(dest_dir).joinpath(relative_path)

            dest_path.parent.mkdir(parents=True, exist_ok=True)
            dest_path.write_text(new_content)

    @staticmethod
    def to_title_case(snake_case_string: str) -> str:
        return "".join(s.title() for s in snake_case_string.split("_"))
