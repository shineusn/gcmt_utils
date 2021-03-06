import sqlite3 as lite
import sys

sqlite_gcmt_table_schema = (
   'Event TEXT, Longitude REAL, Latitude REAL, Depth REAL, Datetime DATETIME, '
  + 'Date TEXT, Time TEXT, Mw REAL, Ms REAL, Mb REAL, Lat_err REAL, '
  + 'Lon_err REAL, Depth_err REAL, Time_err REAL, Strike_1 REAL, '
  + 'Dip_1 REAL, Rake_1 REAL, Strike_2 REAL, Dip_2 REAL, Rake_2 REAL, '
  + 'Mrr REAL, Mtt REAL, Mpp REAL, Mrt REAL, Mrp REAL, Mtp REAL, '
  + 'Mrr_err REAL, Mtt_err REAL, Mpp_err REAL, Mrt_err REAL, Mrp_err REAL, '
  + 'Mtp_err REAL, '
  + 'Scalar_moment REAL' 'Moment_exp INT, '
  + 'T REAL, T_azimuth REAL, T_plunge REAL, '
  + 'N REAL, N_azimuth REAL, N_plunge REAL, '
  + 'P REAL, P_azimuth REAL, P_plunge REAL, '
  + 'Reference_longitude REAL, Reference_latitude REAL, Reference_depth REAL, '
  + 'Reference_date TEXT, Reference_time TEXT, Reference_datetime DATETIME, '
  + 'Body_wave_components INT, Body_wave_stations INT, Body_wave_period REAL, '
  + 'Surface_wave_components INT, Surface_wave_stations INT, '
  + 'Surface_wave_period REAL, '
  + 'Mantle_wave_components INT, Mantle_wave_stations INT, '
  + 'Mantle_wave_period REAL, '
  + 'CMT_Version TEXT, CMT_Type TEXT, Depth_inversion_type TEXT, '
  + 'Geog_location TEXT, Hypocenter_reference_catalog TEXT, '
  + 'CMT_Timestamp TEXT, '
  + 'Moment_rate_function TEXT, Moment_rate_half_duration REAL, '
  + 'Focal_mech BLOB'
)


table_cols = tuple(kw.split()[0] for kw in sqlite_gcmt_table_schema.split(','))


column_key_correlation_d = {
    'Ms' : 'Ms',
    'Mw' : 'Mw',
    'Body_wave_components' : 'body_wave_components',
    'Body_wave_period' : 'body_wave_shortest_period',
    'Body_wave_stations' : 'body_wave_stations',
    'Date' : 'centroid_date',
    'Datimetime' : 'centroid_datetime',
    'Depth' : 'centroid_depth',
    'Depth_err' : 'centroid_depth_err',
    'Lat_err' : 'centroid_lat_err',
    'Latitude' : 'centroid_latitude',
    'Lon_err' :  'centroid_lon_err',
    'Longitude' : 'centroid_longitude',
    'Time' : 'centroid_time',
    'Time_err' : 'centroid_time_err',
    'CMT_Version' : 'cmt_code_version',
    'Event' : 'cmt_event_name',
    'CMT_Timestamp' : 'cmt_timestamp',
    'CMT_Type' : 'cmt_type',
    'Depth_inversion_type' : 'depth_inv_type',
    'Dip_1' : 'dip_1',
    'Dip_2' : 'dip_2',
    'Geog_location' : 'geog_location',
    'Hypocenter_reference_catalog' : 'hypocenter_reference_catalog',
    'Mantle_wave_components' : 'mantle_wave_components',
    'Mantle_wave_period' : 'mantle_wave_shortest_period',
    'Mantle_wave_stations' : 'mantle_wave_stations',
    'Mb' : 'mb',
    'Moment_rate_function' : 'moment_rate_function',
    'Moment_rate_half_duration' : 'moment_rate_half_duration',
    'Mpp' : 'mpp',
    'Mpp_err' : 'mpp_err',
    'Mrp' : 'mrp',
    'Mrp_err' : 'mrp_err',
    'Mrr' : 'mrr',
    'Mrr_err' : 'mrr_err',
    'Mrt' : 'mrt',
    'Mrt_err' : 'mrt_err',
    'Moment_exp' : 'mt_exp',
    'Mtp' : 'mtp',
    'Mtp_err' : 'mtp_err',
    'Mtt' : 'mtt',
    'Mtt_err' : 'mtt_err',
    'N' : 'n',
    'N_azimuth' : 'n_azimuth',
    'N_plunge' : 'n_plunge',
    'P' : 'p',
    'P_azimuth' : 'p_azimuth',
    'P_plunge' : 'p_plunge',
    'Rake_1' : 'rake_1',
    'Rake_2' : 'rake_2',
    'Reference_date' : 'reference_date',
    'Reference_datetime' : 'reference_datetime',
    'Reference_depth' : 'reference_depth',
    'Reference_latitude' : 'reference_latitude',
    'Reference_longitude' : 'reference_longitude',
    'Reference_time' : 'reference_time',
    'Scalar_moment' : 'scalar_moment',
    'Strike_1' : 'strike_1',
    'Strike_2' : 'strike_2',
    'Surface_wave_components' : 'surface_wave_components',
    'Surface_wave_period' : 'surface_wave_shortest_period',
    'Surface_wave_stations' : 'surface_wave_stations',
    'T' : 't',
    'T_azimuth' : 't_azimuth',
    'T_plunge' : 't_plunge',
    'Focal_mech' : 'focal_mech'
        }


def get_eq_dict_val(eq_dict, col):
    try:
        val = eq_dict[ column_key_correlation_d[col]]
    except KeyError:
        val = 'NULL'
    return val


def make_row_tuple(eq_dict):
    return tuple(get_eq_dict_val(eq_dict, col) for col in table_cols)


def make_gcmt_table(table_name, schema, db=None):
    con = lite.connect(db)

    with con:
        cur = con.cursor()
        cur.execute(
            "CREATE TABLE {}({})".format(table_name, schema))
    return


def connect_to_db(db):
    return lite.connect(db)


def insert_row_tuple(cur, table, row_tuple):

    insert_string = make_insert_row_string(table, row_tuple)
    cur.execute(insert_string)
    return


def make_insert_row_string(table, row_tuple):
    return "INSERT INTO {} VALUES{}".format(table, row_tuple)


def insert_row_tuples_iter(con, table, row_tup_list):
    cur = con.cursor()

    (insert_row_tuple(cur, table, rt) for rt in row_tup_list)

    return


def make_big_table_tuple(eq_dict_list):
    return tuple(make_row_tuple(eq_d) for eq_d in eq_dict_list)


def make_multi_row_string(table_name, table_cols=None, n_cols=None):

    if n_cols is None:
        n_cols = len(table_cols)

    q_str = ','.join(' ?' for c in range(n_cols))[1:]

    return 'INSERT INTO {} VALUES({})'.format(table_name, q_str)


def insert_many_rows(con, table_name, n_cols, multi_row_tuple, 
                     print_lastid=False):

    insert_string = make_multi_row_string(table_name, n_cols=n_cols)

    cur = con.cursor()

    cur.executemany(insert_string, multi_row_tuple)

    if print_lastid:
        print('last id is ', cur.lastrowid)

    return
