# -*- coding: utf-8 -*-


import pytest


@pytest.fixture(scope='function')
def code_cusp_vasp(code):
    """
    Create a code object using the cusp.vasp input plugin.
    """
    code.set_attribute('input_plugin', 'cusp.vasp')
    code.store()
    yield code


@pytest.mark.parametrize('valid_input', ['incar', 'kpoints', 'poscar',
                         'potcar', 'restart'])
def test_input_port_availability(valid_input):
    from aiida.plugins import CalculationFactory
    inputs = CalculationFactory('cusp.vasp').get_builder()._valid_fields
    assert valid_input in inputs


def test_vasp_calculation_setup(code_cusp_vasp, incar, kpoints, poscar,
                                with_H_PBE_potcar, temporary_cwd,
                                clear_database_after_test):
    import pathlib

    from aiida.plugins import CalculationFactory
    from aiida.engine import run, submit

    from aiida_cusp.data import VaspPotcarData

    VaspCalc = CalculationFactory('cusp.vasp')
    # setup calculation inputs
    builder = VaspCalc.get_builder()
    builder.code = code_cusp_vasp
    builder.incar = incar
    builder.kpoints = kpoints
    builder.poscar = poscar
    builder.potcar = VaspPotcarData.from_structure(poscar, 'pbe')
    builder.metadata.options.resources = {'num_machines': 1}
    builder.metadata.dry_run = True
    # perform the dry run
    run(builder)
    # assert the written files / folders
    submit_test_path = pathlib.Path.cwd().absolute() / 'submit_test'
    for written_file in submit_test_path.rglob('*'):
        print(written_file)