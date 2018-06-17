"""
Purpose: demostration of triangle mesh generation

Date: 2018-06
Author: kouui
"""

import matplotlib.pyplot as plt
import matplotlib.tri as tri
import numpy as np
import matplotlib.path as mpltPath

def moved_and_pressed(event):

    if event.button==1:
        x = np.append(line.get_xdata(), event.xdata)
        y = np.append(line.get_ydata(), event.ydata)
        line.set_data(x, y)
        fig.canvas.draw()

def released(event):
    if event.button==1:
        plt.close(fig)

if __name__ == "__main__":

    #-- get polygon
    fig, ax = plt.subplots(1,1, figsize=(7,5), dpi=100)
    line, = ax.plot([], [], 'k')
    ax.set_xlim(0,5); ax.set_ylim(0,5)
    cid1 = fig.canvas.mpl_connect('motion_notify_event', moved_and_pressed)
    cid2 = fig.canvas.mpl_connect('button_release_event', released)
    plt.show()

    n_bc = 30
    step = int(line.get_xydata().shape[0]/n_bc)
    boundary_points = line.get_xydata()[:-10:step,:].copy()
    polygon = np.vstack((boundary_points, boundary_points[0,:]))
    path = mpltPath.Path(polygon)

    #-- generate random distribution
    xlim = (boundary_points[:,0].min(),boundary_points[:,0].max())
    ylim = (boundary_points[:,1].min(),boundary_points[:,1].max())

    n_in = 80; index = 0
    interior_points = np.empty((n_in,2),dtype=np.double)
    while index<n_in:
        p = np.array([np.random.uniform(low=ylim[0],high=ylim[1],size=1)[0],np.random.uniform(low=xlim[0],high=xlim[1],size=1)[0]]).reshape(1,2)
        if path.contains_points(p):
            interior_points[index,:] = p[:]
            index += 1

    #-- create triangle mesh
    all_points = np.vstack((boundary_points,interior_points))
    triang = tri.Triangulation(all_points[:,0], all_points[:,1])

    #-- mask those outside the boundary
    ymid = all_points[:,0][triang.triangles].mean(axis=1).reshape(-1,1)
    xmid = all_points[:,1][triang.triangles].mean(axis=1).reshape(-1,1)
    mid_points = np.hstack((ymid,xmid))
    mask = path.contains_points(mid_points)
    triang.set_mask(np.logical_not(mask))


    #-- show points
    if False:
        fig, ax = plt.subplots(1,1, figsize=(7,5), dpi=100)
        ax.plot(interior_points[:,0],interior_points[:,1], 'ok', markersize=3)
        ax.plot(polygon[:,0],polygon[:,1], 'ok--', markersize=4, markerfacecolor="None",markeredgecolor="black",markeredgewidth=1)
        plt.show()

    #-- show mesh
    if True:
        fig, ax = plt.subplots(1,1, figsize=(7,5), dpi=100)
        ax.triplot(triang, 'ko-', linewidth=1,markersize=4, markerfacecolor="None",markeredgecolor="black",markeredgewidth=1)
        plt.show()
