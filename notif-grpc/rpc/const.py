from datetime import datetime

EMAIL_STATIC = {
    "MOPINJAM": {
        "FROM": "noreply@mopinjam.id",
        "LOGO": "Mopinjam",
        "LOGO_URL": "http://147.139.134.250:81/static/logos/mopinjam_298x61.png",
        "WELCOME": "Pelanggan Yth,",
        "WEBSITE": "https://dev.modana.id",
        "INFO": "Jika Anda memiliki pertanyaan dalam menggunakan layanan kami, silahkan hubungi kami di cs@mopinjam.id atau via telp di (021)-22586111 atau via WhatsApp di 08119790000.",
        "THANKS": "Terima kasih atas perhatian dan kerjasamanya.",
        "CHEERS": "Hormat Kami,",
        "TEAM_NAME": "Mopinjam",
        "STREET1": "Puri Indah Financial Tower",
        "STREET2": "Jakarta Barat, Kembangan Selatan, Daerah Khusus Ibukota Jakarta 11610.",
        "COPYRIGHT": "© " + "2019"
        " Hak Cipta Terpelihara PT Amanah Karyananta Nusantara",
    }
}

EMAIL_TEMPLATES = {
    "MOPINJAM": {
        "SUBJECT": {
            "INVESTOR_APPROVE": "Persetujuan – Registrasi Pemberi Pinjaman",
            "INVESTOR_REJECT": "Penolakan – Registrasi Pemberi Pinjaman",
            "INVESTOR_DISBURSE": "Pemberitahuan – Pencairan Pinjaman",
            "INVESTOR_TOPUP": "Pemberitahuan – Pengisian Saldo Rekening Dana Lender",
            "INVESTOR_REPAYMENT": "Pemberitahuan – Penerimaan Pembayaran dari Peminjam",
            "INVESTOR_WITHDRAW": "Pemberitahuan – Penarikan Dana Rekening Lender",
            "LOAN_REQUEST_SEND": "Pengajuan Pinjaman",
            "LOAN_REQUEST_APPROVE": "Persetujuan – Pengajuan Pinjaman",
            "LOAN_REQUEST_REJECT": "Penolakan Pinjaman",
            "LOAN_REQUEST_DISBURSE": "Pencairan Dana Pinjaman ",
            "LOAN_REQUEST_REPAYMENT": "Pemberitahuan Pelunasan Pinjaman Berhasil",
            "LOAN_REQUEST_REPAYMENT_MOBILE": "Pemberitahuan Pelunasan Pinjaman Berhasil",
            "REMINDER_BEFORE_DUEDATE": "Pemberitahuan Jatuh Tempo Pinjaman",
            "REMINDER_AFTER_DUEDATE": "Pemberitahuan Keterlambatan Pembayaran Pinjaman",
        },
        "TEMPLATE": {
            "INVESTOR_APPROVE": "mopinjam",
            "INVESTOR_REJECT": "mopinjam",
            "INVESTOR_DISBURSE": "mopinjam",
            "INVESTOR_TOPUP": "mopinjam",
            "INVESTOR_REPAYMENT": "mopinjam",
            "INVESTOR_WITHDRAW": "mopinjam",
            "LOAN_REQUEST_SEND": "mopinjam",
            "LOAN_REQUEST_APPROVE": "mopinjam",
            "LOAN_REQUEST_REJECT": "mopinjam",
            "LOAN_REQUEST_DISBURSE": "mopinjam",
            "LOAN_REQUEST_REPAYMENT": "mopinjam",
            "LOAN_REQUEST_REPAYMENT_MOBILE": "mopinjam",
            "REMINDER_BEFORE_DUEDATE": "mopinjam",
            "REMINDER_AFTER_DUEDATE": "mopinjam",
        },
        "CONTENT": {
            "INVESTOR_APPROVE": "Selamat! Registrasi anda telah berhasil disetujui. Akses: https://investor.mopinjam.id untuk dapat mengakses akun anda dan mulai pendanaan.",
            "INVESTOR_REJECT": "Mohon maaf, untuk saat ini pengajuan registrasi anda belum dapat disetujui karena belum memenuhi Syarat dan Ketentuan yang berlaku.",
            "INVESTOR_DISBURSE": "Investasi yang anda berikan telah berhasil dicairkan ke rekening peminjam anda.",
            "INVESTOR_TOPUP": "Pengisian saldo Rekening Dana Lender anda telah berhasil. Anda sudah dapat mulai berinvestasi melalui akun anda.",
            "INVESTOR_REPAYMENT": "Anda telah menerima pembayaran dari peminjam: Waktu Pembayaran: $repayment_date Jumlah Pembayaran: Rp. $repayment_amount Jenis Pinjaman:  $product",
            "INVESTOR_WITHDRAW": "Penarikan dana dari Rekening Dana Lender anda telah berhasil dilakukan: Waktu Penarikan: $withdraw_date Jumlah Penarikan: Rp. $withdraw_amount ",
            "LOAN_REQUEST_SEND": "Pengajuan pinjaman $loan_request_code Anda sudah diterima oleh Tim Analis Kami dan akan diproses lebih lanjut.",
            "LOAN_REQUEST_APPROVE": "Pengajuan Pinjaman $loan_request_code Anda telah disetujui, dan akan segera dicairkan dalam 1x24 jam.",
            "LOAN_REQUEST_REJECT": "Mohon maaf, untuk saat ini pengajuan pinjaman Anda $loanRequestCode tidak disetujui karena belum memenuhi Syarat dan Ketentuan yang berlaku.",
            "LOAN_REQUEST_DISBURSE": "Selamat! No Pinjaman $loan_request_code yang Anda ajukan telah berhasil dicairkan ke rekening MODANAKU Anda. Segera melakukan pengecekan saldo MODANAKU Anda. Detil informasi pinjaman dapat dilihat pada menu PINJAMAN Anda.",
            "LOAN_REQUEST_REPAYMENT": "Terima kasih, Anda telah berhasil melakukan pembayaran pinjaman:<br><br>"
            + "Waktu Pembayaran: $repayment_date <br>"
            + "Nomor Pinjaman: $loan_request_code <br>"
            + "Jumlah Pembayaran: Rp. $repayment_amount <br>"
            + "Produk Pinjaman:  $product",
            "REMINDER_BEFORE_DUEDATE": "Pinjaman Anda $loan_request_code akan segera jatuh tempo. Pastikan saldo MODANAKU cukup untuk membayar jumlah pinjaman untuk menghindari denda keterlambatan.",
            "REMINDER_AFTER_DUEDATE": "Pinjaman Anda $loan_request_code telah jatuh tempo. Segera lakukan pembayaran manual via MODANAKU Anda, pembayaran setelah tanggal jatuh tempo akan dikenakan denda keterlambatan sesuai ketentuan yang berlaku",
            "REMINDER_DUEDATE": "Pinjaman Anda $loan_request_code jatuh tempo hari ini. Pastikan saldo MODANAKU cukup untuk membayar jumlah pinjaman untuk menghindari denda keterlambatan.",
        },
    }
}

