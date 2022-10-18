"""Function configurations for cleaning texts
"""

import re

processing_by_re_meta = dict(
    url=dict(
        pattern=r"((www\.[^\s]+)|(https?://[^\s]+))",
        replacement_str="url",
        flags=0,
        capture=True,
    ),
    at_user=dict(pattern=r"@[A-Za-z0-9]+", replacement_str="at_user", flags=0, capture=True),
    additional_white_space=dict(pattern=r"[\s]+", replacement_str=" ", flags=0, capture=False),
    hash_tag=dict(pattern=r"#([^\s]+)", replacement_str=r"\1", flags=0, capture=True),
    emoji= dict(
        pattern="["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "]+",
        replacement_str=" ",
        flags=re.UNICODE,
        capture=True
    )
)
