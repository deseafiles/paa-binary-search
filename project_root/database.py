import mysql.connector
import project_root.database as database
import project_root.search as search
from project_root.barang import Barang

def getConnection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="", 
        database="dataBarang"
    )
    
def buatTableBarang():
    con = getConnection()
    cursor = con.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS barang (
            id_barang INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
            nama VARCHAR(255) NOT NULL,
            stok INTEGER NOT NULL,
            harga INTEGER NOT NULL
        )
    """)
    con.commit()      
    cursor.close()
    con.close() 
    
def tampilkanDataBarang():
    con = getConnection()
    cursor = con.cursor()
    cursor.execute('SELECT nama,stok,harga FROM barang')
    rows = cursor.fetchall()
    print("Isi tabel barang:")
    for row in rows:
        print(row)  
          
    cursor.close()
    con.close() 

def insertDataBarang(nama, stok, harga):
    con = getConnection()
    cursor = con.cursor()
    cursor.execute('INSERT INTO barang (nama, stok, harga) VALUES (%s, %s, %s)', (nama, stok, harga))
    con.commit()      
    cursor.close()
    con.close()   

def tambahDataBarang(stok,nama):
    con = getConnection()
    cursor = con.cursor()
    cursor.execute('UPDATE barang SET stok = %s WHERE nama = %s ' , (stok, nama))
    con.commit()      
    cursor.close()
    con.close()   
    
def editDataBarang(namaBarang, stok, harga):
    con = getConnection()
    cursor = con.cursor()
    cursor.execute("SELECT nama FROM barang")
    hasil = [row[0] for row in cursor.fetchall()]
    hasil.sort()

    idx = search.BinarySearch(hasil, namaBarang)
    
    if idx != -1:
        print(f"Barang {hasil[idx]} diedit")
        cursor.execute('UPDATE barang SET stok = %s, harga = %s WHERE nama = %s', (stok, harga, hasil[idx]))   
    else:
        print(f"Barang {hasil[idx]} tidak ditemukan.")
    con.commit()      
    cursor.close()
    con.close()   
    
def hapusDataBarang(namaBarang):
    con = getConnection()
    cursor = con.cursor()
    cursor.execute("SELECT nama FROM barang")
    hasil = [row[0] for row in cursor.fetchall()]
    hasil.sort()

    idx = search.BinarySearch(hasil, namaBarang)
    
    if idx != -1:
        print(f"Barang {hasil[idx]} dihapus")
        cursor.execute('DELETE FROM barang WHERE nama = %s', (hasil[idx],))
    else:
        print(f"Barang {hasil[idx]} tidak ditemukan.")
    con.commit() 
    cursor.close()
    con.close()

def cariBarangSama(namaBarang):
    con = getConnection()
    cursor = con.cursor()
    cursor.execute("SELECT nama FROM barang")
    hasil = [row[0] for row in cursor.fetchall()]
    hasil.sort()
    idx = search.BinarySearch(hasil, namaBarang)

    if idx != -1:
        stok = int(input('Masukkan Jumlah Stok = '))
        try:
            cursor.execute('SELECT nama, stok, harga FROM barang WHERE nama = %s', (hasil[idx],))
            row = cursor.fetchone()
            stokBaru = row[1] + stok
            database.tambahDataBarang(stokBaru, namaBarang)
            print("Barang berhasil ditambahkan!")

        except ValueError as e:
            print(f"Error saat menambahkan barang: {e}")
    else:
        stok = int(input('Masukkan Jumlah Stok = '))
        harga = int(input('Masukkan Harga Satuan = '))
        
        newBarang = Barang(namaBarang, stok, harga)

        try:
            newBarang.pengecekan_stok()
            newBarang.pengecekan_harga()
            database.insertDataBarang(newBarang.nama, newBarang.stok, newBarang.harga)
            print("Barang berhasil ditambahkan!")

        except ValueError as e:
            print(f"Error saat menambahkan barang: {e}")
    con.commit()
    cursor.close()
    con.close()

def cariBarang(namaBarang):
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute("SELECT nama FROM barang")
    hasil = [row[0] for row in cursor.fetchall()]
    hasil.sort()

    idx = search.BinarySearch(hasil, namaBarang)
    
    if idx != -1:
        print(f"Barang ditemukan: {hasil[idx]}")
        cursor.execute('SELECT nama, stok, harga FROM barang WHERE nama = %s', (hasil[idx],))
        row = cursor.fetchone() #Pelajari lebih dalam hal ini
        print("Detail Barang:")
        print(f"Nama  : {row[0]}")
        print(f"Stok  : {row[1]}")
        print(f"Harga : {row[2]}")
    else:
        print(f"Barang {hasil[idx]} tidak ditemukan.")
    
    cursor.close()
    conn.close()
