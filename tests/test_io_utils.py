from src.regulon_summary import load_interactions

def test_load_interactions_ignores_invalid_lines(tmp_path):
    # Esta prueba verifica que load_interactions solo conserve
    # interacciones válidas desde un archivo TSV temporal.
    #
    # El archivo contiene:
    # - un comentario,
    # - un encabezado,
    # - dos interacciones válidas,
    # - una interacción inválida con efecto "?".

    input_file = tmp_path / "interactions.tsv"

    input_file.write_text(
        "# comentario\n"
        "1)regulatorId\tregulatorName\tX\tX\tgeneName\teffect\tX\n"
        "id1\tCRP\tX\tX\tlacZ\t+\tX\n"
        "id2\tFNR\tX\tX\tnarG\t-\tX\n"
        "id3\tBAD\tX\tX\tgeneX\t?\tX\n"
    )

    interactions = load_interactions(input_file)

    assert interactions == [
        ("CRP", "lacZ", "+"),
        ("FNR", "narG", "-"),
    ]
    

def test_load_interactions_ignores_empty_lines(tmp_path):
    # Esta prueba verifica que load_interactions ignore líneas vacías.
    #
    # El archivo temporal contiene una línea vacía entre dos interacciones válidas.
    # La función debe conservar únicamente las interacciones válidas.

    input_file = tmp_path / "interactions.tsv"

    input_file.write_text(
        "id1\tCRP\tX\tX\tlacZ\t+\tX\n"
        "\n"
        "id2\tFNR\tX\tX\tnarG\t-\tX\n"
    )

    interactions = load_interactions(input_file)

    assert interactions == [
        ("CRP", "lacZ", "+"),
        ("FNR", "narG", "-"),
    ]


def test_load_interactions_keeps_plus_minus_effect(tmp_path):
    # Esta prueba verifica que load_interactions conserve interacciones
    # cuyo efecto sea '+-'.
    #
    # El efecto '+-' representa una regulación dual.

    input_file = tmp_path / "interactions.tsv"

    input_file.write_text(
        "id1\tAraC\tX\tX\taraB\t+-\tX\n"
    )

    interactions = load_interactions(input_file)

    assert ("AraC", "araB", "+-") in interactions
    assert len(interactions) == 1


def test_load_interactions_ignores_lines_with_few_columns(tmp_path):
    # Esta prueba verifica que load_interactions ignore líneas incompletas.
    #
    # La primera línea tiene pocas columnas, por lo tanto debe descartarse.
    # La segunda línea sí tiene las columnas necesarias y debe conservarse.

    input_file = tmp_path / "interactions.tsv"

    input_file.write_text(
        "id1\tCRP\tX\n"
        "id2\tFNR\tX\tX\tnarG\t-\tX\n"
    )

    interactions = load_interactions(input_file)

    assert interactions == [
        ("FNR", "narG", "-"),
    ]


def test_load_interactions_empty_filename_raises_value_error():
    # Esta prueba verifica que load_interactions produzca un ValueError
    # cuando recibe un nombre de archivo vacío.
    #
    # Primero se intenta ejecutar load_interactions("").
    # Como la cadena está vacía, la función debería lanzar un ValueError.
    #
    # Si la función NO lanza el error, se ejecuta assert False
    # y la prueba falla.
    #
    # Si la función SÍ lanza ValueError, el except lo captura
    # y la prueba pasa con assert True.

    try:
        load_interactions("")
        assert False
    except ValueError:
        assert True