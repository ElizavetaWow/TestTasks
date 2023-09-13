import math

class ShapesAdmin:
    """ Counting squares of shapes """

    def __init__(self):
        self.shapes = {}
        self.add_shape('circle', lambda r: math.pi*r**2)
        self.add_shape('triangle', lambda a, b, c: (lambda p=((a + b + c)/2) : (p*(p-a)*(p-b)*(p-c))**0.5)())
        self.add_shape('triangle_right', lambda a, h: a*h/2)


    def count_square(self, name, *params):
        if name not in self.shapes.keys():
            print("There is no such shape in this lib. You can add it by the add_shape function")
            return
        try:
            if 'triangle' in name:
                if checked := self.is_right_triangle(params):
                    name = 'triangle_right'
                    params = checked
            result = self.shapes[name](*params)
        except TypeError:
            print("There are problems with your params. Check their amount and type")
            return
        return result
    

    def is_right_triangle(self, params):
        try:
            if len(params) == 3:
                if params[0]**2+params[1]**2 == params[2]**2:
                    return params[0], params[1]
                if params[0]**2+params[2]**2 == params[1]**2:
                    return params[0], params[2]
                if params[2]**2+params[1]**2 == params[0]**2:
                    return  params[1], params[2]
        except TypeError:
            print("There are problems with your params. Check their amount and type")
        return False
    
    def available_shapes(self):
        return list(self.shapes.keys()) 

    def add_shape(self, name:str, square_formula: callable):
        if isinstance(name, str) and callable(square_formula):
            self.shapes[name] = square_formula

    def del_shape(self, name:str):

        self.shapes.pop(name, None)
