
from compress import Character
from functools import reduce
from bitarray import bitarray


with open('mensaje.jpg', 'rb') as f:
    byte_list = f.read()

print('finished reading the file')

bset = set(byte_list)
caracteres = [Character([a], byte_list.count(a), elemental=True) for a in bset]

print('finished making the alphabet')

codigo = Character.build_tree(caracteres)

print('finished making the code')

codificado = bitarray()
for a in byte_list:
    codificado.extend(codigo.code(a))

print('finished coding')

index = 0
cadena = bytearray()

copia_codificado = bitarray()
copia_codificado.extend(codificado)

while index < len(codificado):
    # want to make it faster
    if index > 64:
        codificado.throw(64)
        index -= 64
    c, index = codigo.decode(codificado, index)
    cadena.append(c)

print('finished decoding')

codificado = bitarray()
codificado.extend(copia_codificado)

bytes_comprimido = (len(codificado) + 7) // 8
bytes_sin_comprimir = len(byte_list)
ratio = 100 * (bytes_comprimido / bytes_sin_comprimir)
print('Comprimido {:d}'.format(bytes_comprimido))
print('Sin comprimir {:d}'.format(bytes_sin_comprimir))
print('Compresion {:4.2f}%'.format(ratio))
print('finished decoding')

with open('resultado.txt', 'wb') as f:
    f.write(cadena)
