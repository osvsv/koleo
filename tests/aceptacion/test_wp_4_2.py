"""WP-4.2 — Avance por distancia con encoders (CA-4.2.1 a CA-4.2.3)."""
import math

import pytest


def _od():
    from pi import odometria
    return odometria


def test_ca_4_2_1_una_vuelta_es_pi_por_6_5_cm():
    """CA-4.2.1"""
    od = _od()
    assert od.pulsos_a_cm(515) == pytest.approx(math.pi * 6.5, abs=0.01)
    assert od.pulsos_a_cm(515) == pytest.approx(20.42, abs=0.01)
    assert od.pulsos_a_cm(0) == 0


@pytest.mark.parametrize("n", [100, 515, 1000])
def test_ca_4_2_2_ida_y_vuelta(n):
    """CA-4.2.2"""
    od = _od()
    assert od.cm_a_pulsos(od.pulsos_a_cm(n)) == pytest.approx(n, abs=1)


def test_ca_4_2_2_30_cm_son_757_pulsos():
    """CA-4.2.2"""
    assert _od().cm_a_pulsos(30) == pytest.approx(757, abs=1)


@pytest.mark.parametrize("pulsos", [-1, -515, -1000])
def test_ca_4_2_3_pulsos_negativos_distancia_negativa(pulsos):
    """CA-4.2.3"""
    od = _od()
    assert od.pulsos_a_cm(pulsos) < 0
    assert od.pulsos_a_cm(pulsos) == pytest.approx(-od.pulsos_a_cm(-pulsos))
