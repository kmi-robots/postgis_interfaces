import argparse
import cv2
import math
import psycopg2
import keyring


def connect_db(user, dbname):
    try:
        conn = psycopg2.connect(dbname=dbname, user=user, password=keyring.get_password(dbname, user))
        cur = conn.cursor()
        print(conn.get_dsn_parameters(), "\n")
        cur.execute("SELECT version();")
        record = cur.fetchone()
        print('You are connected to' + str(record))

    except (Exception, psycopg2.Error) as error:
        print('Error while connecting to PostgreSQL' + str(error))
        conn = None
        cur = None

    return conn, cur


def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.circle(img, (x, y), 3, (0, 0, 255), 3, cv2.FILLED)
        points.append((x, y))
        if len(points) >= 2:
            cv2.line(img, points[-1], points[-2], (255, 0, 0), 5, cv2.LINE_AA)
            xm, ym = points[-1]
            xm = args['x'] + xm*args['resolution']
            ym = args['y'] + (height - ym) * args['resolution']
            xm_, ym_ = points[-2]
            xm_ = args['x'] + xm_ * args['resolution']
            ym_ = args['y'] + (height - ym_) * args['resolution']
            print("coordinates: p1 (%f, %f), p2 (%f, %f)" % (xm, ym, xm_, ym_))
            insert_wall(xm, ym, xm_, ym_)
            points.clear()
        cv2.imshow('Image', img)


def create_table(con, cur):
    cur.execute("CREATE TABLE IF NOT EXISTS walls("
                "id serial PRIMARY KEY,"
                "surface geometry NOT NULL)")
    con.commit()


def insert_wall(xm, ym, xm_, ym_, wdepth=0.1, wheight=4):
    query_mask = "INSERT INTO walls(surface) " \
                 "VALUES(ST_Extrude(ST_GeomFromText('LINESTRING({} {}, {} {})'),0,0,{}))" 
    query = query_mask.format(xm, ym, xm_, ym_, wheight)
    cursor.execute(query)
    connection.commit()


ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the image")
ap.add_argument("-r", "--resolution", required=True, type=float, help="Resolution")
ap.add_argument("-x", required=True, type=float, help="Origin x")
ap.add_argument("-y", required=True, type=float, help="Origin y")
args = vars(ap.parse_args())

print(args['x'])
print(args['y'])

img = image = cv2.imread(args["image"])

connection, cursor = connect_db('agnese', 'gis_database')
create_table(connection, cursor)

height, width = img.shape[:2]
print(width)
print(height)
x0 = math.floor(math.fabs(args['x']) / args['resolution'])
y0 = height - math.floor(math.fabs(args['y']) / args['resolution'])
print(x0)
print(y0)
cv2.circle(img, (x0, y0), 3, (0, 0, 255), 3, cv2.FILLED)
cv2.imshow('Image', img)
points = []

cv2.setMouseCallback('Image', click_event)
cv2.waitKey(0)
cv2.destroyAllWindows()
