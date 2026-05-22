from src.regulon_summary import write_summary, write_sif


def test_write_sif_writes_expected_interaction_labels(tmp_path):
    # Esta prueba verifica que write_sif convierta los efectos
    # +, - y +- en etiquetas SIF correctas.

    interactions = [
        ("CRP", "lacZ", "+"),
        ("FNR", "narG", "-"),
        ("AraC", "araB", "+-"),
    ]
    output_file = tmp_path / "network.sif"

    write_sif(interactions, output_file)

    content = output_file.read_text()

    assert "CRP	activates	lacZ" in content
    assert "FNR	represses	narG" in content
    assert "AraC	regulates	araB" in content
    
def test_write_summary_writes_expected_header_and_sorted_genes(tmp_path):
    # Esta prueba verifica que write_summary escriba correctamente
    # un archivo de resumen.
    #
    # También verifica dos cosas importantes:
    # 1. Que el archivo contenga el encabezado esperado.
    # 2. Que la lista de genes aparezca ordenada alfabéticamente.
    #
    # En el regulón, los genes de CRP están desordenados:
    # ["lacZ", "araB", "zraP"]
    #
    # Pero write_summary debe escribirlos ordenados como:
    # "araB, lacZ, zraP"

    regulon = {
        "CRP": {
            "genes": ["lacZ", "araB", "zraP"],
            "activados": 2,
            "reprimidos": 0,
        },
        "FNR": {
            "genes": ["narG"],
            "activados": 0,
            "reprimidos": 1,
        },
    }

    output_file = tmp_path / "summary.tsv"

    write_summary(regulon, output_file)

    content = output_file.read_text()

    assert "TF\tTotal genes\tActivados\tReprimidos\tTipo\tLista de genes" in content
    assert "CRP\t3\t2\t0\tactivador\taraB, lacZ, zraP" in content
    assert "FNR\t1\t0\t1\trepresor\tnarG" in content


def test_write_summary_with_none_regulon_raises_value_error(tmp_path):
    # Esta prueba verifica que write_summary produzca un ValueError
    # cuando el regulón recibido es None.
    #
    # Esto es importante porque write_summary necesita un diccionario
    # con información de reguladores para poder escribir el resumen.
    #
    # Si la función NO lanza el error, se ejecuta assert False
    # y la prueba falla.
    #
    # Si la función SÍ lanza ValueError, el except lo captura
    # y la prueba pasa con assert True.

    output_file = tmp_path / "summary.tsv"

    try:
        write_summary(None, output_file)
        assert False
    except ValueError:
        assert True


def test_write_sif_empty_output_file_raises_value_error():
    # Esta prueba verifica que write_sif produzca un ValueError
    # cuando output_file está vacío.
    #
    # write_sif necesita una ruta válida para escribir el archivo SIF.
    # Si se le pasa una cadena vacía, debe marcar error.
    #
    # Si la función NO lanza el error, se ejecuta assert False
    # y la prueba falla.
    #
    # Si la función SÍ lanza ValueError, el except lo captura
    # y la prueba pasa con assert True.

    interactions = [
        ("CRP", "lacZ", "+"),
        ("FNR", "narG", "-"),
    ]

    try:
        write_sif(interactions, "")
        assert False
    except ValueError:
        assert True