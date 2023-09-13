import unittest
from mylib import ShapesAdmin

class TestShapesAdmin(unittest.TestCase):

    def setUp(self):
        self.shapesAdmin = ShapesAdmin()
    
    def test_count_square(self):
        self.assertEqual(round(self.shapesAdmin.count_square('circle', 5), 5), 78.53982)
        self.assertEqual(round(self.shapesAdmin.count_square('triangle', 5, 7, 8), 5), 17.32051)
        self.assertEqual(self.shapesAdmin.count_square('triangle_right', 4, 2), 4)
        self.assertIsNone(self.shapesAdmin.count_square('abc', 7))
        self.assertIsNone(self.shapesAdmin.count_square('circle', 7, 8))
        self.assertIsNone(self.shapesAdmin.count_square('circle', '5'))

    def test_is_right_triangle(self):
        self.assertFalse(self.shapesAdmin.is_right_triangle((10, 5, 8)))
        self.assertFalse(self.shapesAdmin.is_right_triangle((3, 4, 5, 6)))
        self.assertFalse(self.shapesAdmin.is_right_triangle((10, 5, '8')))
        self.assertTupleEqual(self.shapesAdmin.is_right_triangle((3, 4, 5)), (3, 4))
        self.assertTupleEqual(self.shapesAdmin.is_right_triangle((4, 3, 5)), (4, 3))
        self.assertTupleEqual(self.shapesAdmin.is_right_triangle((3, 5, 4)), (3, 4))
        self.assertTupleEqual(self.shapesAdmin.is_right_triangle((4, 5, 3)), (4, 3))
        self.assertTupleEqual(self.shapesAdmin.is_right_triangle((5, 3, 4)), (3, 4))
        self.assertTupleEqual(self.shapesAdmin.is_right_triangle((5, 4, 3)), (4, 3))

    def test_available_shapes(self):
        self.assertSetEqual(set(self.shapesAdmin.available_shapes()), {'circle', 'triangle', 'triangle_right'})
        self.shapesAdmin.add_shape('rectangle', lambda a, b: a*b)
        self.assertSetEqual(set(self.shapesAdmin.available_shapes()), {'circle', 'triangle', 'triangle_right', 'rectangle'})


    def test_add_shape(self):
        available_shapes_old = self.shapesAdmin.available_shapes()
        self.shapesAdmin.add_shape('rectangle', lambda a, b: a*b)
        self.assertIn('rectangle', set(self.shapesAdmin.available_shapes())-set(available_shapes_old))
        available_shapes_old = self.shapesAdmin.available_shapes()
        self.shapesAdmin.add_shape('rect', 5)
        self.assertNotIn('rect', set(self.shapesAdmin.available_shapes())-set(available_shapes_old))
        available_shapes_old = self.shapesAdmin.available_shapes()
        self.shapesAdmin.add_shape(6, lambda a, b: a*b)
        self.assertNotIn(6, set(self.shapesAdmin.available_shapes())-set(available_shapes_old))


    def test_del_shape(self):
        self.shapesAdmin.del_shape('circle')
        self.assertNotIn('circle', self.shapesAdmin.available_shapes())
        self.shapesAdmin.del_shape('circ')
        self.assertNotIn('circ', self.shapesAdmin.available_shapes())

if __name__ == '__main__':
    unittest.main()