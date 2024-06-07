<script setup>
import AppLayout from "@/Layouts/AppLayout.vue";
import { router, useForm } from "@inertiajs/vue3";

defineProps({
    mahasiswa: Array,
});

// Form Action
const formTambah = useForm({
    nama: null,
    nim: null,
    kelas: null,
    video: null,
});
function tambah() {
    formTambah.post("/mahasiswa");
}
function deleteMhs(id) {
    router.delete(`/mahasiswa/${id}`);
}
</script>

<template>
    <AppLayout title="Dashboard">
        <template #header>
            <h2 class="font-semibold text-xl text-gray-800 leading-tight">
                Mahasiswa
            </h2>
        </template>

        <div class="py-12">
            <div class="max-w-7xl mx-auto sm:px-6 lg:px-8">
                <div
                    class="bg-white overflow-hidden shadow-xl sm:rounded-lg p-6"
                >
                    <button
                        class="btn btn-success text-white"
                        onclick="tambahMhsModal.showModal()"
                    >
                        + Tambah Mahasiswa
                    </button>

                    <div class="overflow-x-auto mt-6">
                        <table class="table">
                            <thead>
                                <tr>
                                    <th>#</th>
                                    <th>NIM</th>
                                    <th>Nama</th>
                                    <th>Kelas</th>
                                    <th>Status Absen</th>
                                    <th>Jumlah Absen</th>
                                    <th>Action</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="(item, index) in mahasiswa">
                                    <th>{{ index + 1 }}</th>
                                    <td>{{ item.id_mahasiswa }}</td>
                                    <td>{{ item.nama }}</td>
                                    <td>{{ item.kelas }}</td>
                                    <td>{{ item.status_absen }}</td>
                                    <td>{{ item.count_absen }}</td>
                                    <td class="flex gap-2">
                                        <button
                                            class="btn btn-warning text-white"
                                        >
                                            Edit
                                        </button>
                                        <button
                                            @click="deleteMhs(item.id)"
                                            class="btn btn-error text-white"
                                        >
                                            Hapus
                                        </button>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    </AppLayout>

    <dialog id="tambahMhsModal" class="modal">
        <div class="modal-box">
            <h3 class="font-bold text-lg">Tambah Data Mahasiswa</h3>
            <hr class="mb-5" />
            <form @submit.prevent="tambah" class="flex flex-col gap-5">
                <input
                    type="text"
                    placeholder="NIM"
                    class="input input-bordered w-full"
                    v-model="formTambah.nim"
                />
                <input
                    type="text"
                    placeholder="Nama"
                    class="input input-bordered w-full"
                    v-model="formTambah.nama"
                />
                <input
                    type="text"
                    placeholder="Kelas"
                    class="input input-bordered w-full"
                    v-model="formTambah.kelas"
                />
                <input
                    type="file"
                    @input="formTambah.video = $event.target.files[0]"
                    class="file-input file-input-bordered w-full"
                />

                <input
                    type="submit"
                    value="Tambah"
                    class="btn btn-success text-white"
                />
            </form>
        </div>

        <form method="dialog" class="modal-backdrop">
            <button>close</button>
        </form>
    </dialog>
</template>
