"""WP-1.2 — Robot simulado (CA-1.2.1 a CA-1.2.5)."""
import pytest

from _ayudas import def_de_tema, es_valido, errores, eventos_de


def _mision(ruta, peso):
    from simulador.robot_falso import generar_mision
    return generar_mision(ruta, peso)


def _tipos(mision):
    return [e["tipo"] for e in eventos_de(mision)]


def test_ca_1_2_1_mensajes_validos_contra_esquema():
    """CA-1.2.1: todo mensaje es válido contra el esquema."""
    mision = _mision("RUTA_1", 8.45)
    assert mision
    for tema, payload in mision:
        assert not errores(def_de_tema(tema), payload), (tema, payload)


def test_ca_1_2_1_lift_ok_de_tar_101_y_drop_ok_final_en_destino():
    """CA-1.2.1: LIFT_OK de TAR-101 y DROP_OK final en (150, 120)."""
    mision = _mision("RUTA_1", 8.45)
    lifts = eventos_de(mision, "LIFT_OK")
    assert any(e["id_tarima"] == "TAR-101" for e in lifts)
    todos = eventos_de(mision)
    assert todos[-1]["tipo"] == "DROP_OK"
    drop = todos[-1]
    assert drop["id_tarima"] == "TAR-101"
    assert drop["x_cm"] == 150 and drop["y_cm"] == 120


def test_ca_1_2_1_id_evento_unicos():
    """CA-1.2.1"""
    ids = [e["id_evento"] for e in eventos_de(_mision("RUTA_1", 8.45))]
    assert len(ids) >= 2
    assert len(ids) == len(set(ids))


def test_ca_1_2_2_sobrepeso_sin_lift_ni_drop():
    """CA-1.2.2"""
    mision = _mision("RUTA_2", 11.80)
    tipos = _tipos(mision)
    assert "SOBREPESO" in tipos
    assert "LIFT_OK" not in tipos
    assert "DROP_OK" not in tipos
    for tema, payload in mision:
        assert es_valido(def_de_tema(tema), payload)


def test_ca_1_2_3_limite_inclusivo_10_kg():
    """CA-1.2.3: 10.0 se completa."""
    tipos = _tipos(_mision("RUTA_1", 10.0))
    assert "LIFT_OK" in tipos and "DROP_OK" in tipos
    assert "SOBREPESO" not in tipos


def test_ca_1_2_3_10_1_kg_se_rechaza():
    """CA-1.2.3: 10.1 se rechaza."""
    tipos = _tipos(_mision("RUTA_1", 10.1))
    assert "SOBREPESO" in tipos
    assert "LIFT_OK" not in tipos and "DROP_OK" not in tipos


def test_ca_1_2_4_ruta_desconocida():
    """CA-1.2.4"""
    with pytest.raises(ValueError):
        _mision("RUTA_99", 8.45)


@pytest.mark.parametrize("ruta,peso", [("RUTA_1", 8.45), ("RUTA_3", 6.20)])
def test_ca_1_2_5_telemetria_cada_500_ms_o_menos(ruta, peso):
    """CA-1.2.5"""
    ts = [p["ts"] for t, p in _mision(ruta, peso) if t.endswith("/telemetria")]
    assert len(ts) >= 2
    for a, b in zip(ts, ts[1:]):
        assert abs(b - a) <= 500, (a, b)
