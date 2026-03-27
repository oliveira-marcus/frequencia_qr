from math import radians, sin, cos, sqrt, atan2


# Range de IPs permitidos da universidade
# Numa situação real, esses valores viriam do settings.py ou banco de dados
IPS_INSTITUCIONAIS = [
    '127.0.0.1',       # localhost (para testes)
    '192.168.1.',      # exemplo de rede local
    '10.0.0.',         # exemplo de rede institucional
]


def get_ip_cliente(request):
    """
    Obtém o IP real do cliente, considerando proxies.
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')


def validar_rede(ip):
    """
    Verifica se o IP do aluno pertence à rede institucional.
    Retorna True se válido, False caso contrário.
    """
    for ip_permitido in IPS_INSTITUCIONAIS:
        if ip.startswith(ip_permitido) or ip == ip_permitido:
            return True
    return False


def calcular_distancia(lat1, lon1, lat2, lon2):
    """
    Calcula a distância em metros entre dois pontos geográficos
    usando a fórmula de Haversine.
    """
    R = 6371000  # Raio da Terra em metros

    lat1, lon1, lat2, lon2 = map(radians, [
        float(lat1), float(lon1),
        float(lat2), float(lon2)
    ])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c


def validar_geolocalizacao(lat_aluno, lon_aluno, sala):
    """
    Verifica se o aluno está dentro do raio permitido da sala.
    Retorna (True, distancia) se válido, (False, distancia) caso contrário.
    """
    distancia = calcular_distancia(
        lat_aluno, lon_aluno,
        sala.latitude, sala.longitude
    )
    return distancia <= sala.raio_permitido, distancia


def validar_horario(aula):
    """
    Verifica se o registro está sendo feito dentro do horário da aula.
    Permite um intervalo de 15 minutos antes e depois.
    """
    from django.utils import timezone
    from datetime import timedelta

    agora = timezone.localtime(timezone.now())
    hoje = agora.date()
    hora_atual = agora.time()

    # A aula precisa ser hoje
    if aula.data != hoje:
        return False, 'A aula não está ocorrendo hoje.'

    # Calcula janela de tolerância de 15 minutos
    from datetime import datetime
    inicio = datetime.combine(hoje, aula.horario_inicio) - timedelta(minutes=15)
    fim = datetime.combine(hoje, aula.horario_fim) + timedelta(minutes=15)
    agora_dt = datetime.combine(hoje, hora_atual)

    if not (inicio <= agora_dt <= fim):
        return False, f'Fora do horário da aula ({aula.horario_inicio} — {aula.horario_fim}).'

    return True, 'ok'