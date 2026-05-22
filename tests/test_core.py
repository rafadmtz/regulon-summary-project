from src.regulon_summary import build_regulon, get_regulator_type, build_regulon

def test_build_regulon_counts_activated_and_repressed_genes():
    # Esta prueba verifica que build_regulon construya correctamente
    # el resumen de genes activados y reprimidos para cada regulador.

    interactions = [
        ("CRP", "lacZ", "+"),
        ("CRP", "araB", "+"),
        ("FNR", "narG", "-"),
    ]

    regulon = build_regulon(interactions)

    assert "CRP" in regulon
    assert len(regulon["CRP"]["genes"]) == 2
    assert regulon["CRP"]["activados"] == 2
    assert regulon["FNR"]["reprimidos"] == 1
    



def test_get_regulator_type_returns_activador():
    # Caso: tiene genes activados y ningún gen reprimido.
    data = {
        "genes": ["lacZ", "araB"],
        "activados": 2,
        "reprimidos": 0,
    }

    result = get_regulator_type(data)

    assert result == "activador"


def test_get_regulator_type_returns_represor():
    # Caso: no tiene genes activados y sí tiene genes reprimidos.
    data = {
        "genes": ["narG"],
        "activados": 0,
        "reprimidos": 1,
    }

    result = get_regulator_type(data)

    assert result == "represor"


def test_get_regulator_type_returns_dual():
    # Caso: tiene genes activados y genes reprimidos.
    data = {
        "genes": ["araB", "araC"],
        "activados": 1,
        "reprimidos": 1,
    }

    result = get_regulator_type(data)

    assert result == "dual"


def test_build_regulon_does_not_duplicate_same_gene_for_same_regulator():
    # Caso: el mismo gen aparece más de una vez para el mismo regulador.
    # build_regulon debe guardar el gen una sola vez en la lista de genes.

    interactions = [
        ("CRP", "lacZ", "+"),
        ("CRP", "lacZ", "+"),
    ]

    regulon = build_regulon(interactions)

    assert "CRP" in regulon
    assert regulon["CRP"]["genes"] == ["lacZ"]
    assert len(regulon["CRP"]["genes"]) == 1
    assert regulon["CRP"]["activados"] == 2
    assert regulon["CRP"]["reprimidos"] == 0
    
