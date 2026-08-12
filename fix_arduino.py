import codecs

with codecs.open('.firebase/kode iot/sketch_jun10a/sketch_jun10a.ino', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
in_prosesAbsensi = False
brace_count = 0

for i, line in enumerate(lines):
    if line.startswith('void prosesAbsensi('):
        in_prosesAbsensi = True
        
        # Write the new prosesAbsensi function
        new_lines.append('''// ====== Proses Absensi (Kartu Terdaftar) ======
void prosesAbsensi(String uid, String namaSiswa, String nisnSiswa, String kelasSiswa)
{
    timeClient.update();

    int day = timeClient.getDay(); // 0=Minggu, 1=Senin, ..., 5=Jumat, 6=Sabtu
    String namaHariKey = (day >= 0 && day <= 6) ? hariKeys[day] : "senin";
    String namaHariDisplay = (day >= 0 && day <= 6) ? hariNames[day] : "HARI";

    // Ambil jadwal hari ini dari Firebase
    JadwalHari jadwal = getJadwalHari(day);

    // Cek apakah hari ini adalah hari operasional (aktif)
    if (!jadwal.aktif)
    {
        lcd.clear();
        printCenter("HARI LIBUR", 0);
        printCenter(namaHariDisplay + " LIBUR", 1);

        buzzerAlreadyPresent();

        delay(2000);
        tampilStandby();
        return;
    }

    String jam = timeClient.getFormattedTime(); // "HH:MM:SS"
    int menitSekarang = timeToMinutes(jam.substring(0, 5));

    // Konversi jadwal ke menit
    int masukBuka = timeToMinutes(jadwal.masuk_buka);
    int terlambat = timeToMinutes(jadwal.terlambat);
    int masukTutup = timeToMinutes(jadwal.masuk_tutup);
    int pulangBuka = timeToMinutes(jadwal.pulang_buka);
    int pulangTutup = timeToMinutes(jadwal.pulang_tutup);

    String tanggal = getTanggalSekarang();
    String path = "/absensi/" + tanggal + "/" + uid;
    String namaLCD = namaSiswa;
    namaLCD.replace("_", " ");

    // Cek status absensi saat ini di database
    bool sudahMasuk = false;
    bool sudahPulang = false;
    
    if (Firebase.ready() && Firebase.getJSON(fbdo, path) && fbdo.dataType() != "null")
    {
        FirebaseJson &existingData = fbdo.jsonObject();
        FirebaseJsonData checkResult;
        
        existingData.get(checkResult, "jam_masuk");
        if (checkResult.success && checkResult.stringValue.length() > 0) sudahMasuk = true;
        
        existingData.get(checkResult, "jam_pulang");
        if (checkResult.success && checkResult.stringValue.length() > 0) sudahPulang = true;
    }

    // ====== TENTUKAN SESI: MASUK atau PULANG ======
    if (menitSekarang >= masukBuka && menitSekarang < masukTutup)
    {
        // === SESI ABSENSI MASUK ===
        if (sudahMasuk)
        {
            lcd.clear();
            printCenter(namaLCD, 0);
            printCenter("SUDAH ABSEN", 1);
            buzzerAlreadyPresent();
            delay(2000);
            tampilStandby();
            return;
        }

        // Tentukan status: HADIR atau TERLAMBAT
        String status = "HADIR";
        if (menitSekarang >= terlambat)
        {
            status = "TERLAMBAT";
        }

        Serial.print("Jam: "); Serial.println(jam);
        Serial.print("Status Masuk: "); Serial.println(status);

        lcd.clear();
        printCenter(namaLCD, 0);
        String jamLCD = jam.substring(0, 5);
        printCenter(status + " " + jamLCD, 1);
        buzzerSuccess();

        if (Firebase.ready())
        {
            FirebaseJson json;
            json.set("nama", namaSiswa);
            json.set("nisn", nisnSiswa);
            json.set("kelas", kelasSiswa);
            json.set("uid", uid);
            json.set("status", status);
            json.set("tanggal", tanggal);
            json.set("jam", jam);         // Backward compatible
            json.set("jam_masuk", jam);

            Firebase.updateNode(fbdo, path, json); // Gunakan updateNode agar tidak menimpa jika ada data lain

            // Update rekap
            int total = 0;
            if (Firebase.getInt(fbdo, "/rekap/" + namaSiswa + "/total")) total = fbdo.intData();
            total++;
            Firebase.setInt(fbdo, "/rekap/" + namaSiswa + "/total", total);

            if (status == "TERLAMBAT")
            {
                int terlambatCount = 0;
                if (Firebase.getInt(fbdo, "/rekap/" + namaSiswa + "/terlambat")) terlambatCount = fbdo.intData();
                terlambatCount++;
                Firebase.setInt(fbdo, "/rekap/" + namaSiswa + "/terlambat", terlambatCount);
            }
        }
        delay(1500);
        tampilStandby();
    }
    else if (menitSekarang >= pulangBuka && menitSekarang < pulangTutup)
    {
        // === SESI ABSENSI PULANG ===
        if (!sudahMasuk)
        {
            lcd.clear();
            printCenter("BELUM ABSEN", 0);
            printCenter("MASUK HARI INI", 1);
            buzzerSystemError();
            delay(2000);
            tampilStandby();
            return;
        }
        
        if (sudahPulang)
        {
            lcd.clear();
            printCenter(namaLCD, 0);
            printCenter("SUDAH PULANG", 1);
            buzzerAlreadyPresent();
            delay(2000);
            tampilStandby();
            return;
        }

        Serial.print("Jam Pulang: "); Serial.println(jam);

        lcd.clear();
        printCenter(namaLCD, 0);
        String jamLCD = jam.substring(0, 5);
        printCenter("PULANG " + jamLCD, 1);
        buzzerSuccess();

        if (Firebase.ready())
        {
            FirebaseJson json;
            json.set("jam_pulang", jam);
            Firebase.updateNode(fbdo, path, json);
        }
        delay(1500);
        tampilStandby();
    }
    else if (menitSekarang < masukBuka)
    {
        // Belum waktunya absensi masuk
        lcd.clear();
        printCenter("BELUM WAKTUNYA", 0);
        printCenter("BUKA " + jadwal.masuk_buka, 1);
        buzzerAlreadyPresent();
        delay(2000);
        tampilStandby();
    }
    else if (menitSekarang >= masukTutup && menitSekarang < pulangBuka)
    {
        // Waktu di antara masuk tutup dan pulang buka
        lcd.clear();
        printCenter("BELUM WAKTUNYA", 0);
        printCenter("PULANG", 1);
        buzzerAlreadyPresent();
        delay(2000);
        tampilStandby();
    }
    else if (menitSekarang >= pulangTutup)
    {
        // Setelah jam pulang tutup
        lcd.clear();
        printCenter("ABSENSI DITUTUP", 0);
        printCenter("SAMPAI BESOK", 1);
        buzzerAlreadyPresent();
        delay(2000);
        tampilStandby();
    }
}
''')
    
    if in_prosesAbsensi:
        if '{' in line:
            brace_count += line.count('{')
        if '}' in line:
            brace_count -= line.count('}')
        
        if brace_count == 0 and '{' not in lines[i] and not line.startswith('//'):
            # The function ended.
            # But wait, what if brace count is 0 right at the start? It's fine.
            if i > 210: # ensure we passed the start
                in_prosesAbsensi = False
    else:
        if not line.startswith('// ====== Proses Absensi (Kartu Terdaftar) ======'):
            new_lines.append(line)

with codecs.open('.firebase/kode iot/sketch_jun10a/sketch_jun10a.ino', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
print("Updated Arduino sketch!")
