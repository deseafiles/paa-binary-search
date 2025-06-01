import project_root.database as database

def main():
    database.buatTableBarang()
    
    while True:
        print(' ')
        print('=' * 5, ' Program Manajemen Barang ', '='* 5)
        print('1. Tampilkan Data Barang')
        print('2. Tambahkan Barang')
        print('3. Edit Barang')
        print('4. Hapus Barang')
        print('5. Cari Barang')
        pil = int(input('Masukkan Pilihanmu = '))

        match pil:
            case 1:
                database.tampilkanDataBarang()

            case 2:
                nama = input('Masukkan Nama Barang = ')
                database.cariBarangSama(nama)

            case 3:
                nama = input('Masukkan Nama Barang = ')
                stok = input('Masukkan Stok Baru = ')
                harga = input('Masukkan Harga = ')
                
                database.editDataBarang(nama, stok, harga)

            case 4:
                nama = input("Masukkan nama barang yang ingin dihapus: ")
                database.hapusDataBarang(nama)
                
            case 5:
                nama = input('Masukkan Nama Barang yang Dicari = ')
                database.cariBarang(nama)
                
            case _:
                print("Pilihan tidak valid.")

if __name__ == "__main__":
    main()
