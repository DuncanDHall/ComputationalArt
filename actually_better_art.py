""" This is a pretty jank implementation that maybe I'll come back to,
    probs not though...
"""

from PIL import Image
import numpy as np
from math import pi
import pdb


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

    def root(a):
        return np.sqrt(np.abs(a))

    functions = {
        "prod": lambda a, b: a * b,
        "avg": lambda a, b: (a + b) / 2.0,
        "cos_pi": lambda a: np.cos(pi * a),
        "sin_pi": lambda a: np.sin(pi * a),
        "sqrt": root,
        "square": lambda a: a**2
    }

    n_args = {
        "prod": 2,
        "avg": 2,
        "cos_pi": 1,
        "sin_pi": 1,
        "sqrt": 1,
        "square": 1
    }

    function_list = functions.keys()

    def recurse(min_depth, max_depth, root=None):
        if np.random.randint(min_depth, max_depth) <= 0:
            if root is not None:
                if root == "x":
                    return lambda x, y: x
                elif root == "y":
                    return lambda x, y: y
            # sometimes we end up averaging "y" with "y", but wuduva
            else:
                return np.random.choice([lambda x, y: x, lambda x, y: y])
        else:
            function_name = np.random.choice(function_list)
            function = functions[function_name]
            args = [recurse(min_depth-1, max_depth-1, root) for _
                    in range(n_args[function_name])]
            return lambda x, y: function(*[arg(x, y) for arg in args])

    return recurse(min_depth, max_depth)


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
    color_code = remap_interval(val, -1, 1, 0, 255)
    return color_code.astype('uint8')


def generate_art(
        filename, x_size=350, y_size=350,
        pallet=((1.0, 0, 0), (0, 1.0, 0), (0, 0, 1.0))):
    """ Generate computational art and save as an image file.
        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """

    c1, c2, c3 = pallet
    print c1

    # Functions for red, green, and blue channels - where the magic happens!
    c1_function = build_random_function(5, 7)
    c2_function = build_random_function(5, 7)
    c3_function = build_random_function(5, 7)

    # Create image as array, then barf over all pixels at once
    # pdb.set_trace()
    x = np.tile(np.linspace(-1, 1, x_size), (y_size, 1))
    y = np.tile(np.linspace(-1, 1, y_size), (x_size, 1)).T
    r = (c1_function(x, y)*c1[0] +
         c2_function(x, y)*c2[0] +
         c3_function(x, y)*c3[0]) / 2.0
    g = (c1_function(x, y)*c1[1] +
         c2_function(x, y)*c2[1] +
         c3_function(x, y)*c3[1]) / 2.0
    b = (c1_function(x, y)*c1[2] +
         c2_function(x, y)*c2[2] +
         c3_function(x, y)*c3[2]) / 2.0
    pixels = color_map(np.dstack((r, g, b)))
    im = Image.fromarray(pixels, "RGB")
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
    generate_art("myart.png", pallet=(
        (252/255.0, 0/255.0, 255/255.0),
        (0/255.0, 255/255.0, 213/255.0),
        (204/255.0, 164/255.0, 20/255.0)))

    # Test that PIL is installed correctly
    # TODO: Comment or remove this function call after testing PIL install
    # test_image("noise.png")
