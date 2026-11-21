"""hello-forge 的核心逻辑。

从这里开始实现你的业务代码。保持函数纯粹、命名清晰，并为每个公开函数
补充单元测试（见 tests/）。
"""


def hello(name: str = "world") -> str:
    """返回一句问候语。

    >>> hello("repo-forge")
    'Hello, repo-forge!'
    """
    if not isinstance(name, str) or not name.strip():
        raise ValueError("name 必须是非空字符串")
    return "Hello, %s!" % name.strip()
