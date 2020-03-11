"""
    Constant used in lending engine
"""
import os

P2P_ID = os.environ.get("P2P_ID") or "123456"

TYPE_TO_BANK_TYPES = {
    "INVESTOR": "RDL_ACCOUNT",
    "INVESTOR_RDL_ACC": "RDL_ACCOUNT",
    "INVESTMENT": "VIRTUAL_ACCOUNT",
    "MODANAKU": {"ACCOUNT_TYPE": "VIRTUAL_ACCOUNT", "LABEL": "MODANAKU"},
    "REPAYMENT": {"ACCOUNT_TYPE": "VIRTUAL_ACCOUNT", "LABEL": "REPAYMENT"},
    "ESCROW": "BANK_ACCOUNT",
    "PROFIT": "BANK_ACCOUNT",
}

TYPE_TO_MODELS = {
    "INVESTOR": "Investor",
    "INVESTMENT": "Investment",
    "INVESTOR_BANK_ACC": "Investor",
    "INVESTOR_RDL_ACC": "Investor",
    "ESCROW": "Wallet",
    "PROFIT": "Wallet",
    "MODANAKU": "LoanRequest",
    "REPAYMENT": "LoanRequest",
}

# using this variable we can decide what type of provider we select based on
# source
PROVIDER_ROUTES = {
    "RDL_ACCOUNT": "BNI_RDL",
    "BANK_ACCOUNT": "BNI_OPG",
    "VIRTUAL_ACCOUNT": "BNI_OPG",
}
# using this variable we can put conditional based on active or passive
# transaction
TRANSFER_TYPES = {
    "ACTIVE": [
        "INVEST",
        "DISBURSE",
        "UPFRONT_FEE",
        "INVEST_FEE",
        "RECEIVE_UPFRONT_FEE",
        "INVEST_REPAYMENT",
        "RECEIVE_INVEST_FEE",
    ],
    "INTERNAL": ["DEBIT_REFUND", "CREDIT_REFUND"],
    "PASSIVE": ["RECEIVE_INVEST", "RECEIVE_REPAYMENT", "TOP_UP_RDL"],
}


TRANSACTION_TYPE_TO_STATUS = {
    "INVEST": "SEND_TO_INVESTMENT",
    "RECEIVE_INVEST": "RECEIVE_FROM_INVESTMENT",
    "UPFRONT_FEE": "SEND_TO_PROFIT",
    "RECEIVE_UPFRONT_FEE": "RECEIVE_FROM_ESCROW",
    "DISBURSE": "SEND_TO_MODANAKU",
    "RECEIVE_REPAYMENT": "RECEIVE_FROM_MODANAKU",
    "INVEST_FEE": "SEND_FEE_TO_ESCROW",
    "RECEIVE_INVEST_FEE": "RECEIVE_FEE_FROM_PROFIT",
    "INVEST_REPAYMENT": "SEND_TO_RDL",
    "WITHDRAW": "WITHDRAW_FROM_RDL",
    "CREDIT_ADJUSTMENT": "CREDIT_ADJUSTMENT",
    "DEBIT_ADJUSTMENT": "DEBIT_ADJUSTMENT",
    "CREDIT_REFUND": "CREDIT_REFUND",
    "DEBIT_REFUND": "DEBIT_REFUND",
}


SCHEDULES = [
    # IN WIB
    {"name": "UPFRONT_FEE", "start": "19:1", "end": "12:59", "executed_at": "13:0"},
    {"name": "UPFRONT_FEE", "start": "13:1", "end": "18:59", "executed_at": "19:0"},
    {"name": "INVEST_FEE", "start": "20:1", "end": "7:59", "executed_at": "8:0"},
    {"name": "INVEST_FEE", "start": "8:1", "end": "19:59", "executed_at": "20:0"},
]

LOAN_QUALITIES = {
    "LANCAR": {"start": "0", "end": "30", "operator": "<="},
    "TIDAK_LANCAR": {"start": "31", "end": "90", "operator": "<="},
    "MACET": {"start": "91", "operator": ">="},
}

