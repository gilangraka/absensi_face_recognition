<?php

namespace App\Http\Controllers;

use App\Models\Absensi;
use App\Models\Mahasiswa;
use GuzzleHttp\Client;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Storage;
use Inertia\Inertia;

class MahasiswaController extends Controller
{
    /**
     * Display a listing of the resource.
     */
    public function dashboard()
    {
        $sudah_absen = Mahasiswa::where('status_absen', 1)->get();
        return Inertia::render('Dashboard', [
            'sudah_absen' => $sudah_absen,
            'count' => $sudah_absen->count()
        ]);
    }

    public function index()
    {
        $mahasiswa = DB::table('mahasiswa')->join('absensi', 'absensi.id_mahasiswa', '=', 'mahasiswa.id_mahasiswa')
            ->get(['mahasiswa.id', 'mahasiswa.id_mahasiswa', 'nama', 'kelas', 'status_absen', 'count_absen']);

        return Inertia::render('Mahasiswa', [
            'mahasiswa' => $mahasiswa
        ]);
    }

    /**
     * Show the form for creating a new resource.
     */
    public function create()
    {
        //
    }

    /**
     * Store a newly created resource in storage.
     */
    public function store(Request $request)
    {
        $video = $request->file('video');

        $mahasiswa = new Mahasiswa;
        $mahasiswa->id_mahasiswa = $request->nim;
        $mahasiswa->nama = $request->nama;
        $mahasiswa->kelas = $request->kelas;

        $fileName = $mahasiswa->id_mahasiswa . '.' . $video->getClientOriginalExtension();
        $video->storeAs('public/uploads', $fileName);

        $mahasiswa->video_mahasiswa = $fileName;
        $mahasiswa->save();

        $absensi = new Absensi;
        $absensi->id_mahasiswa = $mahasiswa->id_mahasiswa;
        $absensi->save();

        $client = new Client();
        $client->get("http://127.0.0.1:5000/create_user/$fileName");

        return back();
    }

    /**
     * Display the specified resource.
     */
    public function show(string $id)
    {
        //
    }

    /**
     * Show the form for editing the specified resource.
     */
    public function edit(string $id)
    {
        //
    }

    /**
     * Update the specified resource in storage.
     */
    public function update(Request $request, string $id)
    {
        //
    }

    /**
     * Remove the specified resource from storage.
     */
    public function destroy($id)
    {
        $id_mhs = DB::table('mahasiswa')
            ->where('id', $id)->pluck('id_mahasiswa')[0];
        $nama_file = DB::table('mahasiswa')
            ->where('id', $id)->pluck('video_mahasiswa')[0];

        DB::table('absensi')
            ->where('id_mahasiswa', $id_mhs)->delete();
        Storage::delete("public/uploads/$nama_file");

        Mahasiswa::find($id)->delete();
        return back();
    }
}
