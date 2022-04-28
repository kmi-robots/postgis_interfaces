import argparse
import math
import random

import numpy as np

from postgis_connection import PostgisInterface
import cv2

args = dict()
args['image'] = '/home/gianluca/development/postgis_interfaces/kmi_turtlebot_launch/map/map_small.pgm'
args['resolution'] = 0.05
args['x'] = -7.5
args['y'] = -10

tlist = ['2020-05-15-11-04-05_991139',
         '2020-05-15-11-12-27_125515',
         '2020-05-15-11-23-42_195173',
         '2020-05-15-11-03-03_130652',
         '2020-05-15-11-00-52_581669',
         '2020-05-15-11-00-57_141515',
         '2020-05-15-11-07-36_376642',
         '2020-05-15-11-24-12_379522',
         '2020-05-15-11-15-17_674018',
         '2020-05-15-11-13-44_030269',
         '2020-05-15-11-01-29_153828',
         '2020-05-15-11-00-09_353079',
         '2020-05-15-11-15-14_046537',
         '2020-05-15-11-07-23_464388',
         '2020-05-15-11-11-05_493567']


def poses(timestamp):
    query = 'select ST_X(robot_position), ST_Y(robot_position), robot_yaw ' \
            'from semantic_map ' \
            'where object_id LIKE \'' + timestamp + '%\' limit 1'
    return query


def all_poses():
    query = 'select distinct ST_X(robot_position), ST_Y(robot_position), robot_yaw ' \
            'from semantic_map '
    return query


def to_pixel(xc, yc):
    xp = math.floor((xc - args['x']) / args['resolution'])
    yp = height - math.floor((yc - args['y']) / args['resolution'])
    return xp, yp


if __name__ == '__main__':

    # ap = argparse.ArgumentParser()
    # ap.add_argument("-i", "--image", required=True, help="Path to the image")
    # ap.add_argument("-r", "--resolution", required=True, type=float, help="Resolution")
    # ap.add_argument("-x", required=True, type=float, help="Origin x")
    # ap.add_argument("-y", required=True, type=float, help="Origin y")
    # args = vars(ap.parse_args())

    img = image = cv2.imread(args["image"])
    height, width = img.shape[:2]

    db_interface = PostgisInterface()
    db_interface.connect_db('gianluca', 'gis_database')

    records = db_interface.query_db(all_poses())
    for r in records:
        x = math.floor((r[0] - args['x']) / args['resolution'])
        y = height - math.floor((r[1] - args['y']) / args['resolution'])
        cv2.circle(img, (x, y), 4, (255, 0, 0), -1)

    # samples = random.sample(records, 15)
    #
    # for t in samples:
    #
    #     xx = t[0]
    #     yy = t[1]
    #
    #     x1 = 2 * math.cos(t[2] - 0.52)
    #     y1 = 2 * math.sin(t[2] - 0.52)
    #     x1p, y1p = to_pixel(xx + x1, yy + y1)
    #
    #     x2 = 2 * math.cos(t[2] + 0.52)
    #     y2 = 2 * math.sin(t[2] + 0.52)
    #     x2p, y2p = to_pixel(xx + x2, yy + y2)
    #
    #     x, y = to_pixel(xx, yy)
    #
    #     contours = np.array([[x, y], [x1p, y1p], [x2p, y2p]])
    #     cv2.fillPoly(img, np.int32([contours]), color=(153, 255, 255))
    #
    #     cv2.line(img, (x, y), (x1p, y1p), (0, 0, 0), 1)
    #     cv2.line(img, (x1p, y1p), (x2p, y2p), (0, 0, 0), 1)
    #     cv2.line(img, (x2p, y2p), (x, y), (0, 0, 0), 1)
    #
    #     cv2.circle(img, (x, y), 5, (0, 255, 0), -1)

    tlist.reverse()

    for t in tlist:
        records = db_interface.query_db(poses(t))

        xx = records[0][0]
        yy = records[0][1]

        x1 = 2 * math.cos(records[0][2] - 0.52)
        y1 = 2 * math.sin(records[0][2] - 0.52)
        x1p, y1p = to_pixel(xx + x1, yy + y1)

        x2 = 2 * math.cos(records[0][2] + 0.52)
        y2 = 2 * math.sin(records[0][2] + 0.52)
        x2p, y2p = to_pixel(xx + x2, yy + y2)

        x, y = to_pixel(xx, yy)

        contours = np.array([[x, y], [x1p, y1p], [x2p, y2p]])
        cv2.fillPoly(img, np.int32([contours]), color=(153, 255, 255))

        cv2.line(img, (x, y), (x1p, y1p), (0, 0, 0), 1)
        cv2.line(img, (x1p, y1p), (x2p, y2p), (0, 0, 0), 1)
        cv2.line(img, (x2p, y2p), (x, y), (0, 0, 0), 1)

        cv2.circle(img, (x, y), 5, (0, 255, 0), -1)

    x0 = math.floor(math.fabs(args['x']) / args['resolution'])
    y0 = height - math.floor(math.fabs(args['y']) / args['resolution'])

    # cv2.circle(img, (x0, y0), 3, (0, 0, 255), 3, cv2.FILLED)
    cv2.imshow('Image', img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
