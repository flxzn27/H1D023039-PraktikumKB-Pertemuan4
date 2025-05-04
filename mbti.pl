% Database dinamis
:- dynamic sifat_pos/1.
:- dynamic sifat_neg/1.

% Preferensi MBTI
sifat(introvert, ["ISTJ", "ISFJ", "INFJ", "INTJ", "ISTP", "ISFP", "INFP", "INTP"]).
sifat(ekstrovert, ["ESTP", "ESFP", "ENFP", "ENTP", "ESTJ", "ESFJ", "ENFJ", "ENTJ"]).
sifat(intuitif, ["INFJ", "INTJ", "INFP", "INTP", "ENFP", "ENTP", "ENFJ", "ENTJ"]).
sifat(sensing, ["ISTJ", "ISFJ", "ISTP", "ISFP", "ESTP", "ESFP", "ESTJ", "ESFJ"]).
sifat(thinking, ["ISTJ", "INTJ", "ISTP", "INTP", "ESTP", "ENTP", "ESTJ", "ENTJ"]).
sifat(feeling, ["ISFJ", "INFJ", "ISFP", "INFP", "ESFP", "ENFP", "ESFJ", "ENFJ"]).
sifat(perceiving, ["ISTP", "ISFP", "INFP", "INTP", "ESTP", "ESFP", "ENFP", "ENTP"]).
sifat(judging, ["ISTJ", "ISFJ", "INFJ", "INTJ", "ESTJ", "ESFJ", "ENFJ", "ENTJ"]).

% Aturan penilaian MBTI berdasarkan preferensi
hitung_mbti(Tipe) :-
    % Hitung skor dimensi I/E
    hitung_pref(introvert, SkorI),
    hitung_pref(ekstrovert, SkorE),
    (SkorI >= SkorE -> I_E = 'I' ; I_E = 'E'),

    % Hitung skor dimensi N/S
    hitung_pref(intuitif, SkorN),
    hitung_pref(sensing, SkorS),
    (SkorN >= SkorS -> N_S = 'N' ; N_S = 'S'),

    % Hitung skor dimensi T/F
    hitung_pref(thinking, SkorT),
    hitung_pref(feeling, SkorF),
    (SkorT >= SkorF -> T_F = 'T' ; T_F = 'F'),

    % Hitung skor dimensi J/P
    hitung_pref(judging, SkorJ),
    hitung_pref(perceiving, SkorP),
    (SkorJ >= SkorP -> J_P = 'J' ; J_P = 'P'),

    % Gabungkan hasil
    atom_concat(I_E, N_S, A1),
    atom_concat(A1, T_F, A2),
    atom_concat(A2, J_P, Tipe).

% Hitung jumlah sifat_pos(X) yang masuk dalam preferensi tertentu
hitung_pref(Kategori, Count) :-
    findall(1, (sifat_pos(X), atom_concat(Kategori, _, X)), List),
    length(List, Count).

% PERTANYAAN UNTUK MBTI (12 pertanyaan, 3 per dimensi)
pertanyaan(introvert_1, "Apakah Anda lebih suka menyendiri daripada berada di keramaian?").
pertanyaan(introvert_2, "Apakah Anda merasa kehabisan energi setelah bersosialisasi?").
pertanyaan(introvert_3, "Apakah Anda lebih suka berpikir sebelum berbicara?").

pertanyaan(ekstrovert_1, "Apakah Anda senang berbicara di depan umum?").
pertanyaan(ekstrovert_2, "Apakah Anda merasa berenergi setelah bertemu orang banyak?").
pertanyaan(ekstrovert_3, "Apakah Anda mudah bergaul dengan orang baru?").

pertanyaan(intuitif_1, "Apakah Anda lebih fokus pada ide dan konsep daripada fakta?").
pertanyaan(intuitif_2, "Apakah Anda sering memikirkan kemungkinan masa depan?").
pertanyaan(intuitif_3, "Apakah Anda suka mencari pola atau makna tersembunyi?").

pertanyaan(sensing_1, "Apakah Anda lebih suka informasi yang konkret dan nyata?").
pertanyaan(sensing_2, "Apakah Anda cenderung memperhatikan detail?").
pertanyaan(sensing_3, "Apakah Anda lebih percaya pada pengalaman langsung daripada teori?").

pertanyaan(thinking_1, "Apakah Anda lebih mengutamakan logika daripada perasaan dalam membuat keputusan?").
pertanyaan(thinking_2, "Apakah Anda merasa nyaman dalam debat logis?").
pertanyaan(thinking_3, "Apakah Anda cenderung menilai berdasarkan kriteria objektif?").

pertanyaan(feeling_1, "Apakah Anda memperhatikan perasaan orang lain saat membuat keputusan?").
pertanyaan(feeling_2, "Apakah Anda menghindari konflik demi keharmonisan?").
pertanyaan(feeling_3, "Apakah Anda cenderung berempati terhadap masalah orang lain?").

pertanyaan(perceiving_1, "Apakah Anda suka menjaga fleksibilitas dalam rencana Anda?").
pertanyaan(perceiving_2, "Apakah Anda sering menunda keputusan sampai saat terakhir?").
pertanyaan(perceiving_3, "Apakah Anda lebih suka spontanitas daripada struktur?").

pertanyaan(judging_1, "Apakah Anda suka membuat dan mengikuti rencana?").
pertanyaan(judging_2, "Apakah Anda merasa nyaman dengan jadwal yang tetap?").
pertanyaan(judging_3, "Apakah Anda lebih suka menyelesaikan tugas sebelum bersantai?").