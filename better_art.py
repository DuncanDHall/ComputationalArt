""" This is a pretty jank implementation, but it does allow a seed to be
    created which makes the different color channels blend better together.
    It's not that different from my original, just with functions in the
    lists directly. Check out actually_better_art.py for some better
    plotting (courtesy of Oliver Steele)
"""

import random
from PIL import Image
from math import pi, cos, sin, sqrt
from inspect import getargspec, getmembers, isfunction


class Functions(object):
    """ a collection of the building block functions to be used for easy addition
        of new functions. Make sure to decorate it with @staticmethod though.
    """

    @staticmethod
    def prod(a, b):
        return a * b

    @staticmethod
    def avg(a, b):
        return (a + b) / 2.0

    @staticmethod
    def cos_pi(a):
        return cos(pi * a)

    @staticmethod
    def sin_pi(a):
        return sin(pi * a)

    @staticmethod
    def sqrt(a):
        try:
            return sqrt(a)
        except:
            return -sqrt(-a)

    @staticmethod
    def square(a):
        return a**2

    class base(object):
        pass


def build_random_function(min_depth, max_depth, seed=None):
    """ Builds a random function of depth at least min_depth and depth
        at most max_depth (see assignment writeup for definition of depth
        in this context)
        min_depth: the minimum depth of the random function
        max_depth: the maximum depth of the random function
        returns: the randomly generated function represented as a nested
            tuple of the form: ((function_name, <function>), (args,))
        >>> build_random_function(1, 1)
    """
    # functions = [
    #     ('prod', 2),
    #     ('avg', 2),
    #     ('cos_pi', 1),
    #     ('sin_pi', 1),
    #     ('sqrt', 1),
    #     ('square', 1)
    #     ]

    function_list = getmembers(Functions(), isfunction)
    # for f in function_list:
    #     print f

    def recurse(min_depth, max_depth, root=None):
        if random.randint(min_depth, max_depth) <= 0:
            if root is not None:
                return root
            # sometimes we end up averaging "y" with "y", but wuduva
            else:
                return random.choice(["x", "y"])
        else:
            function = random.choice(function_list)
            args = [recurse(min_depth-1, max_depth-1) for arg
                    in getargspec(function[1]).args]
            return [function, args]

    def further_recurse(min_deeper, max_deeper, function):
        f = function[0]
        if f == "x":
            return recurse(min_deeper, max_deeper, "x")
        elif f == "y":
            return recurse(min_deeper, max_deeper, "y")
        else:
            return [f, [
                further_recurse(min_deeper, max_deeper, arg)
                for arg in function[1]]]

    # def recurse(min_depth, max_depth, root=None):
    #     if random.randint(min_depth, max_depth) <= 0:
    #         if root is not None:
    #             return root
    #         # sometimes we end up averaging "y" with "y", but wuduva
    #         else:
    #             return random.choice(["x", "y"])
    #     else:
    #         function = random.choice(function_list)
    #         args = tuple(recurse(min_depth-1, max_depth-1) for arg
    #                      in getargspec(function[1]).args)
    #         return (function, args)

    # def further_recurse(min_deeper, max_deeper, function):
    #     f = function[0]
    #     # pdb.set_trace()
    #     if f == "x":
    #         return recurse(min_deeper, max_deeper, "x")
    #     elif f == "y":
    #         return recurse(min_deeper, max_deeper, "y")
    #     else:
    #         return (f, tuple(
    #             further_recurse(min_deeper, max_deeper, arg)
    #             for arg in function[1]))

    if seed is None:
        return recurse(min_depth, max_depth)
    else:
        function = further_recurse(min_depth, max_depth, seed)
        print "$$$$$$$"
        print function
        print "$$$$$$$"
        return function


