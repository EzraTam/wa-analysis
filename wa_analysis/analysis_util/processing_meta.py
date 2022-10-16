"""Function configurations for cleaning texts
"""

processing_by_re_meta = dict(
    url=dict(
        pattern=r"((www\.[^\s]+)|(https?://[^\s]+))",
        replacement_str="url",
        capture=True,
    ),
    at_user=dict(pattern=r"@[A-Za-z0-9]+", replacement_str="at_user", capture=True),
    additional_white_space=dict(pattern=r"[\s]+", replacement_str=" ", capture=False),
    hash_tag=dict(pattern=r"#([^\s]+)", replacement_str=r"\1", capture=True),
)
