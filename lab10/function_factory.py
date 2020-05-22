class FunctionFactory:
    @staticmethod
    def trapezoidalRegion(a, b, c, d):
        return lambda x: max(0, min((x - a) / (b - a), 1, (d - x) / (d - c)))

    @staticmethod
    def triangularRegion(a, b, c):
        return FunctionFactory.trapezoidalRegion(a, b, b, c)

    @staticmethod
    def inverseLine(a, b):
        return lambda val: val * (b - a) + a

    @staticmethod
    def inverseTriangular(a, b, c):
        return lambda val: (FunctionFactory.inverseLine(a, b)(val) + FunctionFactory.inverseLine(c, b)(val)) / 2