def evaluate_random_function(f, x, y):
    """ Evaluate the random function f with inputs x,y
        Representation of the function f is defined in the assignment writeup
        f: the function to evaluate in following form:
            ((function_name, <function>), (inputs))
        x: the value of x to be used to evaluate the function
        y: the value of y to be used to evaluate the function
        returns: the function value
        >>> evaluate_random_function(["x"],-0.5, 0.75)
        -0.5
        >>> evaluate_random_function(["y"],0.1,0.02)
        0.02
    """

    if f == "x":
        return x
    elif f == "y":
        return y
    else:
        function = f[0][1]
        raw_args = f[1]
        args = tuple(evaluate_random_function(arg, x, y) for arg in raw_args)
        return function(*args)


def remap_interval(val,
                   input_interval_start,
                   input_interval_end,
                   output_interval_start,
                   output_interval_end):
    """ Given an input value in the interval [input_interval_start,
        input_interval_end], return an output value scaled to fall within
        the output interval [output_interval_start, output_interval_end].
        val: the value to remap
        input_interval_start: the start of the interval that contains all
                              possible values for val
        input_interval_end: the end of the interval that contains all possible
                            values for val
        output_interval_start: the start of the interval that contains all
                               possible output values
        output_inteval_end: the end of the interval that contains all possible
                            output values
        returns: the value remapped from the input to the output interval
        >>> remap_interval(0.5, 0, 1, 0, 10)
        5.0
        >>> remap_interval(5, 4, 6, 0, 2)
        1.0
        >>> remap_interval(5, 4, 6, 1, 2)
        1.5
    """
    # TODO: get rid of this
    prop_val = ((val - input_interval_start) /
                float(input_interval_end - input_interval_start))
    return (prop_val * (output_interval_end - output_interval_start) +
            output_interval_start)


def color_map(val):
    """ Maps input value between -1 and 1 to an integer 0-255, suitable for
        use as an RGB color code.
        val: value to remap, must be a float in the interval [-1, 1]
        returns: integer in the interval [0,255]
        >>> color_map(-1.0)
        0
        >>> color_map(1.0)
        255
        >>> color_map(0.0)
        127
        >>> color_map(0.5)
        191
    """
    # NOTE: This relies on remap_interval, which you must provide
    # color_code = remap_interval(val, -1, 1, 0, 255)
    # return int(color_code)

    return int((val + 1) * 255 / 2)


def test_image(filename, x_size=350, y_size=350):
    """ Generate test image with random pixels and save as an image file.
        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            # x = remap_interval(i, 0, x_size, -1, 1)
            # y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (random.randint(0, 255),  # Red channel
                            random.randint(0, 255),  # Green channel
                            random.randint(0, 255))  # Blue channel

    im.save(filename)


def generate_art(filename, x_size=350, y_size=350):
    """ Generate computational art and save as an image file.
        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    seed_function = build_random_function(1, 2)
    print "&&&&&&&&&&&"
    print seed_function
    print "&&&&&&&&&&&"

    # Functions for red, green, and blue channels - where the magic happens!
    red_function = build_random_function(1, 2, seed_function)
    green_function = build_random_function(1, 2, seed_function)
    blue_function = build_random_function(1, 2, seed_function)

    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            # x = i*2.0 / x_size - 1
            y = remap_interval(j, 0, y_size, -1, 1)
            # y = j*2.0 / y_size - 1

            pixels[i, j] = (
                    color_map(evaluate_random_function(red_function, x, y)),
                    color_map(evaluate_random_function(green_function, x, y)),
                    color_map(evaluate_random_function(blue_function, x, y))
                    )

    im.save(filename)


if __name__ == '__main__':
    # function = build_random_function(1, 2)
    # print evaluate_random_function(function, 5, 6)

    # import doctest
    # # doctest.testmod()
    # doctest.run_docstring_examples(color_map,
    #                                globals(), verbose=True,
    #                                name="Jus' Testin'")

    # Create some computational art!
    # TODO: Un-comment the generate_art function call after you
    #       implement remap_interval and evaluate_random_function
    generate_art("myart.png")

    # Test that PIL is installed correctly
    # TODO: Comment or remove this function call after testing PIL install
    # test_image("noise.png")
