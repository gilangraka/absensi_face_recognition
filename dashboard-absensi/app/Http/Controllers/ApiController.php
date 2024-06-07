<?php

namespace App\Http\Controllers;

use App\Models\Absensi;
use App\Models\Mahasiswa;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;

class ApiController extends Controller
{
    public function setAbsen($id_mhs)
    {
        $mhs = DB::table('mahasiswa')
            ->where('id_mahasiswa', $id_mhs);
        $absensi = DB::table('absensi')
            ->where('id_mahasiswa', $id_mhs);
        $status_absen = $mhs->pluck('status_absen')[0];
        $count_absen  = $absensi->pluck('count_absen')[0];

        if ($status_absen == 0) {
            $mhs->update([
                'status_absen'  => 1,
                'updated_at'    => now()
            ]);
            $absensi->update([
                'count_absen' => $count_absen + 1
            ]);

            return response()->json([
                'message' => 'Berhasil absen'
            ]);
        }

        return response()->json([
            'message' => 'Sudah absen!!'
        ]);
    }
}
