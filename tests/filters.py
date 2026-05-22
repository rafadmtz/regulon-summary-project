from src.regulon_summary import filter_by_min_genes, filter_by_type, filter_interactions_by_regulon

def test_filter_by_min_genes_keeps_only_regulators_with_enough_genes():
    # Esta prueba verifica que solo permanezcan los reguladores
    # que tienen al menos el número mínimo de genes indicado.

    regulon = {
        "CRP": {
            "genes": ["lacZ", "araB"],
            "activados": 2,
            "reprimidos": 0,
        },
        "FNR": {
            "genes": ["narG"],
            "activados": 0,
            "reprimidos": 1,
        },
    }

    filtered = filter_by_min_genes(regulon, min_genes=2)

    assert "CRP" in filtered
    assert "FNR" not in filtered
    assert len(filtered) == 1


def test_filter_by_type_keeps_only_activadores():
    # Esta prueba verifica que filter_by_type conserve únicamente
    # los reguladores clasificados como "activador".
    #
    # CRP es activador porque tiene genes activados
    # y no tiene genes reprimidos.

    regulon = {
        "CRP": {
            "genes": ["lacZ", "araB"],
            "activados": 2,
            "reprimidos": 0,
        },
        "FNR": {
            "genes": ["narG"],
            "activados": 0,
            "reprimidos": 1,
        },
        "AraC": {
            "genes": ["araB", "araC"],
            "activados": 1,
            "reprimidos": 1,
        },
    }

    filtered = filter_by_type(regulon, "activador")

    assert "CRP" in filtered
    assert "FNR" not in filtered
    assert "AraC" not in filtered
    assert len(filtered) == 1


def test_filter_by_type_keeps_only_represores():
    # Esta prueba verifica que filter_by_type conserve únicamente
    # los reguladores clasificados como "represor".
    #
    # FNR es represor porque no tiene genes activados
    # y sí tiene genes reprimidos.

    regulon = {
        "CRP": {
            "genes": ["lacZ", "araB"],
            "activados": 2,
            "reprimidos": 0,
        },
        "FNR": {
            "genes": ["narG"],
            "activados": 0,
            "reprimidos": 1,
        },
        "AraC": {
            "genes": ["araB", "araC"],
            "activados": 1,
            "reprimidos": 1,
        },
    }

    filtered = filter_by_type(regulon, "represor")

    assert "CRP" not in filtered
    assert "FNR" in filtered
    assert "AraC" not in filtered
    assert len(filtered) == 1


def test_filter_by_type_keeps_only_duales():
    # Esta prueba verifica que filter_by_type conserve únicamente
    # los reguladores clasificados como "dual".
    #
    # AraC es dual porque tiene genes activados
    # y genes reprimidos.

    regulon = {
        "CRP": {
            "genes": ["lacZ", "araB"],
            "activados": 2,
            "reprimidos": 0,
        },
        "FNR": {
            "genes": ["narG"],
            "activados": 0,
            "reprimidos": 1,
        },
        "AraC": {
            "genes": ["araB", "araC"],
            "activados": 1,
            "reprimidos": 1,
        },
    }

    filtered = filter_by_type(regulon, "dual")

    assert "CRP" not in filtered
    assert "FNR" not in filtered
    assert "AraC" in filtered
    assert len(filtered) == 1


def test_filter_by_type_returns_all_regulon_when_type_is_none():
    # Esta prueba verifica que si regulator_type es None,
    # filter_by_type no aplique ningún filtro.
    #
    # Por lo tanto, debe regresar el regulón completo.

    regulon = {
        "CRP": {
            "genes": ["lacZ", "araB"],
            "activados": 2,
            "reprimidos": 0,
        },
        "FNR": {
            "genes": ["narG"],
            "activados": 0,
            "reprimidos": 1,
        },
        "AraC": {
            "genes": ["araB", "araC"],
            "activados": 1,
            "reprimidos": 1,
        },
    }

    filtered = filter_by_type(regulon, None)

    assert filtered == regulon


def test_filter_interactions_by_regulon_keeps_only_filtered_tfs():
    # Esta prueba verifica que filter_interactions_by_regulon conserve
    # únicamente las interacciones cuyos TFs aparecen en el regulón filtrado.
    #
    # En este caso, el regulón filtrado solo contiene a CRP,
    # por lo tanto, solo deben conservarse las interacciones de CRP.

    interactions = [
        ("CRP", "lacZ", "+"),
        ("CRP", "araB", "+"),
        ("FNR", "narG", "-"),
        ("AraC", "araB", "+-"),
    ]

    regulon_filtrado = {
        "CRP": {
            "genes": ["lacZ", "araB"],
            "activados": 2,
            "reprimidos": 0,
        }
    }

    filtered_interactions = filter_interactions_by_regulon(
        interactions,
        regulon_filtrado,
    )

    assert filtered_interactions == [
        ("CRP", "lacZ", "+"),
        ("CRP", "araB", "+"),
    ]