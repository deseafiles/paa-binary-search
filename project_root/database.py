import sqlite3
from .barang import Barang
import project_root.search as search

def getConnection():
    return sqlite3.connect("dataBarang.db")
    
def buatTableBarang():
    con = getConnection()
    cursor = con.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS barang (
        id_barang INTEGER PRIMARY KEY AUTOINCREMENT,
        nama TEXT NOT NULL,
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
    cursor.execute('SELECT id_barang, nama,stok,harga FROM barang')
    rows = cursor.fetchall()
    print("Isi tabel barang:")
    for row in rows:
        print(row)  
          
    cursor.close()
    con.close() 

def insertDataBarang(nama, stok, harga):
    con = getConnection()
    cursor = con.cursor()
    cursor.execute('INSERT INTO barang (nama, stok, harga) VALUES (?, ?, ?)', (nama, stok, harga))
    con.commit()      
    cursor.close()
    con.close()   

def tambahDataBarang(stok,nama):
    con = getConnection()
    cursor = con.cursor()
    cursor.execute('UPDATE barang SET stok = ? WHERE nama = ? ' , (stok, nama))
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
        cursor.execute('UPDATE barang SET stok = ?, harga = ? WHERE nama = ?', (stok, harga, hasil[idx]))   
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
        cursor.execute('DELETE FROM barang WHERE nama = ?', (hasil[idx],))
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
            cursor.execute('SELECT nama, stok, harga FROM barang WHERE nama = ?', (hasil[idx],))
            row = cursor.fetchone()
            stokBaru = row[1] + stok
            tambahDataBarang(stokBaru, namaBarang)
            print(f"Barang {namaBarang} berhasil ditambahkan!")

        except ValueError as e:
            print(f"Error saat menambahkan barang {hasil[idx]}: {e}")
    else:
        stok = int(input('Masukkan Jumlah Stok = '))
        harga = int(input('Masukkan Harga Satuan = '))
        
        newBarang = Barang(namaBarang, stok, harga)

        try:
            newBarang.pengecekan_stok()
            newBarang.pengecekan_harga()
            insertDataBarang(newBarang.nama, newBarang.stok, newBarang.harga)
            print(f"Barang {hasil[idx]} berhasil ditambahkan!")

        except ValueError as e:
            print(f"Error saat menambahkan barang {hasil[idx]}: {e}")
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
        cursor.execute('SELECT nama, stok, harga FROM barang WHERE nama = ?', (hasil[idx],))
        row = cursor.fetchone()
        print("Detail Barang:")
        print(f"Nama  : {row[0]}")
        print(f"Stok  : {row[1]}")
        print(f"Harga : {row[2]}")
    else:
        print(f"Barang {hasil[idx]} tidak ditemukan.")
    
    cursor.close()
    conn.close()