"""ReportLab vector drawing for the Homogeneous Speed Logistics mark."""

from __future__ import annotations

from reportlab.graphics.shapes import Drawing, Path
from reportlab.lib.colors import HexColor

BRAND_TEAL = HexColor("#3bb6ff")
BRAND_DARK = HexColor("#1d7bb3")

# SVG path commands in the supplied 1600 ? 881 viewBox. Quadratic curves are
# converted to cubic B?zier curves when added to the ReportLab drawing.
_MARK_PATHS = (
    ("dark", (("M", 813, 0), ("L", 778, 83), ("Q", 640, 115, 542, 225),
               ("Q", 600, 80, 813, 0), ("Z",))),
    ("dark", (("M", 1213, 33), ("L", 1185, 109),
               ("C", 800, 150, 590, 220, 479, 356),
               ("C", 560, 130, 800, 80, 1213, 33), ("Z",))),
    ("light", (("M", 1477, 117), ("L", 1600, 235), ("L", 1400, 278),
                ("L", 1418, 241), ("C", 800, 235, 520, 350, 387, 537),
                ("C", 470, 330, 700, 155, 1460, 153), ("Z",))),
)


def create_logo_drawing(width: float = 90, height: float = 90) -> Drawing:
    """Return the supplied speed mark as a scalable ReportLab vector."""
    drawing = Drawing(width, height)
    sx, sy = width / 1600, height / 881

    def point(x: float, y: float, mirrored: bool) -> tuple[float, float]:
        if mirrored:
            x, y = 1600 - x, 881 - y
        return x * sx, height - y * sy

    for mirrored in (False, True):
        for color_name, commands in _MARK_PATHS:
            path = Path()
            path.fillColor = BRAND_DARK if color_name == "dark" else BRAND_TEAL
            path.strokeColor = None
            current = (0.0, 0.0)
            start = (0.0, 0.0)
            for command in commands:
                op, *args = command
                if op == "M":
                    current = (args[0], args[1])
                    start = current
                    path.moveTo(*point(*current, mirrored))
                elif op == "L":
                    current = (args[0], args[1])
                    path.lineTo(*point(*current, mirrored))
                elif op == "C":
                    c1 = (args[0], args[1])
                    c2 = (args[2], args[3])
                    current = (args[4], args[5])
                    path.curveTo(*point(*c1, mirrored), *point(*c2, mirrored),
                                 *point(*current, mirrored))
                elif op == "Q":
                    control = (args[0], args[1])
                    end = (args[2], args[3])
                    c1 = (current[0] + 2 * (control[0] - current[0]) / 3,
                          current[1] + 2 * (control[1] - current[1]) / 3)
                    c2 = (end[0] + 2 * (control[0] - end[0]) / 3,
                          end[1] + 2 * (control[1] - end[1]) / 3)
                    path.curveTo(*point(*c1, mirrored), *point(*c2, mirrored),
                                 *point(*end, mirrored))
                    current = end
                elif op == "Z":
                    path.closePath()
                    current = start
            drawing.add(path)
    return drawing
