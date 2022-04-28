import argparse
import cv2
import math
import postgis_connection


def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.circle(img, (x, y), 3, (0, 0, 255), 3, cv2.FILLED)
        points.append((x, y))
        xm = args['x'] + x * args['resolution']
        ym = args['y'] + (height - y) * args['resolution']
        translated_points.append((xm, ym))
        print("coordinates: (%f, %f)" % (xm, ym))
        if len(points) >= 2:
            cv2.line(img, points[-1], points[-2], (255, 0, 0), 5, cv2.LINE_AA)
    if event == cv2.EVENT_RBUTTONDOWN:
        cv2.line(img, points[-1], points[0], (255, 0, 0), 5, cv2.LINE_AA)
        translated_points.append(translated_points[0])
        db_interface.modify_db(insert_areas(translated_points))
        points.clear()
        translated_points.clear()
    cv2.imshow('Image', img)


def insert_areas(points_list):
    query = "INSERT INTO forbidden_areas(area, stamp) VALUES(ST_MakePolygon('LINESTRING("
    for p in points_list:
        query = query+str(p[0])+" "+str(p[1])+","
    query = query[:-1]
    query = query+")'), CURRENT_TIMESTAMP);"

    return query


ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the image")
ap.add_argument("-r", "--resolution", required=True, type=float, help="Resolution")
ap.add_argument("-x", required=True, type=float, help="Origin x")
ap.add_argument("-y", required=True, type=float, help="Origin y")
ap.add_argument("-db", required=True, help="Database name")
args = vars(ap.parse_args())

print(args['x'])
print(args['y'])

img = image = cv2.imread(args['image'])

db_interface = postgis_connection.PostgisInterface()
db_interface.connect_db('gianluca', args['db'])

height, width = img.shape[:2]
print(width)
print(height)
x0 = math.floor(math.fabs(args['x']) / args['resolution'])
y0 = height - math.floor(math.fabs(args['y']) / args['resolution'])
print(x0)
print(y0)
cv2.circle(img, (x0, y0), 3, (0, 0, 255), 3, cv2.FILLED)
cv2.imshow('Image', img)
translated_points = []
points = []

cv2.setMouseCallback('Image', click_event)
cv2.waitKey(0)
cv2.destroyAllWindows()
