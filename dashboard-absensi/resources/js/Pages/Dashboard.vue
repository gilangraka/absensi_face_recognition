<script setup>
import AppLayout from "@/Layouts/AppLayout.vue";
import Welcome from "@/Components/Welcome.vue";

defineProps({
    sudah_absen: Array,
    count: Number,
});
</script>

<template>
    <AppLayout title="Dashboard">
        <template #header>
            <h2 class="font-semibold text-xl text-gray-800 leading-tight">
                Dashboard
            </h2>
        </template>

        <div class="py-12">
            <div class="max-w-7xl mx-auto sm:px-6 lg:px-8">
                <div
                    class="bg-white overflow-hidden shadow-xl sm:rounded-lg p-6"
                >
                    <h3 class="font-semibold text-m text-gray-800">
                        Riwayat Absensi
                    </h3>

                    <div class="overflow-x-auto mt-6">
                        <table class="table">
                            <thead>
                                <tr>
                                    <th>#</th>
                                    <th>NIM</th>
                                    <th>Nama</th>
                                    <th>Kelas</th>
                                    <th>Waktu Absen</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-if="count == 0">
                                    <td colspan="5" class="text-center">
                                        Data Kosong
                                    </td>
                                </tr>
                                <tr
                                    v-else
                                    v-for="(item, index) in sudah_absen"
                                    :key="item.id"
                                >
                                    <td>{{ index + 1 }}</td>
                                    <td>{{ item.id_mahasiswa }}</td>
                                    <td>{{ item.nama }}</td>
                                    <td>{{ item.kelas }}</td>
                                    <td>{{ item.updated_at }}</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    </AppLayout>
</template>
