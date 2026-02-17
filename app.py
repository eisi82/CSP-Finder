"""Streamlit entrypoint for the CSP Finder application."""

from csp_finder.ui.streamlit_app import create_app


def main() -> None:
    """Execute Streamlit application startup.

    Args:
        None.

    Returns:
        None: The function initializes and runs the UI application.
    """

    create_app().run()


if __name__ == "__main__":
    main()
