import pandas as pd
import re

def run_simulation(input_modal, input_rules, output_file, tahun):

    # =========================
    # LOAD DATA
    # =========================
    modal_df = pd.read_excel(input_modal, sheet_name='Informasi Awal')
    rules_df = pd.read_excel(input_rules, sheet_name='Rules')

    # Month conversions
    month_name_to_num = {
        'Januari': 1, 'Februari': 2, 'Maret': 3, 'April': 4,
        'Mei': 5, 'Juni': 6, 'Juli': 7, 'Agustus': 8,
        'September': 9, 'Oktober': 10, 'November': 11, 'Desember': 12
    }
    num_to_month_name = {v: k for k, v in month_name_to_num.items()}

    # =========================
    # PARSE RULES BY NAME
    # =========================
    rules_by_name = {}
    for _, row in rules_df.iterrows():
        name = row["Nama"]
        periode = str(row["Periode"]).split()
        if len(periode) < 2:
            continue

        month = month_name_to_num.get(periode[0], None)
        year = int(periode[1])
        action = str(row["Tindakan"])

        if month is None:
            continue

        rules_by_name.setdefault(name, []).append((year, month, action))

    # Sort events
    for nm in rules_by_name:
        rules_by_name[nm].sort(key=lambda x: (x[0], x[1]))

    # =========================
    # SPECIAL EVENTS SUSI
    # =========================
    susi_special_events = [
        (2004, 11, "stop_build 150"),
        (2006, 6, "set_rent 750000"),
        (2008, 5, "set_rent 1300000"),
    ]

    # =========================
    # WRITE OUTPUT
    # =========================
    with pd.ExcelWriter(output_file, engine="openpyxl") as writer:

        harta_list = []

        # ==================================================
        # PROCESS EACH OWNER
        # ==================================================
        for _, row in modal_df.iterrows():

            name = row["Nama"]

            # INITIAL VALUES
            p_start = str(row["Periode Mulai"]).split()
            start_month = month_name_to_num[p_start[0]]
            start_year = int(p_start[1])

            current_balance = int(row["Saldo Awal"])
            cost = int(row["Biaya Bangun Per Kamar"])
            inc_rate = float(row["Peningkatan Biaya Pembangunan Per Tahun"])
            rent_price = int(row["Harga Sewa Kos Per Kamar"])
            threshold_str = str(row["Threshold Bangun"])

            # Parse threshold
            threshold_type = None
            threshold_value = None
            threshold_operator = None

            if "%" in threshold_str:
                threshold_type = "percent"
                threshold_value = float(re.findall(r"(\d+)", threshold_str)[0])
            else:
                nums = re.findall(r"(\d+)", threshold_str)
                if nums:
                    threshold_type = "absolute"
                    threshold_value = int(nums[0]) * 1_000_000
                    threshold_operator = "ge" if ">=" in threshold_str else "gt"

            stop_build = None
            last_build_total = None

            # COPY RULES
            events = rules_by_name.get(name, []).copy()

            # Tambahkan event khusus Susi
            if name == "Susi":
                events += susi_special_events

            # Sort ulang event
            events.sort(key=lambda x: (x[0], x[1]))
            ev_index = 0
            timeline = []
            current_rooms = 0
            total_months = tahun * 12 + 1

            # ==================================================
            # SIMULATION (MONTH-by-MONTH)
            # ==================================================
            for step in range(total_months):

                offset = (start_month - 1) + step
                year = start_year + offset // 12
                month_idx = offset % 12 + 1
                month_name = num_to_month_name[month_idx]

                # Annual cost increase
                if step > 0 and month_idx == start_month:
                    cost = int(round(cost * (1 + inc_rate)))

                # FIRST MONTH: INITIAL CAPITAL + INITIAL BUILD
                if step == 0:
                    timeline.append({
                        "Bulan": month_name, "Tahun": year,
                        "Keterangan": "Modal Awal", "Kategori": "Modal",
                        "Nilai": current_balance,
                        "Total Kamar Kos": current_rooms, "Saldo": current_balance
                    })

                    if cost > 0:
                        n_rooms = current_balance // cost
                    else:
                        n_rooms = 0

                    if n_rooms > 0:
                        spent = n_rooms * cost
                        current_rooms += n_rooms
                        current_balance -= spent
                        last_build_total = spent

                        timeline.append({
                            "Bulan": month_name, "Tahun": year,
                            "Keterangan": f"Pembangunan Kamar Kos ({n_rooms} × Rp {cost:,.0f})",
                            "Kategori": "Pengeluaran",
                            "Nilai": -spent,
                            "Total Kamar Kos": current_rooms,
                            "Saldo": current_balance
                        })
                    continue

                # APPLY RULE EVENTS
                while ev_index < len(events) and events[ev_index][0] == year and events[ev_index][1] == month_idx:
                    action = events[ev_index][2].lower()
                    raw = events[ev_index][2]
                    nums = re.findall(r"(\d+)", raw)

                    if "sewa kos" in action or "set_rent" in action:
                        rent_price = int(nums[0])
                        timeline.append({
                            "Bulan": month_name, "Tahun": year,
                            "Keterangan": f"Penyesuaian: harga_sewa → {rent_price}",
                            "Kategori": "Penyesuaian",
                            "Nilai": 0,
                            "Total Kamar Kos": current_rooms,
                            "Saldo": current_balance
                        })

                    elif "stop_build" in action or "berhenti membangun" in action:
                        stop_build = int(nums[0])
                        timeline.append({
                            "Bulan": month_name, "Tahun": year,
                            "Keterangan": f"Penyesuaian: stop_building → {stop_build}",
                            "Kategori": "Penyesuaian",
                            "Nilai": 0,
                            "Total Kamar Kos": current_rooms,
                            "Saldo": current_balance
                        })

                    elif "biaya pembangunan per kamar kos" in action:
                        cost = int(nums[0])
                        timeline.append({
                            "Bulan": month_name, "Tahun": year,
                            "Keterangan": f"Penyesuaian: biaya_bangun → {cost}",
                            "Kategori": "Penyesuaian",
                            "Nilai": 0,
                            "Total Kamar Kos": current_rooms,
                            "Saldo": current_balance
                        })

                    elif "mengubah treshold" in action:
                        threshold_type = "percent"
                        threshold_value = float(nums[0])
                        timeline.append({
                            "Bulan": month_name, "Tahun": year,
                            "Keterangan": f"Penyesuaian: change_threshold → {int(threshold_value)}",
                            "Kategori": "Penyesuaian",
                            "Nilai": 0,
                            "Total Kamar Kos": current_rooms,
                            "Saldo": current_balance
                        })

                    ev_index += 1

                # RENT INCOME
                rent_income = current_rooms * rent_price
                if rent_income > 0:
                    current_balance += rent_income
                    timeline.append({
                        "Bulan": month_name, "Tahun": year,
                        "Keterangan": "Pendapatan Sewa Kamar",
                        "Kategori": "Pendapatan",
                        "Nilai": rent_income,
                        "Total Kamar Kos": current_rooms,
                        "Saldo": current_balance
                    })

                # CHECK BUILD ELIGIBILITY
                can_build = True
                if stop_build is not None and current_rooms >= stop_build:
                    can_build = False

                if can_build:
                    if threshold_type == "percent" and last_build_total is not None:
                        needed = (threshold_value / 100.0) * last_build_total
                        can_build = current_balance >= needed
                    elif threshold_type == "absolute":
                        if threshold_operator == "gt":
                            can_build = current_balance > threshold_value
                        elif threshold_operator == "ge":
                            can_build = current_balance >= threshold_value

                # EXECUTE BUILD
                if can_build and cost > 0:
                    n_rooms = current_balance // cost
                    if n_rooms > 0:
                        spent = n_rooms * cost
                        current_rooms += n_rooms
                        current_balance -= spent
                        last_build_total = spent
                        timeline.append({
                            "Bulan": month_name, "Tahun": year,
                            "Keterangan": f"Investasi Ulang ({n_rooms} × Rp {cost:,.0f})",
                            "Kategori": "Pengeluaran",
                            "Nilai": -spent,
                            "Total Kamar Kos": current_rooms,
                            "Saldo": current_balance
                        })

            # Write personal sheet
            pd.DataFrame(timeline).to_excel(writer, sheet_name=name, index=False)

            # Summary
            harta_list.append({
                "Nama": name,
                "Saldo": current_balance,
                "Kamar": current_rooms
            })

        # Write Harta
        pd.DataFrame(harta_list).to_excel(writer, sheet_name="Harta", index=False)

# MAIN
if __name__ == "__main__":
    run_simulation(
        input_modal="modal.xlsx",
        input_rules="informasi-tambahan.xlsx",
        output_file="simulasi.xlsx",
        tahun=10
    )
