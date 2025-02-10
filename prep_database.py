import sqlite3
import traceback

tarieven = {
            'categorieen': ['0-2kg', '2-5kg', '5-10kg', '10-15kg', '15-20kg'],
            'België': [5.6, 5.6, 12.6, 12.6, 21.6],
            'Nederland': [9.6, 12.6, 12.6 ,21.6, 21.6],
            'Luxemburg': [13.2, 15.5, 15.5, 21.6, 21.6],
            'Frankrijk': [10.0, 15.5, 15.5, 21.6, 21.6],
            'Duitsland': [15.5, 15.5, 15.5, 21.6, 21.6]
        }

landen = list(tarieven.keys())[1:]
categorieen = tarieven['categorieen']

dbVerbinding = sqlite3.connect('verzendkosten.sqlite3')
dbCursor = dbVerbinding.cursor()

try:
    # tabel land
    dbSql = '''
        DROP TABLE IF EXISTS land
    '''
    dbCursor.execute(dbSql)

    dbSql = '''
        CREATE TABLE land (
            landID TEXT NOT NULL PRIMARY KEY
        )
    '''
    dbCursor.execute(dbSql)

    dbSql = '''
        INSERT INTO land(landID) VALUES (?)
    '''
    for land in landen:
        dbCursor.execute(dbSql, (land, ))

    # tabel categorie
    dbSql = '''
        DROP TABLE IF EXISTS categorie
    '''
    dbCursor.execute(dbSql)

    dbSql = '''
        CREATE TABLE categorie (
            categorieID TEXT NOT NULL PRIMARY KEY
        )
    '''
    dbCursor.execute(dbSql)

    dbSql = '''
        INSERT INTO categorie(categorieID)
        VALUES(?)
    ''' 
    for categorie in categorieen:
        dbCursor.execute(dbSql, (categorie,))

    #tarieven
    dbSql = '''
        DROP TABLE IF EXISTS tarief
    '''
    dbCursor.execute(dbSql)

    dbSql = '''
        CREATE TABLE tarief(
            landID TEXT NOT NULL,
            categorieID TEXT NOT NULL,
            prijs REAL NOT NULL,
            PRIMARY KEY(landID, categorieID),
            FOREIGN KEY (landID) REFERENCES land(landID),
            FOREIGN KEY (categorieID) REFERENCES categorie(categorieID)
        )
    '''
    dbCursor.execute(dbSql)

    dbSql = '''
        INSERT INTO tarief(landID, categorieID, prijs)
        VALUES (?, ?, ?)
    '''

    for land in landen:
        tarief = tarieven[land]
        for ndx, categorie in enumerate(categorieen):
            dbCursor.execute(dbSql, (land, categorie, tarief[ndx]))

except Exception as ex:
    print(traceback.format_exception(ex))

dbVerbinding.commit()

if dbCursor:
    dbCursor.close()

if dbVerbinding:
    dbVerbinding.close()