import qrcode
from io import BytesIO
from django.core.files import File
from django.conf import settings


def gerar_qr_code(aula):
    """
    Gera um QR Code para a aula e salva no campo qr_code do modelo.
    O link embutido no QR Code aponta para a página de registro de presença.
    """
    # Monta o link que o aluno vai acessar ao escanear o QR Code
    url = f"http://127.0.0.1:8000/presenca/?id={aula.id}&token={aula.token}"

    # Configura a aparência do QR Code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )

    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    # Salva a imagem em memória (sem precisar gravar em disco manualmente)
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)

    nome_arquivo = f'aula_{aula.id}_{aula.token}.png'

    # Salva no campo ImageField do modelo
    aula.qr_code.save(nome_arquivo, File(buffer), save=True)

    return aula