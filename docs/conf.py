from aiosend import __version__
from datetime import datetime, UTC

project = "aiosend"
copyright = f"{datetime.now(UTC).year}, VoVcHiC"
author = "VoVcHiC"
release = __version__

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx_copybutton",
    "sphinxext.opengraph",
    "sphinx_autodoc_typehints",
]

locale_dirs = ["locale/"]
gettext_compact = False

templates_path = ["_templates"]

html_theme = "furo"
html_static_path = ["_static"]
html_copy_source = False
html_logo = "_static/logo.png"

ogp_site_url = "https://aiosend.readthedocs.io/en/latest/"
ogp_site_name = "aiosend documentation"
ogp_description_length = 0
ogp_social_cards = {"image_mini": "_static/rtd.ico"}

html_css_files = ["extra.css", "snow.css"]
html_js_files = ["snow.js"]

html_theme_options = {
    "light_css_variables": {
        "color-header-text": "#3fa3dd",
        "color-brand-primary": "#3fa3dd",
        "color-brand-content": "#3fa3dd",
        "color-api-name": "#3fa3dd",
        "color-api-pre-name": "#3fa3dd",
        "color-link--visited": "#3fa3dd",
        "color-highlight-on-target": "#aaddff",
        "font-stack": "Inter, sans-serif",
        "font-stack--headings": "Inter, sans-serif",
    },
    "dark_css_variables": {
        "color-highlight-on-target": "#223355",
    },
    "footer_icons": [
        {
            "name": "GitHub",
            "url": "https://github.com/vovchic17/aiosend",
            "html": """
                <svg stroke="currentColor" fill="currentColor" stroke-width="0" viewBox="0 0 16 16">
                    <path fill-rule="evenodd" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0 0 16 8c0-4.42-3.58-8-8-8z"></path>
                </svg>
            """,
            "class": "",
        },
        {
            "name": "Telegram chat",
            "url": "https://aiosend.t.me",
            "html": """
                <svg width="800px" height="800px" viewBox="0 0 240 240" id="svg2" xmlns="http://www.w3.org/2000/svg"><style>.st0{fill:url(#path2995-1-0_1_)}.st1{fill:#c8daea}.st2{fill:#a9c9dd}.st3{fill:url(#path2991_1_)}</style><linearGradient id="path2995-1-0_1_" gradientUnits="userSpaceOnUse" x1="-683.305" y1="534.845" x2="-693.305" y2="511.512" gradientTransform="matrix(6 0 0 -6 4255 3247)"><stop offset="0" stop-color="#37aee2"/><stop offset="1" stop-color="#1e96c8"/></linearGradient><path id="path2995-1-0" class="st0" d="M240 120c0 66.3-53.7 120-120 120S0 186.3 0 120 53.7 0 120 0s120 53.7 120 120z"/><path id="path2993" class="st1" d="M98 175c-3.9 0-3.2-1.5-4.6-5.2L82 132.2 152.8 88l8.3 2.2-6.9 18.8L98 175z"/><path id="path2989" class="st2" d="M98 175c3 0 4.3-1.4 6-3 2.6-2.5 36-35 36-35l-20.5-5-19 12-2.5 30v1z"/><linearGradient id="path2991_1_" gradientUnits="userSpaceOnUse" x1="128.991" y1="118.245" x2="153.991" y2="78.245" gradientTransform="matrix(1 0 0 -1 0 242)"><stop offset="0" stop-color="#eff7fc"/><stop offset="1" stop-color="#ffffff"/></linearGradient><path id="path2991" class="st3" d="M100 144.4l48.4 35.7c5.5 3 9.5 1.5 10.9-5.1L179 82.2c2-8.1-3.1-11.7-8.4-9.3L55 117.5c-7.9 3.2-7.8 7.6-1.4 9.5l29.7 9.3L152 93c3.2-2 6.2-.9 3.8 1.3L100 144.4z"/></svg>
            """,
            "class": "",
        },
    ],
}