NOTIFICATIONS = {
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
        "LOAN_REQUEST_CANCEL": "Pembatalan Pinjaman",
        "LOAN_REQUEST_REPAYMENT": "Pemberitahuan Pelunasan Pinjaman Berhasil",
        "LOAN_REQUEST_REPAYMENT_MOBILE": "Pemberitahuan Pelunasan Pinjaman Berhasil",
        "REMINDER_BEFORE_DUEDATE": "Pemberitahuan Jatuh Tempo Pinjaman",
        "REMINDER_AFTER_DUEDATE": "Pemberitahuan Keterlambatan Pembayaran Pinjaman",
    },
    "TYPE": {
        "INVESTOR_APPROVE": "INVESTOR_APPROVED",
        "INVESTOR_REJECT": "INVESTOR_REJECTED",
        "INVESTOR_DISBURSE": "INVESTOR_DISBURSED",
        "INVESTOR_TOPUP": "TOP_UP",
        "INVESTOR_REPAYMENT": "REPAYMENT",
        "INVESTOR_WITHDRAW": "WITHDRAW",
        "LOAN_REQUEST_SEND": "LOAN_SUBMITTED",
        "LOAN_REQUEST_APPROVE": "LOAN_APPROVED",
        "LOAN_REQUEST_REJECT": "LOAN_REJECTED",
        "LOAN_REQUEST_DISBURSE": "LOAN_DISBURSED",
        "LOAN_REQUEST_REPAYMENT": "LOAN_REPAID",
        "LOAN_REQUEST_REPAYMENT_MOBILE": "LOAN_REPAID",
        "LOAN_REQUEST_CANCEL": "LOAN_CANCELLED",
        "REMINDER_BEFORE_DUEDATE": "DUE_DATE",
        "REMINDER_AFTER_DUEDATE": "OVERDUE_DATE",
    },
    "CONTENT": {
        "web": {
            "INVESTOR_APPROVE": "Selamat! Registrasi anda telah berhasil disetujui. Akses: https://investor.mopinjam.id untuk dapat mengakses akun anda dan mulai pendanaan.",
            "INVESTOR_REJECT": "Mohon maaf, untuk saat ini pengajuan registrasi anda belum dapat disetujui karena belum memenuhi Syarat dan Ketentuan yang berlaku.",
            "INVESTOR_DISBURSE": "Investasi yang anda berikan telah berhasil dicairkan ke rekening peminjam anda.",
            "INVESTOR_TOPUP": "Pengisian saldo Rekening Dana Lender anda telah berhasil. Anda sudah dapat mulai berinvestasi melalui akun anda.",
            "INVESTOR_REPAYMENT": "Anda telah menerima pembayaran dari peminjam: Waktu Pembayaran: $repayment_date Jumlah Pembayaran: Rp. $repayment_amount Jenis Pinjaman:  $product",
            "INVESTOR_WITHDRAW": "Penarikan dana dari Rekening Dana Lender anda telah berhasil dilakukan: Waktu Penarikan: $withdraw_date Jumlah Penarikan: Rp. $withdraw_amount ",
            "LOAN_REQUEST_SEND": "Pengajuan pinjaman $loan_request_code Anda sudah diterima oleh Tim Analis Kami dan akan diproses lebih lanjut.",
            "LOAN_REQUEST_APPROVE": "Pengajuan Pinjaman $loan_request_code Anda telah disetujui, dan akan segera dicairkan dalam 1x24 jam.",
            "LOAN_REQUEST_REJECT": "Mohon maaf, untuk saat ini pengajuan pinjaman Anda $loan_request_code tidak disetujui karena belum memenuhi Syarat dan Ketentuan yang berlaku.",
            "LOAN_REQUEST_DISBURSE": "Selamat! No Pinjaman $loan_request_code yang Anda ajukan telah berhasil dicairkan ke rekening MODANAKU Anda. Segera melakukan pengecekan saldo MODANAKU Anda. Detil informasi pinjaman dapat dilihat pada menu PINJAMAN Anda.",
            "LOAN_REQUEST_REPAYMENT": "Terima kasih, Anda telah berhasil melakukan pembayaran pinjaman:<br><br>"
            + "Waktu Pembayaran: $repayment_date <br>"
            + "Nomor Pinjaman: $loan_request_code <br>"
            + "Jumlah Pembayaran: Rp. $repayment_amount <br>"
            + "Produk Pinjaman:  $product",
            "LOAN_REQUEST_CANCEL": "Mohon maaf, untuk saat ini pengajuan pinjaman Anda $loan_request_code dibatalkan karena belum diproses dalam 1x24 jam",
            "LOAN_REQUEST_REPAYMENT_mobile": "Terima kasih, Anda telah berhasil melakukan pembayaran pinjaman: $product - $loan_request_code sejumlah $repayment_amount",
            "REMINDER_BEFORE_DUEDATE": "Pinjaman Anda $loan_request_code akan segera jatuh tempo. Pastikan saldo MODANAKU cukup untuk membayar jumlah pinjaman untuk menghindari denda keterlambatan.",
            "REMINDER_AFTER_DUEDATE": "Pinjaman Anda $loan_request_code telah jatuh tempo. Segera lakukan pembayaran manual via MODANAKU Anda, pembayaran setelah tanggal jatuh tempo akan dikenakan denda keterlambatan sesuai ketentuan yang berlaku",
            "REMINDER_DUEDATE": "Pinjaman Anda $loan_request_code jatuh tempo hari ini. Pastikan saldo MODANAKU cukup untuk membayar jumlah pinjaman untuk menghindari denda keterlambatan.",
        },
        "mobile": {
            "INVESTOR_APPROVE": "Selamat! Registrasi anda telah berhasil disetujui. Akses: https://investor.mopinjam.id untuk dapat mengakses akun anda dan mulai pendanaan.",
            "INVESTOR_REJECT": "Mohon maaf, untuk saat ini pengajuan registrasi anda belum dapat disetujui karena belum memenuhi Syarat dan Ketentuan yang berlaku.",
            "INVESTOR_DISBURSE": "Investasi yang anda berikan telah berhasil dicairkan ke rekening peminjam anda.",
            "INVESTOR_TOPUP": "Pengisian saldo Rekening Dana Lender anda telah berhasil. Anda sudah dapat mulai berinvestasi melalui akun anda.",
            "INVESTOR_REPAYMENT": "Anda telah menerima pembayaran dari peminjam: Waktu Pembayaran: $repayment_date Jumlah Pembayaran: Rp. $repayment_amount Jenis Pinjaman:  $product",
            "INVESTOR_WITHDRAW": "Penarikan dana dari Rekening Dana Lender anda telah berhasil dilakukan: Waktu Penarikan: $withdraw_date Jumlah Penarikan: Rp. $withdraw_amount ",
            "LOAN_REQUEST_SEND": "Pengajuan pinjaman $loan_request_code Anda sudah diterima oleh Tim Analis Kami dan akan diproses lebih lanjut.",
            "LOAN_REQUEST_APPROVE": "Pengajuan Pinjaman $loan_request_code Anda telah disetujui, dan akan segera dicairkan dalam 1x24 jam.",
            "LOAN_REQUEST_REJECT": "Mohon maaf, untuk saat ini pengajuan pinjaman Anda $loan_request_code tidak disetujui karena belum memenuhi Syarat dan Ketentuan yang berlaku.",
            "LOAN_REQUEST_CANCEL": "Mohon maaf, untuk saat ini pengajuan pinjaman Anda $loan_request_code dibatalkan karena belum diproses dalam 1x24 jam",
            "LOAN_REQUEST_DISBURSE": "Selamat! No Pinjaman $loan_request_code yang Anda ajukan telah berhasil dicairkan ke rekening MODANAKU Anda. Segera melakukan pengecekan saldo MODANAKU Anda. Detil informasi pinjaman dapat dilihat pada menu PINJAMAN Anda.",
            "LOAN_REQUEST_REPAYMENT": "Terima kasih, Anda telah berhasil melakukan pembayaran pinjaman: $product - $loan_request_code sejumlah $repayment_amount",
            "REMINDER_BEFORE_DUEDATE": "Pinjaman Anda $loan_request_code akan segera jatuh tempo. Pastikan saldo MODANAKU cukup untuk membayar jumlah pinjaman untuk menghindari denda keterlambatan.",
            "REMINDER_AFTER_DUEDATE": "Pinjaman Anda $loan_request_code telah jatuh tempo. Segera lakukan pembayaran manual via MODANAKU Anda, pembayaran setelah tanggal jatuh tempo akan dikenakan denda keterlambatan sesuai ketentuan yang berlaku",
            "REMINDER_DUEDATE": "Pinjaman Anda $loan_request_code jatuh tempo hari ini. Pastikan saldo MODANAKU cukup untuk membayar jumlah pinjaman untuk menghindari denda keterlambatan.",
        },
    },
}