MOBILE_TEMPLATES = {
    "MOPINJAM": {
        "SUBJECT": {
            "INVESTOR_APPROVE": "Persetujuan – Registrasi Pemberi Pinjaman",
            "INVESTOR_REJECT": "Penolakan – Registrasi Pemberi Pinjaman",
            "INVESTOR_DISBURSE": "Pemberitahuan – Pencairan Pinjaman",
            "INVESTOR_TOPUP": "Pemberitahuan – Pengisian Saldo Rekening Dana Lender",
            "INVESTOR_REPAYMENT": "Pemberitahuan – Penerimaan Pembayaran dari Peminjam",
            "INVESTOR_WITHDRAW": "Pemberitahuan – Penarikan Dana Rekening Lender",
            "LOAN_REQUEST_SEND": "Pengajuan Pinjaman",
            "LOAN_REQUEST_APPROVE": "Persetujuan – Pengajuan Pinjaman",
            "LOAN_REQUEST_REJECT": "Penolakan Pinjaman",
            "LOAN_REQUEST_DISBURSE": "Pencairan Dana Pinjaman ",
            "LOAN_REQUEST_REPAYMENT": "Pemberitahuan Pelunasan Pinjaman Berhasil",
            "LOAN_REQUEST_REPAYMENT_MOBILE": "Pemberitahuan Pelunasan Pinjaman Berhasil",
            "REMINDER_BEFORE_DUEDATE": "Pemberitahuan Jatuh Tempo Pinjaman",
            "REMINDER_AFTER_DUEDATE": "Pemberitahuan Keterlambatan Pembayaran Pinjaman",
        },
        "CONTENT": {
            "LOAN_REQUEST_SEND": "Pengajuan pinjaman $loan_request_code Anda sudah diterima oleh Tim Analis Kami dan akan diproses lebih lanjut.",
            "LOAN_REQUEST_APPROVE": "Pengajuan Pinjaman $loan_request_code Anda telah disetujui, dan akan segera dicairkan dalam 1x24 jam.",
            "LOAN_REQUEST_REJECT": "Mohon maaf, untuk saat ini pengajuan pinjaman Anda $loan_request_code tidak disetujui karena belum memenuhi Syarat dan Ketentuan yang berlaku.",
            "LOAN_REQUEST_DISBURSE": "Selamat! Pinjaman yang Anda ajukan telah dicairkan ke rekening MODANAKU.",
            "LOAN_REQUEST_REPAYMENT": "Terima kasih, Anda telah berhasil melakukan pembayaran pinjaman: $product - $loan_request_code sejumlah $repayment_amount",
            "REMINDER_BEFORE_DUEDATE": "Pinjaman Anda $loan_request_code akan segera jatuh tempo. Pastikan saldo MODANAKU cukup untuk membayar jumlah pinjaman untuk menghindari denda keterlambatan.",
            "REMINDER_AFTER_DUEDATE": "Pinjaman Anda $loan_request_code telah jatuh tempo. Segera lakukan pembayaran manual via MODANAKU Anda, pembayaran setelah tanggal jatuh tempo akan dikenakan denda keterlambatan sesuai ketentuan yang berlaku",
            "REMINDER_DUEDATE": "Pinjaman Anda $loan_request_code jatuh tempo hari ini. Pastikan saldo MODANAKU cukup untuk membayar jumlah pinjaman untuk menghindari denda keterlambatan.",
        },
    }
}
