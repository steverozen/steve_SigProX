try:
    from .version import short_version as __version__
except Exception:
    try:
        from importlib.metadata import PackageNotFoundError, version
    except Exception:  # pragma: no cover
        PackageNotFoundError = Exception  # type: ignore

        def version(_name: str) -> str:  # type: ignore
            raise PackageNotFoundError()

    try:
        __version__ = version("SigProfilerExtractor")
    except PackageNotFoundError:
        __version__ = "0+unknown"
