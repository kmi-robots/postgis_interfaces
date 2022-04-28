import matplotlib.pyplot as plt
from postgis_connection import PostgisInterface
from shapely import wkb


def walls():
    query = 'select ST_points(ST_force2d(surface)) from walls1'
    return query


def centroid():
    query = 'select st_centroid(st_orientedEnvelope(projection_2d)) ' \
            'from semantic_map ' \
            'where st_centroid(st_orientedEnvelope(projection_2d)) IS NOT NULL '
    return query


if __name__ == '__main__':
    db_interface = PostgisInterface()
    db_interface.connect_db('gianluca', 'gis_database')

    counter = 0

    records = db_interface.query_db(walls())
    for r in records:
        mp = wkb.loads(r[0], hex=True)
        x1, y1 = [mp[0].x, mp[1].x], [mp[0].y, mp[1].y]
        plt.plot(x1, y1)

    records = db_interface.query_db(centroid())
    for r in records:
        mp = wkb.loads(r[0], hex=True)
        plt.plot(mp.x, mp.y, 'r+')

    plt.axis('scaled')
    plt.show()
