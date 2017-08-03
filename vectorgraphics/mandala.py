import numpy as np


def rotate(verts, theta=np.pi/2):

    r = np.array([
        [np.cos(theta), - np.sin(theta)],
        [np.sin(theta), np.cos(theta)]
    ])

    return verts.dot(r)


def mandalate(verts, times=4, reflect=True):

    vertss = []
    # import pudb; pu.db()
    verts_compliment = np.array(list(zip(verts[:,1], verts[:,0])))


    for theta in np.linspace(0.0, np.pi * 2.0, times + 1):
        vertss.append(rotate(verts, theta))
        if reflect:
            vertss.append(rotate(verts_compliment, theta))

    return vertss
