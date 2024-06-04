def hamming_encode(data):
    """
    Кодирование данных с использованием кода Хэмминга.
    Принимает строку и возвращает строку.
    """
    data = list(map(int, data))
    m = len(data)
    r = 0

    while (2**r) < (m + r + 1):
        r += 1

    hamming_code = [0] * (m + r)

    j = 0
    for i in range(1, len(hamming_code) + 1):
        if i == 2**j:
            j += 1
        else:
            hamming_code[i - 1] = data.pop(0)

    for i in range(r):
        position = 2**i
        xor_sum = 0
        for j in range(position - 1, len(hamming_code), 2 * position):
            xor_sum ^= sum(hamming_code[j:j + position])
        hamming_code[position - 1] = xor_sum % 2

    return ''.join(map(str, hamming_code))

def hamming_decode(hamming_code):
    """
    Декодирование данных с использованием кода Хэмминга.
    Принимает строку и возвращает строку.
    """
    hamming_code = list(map(int, hamming_code))
    r = 0

    while (2**r) < len(hamming_code):
        r += 1

    error_position = 0
    for i in range(r):
        position = 2**i
        xor_sum = 0
        for j in range(position - 1, len(hamming_code), 2 * position):
            xor_sum ^= sum(hamming_code[j:j + position])
        error_position += (xor_sum % 2) * position

    if error_position > 0:
        hamming_code[error_position - 1] ^= 1

    decoded_data = []
    j = 0
    for i in range(1, len(hamming_code) + 1):
        if i != 2**j:
            decoded_data.append(hamming_code[i - 1])
        else:
            j += 1

    return ''.join(map(str, decoded_data))