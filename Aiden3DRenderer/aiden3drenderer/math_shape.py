import math

from .renderer import register_shape

class MathShape:
    def __init__(self, name:str, pygame_key: int, function: str, color: tuple[int,int,int] = (100, 20, 200), grid_size:int = 20, y_range=(-10, 10), y_resolution=0.2, centered=True, is_animated=False):
        self.name = name
        self.key = pygame_key
        self.function = function
        self.color = color
        self.grid_size = grid_size
        self.y_range = y_range
        self.y_res = y_resolution
        self.centered = centered
        self.is_animated = is_animated

        self.register_self()

    def register_self(self):
        @register_shape(self.name, self.key, self.is_animated, self.color)
        def shape(grid_size = self.grid_size, time = 0):
            return self.generate_shape_from_equation(self.function, grid_size, self.y_range, self.y_res, time, centered=self.centered)
        
        
    def generate_shape_from_equation(self, equation: str, grid_size=30, y_range=(-10, 10), y_resolution=0.2, time=0, centered=True):

        gridCoords = []

        env = {k: getattr(math, k) for k in dir(math) if not k.startswith("_")}
        env.update({
            "abs": abs,
            "max": max,
            "min": min,
            "pow": pow
        })

        cx = grid_size / 2 if centered else 0
        cz = grid_size / 2 if centered else 0

        is_implicit = "y" in equation and "=" not in equation

        for x_i in range(grid_size):
            row = []
            for z_i in range(grid_size):

                x = x_i - cx
                z = z_i - cz

                env["x"] = x
                env["z"] = z
                env["t"] = time

                if not is_implicit:
                    y = eval(equation, {}, env)

                else:
                    best_y = None
                    best_val = float("inf")

                    y_min, y_max = y_range
                    steps = int((y_max - y_min) / y_resolution)

                    for i in range(steps):
                        y_test = y_min + i * y_resolution
                        env["y"] = y_test

                        val = eval(equation, {}, env)

                        if abs(val) < best_val:
                            best_val = abs(val)
                            best_y = y_test

                        if abs(val) < 0.01:
                            best_val = abs(val)
                            best_y = y_test
                            break

                    y = best_y if best_y is not None else 0

                row.append((x, y, z))

            gridCoords.append(row)

        return gridCoords
