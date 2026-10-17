from vector_clock import VectorClock

# Simulasi sistem dengan 3 proses
vc0 = VectorClock(num_processes=3, process_id=0)
vc1 = VectorClock(num_processes=3, process_id=1)
vc2 = VectorClock(num_processes=3, process_id=2)

print("=== STATUS AWAL ===")
print(vc0)
print(vc1)
print(vc2)

# Proses 0 melakukan local event
vc0.increment()
print("\n=== SETELAH P0 LOCAL EVENT ===")
print(vc0)

# Proses 0 mengirim pesan ke Proses 1
message_from_p0 = vc0.send_message()
vc1.receive_message(message_from_p0)
print("\n=== SETELAH P0 KIRIM PESAN KE P1 ===")
print(vc0)
print(vc1)

# Proses 2 melakukan local event
vc2.increment()
print("\n=== SETELAH P2 LOCAL EVENT ===")
print(vc2)

# Proses 1 mengirim pesan ke Proses 2
message_from_p1 = vc1.send_message()
vc2.receive_message(message_from_p1)
print("\n=== SETELAH P1 KIRIM PESAN KE P2 ===")
print(vc1)
print(vc2)

# Pengecekan Kausalitas
print("\n=== PENGECEKAN KASUALITAS (CAUSALITY) ===")
print(f"vc0 happens before vc1: {vc0.happens_before(vc1)}")
print(f"vc1 happens before vc0: {vc1.happens_before(vc0)}")
print(f"vc0 is concurrent with vc2: {vc0.is_concurrent(vc2)}")